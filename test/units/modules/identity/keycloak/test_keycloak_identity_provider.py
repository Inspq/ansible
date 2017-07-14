import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_identity_provider import *


class KeycloakIdentityProviderTestCase(unittest.TestCase):
 
    def test_create_idp(self):
        toCreate = dict(
            username = "admin", 
            password = "admin",
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
                        claim = "test"
                        )
                    ), 
                dict(
                    name ="test2",
                    config = dict(
                        claim = "test2"
                        )
                    )
                ],
            state = "present",
            force = False
        )
        toCreate['mappers'][0]['config']['user.attribute'] = "lastname"
        toCreate['mappers'][1]['config']['user.attribute'] = "firstname"
        results = idp(toCreate)
        print str(results['ansible_facts'])
        self.assertTrue(results['ansible_facts']['idp']['enabled'])
        
        self.assertTrue(results['ansible_facts']['mappers'][0]['config']['user.attribute'])
        self.assertTrue(results['ansible_facts']['mappers'][0]['config']['claim'])
        self.assertTrue(results['ansible_facts']['mappers'][1]['config']['user.attribute'])
        self.assertTrue(results['ansible_facts']['mappers'][1]['config']['claim'])
        
    def test_delete_idp(self):
        toDelete = dict(
            username = "admin", 
            password = "admin",
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
                        claim = "test" 
                        )
                    ), 
                dict(
                    name ="test2",
                    config = dict(
                        claim = "test2"
                        )
                    )
                ],
            state = "absent",
            force = False
        )        
        toDelete['mappers'][0]['config']['user.attribute'] = "lastname"
        toDelete['mappers'][1]['config']['user.attribute'] = "firstname"
        results = idp(toDelete)
        self.assertEqual(results['stdout'], 'deleted', 'idp has been deleted')
