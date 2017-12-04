import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_realm import *


class KeycloakRealmTestCase(unittest.TestCase):
 
    def test_create_realm(self):
        toCreate = dict(
            realm='test',
            url='http://localhost:18081',
            username='admin',
            password='admin',
            name='test',
            namehtml='ceci est un test',
            accessCodeLifespan=60,
            accessCodeLifespanLogin=1800,
            accessCodeLifespanUserAction=300,
            notBefore = 0,
            revokeRefreshToken = False,
            accessTokenLifespan = 300,
            accessTokenLifespanForImplicitFlow = 900,
            ssoSessionIdleTimeout = 1800,
            ssoSessionMaxLifespan = 36000,
            offlineSessionIdleTimeout = 2592000,
            enabled = True,
            sslRequired = "external",
            registrationAllowed = False,
            registrationEmailAsUsername = False,
            rememberMe = False,
            verifyEmail = False,
            loginWithEmailAllowed = True,
            duplicateEmailsAllowed = False,
            resetPasswordAllowed = False,
            editUsernameAllowed = False,
            bruteForceProtected = False,
            maxFailureWaitSeconds = 900,
            minimumQuickLoginWaitSeconds = 60,
            waitIncrementSeconds = 60,
            quickLoginCheckMilliSeconds = 1000,
            maxDeltaTimeSeconds = 43200,
            failureFactor = 30,
            defaultRoles = [ "offline_access", "uma_authorization" ],
            requiredCredentials = [ "password" ],
            passwordPolicy = "hashIterations(20000)",
            otpPolicyType = "totp",
            otpPolicyAlgorithm = "HmacSHA1",
            otpPolicyInitialCounter = 0,
            otpPolicyDigits = 6,
            otpPolicyLookAheadWindow = 1,
            otpPolicyPeriod = 30,
            smtpServer = {
                "replyToDisplayName": "root",
                "starttls": "",
                "auth": "",
                "port": "25",
                "host": "localhost",
                "replyTo": "root@localhost",
                "fromDisplayName": "local",
                "envelopeFrom": "root@localhost",
                "ssl": "",
                "smtpServer.from": "root@localhost"
            },
            eventsConfig = {
                "eventsEnabled": True,
                "eventsListeners": [ "jboss-logging" ],
                "enabledEventTypes": ["SEND_RESET_PASSWORD", "UPDATE_TOTP", "REMOVE_TOTP", "REVOKE_GRANT", "LOGIN_ERROR", "CLIENT_LOGIN", "RESET_PASSWORD_ERROR", "IMPERSONATE_ERROR", "CODE_TO_TOKEN_ERROR", "CUSTOM_REQUIRED_ACTION", "UPDATE_PROFILE_ERROR", "IMPERSONATE", "LOGIN", "UPDATE_PASSWORD_ERROR", "REGISTER", "LOGOUT", "CLIENT_REGISTER", "UPDATE_PASSWORD", "FEDERATED_IDENTITY_LINK_ERROR", "CLIENT_DELETE", "IDENTITY_PROVIDER_FIRST_LOGIN", "VERIFY_EMAIL", "CLIENT_DELETE_ERROR", "CLIENT_LOGIN_ERROR", "REMOVE_FEDERATED_IDENTITY_ERROR", "EXECUTE_ACTIONS", "SEND_IDENTITY_PROVIDER_LINK_ERROR", "SEND_VERIFY_EMAIL", "EXECUTE_ACTIONS_ERROR", "REMOVE_FEDERATED_IDENTITY", "IDENTITY_PROVIDER_POST_LOGIN", "UPDATE_EMAIL", "REGISTER_ERROR", "REVOKE_GRANT_ERROR", "LOGOUT_ERROR", "UPDATE_EMAIL_ERROR", "CLIENT_UPDATE_ERROR", "UPDATE_PROFILE", "FEDERATED_IDENTITY_LINK", "CLIENT_REGISTER_ERROR", "SEND_VERIFY_EMAIL_ERROR", "SEND_IDENTITY_PROVIDER_LINK", "RESET_PASSWORD", "REMOVE_TOTP_ERROR", "VERIFY_EMAIL_ERROR", "SEND_RESET_PASSWORD_ERROR", "CLIENT_UPDATE", "IDENTITY_PROVIDER_POST_LOGIN_ERROR", "CUSTOM_REQUIRED_ACTION_ERROR", "UPDATE_TOTP_ERROR", "CODE_TO_TOKEN", "IDENTITY_PROVIDER_FIRST_LOGIN_ERROR"],
                "adminEventsEnabled": True,
                "adminEventsDetailsEnabled": True},
            internationalizationEnabled = False,
            supportedLocales= [  ],
            browserFlow= "browser",
            registrationFlow= "registration",
            directGrantFlow= "direct grant",
            resetCredentialsFlow= "reset credentials",
            clientAuthenticationFlow= "clients",
            state='present',
            force=False,
            attributes=None,
            browserSecurityHeaders=None
        )        
    
        results = realm(toCreate)
        print("results: " + str(results))
        self.assertEqual(results['rc'],0,'Return code : ' + str(results['rc']))
        #self.assertTrue(results['ansible_facts']['realm']['enabled'])
        self.assertTrue(results["changed"], "Changed: " + str(results["changed"]))
        self.assertTrue(results["ansible_facts"]["realm"]["eventsEnabled"], "eventsEnabled: " + str(results["ansible_facts"]["realm"]["eventsEnabled"]))
        self.assertTrue(results["ansible_facts"]["realm"]["adminEventsEnabled"], "adminEventsEnabled: " + str(results["ansible_facts"]["realm"]["adminEventsEnabled"]))
        self.assertTrue(results["ansible_facts"]["realm"]["adminEventsDetailsEnabled"], "adminEventsDetailsEnabled: " + str(results["ansible_facts"]["realm"]["adminEventsDetailsEnabled"]))
        
    def test_modify_realm(self):
        toModifiy = dict(
            realm='test1',
            url='http://localhost:18081',
            username='admin',
            password='admin',
            name='test1',
            namehtml='ceci est un test',
            accessCodeLifespan=60,
            accessCodeLifespanLogin=1800,
            accessCodeLifespanUserAction=300,
            notBefore = 0,
            revokeRefreshToken = False,
            accessTokenLifespan = 300,
            accessTokenLifespanForImplicitFlow = 900,
            ssoSessionIdleTimeout = 1800,
            ssoSessionMaxLifespan = 36000,
            offlineSessionIdleTimeout = 2592000,
            enabled = True,
            sslRequired = "external",
            registrationAllowed = False,
            registrationEmailAsUsername = False,
            rememberMe = False,
            verifyEmail = False,
            loginWithEmailAllowed = True,
            duplicateEmailsAllowed = False,
            resetPasswordAllowed = False,
            editUsernameAllowed = False,
            bruteForceProtected = False,
            maxFailureWaitSeconds = 900,
            minimumQuickLoginWaitSeconds = 60,
            waitIncrementSeconds = 60,
            quickLoginCheckMilliSeconds = 1000,
            maxDeltaTimeSeconds = 43200,
            failureFactor = 30,
            defaultRoles = [ "offline_access", "uma_authorization" ],
            requiredCredentials = [ "password" ],
            passwordPolicy = "hashIterations(20000)",
            otpPolicyType = "totp",
            otpPolicyAlgorithm = "HmacSHA1",
            otpPolicyInitialCounter = 0,
            otpPolicyDigits = 6,
            otpPolicyLookAheadWindow = 1,
            otpPolicyPeriod = 30,
            smtpServer = {
                "replyToDisplayName": "root",
                "starttls": "",
                "auth": "",
                "port": "25",
                "host": "localhost",
                "replyTo": "root@localhost",
                "fromDisplayName": "local",
                "envelopeFrom": "root@localhost",
                "ssl": "",
                "smtpServer.from": "root@localhost"
            },
            eventsEnabled = False,
            eventsListeners = [ "jboss-logging" ],
            enabledEventTypes = [],
            adminEventsEnabled= False,
            adminEventsDetailsEnabled = False,
            internationalizationEnabled = False,
            supportedLocales= [ ],
            browserFlow= "browser",
            registrationFlow= "registration",
            directGrantFlow= "direct grant",
            resetCredentialsFlow= "reset credentials",
            clientAuthenticationFlow= "clients",
            state='present',
            force=False,
            attributes=None,
            browserSecurityHeaders=None
        )        
        realm(toModifiy)
        toModifiy["namehtml"] = "New name"
        results = realm(toModifiy)
        
        self.assertEqual(results['rc'],0,'Return code: ' + str(results['rc']))
        self.assertEqual(results['ansible_facts']['realm']['displayNameHtml'], toModifiy["namehtml"], "namehtml: " + results['ansible_facts']['realm']['displayNameHtml'])
        
    def test_delete_realm(self):
        toDelete = dict(
            realm='test2',
            url='http://localhost:18081',
            username='admin',
            password='admin',
            name='test2',
            namehtml='ceci est un test',
            accessCodeLifespan=60,
            accessCodeLifespanLogin=1800,
            accessCodeLifespanUserAction=300,
            notBefore = 0,
            revokeRefreshToken = False,
            accessTokenLifespan = 300,
            accessTokenLifespanForImplicitFlow = 900,
            ssoSessionIdleTimeout = 1800,
            ssoSessionMaxLifespan = 36000,
            offlineSessionIdleTimeout = 2592000,
            enabled = True,
            sslRequired = "external",
            registrationAllowed = False,
            registrationEmailAsUsername = False,
            rememberMe = False,
            verifyEmail = False,
            loginWithEmailAllowed = True,
            duplicateEmailsAllowed = False,
            resetPasswordAllowed = False,
            editUsernameAllowed = False,
            bruteForceProtected = False,
            maxFailureWaitSeconds = 900,
            minimumQuickLoginWaitSeconds = 60,
            waitIncrementSeconds = 60,
            quickLoginCheckMilliSeconds = 1000,
            maxDeltaTimeSeconds = 43200,
            failureFactor = 30,
            defaultRoles = [ "offline_access", "uma_authorization" ],
            requiredCredentials = [ "password" ],
            passwordPolicy = "hashIterations(20000)",
            otpPolicyType = "totp",
            otpPolicyAlgorithm = "HmacSHA1",
            otpPolicyInitialCounter = 0,
            otpPolicyDigits = 6,
            otpPolicyLookAheadWindow = 1,
            otpPolicyPeriod = 30,
            smtpServer = {
                "replyToDisplayName": "root",
                "starttls": "",
                "auth": "",
                "port": "25",
                "host": "localhost",
                "replyTo": "root@localhost",
                "fromDisplayName": "local",
                "envelopeFrom": "root@localhost",
                "ssl": "",
                "smtpServer.from": "root@localhost"
            },
            eventsEnabled = False,
            eventsListeners = [ "jboss-logging" ],
            enabledEventTypes = [],
            adminEventsEnabled= False,
            adminEventsDetailsEnabled = False,
            internationalizationEnabled = False,
            supportedLocales= [ ],
            browserFlow= "browser",
            registrationFlow= "registration",
            directGrantFlow= "direct grant",
            resetCredentialsFlow= "reset credentials",
            clientAuthenticationFlow= "clients",
            state='present',
            force=False,
            attributes=None,
            browserSecurityHeaders=None
        )        
        realm(toDelete)
        toDelete["state"] = "absent"
        results = realm(toDelete)
        self.assertEqual(results['rc'],0,'Code de retour: ' + str(results['rc']))
        self.assertEqual(results['stdout'], 'deleted', 'realm has been deleted')
