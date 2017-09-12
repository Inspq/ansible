#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2017, INSPQ Team SX5
#
# This file is not part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
author: "Etienne Sadio (etienne.sadio@inspq.qc.ca"
module: sx5_client
short_description: Configure a client application url in SX5 DB 
description:
    - This module creates, creat or update client application url.
version_added: "2.3"
options:
    idp_url:
        description:
            - The url of the Keycloak server.
        default: http://localhost:8080/auth    
        required: true
    username:
        description:
            - The username to logon to the master realm in Keycloak.
        required: true
    password:
        description:
            - The password for the user to logon the master realm in Keycloak.
        required: true
    realm:
        description:
            - The name of the Keycloak realm in which is the client.
        required: true
    clientId:
        description:
            - OIDC Client ID for the client in Keycloak.
        required: true
    force:
        choices: [ "yes", "no" ]
        default: "no"
        description:
            - If yes, allows to remove client and recreate it.
        required: false
    state:
        description:
            - Control if the client must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    clientUrl:
        description:
            - Client URL.
        default: 
        required: true
    sx5url:
        description:
            - sx5 REST services URL.
        default: 
        required: true
notes:
    - module does not modify clientId.
'''

EXAMPLES = '''
    - name: Create a client client1 with default settings.
      SX5_client:
        idp_url: http://localhost:8080/auth
        realm: Master
        clientId: client1
        clientUrl: http://localhost:8088/clients
        sx5url: http://localhost/client1
        state: present

    - name: Re-create client1
      SX5_client:
        idp_url: http://localhost:8080/auth
        realm: Master
        clientId: client1
        clientUrl: http://localhost:8088/clients
        sx5url: http://localhost/client1
        state: present
        force: yes
        
    - name: Remove client1
      SX5_client:
        idp_url: http://localhost:8080/auth
        realm: Master
        clientId: client1
        clientUrl: http://localhost:8088/clients
        sx5url: http://localhost/client1
        state: absent

'''

RETURN = '''
result:
    ansible_facts: JSON representation for the client
    stderr: Error message if it is the case
    rc: return code, 0 if success, 1 otherwise
    changed: Return True if the operation changed the client on the SX5 DB, false otherwise.
