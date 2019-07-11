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
module: sx5_habilitation
short_description: remove the accreditations that are expired
description:
    - This module remove, list and extend the accreditations that are expired.
version_added: "2.9"
options:
    realm:
        description:
            - The name of the realm in which is the role.
        required: true
        default: master
        type: str
    spConfigUrl:
        description:
            - sx5-config DB REST services URL.
        required: true
    spConfigClient_id:
        description:
            - Sx5-sp-Config Client ID.
        required: true
    spConfigClient_secret:
        description:
            - Sx5-sp-Config Client Secret.
        required: false
    operation:
        description:
            - operation on the expired accreditation.
        choices: [list, remove, extend]
        default: list
        type: str
    duration:
        description:
            - duration of extension of expired accreditation.
        choices: [list, remove, extend]
        default: list
        type: str
extends_documentation_fragment:
    - keycloak
notes:
    - module does not modify system in sx5_sp_config.
author:
    - INSPQ SX5 Team (@moi8407)
'''

EXAMPLES = '''
    - name: remove the accreditations that are expired.
      sx5_habilitation:
        auth_keycloak_url: http://localhost:8080/auth
        auth_username: admin
        auth_password: password
        realm: master
        spConfigUrl: http://localhost:8089/config
        spConfigClient_id: sx5spconfig
        spConfigClient_secret: client_string
        operation: remove

    - name: list the accreditations that are expired.
      sx5_habilitation:
        auth_keycloak_url: http://localhost:8080/auth
        auth_username: admin
        auth_password: password
        realm: master
        spConfigUrl: http://localhost:8089/config
        spConfigClient_id: sx5spconfig
        spConfigClient_secret: client_string
        operation: list

    - name: extend the accreditations that are expired.
      sx5_habilitation:
        auth_keycloak_url: http://localhost:8080/auth
        auth_username: admin
        auth_password: password
        realm: master
        spConfigUrl: http://localhost:8089/config
        spConfigClient_id: sx5spconfig
        spConfigClient_secret: client_string
        operation: extend
        duration: 24

'''

RETURN = '''
role:
  description: JSON representation for the role.
  returned: on success
  type: dict
composites:
  description: Composites JSON representation for the role.
  returned: on success
  type: list
msg:
  description: Error message if it is the case
  returned: on error
  type: str
changed:
  description: Return True if the operation changed the role on the keycloak server, false otherwise.
  returned: always
  type: bool
