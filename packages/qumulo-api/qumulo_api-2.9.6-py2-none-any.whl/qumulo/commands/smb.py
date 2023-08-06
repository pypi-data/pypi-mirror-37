# Copyright (c) 2012 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

'''
Share commands
'''

import re
import sys

import qumulo.lib.opts
from qumulo.lib.util import bool_from_string, tabulate
import qumulo.rest.smb as smb

#     _    ____ _
#    / \  / ___| |
#   / _ \| |   | |
#  / ___ \ |___| |___
# /_/   \_\____|_____|_             _       _   _
# |  \/  | __ _ _ __ (_)_ __  _   _| | __ _| |_(_) ___  _ __
# | |\/| |/ _` | '_ \| | '_ \| | | | |/ _` | __| |/ _ \| '_ \
# | |  | | (_| | | | | | |_) | |_| | | (_| | |_| | (_) | | | |
# |_|  |_|\__,_|_| |_|_| .__/ \__,_|_|\__,_|\__|_|\___/|_| |_|
#                      |_|
# FIGLET: ACL Manipulation

NO_ACCESS = "NONE"
READ_ACCESS = "READ"
WRITE_ACCESS = "WRITE"
READ_WRITE_ACCESS = "READ|WRITE"
CHANGE_PERMISSIONS_ACCESS = "CHANGE_PERMISSIONS"
ALL_ACCESS = "ALL"
ALL_RIGHTS = (
    NO_ACCESS,
    READ_ACCESS,
    WRITE_ACCESS,
    CHANGE_PERMISSIONS_ACCESS,
    ALL_ACCESS
)

ALLOWED_TYPE = "ALLOWED"
DENIED_TYPE = "DENIED"

LOCAL_DOMAIN = "LOCAL"
WORLD_DOMAIN = "WORLD"
POSIX_USER_DOMAIN = "POSIX_USER"
POSIX_GROUP_DOMAIN = "POSIX_GROUP"
AD_DOMAIN = "ACTIVE_DIRECTORY"

EVERYONE_NAME = 'Everyone'
EVERYONE_AUTH_ID = str(0x200000000) # WORLD_DOMAIN_ID << 32

GUEST_NAME = 'Guest'
GUEST_AUTH_ID = '501'

# A SID starts with S, followed by hyphen separated version, authority, and at
# least one sub-authority
SID_REGEXP = re.compile(r'S-[0-9]+-[0-9]+(?:-[0-9]+)+$')

def parse_trustee(trustee):
    '''
    Given a string representation of a trustee, (e.g "Everyone",
    "SID:S-1-2-3-4", "uid:1001"), produce a corresponding api_smb_share_trustee
    object.
    '''
    trustee = [i.strip() for i in trustee.split(":")]
    if len(trustee) > 2:
        raise ValueError("Trustee may not have more than one ':'")
    if len(trustee) == 1:
        trustee = trustee[0].capitalize()
        if trustee == EVERYONE_NAME:
            return {'auth_id': EVERYONE_AUTH_ID}
        elif trustee == GUEST_NAME:
            return {'auth_id': GUEST_AUTH_ID}
        elif SID_REGEXP.match(trustee):
            return {'sid': trustee}
        else:
            # (No need to complicate the error message by mentioning the
            # convenient sid recognition feature)
            raise ValueError(
                'Trustee name must be either "Everyone" or "Guest"')

    trustee_type, trustee_id = trustee
    trustee_type = trustee_type.lower()
    if trustee_type in ("uid", "gid"):
        return {trustee_type: int(trustee_id)}
    elif trustee_type == 'auth_id':
        # NB: validate int, and allow hex if desired:
        return {trustee_type: str(int(trustee_id, base=0))}
    elif trustee_type == 'sid':
        return {trustee_type: trustee_id}
    else:
        raise ValueError(
            'Trustee type must be "uid", "gid", "sid", or "auth_id"')

def pretty_trustee(api_trustee):
    '''
    The inverse of @ref parse_trustee, for an api_smb_share_trustee returned
    in an API response.
    '''
    # Pick an attribute.  Check in descending order of "user friendliness"
    if api_trustee.get('uid') is not None:
        return 'uid:{}'.format(api_trustee['uid'])
    if api_trustee.get('gid') is not None:
        return 'gid:{}'.format(api_trustee['gid'])

    # Resonse trustees always have domain, auth_id, and SID
    if api_trustee['auth_id'] == EVERYONE_AUTH_ID:
        return EVERYONE_NAME
    if api_trustee['auth_id'] == GUEST_AUTH_ID:
        return GUEST_NAME
    if api_trustee['domain'] == AD_DOMAIN:
        return api_trustee['sid']
    return 'auth_id:{}'.format(api_trustee['auth_id'])

