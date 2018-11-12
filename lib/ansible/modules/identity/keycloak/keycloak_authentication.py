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
module: keycloak_authentication
short_description: Configure authentication in Keycloak
description:
    - This module actually can only make a copy of an existing authentication flow, add an execution to it and configure it.
    - It can also delete the flow.
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
            - The name of the realm in which is the authentication.
        required: true
    alias:
        description:
            - Alias for the authentication flow
        required: true
    providerId:
        description:
            - providerId for the new flow when not copied from an existing flow.
        required: false
    copyForm:
        description:
            - flowAlias of the authentication flow to use for the copy.
        required: false
    authenticationConfig:
        description:
            - Configuration structure for the authenticator. See example.
        required: true
    authenticationExecutions:
        description:
            - Configuration structure for the execution
        required: true
    state:
        description:
            - Control if the authentication flow must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        choices: [ "yes", "no" ]
        default: "no"
        description:
            - If yes, allows to remove the authentication flow and recreate it.
        required: false
notes:
    - This module has very limited functions at the moment. Please contribute if you need more...
'''

EXAMPLES = '''
    - name: Create an authentication flow from first broker login and add an execution to it.
      keycloak_authentication:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        alias: "Copy of first broker login"
        copyFrom: "first broker login"
        authenticationConfig: 
          alias: "test.provisioning.property"
          config: 
            test.provisioning.property: "value"
        authenticationExecutions:
          providerId: "test-provisioning"
          requirement: "REQUIRED"
        state: present

    - name: Re-create the authentication flow
      keycloak_authentication:
        url: http://localhost:8080
        username: admin
        password: password
        realm: master
        alias: "Copy of first broker login"
        copyFrom: "first broker login"
        authenticationConfig: 
          alias: "test.provisioning.property"
          config: 
            test.provisioning.property: "value"
        authenticationExecutions:
          providerId: "test-provisioning"
          requirement: "REQUIRED"
        state: present
        force: yes

    - name: Remove authentication.
      keycloak_authentication:
        url: http://localhost:8080
        username: admin
        password: admin
        realm: master
        alias: "Copy of first broker login"
        state: absent
'''

RETURN = '''
ansible_facts:
  description: JSON representation for the authentication.
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
  description: Return True if the operation changed the authentication on the keycloak server, false otherwise.
  returned: always
  type: bool
