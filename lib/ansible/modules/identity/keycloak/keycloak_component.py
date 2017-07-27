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
module: keycloak_component
short_description: Configure a component in Keycloak
description:
    - This module creates, removes or update Keycloak component.
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
            - The name of the realm in which is the component.
        required: true
    id:
        description:
            - ID of the component when it have already been created and it is known.
        required: false
    name:
        description:
            - Name of the Component
        required: true
    providerId:
        description:
            - ProviderId of the component
        choices: ["ldap","allowed-client-templates","trusted-hosts","allowed-protocol-mappers","max-clients","scope","consent-required","rsa-generated"]
        required: true
    providerType:
        description:
            - Provider type of component
        choices:
            - org.keycloak.storage.UserStorageProvider
            - org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy
            - org.keycloak.keys.KeyProvider
            - authenticatorConfig
            - requiredActions
        required: true
    parentId:
        description:
            - Parent ID of the component. Use the realm name for top level component.
        required: true
    config:
        description:
            - Configuration of the component to create, update or delete.
        required: false
    state:
        description:
            - Control if the component must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        choices: [ "yes", "no" ]
        default: "no"
        description:
            - If yes, allows to remove component and recreate it.
        required: false
'''

EXAMPLES = '''
    - name: Create a LDAP User Storage provider.
      keycloak_component:
        url: http://localhost:8080
        username: admin
        password: admin
        realm: master
        name: ActiveDirectory
        providerId: ldap
        providerType: org.keycloak.storage.UserStorageProvider
        config:
          vendor:
          - "ad"
          usernameLDAPAttribute:
          - "sAMAccountName"
          rdnLDAPAttribute:
          - "cn"
          uuidLDAPAttribute:
          - "objectGUID"
          userObjectClasses:
          - "person"
          - "organizationalPerson"
          - "user"
          connectionUrl:
          - "ldap://ldap.server.com:389"
          usersDn:
          - "OU=USERS,DC=server,DC=com"
          authType: 
          - "simple"
          bindDn:
          - "CN=keycloak,OU=USERS,DC=server,DC=com"
          bindCredential:
          - "UnTresLongMotDePasseQuePersonneNeConnait"
          changedSyncPeriod:
          - "86400"
          fullSyncPeriod:
          - "604800"  
        state: present

    - name: Re-create LDAP User Storage provider.
      keycloak_component:
        url: http://localhost:8080
        username: admin
        password: admin
        realm: master
        name: ActiveDirectory
        providerId: ldap
        providerType: org.keycloak.storage.UserStorageProvider
        config:
          vendor:
          - "ad"
          usernameLDAPAttribute:
          - "sAMAccountName"
          rdnLDAPAttribute:
          - "cn"
          uuidLDAPAttribute:
          - "objectGUID"
          userObjectClasses:
          - "person"
          - "organizationalPerson"
          - "user"
          connectionUrl:
          - "ldap://ldap.server.com:389"
          usersDn:
          - "OU=USERS,DC=server,DC=com"
          authType: 
          - "simple"
          bindDn:
          - "CN=keycloak,OU=USERS,DC=server,DC=com"
          bindCredential:
          - "UnTresLongMotDePasseQuePersonneNeConnait"
          changedSyncPeriod:
          - "86400"
          fullSyncPeriod:
          - "604800"  

        state: present
        force: yes
        
    - name: Remove User Storage Provider.
      keycloak_component:
        url: http://localhost:8080
        username: admin
        password: admin
        realm: master
        name: ActiveDirectory
        providerId: ldap
        providerType: org.keycloak.storage.UserStorageProvider
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
            id=dict(type='str'),
            name=dict(type='str', required=True),
            providerId=dict(choices=["ldap","allowed-client-templates","trusted-hosts","allowed-protocol-mappers","max-clients","scope","consent-required","rsa-generated"], required=True),
            providerType=dict(choices=["org.keycloak.storage.UserStorageProvider", "org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy","org.keycloak.keys.KeyProvider","authenticatorConfig","requiredActions"], required=True),
            parentId=dict(type='str', required=True),
            config=dict(type='dict'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force'])
    
    result = component(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def component(params):
    url = params['url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    state = params['state']
    force = params['force']

    # Créer un représentation du component recu en paramètres
    newComponent = {}
    if "id" in params and params["id"] is not None:
        newComponent["id"] = params['id'].decode("utf-8")
    if "name" in params and params["name"] is not None:
        newComponent["name"] = params['name'].decode("utf-8")
    if "providerId" in params and params["providerId"] is not None:
        newComponent["providerId"] = params['providerId'].decode("utf-8")
    if "providerType" in params and params["providerType"] is not None:
        newComponent["providerType"] = params['providerType'].decode("utf-8")
    if "parentId" in params and params["parentId"] is not None:
        newComponent["parentId"] = params['parentId'].decode("utf-8")
    if "config" in params:
        newComponent["config"] = params["config"]
    
    componentSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/components/"
    
    rc = 0
    result = dict()
    changed = False
    component = None
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
        getResponse = requests.get(componentSvcBaseUrl, headers=headers, params={"name": newComponent["name"],"type": newComponent["providerType"], "parent": newComponent["parentId"]})
        for item in getResponse.json():
            if "providerId" in item and item["providerId"] == newComponent["providerId"]:
                component = item
                break
    except Exception, e:
        result = dict(
            stderr   = 'first client get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    if component is None: # Le composant n'existe pas
        # Creer le client
        
        if (state == 'present'): # Si le status est présent
            try:
                # Stocker le client dans un body prêt a être posté
                data=json.dumps(newComponent)
                # Créer le client
                postResponse = requests.post(componentSvcBaseUrl, headers=headers, data=data)
                # Obtenir le nouveau composant créé
                getResponse = requests.get(componentSvcBaseUrl, headers=headers, params={"name": newComponent["name"],"type": newComponent["providerType"], "parent": newComponent["parentId"]})
                for item in getResponse.json():
                    if "providerId" in item and item["providerId"] == newComponent["providerId"]:
                        component = item
                        break
                changed = True
                fact = dict(
                    component = component
                    )
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                fact = dict(
                    component = newComponent)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post component: ' + newComponent["name"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                fact = dict(
                    component = newComponent)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post component: ' + newComponent["name"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        elif state == 'absent': # Sinon, le status est absent
            result = dict(
                stdout   = newComponent["name"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # Le component existe déjà
        try:
            if (state == 'present'): # si le status est présent
                if force: # Si l'option force est sélectionné
                    # Supprimer le client existant
                    deleteResponse = requests.delete(componentSvcBaseUrl + component["id"], headers=headers)
                    changed = True
                    # Stocker le client dans un body prêt a être posté
                    data=json.dumps(newComponent)
                    # Créer le nouveau client
                    postResponse = requests.post(componentSvcBaseUrl, headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    excludes = []
                    if "bindCredential" in newComponent["config"]:
                        excludes.append("bindCredential")
                   
                    # Comparer les components
                    if (isDictEquals(newComponent, component, excludes)): # Si le nouveau client n'introduit pas de modification au client existant
                        # Ne rien changer
                        changed = False
                    else: # Si le client doit être modifié
                        # Stocker le client dans un body prêt a être posté
                        data=json.dumps(newComponent)
                        # Mettre à jour le client sur le serveur Keycloak
                        updateResponse = requests.put(componentSvcBaseUrl + component["id"], headers=headers, data=data)
                        changed = True
                # Obtenir le composant
                getResponse = getResponse = requests.get(componentSvcBaseUrl + component["id"], headers=headers)
                component = getResponse.json()
                fact = dict(
                    component = component)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            elif state == 'absent': # Le status est absent
                # Supprimer le client
                deleteResponse = requests.delete(componentSvcBaseUrl + component['id'], headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                stderr   = 'put or delete component: ' + newComponent['id'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                stderr   = 'put or delete component: ' + newComponent['id'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    return result
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