def arg_trustee_equals_api_trustee(arg_trustee, api_trustee):
    '''
    Check whether the given @p arg_trustee string is equal to the given
    @p api_trustee api_smb_share_trustee.
    '''
    # When names are supported, may want to do a look-up to resolve
    # ambiguity.  Alternatively, could just require that the given name be
    # exactly the fully qualified name returned by the API.
    arg_trustee = parse_trustee(arg_trustee)

    # Note that there is an invariant that each api_trustee attribute uniquely
    # identifies a fully expanded api_trustee value, so given a partial trustee
    # (parsed from the command line) you only need one common attribute to
    # determine equality.
    for attr in ('auth_id', 'sid', 'uid', 'gid'):
        if (attr not in arg_trustee) or (attr not in api_trustee):
            continue
        return arg_trustee[attr] == api_trustee[attr]
    return False

def pretty_rights(rights):
    '''
    Print a user-friendly representation of the API rights enum,
    e.g. ["READ", "CHANGE_PERMISSIONS"] -> "Read, Change permissions"
    '''
    rights = [r.replace("_", " ") for r in rights] # for CHANGE_PERMISSIONS
    rights = [r.capitalize() for r in rights]
    return ", ".join(rights)

def parse_rights(rights):
    '''
    Transform a list of rights (validated by argparse) to an API ENUM.
    '''
    api_rights = [r.upper().replace(' ', '_') for r in rights]
    assert(all(r in ALL_RIGHTS for r in api_rights))
    return api_rights

def parse_type(ace_type):
    '''
    Check that a case-insensitive ace type is valid and return it in upper case.
    '''
    ace_type = ace_type.strip().upper()
    if ace_type not in {ALLOWED_TYPE, DENIED_TYPE}:
        raise ValueError('Type must be either "Allowed" or "Denied"')
    return ace_type

