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
author: "Etienne Sadio (etienne.sadio@inspq.qc.ca)"
module: keycloak_user
short_description: create and Configure a user in Keycloak
description:
    - This module creates, removes or update Keycloak users.
version_added: "2.3"
options:
    url:
        description:
            - The url of the Keycloak server.
        default: http://localhost:8080/auth    
        required: true    
    masterUsername:
        description:
            - The username to logon to the master realm.
        required: true
    masterPassword:
        description:
            - The password for the user to logon the master realm.
        required: true
    realm:
        description:
            - The name of the realm in which is the client.
        required: true
    username:
        description:
            - username for the user.
        required: false
    enabled:
        description:
            - Enabled user.
        required: false
    emailVerified:
        description:
            - check the validity of user email.
        default: false
        required: false
    firstName:
        description:
            - User firstName.
        required: false
    lastName:
        description:
            - User lastName.
        required: false
    email:
        description:
            - User email.
        required: false
    federationLink:
        description:
            - Federation Link.
        required: false
    serviceAccountClientId:
        description:
            - Description of the client Application.
        required: false
    realmRoles:
        description:
            - List of ClientRoles for the user.
        required: false
    clientRoles:
        description:
            - List of ClientRoles for the user.
        required: false
    clientConsents:
        description: 
            - client Authenticator Type.
        required: false
    groups:
        description:
            - List of groups for the user.
        required: true
    credentials:
        description:
            - User credentials.
        required: false
    consentRequired:
        description:
            - consent Required.
        required: false
    requiredActions:
        description:
            - requiredActions user Auth.
        required: false
    federatedIdentities:
        description:
            - list of IDP of user. 
        required: false
    attributes:
        description:
            - list user attributes. 
        required: false
    access:
        description:
            - list user access. 
        required: false
    clientConsents:
        description:
            - list user clientConsents. 
        required: false
    disableableCredentialTypes:
        description:
            - list user Credential Type. 
        required: false
    origin:
        description:
            - user origin. 
        required: false
    serviceAccountClientId:
        description:
            - service Account ClientId for user. 
        required: false
    self:
        description:
            - user self administration. 
        required: false
    state:
        description:
            - Control if the user must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
    force:
        description:
            - If yes, allows to remove user and recreate it.
        choices: [ "yes", "no" ]
        default: "no"
        required: false
notes:
    - module does not modify userId.
