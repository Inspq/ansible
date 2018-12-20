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

ANSIBLE_METADATA = {'metadata_version': '1.1',
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
    baseUrl:
        description:
            - URL for the Application.
        required: false
    defaultRoles:
        description:
           - Default roles.
        required: false
    enabled:
        description:
            - enabled.
        default: True
        required: false
    clientAuthenticatorType:
        description: 
            - client Authenticator Type.
        required: false
    redirectUris:
        description:
            - List of redirect URIs.
        required: true
    webOrigins:
        description:
            - List of allowed CORS origins.
        required: false
    consentRequired:
        description:
            - consent Required.
        required: false
    standardFlowEnabled:
        description:
            - standard Flow Enabled.
        required: false
    implicitFlowEnabled:
        description:
            - implicitFlowEnabled. 
        required: false
    directAccessGrantsEnabled:
        description:
            - Direct Access Grants Enabled.
        required: false
    serviceAccountsEnabled:
        description:
            - service Accounts Enabled.
        required: false
    authorizationServicesEnabled:
        description:
            - authorization Services Enabled.
        required: false
        default: true
    protocol:
        description:
            - Protocol.
        required: false
    bearerOnly:
        description:
            - bearer Only access type.
        required: false
    publicClient:
        description:
            - Public client access type.
        required: false
    roles:
        description:
            - List of roles for the client
        required: false
    protocolMappers:
        description:
            - List of protocol mappers for the client
        required: false
    state:
        description:
            - Control if the client must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        description:
            - If yes, allows to remove client and recreate it.
        choices: [ "yes", "no" ]
        default: "no"
        required: false
notes:
    - module does not modify clientId.
'''

EXAMPLES = '''
    - name: Create a client client1 with default settings.
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        name: client1
        description: Client App 1
        rootUrl: http://localhost:8081/app
        redirectUris:
          - http://localhost:8081/*
        webOrigins:
          - "*"
        roles: 
          - name: "groupName"
            description: "Role1"
            composite: true
            composites:
              - id: existinqClient
                name: role1ofclient
        protocolMappers:
          - name: MapperName
            protocol: openid-connect
            protocolMapper: oidc-usermodel-attribute-mapper
            consentRequired: false
            config:
              multivalued: false
              userinfo.token.claim: true
              user.attribute: attributeName
              id.token.claim: true
              access.token.claim: true
              claim.name: nameOfTheClaim
              jsonType.label: String
        state: present

    - name: Re-create client1
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        name: client1
        description: Client App 1
        rootUrl: http://localhost:8081/app
        redirectUris:
          - http://localhost:8081/*
        webOrigins:
          - "*"
        roles: 
          - name: "groupName"
            description: "Role1"
            composite: true
            composites:
              - id: existinqClient
                name: role1ofclient
        protocolMappers:
          - name: MapperName
            protocol: openid-connect
            protocolMapper: oidc-usermodel-attribute-mapper
            consentRequired: false
            config:
              multivalued: false
              userinfo.token.claim: true
              user.attribute: attributeName
              id.token.claim: true
              access.token.claim: true
              claim.name: nameOfTheClaim
              jsonType.label: String
        state: present
        force: yes

    - name: Remove client1.
      keycloak_client:
        url: http://localhost:8080
        username: admin
        password: admin
        realm: master
        name: client1
        state: absent
'''

RETURN = '''
ansible_facts:
  description: JSON representation for the client.
  returned: on success
  type: dict
stderr:
  description: Error message if it is the case
  returned: on error
  type: str
rc:
  description: return code, 0 if success, 1 otherwise.
  returned: always
  type: bool
changed:
  description: Return True if the operation changed the client on the keycloak server, false otherwise.
  returned: always
  type: bool
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
            rootUrl=dict(type='str'),
            name=dict(type='str'),
            description = dict(type='str'),
            adminUrl=dict(type='str'),
            baseUrl=dict(type='str'),
            enabled=dict(type='bool',default=True),
            clientAuthenticatorType = dict(type='str'),
            redirectUris = dict(type='list'),
            webOrigins = dict(type='list'),
            consentRequired = dict(type='bool'),
            standardFlowEnabled = dict(type='bool'),
            implicitFlowEnabled = dict(type='bool'),
            directAccessGrantsEnabled = dict(type='bool'),
            serviceAccountsEnabled = dict(type='bool'),
            authorizationServicesEnabled = dict(type='bool', default=True),
            protocol = dict(type='str'),
            bearerOnly = dict(type='bool'),
            publicClient = dict(type='bool'),
            roles = dict(type='list'),
            defaultRoles = dict(type='list'),
            protocolMappers = dict(type='list'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force'])
    params['enabled'] = module.boolean(module.params['enabled'])
    if "consentRequired" in params and params['consentRequired'] is not None:
        params['consentRequired'] = module.boolean(module.params['consentRequired'])
    if "standardFlowEnabled" in params and params['standardFlowEnabled'] is not None:
        params['standardFlowEnabled'] = module.boolean(module.params['standardFlowEnabled'])
    if "implicitFlowEnabled" in params and params['implicitFlowEnabled'] is not None:
        params['implicitFlowEnabled'] = module.boolean(module.params['implicitFlowEnabled'])
    if "directAccessGrantsEnabled" in params and params['directAccessGrantsEnabled'] is not None:
        params['directAccessGrantsEnabled'] = module.boolean(module.params['directAccessGrantsEnabled'])
    if "serviceAccountsEnabled" in params and params['serviceAccountsEnabled'] is not None:
        params['serviceAccountsEnabled'] = module.boolean(module.params['serviceAccountsEnabled'])
    if "authorizationServicesEnabled" in params and params['authorizationServicesEnabled'] is not None:
        params['authorizationServicesEnabled'] = module.boolean(module.params['authorizationServicesEnabled'])
    if "bearerOnly" in params and params['bearerOnly'] is not None:
        params['bearerOnly'] = module.boolean(module.params['bearerOnly'])
    if "publicClient" in params and params['publicClient'] is not None:
        params['publicClient'] = module.boolean(module.params['publicClient'])
    
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
    newClientProtocolMappers = None
    #newComposites = None
    #newRoleRepresentation = None
    
    # Créer un représentation du client recu en paramètres
    newClientRepresentation = {}
    newClientRepresentation["clientId"] = params['clientId'].decode("utf-8")
    if "rootUrl" in params and params['rootUrl'] is not None:
        newClientRepresentation["rootUrl"] = params['rootUrl'].decode("utf-8")
    if "name" in params and params['name'] is not None:
        newClientRepresentation["name"] = params['name'].decode("utf-8")
    if "description" in params and params['description'] is not None:
        newClientRepresentation["description"] = params['description'].decode("utf-8")
    if "adminUrl" in params and params['adminUrl'] is not None:
        newClientRepresentation["adminUrl"] = params['adminUrl'].decode("utf-8")
    if "baseUrl" in params and params['baseUrl'] is not None:
        newClientRepresentation["baseUrl"] = params['baseUrl'].decode("utf-8")
        
    if "enabled" in params:
        newClientRepresentation["enabled"] = params['enabled']
    if "clientAuthenticatorType" in params and params['clientAuthenticatorType'] is not None:
        newClientRepresentation["clientAuthenticatorType"] = params['clientAuthenticatorType'].decode("utf-8")
    if "redirectUris" in params and params['redirectUris'] is not None:
        newClientRepresentation["redirectUris"] = params['redirectUris']
    if "webOrigins" in params and params['webOrigins'] is not None:
        newClientRepresentation["webOrigins"] = params['webOrigins']
    if "defaultRoles" in params and params['defaultRoles'] is not None:
        newClientRepresentation["defaultRoles"] = params['defaultRoles']
    if "consentRequired" in params:
        newClientRepresentation["consentRequired"] = params['consentRequired']   
    if "standardFlowEnabled" in params:
        newClientRepresentation["standardFlowEnabled"] = params['standardFlowEnabled']
    if "implicitFlowEnabled" in params:
        newClientRepresentation["implicitFlowEnabled"] = params['implicitFlowEnabled']
    if "directAccessGrantsEnabled" in params:
        newClientRepresentation["directAccessGrantsEnabled"] = params['directAccessGrantsEnabled']
    if 'authorizationServicesEnabled' in params:
        newClientRepresentation["authorizationServicesEnabled"] = params['authorizationServicesEnabled']
        if newClientRepresentation["authorizationServicesEnabled"]:
            newClientRepresentation["serviceAccountsEnabled"] = True
        elif "serviceAccountsEnabled" in params:
            newClientRepresentation["serviceAccountsEnabled"] = params['serviceAccountsEnabled']
    if "protocol" in params and params['protocol'] is not None:
        newClientRepresentation["protocol"] = params['protocol'].decode("utf-8")
    if "bearerOnly" in params:
        newClientRepresentation["bearerOnly"] = params['bearerOnly']
    if "publicClient" in params:
        newClientRepresentation["publicClient"] = params['publicClient']
    if 'roles' in params and params['roles'] is not None:
        newClientRoles = params['roles']
    if 'protocolMappers' in params and params['protocolMappers'] is not None:
        newClientProtocolMappers = params['protocolMappers']
    
    clientSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/clients/"
    roleSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/roles/"
    
    result = dict()
    changed = False

    if username == 'admin':
        try:
            headers = loginAndSetHeaders(url, username, password)
        except Exception, e:
            result = dict(
                stderr   = 'login: ' + str(e),
                rc       = 1,
                changed  = changed
                )
            return result
    else:
        try:
            headers = realmLoginAndSetHeaders(url, realm, username, password)
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
                requests.post(clientSvcBaseUrl, headers=headers, data=data)
                # Obtenir le nouveau client créé
                getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Créer les rôles
                if newClientRoles is not None:
                    createOrUpdateClientRoles(newClientRoles, clientSvcBaseUrl, roleSvcBaseUrl, clientRepresentation, headers)
                # Créer les protocols mappers
                if newClientProtocolMappers is not None:
                    for newClientProtocolMapper in newClientProtocolMappers:
                        data=json.dumps(newClientProtocolMapper)
                        requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/protocol-mappers/models', headers=headers, data=data)
                # Obtenir la version finale du nouveau client créé
                getResponse = getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Obtenir le ClientSecret
                if not newClientRepresentation["publicClient"]:
                    getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/client-secret', headers=headers)
                    clientSecretRepresentation = getResponse.json()
                else:
                    clientSecretRepresentation = None   
                # Obtenir les rôles pour le client
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                clientRolesRepresentation = getResponse.json()
                addComposistesToClientRoleRepresentation(clientSvcBaseUrl, clientRepresentation, clientRolesRepresentation, headers)
                clientRepresentation["clientRoles"] = clientRolesRepresentation
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/installation/providers/keycloak-oidc-keycloak-json', headers=headers)
                keycloakOidcKeycloakJson = getResponse.json()
                
                changed = True
                fact = dict(
                    client = clientRepresentation,
                    clientSecret = clientSecretRepresentation
                    )
                if keycloakOidcKeycloakJson :
                    fact["keycloakOidcKeycloakJson"] = keycloakOidcKeycloakJson
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
                    requests.delete(clientSvcBaseUrl + clientRepresentation["id"], headers=headers)
                    changed = True
                    # Stocker le client dans un body prêt a être posté
                    data=json.dumps(newClientRepresentation)
                    # Créer le nouveau client
                    requests.post(clientSvcBaseUrl, headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    excludes = []
                    if "webOrigins" in newClientRepresentation and len(newClientRepresentation['webOrigins']) == 0:
                        excludes.append("webOrigins")
                    # Comparer les clients
                    if (isDictEquals(newClientRepresentation, clientRepresentation, excludes)): # Si le nouveau client n'introduit pas de modification au client existant
                        # Ne rien changer
                        changed = False
                    else: # Si le client doit être modifié
                        # Stocker le client dans un body prêt a être posté
                        data=json.dumps(newClientRepresentation)
                        # Mettre à jour le client sur le serveur Keycloak
                        requests.put(clientSvcBaseUrl + clientRepresentation["id"], headers=headers, data=data)
                        changed = True
                # Obtenir client existant
                getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                clientRepresentation = getResponse.json()[0]
                # Obtenir les rôles
                getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers)
                clientRolesRepresentation = getResponse.json()
                
                addComposistesToClientRoleRepresentation(clientSvcBaseUrl, clientRepresentation, clientRolesRepresentation, headers)
                clientRepresentation["clientRoles"] = clientRolesRepresentation
                
                if createOrUpdateClientRoles(newClientRoles, clientSvcBaseUrl, roleSvcBaseUrl, clientRepresentation, headers):
                    changed = True
                # Traiter les protocol Mappers
                if newClientProtocolMappers is not None:
                    # Obtenir la liste des mappers existant pour le client
                    getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/protocol-mappers/models', headers=headers)
                    clientMappers = getResponse.json()
                    for newClientProtocolMapper in newClientProtocolMappers:
                        clientMapperFound = False
                        # Vérifier si le mapper a créer existe déjà pour le client
                        for clientMapper in clientMappers:
                            if (clientMapper['name'] == newClientProtocolMapper['name']):
                                clientMapperFound = True
                                break
                        # Si le mapper existe pour le client
                        if clientMapperFound:
                            if not isDictEquals(newClientProtocolMapper, clientMapper):
                                # S'il est différent, le modifier
                                changed = True
                                newClientProtocolMapper["id"] = clientMapper["id"]
                                data=json.dumps(newClientProtocolMapper)
                                requests.put(clientSvcBaseUrl + clientRepresentation['id'] + '/protocol-mappers/models/' + clientMapper['id'], headers=headers, data=data)
                        else: # Si le mapper n'existe pas pour ce client
                            changed = True
                            # Créer le mapper
                            data=json.dumps(newClientProtocolMapper)
                            requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/protocol-mappers/models', headers=headers, data=data)
                # Obtenir la version finale du client modifié
                getResponse = getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newClientRepresentation["clientId"]})
                modifiedClientRepresentation = getResponse.json()[0]
                # Obtenir le ClientSecret
                getResponse = requests.get(clientSvcBaseUrl + modifiedClientRepresentation['id'] + '/client-secret', headers=headers)
                clientSecretRepresentation = getResponse.json()
                # Obtenir les rôles
                getResponse = requests.get(clientSvcBaseUrl + modifiedClientRepresentation['id'] + '/roles', headers=headers)
                modifiedClientRolesRepresentation = getResponse.json()
                addComposistesToClientRoleRepresentation(clientSvcBaseUrl, modifiedClientRepresentation, modifiedClientRolesRepresentation, headers)
                modifiedClientRepresentation["clientRoles"] = modifiedClientRolesRepresentation

                getResponse = requests.get(clientSvcBaseUrl + modifiedClientRepresentation['id'] + '/installation/providers/keycloak-oidc-keycloak-json', headers=headers)
                keycloakOidcKeycloakJson = getResponse.json()
                fact = dict(
                    client = modifiedClientRepresentation,
                    clientSecret = clientSecretRepresentation
                    )

                if keycloakOidcKeycloakJson :
                    fact["keycloakOidcKeycloakJson"] = keycloakOidcKeycloakJson

                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            elif state == 'absent': # Le status est absent
                # Supprimer le client
                requests.delete(clientSvcBaseUrl + clientRepresentation['id'], headers=headers)
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

