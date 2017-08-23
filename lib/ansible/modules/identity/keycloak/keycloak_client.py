#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2017, Philippe Gauthier INSPQ <philippe.gauthier@inspq.qc.ca>
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
author: "Philippe Gauthier (philippe.gauthier@inspq.qc.ca"
module: keycloak_client
short_description: Configure a client in Keycloak
description:
    - This module creates, removes or update Keycloak client.
version_added: "2.3"
options:
    url:
        description:
            - The url of the Keycloak server.
        default: http://localhost:8080/auth    
        required: true    
    username:
        description:
            - The username to logon to the master realm.
        required: true
    password:
        description:
            - The password for the user to logon the master realm.
        required: true
    realm:
        description:
            - The name of the realm in which is the client.
        required: true
    clientId:
        description:
            - OIDC Client ID for the client.
        required: true
    rootUrl:
        description:
            - The root URL of the client Application.
        required: false
    name:
        description:
            - Name for the client application.
        required: false
    description:
        description:
            - Description of the client Application.
        required: false
    adminUrl:
        description:
            - URL for the admin module for the Application.
        required: false
    enabled:
        description:
            - enabled.
        default: True
        required: false
    clientAuthenticatorType:
        description: 
            - client Authenticator Type.
        default: client-secret
        required: false
    redirectUris:
        description:
            - List of redirect URIs.
        default: 
        required: true
    webOrigins:
        description:
            - List of allowed CORS origins.
        default: []
        required: false
    consentRequired:
        description:
            - consent Required.
        default: False
        required: false
    standardFlowEnabled:
        description:
            - standard Flow Enabled.
        default: True
        required: false
    implicitFlowEnabled:
        description:
            - implicitFlowEnabled. 
        default: True
        required: false
    directAccessGrantsEnabled:
        description:
            - Direct Access Grants Enabled.
        default: True
        required: false
    serviceAccountsEnabled:
        description:
            - service Accounts Enabled.
        default: True
        required: false
    authorizationServicesEnabled:
        description:
            - authorization Services Enabled.
        default: True
        required: false
    protocol:
        description:
            - Protocol.
        default: openid-connect
        required: false
    bearerOnly:
        description:
            - bearer Only access type.
        default: False
        required: false
    publicClient:
        description:
            - Public client access type.
        default: False
        required: false
    roles:
        description:
            - List of roles for the client
        required: false
    state:
        description:
            - Control if the client must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        choices: [ "yes", "no" ]
        default: "no"
        description:
            - If yes, allows to remove realm and recreate it.
        required: false
notes:
    - module does not modify clientId.
'''

EXAMPLES = '''
    - name: Create a client client1 with default settings.
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: admin
        name: client1
        state: present

    - name: Re-create client1
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: admin
        name: client1
        state: present
        force: yes

    - name: Remove client1.
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: admin
        name: client1
        state: absent
'''

RETURN = '''
result:
    ansible_facts: JSON representation for the client
    stderr: Error message if it is the case
    rc: return code, 0 if success, 1 otherwise
    changed: Return True if the operation changed the client on the keycloak server, false otherwise.
