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
module: keycloak_group
short_description: Configure a group in Keycloak
description:
    - This module creates, removes or update Keycloak groups.
    - The module does not support sub-groups (childrens) yet.
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
            - The name of the realm in which is the group.
        required: true
    name:
        description:
            - Name for the group.
        required: true
    path:
        description:
            - Path of the group.
        required: false
        default: "/{{ name }}"
    attributes:
        description:
            - Key/[values] pairs for the group attributes.
            - To delete all the attribute use an empty dict ({})
        required: false
    realmRoles:
        description:
            - Array of realm roles to assign to the group.
        required: false
    clientRoles:
        description:
            - Array of client roles to assign to group.
        required: false
    state:
        description:
            - Control if the group must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        choices: [ "yes", "no" ]
        default: "no"
        description:
            - If yes, allows to remove group and recreate it.
        required: false
notes:
    - module does not modify groupId.
'''

EXAMPLES = '''
    - name: Create the composite realm group group1 with composite groups.
      keycloak_group:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        name: group1
        attributes:
          attr1: 
            - value1
          attr2: 
            - value2
        realmRoles:
          - uma_authorization
        clientRoles:
          - clientid: realm-management
            roles:
              - manage-clients
              - manage-users
        state: present

    - name: Re-create group group1
      keycloak_group:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        name: group1
        attributes:
          attr1: 
            - value1
          attr2: 
            - value2
        state: present
        force: yes

    - name: Remove group group1.
      keycloak_group:
        url: http://localhost:8080
        username: admin
        password: admin
        realm: master
        name: group1
        state: absent
