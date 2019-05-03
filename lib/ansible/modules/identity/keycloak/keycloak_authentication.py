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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
author: "Philippe Gauthier (philippe.gauthier@inspq.qc.ca"
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
author: "Philippe Gauthier (philippe.gauthier@inspq.qc.ca"
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
>>>>>>> SX5-868 Add keycloak_authentication module.
module: keycloak_authentication
short_description: Configure authentication in Keycloak
description:
    - This module actually can only make a copy of an existing authentication flow, add an execution to it and configure it.
    - It can also delete the flow.
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
version_added: "2.9"
options:
=======
version_added: "2.3"
=======
version_added: "2.9"
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
version_added: "2.9"
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
options:
<<<<<<< HEAD
<<<<<<< HEAD
=======
version_added: "2.3"
options:
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
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
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Update documentation for keycloak_authentication module.
=======
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Update documentation for keycloak_authentication module.
=======
version_added: "2.9"
options:
>>>>>>> SX5-868 Add keycloak_authentication module.
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
    copyFrom:
        description:
            - flowAlias of the authentication flow to use for the copy.
        required: false
    authenticationExecutions:
        description:
            - Configuration structure for the executions
        required: false
    state:
        description:
            - Control if the authentication flow must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        type: bool
        default: false
        description:
            - If true, allows to remove the authentication flow and recreate it.
        required: false
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> SX5-868 Update documentation for keycloak_authentication module.
extends_documentation_fragment:
    - keycloak
<<<<<<< HEAD
notes:
    - This module has very limited functions at the moment. Please contribute if you need more...
<<<<<<< HEAD
<<<<<<< HEAD
author:
    - Philippe Gauthier (philippe.gauthier@inspq.qc.ca)
<<<<<<< HEAD
=======
=======
extends_documentation_fragment:
    - keycloak
>>>>>>> SX5-868 Update documentation for keycloak_authentication module.
notes:
    - This module has very limited functions at the moment. Please contribute if you need more...
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
notes:
    - This module has very limited functions at the moment. Please contribute if you need more...
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
=======

<<<<<<< HEAD
>>>>>>> SX5-868 Fix keycloak_authentication module documentation.
author: 
=======
author:
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
author:
<<<<<<< HEAD
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
    - Philippe Gauthier (philippe.gauthier@inspq.qc.ca)
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
extends_documentation_fragment:
    - keycloak
notes:
    - This module has very limited functions at the moment. Please contribute if you need more...
author: 
    - Philippe Gauthier (philippe.gauthier@inspq.qc.ca)
>>>>>>> SX5-868 Add keycloak_authentication module.
=======
    - Philippe Gauthier (@elfelip)
>>>>>>> SX5-868 changed syntax of author in documentation for
'''

EXAMPLES = '''
    - name: Create an authentication flow from first broker login and add an execution to it.
      keycloak_authentication:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
=======
        url: http://localhost:8080
        username: admin
        password: password
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
        url: http://localhost:8080
        username: admin
        password: password
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Add keycloak_authentication module.
        realm: master
        alias: "Copy of first broker login"
        copyFrom: "first broker login"
        authenticationExecutions:
          - providerId: "test-execution1"
            requirement: "REQUIRED"
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            authenticationConfig:
              alias: "test.execution1.property"
              config:
                test1.property: "value"
          - providerId: "test-execution2"
            requirement: "REQUIRED"
            authenticationConfig:
              alias: "test.execution2.property"
              config:
=======
            authenticationConfig: 
=======
            authenticationConfig:
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
              alias: "test.execution1.property"
              config:
                test1.property: "value"
          - providerId: "test-execution2"
            requirement: "REQUIRED"
            authenticationConfig:
              alias: "test.execution2.property"
<<<<<<< HEAD
              config: 
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
              config:
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
            authenticationConfig: 
=======
            authenticationConfig:
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
              alias: "test.execution1.property"
              config:
                test1.property: "value"
          - providerId: "test-execution2"
            requirement: "REQUIRED"
            authenticationConfig:
              alias: "test.execution2.property"
<<<<<<< HEAD
              config: 
