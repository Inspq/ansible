import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_user import *

class KeycloakUserTestCase(unittest.TestCase):
 
    def test_create_user(self):
        toCreate = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user1",
            "firstName": "user1",
            "lastName": "user1",
            "email": "user1@user.ca",
            "enabled": 'true',
            "emailVerified": 'false',
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "state":"present",
            "force":False
        }

        results = user(toCreate)
        print str(results)
        self.assertTrue(results['changed'])

    def test_user_not_changed(self):
        toDoNotChange = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user1",
            "firstName": "user1",
            "lastName": "user1",
            "email": "user1@user.ca",
            "enabled": 'true',
            "emailVerified": 'false',
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "state":"present",
            "force":False
        }

        results = user(toDoNotChange)
        #print str(results)
        results = user(toDoNotChange)
        #print str(results)
        self.assertFalse(results['changed'])
        self.assertEquals(results["ansible_facts"]["user"]["username"], toDoNotChange["username"], "username: " + results["ansible_facts"]["user"]["username"] + " : " + toDoNotChange["username"])
        self.assertEquals(results["ansible_facts"]["user"]["firstName"], toDoNotChange["firstName"], "firstName: " + results["ansible_facts"]["user"]["firstName"] + " : " + toDoNotChange["firstName"])
        self.assertEquals(results["ansible_facts"]["user"]["lastName"], toDoNotChange["lastName"], "lastName: " + results["ansible_facts"]["user"]["lastName"] + " : " + toDoNotChange["lastName"])
        self.assertEquals(results["ansible_facts"]["user"]["enabled"], toDoNotChange["enabled"], "enabled: " + results["ansible_facts"]["user"]["enabled"] + " : " + toDoNotChange["enabled"])

    def test_user_modify_force(self):
        toDoNotChange = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user1",
            "firstName": "user1",
            "lastName": "user1",
            "email": "user1@user.ca",
            "enabled": 'true',
            "emailVerified": 'false',
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "state":"present",
            "force":False
        }

        user(toDoNotChange)
        toDoNotChange["force"] = True
        results = user(toDoNotChange)
        print str(results)
        #self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["user"]["lastName"], toDoNotChange["lastName"], "lastName: " + results["ansible_facts"]["user"]["lastName"] + " : " + toDoNotChange["lastName"])

    def test_modify_user(self):
        toChange = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user1",
            "firstName": "user1",
            "lastName": "user1",
            "email": "user1@user.ca",
            "enabled": 'true',
            "emailVerified": 'false',
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "state":"present",
            "force":False
        }
        user(toChange)
        toChange["lastName"] = "user2"
        results = user(toChange)
        print str(results)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["user"]["lastName"], toChange["lastName"], "lastName: " + results["ansible_facts"]["user"]["lastName"] + " : " + toChange["lastName"])
        
        
    def test_delete_role(self):
        toDelete = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user1",
            "firstName": "user1",
            "lastName": "user1",
            "email": "user1@user.ca",
            "enabled": 'true',
            "emailVerified": 'false',
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "state":"present",
            "force":False
        }

        user(toDelete)
        toDelete["state"] = "absent"
        results = user(toDelete)
        print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'user has been deleted')
