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
module: keycloak_realm
short_description: Configure a realm in Keycloak
description:
  - This module creates, removes or update Keycloak realms.
version_added: "2.3"
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
  loginTheme:
    description:
    - Theme to use at logon for this realm.
    required: false
  adminTheme:
    description:
    - Theme to use for this realm's admin console.
    required: false
  emailTheme:
    description:
    - Theme to use for this realm's emails.
    required: false
  accountTheme:
    description:
    - Theme to use for this realm's accounts.
    required: false
  internationalizationEnabled:
    description:
    - Is internationalization enabled for this realm?
    required: false
  supportedLocales:
    description:
    - List of supported languages for the realm.
    required: false
  defaultLocale:
    description:
    - If multiple locales are suported, which one will be used as default language.
    required: false
  accessCodeLifespan:
    description:
    - access code lifespan.
    default: 60
    required: false
  accessCodeLifespanLogin:
    description: 
    - access code lifespan login.
    default: 1800
    required: false
  accessCodeLifespanUserAction:
    description:
    - access code lifespan user action.
    default: 300
    required: false
  accessTokenLifespan:
    description:
    - Access token lifespan.
    default: 300
    required: false
  accessTokenLifespanForImplicitFlow:
    description:
    - Access token lifespan for implicit flow.
    default: 900
    required: false
  notBefore:
    description:
    - Not Before.
    default: 900
    required: false
  revokeRefreshToken:
    description:
    - Revoke Refresh Token.
    default: 900
    required: false
  ssoSessionMaxLifespan:
    description:
    - Sso Session Max Lifespan.
    default: 36000
    required: false
  offlineSessionIdleTimeout:
    description:
    - Offline Session Idle Timeout.
    default: 2592000
    required: false
  enabled:
    description:
    - Enabled.
    default: True
    required: false
  sslRequired:
    description:
    - Ssl Required.
    default: external
    required: false
  registrationAllowed:
    description:
    - Registration Allowed.
    default: False
    required: false
  registrationEmailAsUsername:
    description:
    - Registration Email As Username.
    default: False
    required: false
  rememberMe:
    description:
    - Remember me.
    default: False
    required: false
  verifyEmail:
    description:
    - Verify Email.
    default: False
    required: false
  loginWithEmailAllowed:
    description:
    - Login With Email Allowed.
    default: True
    required: false
  duplicateEmailsAllowed:
    description:
    - Duplicate Emails Allowed.
    default: 900
    required: false
  resetPasswordAllowed:
    description:
    - Reset Password Allowed.
    default: False
    required: false
  editUsernameAllowed:
    description:
    - Edit Username Allowed.
    default: False
    required: false
  bruteForceProtected:
    description:
    - Brute Force Protected.
    default: False
    required: false
  permanentLockout:
    description:
    - Permanent Lockout.
    default: False
    required: false
  maxFailureWaitSeconds:
    description:
    - Max Failure Wait Seconds.
    default: 900
    required: false
  minimumQuickLoginWaitSeconds:
    description:
    - Minimum Quick Login Wait Seconds.
    default: 60
    required: false
  waitIncrementSeconds:
    description:
    - Wait Increment Seconds.
    default: 60
    required: false
  quickLoginCheckMilliSeconds:
    description:
    - Quick Login Check MilliSeconds.
    default: 1000
    required: false
  maxDeltaTimeSeconds:
    description:
    - Max Delta Time Seconds.
    default: 43200
    required: false
  failureFactor:
    description:
    - Failure Factor.
    default: 30
    required: false
  defaultRoles:
    description:
    - Default roles.
    default: [ "offline_access", "uma_authorization" ]
    required: false
  requiredCredentials:
    description:
    - Required Credentials.
    default: [ "password" ]
    required: false
  passwordPolicy:
    description:
    - Password Policy.
    default: hashIterations(20000)
    required: false
  otpPolicyType:
    description:
    - Otp Policy Type.
    default: totp
    required: false
  otpPolicyAlgorithm:
    description:
    - Otp Policy Algorithm.
    default: HmacSHA1
    required: false
  otpPolicyInitialCounter:
    description:
    - Otp Policy Initial Counter.
    default: 0
    required: false
  otpPolicyDigits:
    description:
    - Otp Policy Digits.
    default: 6
    required: false
  otpPolicyLookAheadWindow:
    description:
    - Otp Policy Look Ahead Window.
    default: 1
    required: false
  otpPolicyPeriod:
    description:
    - Otp Policy Period.
    default: 30
    required: false
  smtpServer:
    description:
    - SMTP Server.
    default: {}
    required: false
  eventsConfig:
    description:
    - Event configuration for the realm.
    required: false
  browserFlow:
    description:
    - Browser Flow.
    default: browser
    required: false
  registrationFlow:
    description:
    - Registration Flow.
    default: registration
    required: false
  directGrantFlow:
    description:
    - Direct Grant Flow.
    default: direct grant
    required: false
  resetCredentialsFlow:
    description:
    - Reset Credentials Flow.
    default: reset credentials
    required: false
  clientAuthenticationFlow:
    description:
    - Client Authentication Flow.
    default: clients
    required: false
  attributes:
    description:
    - Attributes.
    default: None
    required: false
  browserSecurityHeaders:
    description:
    - Browser Security Headers.
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
    - name: Create a realm
      keycloak_realm:
        realm: realm1
        name: "realm1"
        namehtml: "The first Realm"
        url: "http://localhost:8080"
        username: "admin"
        password: "admin"
        smtpServer: 
          replyToDisplayName: root
          starttls: ""
          auth: ""
          port: "25"
          host: "localhost"
          replyTo: "root@localhost"
          from: "root@localhost"
          fromDisplayName: "local"
          envelopeFrom: "root@localhost"
          ssl: ""
        eventsConfig:
          eventsEnabled: true
          eventsListeners :
            - jboss-logging
            - sx5-event-listener
          adminEventsEnabled: true
          adminEventsDetailsEnabled: false
        state : present

    - name: Re-create the realm realm1
      keycloak_realm:
        realm: realm1
        name: "realm1"
        namehtml: "The first Realm"
        url: "http://localhost:8080"
        username: "admin"
        password: "admin"
        state : present
        force: yes

    - name: Remove a the realm realm1.
      keycloak_realm:
        name: realm1
        state: absent