>>>>>>> SX5-868 Add keycloak_authentication module.
=======
              config:
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
                test2.property: "value"
        state: present

    - name: Re-create the authentication flow
      keycloak_authentication:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
=======
        url: http://localhost:8080
        username: admin
        password: password
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
        url: http://localhost:8080
        username: admin
        password: password
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Add keycloak_authentication module.
        realm: master
        alias: "Copy of first broker login"
        copyFrom: "first broker login"
        authenticationExecutions:
          - providerId: "test-provisioning"
            requirement: "REQUIRED"
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            authenticationConfig:
              alias: "test.provisioning.property"
              config:
=======
            authenticationConfig: 
              alias: "test.provisioning.property"
              config: 
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
            authenticationConfig:
              alias: "test.provisioning.property"
              config:
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
            authenticationConfig: 
              alias: "test.provisioning.property"
              config: 
>>>>>>> SX5-868 Add keycloak_authentication module.
=======
            authenticationConfig:
              alias: "test.provisioning.property"
              config:
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
                test.provisioning.property: "value"
        state: present
        force: yes

    - name: Remove authentication.
      keycloak_authentication:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
=======
        url: http://localhost:8080
        username: admin
        password: admin
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
        url: http://localhost:8080
        username: admin
        password: admin
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Mise à jour de la documentation des modules Keycloak suite à la
=======
        auth_keycloak_url: http://localhost:8080/auth
        auth_sername: admin
        auth_password: password
>>>>>>> SX5-868 Add keycloak_authentication module.
        realm: master
        alias: "Copy of first broker login"
        state: absent
'''

RETURN = '''
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
flow:
  description: JSON representation for the authentication.
  returned: on success
  type: dict
msg:
  description: Error message if it is the case
  returned: on error
  type: str
=======
ansible_facts:
=======
flow:
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
  description: JSON representation for the authentication.
  returned: on success
  type: dict
msg:
  description: Error message if it is the case
  returned: on error
  type: str
<<<<<<< HEAD
=======
ansible_facts:
=======
flow:
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
flow:
>>>>>>> SX5-868 Add keycloak_authentication module.
  description: JSON representation for the authentication.
  returned: on success
  type: dict
msg:
  description: Error message if it is the case
  returned: on error
  type: str
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
rc:
  description: return code, 0 if success, 1 otherwise.
  returned: always
  type: bool
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
>>>>>>> SX5-868 Add keycloak_authentication module.
changed:
  description: Return True if the operation changed the authentication on the keycloak server, false otherwise.
  returned: always
  type: bool