class SMBShareAcl(object):
    '''
    Provides methods for manipulating a share ACL.  May start with a current
    ACL (for modify commands), or from an empty ACL (for add or reset).
    '''

    def __init__(self, initial_acl=None):
        self.acl = initial_acl if initial_acl else []

    def grant(self, trustees, rights):
        '''
        Grants the given rights to the given trustees by appending
        ACEs to the ACL.  This would usually be used to build up a new ACL from
        nothing (but this usage is not strictly required).
        @p trustees A list of unparsed trustee strings
        @p rights A list of right options, e.g. ["Read", "Write"] ...
        '''
        self.acl = self.acl + [
            {
                'type': ALLOWED_TYPE,
                'trustee': parse_trustee(trustee),
                'rights': parse_rights(rights)
            }
            for trustee in trustees]

    def deny(self, trustees, rights):
        '''
        Denies the given rights to the given trustees by prepending ACEs
        to the ACL.  This would usually be used to build up a new ACL from
        nothing (but this usage is not strictly required).
        @p trustees A list of unparsed trustee strings
        @p rights A list of right options, e.g. ["Read", "Write"] ...
        '''
        self.acl = [
            {
                'type': DENIED_TYPE,
                'trustee': parse_trustee(trustee),
                'rights': parse_rights(rights)
            }
            for trustee in trustees] + self.acl

    def _find(self, position=None, trustee=None, ace_type=None, rights=None,
            allow_multiple=False):
        '''
        Find the indices of ACEs matching the given description.
        See @ref remove and @ref modify for argument descriptions.
        @return a list of the indices of ACEs matching the arguments.
        '''
        if position is not None:
            if not all((trustee is None, ace_type is None, rights is None)):
                raise ValueError(
                    "Cannot specify trustee by both position and attributes")
            # input is 1-indexed:
            if position < 1:
                raise ValueError("Position must be 1 or greater")
            if position > len(self.acl):
                raise ValueError("Position is past the end of the ACL")
            return [position - 1]

        if ace_type is not None:
            ace_type = parse_type(ace_type)

        if rights is not None:
            rights = parse_rights(rights)

        res = []
        for index, ace in enumerate(self.acl):
            if trustee is not None:
                if not arg_trustee_equals_api_trustee(trustee, ace['trustee']):
                    continue
            if ace_type is not None and ace_type != ace['type']:
                continue
            if rights is not None and rights != ace['rights']:
                continue
            res.append(index)

        if not res:
            raise ValueError("No matching entries found")
        if len(res) > 1 and not allow_multiple:
            raise ValueError(
                "Expected to find exactly 1 entry, but found {}".format(
                    len(res)))

        return res

    def remove(self, position=None,
            trustee=None, ace_type=None, rights=None, allow_multiple=False):
        '''
        Remove ACEs from the ACL, either by position, or by attribute.
        @p position Remove the ACE at the given 1-indexed position.  Mutually
            exclusive with all other arguments.
        @p trustee Remove ACE(s) with this trustee
        @p ace_type Remove ACE(s) with this ace_type (e.g. ALLOWED_TYPE, ...)
        @p rights Remove ACE(s) with these rights (e.g. READ_ACCESS, ...)
        @p allow_multiple If multiple ACEs match the given attributes, remove
            all of them.
        '''
        indices = self._find(
            position, trustee, ace_type, rights, allow_multiple)

        # Remove in reverse-order, so indices are stable
        indices.reverse()
        for i in indices:
            del self.acl[i]

    def modify(self, position=None,
        old_trustee=None, old_type=None, old_rights=None,
        new_trustee=None, new_type=None, new_rights=None,
        allow_multiple=False):
        '''
        Modify a particular ACE in the ACL, either by position, or by matching
        attributes.
        @p position Modify the ACE at the given 1-indexed position.  Mutually
            exclusive with the old_<attr> arguments.
        @p old_trustee, old_type, old_rights Modify the ACE with these
            attributes.  Exactly one ACE must match the given attributes.
        @p new_trustee, new_type, new_rights If present, specify a new value
            for the given attribute.
        @p allow_multiple If multiple ACEs match the given attributes, modify
            all of them.
        '''
        indices = self._find(
            position, old_trustee, old_type, old_rights, allow_multiple)

        if new_trustee is not None:
            new_trustee = parse_trustee(new_trustee)
        if new_type is not None:
            new_type = parse_type(new_type)
        if new_rights is not None:
            new_rights = parse_rights(new_rights)

        for i in indices:
            if new_trustee is not None:
                self.acl[i]['trustee'] = new_trustee
            if new_type is not None:
                self.acl[i]['type'] = new_type
            if new_rights is not None:
                self.acl[i]['rights'] = new_rights

    def pretty_str(self):
        '''
        @return A nice tabular representation of the ACL.
        '''
        headers = ["ID", "Trustee", "Type", "Rights"]
        table = []
        for index, ace in enumerate(self.acl, start=1):
            table.append([
                index,
                pretty_trustee(ace['trustee']),
                ace['type'].capitalize(),
                pretty_rights(ace['rights'])
            ])
        return tabulate(table, headers=headers)

def pretty_share_list(shares):
    headers = ["ID", "Name", "Path", "Description"]
    rows = [[row["id"], row["share_name"], row["fs_path"], row["description"]]
            for row in shares]
    return tabulate(rows, headers)

#  _     _     _     ____  _
# | |   (_)___| |_  / ___|| |__   __ _ _ __ ___  ___
# | |   | / __| __| \___ \| '_ \ / _` | '__/ _ \/ __|
# | |___| \__ \ |_   ___) | | | | (_| | | |  __/\__ \
# |_____|_|___/\__| |____/|_| |_|\__,_|_|  \___||___/
# FIGLET: List Shares

class SMBListSharesCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_list_shares"
    DESCRIPTION = "List all SMB shares"

    @staticmethod
    def options(parser):
        parser.add_argument("--json", action="store_true",
            help="Print JSON representation of shares.")

    @staticmethod
    def main(conninfo, credentials, args):
        res = smb.smb_list_shares(conninfo, credentials)
        if args.json:
            print res
        else:
            print pretty_share_list(res.data)

def _print_share(response, json, outfile):
    if json:
        outfile.write("{}\n".format(response))
    else:
        body, _etag = response
        outfile.write(
            "ID: {id}\n"
            "Name: {share_name}\n"
            "Path: {fs_path}\n"
            "Description: {description}\n"
            "Access Based Enumeration: "
                "{access_based_enumeration_enabled}\n"
            "Default File Create Mode: {default_file_create_mode}\n"
            "Default Directory Create Mode: "
                "{default_directory_create_mode}\n"
            .format(**body))
        outfile.write("\n")
        outfile.write("Permissions:\n{}\n".format(
            SMBShareAcl(body['permissions']).pretty_str()))

class SMBListShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_list_share"
    DESCRIPTION = "List a share"

    @staticmethod
    def options(parser):
        share = parser.add_mutually_exclusive_group(required=True)
        share.add_argument("--id", type=int, default=None,
            help="ID of share to list")

        parser.add_argument("--json", action='store_true', default=False,
            help="Print the raw JSON response.")

    @staticmethod
    def main(conninfo, credentials, args):
        _print_share(
            smb.smb_list_share(conninfo, credentials, args.id),
            args.json, sys.stdout)

#     _       _     _   ____  _
#    / \   __| | __| | / ___|| |__   __ _ _ __ ___
#   / _ \ / _` |/ _` | \___ \| '_ \ / _` | '__/ _ \
#  / ___ \ (_| | (_| |  ___) | | | | (_| | | |  __/
# /_/   \_\__,_|\__,_| |____/|_| |_|\__,_|_|  \___|
# FIGLET: Add Share

class SMBAddShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_add_share"
    DESCRIPTION = "Add a new SMB share"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", type=str, default=None, required=True,
            help="Name of share")
        parser.add_argument("--fs-path", type=str, default=None, required=True,
            help="File system path")
        parser.add_argument("--description", type=str, default='',
            help="Description of this share")
        parser.add_argument("--access-based-enumeration-enabled",
            type=bool, default=False,
            help="Enable Access-based Enumeration on this share")
        parser.add_argument("--create-fs-path", action="store_true",
            help="Creates the specified file system path if it does not exist")
        parser.add_argument("--default-file-create-mode",
            type=str, default=None,
            help="Default POSIX file create mode bits on this SMB share \
                (octal, 0644 will be used if not provided)")
        parser.add_argument("--default-directory-create-mode",
            type=str, default=None,
            help="Default POSIX directory create mode bits on this SMB share \
                (octal, 0755 will be used if not provided)")
        parser.add_argument("--json", action='store_true', default=False,
            help="Print the raw JSON response.")

        # Permissions options:
        parser.add_argument("--read-only", action='store_true', default=False,
            help="Make the share readable by everyone except guest.")
        parser.add_argument("--all-access", action='store_true', default=False,
            help="Make the share fully accessible to everyone except guest.")
        parser.add_argument("--grant-read-access", type=str, nargs='+',
            metavar='TRUSTEE',
            help="Grant read access to these trustees.  e.g. Everyone, "
                 "uid:1000, gid:1001, sid:S-1-5-2-3-4, or auth_id:500")
        parser.add_argument("--grant-read-write-access", type=str, nargs='+',
            metavar="TRUSTEE",
            help="Grant read-write access to these trustees.")
        parser.add_argument("--grant-all-access", type=str, nargs='+',
            metavar="TRUSTEE",
            help="Grant all access to these trustees.")
        parser.add_argument("--deny-access", type=str, nargs='+',
            metavar="TRUSTEE",
            help="Deny all access to these trustees.")

    @staticmethod
    def main(conninfo, credentials, args, outfile=sys.stdout, smb_mod=smb):
        acl = _create_new_acl(args)

        result = smb_mod.smb_add_share(conninfo, credentials,
            args.name,
            args.fs_path,
            args.description,
            permissions=acl,
            allow_fs_path_create=args.create_fs_path,
            access_based_enumeration_enabled=
                args.access_based_enumeration_enabled,
            default_file_create_mode=
                args.default_file_create_mode,
            default_directory_create_mode=
                args.default_directory_create_mode)

        _print_share(result, args.json, outfile)

#  ____       _      _         ____  _
# |  _ \  ___| | ___| |_ ___  / ___|| |__   __ _ _ __ ___
# | | | |/ _ \ |/ _ \ __/ _ \ \___ \| '_ \ / _` | '__/ _ \
# | |_| |  __/ |  __/ ||  __/  ___) | | | | (_| | | |  __/
# |____/ \___|_|\___|\__\___| |____/|_| |_|\__,_|_|  \___|
# FIGLET: Delete Share

class SMBDeleteShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_delete_share"
    DESCRIPTION = "Delete a share"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="ID of share to delete")

    @staticmethod
    def main(conninfo, credentials, args):
        smb.smb_delete_share(conninfo, credentials, args.id)
        print "Share has been deleted."

#  __  __           _ _  __         ____  _
# |  \/  | ___   __| (_)/ _|_   _  / ___|| |__   __ _ _ __ ___
# | |\/| |/ _ \ / _` | | |_| | | | \___ \| '_ \ / _` | '__/ _ \
# | |  | | (_) | (_| | |  _| |_| |  ___) | | | | (_| | | |  __/
# |_|  |_|\___/ \__,_|_|_|  \__, | |____/|_| |_|\__,_|_|  \___|
#                           |___/
# FIGLET: Modify Share

class SMBModShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_mod_share"
    DESCRIPTION = "Modify a share"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="ID of share to modify")
        parser.add_argument("--name", default=None,
            help="Change SMB share name")
        parser.add_argument("--fs-path", type=str, default=None,
            help="Change file system path")
        parser.add_argument("--description", type=str, default=None,
            help="Change description of this share")
        parser.add_argument("--access-based-enumeration-enabled",
            type=str, default=None,
            help="Change if Access-based Enumeration is enabled on this share")
        parser.add_argument("--create-fs-path", action="store_true",
            help="Creates the specified file system path if it does not exist")
        parser.add_argument("--default-file-create-mode",
            type=str, default=None,
            help="Change default POSIX file create mode bits (octal) on this \
                SMB share")
        parser.add_argument("--default-directory-create-mode",
            type=str, default=None,
            help="Change default POSIX directory create mode bits (octal) on \
                this SMB share")

    @staticmethod
    def main(conninfo, credentials, args):
        share_info = {}
        share_info, share_info['if_match'] = \
            smb.smb_list_share(conninfo, credentials, args.id)

        # XXX US22294 should use PATCH
        share_info['id_'] = share_info['id']
        share_info['allow_fs_path_create'] = args.create_fs_path
        del share_info['id']
        if args.name is not None:
            share_info['share_name'] = args.name
        if args.fs_path is not None:
            share_info['fs_path'] = args.fs_path
        if args.description is not None:
            share_info['description'] = args.description
        if args.access_based_enumeration_enabled is not None:
            share_info['access_based_enumeration_enabled'] = bool_from_string(
                args.access_based_enumeration_enabled)
        if args.default_file_create_mode is not None:
            share_info['default_file_create_mode'] = \
                args.default_file_create_mode
        if args.default_directory_create_mode is not None:
            share_info['default_directory_create_mode'] = \
                args.default_directory_create_mode

        print smb.smb_set_share(conninfo, credentials,
            **share_info)

#  __  __           _ _  __
# |  \/  | ___   __| (_)/ _|_   _
# | |\/| |/ _ \ / _` | | |_| | | |
# | |  | | (_) | (_| | |  _| |_| |
# |_|  |_|\___/ \__,_|_|_|  \__, |
#  ___                      |___/     _
# |  _ \ ___ _ __ _ __ ___ (_)___ ___(_) ___  _ __  ___
# | |_) / _ \ '__| '_ ` _ \| / __/ __| |/ _ \| '_ \/ __|
# |  __/  __/ |  | | | | | | \__ \__ \ | (_) | | | \__ \
# |_|   \___|_|  |_| |_| |_|_|___/___/_|\___/|_| |_|___/
# FIGLET: Modify Permissions

TYPE_CHOICES = [t.capitalize() for t in [ALLOWED_TYPE, DENIED_TYPE]]
RIGHT_CHOICES = [t.replace('_', ' ').capitalize() for t in ALL_RIGHTS]

def _put_new_acl(smb_mod, conninfo, creds, share, new_acl, etag, print_json):
    # XXX US22294: use PATCH instead
    result = smb_mod.smb_set_share(conninfo, creds,
        share['id'],
        share['share_name'],
        share['fs_path'],
        share['description'],
        new_acl,
        allow_fs_path_create = False, # should already exist
        access_based_enumeration_enabled =
            share['access_based_enumeration_enabled'],
        default_file_create_mode = share['default_file_create_mode'],
        default_directory_create_mode = share['default_directory_create_mode'],
        if_match=etag)
    if print_json:
        return str(result)
    else:
        body, etag = result
        return 'New permissions:\n{}'.format(
            SMBShareAcl(body['permissions']).pretty_str())

