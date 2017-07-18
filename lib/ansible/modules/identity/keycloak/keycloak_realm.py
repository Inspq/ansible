#!/usr/bin/python
# -*- coding: utf-8 -*-
from pip._vendor.requests.models import Request
from curses.ascii import NUL

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
module: keycloak_realm
short_description: Configure a realm in Keycloak
description:
  - This module creates, removes or update Keycloak realms.
version_added: "1.1"
options:
  realm:
    description:
    - The name of the realm.
    required: true
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
  name:
    description:
    - The display name of the realm.
    required: false
  namehtml:
    description:
    - The name to use within the HTML page of the realm.
    required: true
  accessCodeLifespan:
    description:
    - integer: access code lifespan.
    default: 60
    required: false
  accessCodeLifespanLogin:
    description: 
    - integer : access code lifespan login.
    default: 1800
    required: false
  accessCodeLifespanUserAction:
    description:
    - integer : access code lifespan user action.
    default: 300
    required: false
  accessTokenLifespan:
    description:
    - integer : access token lifespan.
    default: 300
    required: false
  accessTokenLifespanForImplicitFlow:
    description:
    - integer : access token lifespan for implicit flow.
    default: 900
    required: false
  notBefore
    description:
    - integer : not Before.
    default: 900
    required: false
  revokeRefreshToken
    description:
    - bool : revoke Refresh Token.
    default: 900
    required: false
  accessTokenLifespan
    description:
    - integer : access token lifespan.
    default: 300
    required: false
  ssoSessionMaxLifespan
    description:
    - integer : sso Session Max Lifespan.
    default: 36000
    required: false
  offlineSessionIdleTimeout
    description:
    - integer : offline Session Idle Timeout.
    default: 2592000
    required: false
  enabled
    description:
    - bool : enabled.
    default: True
    required: false
  sslRequired
    description:
    - str : sslRequired.
    default: external
    required: false
  registrationAllowed
    description:
    - bool : registration Allowed.
    default: False
    required: false
  registrationEmailAsUsername
    description:
    - bool : registration Email As Username.
    default: False
    required: false
  rememberMe
    description:
    - bool : remember me.
    default: False
    required: false
  verifyEmail
    description:
    - bool : verify Email.
    default: False
    required: false
  loginWithEmailAllowed
    description:
    - bool : login With Email Allowed.
    default: True
    required: false
  duplicateEmailsAllowed
    description:
    - bool : duplicate Emails Allowed.
    default: 900
    required: false
  resetPasswordAllowed
    description:
    - bool : reset Password Allowed.
    default: False
    required: false
  editUsernameAllowed
    description:
    - bool : edit Username Allowed.
    default: False
    required: false
  bruteForceProtected
    description:
    - integer : brute Force Protected.
    default: False
    required: false
  maxFailureWaitSeconds
    description:
    - integer : max Failure Wait Seconds.
    default: 900
    required: false
  minimumQuickLoginWaitSeconds
    description:
    - integer : minimum Quick Login Wait Seconds.
    default: 60
    required: false
  waitIncrementSeconds
    description:
    - integer : wait Increment Seconds.
    default: 60
    required: false
  quickLoginCheckMilliSeconds
    description:
    - integer : quick Login Check MilliSeconds.
    default: 1000
    required: false
  maxDeltaTimeSeconds
    description:
    - integer : max Delta Time Seconds.
    default: 43200
    required: false
  failureFactor
    description:
    - integer : failure Factor.
    default: 30
    required: false
  defaultRoles
    description:
    - list : default roles.
    default: [ "offline_access", "uma_authorization" ]
    required: false
  requiredCredentials
    description:
    - list : required Credentials.
    default: [ "password" ]
    required: false
  passwordPolicy
    description:
    - str : password Policy.
    default: hashIterations(20000)
    required: false
  otpPolicyType
    description:
    - str : otp Policy Type.
    default: totp
    required: false
  otpPolicyAlgorithm
    description:
    - str : otpPolicyAlgorithm.
    default: HmacSHA1
    required: false
  otpPolicyInitialCounter
    description:
    - integer : otpPolicyInitialCounter.
    default: 0
    required: false
  otpPolicyDigits
    description:
    - integer : otp Policy Digits.
    default: 6
    required: false
  otpPolicyLookAheadWindow
    description:
    - integer : otp Policy Look Ahead Window.
    default: 1
    required: false
  otpPolicyPeriod
    description:
    - integer : otp Policy Period.
    default: 30
    required: false
  smtpServer
    description:
    - dict : SMTP Server.
    default: {}
    required: false
  eventsEnabled
    description:
    - bool : events Enabled.
    default: False
    required: false
  eventsListeners
    description:
    - list : events Listeners.
    default: [ "jboss-logging" ]
    required: false
  enabledEventTypes
    description:
    - list : enabledEventTypes.
    default: [ ]
    required: false
  adminEventsEnabled
    description:
    - bool : admin Events Enabled.
    default: False
    required: false
  adminEventsDetailsEnabled
    description:
    - bool : admin Events Details Enabled.
    default: False
    required: false
  internationalizationEnabled
    description:
    - bool : internationalization Enabled.
    default: False
    required: false
  supportedLocales
    description:
    - list : supported Locales.
    default: [ ]
    required: false
  browserFlow
    description:
    - str : browser Flow.
    default: browser
    required: false
  registrationFlow
    description:
    - str : registrationFlow.
    default: registration
    required: false
  directGrantFlow
    description:
    - str : direct Grant Flow.
    default: direct grant
    required: false
  resetCredentialsFlow
    description:
    - integer : reset Credentials Flow.
    default: reset credentials
    required: false
  clientAuthenticationFlow
    description:
    - integer : client Authentication Flow.
    default: clients
    required: false
  attributes=dict(type='dict', default=None),
    description:
    - dict : attributes.
    default: None
    required: false
  browserSecurityHeaders
    description:
    - dict : browser Security Headers.
    default: None
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
  - module does not modify realm name.