'''
import requests
import json
import urllib
from ansible.module_utils.sx5_client_utils import *
from __builtin__ import isinstance    

def main():
    module = AnsibleModule(
        argument_spec = dict(
            idp_url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
            realm=dict(type='str', required=True),
            clientId=dict(type='str', required=True),
            force=dict(type='bool', default=False),
            state=dict(choices=["absent", "present"], default='present'),
            clientUrl = dict(type='str', required=True),
            sx5url = dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force'])
    
    result = client(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
def client(params):
    idp_url = params['idp_url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    force = params['force']
    sx5url = params['sx5url']
    state = params['state']
    
    clientSvcBaseUrl = idp_url + "/auth/admin/realms/" + realm + "/clients/"
        
    # Créer un représentation du client pour BD clientURL
    newClientDBRepresentation = {}
    newClientDBRepresentation["clientId"] = params['clientId'].decode("utf-8")
    newClientDBRepresentation["realmId"] = params['realm'].decode("utf-8")
    newClientDBRepresentation["url"] = params['clientUrl'].decode("utf-8")
    if params['username'] is not None:
        newClientDBRepresentation["username"] = params['username'].decode("utf-8")
    else:
        newClientDBRepresentation["username"] = ""
    if params['password'] is not None:
        newClientDBRepresentation["password"] = params['password'].decode("utf-8")
    else:
        newClientDBRepresentation["password"] = ""
    
    rc = 0
    result = dict()
    changed = False
    
    try:
        headers = loginAndSetHeaders(idp_url, username, password)
    except Exception, e:
        result = dict(
            stderr   = 'login: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
    try: 
        # Vérifier si le client existe sur le serveur Keycloak
        getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientDBRepresentation["clientId"]})
    except Exception, e:
        result = dict(
            stderr   = 'Keycloak client get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
    
    if len(getResponse.json()) == 0: # Le client n'existe pas
        result = dict(
            stderr   = 'Client not exit in IDP: ' + newClientDBRepresentation["clientId"],
            rc       = 1,
            changed  = changed
            )
        return result

    if state == 'present':# Si le status est présent
        if force: # Si force est de yes modifier le client meme s'il existe
            try:
                getResponse = sx5RestClientget(sx5url,newClientDBRepresentation["clientId"],newClientDBRepresentation["realmId"])
                if getResponse.status_code == 200:
                    dataResponse = getResponse.json()
                    body = {
                            "clientId": newClientDBRepresentation["clientId"],
                            "realmId": newClientDBRepresentation["realmId"],
                            "url": newClientDBRepresentation["url"],
                            "username": newClientDBRepresentation["username"],
                            "password": newClientDBRepresentation["password"]
                    }
                    try:
                        getResponse = requests.put(sx5url+'/'+str(dataResponse['id']),json=body)
                        dataResponse = getResponse.json()
                        changed = True
                        fact = dict(
                            clientSx5 = dataResponse
                            )
                        result = dict(
                            ansible_facts = fact,
                            rc = 0,
                            changed = changed
                            )
                    except requests.exceptions.RequestException, e:
                        fact = dict(
                            clientSx5 = newClientDBRepresentation)
                        result = dict(
                            ansible_facts= fact,
                            stderr   = 'Update client: ' + newClientDBRepresentation["clientId"] + ' erreur: ' + str(e),
                            rc       = 1,
                            changed  = changed
                            )
                    except ValueError, e:
                        fact = dict(
                            clientSx5 = newClientDBRepresentation)
                        result = dict(
                            ansible_facts= fact,
                            stderr   = 'Update client: ' + newClientDBRepresentation["clientId"] + ' erreur: ' + str(e),
                            rc       = 1,
                            changed  = changed
                            )
                else:
                    body = {
                            "clientId": newClientDBRepresentation["clientId"],
                            "realmId": newClientDBRepresentation["realmId"],
                            "url": newClientDBRepresentation["url"],
                            "username": newClientDBRepresentation["username"],
                            "password": newClientDBRepresentation["password"]
                    }
                    try:
                        getResponse = requests.post(sx5url,json=body)
                        dataResponse = getResponse.json()
                        changed = true
                        fact = dict(
                            clientSx5 = dataResponse
                            )
                        result = dict(
                            ansible_facts = fact,
                            rc = 0,
                            changed = changed
                            )
                        
                    except requests.exceptions.RequestException, e:
                        fact = dict(
                            clientSx5 = newClientDBRepresentation)
                        result = dict(
                            ansible_facts= fact,
                            stderr   = 'Create client: ' + newClientDBRepresentation["clientId"] + ' erreur: ' + str(e),
                            rc       = 1,
                            changed  = changed
                            )
                    except ValueError, e:
                        fact = dict(
                            clientSx5 = newClientDBRepresentation)
                        result = dict(
                            ansible_facts= fact,
                            stderr   = 'Create client: ' + newClientDBRepresentation["clientId"] + ' erreur: ' + str(e),
                            rc       = 1,
                            changed  = changed
                            )
            except Exception, e:
                result = dict(
                    stderr   = 'Client get in Force = yes and state = present: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        else:  # Si force est de no modifier le client s'il existe change
            try:
                getResponse = sx5RestClientget(sx5url,newClientDBRepresentation["clientId"],newClientDBRepresentation["realmId"])
                if getResponse.status_code == 404:
                    try:
                        clientSx5ServRepresentation = sx5RestClientCreat(sx5url,newClientDBRepresentation["clientId"],newClientDBRepresentation["realmId"],newClientDBRepresentation["url"],newClientDBRepresentation["username"],newClientDBRepresentation["password"])
                        changed = True
                        fact = dict(
                            clientSx5 = clientSx5ServRepresentation
                            )
                        result = dict(
                            ansible_facts = fact,
                            rc = 0,
                            changed = changed
                            )
                    except Exception, e:
                        result = dict(
                            stderr   = 'Client create or update error: ' + str(e),
                            rc       = 1,
                            changed  = changed
                            )
                else:
                    dataResponse = getResponse.json()
                    excludes = []
                    if isDictEquals(dataResponse,newClientDBRepresentation,excludes):
                        changed = False
                    else:
                        try:
                            clientSx5ServRepresentation = sx5RestClientCreat(sx5url,newClientDBRepresentation["clientId"],newClientDBRepresentation["realmId"],newClientDBRepresentation["url"],newClientDBRepresentation["username"],newClientDBRepresentation["password"])
                            changed = True
                            fact = dict(
                                clientSx5 = clientSx5ServRepresentation
                                )
                            result = dict(
                                ansible_facts = fact,
                                rc = 0,
                                changed = changed
                                )
                        except Exception, e:
                            result = dict(
                                stderr   = 'Client create or update error: ' + str(e),
                                rc       = 1,
                                changed  = changed
                                )
            except Exception, e:
                result = dict(
                    stderr   = 'Client get in force = no and state = present: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
    elif state == 'absent':# Supprimer le client
        try:
            getResponse = sx5RestClientget(sx5url,newClientDBRepresentation["clientId"],newClientDBRepresentation["realmId"])
            if getResponse.status_code == 200:
                dataResponse = getResponse.json()
                try:
                    deleteResponse = requests.delete(sx5url+ '/' + dataResponse['id'],headers=headers)
                    changed = True
                    result = dict(
                            stdout   = 'deleted' + deleteResponse,
                            rc       = 0,
                            changed  = changed
                        )
                except requests.exceptions.RequestException, e:
                    fact = dict(
                        clientSx5 = dataResponse)
                    result = dict(
                        ansible_facts= fact,
                        stderr   = 'Delete client: ' + newClientDBRepresentation["clientId"] + ' erreur: ' + str(e),
                        rc       = 1,
                        changed  = changed
                        )
                except ValueError, e:
                    fact = dict(
                        clientSx5 = dataResponse)
                    result = dict(
                        ansible_facts = fact,
                        stderr   = 'Delete client: ' + newClientDBRepresentation["clientId"] + ' erreur: ' + str(e),
                        rc       = 1,
                        changed  = changed
                        )
            else:
                result = dict(
                        stdout   = 'Client or realm not fond',
                        rc       = 0,
                        changed  = changed
                    )
        except Exception, e:
            result = dict(
                stderr   = 'Client get in state = absent : ' + str(e),
                rc       = 1,
                changed  = changed
                )
    return result
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