def addComposistesToClientRoleRepresentation(clientSvcBaseUrl, clientRepresentation, clientRolesRepresentation, headers):
    for clientRole in clientRolesRepresentation:
        if clientRole["composite"]:
            getResponse = requests.get(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ clientRole['name'] +'/composites', headers=headers)
            clientRole["composites"] = getResponse.json()
            for roleComposite in clientRole["composites"]:
                if roleComposite['clientRole']:
                    getResponse = requests.get(clientSvcBaseUrl + roleComposite['containerId'], headers=headers)
                    roleCompositeClient = getResponse.json()
                    roleComposite["clientId"] = roleCompositeClient["clientId"]

def createOrUpdateClientRoles(newClientRoles, clientSvcBaseUrl, roleSvcBaseUrl, clientRepresentation, headers):
    changed = False
    # Traiter les rôles
    if newClientRoles is not None:
        for newClientRole in newClientRoles:
            changeNeeded = False
            if 'composites' in newClientRole and newClientRole['composites'] is not None:
                newComposites = newClientRole['composites']
                for newComposite in newComposites:
                    if "id" in newComposite and newComposite["id"] is not None:
                        getResponse=requests.get(clientSvcBaseUrl, headers=headers)
                        keycloakClients = getResponse.json()
                        for keycloakClient in keycloakClients:
                            if keycloakClient['clientId'] == newComposite["id"]:
                                getResponse=requests.get(clientSvcBaseUrl + keycloakClient['id'] + '/roles', headers=headers)
                                roles = getResponse.json()
                                for role in roles:
                                    if role["name"] == newComposite["name"]:
                                        newComposite['id'] = role['id']
                                        newComposite['clientRole'] = True
                                        break
                    else:
                        getResponse=requests.get(roleSvcBaseUrl, headers=headers)
                        realmRoles = getResponse.json()
                        for realmRole in realmRoles:
                            if realmRole["name"] == newComposite["name"]:
                                newComposite['id'] = realmRole['id']
                                newComposite['clientRole'] = False
                                break;
                
            clientRoleFound = False
            if "clientRoles" in clientRepresentation and clientRepresentation["clientRoles"] is not None and len(clientRepresentation["clientRoles"]) > 0:
                clientRoles = clientRepresentation["clientRoles"]
                # Vérifier si le rôle a créer existe déjà pour le client
                for clientRole in clientRoles:
                    if (clientRole['name'] == newClientRole['name']):
                        clientRoleFound = True
                        break
                # Si le rôle existe pour le client
                if not clientRoleFound:
                    changeNeeded = True
                else:
                    if "composites" in newClientRole:
                        excludes = []
                        excludes.append("composites")
                        if not isDictEquals(newClientRole, clientRole, excludes):
                            changeNeeded = True
                        else:
                            for newComposite in newClientRole['composites']:
                                compositeFound = False
                                for existingComposite in clientRole['composites']:
                                    if isDictEquals(newComposite,existingComposite):
                                        compositeFound = True
                                        break
                                if not compositeFound:
                                    changeNeeded = True
                                    break
                    else:
                        if not isDictEquals(newClientRole, clientRole):
                            changeNeeded = True
            else:
                changeNeeded = True
            if changeNeeded:
                # S'il est différent, le modifier
                newRoleRepresentation = {}
                newRoleRepresentation["name"] = newClientRole['name'].decode("utf-8")
                newRoleRepresentation["description"] = newClientRole['description'].decode("utf-8")
                newRoleRepresentation["composite"] = newClientRole['composite'] if "composite" in newClientRole else False
                newRoleRepresentation["clientRole"] = newClientRole['clientRole'] if "clientRole" in newClientRole else True
                    #data=json.dumps(newClientRole)
                data=json.dumps(newRoleRepresentation)
                if clientRoleFound:
                    requests.put(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/' + newClientRole['name'], headers=headers, data=data)
                else:
                    requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=headers, data=data)
                changed = True
                # rôle composites
                if 'composites' in newClientRole and newClientRole['composites'] is not None and len(newClientRole['composites']) > 0:
                    newComposites = newClientRole['composites']
                    if clientRoleFound and "composites" in clientRole:
                        rolesToDelete = []
                        for roleTodelete in clientRole['composites']:
                            tmprole = {}
                            tmprole['id'] = roleTodelete['id']
                            rolesToDelete.append(tmprole)
                        data=json.dumps(rolesToDelete)
                        requests.delete(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers, data=data)
                        
                    data=json.dumps(newClientRole["composites"])

                    requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles/'+ newClientRole['name'] +'/composites', headers=headers, data=data)
    return changed
    
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