'''

EXAMPLES = '''
    - name: Create a user user1 with default settings.
      keycloak_user:
        url: http://localhost:8080
        masterUsername: admin
        masterpassword: password
        realm: master
        username: user1
        firstName: user1
        lastName: user1
        email: user1
        enabled: true
        emailVerified: false
        credentials:
          - type: password
            value: password
            temporary: false
        attributes:
          attr1: 
            - value1
          attr2: 
            - value2
        state: present

    - name: Re-create client1
      keycloak_user:
        url: http://localhost:8080
        masterUsername: admin
        masterpassword: password
        realm: master
        username: user1
        firstName: user1
        lastName: user1
        email: user1
        enabled: true
        emailVerified: false
        credentials:
          - type: password
            value: password
            temporary: false
        attributes:
          attr1: 
            - value1
          attr2: 
            - value2
        state: present
        force: yes

    - name: Remove client1.
      keycloak_user:
        url: http://localhost:8080
        masterUsername: admin
        masterpassword: password
        realm: master
        username: user1
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
            masterUsername=dict(type='str', required=True),
            masterpassword=dict(required=True),
            realm=dict(type='str', required=True),
            self=dict(type='str'),
            id=dict(type='str'),
            username=dict(type='str', required=True),
            firstName=dict(type='str'),
            lastName=dict(type='str'),
            email=dict(type='str'),
            enabled=dict(type='bool', default=True),
            emailVerified=dict(type='bool', default=False),
            federationLink=dict(type='str'),
            serviceAccountClientId=dict(type='str'),
            attributes=dict(type='dict'),
            access=dict(type='dict'),
            clientRoles=dict(type='dict'),
            realmRoles=dict(type='list', default=[]),
            groups=dict(type='list', default=[]),
            disableableCredentialTypes=dict(type='list', default=[]),
            requiredActions=dict(type='list', default=[]),
            credentials=dict(type='list', default=[]),
            federatedIdentities=dict(type='list', default=[]),
            clientConsents=dict(type='list', default=[]),
            origin=dict(type='str'),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force'])
    
    result = user(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def user(params):
    url = params['url']
    username = params['masterUsername']
    password = params['masterpassword']
    realm = params['realm']
    state = params['state'] if "state" in params else "present"
    force = params['force'] if "force" in params else False
    newUserRepresentation = None
    userClientRoles = None
    
    # Create a representation of the user received in parameters
    newUserRepresentation = {}
    newUserRepresentation["username"] = params['username'].decode("utf-8")
    if "self" in params and params['self'] is not None:
        newUserRepresentation["self"] = params['self'].decode("utf-8")
    if "id" in params and params['id'] is not None:
        newUserRepresentation["id"] = params['id'].decode("utf-8")
    newUserRepresentation["enabled"] = params['enabled'] if "enabled" in params else True
    newUserRepresentation["emailVerified"] = params['emailVerified'] if "enabled" in params else False
    if "firstName" in params and params['firstName'] is not None:
        newUserRepresentation["firstName"] = params['firstName'].decode("utf-8")
    if "lastName" in params and params['lastName'] is not None:
        newUserRepresentation["lastName"] = params['lastName'].decode("utf-8")
    if "email" in params and params['email'] is not None:
        newUserRepresentation["email"] = params['email'].decode("utf-8")
    if "federationLink" in params and params['federationLink'] is not None:
        newUserRepresentation["federationLink"] = params['federationLink']
    if "serviceAccountClientId" in params and params['serviceAccountClientId'] is not None:
        newUserRepresentation["serviceAccountClientId"] = params['serviceAccountClientId']
    if "origin" in params and params['origin'] is not None:
        newUserRepresentation["origin"] = params['origin']
    if "credentials" in params and params['credentials'] is not None:
        newUserRepresentation["credentials"] = params['credentials']
    if "disableableCredentialTypes" in params and params['disableableCredentialTypes'] is not None:
        newUserRepresentation["disableableCredentialTypes"] = params['disableableCredentialTypes']
    if "federatedIdentities" in params and params['federatedIdentities'] is not None:
        newUserRepresentation["federatedIdentities"] = params['federatedIdentities']
    if "requiredActions" in params and params['requiredActions'] is not None:
        newUserRepresentation["requiredActions"] = params['requiredActions']
    if "clientConsents" in params and params['clientConsents'] is not None:
        newUserRepresentation["clientConsents"] = params['clientConsents']
    if "attributes" in params and params['attributes'] is not None:
        newUserRepresentation["attributes"] = params['attributes']
    if "access" in params and params['access'] is not None:
        newUserRepresentation["access"] = params['access']
    if "clientRoles" in params and params['clientRoles'] is not None:
        newUserRepresentation["clientRoles"] = params['clientRoles']
    if "realmRoles" in params and params['realmRoles'] is not None:
        newUserRepresentation["realmRoles"] = params['realmRoles']
    if "groups" in params and params['groups'] is not None:
        newUserRepresentation["groups"] = params['groups']
    
    userSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/users/"
    clientSvcBaseUrl = url + "/auth/admin/realms/" + realm + "/clients/"
    userRepresentation = None
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
        # Check if the user exists on the Keycloak server
        #getResponse = requests.get(userSvcBaseUrl+"?username="+newUserRepresentation["username"], headers=headers)
        getResponse = requests.get(userSvcBaseUrl, headers=headers, params={"username": newUserRepresentation["username"]})
        users = getResponse.json()
        for userRepresentation in users:
            if "username" in userRepresentation and userRepresentation["username"] == newUserRepresentation["username"]:
                break
    except Exception, e:
        result = dict(
            stderr   = 'first user get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    if userRepresentation is None: # The user does not exist
        # Create the user
        if (state == 'present'): # If state is present
            try:
                # Store the user in a post body
                data=json.dumps(newUserRepresentation)
                # Create the user
                postResponse = requests.post(userSvcBaseUrl, headers=headers, data=data)
                # Get new user created
                #getResponse = requests.get(userSvcBaseUrl+"?username="+newUserRepresentation["username"], headers=headers)
                getResponse = requests.get(userSvcBaseUrl, headers=headers, params={"username": newUserRepresentation["username"]})
                #userRepresentation = getResponse.json()[0]        
                users = getResponse.json()
                for userRepresentation in users:
                    if "username" in userRepresentation and userRepresentation["username"] == newUserRepresentation["username"]:
                        break
                #set user ClientsRoles
                if "clientRoles" in newUserRepresentation and newUserRepresentation['clientRoles'] is not None:
                    for userClientRoles in newUserRepresentation["clientRoles"]:
                        try:
                            createOrUpdateClientRoles(userClientRoles,userRepresentation,newUserRepresentation["clientRoles"][userClientRoles], clientSvcBaseUrl, userSvcBaseUrl, headers)
                        except Exception ,e :
                            result = dict(
                                stderr   = 'createOrUpdateClientRoles: ' + userClientRoles + ' error: ' + str(e),
                                rc       = 1,
                                changed  = changed
                                )
                #set ClientsRoles
                #createOrUpdateClientRoles(userClientRoles,userRepresentation, clientSvcBaseUrl, userSvcBaseUrl, headers)
                changed = True
                fact = dict(
                    user = userRepresentation,
                    clientRoles = userClientRoles
                    )
                
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                fact = dict(
                    user = newUserRepresentation)
                result = dict(
                    ansible_facts= fact,
                    stderr   = 'post user: ' + newUserRepresentation["username"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                fact = dict(
                    user = newUserRepresentation)
                result = dict(
                    ansible_facts = fact,
                    stderr   = 'post user: ' + newUserRepresentation["username"] + ' erreur: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        elif state == 'absent': # Otherwise, the status is absent
            result = dict(
                stdout   = newUserRepresentation["username"] + ' absent',
                rc       = 0,
                changed  = changed
            )
                
    else:  # the user already exists
        #userRepresentation = getResponse.json()[0]
        try:
            if (state == 'present'): # if the status is present
                if force == True: # If the force option is set to true
                    # Delete the existing user
                    deleteResponse = requests.delete(userSvcBaseUrl + userRepresentation["id"], headers=headers)
                    changed = True
                    # Store the user in a body for a post
                    data=json.dumps(newUserRepresentation)
                    # Create the new user
                    postResponse = requests.post(userSvcBaseUrl, headers=headers, data=data)
                    #set user ClientsRoles
                    if "clientRoles" in newUserRepresentation and newUserRepresentation['clientRoles'] is not None:
                        for userClientRoles in newUserRepresentation["clientRoles"]:
                            try:
                                createOrUpdateClientRoles(userClientRoles,userRepresentation,newUserRepresentation["clientRoles"][userClientRoles], clientSvcBaseUrl, userSvcBaseUrl, headers)
                            except Exception ,e :
                                result = dict(
                                    stderr   = 'createOrUpdateClientRoles: ' + userClientRoles + ' error: ' + str(e),
                                    rc       = 1,
                                    changed  = changed
                                    )
                else: # If the force option is false
                    excludes = ["access","notBefore","createdTimestamp","totp","credentials","disableableCredentialTypes","realmRoles","clientRoles","groups","clientConsents","federatedIdentities","requiredActions"]
                    # Compare users
                    if (isDictEquals(newUserRepresentation, userRepresentation, excludes)): # If the new user does not introduce a change to the existing user
                        # Do not change anything
                        changed = False
                    else: # Otherwise the user must be updated
                        # Store the user in a body for a post
                        data=json.dumps(newUserRepresentation)
                        # Updated the user on the Keycloak server
                        updateResponse = requests.put(userSvcBaseUrl + userRepresentation["id"], headers=headers, data=data)
                        #set user ClientsRoles
                        if "clientRoles" in newUserRepresentation and newUserRepresentation['clientRoles'] is not None:
                            for userClientRoles in newUserRepresentation["clientRoles"]:
                                try:
                                    createOrUpdateClientRoles(userClientRoles,userRepresentation,newUserRepresentation["clientRoles"][userClientRoles], clientSvcBaseUrl, userSvcBaseUrl, headers)
                                except Exception ,e :
                                    result = dict(
                                        stderr   = 'createOrUpdateClientRoles: ' + userClientRoles + ' error: ' + str(e),
                                        rc       = 1,
                                        changed  = changed
                                        )
                        changed = True
                # Get the new user
                #getResponse = requests.get(userSvcBaseUrl+"?username="+newUserRepresentation["username"], headers=headers)
                getResponse = requests.get(userSvcBaseUrl, headers=headers, params={"username": newUserRepresentation["username"]})
                users = getResponse.json()
                for userRepresentation in users:
                    if "username" in userRepresentation and userRepresentation["username"] == newUserRepresentation["username"]:
                        break
                #userRepresentation = getResponse.json()[0]
                fact = dict(
                    user = userRepresentation
                    )
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            elif state == 'absent': # Status is absent
                # Delete user
                deleteResponse = requests.delete(userSvcBaseUrl + userRepresentation['id'], headers=headers)
                changed = True
                result = dict(
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                stderr   = 'put or delete user: ' + newUserRepresentation['username'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                stderr   = 'put or delete user: ' + newUserRepresentation['username'] + ' error: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    return result

def createOrUpdateClientRoles(userClientRoles, userRepresentation, ClientRoles, clientSvcBaseUrl, userSvcBaseUrl, headers):
    changed = False
    # Get Roles ID
    clientId=None
    try:
        getResponse = requests.get(clientSvcBaseUrl, headers=headers)
        clients = getResponse.json()
        for client in clients:
            if "clientId" in client and client["clientId"] == userClientRoles:
                clientId = client["id"]
                break
        clientRolesToAdd = []
        if clientId is not None:
            #Egt clientsrole for clientID
            getResponse = requests.get(clientSvcBaseUrl +clientId+ "/roles/", headers=headers)
            roles = getResponse.json()
            for rolesToadd in ClientRoles:
                for role in roles:
                    if rolesToadd == role["name"]:
                      clientRolesToAdd.append(role)
        if len(clientRolesToAdd) > 0:
            #Set user role-mappings
            data=json.dumps(clientRolesToAdd)
            postResponse = requests.post(userSvcBaseUrl + userRepresentation["id"] + '/role-mappings/clients/'+clientId, headers=headers, data=data)
            changed = True
    except Exception ,e :
        raise e
    return changed    
        
# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
