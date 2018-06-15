import collections
import os
import unittest
from ansible.modules.identity.sx5.sx5_habilitation_system import *

class Sx5SystemTestCase(unittest.TestCase):

    def test_create_system(self):
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