def _get_share(smb_mod, conninfo, creds, _id):
    return smb_mod.smb_list_share(conninfo, creds, _id)

def do_add_entry(smb_mod, conninfo, creds, args):
    share, etag = _get_share(smb_mod, conninfo, creds, args.id)

    # Modify:
    acl = SMBShareAcl(share['permissions'])
    ace_type = parse_type(args.type)
    if ace_type == ALLOWED_TYPE:
        acl.grant([args.trustee], args.rights)
    else:
        assert ace_type == DENIED_TYPE
        acl.deny([args.trustee], args.rights)

    return _put_new_acl(
        smb_mod, conninfo, creds, share, acl.acl, etag, args.json)

def do_remove_entry(smb_mod, conninfo, creds, args):
    share, etag = _get_share(smb_mod, conninfo, creds, args.id)

    # Remove:
    acl = SMBShareAcl(share['permissions'])
    acl.remove(position=args.position,
        trustee=args.trustee,
        ace_type=args.type,
        rights=args.rights,
        allow_multiple=args.all_matching)

    if args.dry_run:
        return 'New permissions would be:\n{}'.format(acl.pretty_str())

    return _put_new_acl(
        smb_mod, conninfo, creds, share, acl.acl, etag, args.json)

def do_modify_entry(smb_mod, conninfo, creds, args):
    share, etag = _get_share(smb_mod, conninfo, creds, args.id)

    acl = SMBShareAcl(share['permissions'])
    acl.modify(args.position,
        args.old_trustee, args.old_type, args.old_rights,
        args.new_trustee, args.new_type, args.new_rights,
        args.all_matching)

    if args.dry_run:
        return 'New permissions would be:\n{}'.format(acl.pretty_str())

    return _put_new_acl(
        smb_mod, conninfo, creds, share, acl.acl, etag, args.json)

def _create_new_acl(args):
    if args.read_only and any([args.grant_read_access, args.all_access,
            args.grant_read_write_access, args.grant_all_access]):
        raise ValueError("Cannot specify --read-only and grant other access.")

    acl = SMBShareAcl()

    # Note that order shouldn't matter, the SMBShareAcl should always put
    # these ACEs at the beginning, so they will override any grants
    if args.deny_access:
        acl.deny(args.deny_access, [ALL_ACCESS])

    if args.read_only:
        acl.grant([EVERYONE_NAME], [READ_ACCESS])
    if args.all_access:
        acl.grant([EVERYONE_NAME], [ALL_ACCESS])
    if args.grant_read_access:
        acl.grant(args.grant_read_access, [READ_ACCESS])
    if args.grant_read_write_access:
        acl.grant(args.grant_read_write_access, [READ_ACCESS, WRITE_ACCESS])
    if args.grant_all_access:
        acl.grant(args.grant_all_access, [ALL_ACCESS])

    return acl.acl

def do_replace(smb_mod, conninfo, creds, args):
    share, etag = _get_share(smb_mod, conninfo, creds, args.id)
    acl = _create_new_acl(args)
    return _put_new_acl(
        smb_mod, conninfo, creds, share, acl, etag, args.json)

