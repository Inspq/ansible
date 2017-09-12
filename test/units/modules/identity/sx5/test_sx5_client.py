import collections
import os
import unittest

from ansible.modules.identity.sx5.sx5_client import *

class Sx5ClientTestCase(unittest.TestCase):
 
    def test_create_client(self):
        toCreate = {}
        toCreate["idp_url"] = "http://localhost:18081"
        toCreate["username"] = "admin"
        toCreate["password"] = "admin"
        toCreate["realm"] = "master"
        toCreate["state"] = "present"
        toCreate["clientId"] = "test"
        toCreate["force"] = False
        toCreate["clientUrl"] = ["http://test.com"]
        toCreate["sx5url"] = ["http://localhost:8088/clients"]

        results = client(toCreate)
        #print str(results)
        self.assertTrue(results['changed'])
        
    def test_client_not_changed(self):
        toDoNotChange = {}
        toDoNotChange["idp_url"] = "http://localhost:18081"
        toDoNotChange["username"] = "admin"
        toDoNotChange["password"] = "admin"
        toDoNotChange["realm"] = "master"
        toDoNotChange["state"] = "present"
        toDoNotChange["clientId"] = "test2"
        toDoNotChange["force"] = False
        toDoNotChange["clientUrl"] = ["http://test2.com"]
        toDoNotChange["sx5url"] = ["http://localhost:8088/clients"]
        
        client(toDoNotChange)
        results = client(toDoNotChange)
        #print str(results)
        self.assertFalse(results['changed'])

    def test_modify_client(self):
        toChange = {}
        toChange["idp_url"] = "http://localhost:18081"
        toChange["username"] = "admin"
        toChange["password"] = "admin"
        toChange["realm"] = "master"
        toChange["state"] = "present"
        toChange["clientId"] = "test3"
        toChange["force"] = False
        toCreate["clientUrl"] = ["http://test3.com"]
        toCreate["sx5url"] = ["http://localhost:8088/clients"]

        client(toChange)
        toChange["realm"] = "master2"
        results = client(toChange)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['ansible_facts']['client']['realmId'], 'master2', 'master2')
        
    def test_delete_client(self):
        toDelete = {}
        toDelete["idp_url"] = "http://localhost:18081"
        toDelete["username"] = "admin"
        toDelete["password"] = "admin"
        toDelete["realm"] = "master"
        toDelete["state"] = "present"
        toDelete["clientId"] = "test4"
        toDelete["force"] = False
        toCreate["clientUrl"] = ["http://test4.com"]
        toCreate["sx5url"] = ["http://localhost:8088/clients"]

        client(toDelete)
        toDelete["state"] = "absent"
        results = client(toDelete)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'client has been deleted')