'''
from ansible.module_utils.keycloak import KeycloakAPI, keycloak_argument_spec, isDictEquals
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url
import datetime
import json

def main():
    argument_spec = keycloak_argument_spec()
    meta_args = dict(
        realm=dict(type='str', default='master'),
        spConfigUrl = dict(type='str', required=True),
        spConfigClient_id=dict(type='str', required=True),
        spConfigClient_secret=dict(type='str', required=False),
        operation=dict(choices=["list", "remove", "extend"], default='list'),
        duration=dict(type='int', default=0),
    )
    argument_spec.update(meta_args)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = dict(changed=False, msg={}, habilitation={})

    # Obtain access token, initialize API
    kc = KeycloakAPI(module)

    realm = module.params.get('realm')
    operation = module.params.get('operation')
    duration = module.params.get('duration')
    spConfigUrl = module.params.get('spConfigUrl')
    username = module.params.get('auth_username')
    password = module.params.get('auth_password')
    clientid = module.params.get('spConfigClient_id')
    if module.params.get('spConfigClient_secret') is not None:
        clientSecret = module.params.get('spConfigClient_secret')
    else:
        clientSecret = kc.get_client_secret_by_id(kc.get_client_id(clientid,realm),realm)
    changed = False
    accesToken = kc.get_grant_type_password_access_token(clientid, clientSecret, username, password, realm)
    headers = {'Authorization': 'Bearer ' + accesToken,'Content-Type': 'application/json'}
    
    # Search expired accreditation in sx5_sp_config.
    listeExpiredHabilitations = []
    deleteExpiredHabilitations = []
    deleteExpiredHabilitationsInKc = []
    extExpiredHabilitations = []
    msg = []
    #getResponse = requests.get(spConfigUrl+"/habilitations/echue", headers=headers)
    expiredHabilitations = json.load(
        open_url(spConfigUrl+"/habilitations/echue",
        method='GET',
        headers=headers))
    for expiredHabilitation in expiredHabilitations:
        if expiredHabilitation is None:
            changed = False
            break
        else:
            if operation == "list":
                listeExpiredHabilitations.append(expiredHabilitation)
            elif operation == "remove":
                #userRepresentation = kc.search_user_by_username(username=expiredHabilitation["idUtilisateur"], realm=realm)
                getkcResponse = open_url(kc.baseurl+"/admin/realms/"+realm+"/users/"+expiredHabilitation["idUtilisateur"],method='GET',headers=kc.restheaders)
                if getkcResponse.getcode() == 404:  # The user does not exist
                    deleteResponse = open_url(
                        spConfigUrl+"/habilitations/"+expiredHabilitation["idUtilisateur"]+"/"+expiredHabilitation["idRole"],
                        method='DELETE',
                        headers=headers)
                    #deleteResponse = requests.delete(spConfigUrl+"/habilitations/"+expiredHabilitation["idUtilisateur"]+"/"+expiredHabilitation["idRole"],headers=headers)
                    if deleteResponse.getcode() == 204:
                        deleteExpiredHabilitations.append(expiredHabilitation)
                    changed = True
                    message = "Habilitation delete from spConfig DB. msg = status: %s, info: %s" % (deleteResponse.getcode(),deleteResponse.info())
                    msg.append({"result": message})
                elif getkcResponse.getcode() == 200:
                    # Search role in realm role
                    userRealmRoles = kc.get_user_realm_roles_with_id(user_id=expiredHabilitation["idUtilisateur"],realm=realm)
                    for realmRole in userRealmRoles:
                        if realmRole["id"] == expiredHabilitation["idRole"]:
                            # Delete exiting realm Roles
                            deletekcResponse = open_url(
                                kc.baseurl+"/admin/realms/"+realm+"/users/"+expiredHabilitation["idUtilisateur"]+"/role-mappings/realm",
                                method='DELETE',
                                headers=kc.restheaders)
                            deleteResponse = open_url(
                                spConfigUrl+"/habilitations/"+expiredHabilitation["idUtilisateur"]+"/"+expiredHabilitation["idRole"],
                                method='DELETE',
                                headers=headers)
                            if deleteResponse.getcode() == 204:
                                deleteExpiredHabilitations.append(expiredHabilitation)
                            if deletekcResponse.getcode() == 204:
                                deleteExpiredHabilitationsInKc.append(expiredHabilitation)
                            changed = True
                            message = "Habilitation delete from spConfig DB. msg = status: %s, info: %s and delete from kc msg = status: %s, info: %s" % (deleteResponse.getcode(),deleteResponse.info(),deletekcResponse.getcode(),deletekcResponse.info())
                            msg.append({"result": message})
                            break
                    # Search role in client role
                    userClientRoles = kc.get_user_client_roles_with_id(user_id=expiredHabilitation["idUtilisateur"],realm=realm)
                    for clientRole in userClientRoles:
                        # Get the client roles
                        client = kc.get_client_by_clientid(client_id=clientRole["clientId"],realm=realm)
                        if client is not None:
                            client_id = client['id']
                            clientRoles = kc.get_client_roles(client_id=client_id,realm=realm)
                            if clientRoles != {}:
                                for clientRole in clientRoles:
                                    if clientRole["id"] == expiredHabilitation["idRole"]:
                                        # Delete exiting client Roles
                                        deletekcResponse = open_url(
                                            kc.baseurl+"/admin/realms/"+realm+"/users/"+expiredHabilitation["idUtilisateur"]+"/role-mappings/clients/"+client_id,
                                            method='DELETE',
                                            headers=kc.restheaders
                                            )
                                        deleteResponse = open_url(
                                            spConfigUrl+"/habilitations/"+expiredHabilitation["idUtilisateur"]+"/"+expiredHabilitation["idRole"],
                                            method='DELETE',
                                            headers=headers)
                                        if deleteResponse.getcode() == 204:
                                            deleteExpiredHabilitations.append(expiredHabilitation)
                                        if deletekcResponse.getcode() == 204:
                                            deleteExpiredHabilitationsInKc.append(expiredHabilitation)
                                        changed = True
                                        message = "Habilitation delete from spConfig DB. msg = status: %s, info: %s and delete from kc msg = status: %s, info: %s" % (deleteResponse.getcode(),deleteResponse.info(),deletekcResponse.getcode(),deletekcResponse.info())
                                        msg.append({"result": message})
            elif operation == "extend":
                newdate_extension = datetime.datetime.strptime(expiredHabilitation["dateEcheance"], '%Y-%m-%d')
                newdate_extension = newdate_extension + datetime.timedelta(days=duration)
                newHabilitation={
                    "idUtilisateur": expiredHabilitation["idUtilisateur"],
                    "idRole": expiredHabilitation["idRole"],
                    "dateEcheance": newdate_extension.strftime('%Y-%m-%d')
                }
                putResponse = open_url(
                    spConfigUrl+"/habilitations/"+expiredHabilitation["idUtilisateur"]+"/"+expiredHabilitation["idRole"],
                    method='PUT',
                    headers=headers,
                    data=json.dumps(newHabilitation)
                )
                if putResponse.getcode() == 200:
                    extExpiredHabilitations.append(newHabilitation)
                changed = True
                message = "Habilitation update from spConfig DB. msg = status: %s, info: %s" % (putResponse.getcode(),putResponse.info())
                msg.append({"result": message})
    msgResponse = {
        "operationType": operation,
        "ExpiredHabilitations": listeExpiredHabilitations,
        "deleteExpiredHabilitations": deleteExpiredHabilitations,
        "deleteExpiredHabilitationsInKc": deleteExpiredHabilitationsInKc,
        "extExpiredHabilitations": extExpiredHabilitations
    }
    result["msg"] = msg
    result["habilitation"] = msgResponse
    result['changed'] = changed
    module.exit_json(**result)


if __name__ == '__main__':
    main()
