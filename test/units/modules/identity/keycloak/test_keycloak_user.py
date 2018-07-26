import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_user import user
from ansible.modules.identity.keycloak.keycloak_group import group
from ansible.modules.identity.keycloak.keycloak_role import role
from ansible.module_utils.keycloak_utils import isDictEquals

class KeycloakUserTestCase(unittest.TestCase):
    testGroups = [
        {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"testUserGroup1",
            "state":"present",
            "force":False
            },
        {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"testUserGroup2",
            "state":"present",
            "force":False
            }
        ]
    compareExcludes = ["url", "masterUsername", "masterpassword", "realm", "state", "force", "credentials"]
    testRoles = [
        {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"testUserRole1",
            "description":"Test1",
            "state":"present",
            "force":False
        },
                {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"testUserRole2",
            "description":"Test2",
            "state":"present",
            "force":False
        }]
    
    def setUp(self):
        #unittest.TestCase.setUp(self)
        for theGroup in self.testGroups:
            theGroup["state"] = "present"
            group(theGroup)
        for theRole in self.testRoles:
            theRole["state"] = "present"
            role(theRole)
 
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
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}], 
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1","testUserRole2"],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "groups": ["testUserGroup1","testUserGroup2"],
            "state":"present",
            "force":"no"
        }

        results = user(toCreate)
        self.assertTrue(results['changed'])
        self.assertTrue(isDictEquals(toCreate, results["ansible_facts"]["user"], self.compareExcludes), "user: " + str(toCreate) + " : " + str(results["ansible_facts"]["user"]))

    def test_user_not_changed(self):
        toDoNotChange = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user2",
            "firstName": "user2",
            "lastName": "user2",
            "email": "user2@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1","testUserRole2"],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "groups": ["testUserGroup1","testUserGroup2"],
            "state": "present",
            "force": False
        }

        user(toDoNotChange)
        results = user(toDoNotChange)

        self.assertFalse(results['changed'])
        self.assertEquals(results["ansible_facts"]["user"]["username"], toDoNotChange["username"], "username: " + results["ansible_facts"]["user"]["username"] + " : " + toDoNotChange["username"])
        self.assertEquals(results["ansible_facts"]["user"]["firstName"], toDoNotChange["firstName"], "firstName: " + results["ansible_facts"]["user"]["firstName"] + " : " + toDoNotChange["firstName"])
        self.assertEquals(results["ansible_facts"]["user"]["lastName"], toDoNotChange["lastName"], "lastName: " + results["ansible_facts"]["user"]["lastName"] + " : " + toDoNotChange["lastName"])
        self.assertTrue(isDictEquals(toDoNotChange, results["ansible_facts"]["user"], self.compareExcludes), "user: " + str(toDoNotChange) + " : " + str(results["ansible_facts"]["user"]))

    def test_user_modify_force(self):
        toDoNotChange = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user3",
            "firstName": "user3",
            "lastName": "user3",
            "email": "user3@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1","testUserRole2"],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "groups": ["testUserGroup1","testUserGroup2"],
            "state":"present",
            "force": False
        }

        user(toDoNotChange)
        toDoNotChange["force"] = True
        results = user(toDoNotChange)
        self.assertTrue(results['changed'])
        self.assertTrue(isDictEquals(toDoNotChange, results["ansible_facts"]["user"], self.compareExcludes), "user: " + str(toDoNotChange) + " : " + str(results["ansible_facts"]["user"]))

    def test_modify_user(self):
        toChange = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user4",
            "firstName": "user4",
            "lastName": "user4",
            "email": "user4@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1"],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "groups": ["testUserGroup1"],
            "state":"present",
            "force": False
        }
        user(toChange)
        toChange["lastName"] = "usernew4"
        toChange["clientRoles"] = [{"clientId": "master-realm","roles": ["manage-clients","query-groups"]}]
        toChange["realmRoles"] = ["testUserRole1","testUserRole2"]
        results = user(toChange)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["user"]["lastName"], toChange["lastName"], "lastName: " + results["ansible_facts"]["user"]["lastName"] + " : " + toChange["lastName"])
        self.assertTrue(isDictEquals(toChange, results["ansible_facts"]["user"], self.compareExcludes), "user: " + str(toChange) + " : " + str(results["ansible_facts"]["user"]))
        
    def test_delete_user(self):
        toDelete = {
            "url": "http://localhost:18081",
            "masterUsername": "admin",
            "masterpassword": "admin",
            "realm": "master",
            "username": "user5",
            "firstName": "user5",
            "lastName": "user5",
            "email": "user5@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["uma_authorization","offline_access"],
            "attributes": {"attr1": ["value1"],"attr2": ["value2"]},
            "groups": ["testUserGroup1","testUserGroup2"],
            "state":"present",
            "force": False
        }

        user(toDelete)
        toDelete["state"] = "absent"
        results = user(toDelete)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'user has been deleted')

    def tearDown(self):
        #unittest.TestCase.tearDown(self)
        for theGroup in self.testGroups:
            theGroup["state"] = "absent"
            group(theGroup)
        for theRole in self.testRoles:
            theRole["state"] = "absent"
            role(theRole)
