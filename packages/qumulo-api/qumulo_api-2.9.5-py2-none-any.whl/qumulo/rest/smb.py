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
def smb_list_shares(conninfo, credentials):
    method = "GET"
    uri = "/v1/smb/shares/"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def smb_add_share(conninfo, credentials,
                          share_name, fs_path, description,
                          read_only=False, allow_guest_access=False,
                          allow_fs_path_create=False,
                          access_based_enumeration_enabled=False,
                          default_file_create_mode=None,
                          default_directory_create_mode=None):
    method = "POST"
    allow_fs_path_create_ = "true" if allow_fs_path_create else "false"
    uri = "/v1/smb/shares/?allow-fs-path-create=%s" % allow_fs_path_create_

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

    return request.rest_request(conninfo, credentials, method, uri,
        body=share_info)

@request.request
def smb_list_share(conninfo, credentials, id_):
    id_ = unicode(id_)

    method = "GET"
    uri = "/v1/smb/shares/%s" % id_

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def smb_modify_share(conninfo, credentials, id_, share_name,
        fs_path, description, read_only, allow_guest_access,
        allow_fs_path_create=False, if_match=None,
        access_based_enumeration_enabled=None,
        default_file_create_mode=None,
        default_directory_create_mode=None):
    id_ = unicode(id_)
    allow_fs_path_create_ = "true" if allow_fs_path_create else "false"

    if_match = if_match if if_match is None else unicode(if_match)

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
def smb_delete_share(conninfo, credentials, id_):
    id_ = unicode(id_)

    method = "DELETE"
    uri = "/v1/smb/shares/%s" % id_

    return request.rest_request(conninfo, credentials, method, uri)

class NFSRestriction(obj.Object):
    @classmethod
    def create_default(cls):
        return cls({'read_only': False, 'host_restrictions': [],
                    'user_mapping': 'NFS_MAP_NONE', 'map_to_user_id': '0'})
