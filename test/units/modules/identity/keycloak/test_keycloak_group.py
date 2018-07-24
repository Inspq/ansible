import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_group import *
from ansible.module_utils.keycloak_utils import isDictEquals

class KeycloakGroupTestCase(unittest.TestCase):
 
    def test_create_group(self):
        toCreate = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test1",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "realmRoles": [
                "uma_authorization"
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users",
                    "view-identity-providers"
                    ]
                }
            ], 
            "state":"present",
            "force":False
        }

        results = group(toCreate)
        print (str(results))
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toCreate["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toCreate["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], toCreate["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toCreate["attributes"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toCreate["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toCreate["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toCreate["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toCreate["realmRoles"]))
        
    def test_group_not_changed(self):
        toDoNotChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test2",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "realmRoles": [
                "uma_authorization"
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users"
                    ]
                }
            ], 
            "state":"present",
            "force":False
        }

        group(toDoNotChange)
        results = group(toDoNotChange)
        
        self.assertFalse(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toDoNotChange["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toDoNotChange["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], toDoNotChange["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toDoNotChange["attributes"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toDoNotChange["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toDoNotChange["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toDoNotChange["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toDoNotChange["realmRoles"]))

    def test_group_modify_force(self):
        toDoNotChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test3",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "realmRoles": [
                "uma_authorization"
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users"
                    ]
                }
            ], 
            "state":"present",
            "force":False
        }

        group(toDoNotChange)
        toDoNotChange["force"] = True
        results = group(toDoNotChange)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toDoNotChange["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toDoNotChange["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], toDoNotChange["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toDoNotChange["attributes"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toDoNotChange["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toDoNotChange["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toDoNotChange["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toDoNotChange["realmRoles"]))

    def test_modify_group(self):
        toChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test4",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "realmRoles": [
                "uma_authorization",
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users",
                    "view-identity-providers"
                    ]
                }
            ],
            "state":"present",
            "force":False
        }
        group(toChange)
        toChange["attributes"] = {
            "attr3":["value3"]
            }
        toChange["realmRoles"] = [
                "uma_authorization",
                "offline_access"
            ]

        toChange["clientRoles"] = [{
            "clientid": "master-realm",
            "roles": [
                "view-clients",
                "query-realms",
                "view-users"
                ]
            },{
            "clientid": "account",
            "roles": [
                "manage-account-links",
                "view-profile",
                "manage-account"
                ]
            }
        ]
        results = group(toChange)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toChange["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toChange["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], toChange["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toChange["attributes"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toChange["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toChange["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toChange["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toChange["realmRoles"]))

        
    def test_delete_group(self):
        toDelete = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test5",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "state":"present",
            "force":False
        }

        group(toDelete)
        toDelete["state"] = "absent"
        results = group(toDelete)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'group has been deleted')
