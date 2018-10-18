import collections
import os
import unittest
import requests
from ansible.module_utils.keycloak_utils import *
from ansible.modules.identity.keycloak.keycloak_role import *
from ansible.modules.network.panos.panos_admin import admin_exists

class KeycloakRoleTestCase(unittest.TestCase):
    testClients = [ 
                    {
                        "clientId": "test1",
                        "name": "test1",
                        "description": "Ceci est un test1",
                        "adminUrl": "http://test1.com:8080/admin",
                        "baseUrl": "http://test1.com:8080",
                        "enabled": True,
                        "clientAuthenticatorType": "client-secret",
                        "redirectUris": ["http://test1.com:8080/secure"],
                        "webOrigins": ["http://test1.com:8080/secure"],
                        "consentRequired": False,   
                        "standardFlowEnabled": True,
                        "implicitFlowEnabled": True,
                        "directAccessGrantsEnabled": True,
                        "serviceAccountsEnabled": True,
                        "protocol": "openid-connect",
                        "bearerOnly": False,
                        "publicClient": False,
                        },
                    {
                        "clientId": "test2",
                        "name": "test2",
                        "description": "Ceci est un test2",
                        "adminUrl": "http://test2.com:8080/admin",
                        "baseUrl": "http://test2.com:8080",
                        "enabled": True,
                        "clientAuthenticatorType": "client-secret",
                        "redirectUris": ["http://test2.com:8080/secure"],
                        "webOrigins": ["http://test2.com:8080/secure"],
                        "consentRequired": False,   
                        "standardFlowEnabled": True,
                        "implicitFlowEnabled": True,
                        "directAccessGrantsEnabled": True,
                        "serviceAccountsEnabled": True,
                        "protocol": "openid-connect",
                        "bearerOnly": False,
                        "publicClient": False,
                        }
                    ]
    clientRoles = [
                    {
                        "name":"admin",
                        "description": "Administrator",
                        "composite": False
                        },
                    {
                        "name":"manager",
                        "description": "Manager",
                        "composite": False
                        }
                    ]
    url = "http://localhost:18081"
    headers = ""
    roleSvcBaseUrl = ""
    
    def setUp(self):
        username = "admin"
        password = "admin"
        self.roleSvcBaseUrl = self.url + "/auth/admin/realms/master/roles/"
        # Create Clients
        try:
            self.headers = loginAndSetHeaders(self.url, username, password)
            clientSvcBaseUrl = self.url + "/auth/admin/realms/master/clients/"
            
            for testClient in self.testClients:
                getResponse = requests.get(clientSvcBaseUrl, headers=self.headers, params={'clientId': testClient["clientId"]})
                
                if len(getResponse.json()) == 0:
                    clientData=json.dumps(testClient)
                    requests.post(clientSvcBaseUrl, headers=self.headers, data=clientData)
                    getResponse = requests.get(clientSvcBaseUrl, headers=self.headers, params={'clientId': testClient["clientId"]})
                    clientRepresentation = getResponse.json()[0]
                else:
                    clientRepresentation = getResponse.json()[0]

                getResponse = requests.get(clientSvcBaseUrl, headers=self.headers, params={'clientId': testClient["clientId"]})
                clientRepresentation = getResponse.json()[0]

                for clientRole in self.clientRoles:
                    roleData=json.dumps(clientRole)
                    requests.post(clientSvcBaseUrl + clientRepresentation['id'] + '/roles', headers=self.headers, data=roleData)
                    
        except requests.exceptions.RequestException, e:
            print(str(e))
                
        
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
        try:
            getResponse = requests.get(self.roleSvcBaseUrl + toCreate["name"], headers=self.headers)
            keycloakRole = getResponse.json()
            getResponse = requests.get(self.roleSvcBaseUrl + toCreate["name"] + "/composites", headers=self.headers)
            keycloakRoleComposites = getResponse.json()
        except requests.exceptions.RequestException, e:
            print(str(e)) 
        self.assertTrue(results['changed'])
        self.assertTrue(results['ansible_facts']['role']['composite'])
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
        self.assertTrue(keycloakRole['composite'])
        self.assertEquals(keycloakRole["name"], toCreate["name"], "name: " + keycloakRole["name"] + " : " + toCreate["name"])
        self.assertEquals(keycloakRole["description"], toCreate["description"], "description: " + keycloakRole["description"] + " : " + toCreate["description"])
        self.assertEquals(keycloakRole["containerId"], toCreate["realm"], "containerId: " + keycloakRole["containerId"] + " : " + toCreate["realm"])
        for toCreateComposite in toCreate["composites"]:
            compositeFound = False
            for composite in keycloakRoleComposites:
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
        try:
            getResponse = requests.get(self.roleSvcBaseUrl, headers=self.headers)
            keycloakRoles = getResponse.json()
            roleFound = False
            for keycloakRole in keycloakRoles:
                if keycloakRole["name"] == toDelete["name"]:
                    roleFound = True
                    break
            self.assertFalse(roleFound, 'role ' + toDelete["name"] + ' not deleted')
        except requests.exceptions.RequestException, e:
            print(str(e)) 
    
    def test_modify_role_two_client_role_with_same_name(self):
        toChangeTwoRoles = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test5",
            "description":"Test5",
            "composite":True,
            "composites":[
                {
                    "clientId":"test1",
                    "name":"admin"
                    },
                {
                    "clientId":"test1",
                    "name":"manager"
                    }
            ],
            "state":"present",
            "force":False
        }
        role(toChangeTwoRoles)
        newToChangeTwoRoles = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test5",
            "description":"Modified Test5",
            "composite":True,
            "composites":[
                {
                    "clientId":"test2",
                    "name":"admin"
                    },
                {
                    "clientId":"test2",
                    "name":"manager"
                    }
            ],
            "state":"present",
            "force":False
        }
        results = role(newToChangeTwoRoles)
        try:
            getResponse = requests.get(self.roleSvcBaseUrl + toChangeTwoRoles["name"], headers=self.headers)
            keycloakRole = getResponse.json()
            getResponse = requests.get(self.roleSvcBaseUrl + toChangeTwoRoles["name"] + "/composites", headers=self.headers)
            keycloakRoleComposites = getResponse.json()
            print str(keycloakRole)
            print str(keycloakRoleComposites)
        except requests.exceptions.RequestException, e:
            print(str(e))
        self.assertTrue(results['changed'])
        self.assertTrue(results['ansible_facts']['role']['composite'])
        self.assertEquals(results["ansible_facts"]["role"]["name"], newToChangeTwoRoles["name"], "name: " + results["ansible_facts"]["role"]["name"] + " : " + newToChangeTwoRoles["name"])
        self.assertEquals(results["ansible_facts"]["role"]["description"], newToChangeTwoRoles["description"], "description: " + results["ansible_facts"]["role"]["description"] + " : " + newToChangeTwoRoles["description"])
        self.assertEquals(results["ansible_facts"]["role"]["containerId"], newToChangeTwoRoles["realm"], "containerId: " + results["ansible_facts"]["role"]["containerId"] + " : " + newToChangeTwoRoles["realm"])
        for toChangeComposite in toChangeTwoRoles["composites"]:
            compositeFound = False
            for composite in results['ansible_facts']['composites']:
                if composite["name"] == toChangeComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toChangeComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toChangeComposite["name"], "name: " + toChangeComposite["name"] + ": " + composite["name"])
        for toChangeComposite in newToChangeTwoRoles["composites"]:
            compositeFound = False
            for composite in results['ansible_facts']['composites']:
                if composite["name"] == toChangeComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toChangeComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toChangeComposite["name"], "name: " + toChangeComposite["name"] + ": " + composite["name"])
        
        self.assertTrue(keycloakRole['composite'])
        self.assertEquals(keycloakRole["name"], newToChangeTwoRoles["name"], "name: " + keycloakRole["name"] + " : " + newToChangeTwoRoles["name"])
        self.assertEquals(keycloakRole["description"], newToChangeTwoRoles["description"], "description: " + keycloakRole["description"] + " : " + newToChangeTwoRoles["description"])
        self.assertEquals(keycloakRole["containerId"], newToChangeTwoRoles["realm"], "containerId: " + keycloakRole["containerId"] + " : " + newToChangeTwoRoles["realm"])
        for toChangeComposite in toChangeTwoRoles["composites"]:
            compositeFound = False
            for composite in keycloakRoleComposites:
                if composite["name"] == toChangeComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toChangeComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toChangeComposite["name"], "name: " + toChangeComposite["name"] + ": " + composite["name"])
        for toChangeComposite in newToChangeTwoRoles["composites"]:
            compositeFound = False
            for composite in keycloakRoleComposites:
                if composite["name"] == toChangeComposite["name"]:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, "no composite found: " + toChangeComposite["name"])
            if compositeFound:
                self.assertEqual(composite["name"], toChangeComposite["name"], "name: " + toChangeComposite["name"] + ": " + composite["name"])
