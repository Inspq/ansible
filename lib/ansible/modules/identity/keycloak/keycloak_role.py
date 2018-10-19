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
module: keycloak_role
short_description: Configure a role in Keycloak
description:
    - This module creates, removes or update Keycloak realm level role.
    - For client level role, use keycloak_client module.
version_added: "2.3"
options:
    url:
        description:
            - The url of the Keycloak server.
        default: http://localhost:8080    
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
            - The name of the realm in which is the role.
        required: true
    name:
        description:
            - Name for the realm level role.
        required: true
    description:
        description:
            - Description of the role.
        required: false
    composite:
        description:
            - If true, the role is a composition of other realm and/or client role.
        default: false
        required: false
    clientRole:
        description: 
            - This parameter indicate if the role is a client role.
            - For a ream role, this parameter must be false.
        default: false
        required: false
    containerId:
        description:
            - Id for the container of the role. For a realm role, it must be the realm name
        default: "{{ realm }}"
        required: false
    composites:
        description:
            - List of roles to include to the composite realm role.
            - If the composite role is a client role, the clientId (not id of the client) must be specified.
        required: false
    state:
        description:
            - Control if the role must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        choices: [ "yes", "no" ]
        default: "no"
        description:
            - If yes, allows to remove role and recreate it.
        required: false
notes:
    - module does not modify roleId.
'''

EXAMPLES = '''
    - name: Create the composite realm role role1 with composite roles.
      keycloak_role:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        name: role1
        description: Super composite role
        composite: true
        composites:
          - clientName: realm-management
            name: "manage-clients"
          - name: uma_authorization
        state: present

    - name: Re-create realm role role1
      keycloak_role:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        name: role1
        description: Super composite role
        composite: true
        composites:
          - clientId: realm-management
            name: "manage-clients"
          - name: uma_authorization
        state: present
        force: yes

    - name: Remove realm role role1.
      keycloak_role:
        url: http://localhost:8080
        username: admin
        password: admin
        realm: master
        name: role1
        state: absent
