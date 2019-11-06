from ansible.module_utils.identity.keycloak.keycloak import isDictEquals
from ansible.module_utils.keycloak_utils import loginAndSetHeaders
from ansible.modules.identity.keycloak import keycloak_role
from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args
import requests
import json

class KeycloakRoleTestCase(ModuleTestCase):
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
                    },
                    {
                        "clientId": "TestUPPER_underscore",
                        "name": "Test client with uppercase and underscore",
                        "description": "Tish is a client with uppercase letters and underscore in clientID",
                        "adminUrl": "http://testupper.com:8080/admin",
                        "baseUrl": "http://testupper.com:8080",
                        "enabled": True,
                        "clientAuthenticatorType": "client-secret",
                        "redirectUris": ["http://testupper.com:8080/secure"],
                        "webOrigins": ["http://testupper.com:8080/secure"],
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
    testRoles = [
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_create_role",
            "description":"Test create role",
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
            "state":"absent",
            "force":False
        },
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_role_not_changed",
            "description":"Test role not changed",
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
        },
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_role_modify_force",
            "description":"test_role_modify_force",
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
        },
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_modify_role",
            "description":"Test modify role",
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
        },
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_delete_role",
            "description":"Test delete role",
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
        },
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_modify_role_two_client_role_with_same_name",
            "description":"Test modify role two client roles with same name",
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
        },
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_role_with_client_roles_containing_uppercase_and_underscore",
            "description":"Test create role with client roles containing uppercase and underscore",
            "composite":True,
            "composites":[
                {
                    "clientId":"TestUPPER_underscore",
                    "name":"admin"
                    }
            ],
            "state":"absent",
            "force":False
        },
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_role_with_non_existing_client_role",
            "description":"Test create role with client roles of non existing client",
            "state":"absent",
            "force":False
        },
        {
            "auth_username":"admin", 
            "auth_password":"admin",
            "realm":"master",
            "auth_keycloak_url":"http://localhost:18081/auth",
            "name":"test_role_with_existing_client_but_non_existing_role",
            "description":"Test modify role with existing client but non existing roles",
            "state":"present",
            "force":False
        }
    ]

    roleExcudes = ["auth_keycloak_url","auth_username","auth_password","state","force","realm","composites","_ansible_keep_remote_files","_ansible_remote_tmp"]
    kc = None
    
    def setUp(self):
        super(KeycloakRoleTestCase, self).setUp()
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

        self.module = keycloak_role
        for role in self.testRoles:
            set_module_args(role)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()

    def tearDown(self):
        username = "admin"
        password = "admin"
        # Delete Clients
        try:
            self.headers = loginAndSetHeaders(self.url, username, password)
            clientSvcBaseUrl = self.url + "/auth/admin/realms/master/clients/"
            
            for testClient in self.testClients:
                getResponse = requests.get(clientSvcBaseUrl, headers=self.headers, params={'clientId': testClient["clientId"]})
                
                if len(getResponse.json()) > 0:
                    clientRepresentation = getResponse.json()[0]
                    requests.delete(clientSvcBaseUrl + clientRepresentation["id"], headers=self.headers)
        except requests.exceptions.RequestException, e:
            print(str(e))
        # Delete roles
        self.module = keycloak_role
        for role in self.testRoles:
            theRole = role.copy()
            theRole["state"] = "absent"
            set_module_args(theRole)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
        
        super(KeycloakRoleTestCase, self).tearDown()           
        
    def test_create_role(self):
        toCreate = self.testRoles[0].copy()
        toCreate["state"] = "present"
        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(toCreate, results.exception.args[0]['role'], self.roleExcudes), 'Realm role created does not comply to specifications.')
        self.assertTrue(isDictEquals(toCreate["composites"], results.exception.args[0]['composites'], self.roleExcudes), 'Realm role composites created does not comply to specifications.')
    
    def test_role_not_changed(self):
        toDoNotChange = self.testRoles[1].copy()
        set_module_args(toDoNotChange)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertFalse(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(toDoNotChange, results.exception.args[0]['role'], self.roleExcudes), 'Realm role not modified does not comply to specifications.')
        self.assertTrue(isDictEquals(toDoNotChange["composites"], results.exception.args[0]['composites'], self.roleExcudes), 'Realm role composites not modified does not comply to specifications.')

    def test_role_modify_force(self):
        toDoNotChange = self.testRoles[2].copy()
        toDoNotChange["force"] = True
        set_module_args(toDoNotChange)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(toDoNotChange, results.exception.args[0]['role'], self.roleExcudes), 'Realm role not modified force does not comply to specifications.')
        self.assertTrue(isDictEquals(toDoNotChange["composites"], results.exception.args[0]['composites'], self.roleExcudes), 'Realm role composites not modified force does not comply to specifications.')

    def test_modify_role(self):
        newToChange = self.testRoles[3].copy()
        newToChange["description"] = newToChange["description"] + " modified"
        set_module_args(newToChange)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(newToChange, results.exception.args[0]['role'], self.roleExcudes), 'Realm role modified does not comply to specifications.')
        self.assertTrue(isDictEquals(newToChange["composites"], results.exception.args[0]['composites'], self.roleExcudes), 'Realm role composites modified does not comply to specifications.')        
        
    def test_delete_role(self):
        toDelete = self.testRoles[4].copy()
        toDelete["state"] = "absent"
        set_module_args(toDelete)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'deleted', 'Realm role not deleted')

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
        newToChangeTwoRoles = self.testRoles[5].copy()
        newToChangeTwoRoles["description"] = newToChangeTwoRoles["description"] + " modified"
        newToChangeTwoRoles["composites"] = [
                {
                    "clientId":"test2",
                    "name":"admin"
                    },
                {
                    "clientId":"test2",
                    "name":"manager"
                    }
            ]
        set_module_args(newToChangeTwoRoles)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(newToChangeTwoRoles, results.exception.args[0]['role'], self.roleExcudes), 'Realm role modified two client roles does not comply to specifications.')
        newComposites = []
        for composite in self.testRoles[5]["composites"]:
            newComposites.append(composite)
        for composite in newToChangeTwoRoles["composites"]:
            newComposites.append(composite)
        self.assertTrue(isDictEquals(newComposites, results.exception.args[0]['composites'], self.roleExcudes), 'Realm role composites modified two client roles does not comply to specifications.')
        
    def test_create_role_composites_with_client_role_clientid_contain_uppercase_and_underscore(self):
        toCreate = self.testRoles[6].copy()
        toCreate["state"] = "present"
        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(toCreate, results.exception.args[0]['role'], self.roleExcudes), 'Realm role created does not comply to specifications.')
        self.assertTrue(isDictEquals(toCreate["composites"], results.exception.args[0]['composites'], self.roleExcudes), 'Realm role composites created does not comply to specifications.')

    def test_create_role_composites_with_non_existing_client(self):
        toCreate = self.testRoles[7].copy()
        toCreate["composite"] = True
        toCreate["composites"] = [
            {
                "clientId":"InexistingClient",
                "name":"admin"
                }
            ]
        toCreate["state"] = "present"
        set_module_args(toCreate)
        with self.assertRaises(AnsibleFailJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['failed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'client ' + toCreate["composites"][0]["clientId"] + ' not found', 'error not generated: ' + results.exception.args[0]['msg'])

    def test_modify_role_composites_existing_client_but_non_existing_role(self):
        toCreate = self.testRoles[8].copy()
        toCreate["composite"] = True
        toCreate["composites"] = [
            {
                "clientId":"TestUPPER_underscore",
                "name":"nonexistingrole"
                }
            ]
        set_module_args(toCreate)
        with self.assertRaises(AnsibleFailJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['failed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'HTTP Error 404', 'error not generated: ' + results.exception.args[0]['msg'])