'''

RETURN = '''
ansible_facts:
  description: JSON representation for the REALM.
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
  description: Return True if the operation changed the REALM on the keycloak server, false otherwise.
  returned: always
  type: bool
'''

import json
import urllib
from ansible.module_utils.keycloak_utils import * 

def main():
    module = AnsibleModule(
        argument_spec = dict(
            realm=dict(type='str', required=True),
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(required=True),
            name=dict(type='str', default=""),
            namehtml=dict(type='str', default=""),
            loginTheme=dict(type="str"),
            adminTheme=dict(type="str"),
            emailTheme=dict(type="str"),
            accountTheme=dict(type="str"),
            internationalizationEnabled=dict(type="bool"),
            supportedLocales=dict(type="list"),
            defaultLocale=dict(type="str"),
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
            permanentLockout = dict(type='bool', default=False),
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
            eventsConfig = dict(type='dict'),
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
        displayName = dict(type='unicode', default=params['name'].decode("utf-8")), 
        displayNameHtml = dict(type='unicode', default=params['namehtml'].decode("utf-8")), 
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
    if "loginTheme" in params and params["loginTheme"] is not None:
        newRealmRepresentation["loginTheme"] = params["loginTheme"].decode("utf-8")
    if "adminTheme" in params and params["adminTheme"] is not None:
        newRealmRepresentation["adminTheme"] = params["adminTheme"].decode("utf-8")
    if "emailTheme" in params and params["emailTheme"] is not None:
        newRealmRepresentation["emailTheme"] = params["emailTheme"].decode("utf-8")
    if "accountTheme" in params and params["accountTheme"] is not None:
        newRealmRepresentation["accountTheme"] = params["accountTheme"].decode("utf-8")
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
    newRealmRepresentation["permanentLockout"] = params['permanentLockout']
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
    newRealmRepresentation["smtpServer"] = params['smtpServer']
    if "supportedLocales" in params and params["supportedLocales"] is not None:
        if "internationalizationEnabled" in params and params["internationalizationEnabled"] is not None:
            newRealmRepresentation["internationalizationEnabled"] = params["internationalizationEnabled"]
        else:
            newRealmRepresentation["internationalizationEnabled"] = True
        newRealmRepresentation["supportedLocales"] = params["supportedLocales"]
        if "defaultLocale" in params and params["defaultLocale"]:
            newRealmRepresentation["defaultLocale"] = params["defaultLocale"].decode("utf-8")
    else:
        newRealmRepresentation["internationalizationEnabled"] = False
    newRealmRepresentation["browserFlow"] = params['browserFlow'].decode("utf-8")
    newRealmRepresentation["registrationFlow"] = params['registrationFlow'].decode("utf-8")
    newRealmRepresentation["directGrantFlow"] = params['directGrantFlow'].decode("utf-8")
    newRealmRepresentation["resetCredentialsFlow"] = params['resetCredentialsFlow'].decode("utf-8")
    newRealmRepresentation["clientAuthenticationFlow"] = params['clientAuthenticationFlow'].decode("utf-8")
    
    # Stocker le REALM dans un body prèt a être posté
    data=json.dumps(newRealmRepresentation)
    # Read Events configuration for the Realm
    newEventsConfig = params["eventsConfig"] if "eventsConfig" in params and params["eventsConfig"] is not None else None
    
    rc = 0
    result = dict()
    changed = False
    realmExists = False
    realmRepresentation = {}
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
        # Vérifier si le REALM existe sur le serveur Keycloak
        getResponse = requests.get(url + "/auth/admin/realms/", headers=headers)
        listRealms = getResponse.json()
        
        for realm in listRealms:
            if realm['id'] == newRealmRepresentation["id"]:
                realmExists = True
                realmRepresentation = realm
                break
    except Exception, e:
        result = dict(
            stderr   = 'first realm get: ' + str(e),
            rc       = 1,
            changed  = changed
            )
        return result
        
    if not realmExists: # Le realm n'existe pas
        # Creer le realm
        
        if (state == 'present'): # Si le status est présent
            try:
                fact = dict()
                # Créer le REALM
                postResponse = requests.post(url + "/auth/admin/realms/", headers=headers, data=data)
                # if there is a configuration for Events
                if newEventsConfig is not None:
                    data=json.dumps(newEventsConfig)
                    # Update the Config
                    putResponse = requests.put(url + "/auth/admin/realms/" + newRealmRepresentation["id"] + "/events/config", headers=headers, data=data)
                    # Get the actual config from Keycloak server
                    getResponse = requests.get(url + "/auth/admin/realms/" + newRealmRepresentation["id"] + "/events/config", headers=headers)
                    eventsConfig = getResponse.json()
                    fact["eventsConfig"] = eventsConfig
                # Obtenir le nouveau REALM créé
                getResponse = requests.get(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers=headers)
                realmRepresentation = getResponse.json()
                fact["realm"] = realmRepresentation
                changed = True
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
                
    else:  # Le realm existe déjà
        try:
            if (state == 'present'): # si le status est présent
                # Obtenir le REALM exitant
                #realmRepresentation = getResponse.json()
                if force: # Si l'option force est sélectionné
                    # Supprimer le REALM existant
                    deleteResponse = requests.delete(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers={'Authorization' : bearerHeader, 'Content-type': 'application/json'})
                    changed = True
                    # Créer le nouveau REALM
                    postResponse = requests.post(url + "/auth/admin/realms", headers=headers, data=data)
                else: # Si l'option force n'est pas sélectionné
                    # Comparer les realms
                    if (isDictEquals(newRealmRepresentation, realmRepresentation)): # Si le nouveau REALM n'introduit pas de modification au REALM existant
                        # Ne rien changer
                        changed = False
                    else: # Si le REALM doit être modifié
                        # Mettre à jour le REALM sur le serveur Keycloak
                        updateResponse = requests.put(url + "/auth/admin/realms/" + newRealmRepresentation["id"], headers=headers, data=data)
                        changed = True
                        
                # Obtenir sa nouvelle représentation JSON sur le serveur Keycloak                        
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

    return result

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