'''

EXAMPLES = '''
# Create a realm realm1 with default settings.
- keycloak_realm:
    name: realm1 
    state: present

# Re-create the realm realm1
- keycloak_realm:
    name: realm1
    state: present
    force: yes

# Remove a the realm realm1.
- keycloak_realm:
    name: realm1
    state: absent
'''

RETURN = '''
result:
    ansible_facts: Representation JSON du REALM
    stderr: Message d'erreur s'il y en a un
    rc: Code de retour, 0 si succès, 1 si erreur
    changed: Retourne vrai si l'action a modifié de REALM, faux sinon.
'''
import requests
import json
import urllib
from ansible.module_utils.keycloak_utils import *
'''
def login(url, username, password):
    
Fonction : login
Description :
    Cette fonction permet de s'authentifier sur le serveur Keycloak.
Arguments :
    url :
        type : str
        description :
            url de base du serveur Keycloak        
    username :
        type : str
        description :
            identifiant à utiliser pour s'authentifier au serveur Keycloak        
    password :
        type : str
        description :
            Mot de passe pour s'authentifier au serveur Keycloak        
    
    # Login to Keycloak
    accessToken = ""
    body = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': 'admin-cli'
    }
    try:
        loginResponse = requests.post(url + '/auth/realms/master/protocol/openid-connect/token',data=body)
    
        loginData = loginResponse.json()
        accessToken = loginData['access_token']
    except requests.exceptions.RequestException, e:
        raise e
    except ValueError, e:
        raise e

    return accessToken