'''

RETURN = '''
ansible_facts:
  description: JSON representation for the group.
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
  description: Return True if the operation changed the group on the keycloak server, false otherwise.
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
            path = dict(type='str'),
            attributes=dict(type='dict'),
            realmRoles=dict(type='list'),
            clientRoles=dict(type='list'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force']) if "force" in module.params else False
    
    result = group(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def group(params):
    url = params['url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    state = params['state'] if "state" in params else "present"
    force = params['force'] if "force" in params else False
    newComposites = None
    groupRepresentation = None
    
    # Créer un représentation du group recu en paramètres
    newGroupRepresentation = {}
    newGroupRepresentation["name"] = params['name'].decode("utf-8")
    newGroupRepresentation["path"] = params['path'].decode("utf-8") if "path" in params and params['path'] is not None else "/" + newGroupRepresentation["name"]
    if 'attributes' in params and params['attributes'] is not None:
        newGroupRepresentation["attributes"] = params['attributes']
    if 'realmRoles' in params and params['realmRoles'] is not None:
        newGroupRepresentation["realmRoles"] = params['realmRoles']
    if 'clientRoles' in params and params['clientRoles'] is not None:
        newGroupRepresentation["clientRoles"] = ansible2keycloakClientRoles(params['clientRoles'])
    
    #f = open('/tmp/ansible_debug.log', 'a')
    #f.write(str(newGroupRepresentation))
    
    groupSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/groups/"
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
        groupRepresentation = None 
        # Vérifier si le group existe sur le serveur Keycloak
        getResponse = requests.get(groupSvcBaseUrl, headers=headers)
        for group in getResponse.json():
            if group["name"] == newGroupRepresentation["name"]:
                groupRepresentation = group
                break
    except Exception, e:
        result = dict(
            stderr   = 'first group get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    if groupRepresentation is None: # Le group n'existe pas
        # Creer le group
        
        if (state == 'present'): # Si le status est présent
            try:
                # Keep realm roles in a variable and remove them from representation
                groupRealmRoles = []
                if "realmRoles" in newGroupRepresentation:
                    groupRealmRoles = newGroupRepresentation["realmRoles"]
                    newGroupRepresentation["realmRoles"] = []
                # Keep realm roles in a variable and remove them from representation
                groupClientRoles = {}
                if "clientRoles" in newGroupRepresentation:
                    groupClientRoles = newGroupRepresentation["clientRoles"]
                    newGroupRepresentation["clientRoles"] = {}
                # Stocker le group dans un body prêt a être posté
                data=json.dumps(newGroupRepresentation)
                # Créer le group
                postResponse = requests.post(groupSvcBaseUrl, headers=headers, data=data)

                # Rechercher le nouveau groupe qui vient d'être créé
                getResponse = requests.get(groupSvcBaseUrl, headers=headers)
                for group in getResponse.json():
                    if group["name"] == newGroupRepresentation["name"]:
                        groupRepresentation = group
                        break
                # If the group still not exist on the server, raise an exception.
                if groupRepresentation is None:
                    raise Exception("Group just created not found: " + str(newGroupRepresentation))
                # Get new role representation without group
                getResponse = requests.get(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
                groupRepresentation = getResponse.json()
                # Assing roles to group
                assingRolestoGroup(headers, groupRepresentation, groupRealmRoles, groupClientRoles, groupSvcBaseUrl, roleSvcBaseUrl, clientSvcBaseUrl)
                # Get final group representation with roles
                getResponse = requests.get(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
                groupRepresentation = getResponse.json()

                if "clientRoles" in groupRepresentation:
                    tmpClientRoles = groupRepresentation["clientRoles"]
                    groupRepresentation["clientRoles"] = keycloak2ansibleClientRoles(tmpClientRoles)
                changed = True
                fact = dict(
                    group = groupRepresentation)                
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                fact = dict(
                    group = newGroupRepresentation)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post group: ' + newGroupRepresentation["name"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                fact = dict(
                    group = newGroupRepresentation)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post group: ' + newGroupRepresentation["name"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        elif state == 'absent': # Sinon, le status est absent
            result = dict(
                stdout   = newGroupRepresentation["name"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # Le group existe déjà
        try:
            # Obtenir les détails du group a modifier
            getResponse = requests.get(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
            groupRepresentation = getResponse.json()
            if (state == 'present'): # si le status est présent
                if force: # Si l'option force est sélectionné
                    # Supprimer le group existant
                    deleteResponse = requests.delete(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
                    changed = True
                    # Keep realm roles in a variable and remove them from representation
                    groupRealmRoles = []
                    if "realmRoles" in newGroupRepresentation:
                        groupRealmRoles = newGroupRepresentation["realmRoles"]
                        newGroupRepresentation["realmRoles"] = []
                    # Keep realm roles in a variable and remove them from representation
                    groupClientRoles = {}
                    if "clientRoles" in newGroupRepresentation:
                        groupClientRoles = newGroupRepresentation["clientRoles"]
                        newGroupRepresentation["clientRoles"] = {}
                    # Stocker le group dans un body prêt a être posté
                    data=json.dumps(newGroupRepresentation)
                    # Créer le group
                    postResponse = requests.post(groupSvcBaseUrl, headers=headers, data=data)
    
                    # Rechercher le nouveau groupe qui vient d'être créé
                    getResponse = requests.get(groupSvcBaseUrl, headers=headers)
                    for group in getResponse.json():
                        if group["name"] == newGroupRepresentation["name"]:
                            groupRepresentation = group
                            break
                    # If the group still not exist on the server, raise an exception.
                    if groupRepresentation is None:
                        raise Exception("Group just created not found: " + str(newGroupRepresentation))
                    # Get new role representation without group
                    getResponse = requests.get(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
                    groupRepresentation = getResponse.json()
                    # Assing roles to group
                    assingRolestoGroup(headers, groupRepresentation, groupRealmRoles, groupClientRoles, groupSvcBaseUrl, roleSvcBaseUrl, clientSvcBaseUrl)
                    # Get final group representation with roles
                    getResponse = requests.get(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
                    groupRepresentation = getResponse.json()
    
                    if "clientRoles" in groupRepresentation:
                        tmpClientRoles = groupRepresentation["clientRoles"]
                        groupRepresentation["clientRoles"] = keycloak2ansibleClientRoles(tmpClientRoles)
                    changed = True
                    fact = dict(
                        group = groupRepresentation)                
                    result = dict(
                        ansible_facts = fact,
                        rc = 0,
                        changed = changed
                        )
                else: # Si l'option force n'est pas sélectionné
                    # Keep realm roles in a variable and remove them from representation
                    groupRealmRoles = []
                    if "realmRoles" in newGroupRepresentation:
                        groupRealmRoles = newGroupRepresentation["realmRoles"]
                        newGroupRepresentation["realmRoles"] = []
                    # Keep realm roles in a variable and remove them from representation
                    groupClientRoles = {}
                    if "clientRoles" in newGroupRepresentation:
                        groupClientRoles = newGroupRepresentation["clientRoles"]
                        newGroupRepresentation["clientRoles"] = {}
                    # Comparer les groups
                    excludes = ["realmRoles","clientRoles"]
                    if not (isDictEquals(newGroupRepresentation, groupRepresentation, excludes)): # Si le nouveau group introduit des modifications aux groups existants
                        # Stocker le group dans un body prêt a être posté
                        data=json.dumps(newGroupRepresentation)
                        # Mettre à jour le group sur le serveur Keycloak
                        updateResponse = requests.put(groupSvcBaseUrl + groupRepresentation["id"], headers=headers, data=data)
                        changed = True
                # Obtenir la nouvelle représentation du groupe
                getResponse = requests.get(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
                groupRepresentation = getResponse.json()
                # Assing roles to group
                if assingRolestoGroup(headers, groupRepresentation, groupRealmRoles, groupClientRoles, groupSvcBaseUrl, roleSvcBaseUrl, clientSvcBaseUrl):
                    changed = True
                # Get final group representation with roles
                getResponse = requests.get(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
                groupRepresentation = getResponse.json()
                if "clientRoles" in groupRepresentation:
                    tmpClientRoles = groupRepresentation["clientRoles"]
                    groupRepresentation["clientRoles"] = keycloak2ansibleClientRoles(tmpClientRoles)

                fact = dict(
                    group = groupRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            elif state == 'absent': # Le status est absent
                # Supprimer le group
                deleteResponse = requests.delete(groupSvcBaseUrl + groupRepresentation['id'], headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                stderr   = 'put or delete group: ' + newGroupRepresentation['name'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                stderr   = 'put or delete group: ' + newGroupRepresentation['name'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    return result

def assingRolestoGroup(headers, groupRepresentation, groupRealmRoles, groupClientRoles, groupSvcBaseUrl, roleSvcBaseUrl, clientSvcBaseUrl):
    changed = False
    # Assing Realm Roles
    realmRolesRepresentation = []
    for realmRole in groupRealmRoles:
        # Look for existing role into group representation
        if not realmRole in groupRepresentation["realmRoles"]:
            roleid = None
            # Get all realm roles
            getResponse = requests.get(roleSvcBaseUrl, headers=headers)
            # Find the role id
            for role in getResponse.json():
                if role["name"] == realmRole:
                    roleid = role["id"]
                    break
            if roleid is not None:
                realmRoleRepresentation = {}
                realmRoleRepresentation["id"] = roleid
                realmRoleRepresentation["name"] = realmRole
                realmRolesRepresentation.append(realmRoleRepresentation)
    if len(realmRolesRepresentation) > 0 :
        data=json.dumps(realmRolesRepresentation)
        # Assing Role
        postResp = requests.post(groupSvcBaseUrl + groupRepresentation["id"] + "/role-mappings/realm", headers=headers, data=data)
        changed = True
    # Assing clients roles            
    for clientToAssingRole in groupClientRoles.keys():
        # Get the client id
        getResponse = requests.get(clientSvcBaseUrl, headers=headers, params={'clientId': clientToAssingRole})
        if len(getResponse.json()) > 0 and "id" in getResponse.json()[0]:
            clientId = getResponse.json()[0]["id"]
            # Get the client roles
            getResponse = requests.get(clientSvcBaseUrl + clientId + '/roles', headers=headers)
            clientRoles = getResponse.json()
            if not clientToAssingRole in groupRepresentation["clientRoles"].keys() or not isDictEquals(groupRepresentation["clientRoles"][clientToAssingRole], groupClientRoles[clientToAssingRole]):
                rolesToAssing = []
                for roleToAssing in groupClientRoles[clientToAssingRole]:
                    newRole = {}
                    # Find his Id
                    for clientRole in clientRoles:
                        if clientRole["name"] == roleToAssing:
                            newRole["id"] = clientRole["id"]
                            newRole["name"] = roleToAssing
                            rolesToAssing.append(newRole)
                if len(rolesToAssing) > 0:
                    # Delete exiting client Roles
                    requests.delete(groupSvcBaseUrl + groupRepresentation["id"] + "/role-mappings/clients/" + clientId, headers=headers)
                    data=json.dumps(rolesToAssing)
                    # Assing Role
                    requests.post(groupSvcBaseUrl + groupRepresentation["id"] + "/role-mappings/clients/" + clientId, headers=headers, data=data)
                    changed = True
            
    return changed             

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
