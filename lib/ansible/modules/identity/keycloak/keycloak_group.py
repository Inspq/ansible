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
            - This parameter does not change the group configuration actually.
        required: false
    clientRoles:
        description:
            - Key/[values] pairs for client roles to assign to group.
            - This parameter does not change the group configuration actually.
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
          realm-management:
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
            clientRoles=dict(type='dict'),
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
        newGroupRepresentation["clientRoles"] = params['clientRoles']
    
    groupSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/groups/"
    
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
                # Obtenir la nouvelle représentation du groupe
                getResponse = requests.get(groupSvcBaseUrl + groupRepresentation["id"], headers=headers)
                groupRepresentation = getResponse.json()
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
                    # Stocker le group dans un body prêt a être posté
                    data=json.dumps(newGroupRepresentation)
                    # Créer à nouveau le group
                    postResponse = requests.post(groupSvcBaseUrl, headers=headers, data=data)
                    # Rechercher le nouveau groupe qui vient d'être créé pour obtenir son ID
                    getResponse = requests.get(groupSvcBaseUrl, headers=headers)
                    for group in getResponse.json():
                        if group["name"] == newGroupRepresentation["name"]:
                            groupRepresentation = group
                            break
                    # If the group still not exist on the server, raise an exception.
                    if groupRepresentation is None:
                        raise Exception("Group just created not found: " + str(newGroupRepresentation))
                else: # Si l'option force n'est pas sélectionné
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
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