'''
def main():
    module = AnsibleModule(
        argument_spec = dict(
            realm=dict(type='str', required=True),
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
            name=dict(type='str', default=""),
            namehtml=dict(type='str', default=""),
            accessCodeLifespan=dict(type='int', default=60),
            accessCodeLifespanLogin=dict(type='int', default=1800),
            accessCodeLifespanUserAction=dict(type='int',default=300),
            notBefore = dict(type='int',default=0),
            revokeRefreshToken = dict(type='bool', default=False),
            accessTokenLifespan = dict(type='int', default=300),
            accessTokenLifespanForImplicitFlow = dict(type='int', default=900),
            ssoSessionIdleTimeout = dict(type='int', default=1800),
            ssoSessionMaxLifespan = dict(type='int', default=36000),
            offlineSessionIdleTimeout = dict(type='int', default=2592000),
            enabled = dict(type='bool', default=True),
            sslRequired = dict(type='str', default="external"),
            registrationAllowed = dict(type='bool', default=False),
            registrationEmailAsUsername = dict(type='bool', default=False),
            rememberMe = dict(type='bool', default=False),
            verifyEmail = dict(type='bool', default=False),
            loginWithEmailAllowed = dict(type='bool', default=True),
            duplicateEmailsAllowed = dict(type='bool', default=False),
            resetPasswordAllowed = dict(type='bool', default=False),
            editUsernameAllowed = dict(type='bool', default=False),
            bruteForceProtected = dict(type='bool', default=False),
            maxFailureWaitSeconds = dict(type='int', default=900),
            minimumQuickLoginWaitSeconds = dict(type='int', default=60),
            waitIncrementSeconds = dict(type='int', default=60),
            quickLoginCheckMilliSeconds = dict(type='int', default=1000),
            maxDeltaTimeSeconds = dict(type='int', default=43200),
            failureFactor = dict(type='int', default=30),
            defaultRoles = dict(type='list', default=[ "offline_access", "uma_authorization" ]),
            requiredCredentials = dict(type='list', default=[ "password" ]),
            passwordPolicy = dict(type='str', default="hashIterations(20000)"),
            otpPolicyType = dict(type='str', default="totp"),
            otpPolicyAlgorithm = dict(type='str', default="HmacSHA1"),
            otpPolicyInitialCounter = dict(type='int', default=0),
            otpPolicyDigits = dict(type='int', default=6),
            otpPolicyLookAheadWindow = dict(type='int', default=1),
            otpPolicyPeriod = dict(type='int', default=30),
            smtpServer = dict(type='dict', default={}),
            eventsEnabled = dict(type='bool', default=False),
            eventsListeners = dict(type='list', default=[ "jboss-logging" ]),
            enabledEventTypes = dict(type='list', default=[ ]),
            adminEventsEnabled= dict(type='bool', default=False),
            adminEventsDetailsEnabled= dict(type='bool', default=False),
            internationalizationEnabled= dict(type='bool', default=False),
            supportedLocales= dict(type='list', default=[ ]),
            browserFlow= dict(type='str', default="browser"),
            registrationFlow= dict(type='str', default="registration"),
            directGrantFlow= dict(type='str', default="direct grant"),
            resetCredentialsFlow= dict(type='str', default="reset credentials"),
            clientAuthenticationFlow= dict(type='str', default="clients"),
            state=dict(choices=["absent", "present"], default='present'),
            force=dict(type='bool', default=False),
            attributes=dict(type='dict', default=None),
            browserSecurityHeaders=dict(type='dict', default=None)
        ),
        supports_check_mode=True,
    )
    params = module.params.copy()
    params['force'] = module.boolean(module.params['force'])
    
    result = realm(params)
    
    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)
    
    
def realm(params):    
    defaultAttributes = dict(
        _browser_header = dict(
            contentSecurityPolicy = dict(type='unicode', default= "frame-src 'self'"), 
            xContentTypeOptions = dict(type='unicode', default="nosniff"), 
            xFrameOptions = dict(type='unicode', default = "SAMEORIGIN"), 
            xRobotsTag = dict(type='unicode', default = "none"), 
            xXSSProtection = dict(type='unicode', default="1; mode=block")
            ), 
        actionTokenGeneratedByAdminLifespan = dict(type='int', default=43200), 
        actionTokenGeneratedByUserLifespan = dict(type='int', default=300), 
        bruteForceProtected = dict(type='bool', default=False), 
        displayName = dict(type='unicode', default=params['name'].decode("utf-8")), 
        displayNameHtml = dict(type='unicode', default=params['namehtml'].decode("utf-8")), 
        failureFactor = dict(type='int', default=30), 
        maxDeltaTimeSeconds = dict(type='int', default=43200), 
        maxFailureWaitSeconds = dict(type='int', default=900), 
        minimumQuickLoginWaitSeconds = dict(type='int', default=60), 
        permanentLockout = dict(type='bool', default=False), 
        quickLoginCheckMilliSeconds = dict(type='int', default=1000), 
        waitIncrementSeconds = dict(type='int', default=60)
        )
    defaultBrowserSecurityHeaders = dict(
        contentSecurityPolicy = dict(type='unicode', default="frame-src 'self'"), 
        xContentTypeOptions = dict(type='unicode', default="nosniff"), 
        xFrameOptions = dict(type='unicode', default="SAMEORIGIN"), 
        xRobotsTag = dict(type='unicode', default="none"), 
        xXSSProtection = dict(type='unicode', default="1; mode=block")
        )

    url = params['url']
    username = params['username']
    password = params['password']
    state = params['state']
    force = params['force']
    masterRealm = 'master'

    # Créer un représentation du realm recu en paramètres
    newRealmRepresentation = {}
    newRealmRepresentation["id"] = params['realm'].decode("utf-8")
    newRealmRepresentation["realm"] = params['realm'].decode("utf-8")
    newRealmRepresentation["displayName"] = params['name'].decode("utf-8")
    newRealmRepresentation["displayNameHtml"] = params['namehtml'].decode("utf-8")
    newRealmRepresentation["accessCodeLifespan"] = params['accessCodeLifespan']
    newRealmRepresentation["accessCodeLifespanLogin"] = params['accessCodeLifespanLogin']
    newRealmRepresentation["accessCodeLifespanUserAction"] = params['accessCodeLifespanUserAction']
    newRealmRepresentation["notBefore"] = params['notBefore']
    newRealmRepresentation["revokeRefreshToken"] = params['revokeRefreshToken']
    newRealmRepresentation["accessTokenLifespan"] = params['accessTokenLifespan']
    newRealmRepresentation["accessTokenLifespanForImplicitFlow"] = params['accessTokenLifespanForImplicitFlow']
    newRealmRepresentation["ssoSessionIdleTimeout"] = params['ssoSessionIdleTimeout']
    newRealmRepresentation["ssoSessionMaxLifespan"] = params['ssoSessionMaxLifespan']
    newRealmRepresentation["offlineSessionIdleTimeout"] = params['offlineSessionIdleTimeout']
    newRealmRepresentation["enabled"] = params['enabled']
    newRealmRepresentation["sslRequired"] = params['sslRequired'].decode("utf-8")
    newRealmRepresentation["registrationAllowed"] = params['registrationAllowed']
    newRealmRepresentation["registrationEmailAsUsername"] = params['registrationEmailAsUsername']
    newRealmRepresentation["rememberMe"] = params['rememberMe']
    newRealmRepresentation["verifyEmail"] = params['verifyEmail']
    newRealmRepresentation["loginWithEmailAllowed"] = params['loginWithEmailAllowed']
    newRealmRepresentation["duplicateEmailsAllowed"] = params['duplicateEmailsAllowed']
    newRealmRepresentation["resetPasswordAllowed"] = params['resetPasswordAllowed']
    newRealmRepresentation["editUsernameAllowed"] = params['editUsernameAllowed']
    newRealmRepresentation["bruteForceProtected"] = params['bruteForceProtected']
    newRealmRepresentation["maxFailureWaitSeconds"] = params['maxFailureWaitSeconds']
    newRealmRepresentation["minimumQuickLoginWaitSeconds"] = params['minimumQuickLoginWaitSeconds']
    newRealmRepresentation["waitIncrementSeconds"] = params['waitIncrementSeconds']
    newRealmRepresentation["quickLoginCheckMilliSeconds"] = params['quickLoginCheckMilliSeconds']
    newRealmRepresentation["maxDeltaTimeSeconds"] = params['maxDeltaTimeSeconds']
    newRealmRepresentation["failureFactor"] = params['failureFactor']
    newRealmRepresentation["defaultRoles"] = params['defaultRoles']
    newRealmRepresentation["requiredCredentials"] = params['requiredCredentials']
    newRealmRepresentation["passwordPolicy"] = params['passwordPolicy'].decode("utf-8")
    newRealmRepresentation["otpPolicyType"] = params['otpPolicyType'].decode("utf-8")
    newRealmRepresentation["otpPolicyAlgorithm"] = params['otpPolicyAlgorithm'].decode("utf-8")
    newRealmRepresentation["otpPolicyInitialCounter"] = params['otpPolicyInitialCounter']
    newRealmRepresentation["otpPolicyDigits"] = params['otpPolicyDigits']
    newRealmRepresentation["otpPolicyLookAheadWindow"] = params['otpPolicyLookAheadWindow']
    newRealmRepresentation["otpPolicyPeriod"] = params['otpPolicyPeriod']
    #if len(params['smtpServer']):
    newRealmRepresentation["smtpServer"] = params['smtpServer']
    newRealmRepresentation["eventsEnabled"] = params['eventsEnabled']
    newRealmRepresentation["eventsListeners"] = params['eventsListeners']
    newRealmRepresentation["enabledEventTypes"] = params['enabledEventTypes']
    newRealmRepresentation["adminEventsEnabled"] = params['adminEventsEnabled']
    newRealmRepresentation["adminEventsDetailsEnabled"] = params['adminEventsDetailsEnabled']
    newRealmRepresentation["internationalizationEnabled"] = params['internationalizationEnabled']
    newRealmRepresentation["supportedLocales"] = params['supportedLocales']
    newRealmRepresentation["browserFlow"] = params['browserFlow'].decode("utf-8")
    newRealmRepresentation["registrationFlow"] = params['registrationFlow'].decode("utf-8")
    newRealmRepresentation["directGrantFlow"] = params['directGrantFlow'].decode("utf-8")
    newRealmRepresentation["resetCredentialsFlow"] = params['resetCredentialsFlow'].decode("utf-8")
    newRealmRepresentation["clientAuthenticationFlow"] = params['clientAuthenticationFlow'].decode("utf-8")
    # Stocker le REALM dans un body prèt a être posté
    data=json.dumps(newRealmRepresentation)
    rc = 0
    result = dict()
    changed = False

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
        # Vérifier si le REALM existe sur le serveur Keycloak
        #getResponse = requests.get(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers={'Authorization' : bearerHeader})
        getResponse = requests.get(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers=headers)
    except requests.HTTPError, e:
        getStatusCode = getResponse.status_code
    except:
        getStatusCode = 0
    else:
        getStatusCode = getResponse.status_code
        
    
   
    if (getStatusCode == 404): # Le realm n'existe pas
        # Creer le realm
        
        if (state == 'present'): # Si le status est présent
            try:
                # Créer le REALM
                #postResponse = requests.post(url + "/auth/admin/realms", headers={'Authorization' : bearerHeader, 'Content-type': 'application/json'}, data=data)
                postResponse = requests.post(url + "/auth/admin/realms", headers=headers, data=data)
                # Obtenir le nouveau REALM créé
                #getResponse = requests.get(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers={'Authorization' : bearerHeader})
                getResponse = requests.get(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers=headers)
                realmRepresentation = getResponse.json()
                changed = True
                fact = dict(
                    realm = realmRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
            except requests.exceptions.RequestException, e:
                result = dict(
                    realm    = newRealmRepresentation["id"],
                    stderr   = 'post realm: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
            except ValueError, e:
                result = dict(
                    realm    = newRealmRepresentation["id"],
                    stderr   = 'post realm: ' + str(e),
                    rc       = 1,
                    changed  = changed
                    )
        else: # Sinon, le status est absent
            result = dict(
                realm    = newRealmRepresentation["id"],
                stdout   = 'absent',
                rc       = 0,
                changed  = changed
            )
                
    elif (getStatusCode == 200):  # Le realm existe déjà
        try:
            if (state == 'present'): # si le status est présent
                # Obtenir le REALM exitant
                realmRepresentation = getResponse.json()
                if force: # Si l'option force est sélectionné
                    # Supprimer le REALM existant
                    #deleteResponse = requests.delete(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers={'Authorization' : bearerHeader, 'Content-type': 'application/json'})
                    deleteResponse = requests.delete(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers={'Authorization' : bearerHeader, 'Content-type': 'application/json'})
                    changed = True
                    # Créer le nouveau REALM
                    #postResponse = requests.post(url + "/auth/admin/realms", headers={'Authorization' : bearerHeader, 'Content-type': 'application/json'}, data=data)
                    postResponse = requests.post(url + "/auth/admin/realms", headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    # Comparer les realms
                    if (isDictEquals(newRealmRepresentation, realmRepresentation)): # Si le nouveau REALM n'introduit pas de modification au REALM existant
                        # Ne rien changer
                        changed = False
                    else: # Si le REALM doit être modifié
                        # Mettre à jour le REALM sur le serveur Keycloak
                        #updateResponse = requests.put(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers={'Authorization' : bearerHeader, 'Content-type': 'application/json'}, data=data)
                        updateResponse = requests.put(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers=headers, data=data)
                        changed = True
                        
                # Obtenir sa représentation JSON sur le serveur Keycloak                        
                #getResponse = requests.get(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers={'Authorization' : bearerHeader})
                getResponse = requests.get(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers=headers)
                realmRepresentation = getResponse.json()
                
                fact = dict(
                    realm = realmRepresentation)
                result = dict(
                    ansible_facts = fact,
                    rc = 0,
                    changed = changed
                    )
                    
            else: # Le status est absent
                # Supprimer le REALM
                #deleteResponse = requests.delete(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers={'Authorization' : bearerHeader, 'Content-type': 'application/json'})
                deleteResponse = requests.delete(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers=headers)
                changed = True
                result = dict(
                    realm    = newRealmRepresentation["id"],
                    stdout   = 'deleted',
                    rc       = 0,
                    changed  = changed
                )
        except requests.exceptions.RequestException, e:
            result = dict(
                realm    = newRealmRepresentation["id"],
                stderr   = 'put or delete realm: ' + str(e),
                rc       = 1,
                changed  = changed
                )
        except ValueError, e:
            result = dict(
                realm    = newRealmRepresentation["id"],
                stderr   = 'put or delete realm: ' + str(e),
                rc       = 1,
                changed  = changed
                )
    else: # Le status HTTP du GET n'est ni 200 ni 404, c'est considéré comme une erreur.
        rc = 1
        result = dict(
            realm = newRealmRepresentation["id"],
            stderr = getStatusCode,
            rc = 1,
            changed = changed
            )

    return result

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
