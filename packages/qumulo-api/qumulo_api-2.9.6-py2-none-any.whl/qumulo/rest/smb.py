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

import qumulo.lib.request as request
import qumulo.lib.obj as obj

@request.request
def smb_list_shares_v1(conninfo, credentials):
    '''
    Deprecated.  List all shares, with read_only/allow_guest_access permissions
    flags displayed (even if permissions are more complex)
    '''
    method = "GET"
    uri = "/v1/smb/shares/"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def smb_list_share_v1(conninfo, credentials, id_):
    '''
    Deprecated.  Get a given share, with read_only/allow_guest_access
    permissions flags displayed (even if permissions are more complex)
    '''
    id_ = unicode(id_)

    method = "GET"
    uri = "/v1/smb/shares/%s" % id_

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def smb_list_shares(conninfo, credentials):
    return request.rest_request(conninfo, credentials, "GET", "/v2/smb/shares/")

@request.request
def smb_list_share(conninfo, credentials, id_):
    # XXX US22294: Support list by name
    id_ = unicode(id_)

    method = "GET"
    uri = "/v2/smb/shares/%s" % id_

    return request.rest_request(conninfo, credentials, method, uri)

# Permissions constants
NO_ACCESS = u'NONE'
READ_ACCESS = u'READ'
WRITE_ACCESS = u'WRITE'
CHANGE_PERMISSIONS_ACCESS = u'CHANGE_PERMISSIONS'
ALL_ACCESS = u'ALL'

ALLOWED_TYPE = u'ALLOWED'
DENIED_TYPE = u'DENIED'

# These identities always have well-known auth_ids:
EVERYONE_AUTH_ID = unicode(0x200000000)
GUEST_AUTH_ID = u'501'

@request.request
def smb_add_share(conninfo, credentials,
        share_name,
        fs_path,
        description,
        read_only=None,
        allow_guest_access=None,
        allow_fs_path_create=False,
        access_based_enumeration_enabled=False,
        default_file_create_mode=None,
        default_directory_create_mode=None,
        permissions=None):
    if permissions is None:
        # Use the old v1 API and its semantics (i.e. default full control but
        # deny guest)
        share_info = {
            'share_name':         unicode(share_name),
            'fs_path':            unicode(fs_path),
            'description':        unicode(description),
            'read_only':          bool(read_only),
            'allow_guest_access': bool(allow_guest_access),
            'access_based_enumeration_enabled': \
                bool(access_based_enumeration_enabled)
        }

        if default_file_create_mode is not None:
            share_info['default_file_create_mode'] = \
                unicode(default_file_create_mode)
        if default_directory_create_mode is not None:
            share_info['default_directory_create_mode'] = \
                unicode(default_directory_create_mode)

        uri = "/v1/smb/shares/?allow-fs-path-create={}".format(
            "true" if allow_fs_path_create else "false")
        return request.rest_request(conninfo, credentials, "POST", uri,
            body=share_info)
    else:
        # Use the new API.
        if read_only is not None:
            raise ValueError("read_only may not be specified with permissions")
        if allow_guest_access is not None:
            raise ValueError(
                "allow_guest_access may not be specified with permissions")

        share_info = {
            'share_name':  unicode(share_name),
            'fs_path':     unicode(fs_path),
            'description': unicode(description),
            'permissions': permissions,
        }
        if access_based_enumeration_enabled is not None:
            share_info['access_based_enumeration_enabled'] = bool(
                access_based_enumeration_enabled)
        if default_file_create_mode is not None:
            share_info['default_file_create_mode'] = unicode(
                default_file_create_mode)
        if default_directory_create_mode is not None:
            share_info['default_directory_create_mode'] = unicode(
                default_directory_create_mode)

        uri = "/v2/smb/shares/?allow-fs-path-create={}".format(
            "true" if allow_fs_path_create else "false")
        return request.rest_request(conninfo, credentials, "POST", uri,
            body=share_info)

@request.request
def smb_modify_share(conninfo, credentials, id_, share_name,
        fs_path, description, read_only, allow_guest_access,
        allow_fs_path_create=False, if_match=None,
        access_based_enumeration_enabled=None,
        default_file_create_mode=None,
        default_directory_create_mode=None):
    # XXX US22294: This should start using PATCH and all arguments should
    # become optional.
    # Also, need to support modify by name
    id_ = unicode(id_)
    allow_fs_path_create_ = "true" if allow_fs_path_create else "false"

    if_match = None if if_match is None else unicode(if_match)

    method = "PUT"
    uri = "/v1/smb/shares/%s?allow-fs-path-create=%s" % \
        (id_, allow_fs_path_create_)

    share_info = {
        'id': id_,
        'share_name':         unicode(share_name),
        'fs_path':            unicode(fs_path),
        'description':        unicode(description),
        'read_only':          bool(read_only),
        'allow_guest_access': bool(allow_guest_access)
    }

    # "ABE enabled" is an optional field. It may be absent if we use this client
    # code with the clusters running previous versions of qfsd.
    if access_based_enumeration_enabled is not None:
        share_info['access_based_enumeration_enabled'] = \
            bool(access_based_enumeration_enabled)

    if default_file_create_mode is not None:
        share_info['default_file_create_mode'] = \
            unicode(default_file_create_mode)
    if default_directory_create_mode is not None:
        share_info['default_directory_create_mode'] = \
            unicode(default_directory_create_mode)

    return request.rest_request(conninfo, credentials, method, uri,
        body=share_info, if_match=if_match)

@request.request
def smb_set_share(conninfo,
        credentials,
        id_,
        share_name,
        fs_path,
        description,
        permissions,
        allow_fs_path_create=False,
        access_based_enumeration_enabled=None,
        default_file_create_mode=None,
        default_directory_create_mode=None,
        if_match=None):
    '''
    Replaces all share attributes.  The result is a share identical to what
    would have been produced if the same arguments were given on creation.
    Note that this means that an unspecified optional argument will result in
    that attribute being reset to default, even if the share currently has a
    non-default value.
    '''
    id_ = unicode(id_)
    share_info = {
        'id': id_,
        'share_name':  unicode(share_name),
        'fs_path':     unicode(fs_path),
        'description': unicode(description),
        'permissions': permissions,
    }
    if access_based_enumeration_enabled is not None:
        share_info['access_based_enumeration_enabled'] = \
            bool(access_based_enumeration_enabled)
    if default_file_create_mode is not None:
        share_info['default_file_create_mode'] = \
            unicode(default_file_create_mode)
    if default_directory_create_mode is not None:
        share_info['default_directory_create_mode'] = \
            unicode(default_directory_create_mode)

    uri = "/v2/smb/shares/{}?allow-fs-path-create={}".format(
        id_, "true" if allow_fs_path_create else "false")
    if_match = None if if_match is None else unicode(if_match)
    return request.rest_request(conninfo, credentials, "PUT", uri,
        body=share_info, if_match=if_match)

@request.request
def smb_delete_share(conninfo, credentials, id_):
    # XXX US22294: Support delete by name
    id_ = unicode(id_)

    method = "DELETE"
    uri = "/v1/smb/shares/%s" % id_

    return request.rest_request(conninfo, credentials, method, uri)

class NFSRestriction(obj.Object):
    @classmethod
    def create_default(cls):
        return cls({'read_only': False, 'host_restrictions': [],
                    'user_mapping': 'NFS_MAP_NONE', 'map_to_user_id': '0'})