# This is separate from smb_mode_share because argparse doesn't allow
# sub-commands to be optional.
class SMBModShareAclCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_mod_share_permissions"
    DESCRIPTION = "Modify a share's permissions"

    @staticmethod
    def options(parser):
        share = parser.add_mutually_exclusive_group(required=True)
        share.add_argument("--id", type=int, default=None,
            help="ID of share to modify")

        parser.add_argument("--json", action='store_true', default=False,
            help="Print the raw JSON response.")

        subparsers = parser.add_subparsers()

        add_entry = subparsers.add_parser("add_entry",
            help="Add an entry to the share's permissions.")
        add_entry.set_defaults(function=do_add_entry)
        add_entry.add_argument("-t", "--trustee", type=str, required=True,
            help="The trustee to add.  e.g. Everyone, uid:1000, gid:1001, "
                 "sid:S-1-5-2-3-4, or auth_id:500")
        add_entry.add_argument("-y", "--type", type=str, required=True,
            choices=TYPE_CHOICES,
            help="Whether the trustee should be allowed or denied the "
                "given rights")
        add_entry.add_argument("-r", "--rights", type=str, nargs="+",
            required=True, metavar='RIGHT',
            choices=RIGHT_CHOICES,
            help="The rights that should be allowed or denied.  Choices: "
                 + (", ".join(RIGHT_CHOICES)))

        remove_entry = subparsers.add_parser("remove_entry",
            help="Remove an entry from the share's permissions")
        remove_entry.set_defaults(function=do_remove_entry)
        remove_entry.add_argument("-p", "--position", type=int,
            help="The position of the entry to remove.")
        remove_entry.add_argument("-t", "--trustee", type=str,
            help="Remove an entry with this trustee.  e.g. Everyone, "
                 "uid:1000, gid:1001, sid:S-1-5-2-3-4, or auth_id:500")
        remove_entry.add_argument("-y", "--type", type=str,
            choices=TYPE_CHOICES, help="Remove an entry of this type")
        remove_entry.add_argument("-r", "--rights", type=str, nargs="+",
             metavar='RIGHT',
            choices=RIGHT_CHOICES,
            help="Remove an entry with these rights.  Choices: "
                 + (", ".join(RIGHT_CHOICES)))
        remove_entry.add_argument("-a", "--all-matching", action='store_true',
            default=False, help="If multiple entries match the "
                "arguments, remove all of them")
        remove_entry.add_argument("-d", "--dry-run", action='store_true',
            default=False,
            help="Do nothing; display what the result of the change would be.")

        modify_entry = subparsers.add_parser("modify_entry",
            help="Modify an existing permission entry in place")
        modify_entry.set_defaults(function=do_modify_entry)
        modify_entry.add_argument("-p", "--position", type=int,
            help="The position of the entry to modify.")
        modify_entry.add_argument("--old-trustee", type=str,
            help="Modify an entry with this trustee.  e.g. Everyone, "
                 "uid:1000, gid:1001, sid:S-1-5-2-3-4, or auth_id:500")
        modify_entry.add_argument("--old-type", type=str,
            choices=TYPE_CHOICES, help="Modify an entry of this type")
        modify_entry.add_argument("--old-rights", type=str, nargs="+",
             metavar='RIGHT',
            choices=RIGHT_CHOICES,
            help="Modify an entry with these rights.  Choices: "
                 + (", ".join(RIGHT_CHOICES)))
        modify_entry.add_argument("--new-trustee", type=str,
            help="Set the entry to have this trustee.  e.g. Everyone, "
                 "uid:1000, gid:1001, sid:S-1-5-2-3-4, or auth_id:500")
        modify_entry.add_argument("--new-type", type=str,
            choices=TYPE_CHOICES, help="Set the type of the entry.")
        modify_entry.add_argument("--new-rights", type=str, nargs="+",
             metavar='RIGHT',
            choices=RIGHT_CHOICES,
            help="Set the rights of the entry.  Choices: "
                 + (", ".join(RIGHT_CHOICES)))
        modify_entry.add_argument("-a", "--all-matching", action='store_true',
            default=False, help="If multiple entries match the arguments, "
                "modify all of them")
        modify_entry.add_argument(
            "-d", "--dry-run", action='store_true', default=False,
            help="Do nothing; display what the result of the change would be.")

        replace = subparsers.add_parser("replace",
            help="Replace any existing share permissions with new permissions. "
                 "If no new permissions are specified, all access will be "
                 "denied.")
        replace.add_argument("--read-only", action='store_true', default=False,
            help="Grant everyone except guest read-only access.")
        replace.add_argument("--all-access", action='store_true', default=False,
            help="Grant everyone except guest full access.")
        replace.add_argument("--grant-read-access", type=str, nargs='+',
            metavar='TRUSTEE',
            help="Grant read access to these trustees.  e.g. Everyone, "
                 "uid:1000, gid:1001, sid:S-1-5-2-3-4, or auth_id:500")
        replace.add_argument("--grant-read-write-access", type=str, nargs='+',
            metavar="TRUSTEE",
            help="Grant read-write access to these trustees.")
        replace.add_argument("--grant-all-access", type=str, nargs='+',
            metavar="TRUSTEE",
            help="Grant all access to these trustees.")
        replace.add_argument("--deny-access", type=str, nargs='+',
            metavar="TRUSTEE",
            help="Deny all access to these trustees.")
        replace.set_defaults(function=do_replace)

    @staticmethod
    def main(conninfo, credentials, args, outfile=sys.stdout, smb_mod=smb):
        outfile.write('{}\n'.format(
            args.function(smb_mod, conninfo, credentials, args)))