'''
import requests
import json
import urllib
from ansible.module_utils.keycloak_utils import *
from __builtin__ import isinstance    

def copyAuthFlow(url, config, headers):
    
    copyFrom = config["copyFrom"]
    
    newName = dict(
        newName = config["alias"]
    )
    
    data = json.dumps(newName)
    requests.post(url + "flows/" + urllib.quote(config["copyFrom"]) + "/copy", headers=headers, data=data)
    getResponse = requests.get(url + "flows/", headers = headers)
    flowList = getResponse.json()
    for flow in flowList:
        if flow["alias"] == config["alias"]:
            return flow
    return None

def createEmptyAuthFlow(url, config, headers):
    
    newFlow = dict(
        alias = config["alias"],
        providerId = config["providerId"],
        topLevel = True
    )
    data = json.dumps(newFlow)
    requests.post(url + "flows", headers=headers, data=data)
    getResponse = requests.get(url + "flows/", headers = headers)
    flowList = getResponse.json()
    for flow in flowList:
        if flow["alias"] == config["alias"]:
            return flow
    return None
def addAuthenticationConfig(url, config, headers):
    # Prepare post to create the execution
    postJson = dict(
        provider = config["authenticationExecutions"]["providerId"],
        )
    # Create execution without configuration
    data = json.dumps(postJson)
    requests.post(url + "flows/" + urllib.quote(config["alias"]) + "/executions/execution", headers=headers, data=data)
    # get the execution Id
    getResponse = requests.get(url + "flows/" + urllib.quote(config["alias"]) + "/executions", headers=headers)
    executions = getResponse.json()
    execution = None
    for execution in executions:
        if "providerId" in execution and execution["providerId"] == config["authenticationExecutions"]["providerId"]:
            break
    
    # Add the autenticatorConfig to the execution
    data = json.dumps(config["authenticationConfig"])
    if execution is not None:
        requests.post(url + "executions/" + execution["id"] + "/config", headers=headers, data=data)
        # Configure the execution itself
        config["authenticationExecutions"]["id"] = execution["id"]
        data = json.dumps(config["authenticationExecutions"])
        requests.put(url + "flows/" + urllib.quote(config["alias"]) + "/executions", headers=headers, data=data)
    getResponse = requests.get(url + "flows/" + urllib.quote(config["alias"]) + "/executions", headers=headers)
    executions = getResponse.json()
    execution = None
    for execution in executions:
        if "providerId" in execution and execution["providerId"] == config["authenticationExecutions"]["providerId"]:
            break
    authenticationConfig = None
    if execution is not None:
        getResponse = requests.get(url + "config/" + execution["authenticationConfig"], headers=headers)
        authenticationConfig = getResponse.json()
    toReturn = dict(
        authenticationExecutions = execution,
        authenticationConfig = authenticationConfig
        )
    return toReturn

def main():
    module = AnsibleModule(
        argument_spec = dict(
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
            realm=dict(type='str', required=True),
            alias=dict(type='str', required=True),
            providerId=dict(type='str'),
            copyFrom = dict(type='str'),
            authenticationConfig=dict(type='dict'),
            authenticationExecutions=dict(type='dict'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force']) if "force" in module.params else False
    
    result = authentication(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def authentication(params):
    url = params['url']
    username = params['username']
    password = params['password']
    realm = params['realm']
    state = params['state'] if "state" in params else "present"
    force = params['force'] if "force" in params else False
    newComposites = None
    authenticationRepresentation = None
    
    # Créer un représentation du authentication recu en paramètres
    newAuthenticationRepresentation = {}
    newAuthenticationRepresentation["alias"] = params["alias"].decode("utf-8")
    if "copyFrom" in params and params["copyFrom"] is not None:
        newAuthenticationRepresentation["copyFrom"] = params["copyFrom"].decode("utf-8")
    if "providerId" in params and params["providerId"] is not None:
        newAuthenticationRepresentation["providerId"] = params["providerId"].decode("utf-8")
    if "authenticationConfig" in params and params["authenticationConfig"] is not None:
        newAuthenticationRepresentation["authenticationConfig"] = params["authenticationConfig"]
    if "authenticationExecutions" in params and params["authenticationExecutions"] is not None:
        newAuthenticationRepresentation["authenticationExecutions"] = params["authenticationExecutions"]
   
    authenticationSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/authentication/"
    
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
        authenticationRepresentation = None 
        # Check if the authentication flow exists on the Keycloak server
        getResponse = requests.get(authenticationSvcBaseUrl + "flows", headers=headers)
        for authentication in getResponse.json():
            if authentication["alias"] == newAuthenticationRepresentation["alias"]:
                authenticationRepresentation = authentication
                break
    except Exception, e:
        result = dict(
            stderr   = 'first authentication get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    if authenticationRepresentation is None: # Le authentication n'existe pas
        # Creer le authentication
        
        if (state == 'present'): # Si le status est présent
            try:
                # Create authentication flow from a copy
                if "copyFrom" in newAuthenticationRepresentation and newAuthenticationRepresentation["copyFrom"] is not None:
                    authenticationRepresentation = copyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
                else:
                    authenticationRepresentation = createEmptyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
                # If the authentication still not exist on the server, raise an exception.
                if authenticationRepresentation is None:
                    raise Exception("Authentication just created not found: " + str(newAuthenticationRepresentation))
                # Configure the executions for the flow
                flowConfig = addAuthenticationConfig(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
                changed = True
                fact = dict(
                    flow = authenticationRepresentation,
                    authenticationExecutions = flowConfig["authenticationExecutions"],
                    authenticationConfig = flowConfig["authenticationConfig"]
                    )                
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                fact = dict(
                    authentication = newAuthenticationRepresentation)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post authentication: ' + newAuthenticationRepresentation["alias"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                fact = dict(
                    authentication = newAuthenticationRepresentation)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post authentication: ' + newAuthenticationRepresentation["alias"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        elif state == 'absent': # Sinon, le status est absent
            result = dict(
                stdout   = newAuthenticationRepresentation["alias"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # The authentication flow already exist
        try:
            if (state == 'present'): # si le status est présent
                if force: # Si l'option force est sélectionné
                    # Supprimer le authentication existant
                    requests.delete(authenticationSvcBaseUrl + "flows/" + authenticationRepresentation["id"], headers=headers)
                    changed = True
                    # Create authentication flow from a copy
                    authenticationRepresentation = copyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
                    # If the authentication still not exist on the server, raise an exception.
                    if authenticationRepresentation is None:
                        raise Exception("Authentication just created not found: " + str(newAuthenticationRepresentation))
                    # Configure the executions for the flow
                    flowConfig = addAuthenticationConfig(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
                    changed = True
                    fact = dict(
                        flow = authenticationRepresentation,
                        authenticationExecutions = flowConfig["authenticationExecutions"],
                        authenticationConfig = flowConfig["authenticationConfig"]
                        )
                else:
                    # The module does not modify an existing authentication flow. Use force to delete it and recreate it
                    getResponse = requests.get(authenticationSvcBaseUrl + "flows/" + urllib.quote(newAuthenticationRepresentation["alias"]) + "/executions", headers=headers)
                    executions = getResponse.json()
                    execution = None
                    for execution in executions:
                        if "providerId" in execution and execution["providerId"] == newAuthenticationRepresentation["authenticationExecutions"]["providerId"]:
                            break
                    authenticationConfig = None
                    if execution is not None:
                        getResponse = requests.get(authenticationSvcBaseUrl + "config/" + execution["authenticationConfig"], headers=headers)
                        authenticationConfig = getResponse.json()
                    fact = dict(
                        flow = authenticationRepresentation,
                        authenticationExecutions = execution,
                        authenticationConfig = authenticationConfig
                        )
                             
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            elif state == 'absent': # Le status est absent
                # Supprimer le authentication
                requests.delete(authenticationSvcBaseUrl + "flows/" + authenticationRepresentation["id"], headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                stderr   = 'put or delete authentication: ' + newAuthenticationRepresentation['alias'] + ' id: ' + authenticationRepresentation["id"] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                stderr   = 'put or delete authentication: ' + newAuthenticationRepresentation['alias']  + ' id: ' + authenticationRepresentation["id"] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    return result
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
