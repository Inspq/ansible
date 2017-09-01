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
module: keycloak_identity_provider
short_description: Configure an identity provider in Keycloak
description:
  - This module creates, removes or update Keycloak identity provider.
version_added: "1.1"
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
    - The name of the realm in which is the identity provider.
    required: true
  alias:
    description:
    - The alias of the identity provider.
    required: true
  displayName:
    description:
    - The display name of the realm.
    required: false
  providerId:
    description:
    - Type of identity provider.
    default: oidc
    required: false
  enabled:
    description:
    - enabled.
    default: True
    required: false
  updateProfileFirstLoginMode:
    description:
    - update Profile First Login Mode.
    default: on
    required: false
  trustEmail:
    description: 
    - trust Email.
    default: False
    required: false
  storeToken:
    description:
    - store Token.
    default: True
    required: false
  addReadTokenRoleOnCreate:
    description:
    - add Read Token Role On Create.
    default: True
    required: false
  authenticateByDefault:
    description:
    - authenticate By Default.
    default: False
    required: false
  linkOnly:
    description:
    - link Only.
    default: False
    required: false
  firstBrokerLoginFlowAlias:
    description:
    - first Broker Login Flow Alias.
    default: first broker login
    required: false
  config:
    description:
    - Detailed configuration of the identity provider. 
    required: false
  mappers:
    description:
    - List of mappers for the Identity provider.
    default: []
    required: false
  state:
    choices: [ "present", "absent" ]
    default: present
    description:
    - Control if the realm exists.
    required: false
  force:
    choices: [ "yes", "no" ]
    default: "no"
    description:
    - If yes, allows to remove realm and recreate it.
    required: false
notes:
  - module does not modify identity provider alias.
'''

EXAMPLES = '''
    - name: Create IdP1 fully configured with idp user attribute mapper and a role mapper
      keycloak_identity_provider:
        realm: "master"
        url: "http://localhost:8080"
        username: "admin"
        password: "password"  
        alias: "IdP1"
        displayName: "My super dooper IdP"
        providerId: "oidc"
        config:
          openIdConfigurationUrl: https://my.idp.com/auth
          clientId: ClientIdMyIdpGaveMe
          clientSecret: ClientSecretMyIdpGaveMe
          disableUserInfo: False
          defaultScope: "openid email profile"
        mappers:
          - name: ClaimMapper
            identityProviderMapper: oidc-user-attribute-idp-mapper
            config:
              claim: claim1
              user.attribute: attr1
          - name: MyRoleMapper
            identityProviderMapper: oidc-role-idp-mapper
            config:
              claim: claimName
              claim.value: valueTahtGiveRole
              role: roleName
        state: present

    - name: Re-create the Idp1 without mappers. The existing Idp will be deleted.
      keycloak_identity_provider:
        realm: "master"
        url: "http://localhost:8080"
        username: "admin"
        password: "password"  
        alias: "IdP1"
        displayName: "My super dooper IdP"
        providerId: "oidc"
        config:
          openIdConfigurationUrl: https://my.idp.com/auth
          clientId: ClientIdMyIdpGaveMe
          clientSecret: ClientSecretMyIdpGaveMe
          disableUserInfo: False
          defaultScope: "openid email profile"
        state: present
        force: yes

    - name: Remove a the Idp IdP1.
      keycloak_identity_provider:
        alias: IdP1
        state: absent
'''

RETURN = '''
result:
    ansible_facts: JSON Representation for the identity provider
    stderr: Error message if ther is any.
    rc: Return code, 1 if fail, 0 if success.
    changed: True if the action changed the configuration of the Keycloak server, False otherwise.
'''
import requests
import json
import urllib
from ansible.module_utils.keycloak_utils import *
    
def addIdPEndpoints(idPConfiguration, url):
    '''
fonction :      addIdPEndpoints
description:    Cette fonction permet d'intéroger le endpoint openid-configuration d'un fournisseur
                d'identité afin d'en extraire les différents endpoints à mettre dans l'objet
                config de keycloak.
