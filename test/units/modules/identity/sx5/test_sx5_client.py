import collections
import os
import unittest


from ansible.modules.identity.sx5.sx5_client import *

class KeycloakClientTestCase(unittest.TestCase):
 
    def test_create_client(self):
        toCreate = {}
        toCreate["idp_url"] = "http://localhost:18081"
        toCreate["username"] = "admin"
        toCreate["password"] = "admin"
        toCreate["realm"] = "master"
        toCreate["sx5url"] = "http://localhost:18084/clients"
        toCreate["clientUrl"] = "http://localhost/test1"
        toCreate["state"] = "present"
        toCreate["clientId"] = "test"
        toCreate["force"] = False
        
        results = client(toCreate)
        #print str(results)
    
        self.assertTrue(results['changed'])

    def test_client_not_changed(self):
        toDoNotChange = {}
        toDoNotChange["idp_url"] = "http://localhost:18081"
        toDoNotChange["username"] = "admin"
        toDoNotChange["password"] = "admin"
        toDoNotChange["realm"] = "master"
        toDoNotChange["sx5url"] = "http://localhost:18084/clients"
        toDoNotChange["clientUrl"] = "http://localhost/test1"
        toDoNotChange["state"] = "present"
        toDoNotChange["clientId"] = "test"
        toDoNotChange["force"] = False

        client(toDoNotChange)
        #print str(results)
        results = client(toDoNotChange)
        #print str(results)
        self.assertFalse(results['changed'])

    def test_modify_client(self):
        toChange = {}
        toChange["idp_url"] = "http://localhost:18081"
        toChange["username"] = "admin"
        toChange["password"] = "admin"
        toChange["realm"] = "master"
        toChange["sx5url"] = "http://localhost:18084/clients"
        toChange["clientUrl"] = "http://localhost/test1"
        toChange["state"] = "present"
        toChange["clientId"] = "test"
        toChange["force"] = False

        client(toChange)
        toChange["clientUrl"] = "http://localhost/test1"
       
        results = client(toChange)
        print str(results)
        self.assertTrue(results['changed'])
        
        
    def test_delete_client(self):
        toDelete = {}
        toDelete["idp_url"] = "http://localhost:18081"
        toDelete["username"] = "admin"
        toDelete["password"] = "admin"
        toDelete["realm"] = "master"
        toDelete["clientUrl"] = "http://localhost:18084/clients"
        toDelete["sx5url"] = "http://localhost/client1"
        toDelete["state"] = "present"
        toDelete["clientId"] = "test"
        toDelete["force"] = False

        client(toDelete)
        toDelete["state"] = "absent"
        results = client(toDelete)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'client has been deleted')
