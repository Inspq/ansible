import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_client import *

class KeycloakClientTestCase(unittest.TestCase):
 
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
        toCreate["roles"] = [{"name":"test1"},{"name":"test2"}]
        toCreate["publicClient"] = False
        toCreate["force"] = False

        results = client(toCreate)
        #print str(results)
    
        self.assertTrue(results['ansible_facts']['client']['enabled'])
        self.assertTrue(results['changed'])
        self.assertTrue(results['ansible_facts']['clientSecret'])
        OrderdRoles = sorted(results['ansible_facts']['clientRoles'], key=lambda k: k['name'])
        self.assertEqual(OrderdRoles[0]['name'], toCreate["roles"][0]['name'], "roles : " + OrderdRoles[0]['name'])
        self.assertEqual(OrderdRoles[1]['name'], toCreate["roles"][1]['name'], "roles : " + OrderdRoles[1]['name'])
        self.assertEqual(results['ansible_facts']['client']['redirectUris'].sort(),toCreate["redirectUris"].sort(),"redirectUris: " + str(results['ansible_facts']['client']['redirectUris'].sort()))
        
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
        toDoNotChange["roles"] = [{"name":"test1"},{"name":"test2"}]
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
        toChange["roles"] = [{"name":"test1"},{"name":"test2"}]
        toChange["force"] = False

        client(toChange)
        toChange["name"] = "test3"
        toChange["description"] = "Ceci est un test3"
        results = client(toChange)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['ansible_facts']['client']['name'], toChange["name"], "name: " + results['ansible_facts']['client']['name'])
        self.assertEqual(results['ansible_facts']['client']['description'], toChange["description"], 'description: ' + results['ansible_facts']['client']['description'])
        OrderdRoles = sorted(results['ansible_facts']['clientRoles'], key=lambda k: k['name'])
        self.assertEqual(OrderdRoles[0]['name'], toChange["roles"][0]['name'], "roles : " + OrderdRoles[0]['name'])
        self.assertEqual(OrderdRoles[1]['name'], toChange["roles"][1]['name'], "roles : " + OrderdRoles[1]['name'])
        self.assertEqual(results['ansible_facts']['client']['redirectUris'].sort(),toChange["redirectUris"].sort(),"redirectUris: " + str(results['ansible_facts']['client']['redirectUris'].sort()))
        
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
