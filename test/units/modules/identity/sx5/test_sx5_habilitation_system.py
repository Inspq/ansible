import collections
import os
import unittest
from ansible.modules.identity.sx5.sx5_habilitation_system import *
from ansible.modules.identity.keycloak.keycloak_client import *

class Sx5SystemTestCase(unittest.TestCase):

    def test_create_system(self):
        #client for the test
        toCreateClient = {}
        toCreateClient["url"] = "http://localhost:18081"
        toCreateClient["username"] = "admin"
        toCreateClient["password"] = "admin"
        toCreateClient["realm"] = "master"
        toCreateClient["state"] = "present"
        toCreateClient["clientId"] = "clientsystem11"
        toCreateClient["rootUrl"] = "http://test.com:8080"
        toCreateClient["name"] = "clientsystem11"
        toCreateClient["description"] = "Ceci est un test"
        toCreateClient["adminUrl"] = "http://test.com:8080/admin"
        toCreateClient["enabled"] = True
        toCreateClient["clientAuthenticatorType"] = "client-secret"
        toCreateClient["redirectUris"] = ["http://test.com:8080/secure","http://test1.com:8080/secure"]
        toCreateClient["webOrigins"] = ["*"]
        toCreateClient["bearerOnly"] = False
        toCreateClient["publicClient"] = False
        toCreateClient["force"] = False
        client(toCreateClient)
        toCreateClient["clientId"] = "clientsystem12"
        toCreateClient["name"] = "clientsystem12"
        client(toCreateClient)
        ##########################################
        toCreate = {}
        toCreate["spUrl"] = "http://localhost:18081"
        toCreate["spUsername"] = "admin"
        toCreate["spPassword"] = "admin"
        toCreate["spRealm"] = "master"
        toCreate["habilitationClient_id"] = "admin-cli"
        toCreate["habilitationClient_secret"] = ""
        toCreate["habilitationUrl"] = "http://localhost:8080/config"
        toCreate["systemName"] = "system1"
        toCreate["clientKeycloak"] = [{"spClient": "clientsystem11"},{"spClient": "clientsystem12"}]
        toCreate["state"] = "present"
        toCreate["force"] = False
    
        results = system(toCreate)
        print str(results)
        self.assertTrue(results['changed'])

    def test_system_not_changed(self):
        #client for the test
        toCreateClient = {}
        toCreateClient["url"] = "http://localhost:18081"
        toCreateClient["username"] = "admin"
        toCreateClient["password"] = "admin"
        toCreateClient["realm"] = "master"
        toCreateClient["state"] = "present"
        toCreateClient["clientId"] = "clientsystem21"
        toCreateClient["rootUrl"] = "http://test.com:8080"
        toCreateClient["name"] = "clientsystem21"
        toCreateClient["description"] = "Ceci est un test"
        toCreateClient["adminUrl"] = "http://test.com:8080/admin"
        toCreateClient["enabled"] = True
        toCreateClient["clientAuthenticatorType"] = "client-secret"
        toCreateClient["redirectUris"] = ["http://test.com:8080/secure","http://test1.com:8080/secure"]
        toCreateClient["webOrigins"] = ["*"]
        toCreateClient["bearerOnly"] = False
        toCreateClient["publicClient"] = False
        toCreateClient["force"] = False
        client(toCreateClient)
        toCreateClient["clientId"] = "clientsystem22"
        toCreateClient["name"] = "clientsystem22"
        client(toCreateClient)
        ##########################################
        toDoNotChange = {}
        toDoNotChange["spUrl"] = "http://localhost:18081"
        toDoNotChange["spUsername"] = "admin"
        toDoNotChange["spPassword"] = "admin"
        toDoNotChange["spRealm"] = "master"
        toDoNotChange["habilitationClient_id"] = "admin-cli"
        toDoNotChange["habilitationClient_secret"] = ""
        toDoNotChange["habilitationUrl"] = "http://localhost:8080/config"
        toDoNotChange["systemName"] = "system2"
        toDoNotChange["clientKeycloak"] = [{"spClient": "clientsystem21"},{"spClient": "clientsystem22"}]
        toDoNotChange["state"] = "present"
        toDoNotChange["force"] = False

        system(toDoNotChange)
        #print str(results)
        results = system(toDoNotChange)
        #print str(results)
        self.assertFalse(results['changed'])

    def test_modify_system(self):
        #client for the test
        toCreateClient = {}
        toCreateClient["url"] = "http://localhost:18081"
        toCreateClient["username"] = "admin"
        toCreateClient["password"] = "admin"
        toCreateClient["realm"] = "master"
        toCreateClient["state"] = "present"
        toCreateClient["clientId"] = "clientsystem31"
        toCreateClient["rootUrl"] = "http://test.com:8080"
        toCreateClient["name"] = "clientsystem31"
        toCreateClient["description"] = "Ceci est un test"
        toCreateClient["adminUrl"] = "http://test.com:8080/admin"
        toCreateClient["enabled"] = True
        toCreateClient["clientAuthenticatorType"] = "client-secret"
        toCreateClient["redirectUris"] = ["http://test.com:8080/secure","http://test1.com:8080/secure"]
        toCreateClient["webOrigins"] = ["*"]
        toCreateClient["bearerOnly"] = False
        toCreateClient["publicClient"] = False
        toCreateClient["force"] = False
        client(toCreateClient)
        toCreateClient["clientId"] = "clientsystem32"
        toCreateClient["name"] = "clientsystem32"
        client(toCreateClient)
        toCreateClient["clientId"] = "clientsystemChange31"
        toCreateClient["name"] = "clientsystemChange31"
        client(toCreateClient)
        toCreateClient["clientId"] = "clientsystemChange32"
        toCreateClient["name"] = "clientsystemChange32"
        client(toCreateClient)
        ##########################################
        toChange = {}
        toChange["spUrl"] = "http://localhost:18081"
        toChange["spUsername"] = "admin"
        toChange["spPassword"] = "admin"
        toChange["spRealm"] = "master"
        toChange["habilitationClient_id"] = "admin-cli"
        toChange["habilitationClient_secret"] = ""
        toChange["habilitationUrl"] = "http://localhost:8080/config"
        toChange["systemName"] = "system3"
        toChange["clientKeycloak"] = [{"spClient": "clientsystem31"},{"spClient": "clientsystem32"}]
        toChange["state"] = "present"
        toChange["force"] = False

        results = system(toChange)
        #print str(results)
        toChange["clientKeycloak"] = [{"spClient": "clientsystemChange31"},{"spClient": "clientsystemChange32"}]
        results = system(toChange)
        #print str(results)
        self.assertTrue(results['changed'])
        
        
    def test_delete_system(self):
        #client for the test
        toCreateClient = {}
        toCreateClient["url"] = "http://localhost:18081"
        toCreateClient["username"] = "admin"
        toCreateClient["password"] = "admin"
        toCreateClient["realm"] = "master"
        toCreateClient["state"] = "present"
        toCreateClient["clientId"] = "clientsystem42"
        toCreateClient["rootUrl"] = "http://test.com:8080"
        toCreateClient["name"] = "clientsystem42"
        toCreateClient["description"] = "Ceci est un test"
        toCreateClient["adminUrl"] = "http://test.com:8080/admin"
        toCreateClient["enabled"] = True
        toCreateClient["clientAuthenticatorType"] = "client-secret"
        toCreateClient["redirectUris"] = ["http://test.com:8080/secure","http://test1.com:8080/secure"]
        toCreateClient["webOrigins"] = ["*"]
        toCreateClient["bearerOnly"] = False
        toCreateClient["publicClient"] = False
        toCreateClient["force"] = False
        client(toCreateClient)
        toCreateClient["clientId"] = "clientsystem41"
        toCreateClient["name"] = "clientsystem41"
        client(toCreateClient)
        ##########################################
        toDelete = {}
        toDelete["spUrl"] = "http://localhost:18081"
        toDelete["spUsername"] = "admin"
        toDelete["spPassword"] = "admin"
        toDelete["spRealm"] = "master"
        toDelete["habilitationClient_id"] = "admin-cli"
        toDelete["habilitationClient_secret"] = ""
        toDelete["habilitationUrl"] = "http://localhost:8080/config"
        toDelete["systemName"] = "system4"
        toDelete["clientKeycloak"] = [{"spClient": "clientsystem41"},{"spClient": "clientsystem42"}]
        toDelete["state"] = "present"
        toDelete["force"] = False

        system(toDelete)
        toDelete["state"] = "absent"
        results = system(toDelete)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'system has been deleted')
