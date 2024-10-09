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
module: keycloak_keyprovider

short_description: Configure LDAP user storage component in Keycloak.

version_added: "v2.10.16-keycloak-sx5-11"

description:
    - This module creates, removes or update Keycloak component.
    - It can be use to create a KeyProvider to a realm in the Keycloak server
options:
    realm:
        description:
            - The name of the realm in which is the component.
        required: true
        type: str
    id:
        description:
            - ID of the component when it have already been created and it is known.
        required: false
        type: str
    name:
        description:
        - Name of the Component
        required: true
        type: str
    providerId:
        description:
            - ProviderId of the component
        choices:
        - rsa-generated
        - rsa-enc-generated
        required: true
        type: str
    providerType:
        description:
            - Provider type of component
        choices:
        - org.keycloak.keys.KeyProvider
        default: org.keycloak.keys.KeyProvider
        type: str
    parentId:
        description:
            - Parent ID of the component. Use the realm name for top level component.
        required: false
        type: str
    config:
        description:
            - Configuration of the component to create, update or delete.
        required: false
        type: dict
        suboptions:
            keySize:
                description:
                    -
                type: list
                default: 
                - '2048'
            active:
                description:
                    -
                type: list
                default:
                - 'True'
            priority:
                description:
                    -
                type: list
            enabled:
                description:
                    - 
                type: list
                default:
                - 'True'
            algorithm:
                description:
                    - 
                type: list
                choices:
                - RSA1_5
                - RSA-OAEP
                - RSA-OAEP-256
    state:
        description:
            - Control if the component must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
        type: str
    force:
        description:
            - If true, remove component and recreate it.
        type: bool
        default: false
extends_documentation_fragment:
    - keycloak

author:
    - Andre Desrosiers
    - Philippe Gauthier (@elfelip)
'''

EXAMPLES = '''
    - name: Create a rsa-enc-generated provider in "test-realm"
      keycloak_keyprovider:
        auth_client_id: admin-cli
        auth_keycloak_url: http://localhost:8080/auth
        auth_realm: master
        auth_username: admin
        auth_password: password
        name: rsa-enc-generated
        parentId: test-realm
        providerId: rsa-enc-generated
        providerType: org.keycloak.keys.KeyProvider
        config:
            active:
            - 'true'
            algorithm:
            - RSA-OAEP-256
            enabled:
            - 'true'
            keySize:
            - '2048'
            priority:
            - '100'
        realm: test-realm
        state: present

    - name: Re-create a rsa-enc-generated provider in "test-realm"
      keycloak_keyprovider:
        auth_client_id: admin-cli
        auth_keycloak_url: http://localhost:8080/auth
        auth_realm: master
        auth_username: admin
        auth_password: password
        name: rsa-enc-generated
        parentId: test-realm
        providerId: rsa-enc-generated
        providerType: org.keycloak.keys.KeyProvider
        config:
            active:
            - 'true'
            algorithm:
            - RSA-OAEP-256
            enabled:
            - 'true'
            keySize:
            - '2048'
            priority:
            - '100'
        realm: test-realm
        state: present
        force: yes

    - name: Remove rsa-enc-generated Provider.
      keycloak_keyprovider:
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
        realm: master
        name: rsa-enc-generated
        providerId: rsa-enc-generated
        providerType: org.keycloak.keys.KeyProvider
        state: absent
'''

RETURN = '''
component:
  description: JSON representation for the component.
  returned: on success
  type: dict
msg:
  description: Error message if it is the case
  returned: on error
  type: str
changed:
  description: Return True if the operation changed the component on the keycloak server, false otherwise.
  returned: always
  type: bool