'''

RETURN = '''
ansible_facts:
  description: JSON representation for the role.
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
  description: Return True if the operation changed the role on the keycloak server, false otherwise.
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
            name=dict(type='str', required=True),
            description = dict(type='str', default=None),
            # scopeParamRequired=dict(type='bool', default=False),
            composite=dict(type='bool',default=False),
            clientRole = dict(type='bool',default=False),
            containerId = dict(type='str', required=False),
            composites = dict(type='list', default=[]),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force']) if "force" in module.params else False
    
    result = role(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def role(params):
    url = params['url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    state = params['state']
    force = params['force'] if "force" in params else False
    newComposites = None
    roleRepresentation = None
    
    # Créer un représentation du role recu en paramètres
    newRoleRepresentation = {}
    newRoleRepresentation["name"] = params['name'].decode("utf-8")
    if params['description'] is not None:
        newRoleRepresentation["description"] = params['description'].decode("utf-8")
    # newRoleRepresentation["scopeParamRequired"] = params["scopeParamRequired"] if "scopeParamRequired" in params else False 
    newRoleRepresentation["composite"] = params['composite'] if "composite" in params else False
    newRoleRepresentation["clientRole"] = params['clientRole'] if "clientRole" in params else False
    newRoleRepresentation["containerId"] = params['containerId'].decode("utf-8") if "containerId" in params and params['containerId'] is not None else realm
    if 'composites' in params and params['composites'] is not None:
        newComposites = params['composites']
    
    roleSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/roles/"
    clientSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/clients/"
    
    rc = 0
    result = dict()
    changed = False

    if username == 'admin':
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
        # Vérifier si le role existe sur le serveur Keycloak
        getResponse = requests.get(roleSvcBaseUrl + newRoleRepresentation["name"], headers=headers)
        if getResponse.status_code != 404:
            roleRepresentation = getResponse.json()
    except Exception, e:
        result = dict(
            stderr   = 'first role get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    if roleRepresentation is None: # Le role n'existe pas
        # Creer le role
        
        if (state == 'present'): # Si le status est présent
            try:
                # Stocker le role dans un body prêt a être posté
                data=json.dumps(newRoleRepresentation)
                # Créer le role
                requests.post(roleSvcBaseUrl, headers=headers, data=data)
                # Obtenir le nouveau role créé
                getResponse = requests.get(roleSvcBaseUrl + newRoleRepresentation["name"], headers=headers)
                if getResponse.status_code == 404:
                    raise Exception("Role just created not found: " + str(newRoleRepresentation))
                roleRepresentation = getResponse.json()
                # Créer assigner les roles composites
                createOrUpdateComposites(newComposites,newRoleRepresentation, roleSvcBaseUrl, clientSvcBaseUrl, headers)                # Obtenir les composites pour le role
                # Obtenir la dernière version du nouveau role
                getResponse = requests.get(roleSvcBaseUrl + newRoleRepresentation["name"], headers=headers)
                if getResponse.status_code == 404:
                    raise Exception("Role just created not found: " + str(newRoleRepresentation))
                roleRepresentation = getResponse.json()
                # Obtenir les composites du rôle
                getResponse = requests.get(roleSvcBaseUrl + newRoleRepresentation["name"] + '/composites', headers=headers)
                composites = getResponse.json()
                changed = True
                fact = dict(
                    role = roleRepresentation,
                    composites = composites)
                
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                fact = dict(
                    role = newRoleRepresentation)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post role: ' + newRoleRepresentation["name"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                fact = dict(
                    role = newRoleRepresentation)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post role: ' + newRoleRepresentation["name"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        elif state == 'absent': # Sinon, le status est absent
            result = dict(
                stdout   = newRoleRepresentation["name"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # Le role existe déjà
        try:
            if (state == 'present'): # si le status est présent
                if force: # Si l'option force est sélectionné
                    # Supprimer le role existant
                    requests.delete(roleSvcBaseUrl + roleRepresentation["id"], headers=headers)
                    changed = True
                    # Stocker le role dans un body prêt a être posté
                    data=json.dumps(newRoleRepresentation)
                    # Créer à nouveau le role
                    requests.post(roleSvcBaseUrl, headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    # Comparer les roles
                    if not (isDictEquals(newRoleRepresentation, roleRepresentation)): # Si le nouveau role introduit des modifications aux roles existants
                        # Stocker le role dans un body prêt a être posté
                        data=json.dumps(newRoleRepresentation)
                        # Mettre à jour le role sur le serveur Keycloak
                        requests.put(roleSvcBaseUrl + roleRepresentation["name"], headers=headers, data=data)
                        changed = True
                # Obtenir le nouveau role créé
                getResponse = requests.get(roleSvcBaseUrl + newRoleRepresentation["name"], headers=headers)
                roleRepresentation = getResponse.json()
                # Traiter les rôles composite
                if createOrUpdateComposites(newComposites,newRoleRepresentation, roleSvcBaseUrl, clientSvcBaseUrl, headers):
                    changed = True
                # Obtenir la dernière version du nouveau role
                getResponse = requests.get(roleSvcBaseUrl + newRoleRepresentation["name"], headers=headers)
                if getResponse.status_code == 404:
                    raise Exception("Role just created not found: " + str(newRoleRepresentation))
                roleRepresentation = getResponse.json()
                # Obtenir les composites du rôle
                getResponse = requests.get(roleSvcBaseUrl + newRoleRepresentation["name"] + '/composites', headers=headers)
                composites = getResponse.json()

                fact = dict(
                    role = roleRepresentation,
                    composites = composites)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            elif state == 'absent': # Le status est absent
                # Supprimer le role
                requests.delete(roleSvcBaseUrl + roleRepresentation['name'], headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                stderr   = 'put or delete role: ' + newRoleRepresentation['name'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                stderr   = 'put or delete role: ' + newRoleRepresentation['name'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    return result

def createOrUpdateComposites(newComposites,newRoleRepresentation, roleSvcBaseUrl, clientSvcBaseUrl, headers):
    changed = False
    newCompositesToCreate = []
    try:
        getResponse = requests.get(roleSvcBaseUrl + newRoleRepresentation["name"] + '/composites', headers=headers)
        existingComposites = getResponse.json()
        if existingComposites is None:
            existingComposites = []
        for existingComposite in existingComposites:
            newCompositesToCreate.append(existingComposite)
        # Créer assigner les roles composites
    #    if newComposites is not None and newRoleRepresentation["composite"]:
        if newComposites is not None and newRoleRepresentation["composite"]:
            for newComposite in newComposites:
                newCompositeFound = False
                # Rechercher le composite à assigner au rôle dans le rôle en place sur le serveur
                for composite in existingComposites:
                    if composite["clientRole"] and "clientId" in newComposite:
                        getResponse = requests.get(clientSvcBaseUrl + composite["containerId"], headers=headers)
                        clientId = getResponse.json()["clientId"]
                        if composite["name"] == newComposite["name"] and clientId == newComposite["clientId"]:
                            newCompositeFound = True
                            break
                    elif composite["name"] == newComposite["name"]:
                        newCompositeFound = True
                        break
                # Si le role n'est pas déjà assigné au role composite car in n'a pas été trouvé
                if not newCompositeFound:
                    roles = []
                    # Si le composite est de type role client
                    if "clientId" in newComposite:
                        # Obtenir id de ce client
                        client = None
                        getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': newComposite["clientId"]})
                        for client in getResponse.json():
                            if client["clientId"] == newComposite["clientId"]:
                                break
                        if client is not None:
                            # Obtenir les rôles de ce client
                            getResponse = requests.get(clientSvcBaseUrl + client["id"] + "/roles", headers=headers)
                            roles = getResponse.json()
                    else: # Sinon, on assume que le rôle a mettre dans le composite en est un de realm
                        # Obtenir la liste des rôles du realm
                        getResponse = requests.get(roleSvcBaseUrl, headers=headers)
                        roles = getResponse.json()
                    # Rechercher le rôle correspondant à celui à assigner
                    for role in roles:                   
                        # Si le rôle est trouvé
                        if role["name"] == newComposite["name"]:
                            newCompositesToCreate.append(role)
                            changed = True
        if changed:
            # Delete existing composites
            #if len(existingComposites) > 0:
            #    data=json.dumps(existingComposites)
            #    requests.delete(roleSvcBaseUrl + newRoleRepresentation["name"] + '/composites', headers=headers, data=data)
            # Create all composites
            data=json.dumps(newCompositesToCreate)
            requests.post(roleSvcBaseUrl + newRoleRepresentation["name"] + '/composites', headers=headers, data=data)
    except requests.exceptions.RequestException, e:
        raise e
    except ValueError, e:
        raise e
    return changed
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