'''
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from ansible.module_utils.keycloak import KeycloakAPI, keycloak_argument_spec
from ansible.module_utils.basic import AnsibleModule

<<<<<<< HEAD
=======
=======
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
import json
import urllib
from ansible.module_utils.keycloak_utils import isDictEquals
from ansible.module_utils.keycloak import KeycloakAPI, camel, keycloak_argument_spec
from ansible.module_utils.basic import AnsibleModule

#def copyAuthFlow(url, config, headers):
#    
#    copyFrom = config["copyFrom"]
#    
#    newName = dict(
#        newName = config["alias"]
#    )
    
#    data = json.dumps(newName)
#    requests.post(url + "flows/" + urllib.quote(config["copyFrom"]) + "/copy", headers=headers, data=data)
#    getResponse = requests.get(url + "flows/", headers = headers)
#    flowList = getResponse.json()
#    for flow in flowList:
#        if flow["alias"] == config["alias"]:
#            return flow
#    return None

#def createEmptyAuthFlow(url, config, headers):
#    
#    newFlow = dict(
#        alias = config["alias"],
#        providerId = config["providerId"],
#        topLevel = True
#    )
#    data = json.dumps(newFlow)
#    requests.post(url + "flows", headers=headers, data=data)
#    getResponse = requests.get(url + "flows/", headers = headers)
#    flowList = getResponse.json()
#    for flow in flowList:
#        if flow["alias"] == config["alias"]:
#            return flow
#    return None

#def createOrUpdateExecutions(url, config, headers):
#    changed = False
#
#    if "authenticationExecutions" in config:
#        for newExecution in config["authenticationExecutions"]:
#            # Get existing executions on the Keycloak server for this alias
#            getResponse = requests.get(url + "flows/" + urllib.quote(config["alias"]) + "/executions", headers=headers)
#            existingExecutions = getResponse.json()
#            executionFound = False
#            for existingExecution in existingExecutions:
#                if "providerId" in existingExecution and existingExecution["providerId"] == newExecution["providerId"]:
#                    executionFound = True
#                    break
#            if executionFound:
#                # Replace config id of the execution config by it's complete representation
#                if "authenticationConfig" in existingExecution:
#                    execConfigId = existingExecution["authenticationConfig"]
#                    getResponse = requests.get(url + "config/" + execConfigId, headers=headers)
#                    execConfig = getResponse.json()
#                    existingExecution["authenticationConfig"] = execConfig
#
#                # Compare the executions to see if it need changes
#                if not isDictEquals(newExecution, existingExecution):
#                    changed = True
#            else:
#                # Create the new execution
#                newExec = {}
#                newExec["provider"] = newExecution["providerId"]
#                newExec["requirement"] = newExecution["requirement"]
#                data = json.dumps(newExec)
#                requests.post(url + "flows/" + urllib.quote(config["alias"]) + "/executions/execution", headers=headers, data=data)
#                changed = True
#            if changed:
#                # Get existing executions on the Keycloak server for this alias
#                getResponse = requests.get(url + "flows/" + urllib.quote(config["alias"]) + "/executions", headers=headers)
#                existingExecutions = getResponse.json()
#                executionFound = False
#                for existingExecution in existingExecutions:
#                    if "providerId" in existingExecution and existingExecution["providerId"] == newExecution["providerId"]:
#                        executionFound = True
#                        break
#                if executionFound:
#                    # Update the existing execution
#                    updatedExec = {}
#                    updatedExec["id"] = existingExecution["id"]
#                    for key in newExecution:
#                        # create the execution configuration
#                        if key == "authenticationConfig":
#                            # Add the autenticatorConfig to the execution
#                            data = json.dumps(newExecution["authenticationConfig"])
#                            requests.post(url + "executions/" + existingExecution["id"] + "/config", headers=headers, data=data)
#                        else:
#                            updatedExec[key] = newExecution[key]
#                    data = json.dumps(updatedExec)
#                    requests.put(url + "flows/" + urllib.quote(config["alias"]) + "/executions", headers=headers, data=data)
#    return changed

#def getExecutionsRepresentation(url, config, headers):
#    # Get executions created
#    getResponse = requests.get(url + "flows/" + urllib.quote(config["alias"]) + "/executions", headers=headers)
#    executions = getResponse.json()
#    for execution in executions:
#        if "authenticationConfig" in execution:
#            execConfigId = execution["authenticationConfig"]
#            getResponse = requests.get(url + "config/" + execConfigId, headers=headers)
#            execConfig = getResponse.json()
#            execution["authenticationConfig"] = execConfig
#    return executions
        

<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
from ansible.module_utils.keycloak import KeycloakAPI, keycloak_argument_spec
from ansible.module_utils.basic import AnsibleModule

>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======

>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
def main():
    """
    Module execution
=======
=======
from ansible.module_utils.keycloak import KeycloakAPI, keycloak_argument_spec
from ansible.module_utils.basic import AnsibleModule

<<<<<<< HEAD
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
from ansible.module_utils.keycloak import KeycloakAPI, keycloak_argument_spec
from ansible.module_utils.basic import AnsibleModule

<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module.
def main():
    """
    Module execution
    
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======

def main():
    """
    Module execution
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
>>>>>>> SX5-868 Add keycloak_authentication module.
=======

def main():
    """
    Module execution
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
    :returm:
    """
    argument_spec = keycloak_argument_spec()
    meta_args = dict(
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Add keycloak_user module and non mock unit tests.
=======
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Add keycloak_user module and non mock unit tests.
=======
>>>>>>> SX5-868 Add keycloak_authentication module.
            realm=dict(type='str', required=True),
            alias=dict(type='str', required=True),
            providerId=dict(type='str'),
            copyFrom = dict(type='str'),
            authenticationExecutions=dict(type='list'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        )
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
        realm=dict(type='str', required=True),
        alias=dict(type='str', required=True),
        providerId=dict(type='str'),
        copyFrom=dict(type='str'),
        authenticationExecutions=dict(type='list'),
        state=dict(choices=["absent", "present"], default='present'),
        force=dict(type='bool', default=False),
    )
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
>>>>>>> SX5-868 Add keycloak_authentication module.
=======
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
    argument_spec.update(meta_args)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = dict(changed=False, msg='', flow={})
    kc = KeycloakAPI(module)

    realm = module.params.get('realm')
    state = module.params.get('state')
    force = module.params.get('force')
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
    newAuthenticationRepresentation = {}
    newAuthenticationRepresentation["alias"] = module.params.get("alias")
    newAuthenticationRepresentation["copyFrom"] = module.params.get("copyFrom")
    newAuthenticationRepresentation["providerId"] = module.params.get("providerId")
    newAuthenticationRepresentation["authenticationExecutions"] = module.params.get("authenticationExecutions")
<<<<<<< HEAD
=======
    # Créer un représentation du authentication recu en paramètres
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
    
>>>>>>> SX5-868 Add keycloak_authentication module.
    newAuthenticationRepresentation = {}
    newAuthenticationRepresentation["alias"] = module.params.get("alias")
    newAuthenticationRepresentation["copyFrom"] = module.params.get("copyFrom")
    newAuthenticationRepresentation["providerId"] = module.params.get("providerId")
    newAuthenticationRepresentation["authenticationExecutions"] = module.params.get("authenticationExecutions")
<<<<<<< HEAD
<<<<<<< HEAD
   
    #authenticationSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/authentication/"
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
    
=======

>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
    changed = False

    authenticationRepresentation = kc.get_authentication_flow_by_alias(alias=newAuthenticationRepresentation["alias"], realm=realm)

    if authenticationRepresentation == {}:  # Authentication flow does not exist
        if (state == 'present'):  # If desired state is prenset
            # If copyFrom is defined, create authentication flow from a copy
            if "copyFrom" in newAuthenticationRepresentation and newAuthenticationRepresentation["copyFrom"] is not None:
<<<<<<< HEAD
<<<<<<< HEAD
                authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
            else: # Create an empty authentication flow
=======
=======
    
=======

>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======

>>>>>>> SX5-868 fix code style in keycloak_authentication module.
    newAuthenticationRepresentation = {}
    newAuthenticationRepresentation["alias"] = module.params.get("alias")
    newAuthenticationRepresentation["copyFrom"] = module.params.get("copyFrom")
    newAuthenticationRepresentation["providerId"] = module.params.get("providerId")
    newAuthenticationRepresentation["authenticationExecutions"] = module.params.get("authenticationExecutions")

<<<<<<< HEAD
    changed = False

    authenticationRepresentation = kc.get_authentication_flow_by_alias(alias=newAuthenticationRepresentation["alias"], realm=realm)

    if authenticationRepresentation == {}:  # Authentication flow does not exist
        if (state == 'present'):  # If desired state is prenset
            # If copyFrom is defined, create authentication flow from a copy
            if "copyFrom" in newAuthenticationRepresentation and newAuthenticationRepresentation["copyFrom"] is not None:
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
                #authenticationRepresentation = copyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
                authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
            else: # Create an empty authentication flow
                #authenticationRepresentation = createEmptyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
                authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
<<<<<<< HEAD
            else: # Create an empty authentication flow
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
            else:  # Create an empty authentication flow
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
                authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
<<<<<<< HEAD
            else: # Create an empty authentication flow
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
            else:  # Create an empty authentication flow
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
    
=======
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
    changed = False

    authenticationRepresentation = kc.get_authentication_flow_by_alias(alias=newAuthenticationRepresentation["alias"], realm=realm)

    if authenticationRepresentation == {}:  # Authentication flow does not exist
        if (state == 'present'):  # If desired state is prenset
            # If copyFrom is defined, create authentication flow from a copy
            if "copyFrom" in newAuthenticationRepresentation and newAuthenticationRepresentation["copyFrom"] is not None:
                authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
<<<<<<< HEAD
            else: # Create an empty authentication flow
>>>>>>> SX5-868 Add keycloak_authentication module.
=======
            else:  # Create an empty authentication flow
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
                authenticationRepresentation = kc.create_empty_auth_flow(config=newAuthenticationRepresentation, realm=realm)
            # If the authentication still not exist on the server, raise an exception.
            if authenticationRepresentation is None:
                result['msg'] = "Authentication just created not found: " + str(newAuthenticationRepresentation)
                module.fail_json(**result)
            # Configure the executions for the flow
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm)
            changed = True
            # Get executions created
=======
=======
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
            #createOrUpdateExecutions(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
            kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm)
            changed = True
            # Get executions created
            #executionsRepresentation = getExecutionsRepresentation(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
            kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm)
            changed = True
            # Get executions created
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
            executionsRepresentation = kc.get_executions_representation(config=newAuthenticationRepresentation, realm=realm)
            if executionsRepresentation is not None:
                authenticationRepresentation["authenticationExecutions"] = executionsRepresentation
            result['changed'] = changed
            result['flow'] = authenticationRepresentation
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        elif state == 'absent': # If desired state is absent.
=======
        elif state == 'absent': # Sinon, le status est absent
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
        elif state == 'absent': # If desired state is absent.
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
        elif state == 'absent':  # If desired state is absent.
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
            result['msg'] = newAuthenticationRepresentation["alias"] + ' absent'
    else:  # The authentication flow already exist
<<<<<<< HEAD
        if (state == 'present'): # if desired state is present
            if force: # If force option is true
<<<<<<< HEAD
<<<<<<< HEAD
=======
                #requests.delete(authenticationSvcBaseUrl + "flows/" + authenticationRepresentation["id"], headers=headers)
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
        if (state == 'present'):  # if desired state is present
            if force:  # If force option is true
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
=======
            kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm)
            changed = True
            # Get executions created
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
            executionsRepresentation = kc.get_executions_representation(config=newAuthenticationRepresentation, realm=realm)
            if executionsRepresentation is not None:
                authenticationRepresentation["authenticationExecutions"] = executionsRepresentation
            result['changed'] = changed
            result['flow'] = authenticationRepresentation
        elif state == 'absent':  # If desired state is absent.
            result['msg'] = newAuthenticationRepresentation["alias"] + ' absent'
    else:  # The authentication flow already exist
<<<<<<< HEAD
        if (state == 'present'): # if desired state is present
            if force: # If force option is true
<<<<<<< HEAD
                #requests.delete(authenticationSvcBaseUrl + "flows/" + authenticationRepresentation["id"], headers=headers)
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
        if (state == 'present'):  # if desired state is present
            if force:  # If force option is true
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
            kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm)
            changed = True
            # Get executions created
            executionsRepresentation = kc.get_executions_representation(config=newAuthenticationRepresentation, realm=realm)
            if executionsRepresentation is not None:
                authenticationRepresentation["authenticationExecutions"] = executionsRepresentation
            result['changed'] = changed
            result['flow'] = authenticationRepresentation
        elif state == 'absent':  # If desired state is absent.
            result['msg'] = newAuthenticationRepresentation["alias"] + ' absent'
    else:  # The authentication flow already exist
<<<<<<< HEAD
        if (state == 'present'): # if desired state is present
            if force: # If force option is true
>>>>>>> SX5-868 Add keycloak_authentication module.
=======
        if (state == 'present'):  # if desired state is present
            if force:  # If force option is true
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
                # Delete the actual authentication flow
                kc.delete_authentication_flow_by_id(id=authenticationRepresentation["id"], realm=realm)
                changed = True
                # If copyFrom is defined, create authentication flow from a copy
                if "copyFrom" in newAuthenticationRepresentation and newAuthenticationRepresentation["copyFrom"] is not None:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
                else: # Create an empty authentication flow
=======
                    #authenticationRepresentation = copyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
                    authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
<<<<<<< HEAD
<<<<<<< HEAD
                else: # Create an empty authentication flow
<<<<<<< HEAD
                    #authenticationRepresentation = createEmptyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
                    authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
                else: # Create an empty authentication flow
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
                else:  # Create an empty authentication flow
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
                    #authenticationRepresentation = copyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
                    authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
                else: # Create an empty authentication flow
                    #authenticationRepresentation = createEmptyAuthFlow(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
                else:  # Create an empty authentication flow
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
                    authenticationRepresentation = kc.copy_auth_flow(config=newAuthenticationRepresentation, realm=realm)
<<<<<<< HEAD
                else: # Create an empty authentication flow
>>>>>>> SX5-868 Add keycloak_authentication module.
=======
                else:  # Create an empty authentication flow
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
                    authenticationRepresentation = kc.create_empty_auth_flow(config=newAuthenticationRepresentation, realm=realm)
                # If the authentication still not exist on the server, raise an exception.
                if authenticationRepresentation is None:
                    result['msg'] = "Authentication just created not found: " + str(newAuthenticationRepresentation)
                    result['changed'] = changed
                    module.fail_json(**result)
            # Configure the executions for the flow
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            if kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm):
                changed = True
            # Get executions created
=======
=======
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
            #changed = createOrUpdateExecutions(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
            if kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm):
                changed = True
            # Get executions created
            #executionsRepresentation = getExecutionsRepresentation(authenticationSvcBaseUrl, newAuthenticationRepresentation, headers)
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
            if kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm):
                changed = True
            # Get executions created
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
            if kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm):
                changed = True
            # Get executions created
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
            if kc.create_or_update_executions(config=newAuthenticationRepresentation, realm=realm):
                changed = True
            # Get executions created
>>>>>>> SX5-868 Add keycloak_authentication module.
            executionsRepresentation = kc.get_executions_representation(config=newAuthenticationRepresentation, realm=realm)
            if executionsRepresentation is not None:
                authenticationRepresentation["authenticationExecutions"] = executionsRepresentation
            result['flow'] = authenticationRepresentation
            result['changed'] = changed
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        elif state == 'absent':  # If desired state is absent
            # Delete the authentication flow alias.
<<<<<<< HEAD
<<<<<<< HEAD
=======
            #requests.delete(authenticationSvcBaseUrl + "flows/" + authenticationRepresentation["id"], headers=headers)
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
        elif state == 'absent': # If desired state is absent
=======
        elif state == 'absent':  # If desired state is absent
>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
        elif state == 'absent':  # If desired state is absent
>>>>>>> SX5-868 fix code style in keycloak_authentication module.
            # Delete the authentication flow alias.
<<<<<<< HEAD
            #requests.delete(authenticationSvcBaseUrl + "flows/" + authenticationRepresentation["id"], headers=headers)
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======
>>>>>>> SX5-868 Code cleaning and documentation for keycloak_authentication
=======
        elif state == 'absent': # If desired state is absent
            # Delete the authentication flow alias.
>>>>>>> SX5-868 Add keycloak_authentication module.
            kc.delete_authentication_flow_by_id(id=authenticationRepresentation["id"], realm=realm)
            changed = True
            result['msg'] = 'Authentication flow: ' + newAuthenticationRepresentation['alias'] + ' id: ' + authenticationRepresentation["id"] + ' is deleted'
            result['changed'] = changed
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

    module.exit_json(**result)


=======
=======
>>>>>>> SX5-868 Add keycloak_authentication module.
    
    module.exit_json(**result)
    
    
<<<<<<< HEAD
>>>>>>> SX5-868 Add keycloak_authentication module to manage Authentication
=======

    module.exit_json(**result)


>>>>>>> SX5-868 Ajustement du codestyle des modules Keycloak en préparation des
=======
>>>>>>> SX5-868 Add keycloak_authentication module.
=======

    module.exit_json(**result)


>>>>>>> SX5-868 fix code style in keycloak_authentication module.
if __name__ == '__main__':
    main()