'''

from ansible.module_utils.identity.keycloak.keycloak import KeycloakAPI, camel, \
    keycloak_argument_spec, get_token, KeycloakError, isDictEquals, remove_arguments_with_value_none
# import module snippets
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = keycloak_argument_spec()
    config_spec = dict(
        keySize=dict(type='list', options='int', default=2048),
        active=dict(type='list', options='bool', default=True),
        priority=dict(type='list', options='int'),
        enabled=dict(type='list', options='bool', default=True),
        algorithm=dict(type='list', 
                       choices=[
                           'RSA1_5', 
                           'RSA-OAEP', 
                           'RSA-OAEP-256'
                        ], default=['RSA-OAEP']),
    )

    meta_args = dict(
        id=dict(type='str'),
        name=dict(type='str', required=True),
        realm=dict(type='str', required=True),
        providerId=dict(
            choices=[
                "rsa-enc-generated",
                "rsa-generated"],
            required=True),
        providerType=dict(
            choices=["org.keycloak.keys.KeyProvider"],
            default="org.keycloak.keys.KeyProvider"),
        parentId=dict(type='str'),
        config=dict(type='dict', options=config_spec),
        state=dict(choices=["absent", "present"], default='present'),
        force=dict(type='bool', default=False),
    )
    argument_spec.update(meta_args)

    required_if=[['state', 'present', ['config']]]
    module = AnsibleModule(argument_spec=argument_spec,
                           required_if=required_if,
                           supports_check_mode=True)

    result = dict(changed=False, msg='', diff={}, component='')

    # Obtain access token, initialize API
    try:
        connection_header = get_token(
            base_url=module.params.get('auth_keycloak_url'),
            validate_certs=module.params.get('validate_certs'),
            auth_realm=module.params.get('auth_realm'),
            client_id=module.params.get('auth_client_id'),
            auth_username=module.params.get('auth_username'),
            auth_password=module.params.get('auth_password'),
            client_secret=module.params.get('auth_client_secret'),
        )
    except KeycloakError as e:
        module.fail_json(msg=str(e))

    kc = KeycloakAPI(module, connection_header)

    realm = module.params.get('realm')
    state = module.params.get('state')
    force = module.params.get('force')

    # Create a representation from module parameters
    newComponent = {}
    newComponent["id"] = module.params.get('id')
    newComponent["name"] = module.params.get('name')
    newComponent["providerId"] = module.params.get('providerId')
    newComponent["providerType"] = module.params.get('providerType')
    objRealm = kc.search_realm(realm)
    if not objRealm:
        module.fail_json(msg="Failed to retrive realm '{realm}'".format(realm=realm))
    newComponent["parentId"] = objRealm['id']
    newComponent["config"] = remove_arguments_with_value_none(
        module.params.get("config").copy() if module.params.get("config") else dict()
    )
    
    changed = False

    component = kc.get_component_by_name_provider_and_parent(
        name=newComponent["name"],
        provider_type=newComponent["providerType"],
        provider_id=newComponent["providerId"],
        parent_id=newComponent["parentId"],
        realm=realm)

    if component == {}:  # If component does not exist
        if (state == 'present'):  # If desired stat is present
            # Create the component and it's sub-components
            component = kc.create_component(
                newComponent=newComponent,
                newSubComponents=None,
                syncLdapMappers=None,
                realm=realm)

            changed = True
            result['component'] = component
            result['changed'] = changed
        elif state == 'absent':  # Id desired state is absent, return absent and do nothing.
            result['msg'] = newComponent["name"] + ' absent'
            result['component'] = newComponent
            result['changed'] = changed

    else:  # If component already exist
        if (state == 'present'):  # if desired state is present
            if force:  # If force option is true
                # Delete the existing component
                kc.delete_component(component_id=component["id"], realm=realm)
                changed = True
                # Re-create the component.
                component = kc.create_component(newComponent=newComponent,
                                                newSubComponents=None,
                                                syncLdapMappers=None,
                                                realm=realm)
            else:  # If force option is false
                # Copy existing id in new component
                newComponent['id'] = component['id']
                newComponent['parentId'] = component['parentId']
                excludes = []
                # Compare the new component with the existing
                #excludes.append("bindCredential")
                if not isDictEquals(newComponent, component, excludes):  # If the component need to be changed
                    # Update the component
                    component = kc.update_component(newComponent=newComponent, realm=realm)
                    changed = True

            result['component'] = component
            result['changed'] = changed

        elif state == 'absent':  # if desired state is absent
            # Delete the component
            kc.delete_component(component_id=component['id'], realm=realm)
            changed = True
            result['msg'] = newComponent["name"] + ' deleted'
            result['changed'] = changed

    module.exit_json(**result)


if __name__ == '__main__':
    main()
