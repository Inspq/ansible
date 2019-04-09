import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_authentication import *

class KeycloakAuthenticationTestCase(unittest.TestCase):
 
    def test_create_authentication_flow(self):
        toCreate = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Copy of first broker login",
            "copyFrom": "first broker login",
            "authenticationExecutions":[
                {
                    "providerId": "identity-provider-redirector",
                    "requirement": "ALTERNATIVE",
                    "authenticationConfig": {
                        "alias": "name",
                        "config": {
                            "defaultProvider": "value"
                        }
                    }
                },
            ], 
            "state":"present",
            "force":False
        }

        results = authentication(toCreate)
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toCreate["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toCreate["alias"] )
        self.assertTrue(results['changed'])
        for expectedExecutions in toCreate["authenticationExecutions"]:
            executionFound = False
            for execution in results["ansible_facts"]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])

    def test_create_authentication_flow_with_update_profile_on_first_login_on(self):
        toCreate = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "First broker login with update profile on first login",
            "copyFrom": "first broker login",
            "authenticationExecutions": [
                {
                    "providerId": "idp-review-profile",
                    "requirement": "REQUIRED",
                    "authenticationConfig": {
                        "alias": "New review profile config",
                        "config": {
                            "update.profile.on.first.login": "on"
                        }
                    } 
                },
            ], 
            "state":"present",
            "force":False
        }

        results = authentication(toCreate)
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toCreate["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toCreate["alias"] )
        self.assertTrue(results['changed'])
        for expectedExecutions in toCreate["authenticationExecutions"]:
            executionFound = False
            for execution in results["ansible_facts"]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])
        
    def test_create_authentication_flow_without_copy(self):
        toCreate = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "No Copy broker login",
            "providerId": "basic-flow",
            "authenticationExecutions": [
                {
                    "providerId": "identity-provider-redirector",
                    "requirement": "ALTERNATIVE",
                    "authenticationConfig": {
                        "alias": "name",
                        "config": {
                            "defaultProvider": "value"
                        }
                    }
                }
            ], 
            "state":"present",
            "force":False
        }

        results = authentication(toCreate)
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toCreate["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toCreate["alias"] )
        self.assertTrue(results['changed'])
        for expectedExecutions in toCreate["authenticationExecutions"]:
            executionFound = False
            for execution in results["ansible_facts"]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])

    def test_create_authentication_flow_with_two_executions_without_copy(self):
        toCreate = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Authentication flow with an execution added",
            "providerId": "basic-flow",
            "authenticationExecutions": [
                {
                    "providerId": "identity-provider-redirector",
                    "requirement": "ALTERNATIVE",
                    "authenticationConfig": {
                        "alias": "name",
                        "config": {
                            "defaultProvider": "value"
                        }
                    }
                },
                {
                    "providerId": "auth-conditional-otp-form",
                    "requirement": "REQUIRED",
                    "authenticationConfig": {
                        "alias": "test-conditional-otp",
                        "config": {
                            "skipOtpRole": "admin",
                            "forceOtpRole": "broker.read-token",
                            "defaultOtpOutcome": "skip"
                        }
                    }
                }
            ], 
            "state":"present",
            "force":False
        }

        results = authentication(toCreate)
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toCreate["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toCreate["alias"] )
        self.assertTrue(results['changed'])
        for expectedExecutions in toCreate["authenticationExecutions"]:
            executionFound = False
            for execution in results["ansible_facts"]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])
                
    def test_add_execution_to_authentication_flow_without_copy(self):
        toChange = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Authentication flow with two executions",
            "providerId": "basic-flow",
            "authenticationExecutions": [
                {
                    "providerId": "identity-provider-redirector",
                    "requirement": "ALTERNATIVE",
                    "authenticationConfig": {
                        "alias": "name",
                        "config": {
                            "defaultProvider": "value"
                        }
                    }
                }
            ], 
            "state":"present",
            "force":False
        }

        executionToAdd = {
            "providerId": "auth-conditional-otp-form",
            "requirement": "ALTERNATIVE",
            "authenticationConfig": {
                "alias": "test-conditional-otp",
                "config": {
                    "skipOtpRole": "admin",
                    "forceOtpRole": "broker.read-token",
                    "defaultOtpOutcome": "skip"
                }
            }
        }
        authentication(toChange)
        toChange["authenticationExecutions"].append(executionToAdd)
        results = authentication(toChange)
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toChange["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toChange["alias"] )
        self.assertTrue(results['changed'])
        for expectedExecutions in toChange["authenticationExecutions"]:
            executionFound = False
            for execution in results["ansible_facts"]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])

    def test_authentication_flow_not_changed(self):
        toDoNotChange = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Copy of first broker login 2",
            "copyFrom": "first broker login",
            "authenticationExecutions": [
                {
                    "providerId": "identity-provider-redirector",
                    "requirement": "ALTERNATIVE",
                    "authenticationConfig": {
                        "alias": "name",
                        "config": {
                            "defaultProvider": "value"
                        }
                    }
                }
            ], 
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
            "authenticationExecutions": [
                {
                    "providerId": "identity-provider-redirector",
                    "requirement": "ALTERNATIVE",
                    "authenticationConfig": {
                        "alias": "name",
                        "config": {
                            "defaultProvider": "value"
                        }
                    }
                }
            ],
            "state":"present",
            "force":True
        }
        authentication(toChange)
        toChange["authenticationExecutions"][0]["authenticationConfig"]["config"]["defaultProvider"] = "modified value"
        results = authentication(toChange)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["flow"]["alias"], toChange["alias"], results["ansible_facts"]["flow"]["alias"] + "is not" + toChange["alias"] )
        for expectedExecutions in toChange["authenticationExecutions"]:
            executionFound = False
            for execution in results["ansible_facts"]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])
        
    def test_delete_authentication_flow(self):
        toDelete = {
            "url":  "http://localhost:18081",
            "username": "admin",
            "password": "admin",
            "realm": "master",
            "alias": "Copy of first broker login 4",
            "copyFrom": "first broker login",
            "authenticationExecutions": [
                {
                    "providerId": "identity-provider-redirector",
                    "requirement": "ALTERNATIVE",
                    "authenticationConfig": {
                        "alias": "name",
                        "config": {
                            "defaultProvider": "value"
                        }
                    }
                }
            ], 
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
