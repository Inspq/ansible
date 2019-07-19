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
        type: str
    spConfigClient_id:
        description:
            - Sx5-sp-Config Client ID.
        required: true
        type: str
    spConfigClient_secret:
        description:
            - Sx5-sp-Config Client Secret.
        required: false
        type: str
    operation:
        description:
            - operation on the expired accreditation.
        choices: [list, remove, extend]
        default: list
        type: str
    duration:
        description:
            - duration of extension of expired accreditation.
        type: int
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
from ansible.module_utils.keycloak import KeycloakAPI, keycloak_argument_spec
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url
import datetime
import json

URL_HABILITATION = "{url}/habilitations/utilisateurs/{idUtilisateur}/roles/{idRole}"
#URL_HABILITATION = "{url}/habilitations/{idUtilisateur}/{idRole}"
URL_ECHUE = "{url}/habilitations/echue"

def getExpiredHabilitations(url, headers):
    urlEchue = URL_ECHUE.format(url=url)
    expiredHabilitations = json.load(
        open_url(
            urlEchue,
            method='GET',
            headers=headers))
    return expiredHabilitations


def deleteHabilitation(url, user_id, role_id, headers):
    urlHabilitation = URL_HABILITATION.format(url=url, idUtilisateur=user_id, idRole=role_id)
    deleteResponse = open_url(
        urlHabilitation,
        method='DELETE',
        headers=headers)
    return deleteResponse


def updateHabilitation(url, user_id, role_id, habilitation, headers):
    urlHabilitation = URL_HABILITATION.format(url=url, idUtilisateur=user_id, idRole=role_id)
    putResponse = open_url(
        urlHabilitation,
        method='PUT',
        headers=headers,
        data=json.dumps(habilitation)
    )
    return putResponse


def main():
    argument_spec = keycloak_argument_spec()
    meta_args = dict(
        realm=dict(type='str', default='master'),
        spConfigUrl=dict(type='str', required=True),
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
    changed = False
    headers = kc.restheaders

    # Search expired accreditation in sx5_sp_config.
    listeExpiredHabilitations = []
    deleteExpiredHabilitations = []
    deleteExpiredHabilitationsInKc = []
    extExpiredHabilitations = []
    msgList = []
    msgRm = []
    msgExt = []
    expiredHabilitations = getExpiredHabilitations(url=spConfigUrl, headers=headers)
    for expiredHabilitation in expiredHabilitations:
        if expiredHabilitation is None:
            changed = False
            break
        else:
            if operation == "list":
                listeExpiredHabilitations.append(expiredHabilitation)
                message = "Habilitation ExpiredHabilitations added"
                msgList.append({"info": message})
            elif operation == "remove":
                try:
                    # Check if the user still exist on the Keycloak server
                    userRepresentation = kc.get_user_by_id(user_id=expiredHabilitation["idUtilisateur"], realm=realm)
                except Exception as e:
                    if "msg" in e.message and "HTTP Error 404" in e.message["msg"]:
                        userRepresentation = None
                    else:
                        module.fail_json(msg=e.message["msg"])
                try:
                    # Get the role to expire if it still exists
                    roleRepresentation = kc.get_role_by_id(roleid=expiredHabilitation["idRole"], realm=realm)
                except Exception as e:
                    if "msg" in e.message and "HTTP Error 404" in e.message["msg"]:
                        roleRepresentation = None
                    else:
                        module.fail_json(msg=e.message["msg"])
                if userRepresentation is not None and roleRepresentation is not None:
                    if roleRepresentation["clientRole"]:  # If it's a client Role
                        # Get the client ID
                        clientId = roleRepresentation["containerId"]
                        # Remove the client Role mapping for the user
                        kc.delete_user_client_role(user_id=expiredHabilitation["idUtilisateur"], client_id=clientId, role=roleRepresentation, realm=realm)
                        deleteExpiredHabilitationsInKc.append(expiredHabilitation)
                    else:  # It's a realm role
                        # Delete the realm role user mapping
                        kc.delete_user_realm_role(user_id=expiredHabilitation["idUtilisateur"], role=roleRepresentation, realm=realm)
                        deleteExpiredHabilitationsInKc.append(expiredHabilitation)
                # Delete expired habilitation form spconfig
                deleteHabilitation(url=spConfigUrl, user_id=expiredHabilitation["idUtilisateur"], role_id=expiredHabilitation["idRole"], headers=headers)
                deleteExpiredHabilitations.append(expiredHabilitation)
                changed = True
            elif operation == "extend":
                newdate_extension = datetime.datetime.strptime(expiredHabilitation["dateEcheance"], '%Y-%m-%d')
                newdate_extension = newdate_extension + datetime.timedelta(days=duration)
                newHabilitation = {
                    "idUtilisateur": expiredHabilitation["idUtilisateur"],
                    "idRole": expiredHabilitation["idRole"],
                    "dateEcheance": newdate_extension.strftime('%Y-%m-%d')
                }
                putResponse = updateHabilitation(
                    url=spConfigUrl,
                    user_id=expiredHabilitation["idUtilisateur"],
                    role_id=expiredHabilitation["idRole"],
                    habilitation=newHabilitation,
                    headers=headers)
                if putResponse.getcode() == 200:
                    extExpiredHabilitations.append(newHabilitation)
                changed = True
                message = "Habilitation update from spConfig DB. msg = status: %s, info: %s" % (
                    putResponse.getcode(),
                    putResponse.info())
                msgExt.append({"info": message})
    msgResponse = {
        "operationType": operation,
        "ExpiredHabilitations": listeExpiredHabilitations,
        "deleteExpiredHabilitations": deleteExpiredHabilitations,
        "deleteExpiredHabilitationsInKc": deleteExpiredHabilitationsInKc,
        "extExpiredHabilitations": extExpiredHabilitations
    }
    msgInfo = {
        "List": msgList,
        "Remove": msgRm,
        "Extend": msgExt
    }
    result["msg"] = msgInfo
    result["habilitation"] = msgResponse
    result['changed'] = changed
    module.exit_json(**result)


if __name__ == '__main__':
    main()
