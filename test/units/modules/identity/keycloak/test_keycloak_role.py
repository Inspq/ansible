import collections
import os
import unittest

from ansible.modules.identity.keycloak.keycloak_role import *

class KeycloakRoleTestCase(unittest.TestCase):
 
    def test_create_role(self):
        toCreate = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test1",
            "description":"Test1",
            "composite":True,
            "composites":[
                {
                    "clientId":"master-realm",
                    "name":"manage-clients"
                    },
                {
                    "clientId":"master-realm",
                    "name":"manage-users"
                    },
                {
                    "name":"uma_authorization"}
            ],
            "state":"present",
            "force":False
        }

        results = role(toCreate)
        
        self.assertTrue(results['ansible_facts']['role']['composite'])
        # self.assertFalse(results['ansible_facts']['role']['scopeParamRequired'])
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["role"]["name"], toCreate["name"], "name: " + results["ansible_facts"]["role"]["name"] + " : " + toCreate["name"])
        self.assertEquals(results["ansible_facts"]["role"]["description"], toCreate["description"], "description: " + results["ansible_facts"]["role"]["description"] + " : " + toCreate["description"])
        self.assertEquals(results["ansible_facts"]["role"]["containerId"], toCreate["realm"], "containerId: " + results["ansible_facts"]["role"]["containerId"] + " : " + toCreate["realm"])
        for toCreateComposite in toCreate["composites"]:
            compositeFound = False
            for composite in results['ansible_facts']['composites']:
                if composite["name"] == toCreateComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toCreateComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toCreateComposite["name"], "name: " + toCreateComposite["name"] + ": " + composite["name"])

    def test_role_not_changed(self):
        toDoNotChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test2",
            "description":"Test2",
            "composite":True,
            "composites":[
                {
                    "clientId":"master-realm",
                    "name":"manage-clients"
                    },
                {
                    "clientId":"master-realm",
                    "name":"manage-users"
                    },
                {
                    "name":"uma_authorization"}
            ],
            "state":"present",
            "force":False
        }

        role(toDoNotChange)
        results = role(toDoNotChange)
        
        self.assertFalse(results['changed'])
        self.assertTrue(results['ansible_facts']['role']['composite'])
        # self.assertFalse(results['ansible_facts']['role']['scopeParamRequired'])
        self.assertEquals(results["ansible_facts"]["role"]["name"], toDoNotChange["name"], "name: " + results["ansible_facts"]["role"]["name"] + " : " + toDoNotChange["name"])
        self.assertEquals(results["ansible_facts"]["role"]["description"], toDoNotChange["description"], "description: " + results["ansible_facts"]["role"]["description"] + " : " + toDoNotChange["description"])
        self.assertEquals(results["ansible_facts"]["role"]["containerId"], toDoNotChange["realm"], "containerId: " + results["ansible_facts"]["role"]["containerId"] + " : " + toDoNotChange["realm"])
        for toDoNotChangeComposite in toDoNotChange["composites"]:
            compositeFound = False
            for composite in results['ansible_facts']['composites']:
                if composite["name"] == toDoNotChangeComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toDoNotChangeComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toDoNotChangeComposite["name"], "name: " + toDoNotChangeComposite["name"] + ": " + composite["name"])

    def test_role_modify_force(self):
        toDoNotChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test5",
            "description":"Test5",
            "composite":True,
            "composites":[
                {
                    "clientId":"master-realm",
                    "name":"manage-clients"
                    },
                {
                    "clientId":"master-realm",
                    "name":"manage-users"
                    },
                {
                    "name":"uma_authorization"}
            ],
            "state":"present",
            "force":False
        }

        role(toDoNotChange)
        toDoNotChange["force"] = True
        results = role(toDoNotChange)
        self.assertTrue(results['changed'])
        self.assertTrue(results['ansible_facts']['role']['composite'])
        # self.assertFalse(results['ansible_facts']['role']['scopeParamRequired'])
        self.assertEquals(results["ansible_facts"]["role"]["name"], toDoNotChange["name"], "name: " + results["ansible_facts"]["role"]["name"] + " : " + toDoNotChange["name"])
        self.assertEquals(results["ansible_facts"]["role"]["description"], toDoNotChange["description"], "description: " + results["ansible_facts"]["role"]["description"] + " : " + toDoNotChange["description"])
        self.assertEquals(results["ansible_facts"]["role"]["containerId"], toDoNotChange["realm"], "containerId: " + results["ansible_facts"]["role"]["containerId"] + " : " + toDoNotChange["realm"])
        for toDoNotChangeComposite in toDoNotChange["composites"]:
            compositeFound = False
            for composite in results['ansible_facts']['composites']:
                if composite["name"] == toDoNotChangeComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toDoNotChangeComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toDoNotChangeComposite["name"], "name: " + toDoNotChangeComposite["name"] + ": " + composite["name"])

    def test_modify_role(self):
        toChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test3",
            "description":"Test3",
            "composite":True,
            "composites":[
                {
                    "clientId":"master-realm",
                    "name":"manage-clients"
                    },
                {
                    "clientId":"master-realm",
                    "name":"manage-users"
                    },
                {
                    "name":"uma_authorization"}
            ],
            "state":"present",
            "force":False
        }
        role(toChange)
        newToChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test3",
            "description":"Modified Test3",
            "composite":True,
            "composites":[
                {
                    "clientId":"master-realm",
                    "name":"manage-events"
                    },
                {
                    "clientId":"account",
                    "name":"manage-account"
                    }
            ],
            "state":"present",
            "force":False
        }
        results = role(newToChange)
        self.assertTrue(results['ansible_facts']['role']['composite'])
        # self.assertFalse(results['ansible_facts']['role']['scopeParamRequired'])
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["role"]["name"], newToChange["name"], "name: " + results["ansible_facts"]["role"]["name"] + " : " + newToChange["name"])
        self.assertEquals(results["ansible_facts"]["role"]["description"], newToChange["description"], "description: " + results["ansible_facts"]["role"]["description"] + " : " + newToChange["description"])
        self.assertEquals(results["ansible_facts"]["role"]["containerId"], newToChange["realm"], "containerId: " + results["ansible_facts"]["role"]["containerId"] + " : " + newToChange["realm"])
        for toChangeComposite in toChange["composites"]:
            compositeFound = False
            for composite in results['ansible_facts']['composites']:
                if composite["name"] == toChangeComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toChangeComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toChangeComposite["name"], "name: " + toChangeComposite["name"] + ": " + composite["name"])
        for toChangeComposite in newToChange["composites"]:
            compositeFound = False
            for composite in results['ansible_facts']['composites']:
                if composite["name"] == toChangeComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toChangeComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toChangeComposite["name"], "name: " + toChangeComposite["name"] + ": " + composite["name"])
        
        
    def test_delete_role(self):
        toDelete = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test4",
            "description":"Test4",
            "composite":True,
            "composites":[
                {
                    "clientId":"master-realm",
                    "name":"manage-clients"
                    },
                {
                    "clientId":"master-realm",
                    "name":"manage-users"
                    },
                {
                    "name":"uma_authorization"}
            ],
            "state":"present",
            "force":False
        }

        role(toDelete)
        toDelete["state"] = "absent"
        results = role(toDelete)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'role has been deleted')
