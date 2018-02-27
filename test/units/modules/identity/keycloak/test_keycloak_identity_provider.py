import collections
import os
import unittest
import copy
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
                openIdConfigurationUrl = "http://localhost:18081/auth/realms/master/.well-known/openid-configuration",
                clientId = "test",
                clientSecret = "test",
                defaultScope = "openid email profile",
                disableUserInfo = "false",
                guiOrder = "1",
                backchannelSupported = "false"
                ),
            mappers = [ 
                    {
                        "name": "test",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim" : "test",
                            "user.attribute": "lastname"
                            }
                    }, 
                    {
                        "name" : "test2",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim": "test2",
                            "user.attribute":"firstname"
                        }
                    },
                    {
                        "name" : "test3",
                        "identityProviderMapper": "oidc-role-idp-mapper", 
                        "config" : {
                            "claim": "claimName",
                            "claim.value": "valueThatGiveRole",
                            "role": "roleName"
                        }
                    }

                ],
            state = "present",
            force = False
        )
        results = idp(toCreate)
        self.assertTrue(results['changed'])
        #err = results['stderr'] if 'stderr' in results else ""            
        #out = results['stdout'] if 'stdout' in results else ""
        self.assertEquals(results['rc'], 0, "rc: " + str(results['rc']) + " : " + results['stdout'] if 'stdout' in results else "" + " : " + results['stderr'] if 'stderr' in results else "")
        self.assertTrue(results['ansible_facts']['idp']['enabled'])
        self.assertEquals(results['ansible_facts']['idp']['alias'],toCreate["alias"], 'Alias = ' + results['ansible_facts']['idp']['alias'])
        self.assertEquals(results['ansible_facts']['idp']['config']['clientId'],toCreate["config"]["clientId"],"ClientId: " + results['ansible_facts']['idp']['config']['clientId'])
        self.assertEquals(results['ansible_facts']['idp']['config']['guiOrder'], toCreate["config"]["guiOrder"],"GuiOrder: " + results['ansible_facts']['idp']['config']['guiOrder'] + ": " + toCreate["config"]["guiOrder"])
        for mapperToCreate in toCreate["mappers"]:
            mapperFound = False
            for mapper in results['ansible_facts']['mappers']:
                if mapper["name"] == mapperToCreate["name"]:
                    mapperFound = True
                    self.assertEquals(mapper["identityProviderMapper"], mapperToCreate["identityProviderMapper"], "identityProviderMapper: " + mapper["identityProviderMapper"] + "not equal " + mapperToCreate["identityProviderMapper"])
                    self.assertDictEqual(mapper["config"], mapperToCreate["config"], "config: " + str(mapper["config"]) + "not equal " + str(mapperToCreate["config"]))
            self.assertTrue(mapperFound, "mapper " + mapperToCreate["name"] + " not found")                                          
        
    def test_idp_not_changed(self):
        ToDoNotChange = {
            "username": "admin", 
            "password": "admin",
            "realm": "master",
            "url": "http://localhost:18081",
            "alias": "test1",
            "providerId": "oidc",
            "displayName": "Test1",
            "enabled": True,
            "updateProfileFirstLoginMode": "on",
            "trustEmail": False,
            "storeToken": True,
            "addReadTokenRoleOnCreate": True,
            "authenticateByDefault": False,
            "linkOnly": False,
            "firstBrokerLoginFlowAlias": "first broker login",
            "config": { 
                "openIdConfigurationUrl": "http://localhost:18081/auth/realms/master/.well-known/openid-configuration",
                "clientId": "test1",
                "defaultScope": "openid email profile",
                "disableUserInfo": "false",
                "guiOrder": "1",
                "backchannelSupported": "true"
                },
            "mappers": [ 
                    {
                        "name": "test11",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim" : "test",
                            "user.attribute": "lastname"
                            }
                    }, 
                    {
                        "name" : "test12",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim": "test2",
                            "user.attribute":"firstname"
                        }
                    },
                    {
                        "name" : "test13",
                        "identityProviderMapper": "oidc-role-idp-mapper", 
                        "config" : {
                            "claim": "claimName",
                            "claim.value": "valueThatGiveRole",
                            "role": "roleName"
                        }
                    }

                ],
            "state": "present",
            "force": False
        }
        idp(ToDoNotChange)
        
        results = idp(ToDoNotChange)
        print(str(results).decode("utf-8"))
        self.assertFalse(results['changed'])
        self.assertEquals(results['rc'], 0, "rc: " + str(results['rc']) + " : " + results['stdout'] if 'stdout' in results else "" + " : " + results['stderr'] if 'stderr' in results else "")
        self.assertEquals(results['ansible_facts']['idp']['alias'],'test1', 'Alias = ' + results['ansible_facts']['idp']['alias'])
        for mapperToDoNotChange in ToDoNotChange["mappers"]:
            mapperFound = False
            for mapper in results['ansible_facts']['mappers']:
                if mapper["name"] == mapperToDoNotChange["name"]:
                    mapperFound = True
                    self.assertEquals(mapper["identityProviderMapper"], mapperToDoNotChange["identityProviderMapper"], "identityProviderMapper: " + mapper["identityProviderMapper"] + "not equal " + mapperToDoNotChange["identityProviderMapper"])
                    self.assertDictEqual(mapper["config"], mapperToDoNotChange["config"], "config: " + str(mapper["config"]) + "not equal " + str(mapperToDoNotChange["config"]))
            self.assertTrue(mapperFound, "mapper " + mapperToDoNotChange["name"] + " not found")                                          

    def test_modify_idp(self):
        ToChange = dict(
            username = "admin", 
            password = "admin",
            realm = "master",
            url = "http://localhost:18081",
            alias = "test2",
            providerId = "oidc",
            displayName = "Test2",
            enabled = True,
            updateProfileFirstLoginMode="on",
            trustEmail=False,
            storeToken = True,
            addReadTokenRoleOnCreate = True,
            authenticateByDefault = False,
            linkOnly = False,
            firstBrokerLoginFlowAlias = "first broker login",
            config = dict(
                openIdConfigurationUrl = "http://localhost:18081/auth/realms/master/.well-known/openid-configuration",
                clientId = "test2",
                clientSecret = "test2",
                defaultScope = "openid email profile",
                disableUserInfo = "false",
                guiOrder = "1",
                backchannelSupported = "true"
                ),
            mappers = [ 
                    {
                        "name": "test21",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim" : "test",
                            "user.attribute": "lastname"
                            }
                    }, 
                    {
                        "name" : "test22",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim": "test2",
                            "user.attribute":"firstname"
                        }
                    },
                    {
                        "name" : "test23",
                        "identityProviderMapper": "oidc-role-idp-mapper", 
                        "config" : {
                            "claim": "claimName",
                            "claim.value": "valueThatGiveRole",
                            "role": "roleName"
                        }
                    }

                ],
            state = "present",
            force = False
        )
        idp(ToChange)
        
        #newToChange = copy.deepcopy(ToChange)
        newToChange = {
            "username": "admin",
            "password":"admin",
            "realm": "master",
            "url": "http://localhost:18081",
            "alias": "test2",
            "providerId": "oidc",
            "storeToken": False,
            "firstBrokerLoginFlowAlias": "registration",
            "config": { 
                "openIdConfigurationUrl": "http://localhost:18081/auth/realms/master/.well-known/openid-configuration",
                "clientId": "test2",
                "clientSecret": "password",
                "defaultScope": "openid email profile",
                "disableUserInfo": "false",
                "guiOrder": "2"
                },
                "state": "present",
                "force": False
            }
        
        results = idp(newToChange)
        
        self.assertEquals(results['rc'], 0, "rc: " + str(results['rc']) + " : " + results['stdout'] if 'stdout' in results else "" + " : " + results['stderr'] if 'stderr' in results else "")
        self.assertEquals(results['ansible_facts']['idp']['alias'],ToChange["alias"], 'Alias = ' + results['ansible_facts']['idp']['alias'])
        self.assertFalse(results['ansible_facts']['idp']['storeToken'], 'storeToken should be false : ' + str(results['ansible_facts']['idp']['storeToken']))
        self.assertEquals(results['ansible_facts']['idp']['firstBrokerLoginFlowAlias'], newToChange["firstBrokerLoginFlowAlias"], "firstBrokerLoginFlowAlias: " + results['ansible_facts']['idp']['firstBrokerLoginFlowAlias'])
        self.assertEquals(results['ansible_facts']['idp']['config']['guiOrder'],newToChange["config"]["guiOrder"],"GuiOrder: " + results['ansible_facts']['idp']['config']['guiOrder'])
        self.assertTrue(results['changed'])

    def test_modify_idp_modify_mappers(self):
        ToChange = dict(
            username = "admin", 
            password = "admin",
            realm = "master",
            url = "http://localhost:18081",
            alias = "test5",
            providerId = "oidc",
            displayName = "Test5",
            enabled = True,
            updateProfileFirstLoginMode="on",
            trustEmail=False,
            storeToken = True,
            addReadTokenRoleOnCreate = True,
            authenticateByDefault = False,
            linkOnly = False,
            firstBrokerLoginFlowAlias = "first broker login",
            config = dict(
                openIdConfigurationUrl = "http://localhost:18081/auth/realms/master/.well-known/openid-configuration",
                clientId = "test2",
                clientSecret = "test2",
                defaultScope = "openid email profile",
                disableUserInfo = "false"
                ),
            mappers = [ 
                    {
                        "name": "test21",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim" : "test",
                            "user.attribute": "lastname"
                            }
                    }, 
                    {
                        "name" : "test22",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim": "test2",
                            "user.attribute":"firstname"
                        }
                    },
                    {
                        "name" : "test23",
                        "identityProviderMapper": "oidc-role-idp-mapper", 
                        "config" : {
                            "claim": "claimName",
                            "claim.value": "valueThatGiveRole",
                            "role": "roleName"
                        }
                    }

                ],
            state = "present",
            force = False
        )
        idp(ToChange)
        
        #newToChange = copy.deepcopy(ToChange)
        newToChange = {
            "username": "admin",
            "password":"admin",
            "realm": "master",
            "url": "http://localhost:18081",
            "alias": "test5",
            "providerId": "oidc",
            "mappers": [
                {
                    "name": "test24",
                    "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                    "config" : {
                        "claim" : "newTest",
                        "user.attribute": "lastname"
                        }
                 },
                {
                    "name" : "test25",
                    "identityProviderMapper": "oidc-role-idp-mapper", 
                    "config" : {
                        "claim": "claimName",
                        "claim.value": "valueThatGiveRole",
                        "role": "roleName"
                        }
                    }
                 ],
                "state": "present",
                "force": False
            }
        
        results = idp(newToChange)
        
        self.assertEquals(results['rc'], 0, "rc: " + str(results['rc']) + " : " + results['stdout'] if 'stdout' in results else "" + " : " + results['stderr'] if 'stderr' in results else "")
        self.assertEquals(results['ansible_facts']['idp']['alias'], ToChange["alias"], 'Alias = ' + results['ansible_facts']['idp']['alias'])
        self.assertTrue(results['changed'])
        for mapperToChange in newToChange["mappers"]:
            mapperFound = False
            for mapper in results['ansible_facts']['mappers']:
                if mapper["name"] == mapperToChange["name"]:
                    mapperFound = True
                    self.assertEquals(mapper["identityProviderMapper"], mapperToChange["identityProviderMapper"], "identityProviderMapper: " + mapper["identityProviderMapper"] + "not equal " + mapperToChange["identityProviderMapper"])
                    self.assertDictEqual(mapper["config"], mapperToChange["config"], "config: " + str(mapper["config"]) + "not equal " + str(mapperToChange["config"]))
            self.assertTrue(mapperFound, "mapper " + mapperToChange["name"] + " not found")  

    def test_delete_idp(self):
        toDelete = dict(
            username = "admin", 
            password = "admin",
            realm = "master",
            url = "http://localhost:18081",
            alias = "test3",
            providerId = "oidc",
            displayName = "Test3",
            enabled = True,
            updateProfileFirstLoginMode="on",
            trustEmail=False,
            storeToken = True,
            addReadTokenRoleOnCreate = True,
            authenticateByDefault = False,
            linkOnly = False,
            firstBrokerLoginFlowAlias = "first broker login",
            config = dict(
                openIdConfigurationUrl = "http://localhost:18081/auth/realms/master/.well-known/openid-configuration",
                clientId = "test3",
                clientSecret = "test3",
                defaultScope = "openid email profile",
                disableUserInfo = "false"
                ),
            mappers = [ 
                    {
                        "name": "test31",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim" : "test",
                            "user.attribute": "lastname"
                            }
                    }, 
                    {
                        "name" : "test32",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim": "test2",
                            "user.attribute":"firstname"
                        }
                    },
                    {
                        "name" : "test33",
                        "identityProviderMapper": "oidc-role-idp-mapper", 
                        "config" : {
                            "claim": "claimName",
                            "claim.value": "valueThatGiveRole",
                            "role": "roleName"
                        }
                    }

                ],
            state = "present",
            force = False
        )        
        idp(toDelete)
        toDelete['state'] = "absent"
        results = idp(toDelete)
        self.assertEquals(results['rc'], 0, "rc: " + str(results['rc']) + " : " + results['stdout'] if 'stdout' in results else "" + " : " + results['stderr'] if 'stderr' in results else "")
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'idp has been deleted')

    def test_change_client_secret(self):
        ToChange = dict(
            username = "admin", 
            password = "admin",
            realm = "master",
            url = "http://localhost:18081",
            alias = "test4",
            providerId = "oidc",
            displayName = "Test4",
            enabled = True,
            updateProfileFirstLoginMode="on",
            trustEmail=False,
            storeToken = True,
            addReadTokenRoleOnCreate = True,
            authenticateByDefault = False,
            linkOnly = False,
            firstBrokerLoginFlowAlias = "first broker login",
            config = dict(
                openIdConfigurationUrl = "http://localhost:18081/auth/realms/master/.well-known/openid-configuration",
                clientId = "test4",
                defaultScope = "openid email profile",
                disableUserInfo = "false"
                ),
            mappers = [ 
                    {
                        "name": "test41",
                        "identityProviderMapper": "oidc-user-attribute-idp-mapper", 
                        "config" : {
                            "claim" : "test",
                            "user.attribute": "lastname"
                            }
                    } 
                ],
            state = "present",
            force = False
        )
        idp(ToChange)
        toChangeSecret = dict(
            username = "admin", 
            password = "admin",
            realm = "master",
            url = "http://localhost:18081",
            alias = "test4",
            config = dict(
                clientId = "test4",
                clientSecret = "CeciEstMonSecret"
                ),
            state="present",
            force=False
            )
    
        results = idp(toChangeSecret)
        self.assertEquals(results['rc'], 0, "rc: " + str(results['rc']) + " : " + results['stdout'] if 'stdout' in results else "" + " : " + results['stderr'] if 'stderr' in results else "")
        self.assertTrue(results['changed'])
        
    def test_change_client_secret_without_alias(self):
        toChangeSecret = dict(
            username = "admin", 
            password = "admin",
            realm = "master",
            url = "http://localhost:18081",
            config = dict(
                clientId = "test4",
                clientSecret = "CeciEstMonSecret"
                ),
            state="present",
            force=False
            )
    
        results = idp(toChangeSecret)
        self.assertEquals(results['rc'], 1, "rc: " + str(results['rc']) + " : " + results['stdout'] if 'stdout' in results else "" + " : " + results['stderr'] if 'stderr' in results else "")
        self.assertFalse(results['changed'])