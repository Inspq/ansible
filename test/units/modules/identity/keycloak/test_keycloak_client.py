import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_client import *

class KeycloakClientTestCase(unittest.TestCase):
    testClientRoles = [
            {
                "name":"test1",
                "description": "test1",
                "composite": False
                },
            {
                "name":"test2",
                "description": "test2",
                "composite": False
            }
        ]
    testClient = {
        "url": "http://localhost:18081",
        "username": "admin",
        "password": "admin",
        "realm": "master",
        "state": "present",
        "clientId": "basetest",
        "rootUrl": "http://test.com:8080",
        "name": "basetest",
        "description": "Base testing",
        "publicClient": False,
        "force": False
    }
    
    def setUp(self):
        self.testClient["roles"] = self.testClientRoles
        client(self.testClient)
 
    def test_create_client(self):
        toCreate = {}
        toCreate["url"] = "http://localhost:18081"
        toCreate["username"] = "admin"
        toCreate["password"] = "admin"
        toCreate["realm"] = "master"
        toCreate["state"] = "present"
        toCreate["clientId"] = "test"
        toCreate["rootUrl"] = "http://test.com:8080"
        toCreate["name"] = "test"
        toCreate["description"] = "Ceci est un test"
        toCreate["adminUrl"] = "http://test.com:8080/admin"
        toCreate["baseUrl"] = "http://test.com:8080"
        toCreate["enabled"] = True
        toCreate["clientAuthenticatorType"] = "client-secret"
        toCreate["redirectUris"] = ["http://test.com:8080/secure","http://test1.com:8080/secure"]
        toCreate["webOrigins"] = ["*"]
        toCreate["consentRequired"] = False   
        toCreate["standardFlowEnabled"] = True
        toCreate["implicitFlowEnabled"] = True
        toCreate["directAccessGrantsEnabled"] = True
        toCreate["serviceAccountsEnabled"] = True
        #toCreate["authorizationServicesEnabled"] = False
        toCreate["protocol"] = "openid-connect"
        toCreate["bearerOnly"] = False
        toCreate["roles"] = [
            {
                "name":"test1",
                "description": "test1",
                "composite": False
            },
            {
                "name":"toCreate",
                "description": "toCreate",
                "composite": True,
                "composites": [
                    {
                        "id": self.testClient['name'],
                        "name": self.testClientRoles[0]['name']
                    },
                    {
                        "name": "admin"
                    }
                ]
            }
        ]
        toCreate["protocolMappers"] = [{"name": "test1Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": 'true',
                                            "user.attribute": "test1",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test1",
                                            "jsonType.label": "String"}},
                                       {"name": "test2Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": 'true',
                                            "user.attribute": "test2",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test2",
                                            "jsonType.label": "String"}}]
        toCreate["publicClient"] = False
        toCreate["force"] = False

        results = client(toCreate)
        #print str(results)
    
        self.assertTrue(results['ansible_facts']['client']['enabled'])
        self.assertTrue(results['changed'])
        self.assertTrue(results['ansible_facts']['clientSecret'])
        OrderdRoles = sorted(results['ansible_facts']['client']['clientRoles'], key=lambda k: k['name'])
        self.assertEqual(OrderdRoles[0]['name'], toCreate["roles"][0]['name'], "roles : " + OrderdRoles[0]['name'])
        self.assertEqual(OrderdRoles[1]['name'], toCreate["roles"][1]['name'], "roles : " + OrderdRoles[1]['name'])
        for newComposite in toCreate["roles"][1]['composites']:
            compositeFound = False
            for createdComposite in OrderdRoles[1]['composites']:
                if "id" in newComposite and newComposite["id"] == createdComposite['id'] and newComposite["name"] == createdComposite['name']:
                    compositeFound = True
                elif newComposite["name"] == createdComposite['name']:
                    compositeFound = True
            if "id" in newComposite:
                message = "Composite: id:" + newComposite["id"] + " name:" + newComposite["name"] + " not found"
            else:
                message = "Composite: name:" + newComposite["name"] + " not found"
            self.assertTrue(compositeFound, message)
            
        self.assertEqual(results['ansible_facts']['client']['redirectUris'].sort(),toCreate["redirectUris"].sort(),"redirectUris: " + str(results['ansible_facts']['client']['redirectUris'].sort()))
        for toCreateMapper in toCreate["protocolMappers"]:
            mapperFound = False
            for mapper in results['ansible_facts']['client']['protocolMappers']:
                if mapper["name"] == toCreateMapper["name"]:
                    mapperFound = True
                    break
            self.assertTrue(mapperFound, "no mapper found: " + toCreateMapper["name"])
            if mapperFound:
                self.assertEqual(mapper["config"]["claim.name"], toCreateMapper["config"]["claim.name"], "claim.name: " + toCreateMapper["config"]["claim.name"] + ": " + mapper["config"]["claim.name"])
                self.assertEqual(mapper["config"]["user.attribute"], toCreateMapper["config"]["user.attribute"], "user.attribute: " + mapper["config"]["user.attribute"] + ": " + mapper["config"]["user.attribute"])

    def test_client_not_changed(self):
        toDoNotChange = {}
        toDoNotChange["url"] = "http://localhost:18081"
        toDoNotChange["username"] = "admin"
        toDoNotChange["password"] = "admin"
        toDoNotChange["realm"] = "master"
        toDoNotChange["state"] = "present"
        toDoNotChange["clientId"] = "test2"
        toDoNotChange["rootUrl"] = "http://test2.com:8080"
        toDoNotChange["name"] = "test2"
        toDoNotChange["description"] = "Ceci est un test2"
        toDoNotChange["adminUrl"] = "http://test2.com:8080/admin"
        toDoNotChange["baseUrl"] = "http://test2.com:8080"
        toDoNotChange["enabled"] = True
        toDoNotChange["clientAuthenticatorType"] = "client-secret"
        toDoNotChange["redirectUris"] = ["http://test2.com:8080/secure"]
        toDoNotChange["webOrigins"] = ["http://test2.com:8080/secure"]
        toDoNotChange["consentRequired"] = False   
        toDoNotChange["standardFlowEnabled"] = True
        toDoNotChange["implicitFlowEnabled"] = True
        toDoNotChange["directAccessGrantsEnabled"] = True
        toDoNotChange["serviceAccountsEnabled"] = True
        #toDoNotChange["authorizationServicesEnabled"] = False
        toDoNotChange["protocol"] = "openid-connect"
        toDoNotChange["bearerOnly"] = False
        toDoNotChange["publicClient"] = False
        toDoNotChange["roles"] = [
            {
                "name":"test1",
                "description": "test1",
                "composite": False
            },
            {
                "name":"toDoNotChange",
                "description": "toDoNotChange",
                "composite": True,
                "composites": [
                    {
                        "id": self.testClient['name'],
                        "name": self.testClientRoles[0]['name']
                    }
                ]
            }
                                  ]
        toDoNotChange["protocolMappers"] = [{"name": "test1Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": True,
                                            "user.attribute": "test1",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test1",
                                            "jsonType.label": "String"}},
                                       {"name": "test2Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'true',
                                            "userinfo.token.claim": 'true',
                                            "user.attribute": "test2",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test2",
                                            "jsonType.label": "String"}}]
        toDoNotChange["force"] = False

        client(toDoNotChange)
        results = client(toDoNotChange)
        #print str(results)
        self.assertFalse(results['changed'])

    def test_modify_client(self):
        toChange = {}
        toChange["url"] = "http://localhost:18081"
        toChange["username"] = "admin"
        toChange["password"] = "admin"
        toChange["realm"] = "master"
        toChange["state"] = "present"
        toChange["clientId"] = "test3"
        toChange["rootUrl"] = "http://test3.com:8080"
        toChange["name"] = "test2"
        toChange["description"] = "Ceci est un test2"
        toChange["adminUrl"] = "http://test3.com:8080/admin"
        toChange["baseUrl"] = "http://test3.com:8080"
        toChange["enabled"] = True
        toChange["clientAuthenticatorType"] = "client-secret"
        toChange["redirectUris"] = ["http://test3.com:8080/secure"]
        toChange["webOrigins"] = ["http://test3.com:8080/secure"]
        toChange["consentRequired"] = False   
        toChange["standardFlowEnabled"] = True
        toChange["implicitFlowEnabled"] = True
        toChange["directAccessGrantsEnabled"] = True
        toChange["serviceAccountsEnabled"] = True
        #toChange["authorizationServicesEnabled"] = False
        toChange["protocol"] = "openid-connect"
        toChange["bearerOnly"] = False
        toChange["publicClient"] = False
        toChange["roles"] = [
            {
                "name":"test1",
                "description": "test1",
                "composite": False
            },
            {
                "name":"test2",
                "description": "test2",
                "composite": True,
                "composites": [
                    {
                        "id": self.testClient['name'],
                        "name": self.testClientRoles[0]['name']
                    }
                ]
            }
        ]
        toChange["protocolMappers"] = [{"name": "test1Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": False,
                                            "user.attribute": "test1",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test1",
                                            "jsonType.label": "String"}},
                                       {"name": "test2Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": 'true',
                                            "user.attribute": "test2",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test2",
                                            "jsonType.label": "String"}}]
        toChange["force"] = False

        client(toChange)
        toChange["name"] = "test3"
        toChange["description"] = "Ceci est un test3"
        toChange["protocolMappers"] = [{"name": "test1Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": 'false',
                                            "user.attribute": "test12",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test12",
                                            "jsonType.label": "String"}}]
        results = client(toChange)
        print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['ansible_facts']['client']['name'], toChange["name"], "name: " + results['ansible_facts']['client']['name'])
        self.assertEqual(results['ansible_facts']['client']['description'], toChange["description"], 'description: ' + results['ansible_facts']['client']['description'])
        OrderdRoles = sorted(results['ansible_facts']['client']['clientRoles'], key=lambda k: k['name'])
        self.assertEqual(OrderdRoles[0]['name'], toChange["roles"][0]['name'], "roles : " + OrderdRoles[0]['name'])
        self.assertEqual(OrderdRoles[1]['name'], toChange["roles"][1]['name'], "roles : " + OrderdRoles[1]['name'])
        self.assertEqual(results['ansible_facts']['client']['redirectUris'].sort(),toChange["redirectUris"].sort(),"redirectUris: " + str(results['ansible_facts']['client']['redirectUris'].sort()))
        for toChangeMapper in toChange["protocolMappers"]:
            mapperFound = False
            for mapper in results['ansible_facts']['client']['protocolMappers']:
                if mapper["name"] == toChangeMapper["name"]:
                    mapperFound = True
                    break
            self.assertTrue(mapperFound, "no mapper found: " + toChangeMapper["name"])
            if mapperFound:
                self.assertEqual(mapper["config"]["claim.name"], toChangeMapper["config"]["claim.name"], "claim.name: " + toChangeMapper["config"]["claim.name"] + ": " + mapper["config"]["claim.name"])
                self.assertEqual(mapper["config"]["user.attribute"], toChangeMapper["config"]["user.attribute"], "user.attribute: " + toChangeMapper["config"]["user.attribute"] + ": " + mapper["config"]["user.attribute"])
 
    def test_add_client_composite_roles(self):
        clientRoles = [
            {
                "name":"test1",
                "description": "test1",
                "composite": False
                },
            {
                "name":"test2",
                "description": "test2",
                "composite": True,
                "composites": [
                    {
                        "id": self.testClient['name'],
                        "name": self.testClientRoles[0]['name']
                    }
                ]
            }
        ]
        toChange = {}
        toChange["url"] = "http://localhost:18081"
        toChange["username"] = "admin"
        toChange["password"] = "admin"
        toChange["realm"] = "master"
        toChange["state"] = "present"
        toChange["clientId"] = "test5"
        toChange["rootUrl"] = "http://test5.com:8080"
        toChange["name"] = "test5"
        toChange["description"] = "Ceci est un test5"
        toChange["adminUrl"] = "http://test5.com:8080/admin"
        toChange["baseUrl"] = "http://test5.com:8080"
        toChange["enabled"] = True
        toChange["clientAuthenticatorType"] = "client-secret"
        toChange["redirectUris"] = ["http://test5.com:8080/secure"]
        toChange["webOrigins"] = ["http://test5.com:8080/secure"]
        toChange["consentRequired"] = False   
        toChange["standardFlowEnabled"] = True
        toChange["implicitFlowEnabled"] = True
        toChange["directAccessGrantsEnabled"] = True
        toChange["serviceAccountsEnabled"] = True
        #toChange["authorizationServicesEnabled"] = False
        toChange["protocol"] = "openid-connect"
        toChange["bearerOnly"] = False
        toChange["publicClient"] = False
        toChange["roles"] = clientRoles
        toChange["protocolMappers"] = [{"name": "test1Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": False,
                                            "user.attribute": "test1",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test1",
                                            "jsonType.label": "String"}},
                                       {"name": "test2Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": 'true',
                                            "user.attribute": "test2",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "test2",
                                            "jsonType.label": "String"}}]
        toChange["force"] = False

        client(toChange)
        newClientRoles = [
            {
                "name":"test1",
                "description": "test1",
                "composite": False
                },
            {
                "name":"test2",
                "description": "test2",
                "composite": True,
                "composites": [
                    {
                        "id": self.testClient['name'],
                        "name": self.testClientRoles[0]['name']
                    },
                    {
                        "id": self.testClient['name'],
                        "name": self.testClientRoles[1]['name']
                    },
                    {
                        "name": "admin"
                    }
                ]
            }
        ]
        toChange["roles"] = newClientRoles
        results = client(toChange)
        print str(results)
        self.assertTrue(results['changed'])
        OrderdRoles = sorted(results['ansible_facts']['client']['clientRoles'], key=lambda k: k['name'])
        self.assertEqual(OrderdRoles[0]['name'], newClientRoles[0]['name'], "roles : " + OrderdRoles[0]['name'])
        self.assertEqual(OrderdRoles[1]['name'], newClientRoles[1]['name'], "roles : " + OrderdRoles[1]['name'])
        #self.assertEqual(len(OrderdRoles[1]['composites']), len(newClientRoles[1]['composites']), 'Composite length: ' + len(OrderdRoles[1]['composites']) + ' : ' + len(newClientRoles[1]['composites']))
        OrderedComposites = sorted(OrderdRoles[1]['composites'], key=lambda k:['name]'])
        for index, composite in enumerate(OrderedComposites):
            compositeFound = False
            for toChangeComposite in newClientRoles[1]['composites']:
                if toChangeComposite['name'] == composite['name']:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, 'Composite ' + composite['name'] + ' not found')
                        
    def test_delete_client(self):
        toDelete = {}
        toDelete["url"] = "http://localhost:18081"
        toDelete["username"] = "admin"
        toDelete["password"] = "admin"
        toDelete["realm"] = "master"
        toDelete["state"] = "present"
        toDelete["clientId"] = "test4"
        toDelete["rootUrl"] = "http://test4.com:8080"
        toDelete["name"] = "test4"
        toDelete["description"] = "Ceci est un test4"
        toDelete["adminUrl"] = "http://test4.com:8080/admin"
        toDelete["baseUrl"] = "http://test4.com:8080"
        toDelete["enabled"] = True
        toDelete["clientAuthenticatorType"] = "client-secret"
        toDelete["redirectUris"] = ["http://test4.com:8080/secure"]
        toDelete["webOrigins"] = ["http://test4.com:8080/secure"]
        toDelete["consentRequired"] = False   
        toDelete["standardFlowEnabled"] = True
        toDelete["implicitFlowEnabled"] = True
        toDelete["directAccessGrantsEnabled"] = True
        toDelete["serviceAccountsEnabled"] = True
        #toDelete["authorizationServicesEnabled"] = False
        toDelete["protocol"] = "openid-connect"
        toDelete["bearerOnly"] = False
        toDelete["publicClient"] = False
        toDelete["force"] = False

        client(toDelete)
        toDelete["state"] = "absent"
        results = client(toDelete)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'client has been deleted')
