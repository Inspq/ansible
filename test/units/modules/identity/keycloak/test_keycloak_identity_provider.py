import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_identity_provider import *


class KeycloakIdentityProviderTestCase(unittest.TestCase):
 
    def test_create_idp(self):
        toCreate = dict(
            username = "admin", 
            password = "Pan0rama",
            realm = "master",
            url = "http://localhost:18081",
            alias = "test",
            providerId = "oidc",
            displayName = "Test",
            enabled = True,
            updateProfileFirstLoginMode="on",
            trustEmail=False,
            storeToken = True,
            addReadTokenRoleOnCreate = True,
            authenticateByDefault = False,
            linkOnly = False,
            firstBrokerLoginFlowAlias = "first broker login",
            config = dict(
                openIdConfigurationUrl = "https://accounts.google.com/.well-known/openid-configuration",
                clientId = "test",
                clientSecret = "test",
                defaultScope = "openid email profile",
                disableUserInfo = "false"
            ),
            mappers = [ 
                dict(
                    name = "test", 
                    config = dict(
                        claim = "test", 
                        user = dict(attribute = "lastName")
                        )
                    ), 
                dict(
                    name ="test2",
                    config = dict(
                        claim = "test2",
                        user = dict(attribute = "firstName")
                        )
                    )
                ],
            state = "present",
            force = False
        )
    
        results = idp(toCreate)
        self.assertTrue(results['ansible_facts']['idp']['enabled'])
        
    def test_delete_idp(self):
        toDelete = dict(
            username = "admin", 
            password = "Pan0rama",
            realm = "master",
            url = "http://localhost:18081",
            alias = "test",
            providerId = "oidc",
            displayName = "Test",
            enabled = True,
            updateProfileFirstLoginMode="on",
            trustEmail=False,
            storeToken = True,
            addReadTokenRoleOnCreate = True,
            authenticateByDefault = False,
            linkOnly = False,
            firstBrokerLoginFlowAlias = "first broker login",
            config = dict(
                openIdConfigurationUrl = "https://accounts.google.com/.well-known/openid-configuration",
                clientId = "test",
                clientSecret = "test",
                defaultScope = "openid email profile",
                disableUserInfo = "false"
            ),
            mappers = [ 
                dict(
                    name = "test", 
                    config = dict(
                        claim = "test", 
                        user = dict(attribute = "lastName")
                        )
                    ), 
                dict(
                    name ="test2",
                    config = dict(
                        claim = "test2",
                        user = dict(attribute = "firstName")
                        )
                    )
                ],
            state = "absent",
            force = False
        )        
        
        results = idp(toDelete)
        self.assertEqual(results['stdout'], 'deleted', 'idp has been deleted')
