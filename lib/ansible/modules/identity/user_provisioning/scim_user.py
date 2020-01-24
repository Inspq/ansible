#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, INSPQ <philippe.gauthier@inspq.qc.ca>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: scim_user
short_description: User provisiono9ng module for SCIM compliant user repository
description:
    - This module can synchronize user to SCIM V2 compliant repository.
    - An access token must be supplied when scim server is secured
version_added: "2.9"
options:
    scim_server_url:
        description:
            - URL of the SCIM Server
        required: true
        type: str
    access_token:
        description:
            - Oauth2/OpenID Connect access token for serveur Authentication
        required: false
        type: str
    userName:
        description:
            - userName for whom to do provisioning
        required: true
        type: str
    name:
        description:
            - Name of the user
        required: false
        type: dict
        suboptions:
            givenName:
                description:
                    - First name of the user.
                type: str
            familyName:
                description:
                    - Last name of the user
                type: str
            middleName:
                description:
                    - Middle name of the user
                type: str
    displayName:
        description:
            - Display Name
        required: false
        type: str
    roles:
        description:
        - List of roles for the user.
        required: false
        type: list
        suboptions:
            display:
                description:
                - Name of the role
                type: str
                required: true
            type:
                description:
                - Type of role
                type: str
                required: false
            primary:
                description:
                - Is this role primary
                type: bool
                required: false
    state:
        description:
            - Control if the user must exist or not
        choices: [ "present", "absent" ]
        default: present
        required: false
        type: str
    force:
        type: bool
        default: false
        description:
            - If true, allows to remove the user and recreate it.
        required: false


author:
    - Philippe Gauthier (@elfelip)
'''

EXAMPLES = '''
    - name: Ensure a user exist.
      scim_user:
        scim_server_url: http://scim.server.url/scim/v2
        access_token: eyasdijhoijf0983jf98034j890g
        name:
          userName: toto12
          givenName: Totally
          familyName: Totest
        displayName: "user 12"
        roles:
        - display: FA-SAISIE
          type: test
          primary: True
        state: present

    - name: Re-create the user
      scim_user:
        scim_server_url: http://scim.server.url/scim/v2
        access_token: eyasdijhoijf0983jf98034j890g
        name:
          userName: toto12
          givenName: Totally
          familyName: Totest
        displayName: "user 12"
        state: present
        force: yes

    - name: Remove the user
      scim_user:
        scim_server_url: http://scim.server.url/scim/v2
        access_token: eyasdijhoijf0983jf98034j890g
        userName: toto12
        state: absent
'''

RETURN = '''
user:
  description: SCIM representation for the user
  returned: on success
  type: dict
msg:
  description: Error message if it is the case
  returned: on error
  type: str
changed:
  description: Return True if the operation changed the user, false otherwise.
  returned: always
  type: bool
'''
from ansible.module_utils.identity.user_provisioning.scim import SCIMClient, User
from ansible.module_utils.identity.keycloak.keycloak import isDictEquals
from ansible.module_utils.basic import AnsibleModule
import json


def main():
    """
    Module execution
    :returm:
    """
    name_spec = dict(
        givenName=dict(type='str'),
        familyName=dict(type='str'),
        middleName=dict(type='str')
    )
    role_spec = dict(
        display=dict(type='str', required=True),
        type=dict(type='str'),
        primary=dict(type='bool')
    )
    argument_spec = dict(
        scim_server_url=dict(type='str', required=True),
        userName=dict(type='str', required=True),
        name=dict(type='dict', options=name_spec),
        displayName=dict(type='str'),
        roles=dict(type='list', options=role_spec),
        access_token=dict(type='str'),
        state=dict(choices=["absent", "present"], default='present'),
        force=dict(type='bool', default=False),
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    result = dict(changed=False, msg='', flow={})
    # Initialize SCIM client API
    scimClient = SCIMClient(module, base_url=module.params.get("scim_server_url"), access_token=module.params.get("access_token"))

    newUser = {
        "userName": module.params.get("userName"),
        "id": module.params.get("userName"),
        "name": module.params.get("name"),
        "roles": module.params.get("roles"),
        "displayName": module.params.get("displayName")
    }
    newScimUser = User(newUser)
    # Search the user
    existingScimUser = scimClient.searchUserByUserName(userName=module.params.get("userName"))

    if existingScimUser is None:
        if module.params.get("state") == "present":
            createdSCIMUser = scimClient.createUser(newScimUser)
            result['changed'] = True
            result['user'] = json.loads(createdSCIMUser.to_json())
        else:
            result['changed'] = False
            result['msg'] = 'The user to be deleted does not exist'
    else:
        if module.params.get("state") == "absent":
            response = scimClient.deleteUser(existingScimUser)
            result['changed'] = True
            result['msg'] = 'User %s deleted: %s' % (existingScimUser.userName, str(response.code))
        else:
            # Check if user need to be changed
            if isDictEquals(json.loads(newScimUser.to_json()), json.loads(existingScimUser.to_json()), exclude=[]):  # User does not need to be changed
                result['changed'] = False
                result['user'] = json.loads(existingScimUser.to_json())
            else:
                mergedScimUser = existingScimUser.update(newScimUser)
                updatedSCIMUser = scimClient.updateUser(mergedScimUser)
                result['changed'] = True
                result['user'] = json.loads(updatedSCIMUser.to_json())

    module.exit_json(**result)


if __name__ == '__main__':
    main()
