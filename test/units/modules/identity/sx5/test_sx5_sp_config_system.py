import requests

from ansible.modules.identity.sx5.sx5_sp_config_system import system
from ansible.modules.identity.keycloak import keycloak_client
from ansible.module_utils.sx5_sp_config_system_utils import loginAndSetHeaders
from units.modules.utils import AnsibleExitJson, ModuleTestCase, set_module_args

class Sx5SystemTestCase(ModuleTestCase):
    def setUp(self):
        super(Sx5SystemTestCase, self).setUp()
        clientsToCreate = [
            {
                "clientId": "clientsystem11",
                "name": "clientsystem11",
                "roles": [{"name":"test1","description": "test1","composite": "False"},
                             {"name":"toCreate","description": "toCreate","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystem21",
                "name": "clientsystem21",
                "roles": [{"name":"test2","description": "test2","composite": "False"},
                             {"name":"toDoNotChange","description": "toDoNotChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystem31",
                "name": "clientsystem31",
                "roles": [{"name":"test31","description": "test31","composite": "False"},
                             {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystemChange31",
                "name": "clientsystemChange31",
                "roles": [{"name":"test31","description": "test31","composite": "False"},
                             {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystem32",
                "name": "clientsystem32",
                "roles": [{"name":"test32","description": "test32","composite": "False"},
                             {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystemChange32",
                "name": "clientsystemChange32",
                "roles": [{"name":"test32","description": "test32","composite": "False"},
                             {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystemNS1",
                "name": "clientsystemNS1",
                "roles": [{"name":"testNS1","description": "testNS1","composite": "False"},
                             {"name":"toCreate","description": "toCreate","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            
            {
                "clientId": "clientsystemNS21",
                "name": "clientsystemNS21",
                "roles": [{"name":"testNS2","description": "testNS2","composite": "False"},
                             {"name":"toDoNotChange","description": "toDoNotChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystemNS31",
                "name": "clientsystemNS31",
                "roles": [{"name":"testNS31","description": "testNS31","composite": "False"},
                             {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystemChangeNS31",
                "name": "clientsystemChangeNS31",
                "roles": [{"name":"testNS31","description": "testNS31","composite": "False"},
                             {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystemNS32",
                "name": "clientsystemNS32",
                "roles": [{"name":"testNS32","description": "testNS32","composite": "False"},
                             {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystemChangeNS32",
                "name": "clientsystemChangeNS32",
                "roles": [{"name":"testNS32","description": "testNS32","composite": "False"},
                             {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "clientsystem41",
                "name": "clientsystem41",
                "roles": [{"name":"test4","description": "test4","composite": "False"},
                             {"name":"toDelete","description": "toDelete","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "habilitationClient1",
                "name": "habilitationClient1",
                "roles": [{"name":"HRole1","description": "HRole1","composite": "False"},
                             {"name":"HRole2","description": "HRole2","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "habilitationClient2",
                "name": "habilitationClient2",
                "roles": [{"name":"HRole1","description": "HRole1","composite": "False"},
                             {"name":"HRole2","description": "HRole2","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "habilitationClient3",
                "name": "habilitationClient3",
                "roles": [{"name":"HRole1","description": "HRole1","composite": "False"},
                             {"name":"HRole2","description": "HRole2","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "habilitationClient4",
                "name": "habilitationClient4",
                "roles": [{"name":"HRole1","description": "HRole1","composite": "False"},
                             {"name":"HRole2","description": "HRole2","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                },
            {
                "clientId": "habilitationClient5",
                "name": "habilitationClient5",
                "roles": [{"name":"HRole1","description": "HRole1","composite": "False"},
                             {"name":"HRole2","description": "HRole2","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                }
            ]
        toCreateClient = {}
        toCreateClient["auth_keycloak_url"] = "http://localhost:18081/auth"
        toCreateClient["auth_username"] = "admin"
        toCreateClient["auth_password"] = "admin"
        toCreateClient["realm"] = "master"
        toCreateClient["state"] = "present"
        toCreateClient["rootUrl"] = "http://test.com:18182"
        toCreateClient["description"] = "Ceci est un test"
        toCreateClient["adminUrl"] = "http://test.com:18182/admin"
        toCreateClient["enabled"] = True
        toCreateClient["clientAuthenticatorType"] = "client-secret"
        toCreateClient["redirectUris"] = ["http://test.com:18182/secure","http://test1.com:18182/secure"]
        toCreateClient["webOrigins"] = ["*"]
        toCreateClient["bearerOnly"] = False
        toCreateClient["publicClient"] = False
        toCreateClient["force"] = False
        self.module = keycloak_client

        for theClient in clientsToCreate:
            toCreateClient["clientId"] = theClient["clientId"]
            toCreateClient["name"] = theClient["name"]
            toCreateClient["roles"] = theClient["roles"]
            set_module_args(toCreateClient)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
    
    def test_create_system(self):
        toCreate = {}
        toCreate["spUrl"] = "http://localhost:18081"
        toCreate["spUsername"] = "admin"
        toCreate["spPassword"] = "admin"
        toCreate["spRealm"] = "master"
        toCreate["spConfigClient_id"] = "admin-cli" 
        toCreate["spConfigClient_secret"] = ""
        toCreate["spConfigUrl"] = "http://localhost:18182/config"
        toCreate["systemName"] = "system1"
        toCreate["systemShortName"] = "S1"
        toCreate["clients"] = [{"clientId": "clientsystem11"}]
        toCreate["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toCreate["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toCreate["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toCreate["clientRoles"] = [{"spClientRoleId": "test1", "spClientRoleName": "test1", "spClientRoleDescription": "test1"},{"spClientRoleId": "toCreate", "spClientRoleName": "toCreate", "spClientRoleDescription": "toCreate"}]
        toCreate["pilotRoles"] = [{"habilitationClientId": "habilitationClient1", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        toCreate["state"] = "present"
        toCreate["force"] = False
    
        results = system(toCreate)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["systemes"]["nom"], toCreate["systemName"], "systemName: " + results["ansible_facts"]["systemes"]["nom"] + " : " + toCreate["systemName"])

    def test_system_not_changed(self):
        toDoNotChange = {}
        toDoNotChange["spUrl"] = "http://localhost:18081"
        toDoNotChange["spUsername"] = "admin"
        toDoNotChange["spPassword"] = "admin"
        toDoNotChange["spRealm"] = "master"
        toDoNotChange["spConfigClient_id"] = "admin-cli" 
        toDoNotChange["spConfigClient_secret"] = ""
        toDoNotChange["spConfigUrl"] = "http://localhost:18182/config"
        toDoNotChange["systemName"] = "system2"
        toDoNotChange["systemShortName"] = "S2"
        toDoNotChange["clients"] = [{"clientId": "clientsystem21"}]
        toDoNotChange["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toDoNotChange["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toDoNotChange["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toDoNotChange["clientRoles"] = [{"spClientRoleId": "test2", "spClientRoleName": "test2", "spClientRoleDescription": "test2"},{"spClientRoleId": "toDoNotChange", "spClientRoleName": "toDoNotChange", "spClientRoleDescription": "toDoNotChange"}]
        toDoNotChange["pilotRoles"] = [{"habilitationClientId": "habilitationClient2", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem21", "name": "test2"}], "state": "present"}]}]
        toDoNotChange["state"] = "present"
        toDoNotChange["force"] = False

        system(toDoNotChange)
        #print str(results)
        results = system(toDoNotChange)
        #print str(results)
        self.assertFalse(results['changed'])

    def test_modify_system_no_pilotRoles(self):
        toChange1 = {}
        toChange1["spUrl"] = "http://localhost:18081"
        toChange1["spUsername"] = "admin"
        toChange1["spPassword"] = "admin"
        toChange1["spRealm"] = "master"
        toChange1["spConfigClient_id"] = "admin-cli" 
        toChange1["spConfigClient_secret"] = ""
        toChange1["spConfigUrl"] = "http://localhost:18182/config"
        toChange1["systemName"] = "system3"
        toChange1["systemShortName"] = "S3"
        toChange1["clients"] = [{"clientId": "clientsystem31"}]
        toChange1["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toChange1["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toChange1["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toChange1["clientRoles"] = [{"spClientRoleId": "test31", "spClientRoleName": "test31", "spClientRoleDescription": "test31"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChange1["state"] = "present"
        toChange1["force"] = False

        results = system(toChange1)
        print str(results)
        toChange1["sadu_principal"] = "http://localhost/test3"
        toChange1["clients"] = [{"clientId": "clientsystemChange31"}]
        NnClient=len(toChange1["clients"])+1
        results = system(toChange1)
        print str(results)
        self.assertTrue(results['changed'])
        for adressesApprovisionnement in results["ansible_facts"]["entreesAdressesApprovisionnement"]["entreesAdressesApprovisionnement"]:
            if adressesApprovisionnement["principale"]:
                self.assertEquals(adressesApprovisionnement["adresse"], toChange1["sadu_principal"], "sadu_principal: " + adressesApprovisionnement["adresse"] + " : " + toChange1["sadu_principal"])
        
        self.assertEquals(len(results["ansible_facts"]["systemes"]["composants"]), 
                          NnClient, 
                          str(len(results["ansible_facts"]["systemes"]["composants"])) + " : " + str(NnClient))

    def test_modify_system_with_pilotRoles(self):
        toChangep = {}
        toChangep["spUrl"] = "http://localhost:18081"
        toChangep["spUsername"] = "admin"
        toChangep["spPassword"] = "admin"
        toChangep["spRealm"] = "master"
        toChangep["spConfigClient_id"] = "admin-cli" 
        toChangep["spConfigClient_secret"] = ""
        toChangep["spConfigUrl"] = "http://localhost:18182/config"
        toChangep["systemName"] = "system3"
        toChangep["systemShortName"] = "S3"
        toChangep["clients"] = [{"clientId": "clientsystem31"}]
        toChangep["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toChangep["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toChangep["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toChangep["clientRoles"] = [{"spClientRoleId": "test31", "spClientRoleName": "test31", "spClientRoleDescription": "test31"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChangep["pilotRoles"] = [{"habilitationClientId": "habilitationClient3", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        toChangep["state"] = "present"
        toChangep["force"] = False

        results = system(toChangep)
        #print str(results)
        toChangep["sadu_principal"] = "http://localhost/test3"
        toChangep["clients"] = [{"clientId": "clientsystemChange31"}]
        NnClient=len(toChangep["clients"])+1
        results = system(toChangep)
        #print str(results)
        self.assertTrue(results['changed'])
        for adressesApprovisionnement in results["ansible_facts"]["entreesAdressesApprovisionnement"]["entreesAdressesApprovisionnement"]:
            if adressesApprovisionnement["principale"]:
                self.assertEquals(adressesApprovisionnement["adresse"], toChangep["sadu_principal"], "sadu_principal: " + adressesApprovisionnement["adresse"] + " : " + toChangep["sadu_principal"])
        
        self.assertEquals(len(results["ansible_facts"]["systemes"]["composants"]), 
                          NnClient, 
                          str(len(results["ansible_facts"]["systemes"]["composants"])) + " : " + str(NnClient))

    def test_modify_system_add_clients(self):
        toChange2 = {}
        toChange2["spUrl"] = "http://localhost:18081"
        toChange2["spUsername"] = "admin"
        toChange2["spPassword"] = "admin"
        toChange2["spRealm"] = "master"
        toChange2["spConfigClient_id"] = "admin-cli" 
        toChange2["spConfigClient_secret"] = ""
        toChange2["spConfigUrl"] = "http://localhost:18182/config"
        toChange2["systemName"] = "test3"
        toChange2["systemShortName"] = "T3"
        toChange2["clients"] = [{"clientId": "clientsystem32"}]
        toChange2["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toChange2["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toChange2["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toChange2["clientRoles"] = [{"spClientRoleId": "test32", "spClientRoleName": "test32", "spClientRoleDescription": "test32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChange2["pilotRoles"] = [{"habilitationClientId": "habilitationClient4", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        toChange2["state"] = "present"
        toChange2["force"] = False

        results = system(toChange2)

        newToChange = {}
        newToChange["spUrl"] = "http://localhost:18081"
        newToChange["spUsername"] = "admin"
        newToChange["spPassword"] = "admin"
        newToChange["spRealm"] = "master"
        newToChange["spConfigClient_id"] = "admin-cli" 
        newToChange["spConfigClient_secret"] = ""
        newToChange["spConfigUrl"] = "http://localhost:18182/config"
        newToChange["systemName"] = "test3"
        newToChange["systemShortName"] = "T3"
        newToChange["clients"] = [{"clientId": "clientsystemChange32"}]
        newToChange["sadu_principal"] = "http://sadu_principal"
        newToChange["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        newToChange["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        newToChange["clientRoles"] = [{"spClientRoleId": "test32", "spClientRoleName": "test32", "spClientRoleDescription": "test32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        newToChange["pilotRoles"] = [{"habilitationClientId": "habilitationClient4", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        newToChange["state"] = "present"
        newToChange["force"] = False

        results = system(newToChange)
        print str(results)
        self.assertTrue(results['changed'])
        systemClients = results["ansible_facts"]["systemes"]["composants"]
        print str(systemClients)
        for toChangeClient in toChange2["clients"]:
            clientFound = False
            for systemClient in systemClients:
                if toChangeClient["clientId"] == systemClient["clientId"]:
                    clientFound = True
                    break
            self.assertTrue(clientFound, toChangeClient["clientId"] + " not found")
        for newToChangeClient in newToChange["clients"]:
            clientFound = False
            for systemClient in systemClients:
                if newToChangeClient["clientId"] == systemClient["clientId"]:
                    clientFound = True
                    break
            self.assertTrue(clientFound, newToChangeClient["clientId"] + " not found")
    
    def test_modify_system_habilitation_clients(self):
        createHabiliatationClient = {
                "clientId": "habilitationClient6",
                "name": "habilitationClient6",
                "roles": [{"name":"HPilot1","description": "HPilot1","composite": "False"},
                             {"name":"HPilot2","description": "HPilot2","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                             ]
                }
        toCreateClient = {}
        toCreateClient["auth_keycloak_url"] = "http://localhost:18081/auth"
        toCreateClient["auth_username"] = "admin"
        toCreateClient["auth_password"] = "admin"
        toCreateClient["realm"] = "master"
        toCreateClient["state"] = "present"
        toCreateClient["rootUrl"] = "http://test.com:18182"
        toCreateClient["description"] = "Ceci est un test"
        toCreateClient["adminUrl"] = "http://test.com:18182/admin"
        toCreateClient["enabled"] = True
        toCreateClient["clientAuthenticatorType"] = "client-secret"
        toCreateClient["redirectUris"] = ["http://test.com:18182/secure","http://test1.com:18182/secure"]
        toCreateClient["webOrigins"] = ["*"]
        toCreateClient["bearerOnly"] = False
        toCreateClient["publicClient"] = False
        toCreateClient["force"] = False
        toCreateClient["clientId"] = createHabiliatationClient["clientId"]
        toCreateClient["name"] = createHabiliatationClient["name"]
        toCreateClient["roles"] = createHabiliatationClient["roles"]
        
        self.module = keycloak_client
        set_module_args(toCreateClient)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()


        toCreate1 = {}
        toCreate1["spUrl"] = "http://localhost:18081"
        toCreate1["spUsername"] = "admin"
        toCreate1["spPassword"] = "admin"
        toCreate1["spRealm"] = "master"
        toCreate1["spConfigClient_id"] = "admin-cli" 
        toCreate1["spConfigClient_secret"] = ""
        toCreate1["spConfigUrl"] = "http://localhost:18182/config"
        toCreate1["systemName"] = "testH"
        toCreate1["systemShortName"] = "TH"
        toCreate1["clients"] = [{"clientId": "habilitationClient6"}]
        toCreate1["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toCreate1["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toCreate1["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toCreate1["clientRoles"] = [{"spClientRoleId": "HPilot1", "spClientRoleName": "HPilot1", "spClientRoleDescription": "HPilot1"}]
        NnClient=len(toCreate1["clientRoles"])+1
        toCreate1["pilotRoles"] = [{"habilitationClientId": "habilitationClient6", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        toCreate1["state"] = "present"
        toCreate1["force"] = False
        results = system(toCreate1)
        #print str(results)
        toCreate2 = {}
        toCreate2["spUrl"] = "http://localhost:18081"
        toCreate2["spUsername"] = "admin"
        toCreate2["spPassword"] = "admin"
        toCreate2["spRealm"] = "master"
        toCreate2["spConfigClient_id"] = "admin-cli" 
        toCreate2["spConfigClient_secret"] = ""
        toCreate2["spConfigUrl"] = "http://localhost:18182/config"
        toCreate2["systemName"] = "test3"
        toCreate2["systemShortName"] = "T3"
        toCreate2["clients"] = [{"clientId": "clientsystem11"}]
        toCreate2["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toCreate2["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toCreate2["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toCreate2["clientRoles"] = [{"spClientRoleId": "test32", "spClientRoleName": "test32", "spClientRoleDescription": "test32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toCreate2["pilotRoles"] = [{"habilitationClientId": "habilitationClient6", "roles": [{"name": "pilot-systemT3", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        toCreate2["state"] = "present"
        toCreate2["force"] = False
        results = system(toCreate2)
        #print str(results)
        NnClient=NnClient+1
        headers = loginAndSetHeaders(toCreate1["spUrl"], toCreate1["spRealm"], toCreate1["spUsername"], toCreate1["spPassword"], toCreate1["spConfigClient_id"], toCreate1["spConfigClient_secret"])
        getResponse = requests.get(toCreate1["spConfigUrl"]+"/systemes/"+toCreate1["systemShortName"], headers=headers)
        dataResponse = getResponse.json()
        print str(dataResponse["composants"][0]["roles"])
        self.assertEquals(len(dataResponse["composants"][0]["roles"]),NnClient,str(len(dataResponse["composants"][0]["roles"])) + " : " + str(NnClient))
        results = system(toCreate1)
        print str(results)
        headers = loginAndSetHeaders(toCreate1["spUrl"], toCreate1["spRealm"], toCreate1["spUsername"], toCreate1["spPassword"], toCreate1["spConfigClient_id"], toCreate1["spConfigClient_secret"])
        getResponse = requests.get(toCreate1["spConfigUrl"]+"/systemes/"+toCreate1["systemShortName"], headers=headers)
        dataResponse = getResponse.json()
        print str(dataResponse["composants"][0]["roles"])
        self.assertEquals(len(dataResponse["composants"][0]["roles"]),NnClient,str(len(dataResponse["composants"][0]["roles"])) + " : " + str(NnClient))


    def test_create_system_no_sadu(self):
        toCreate = {}
        toCreate["spUrl"] = "http://localhost:18081"
        toCreate["spUsername"] = "admin"
        toCreate["spPassword"] = "admin"
        toCreate["spRealm"] = "master"
        toCreate["spConfigClient_id"] = "admin-cli" 
        toCreate["spConfigClient_secret"] = ""
        toCreate["spConfigUrl"] = "http://localhost:18182/config"
        toCreate["systemName"] = "systemNS1"
        toCreate["systemShortName"] = "NS1"
        toCreate["clients"] = [{"clientId": "clientsystemNS1"}]
        toCreate["clientRoles"] = [{"spClientRoleId": "testNS1", "spClientRoleName": "testNS1", "spClientRoleDescription": "testNS1"},{"spClientRoleId": "toCreate", "spClientRoleName": "toCreate", "spClientRoleDescription": "toCreate"}]
        toCreate["state"] = "present"
        toCreate["force"] = False
    
        results = system(toCreate)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["systemes"]["nom"], toCreate["systemName"], "systemName: " + results["ansible_facts"]["systemes"]["nom"] + " : " + toCreate["systemName"])

    def test_system_no_sadu_not_changed(self):
        toDoNotChange = {}
        toDoNotChange["spUrl"] = "http://localhost:18081"
        toDoNotChange["spUsername"] = "admin"
        toDoNotChange["spPassword"] = "admin"
        toDoNotChange["spRealm"] = "master"
        toDoNotChange["spConfigClient_id"] = "admin-cli" 
        toDoNotChange["spConfigClient_secret"] = ""
        toDoNotChange["spConfigUrl"] = "http://localhost:18182/config"
        toDoNotChange["systemName"] = "systemNS2"
        toDoNotChange["systemShortName"] = "SNS2"
        toDoNotChange["clients"] = [{"clientId": "clientsystemNS21"}]
        toDoNotChange["clientRoles"] = [{"spClientRoleId": "testNS2", "spClientRoleName": "testNS2", "spClientRoleDescription": "testNS2"},{"spClientRoleId": "toDoNotChange", "spClientRoleName": "toDoNotChange", "spClientRoleDescription": "toDoNotChange"}]
        toDoNotChange["state"] = "present"
        toDoNotChange["force"] = False

        system(toDoNotChange)
        #print str(results)
        results = system(toDoNotChange)
        #print str(results)
        self.assertFalse(results['changed'])

    def test_modify_system_no_sadu(self):
        toChange = {}
        toChange["spUrl"] = "http://localhost:18081"
        toChange["spUsername"] = "admin"
        toChange["spPassword"] = "admin"
        toChange["spRealm"] = "master"
        toChange["spConfigClient_id"] = "admin-cli" 
        toChange["spConfigClient_secret"] = ""
        toChange["spConfigUrl"] = "http://localhost:18182/config"
        toChange["systemName"] = "systemNS3"
        toChange["systemShortName"] = "SNS3"
        toChange["clients"] = [{"clientId": "clientsystemNS31"}]
        toChange["clientRoles"] = [{"spClientRoleId": "testNS31", "spClientRoleName": "testNS31", "spClientRoleDescription": "testNS31"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChange["state"] = "present"
        toChange["force"] = False

        results = system(toChange)
        #print str(results)
        toChange["clients"] = [{"clientId": "clientsystemChangeNS31"}]
        NnClient=len(toChange["clients"])+1
        results = system(toChange)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEquals(len(results["ansible_facts"]["systemes"]["composants"]), 
                          NnClient, 
                          str(len(results["ansible_facts"]["systemes"]["composants"])) + " : " + str(NnClient))

    def test_modify_system_no_sadu_add_clients(self):
        toChange = {}
        toChange["spUrl"] = "http://localhost:18081"
        toChange["spUsername"] = "admin"
        toChange["spPassword"] = "admin"
        toChange["spRealm"] = "master"
        toChange["spConfigClient_id"] = "admin-cli" 
        toChange["spConfigClient_secret"] = ""
        toChange["spConfigUrl"] = "http://localhost:18182/config"
        toChange["systemName"] = "testNS3"
        toChange["systemShortName"] = "TNS3"
        toChange["clients"] = [{"clientId": "clientsystemNS32"}]
        toChange["clientRoles"] = [{"spClientRoleId": "testNS32", "spClientRoleName": "testNS32", "spClientRoleDescription": "testNS32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChange["state"] = "present"
        toChange["force"] = False

        results = system(toChange)

        newToChange = {}
        newToChange["spUrl"] = "http://localhost:18081"
        newToChange["spUsername"] = "admin"
        newToChange["spPassword"] = "admin"
        newToChange["spRealm"] = "master"
        newToChange["spConfigClient_id"] = "admin-cli" 
        newToChange["spConfigClient_secret"] = ""
        newToChange["spConfigUrl"] = "http://localhost:18182/config"
        newToChange["systemName"] = "testNS3"
        newToChange["systemShortName"] = "TNS3"
        newToChange["clients"] = [{"clientId": "clientsystemChangeNS32"}]
        newToChange["clientRoles"] = [{"spClientRoleId": "testNS32", "spClientRoleName": "testNS32", "spClientRoleDescription": "testNS32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        newToChange["state"] = "present"
        newToChange["force"] = False

        results = system(newToChange)
        print str(results)
        self.assertTrue(results['changed'])
        systemClients = results["ansible_facts"]["systemes"]["composants"]
        print str(systemClients)
        for toChangeClient in toChange["clients"]:
            clientFound = False
            for systemClient in systemClients:
                if toChangeClient["clientId"] == systemClient["clientId"]:
                    clientFound = True
                    break
            self.assertTrue(clientFound, toChangeClient["clientId"] + " not found")
        for newToChangeClient in newToChange["clients"]:
            clientFound = False
            for systemClient in systemClients:
                if newToChangeClient["clientId"] == systemClient["clientId"]:
                    clientFound = True
                    break
            self.assertTrue(clientFound, newToChangeClient["clientId"] + " not found")
    def test_delete_system(self):
        toDelete = {}
        toDelete["spUrl"] = "http://localhost:18081"
        toDelete["spUsername"] = "admin"
        toDelete["spPassword"] = "admin"
        toDelete["spRealm"] = "master"
        toDelete["spConfigClient_id"] = "admin-cli" 
        toDelete["spConfigClient_secret"] = ""
        toDelete["spConfigUrl"] = "http://localhost:18182/config"
        toDelete["systemName"] = "system4"
        toDelete["systemShortName"] = "S4"
        toDelete["clients"] = [{"clientId": "clientsystem41"}]
        toDelete["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toDelete["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toDelete["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toDelete["clientRoles"] = [{"spClientRoleId": "test4", "spClientRoleName": "test4", "spClientRoleDescription": "test4"},{"spClientRoleId": "toDelete", "spClientRoleName": "toDelete", "spClientRoleDescription": "toDelete"}]
        toDelete["pilotRoles"] = [{"habilitationClientId": "habilitationClient5", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "absent"}]}]
        toDelete["state"] = "present"
        toDelete["force"] = False

        system(toDelete)
        toDelete["state"] = "absent"
        results = system(toDelete)
        #print str(results)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'system has been deleted')