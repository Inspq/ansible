from ansible.modules.identity.keycloak import keycloak_authentication
from units.modules.utils import AnsibleExitJson, ModuleTestCase, set_module_args

class KeycloakAuthenticationTestCase(ModuleTestCase):
    authenticationTestFlows = [
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test create authentication flow copy",
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
            "state":"absent",
            "force":False
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test create authentication flow set update profile on first login to on",
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
            "state":"absent",
            "force":False
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test create authentication flow without copy",
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
            "state":"absent",
            "force":False
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test create authentication flow with two executions without copy",
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
            "state":"absent",
            "force":False
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test add execution to authentication flow without copy",
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
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test authentication flow not changed",
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
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test modify authentication flow",
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
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test delete authentication flow",
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
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Test delete inexisting authentication flow",
            "state":"absent",
            "force":False
        },
        {
            "auth_keycloak_url":  "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "alias": "Reorder executions",
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
        },
        
    ]
    def setUp(self):
        super(KeycloakAuthenticationTestCase, self).setUp()
        self.module = keycloak_authentication
        for flow in self.authenticationTestFlows:
            set_module_args(flow)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
 
    def tearDown(self):
        self.module = keycloak_authentication
        for flow in self.authenticationTestFlows:
            flowToDelete = flow.copy()
            flowToDelete["state"] = "absent"
            set_module_args(flowToDelete)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
        super(KeycloakAuthenticationTestCase, self).tearDown()
                
    def test_create_authentication_flow_copy(self):
        toCreate = self.authenticationTestFlows[0].copy()
        toCreate["state"] = "present"
        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertEquals(results.exception.args[0]["flow"]["alias"], toCreate["alias"], results.exception.args[0]["flow"]["alias"] + "is not" + toCreate["alias"] )
        for expectedExecutions in toCreate["authenticationExecutions"]:
            executionFound = False
            for execution in results.exception.args[0]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])

    def test_create_authentication_flow_set_update_profile_on_first_login_to_on(self):
        toCreate = self.authenticationTestFlows[1].copy()
        toCreate["state"] = "present"        
        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertEquals(results.exception.args[0]["flow"]["alias"], toCreate["alias"], results.exception.args[0]["flow"]["alias"] + "is not" + toCreate["alias"] )
        for expectedExecutions in toCreate["authenticationExecutions"]:
            executionFound = False
            for execution in results.exception.args[0]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])
        
    def test_create_authentication_flow_without_copy(self):
        toCreate = self.authenticationTestFlows[2].copy()
        toCreate["state"] = "present"
        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertEquals(results.exception.args[0]["flow"]["alias"], toCreate["alias"], results.exception.args[0]["flow"]["alias"] + "is not" + toCreate["alias"] )
        for expectedExecutions in toCreate["authenticationExecutions"]:
            executionFound = False
            for execution in results.exception.args[0]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])

    def test_create_authentication_flow_with_two_executions_without_copy(self):
        toCreate = self.authenticationTestFlows[3].copy()
        toCreate["state"] = "present" 

        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertEquals(results.exception.args[0]["flow"]["alias"], toCreate["alias"], results.exception.args[0]["flow"]["alias"] + "is not" + toCreate["alias"] )
        for expectedExecutions in toCreate["authenticationExecutions"]:
            executionFound = False
            for execution in results.exception.args[0]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])
                
    def test_add_execution_to_authentication_flow_without_copy(self):
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
        toModify = self.authenticationTestFlows[4].copy()
        toModify["authenticationExecutions"].append(executionToAdd)
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertEquals(results.exception.args[0]["flow"]["alias"], toModify["alias"], results.exception.args[0]["flow"]["alias"] + "is not" + toModify["alias"] )
        for expectedExecutions in toModify["authenticationExecutions"]:
            executionFound = False
            for execution in results.exception.args[0]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])

    def test_authentication_flow_not_changed(self):
        toModify = self.authenticationTestFlows[5].copy()
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertFalse(results.exception.args[0]['changed'])

    def test_modify_authentication_flow(self):
        toModify = self.authenticationTestFlows[6].copy()
        toModify["authenticationExecutions"][0]["authenticationConfig"]["config"]["defaultProvider"] = "modified value"
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertEquals(results.exception.args[0]["flow"]["alias"], toModify["alias"], results.exception.args[0]["flow"]["alias"] + "is not" + toModify["alias"] )
        for expectedExecutions in toModify["authenticationExecutions"]:
            executionFound = False
            for execution in results.exception.args[0]["flow"]["authenticationExecutions"]:
                if "providerId" in execution and execution["providerId"] == expectedExecutions["providerId"]:
                    executionFound = True
                    break
            self.assertTrue(executionFound, "Execution " + expectedExecutions["providerId"] + " not found")
            self.assertEquals(execution["requirement"], expectedExecutions["requirement"], execution["requirement"] + " is not equals to " + expectedExecutions["requirement"])
            for key in expectedExecutions["authenticationConfig"]["config"]:
                self.assertEquals(expectedExecutions["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key], execution["authenticationConfig"]["config"][key] + " is not equals to " + expectedExecutions["authenticationConfig"]["config"][key])
        
    def test_delete_authentication_flow(self):
        toDelete = self.authenticationTestFlows[7].copy()
        toDelete['state'] = 'absent'
        set_module_args(toDelete)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'deleted', 'authentication flow not deleted')

    def test_delete_inexisting_authentication_flow(self):
        toDelete = self.authenticationTestFlows[8].copy()
        set_module_args(toDelete)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertFalse(results.exception.args[0]['changed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'absent', 'authentication flow is not absent')
        
    def test_reorder_executions_in_existing_authentication_flow(self):
        newOrder = [
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
            },
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
        ]
        toModify = self.authenticationTestFlows[9].copy()
        toModify["authenticationExecutions"] = newOrder
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        executionsInSameOrder = True
        for i, expectedExecution in enumerate(toModify["authenticationExecutions"], start=0):
            if expectedExecution["providerId"] != results.exception.args[0]["flow"]["authenticationExecutions"][i]["providerId"]:
                executionsInSameOrder = False
                break
        self.assertTrue(executionsInSameOrder, "Execution have not been reordered")

            