'''
import requests
import json
import urllib
from ansible.module_utils.keycloak_utils import *
from __builtin__ import isinstance    

def main():
    module = AnsibleModule(
        argument_spec = dict(
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
            realm=dict(type='str', required=True),
            clientId=dict(type='str', required=True),
            rootUrl=dict(type='str', default=None),
            name=dict(type='str', default=None),
            description = dict(type='str', default=None),
            adminUrl=dict(type='str', default=None),
            enabled=dict(type='bool',default=True),
            clientAuthenticatorType = dict(type='str',default='client-secret'),
            redirectUris = dict(type='list', required=True),
            webOrigins = dict(type='list', default=[]),
            consentRequired = dict(type='bool', default=False),
            standardFlowEnabled = dict(type='bool', default=True),
            implicitFlowEnabled = dict(type='bool', default=True),
            directAccessGrantsEnabled = dict(type='bool', default=True),
            serviceAccountsEnabled = dict(type='bool', default=True),
            #authorizationServicesEnabled = dict(type='bool', default=True),
            protocol = dict(type='str', default='openid-connect'),
            bearerOnly = dict(type='bool', default=False),
            publicClient = dict(type='bool', default=False),
            roles = dict(type='list'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
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
    url = params['url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    state = params['state']
    force = params['force']
    newClientRoles = None
    
    # Créer un représentation du client recu en paramètres
    newClientRepresentation = {}
    newClientRepresentation["clientId"] = params['clientId'].decode("utf-8")
    if params['rootUrl'] is not None:
        newClientRepresentation["rootUrl"] = params['rootUrl'].decode("utf-8")
    if params['name'] is not None:
        newClientRepresentation["name"] = params['name'].decode("utf-8")
    if params['description'] is not None:
        newClientRepresentation["description"] = params['description'].decode("utf-8")
    if params['adminUrl'] is not None:
        newClientRepresentation["adminUrl"] = params['adminUrl'].decode("utf-8")
    newClientRepresentation["enabled"] = params['enabled']
    newClientRepresentation["clientAuthenticatorType"] = params['clientAuthenticatorType'].decode("utf-8")
    newClientRepresentation["redirectUris"] = params['redirectUris']
    newClientRepresentation["webOrigins"] = params['webOrigins']
    newClientRepresentation["consentRequired"] = params['consentRequired']   
    newClientRepresentation["standardFlowEnabled"] = params['standardFlowEnabled']
    newClientRepresentation["implicitFlowEnabled"] = params['implicitFlowEnabled']
    newClientRepresentation["directAccessGrantsEnabled"] = params['directAccessGrantsEnabled']
    newClientRepresentation["serviceAccountsEnabled"] = params['serviceAccountsEnabled']
    #newClientRepresentation["authorizationServicesEnabled"] = params['authorizationServicesEnabled']
    newClientRepresentation["protocol"] = params['protocol'].decode("utf-8")
    newClientRepresentation["bearerOnly"] = params['bearerOnly']
    newClientRepresentation["publicClient"] = params['publicClient']
    if 'roles' in params and params['roles'] is not None:
        newClientRoles = params['roles']
    
    clientSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/clients/"
    
    rc = 0
    result = dict()
    changed = False

    try:
        headers = loginAndSetHeaders(url, username, password)
    except Exception, e:
        result = dict(
            stderr   = 'login: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
    try: 
        # Vérifier si le client existe sur le serveur Keycloak
        getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
    except Exception, e:
        result = dict(
            stderr   = 'first client get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    if len(getResponse.json()) == 0: # Le client n'existe pas
        # Creer le client
        
        if (state == 'present'): # Si le status est présent
            try:
                # Stocker le client dans un body prêt a être posté
                data=json.dumps(newClientRepresentation)
                # Créer le client
                postResponse = requests.post(clientSvcBaseUrl, headers=headers, data=data)
                # Obtenir le nouveau client créé
                getResponse = getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Créer les rôles
                if newClientRoles is not None:
                    for newClientRole in newClientRoles:
                        data=json.dumps(newClientRole)
                        postResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers, data=data)
                # Obtenir le ClientSecret
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/client-secret', headers=headers)
                clientSecretRepresentation = getResponse.json()
                # Obtenir les rôles pour le client
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                clientRolesRepresentation = getResponse.json()
                changed = True
                fact = dict(
                    client = clientRepresentation,
                    clientSecret = clientSecretRepresentation,
                    clientRoles = clientRolesRepresentation)
                
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                fact = dict(
                    client = newClientRepresentation)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post client: ' + newClientRepresentation["clientId"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                fact = dict(
                    client = newClientRepresentation)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post client: ' + newClientRepresentation["clientId"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        elif state == 'absent': # Sinon, le status est absent
            result = dict(
                stdout   = newClientRepresentation["clientId"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # Le client existe déjà
        clientRepresentation = getResponse.json()[0]
        try:
            if (state == 'present'): # si le status est présent
                if force: # Si l'option force est sélectionné
                    # Supprimer le client existant
                    deleteResponse = requests.delete(clientSvcBaseUrl + clientRepresentation["id"], headers=headers)
                    changed = True
                    # Stocker le client dans un body prêt a être posté
                    data=json.dumps(newClientRepresentation)
                    # Créer le nouveau client
                    postResponse = requests.post(clientSvcBaseUrl, headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    #print 'newClientRepresentation : ' + str(newClientRepresentation)
                    #print 'clientRepresentation : ' + str(clientRepresentation)
                    excludes = []
                    if len(newClientRepresentation['webOrigins']) == 0:
                        excludes.append("webOrigins")
                    # Comparer les clients
                    if (isDictEquals(newClientRepresentation, clientRepresentation, excludes)): # Si le nouveau client n'introduit pas de modification au client existant
                        # Ne rien changer
                        changed = False
                    else: # Si le client doit être modifié
                        # Stocker le client dans un body prêt a être posté
                        data=json.dumps(newClientRepresentation)
                        # Mettre à jour le client sur le serveur Keycloak
                        updateResponse = requests.put(clientSvcBaseUrl + clientRepresentation["id"], headers=headers, data=data)
                        changed = True
                # Obtenir le nouveau client créé
                getResponse = getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Traiter les rôles
                if newClientRoles is not None:
                    # Obtenir la liste des rôles existant pour le client
                    getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                    clientRoles = getResponse.json()
                    for newClientRole in newClientRoles:
                        data=json.dumps(newClientRole)
                        clientRoleFound = False
                        # Vérifier si le rôle a créer exite déjà pour le client
                        for clientRole in clientRoles:
                            if (clientRole['name'] == newClientRole['name']):
                                clientRoleFound = True
                                exit
                        # Si le rôle existe pour le client
                        if clientRoleFound:
                            # Obtenir la définition du rôle    
                            getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/' + newClientRole['name'], headers=headers)
                            clientRole = getResponse.json()
                            # Comparer le rôle existant avec celui envoyé
                            if not isDictEquals(newClientRole, clientRole):
                                # S'il est différent, le modifier
                                changed = True
                                putResponse=requests.put(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/' + newClientRole['name'], headers=headers, data=data)
                        else: # Si le rôle n'existe pas pour ce client
                            changed = True
                            # Créer le rôle
                            postResponse = requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers, data=data)
                # Obtenir le ClientSecret
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/client-secret', headers=headers)
                clientSecretRepresentation = getResponse.json()
                # Obtenir les rôles
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                clientRolesRepresentation = getResponse.json()

                fact = dict(
                    client = clientRepresentation,
                    clientSecret = clientSecretRepresentation,
                    clientRoles = clientRolesRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            elif state == 'absent': # Le status est absent
                # Supprimer le client
                deleteResponse = requests.delete(clientSvcBaseUrl + clientRepresentation['id'], headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                stderr   = 'put or delete client: ' + newClientRepresentation['clientId'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                stderr   = 'put or delete client: ' + newClientRepresentation['clientId'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    return result
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
