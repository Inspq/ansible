import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_authentication import *

class KeycloakGroupTestCase(unittest.TestCase):
 
    def test_create_authentication_flow(self):
        toCreate = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Copy of first broker login",
            "copyFrom": "first broker login",
            "authenticationConfig": {
                "alias": "name",
                "config": {
                    "defaultProvider": "value"
                }
            },
            "authenticationExecutions":{
                "providerId": "identity-provider-redirector",
                "requirement": "ALTERNATIVE"
            }, 
            "state":"present",
            "force":False
        }

        results = authentication(toCreate)
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toCreate["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toCreate["alias"] )
        self.assertTrue(results['changed'])
        
    def test_create_authentication_flow_without_copy(self):
        toCreate = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "No Copy broker login",
            "providerId": "basic-flow",
            "authenticationConfig": {
                "alias": "name",
                "config": {
                    "defaultProvider": "value"
                }
            },
            "authenticationExecutions":{
                "providerId": "identity-provider-redirector",
                "requirement": "ALTERNATIVE"
            }, 
            "state":"present",
            "force":False
        }

        results = authentication(toCreate)
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toCreate["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toCreate["alias"] )
        self.assertTrue(results['changed'])

    def test_authentication_flow_not_changed(self):
        toDoNotChange = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Copy of first broker login 2",
            "copyFrom": "first broker login",
            "authenticationConfig": {
                "alias": "name",
                "config": {
                    "defaultProvider": "value"
                }
            },
            "authenticationExecutions":{
                "providerId": "identity-provider-redirector",
                "requirement": "ALTERNATIVE"
            }, 
            "state":"present",
            "force":False
        }

        authentication(toDoNotChange)
        results = authentication(toDoNotChange)
        
        self.assertFalse(results['changed'])


    def test_modify_authentication_flow(self):
        toChange = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Copy of first broker login 3",
            "copyFrom": "first broker login",
            "authenticationConfig": {
                "alias": "name",
                "config": {
                    "defaultProvider": "value"
                }
            },
            "authenticationExecutions":{
                "providerId": "identity-provider-redirector",
                "requirement": "ALTERNATIVE"
            }, 
            "state":"present",
            "force":True
        }
        authentication(toChange)
        toChange["authenticationConfig"]["config"]["defaultProvider"] = "modified value"
        results = authentication(toChange)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toChange["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toChange["alias"] )
        self.assertEquals(results["ansible_facts"]["authenticationConfig"]["config"]["defaultProvider"], toChange["authenticationConfig"]["config"]["defaultProvider"], "config: " + str(results["ansible_facts"]["authenticationConfig"]["config"]) + " : " + str(toChange["authenticationConfig"]["config"]))
        
    def test_delete_authentication_flow(self):
        toDelete = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Copy of first broker login 4",
            "copyFrom": "first broker login",
            "authenticationConfig": {
                "alias": "name",
                "config": {
                    "defaultProvider": "value"
                }
            },
            "authenticationExecutions":{
                "providerId": "identity-provider-redirector",
                "requirement": "ALTERNATIVE"
            }, 
            "state":"present",
            "force":False
        }

        authentication(toDelete)
        toDelete = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Copy of first broker login 4",
            "state":"absent",
            "force":False
        }
        results = authentication(toDelete)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'authentication flow has been deleted')

    def test_delete_inexisting_authentication_flow(self):
        toDelete = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Non existing first broker login",
            "state":"absent",
            "force":False
        }
        results = authentication(toDelete)
        self.assertFalse(results['changed'])
        self.assertEqual(results['stdout'], toDelete["alias"] + ' absent', 'authentication flow has been deleted')