paramètres:
    idPConfiguration:
    type: dict
    description: Dictionnaire contenant ls structure config à compléter.
    url:
    type: str
    description: URL de la configuration OpenID connect à intérroger
    '''
#    url = None
#    if 'openIdConfigurationUrl' in idPConfiguration.keys():
#        url = idPConfiguration["openIdConfigurationUrl"]
#        del idPConfiguration["openIdConfigurationUrl"]
    if url is not None:
        try:
            openidConfigRequest = requests.get(url, verify=False)
            openIdConfig = openidConfigRequest.json()
            if 'userinfo_endpoint' in openIdConfig.keys():
                idPConfiguration["userInfoUrl"] = openIdConfig["userinfo_endpoint"]
            if 'token_endpoint' in openIdConfig.keys():
                idPConfiguration["tokenUrl"] = openIdConfig["token_endpoint"]
            if 'jwks_uri' in openIdConfig.keys():
                idPConfiguration["jwksUrl"] = openIdConfig["jwks_uri"]
            if 'issuer' in openIdConfig.keys():
                idPConfiguration["issuer"] = openIdConfig["issuer"]
            if 'authorization_endpoint' in openIdConfig.keys():
                idPConfiguration["authorizationUrl"] = openIdConfig["authorization_endpoint"]
            if 'end_session_endpoint' in openIdConfig.keys():
                idPConfiguration["logoutUrl"] = openIdConfig["end_session_endpoint"]        
        except Exception, e:
            raise e

def deleteAllMappers(url, bearerHeader):
    changed = False
    try:
        # Obtenir la liste des mappers existant
        getMappersRequest = requests.get(url + '/mappers', headers={'Authorization' : bearerHeader})
        mappers = getMappersRequest.json()
        for mapper in mappers:
            requests.delete(url + '/mappers/' + mapper['id'], headers={'Authorization' : bearerHeader})
    except requests.exceptions.RequestException, ValueError:
        return False
    except Exception, e:
        raise e
     
    return changed
def createOrUpdateMappers(url, headers, alias, idPMappers):
    changed = False
    create = False
   
    try:
        # Obtenir la liste des mappers existant
        getMappersRequest = requests.get(url + '/mappers', headers=headers)
        try:
            mappers = getMappersRequest.json()
        except ValueError: # Il n'y a pas de mapper de défini pour cet IdP
            mappers = []
            create = True
        for idPMapper in idPMappers:
            mapperFound = False
            mapperId = ""
            for mapper in mappers:
                if mapper['name'] == idPMapper['name']:
                    mapperId = mapper['id']
        
            if len(mapperId) == 0:
                mapper = {}
                
            for key in idPMapper: 
                mapperChanged = False
                if key in mapper.keys():
                    if isinstance(idPMapper[key],dict):
                        for dictKey in idPMapper[key]:
                            if dictKey not in mapper[key].keys() or idPMapper[key][dictKey] <> mapper[key][dictKey]:
                                mapper[key][dictKey] = idPMapper[key][dictKey]
                                mapperChanged = True
                    elif idPMapper[key] <> mapper[key]:      
                        mapper[key] = idPMapper[key]
                        mapperChanged = True
                else:
                    mapper[key] = idPMapper[key]
                    mapperChanged = True
            if 'identityProviderMapper' in idPMapper.keys(): # si le type de mapper a été fourni
                if mapper['identityProviderMapper'] <> idPMapper['identityProviderMapper']:
                    mapper['identityProviderMapper'] = idPMapper['identityProviderMapper']
                    mapperChanged = True
            else: # Sinon, utiliser la valeur par défaut
                if 'identityProviderMapper' not in mapper.keys():
                    mapper['identityProviderMapper'] = 'oidc-user-attribute-idp-mapper'
                    mapperChanged = True
            if 'identityProviderAlias' not in mapper.keys() or mapper['identityProviderAlias'] <> alias:
                mapper['identityProviderAlias'] = alias
                mapperChanged = True
            if mapperChanged:
                data=json.dumps(mapper)
                #print str(data)
                if len(mapperId) == 0:
                    response = requests.post(url + '/mappers', headers=headers, data=data)
                else:
                    response = requests.put(url + '/mappers/' + mapperId, headers=headers, data=data)
                changed = True 
    except Exception ,e :
        raise e
    return changed

def main():
    module = AnsibleModule(
        argument_spec = dict(
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
            realm=dict(type='str', required=True),
            alias=dict(type='str', required=True),
            displayName=dict(type='str', default=""),
            providerId=dict(type='str', default="oidc"),
            enabled = dict(type='bool', default=True),
            updateProfileFirstLoginMode=dict(type='str', default="on"),
            trustEmail=dict(type='bool',default=False),
            storeToken = dict(type='bool',default=True),
            addReadTokenRoleOnCreate = dict(type='bool', default=True),
            authenticateByDefault = dict(type='bool', default=False),
            linkOnly = dict(type='bool', default=False),
            firstBrokerLoginFlowAlias = dict(type='str', default="first broker login"),
            config = dict(type='dict'),
            mappers = dict(type='list', default=[]),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    
    
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force'])
    
    result = idp(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def idp(params):
    url = params['url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    state = params['state']
    force = params['force']
    rc = 0
    result = dict()
    changed = False
    idPExists = False
    # Créer un représentation du realm recu en paramètres
    newIdPRepresentation = {}
    if 'alias' in params and params['alias'] is not None and len(params['alias']) > 0:
        newIdPRepresentation["alias"] = params['alias'].decode("utf-8")
        queryParams = {'alias': params['alias'].decode("utf-8")}
    else:
        #if 'config' in params and 'clientId' in params['config']:
        #    queryParams = {'clientId': params['config']['clientId'].decode("utf-8")}
        #else:
        result = dict(
            stderr   = 'Alias must be provided',
            rc       = 1,
            changed  = changed
            )
        return result
    if 'displayName' in params:
        newIdPRepresentation["displayName"] = params['displayName'].decode("utf-8")
    if 'providerId' in params:
        newIdPRepresentation["providerId"] = params['providerId'].decode("utf-8")
    if 'enabled' in params:
        newIdPRepresentation["enabled"] = params['enabled']
    if 'updateProfileFirstLoginMode' in params:
        newIdPRepresentation["updateProfileFirstLoginMode"] = params['updateProfileFirstLoginMode'].decode("utf-8")
    if 'trustEmail' in params:
        newIdPRepresentation["trustEmail"] = params['trustEmail']
    if 'storeToken' in params:
        newIdPRepresentation["storeToken"] = params['storeToken']
    if 'addReadTokenRoleOnCreate' in params:
        newIdPRepresentation["addReadTokenRoleOnCreate"] = params['addReadTokenRoleOnCreate']
    if 'authenticateByDefault' in params:
        newIdPRepresentation["authenticateByDefault"] = params['authenticateByDefault']
    if 'linkOnly' in params:
        newIdPRepresentation["linkOnly"] = params['linkOnly']
    if 'firstBrokerLoginFlowAlias' in params:
        newIdPRepresentation["firstBrokerLoginFlowAlias"] = params['firstBrokerLoginFlowAlias'].decode("utf-8")
     
    if 'config' in params:
        #newIdPConfig = params['config']
        newIdPConfig = {}  
        if "hideOnLoginPage" in params["config"]:
            newIdPConfig["hideOnLoginPage"] = params["config"]["hideOnLoginPage"]
        if "userInfoUrl" in params["config"]:
            newIdPConfig["userInfoUrl"] = params["config"]["userInfoUrl"] 
        if "validateSignature" in params["config"]:
            newIdPConfig["validateSignature"] = params["config"]["validateSignature"]
        if "clientId" in params["config"]:
            newIdPConfig["clientId"] = params["config"]["clientId"]
        if "tokenUrl" in params["config"]:
            newIdPConfig["tokenUrl"] = params["config"]["tokenUrl"]
        if "jwksUrl" in params["config"]:
            newIdPConfig["jwksUrl"] = params["config"]["jwksUrl"]
        if "issuer" in params["config"]:
            newIdPConfig["issuer"] = params["config"]["issuer"]
        if "useJwksUrl" in params["config"]:
            newIdPConfig["useJwksUrl"] = params["config"]["useJwksUrl"]
        if "authorizationUrl" in params["config"]:
            newIdPConfig["authorizationUrl"] = params["config"]["authorizationUrl"]
        if "disableUserInfo" in params["config"]:
             newIdPConfig["disableUserInfo"] = params["config"]["disableUserInfo"]
        if "clientSecret" in params["config"]:
            newIdPConfig["clientSecret"] = params["config"]["clientSecret"]
        if "defaultScope" in params["config"]:
            newIdPConfig["defaultScope"] = params["config"]["defaultScope"]
    
    if 'providerId' in newIdPRepresentation and newIdPRepresentation["providerId"] == 'google' and 'userIp' in params["config"]:
        newIdPConfig["userIp"] = params["config"]["userIp"]
    newIdPMappers = params['mappers'] if 'mappers' in params else None
    
    idPSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/identity-provider/instances/"
    
    #print str(newIdPRepresentation)

    try:
        #accessToken = login(url, username, password)
        #bearerHeader = "bearer " + accessToken
        headers = loginAndSetHeaders(url, username, password)
    except Exception, e:
        result = dict(
            stderr   = 'login: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
    try:
        if 'openIdConfigurationUrl' in params['config']:
            addIdPEndpoints(newIdPConfig, params["config"]['openIdConfigurationUrl'])
        
        newIdPRepresentation["config"] = newIdPConfig
    except Exception, e:
        result = dict(
            stderr   = 'addIdPEndpoints: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result

    try: 
        # Vérifier si le IdP existe sur le serveur Keycloak
        getResponse = requests.get(idPSvcBaseUrl, headers=headers)
        listIdPs = getResponse.json()
        
        for idP in listIdPs:
            if ('alias' in queryParams and idP['alias'] == queryParams['alias']) or ('clientId' in queryParams and idP['config']['clientId'] == queryParams['clientId']):
                idPExists = True
                # Obtenir le IdP exitant
                idPRepresentation = idP
                break
                
        #print str(queryParams)
        #print str(getResponse.json())
    except Exception, e:
        result = dict(
            stderr   = 'first realm get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    
   
    if not idPExists: # Le IdP n'existe pas
        # Creer le IdP
        if not 'alias' in newIdPRepresentation:
            result = dict(
                stderr   = 'No Alias provided while creating a new Identity Provider or updating a non existing identity provider',
                rc       = 1,
                changed  = changed
                )
            return result
        idPSvcUrl = idPSvcBaseUrl + newIdPRepresentation['alias']
        if (state == 'present'): # Si le status est présent
            try:
                # Stocker le IdP dans un body prêt a être posté
                data=json.dumps(newIdPRepresentation)
                # Créer le IdP
                postResponse = requests.post(idPSvcBaseUrl, headers=headers, data=data)
                # S'il y a des mappers de définis pour l'IdP
                if newIdPMappers is not None and len(newIdPMappers) > 0:
                    createOrUpdateMappers(idPSvcUrl, headers, newIdPRepresentation["alias"], newIdPMappers)
                # Obtenir le nouvel IdP créé
                getResponse = requests.get(idPSvcUrl, headers=headers)
                changed = True
                idPRepresentation = getResponse.json()
                
                getResponse = requests.get(idPSvcUrl + "/mappers", headers=headers)
                try:
                    mappersRepresentation = getResponse.json()
                except ValueError:
                    mappersRepresentation = {}
                
                fact = dict(
                    idp = idPRepresentation,
                    mappers = mappersRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                fact = dict(
                    idp = newIdPRepresentation)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post idp: ' + newIdPRepresentation["alias"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                fact = dict(
                    idp = newIdPRepresentation)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post idp: ' + newIdPRepresentation["alias"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        else: # Sinon, le status est absent
            result = dict(
                stdout   = newIdPRepresentation["alias"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # Le realm existe déjà
        alias = idPRepresentation['alias']
        idPSvcUrl = idPSvcBaseUrl + alias
        try:
            if (state == 'present'): # si le status est présent
                
                if force: # Si l'option force est sélectionné
                    # Supprimer les mappings existants
                    deleteAllMappers(idPSvcUrl, bearerHeader)
                    # Supprimer le IdP existant
                    deleteResponse = requests.delete(idPSvcUrl, headers=headers)
                    changed = True
                    # Stocker le IdP dans un body prêt a être posté
                    data=json.dumps(newIdPRepresentation)
                    # Créer le nouveau IdP
                    postResponse = requests.post(idPSvcBaseUrl, headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    # Comparer les realms
                    if (isDictEquals(newIdPRepresentation, idPRepresentation, ["clientSecret", "openIdConfigurationUrl", "mappers"])): # Si le nouveau IdP n'introduit pas de modification au IdP existant
                        # Ne rien changer
                        changed = False
                    else: # Si le IdP doit être modifié
                        # Stocker le IdP dans un body prêt a être posté
                        data=json.dumps(newIdPRepresentation)
                        # Mettre à jour le IdP sur le serveur Keycloak
                        updateResponse = requests.put(idPSvcUrl, headers=headers, data=data)
                        changed = True
                if changed and newIdPMappers is not None and len(newIdPMappers) > 0:
                    createOrUpdateMappers(idPSvcUrl, headers, alias, newIdPMappers)
        
                # Obtenir sa représentation JSON sur le serveur Keycloak                        
                getResponse = requests.get(idPSvcUrl, headers=headers)
                idPRepresentation = getResponse.json()
                
                getResponse = requests.get(idPSvcUrl + "/mappers", headers=headers)
                try:
                    mappersRepresentation = getResponse.json()
                except ValueError:
                    mappersRepresentation = {}
                
                fact = dict(
                    idp = idPRepresentation,
                    mappers = mappersRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            else: # Le status est absent
                # Supprimer le IdP
                deleteResponse = requests.delete(idPSvcUrl, headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                stderr   = 'put or delete idp: ' + str(newIdPRepresentation) + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                stderr   = 'put or delete idp: ' + str(newIdPRepresentation) + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    
    return result
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
