#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017, Eike Frost <ei@kefro.st>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: keycloak_client_info

short_description: Allows administration of Keycloak clients via Keycloak API

version_added: "2.10.16"

description:
    - This module allows return client info with secret

options:
    realm:
        description:
            - The realm to fetch the client.
        type: str
        default: master
    client_id:
        description:
            - Client id of client to be return.
              Either this or I(id) is required. If you specify both, I(id) takes precedence.
              This is 'clientId' in the Keycloak REST API.
        aliases:
            - clientId
        type: str
    id:
        description:
            - Id of client to be return. This is usually an UUID. Either this or I(client_id)
              is required. If you specify both, this takes precedence.
        type: str
    

extends_documentation_fragment:
    - keycloak
author:
    - Andre
'''

EXAMPLES = '''
- name: Get fact Keycloak client
  local_action:
    module: keycloak_client_info
    auth_client_id: admin-cli
    auth_keycloak_url: https://auth.example.com/auth
    auth_realm: master
    auth_username: USERNAME
    auth_password: PASSWORD
    realm: myrealm
    client_id: test

'''

RETURN = '''
msg:
  description: Message as to what action was taken
  returned: always
  type: str
existing:
    description: client representation of existing client (sample is truncated)
    returned: always
    type: dict
    sample: {
        "adminUrl": "http://www.example.com/admin_url",
        "attributes": {
            "request.object.signature.alg": "RS256",
        }
    }
clientSecret:
    description: client Secret
    returned: always
    type: dict
    sample: {
        type: "secret",
        value: "691ccfeb-13f0-4bbf-91bb-a57b42f47e31"
    }
'''

from ansible.module_utils.identity.keycloak.keycloak import KeycloakAPI, camel, \
    keycloak_argument_spec, get_token, KeycloakError, isDictEquals
from ansible.module_utils.basic import AnsibleModule


def sanitize_cr(clientrep):
    """ Removes probably sensitive details from a client representation

    :param clientrep: the clientrep dict to be sanitized
    :return: sanitized clientrep dict
    """
    result = clientrep.copy()
    if 'secret' in result:
        result['secret'] = 'no_log'
    if 'attributes' in result:
        if 'saml.signing.private.key' in result['attributes']:
            result['attributes']['saml.signing.private.key'] = 'no_log'
    return result

def main():
    """
    Module execution

    :return:
    """
    argument_spec = keycloak_argument_spec()

    meta_args = dict(
        realm=dict(type='str', default='master'),
        id=dict(type='str'),
        client_id=dict(type='str', aliases=['clientId']),
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           required_one_of=([['client_id', 'id']]))

    result = dict(changed=False, existing={}, clientSecret='')

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
    cid = module.params.get('id')
    

    keycloak_argument_spec().keys()
    # See whether the client already exists in Keycloak
    if cid is None:
        before_client = kc.get_client_by_clientid(module.params.get('client_id'), realm=realm)
        if before_client is not None:
            cid = before_client['id']
    else:
        before_client = kc.get_client_by_id(cid, realm=realm)

    if before_client is None:
        before_client = dict()

    result['existing'] = sanitize_cr(before_client)

    if before_client == dict():
        #nothing to do
        None
    else:
        client_secret = kc.get_client_secret_by_id(cid, realm=realm)
        if client_secret is not None:
            result['clientSecret'] = client_secret

    module.exit_json(**result)


if __name__ == '__main__':
    main()
