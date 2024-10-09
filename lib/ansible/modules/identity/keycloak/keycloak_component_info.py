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
module: keycloak_component_info

short_description: Retrive component info in Keycloak.

version_added: "2.9"

description:
    - This module creates, removes or update Keycloak component.
    - It can be use to create a LDAP and AD user federation to a realm in the Keycloak server
options:
    realm:
        description:
            - The name of the realm in which is the component.
        required: true
        type: str
    name:
        description:
            - Name of the Component
        required: true
        type: str
    providerId:
        description:
            - ProviderId of the component
        choices: [
            "ldap",
            "allowed-client-templates",
            "trusted-hosts",
            "allowed-protocol-mappers",
            "max-clients",
            "scope",
            "consent-required",
            "rsa-generated",
            "rsa-enc-generated"
        ]
        required: true
        type: str
    providerType:
        description:
            - Provider type of component
        choices:
            - org.keycloak.storage.UserStorageProvider
            - org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy
            - org.keycloak.keys.KeyProvider
            - authenticatorConfig
            - requiredActions
        required: true
        type: str

    
extends_documentation_fragment:
    - keycloak

author:
    - Philippe Gauthier (@elfelip)
    - Andre Desrosiers (@desand01)
'''

EXAMPLES = '''
    - name: Retrive info for ldap component
      keycloak_component_info:
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
        realm: master
        name: ActiveDirectory
        providerId: ldap
        providerType: org.keycloak.storage.UserStorageProvider

    - name: Retrive info for ldap component
      keycloak_component_info:
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
        realm: master
        name: rsa-enc-generated
        providerId: rsa-enc-generated
        providerType: org.keycloak.keys.KeyProvider


'''

RETURN = '''
component:
  description: JSON representation for the component.
  returned: on success
  type: dict
subComponents:
  description: JSON representation of the sub components list.
  returned: on success
  type: list
changed:
  description: Always return False.
  returned: always
  type: bool
'''

from ansible.module_utils.identity.keycloak.keycloak import KeycloakAPI, \
    keycloak_argument_spec, get_token, KeycloakError
# import module snippets
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = keycloak_argument_spec()
    
    meta_args = dict(
        name=dict(type='str', required=True),
        realm=dict(type='str', required=True),
        providerId=dict(
            choices=[
                "ldap",
                "allowed-client-templates",
                "trusted-hosts",
                "allowed-protocol-mappers",
                "max-clients",
                "scope",
                "consent-required",
                "rsa-generated",
                "rsa-enc-generated"],
            required=True),
        providerType=dict(
            choices=[
                "org.keycloak.storage.UserStorageProvider",
                "org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy",
                "org.keycloak.keys.KeyProvider",
                "authenticatorConfig",
                "requiredActions"],
            required=True),
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = dict(changed=False, component={}, subComponents={})

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

    # Create a representation from module parameters
    newComponent = {}
    newComponent["name"] = module.params.get('name')
    newComponent["providerId"] = module.params.get('providerId')
    newComponent["providerType"] = module.params.get('providerType')
    objRealm = kc.search_realm(realm)
    if not objRealm:
        module.fail_json(msg="Failed to retrive realm '{realm}'".format(realm=realm))
    newComponent["parentId"] = objRealm['id']

    component = kc.get_component_by_name_provider_and_parent(
        name=newComponent["name"],
        provider_type=newComponent["providerType"],
        provider_id=newComponent["providerId"],
        parent_id=newComponent["parentId"],
        realm=realm)

    if component:
        subComponents = kc.get_all_sub_components(parent_id=component["id"], realm=realm)
        result['component'] = component
        result['subComponents'] = subComponents

    module.exit_json(**result)


if __name__ == '__main__':
    main()
