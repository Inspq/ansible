from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args
from units.compat.mock import patch
from ansible.modules.identity.keycloak import keycloak_user, keycloak_role, keycloak_client
from ansible.modules.identity.sx5 import sx5_habilitation
from ansible.module_utils.keycloak import KeycloakAPI, keycloak_argument_spec, isDictEquals
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.sx5_sp_config_system_utils import loginAndSetHeaders
from ansible.module_utils.urls import open_url
from ansible.modules.identity.sx5.sx5_sp_config_system import system
import json
import datetime

class Sx5HabilitationTestCase(ModuleTestCase):
    testUsers = [
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "username": "user1",
            "firstName": "user1",
            "lastName": "User",
            "email": "user1@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}], 
            "clientRoles": [{"clientId": "clientsystem11","roles": ["test1"]}],
            "realmRoles": ["create-realm","uma_authorization"],
            "state":"present",
            "force":"no"
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "username": "user2",
            "firstName": "user2",
            "lastName": "User",
            "email": "user2@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "clientRoles": [{"clientId": "clientsystem11","roles": ["test1"]}],
            "realmRoles": ["create-realm","uma_authorization"],
            "state": "present",
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "username": "user3",
            "firstName": "user3",
            "lastName": "User",
            "email": "user3@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "clientRoles": [{"clientId": "clientsystem11","roles": ["test1"]}],
            "realmRoles": ["create-realm","uma_authorization"],
            "state":"present",
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "username": "user4",
            "firstName": "user4",
            "lastName": "User",
            "email": "user4@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "clientRoles": [{"clientId": "clientsystem21","roles": ["test2"]}],
            "realmRoles": ["create-realm","uma_authorization"],
            "state":"present",
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "username": "user5",
            "firstName": "user5",
            "lastName": "User",
            "email": "user5@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}],
            "clientRoles": [{"clientId": "clientsystem21","roles": ["test2"]}],
            "realmRoles": ["create-realm","uma_authorization"],
            "state":"present",
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "username": "user6",
            "firstName": "user6",
            "lastName": "User",
            "email": "user6@user.ca",
            "enabled": True,
            "emailVerified": False,
            "credentials": [{"temporary": 'false',"type": "password","value": "password"}], 
            "clientRoles": [{"clientId": "clientsystem21","roles": ["test2"]}],
            "realmRoles": ["create-realm","uma_authorization"],
            "state":"present",
            "force":"no"
        }                
    ]
    clientTemplate = {
        "auth_keycloak_url": "http://localhost:18081/auth",
        "auth_username": "admin",
        "auth_password": "admin",
        "realm": "master",
        "state": "present",
        "rootUrl": "http://test.com:18182",
        "description": "Ceci est un test",
        "adminUrl": "http://test.com:18182/admin",
        "enabled": True,
        "clientAuthenticatorType": "client-secret",
        "redirectUris": ["http://test.com:18182/secure","http://test1.com:18182/secure"],
        "webOrigins": ["*"],
        "bearerOnly": False,
        "publicClient": False,
        "force": False
        }
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
                         {"name":"toremoveChange","description": "toremoveChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            }
    ]
    def setUp(self):
        super(Sx5HabilitationTestCase, self).setUp()
        toCreateClient = self.clientTemplate.copy()
        self.module = keycloak_client
        for theClient in self.clientsToCreate:
            toCreateClient["clientId"] = theClient["clientId"]
            toCreateClient["name"] = theClient["name"]
            toCreateClient["roles"] = theClient["roles"]
            set_module_args(toCreateClient)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
    def tearDown(self):
        toCreateClient = self.clientTemplate.copy()
        self.module = keycloak_client
        for theClient in self.clientsToCreate:
            toCreateClient["clientId"] = theClient["clientId"]
            toCreateClient["name"] = theClient["name"]
            toCreateClient["roles"] = theClient["roles"]
            toCreateClient["state"] = "absent"
            set_module_args(toCreateClient)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
        super(Sx5HabilitationTestCase, self).tearDown()           
 
    def test_operation_list(self):
        
        toCreateSystem = {}
        toCreateSystem["spUrl"] = "http://localhost:18081"
        toCreateSystem["spUsername"] = "admin"
        toCreateSystem["spPassword"] = "admin"
        toCreateSystem["spRealm"] = "master"
        toCreateSystem["spConfigClient_id"] = "admin-cli" 
        toCreateSystem["spConfigClient_secret"] = ""
        toCreateSystem["spConfigUrl"] = "http://localhost:18182/config"
        toCreateSystem["systemName"] = "system1"
        toCreateSystem["systemShortName"] = "S1"
        toCreateSystem["clients"] = [{"clientId": "clientsystem11"}]
        toCreateSystem["clientRoles"] = [{"spClientRoleId": "test1", "spClientRoleName": "test1", "spClientRoleDescription": "test1"},{"spClientRoleId": "toCreate", "spClientRoleName": "toCreate", "spClientRoleDescription": "toCreate"}]
        toCreateSystem["state"] = "present"
        toCreateSystem["force"] = False
        system(toCreateSystem)

        toList = {}
        toList["auth_keycloak_url"] = "http://localhost:18081/auth"
        toList["auth_username"] = "admin"
        toList["auth_password"] = "admin"
        toList["realm"] = "master"
        toList["spConfigUrl"] = "http://localhost:18182/config"
        toList["spConfigClient_id"] = "admin-cli"
        toList["spConfigClient_secret"] = ""
        toList["operation"] = "list"
        headers = loginAndSetHeaders("http://localhost:18081", toList["realm"], toList["auth_username"], toList["auth_password"], toList["spConfigClient_id"], toList["spConfigClient_secret"])
        ExpiredHabilitations = []
        self.module = keycloak_user
        for theUser in self.testUsers:
            set_module_args(theUser)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
            #print results.exception.args[0]["user"]["clientRoles"]
            newdate_echeance = datetime.date.today().strftime('%Y-%m-%d')
            for roles in results.exception.args[0]["user"]["clientRoles"]:
                for role in roles["roles"]:
                    newHabilitation={"idUtilisateur": results.exception.args[0]["user"]["id"],"idRole": role["id"],"dateEcheance": newdate_echeance}
                    getSysteme = open_url(toList["spConfigUrl"]+"/systemes/"+toCreateSystem["systemShortName"],headers=headers,method='GET')
                    exitSysteme = getSysteme.read()
                    exitSysteme = json.loads(exitSysteme)
                    for c in exitSysteme["composants"]:
                        for r in c["roles"]:
                            if r["uuidRoleKeycloak"] == role["id"]:
                                postResponse = open_url(toList["spConfigUrl"]+"/habilitations/",headers=headers,data=json.dumps(newHabilitation),method='POST')
                                print postResponse.read()
                                ExpiredHabilitations.append(newHabilitation)

        self.module = sx5_habilitation
        set_module_args(toList)
        with self.assertRaises(AnsibleExitJson) as results1:
            self.module.main()
        self.assertEqual(results1.exception.args[0]["habilitation"]["ExpiredHabilitations"],ExpiredHabilitations,"operation = list : mismatch ExpiredHabilitations")

    def test_operation_remove(self):
        toCreateSystem = {}
        toCreateSystem["spUrl"] = "http://localhost:18081"
        toCreateSystem["spUsername"] = "admin"
        toCreateSystem["spPassword"] = "admin"
        toCreateSystem["spRealm"] = "master"
        toCreateSystem["spConfigClient_id"] = "admin-cli" 
        toCreateSystem["spConfigClient_secret"] = ""
        toCreateSystem["spConfigUrl"] = "http://localhost:18182/config"
        toCreateSystem["systemName"] = "system2"
        toCreateSystem["systemShortName"] = "S2"
        toCreateSystem["clients"] = [{"clientId": "clientsystem21"}]
        toCreateSystem["clientRoles"] = [{"spClientRoleId": "test2", "spClientRoleName": "test2", "spClientRoleDescription": "test2"},{"spClientRoleId": "toremoveChange", "spClientRoleName": "toremoveChange", "spClientRoleDescription": "toremoveChange"}]
        toCreateSystem["state"] = "present"
        toCreateSystem["force"] = False
        system(toCreateSystem)

        toRemove = {}
        toRemove["auth_keycloak_url"] = "http://localhost:18081/auth"
        toRemove["auth_username"] = "admin"
        toRemove["auth_password"] = "admin"
        toRemove["realm"] = "master"
        toRemove["spConfigUrl"] = "http://localhost:18182/config"
        toRemove["spConfigClient_id"] = "admin-cli"
        toRemove["spConfigClient_secret"] = ""
        toRemove["operation"] = "remove"
        headers = loginAndSetHeaders("http://localhost:18081", toRemove["realm"], toRemove["auth_username"], toRemove["auth_password"], toRemove["spConfigClient_id"], toRemove["spConfigClient_secret"])
        ExpiredHabilitations = []
        self.module = keycloak_user
        for theUser in self.testUsers:
            set_module_args(theUser)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
            #print results.exception.args[0]["user"]["clientRoles"]
            newdate_echeance = datetime.date.today().strftime('%Y-%m-%d')
            for roles in results.exception.args[0]["user"]["clientRoles"]:
                for role in roles["roles"]:
                    newHabilitation={"idUtilisateur": results.exception.args[0]["user"]["id"],"idRole": role["id"],"dateEcheance": newdate_echeance}
                    getSysteme = open_url(toRemove["spConfigUrl"]+"/systemes/"+toCreateSystem["systemShortName"],headers=headers,method='GET')
                    exitSysteme = getSysteme.read()

                    exitSysteme = json.loads(exitSysteme)
                    for c in exitSysteme["composants"]:
                        for r in c["roles"]:
                            if r["uuidRoleKeycloak"] == role["id"]:
                                postResponse = open_url(toRemove["spConfigUrl"]+"/habilitations/",headers=headers,data=json.dumps(newHabilitation),method='POST')
                                print postResponse.read()
                                ExpiredHabilitations.append(newHabilitation)
        self.module = sx5_habilitation
        set_module_args(toRemove)
        with self.assertRaises(AnsibleExitJson) as results1:
            self.module.main()
        #print results1.exception.args[0]["msg"]
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitations"],ExpiredHabilitations,"operation = list : mismatch deleteExpiredHabilitations")
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitationsInKc"],ExpiredHabilitations,"operation = list : mismatch deleteExpiredHabilitationsInKc")

    def test_operation_expend(self):
        toCreateSystem = {}
        toCreateSystem["spUrl"] = "http://localhost:18081"
        toCreateSystem["spUsername"] = "admin"
        toCreateSystem["spPassword"] = "admin"
        toCreateSystem["spRealm"] = "master"
        toCreateSystem["spConfigClient_id"] = "admin-cli" 
        toCreateSystem["spConfigClient_secret"] = ""
        toCreateSystem["spConfigUrl"] = "http://localhost:18182/config"
        toCreateSystem["systemName"] = "system1"
        toCreateSystem["systemShortName"] = "S1"
        toCreateSystem["clients"] = [{"clientId": "clientsystem11"}]
        toCreateSystem["clientRoles"] = [{"spClientRoleId": "test1", "spClientRoleName": "test1", "spClientRoleDescription": "test1"},{"spClientRoleId": "toCreate", "spClientRoleName": "toCreate", "spClientRoleDescription": "toCreate"}]
        toCreateSystem["state"] = "present"
        toCreateSystem["force"] = False
        system(toCreateSystem)
        toCreateSystem = {}
        toCreateSystem["spUrl"] = "http://localhost:18081"
        toCreateSystem["spUsername"] = "admin"
        toCreateSystem["spPassword"] = "admin"
        toCreateSystem["spRealm"] = "master"
        toCreateSystem["spConfigClient_id"] = "admin-cli" 
        toCreateSystem["spConfigClient_secret"] = ""
        toCreateSystem["spConfigUrl"] = "http://localhost:18182/config"
        toCreateSystem["systemName"] = "system2"
        toCreateSystem["systemShortName"] = "S2"
        toCreateSystem["clients"] = [{"clientId": "clientsystem21"}]
        toCreateSystem["clientRoles"] = [{"spClientRoleId": "test2", "spClientRoleName": "test2", "spClientRoleDescription": "test2"},{"spClientRoleId": "toremoveChange", "spClientRoleName": "toremoveChange", "spClientRoleDescription": "toremoveChange"}]
        toCreateSystem["state"] = "present"
        toCreateSystem["force"] = False
        system(toCreateSystem)
        
        toExpend = {}
        toExpend["auth_keycloak_url"] = "http://localhost:18081/auth"
        toExpend["auth_username"] = "admin"
        toExpend["auth_password"] = "admin"
        toExpend["realm"] = "master"
        toExpend["spConfigUrl"] = "http://localhost:18182/config"
        toExpend["spConfigClient_id"] = "admin-cli"
        toExpend["spConfigClient_secret"] = ""
        toExpend["operation"] = "extend"
        toExpend["duration"] = 1

        toList = {}
        toList["auth_keycloak_url"] = "http://localhost:18081/auth"
        toList["auth_username"] = "admin"
        toList["auth_password"] = "admin"
        toList["realm"] = "master"
        toList["spConfigUrl"] = "http://localhost:18182/config"
        toList["spConfigClient_id"] = "admin-cli"
        toList["spConfigClient_secret"] = ""
        toList["operation"] = "list"
        headers = loginAndSetHeaders("http://localhost:18081", toExpend["realm"], toExpend["auth_username"], toExpend["auth_password"], toExpend["spConfigClient_id"], toExpend["spConfigClient_secret"])
        ExpiredHabilitations = []
        self.module = keycloak_user
        for theUser in self.testUsers:
            set_module_args(theUser)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
            #print results.exception.args[0]["user"]["clientRoles"]
            newdate_echeance = datetime.date.today().strftime('%Y-%m-%d')
            for roles in results.exception.args[0]["user"]["clientRoles"]:
                for role in roles["roles"]:
                    newHabilitation={"idUtilisateur": results.exception.args[0]["user"]["id"],"idRole": role["id"],"dateEcheance": newdate_echeance}
                    getSysteme = open_url(toExpend["spConfigUrl"]+"/systemes/"+toCreateSystem["systemShortName"],headers=headers,method='GET')
                    exitSysteme = getSysteme.read()
                    exitSysteme = json.loads(exitSysteme)
                    for c in exitSysteme["composants"]:
                        for r in c["roles"]:
                            if r["uuidRoleKeycloak"] == role["id"]:
                                postResponse = open_url(toExpend["spConfigUrl"]+"/habilitations/",headers=headers,data=json.dumps(newHabilitation),method='POST')
                                #print postResponse.read()
                                ExpiredHabilitations.append(newHabilitation)
        
        toListBifor = toList
        self.module = sx5_habilitation
        set_module_args(toListBifor)
        with self.assertRaises(AnsibleExitJson) as results1:
            self.module.main()
        #print results1.exception.args[0]
        self.assertEqual(results1.exception.args[0]["habilitation"]["ExpiredHabilitations"],ExpiredHabilitations,"operation = list : mismatch ExpiredHabilitations")

        self.module = sx5_habilitation
        set_module_args(toExpend)
        with self.assertRaises(AnsibleExitJson) as results2:
            self.module.main()
        #print results2.exception.args[0]
        self.assertNotEqual(results2.exception.args[0]["habilitation"]["extExpiredHabilitations"],ExpiredHabilitations,"operation = extend : mismatch extend ExpiredHabilitations")

        toListAfter = toList
        self.module = sx5_habilitation
        set_module_args(toListAfter)
        with self.assertRaises(AnsibleExitJson) as results3:
            self.module.main()
        #print results3.exception.args[0]
        self.assertNotEqual(results3.exception.args[0]["habilitation"]["extExpiredHabilitations"],results2.exception.args[0]["habilitation"]["extExpiredHabilitations"],"operation = extend : mismatch ExpiredHabilitations")
        self.assertEqual(results3.exception.args[0]["habilitation"]["ExpiredHabilitations"],[],"operation = extend : mismatch ExpiredHabilitations")
        
