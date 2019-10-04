from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args
from ansible.modules.identity.keycloak import keycloak_user, keycloak_role, keycloak_client
from ansible.modules.identity.sx5 import sx5_habilitation
from ansible.module_utils.keycloak import KeycloakAPI, keycloak_argument_spec, isDictEquals
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.sx5_sp_config_system_utils import loginAndSetHeaders
from ansible.module_utils.urls import open_url
from ansible.modules.identity.sx5.sx5_sp_config_system import system
from ansible.module_utils.six.moves.urllib.error import HTTPError

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
    systemsToCreate = [
        {
            "spUrl": "http://localhost:18081",
            "spUsername": "admin",
            "spPassword": "admin",
            "spRealm": "master",
            "spConfigClient_id": "admin-cli", 
            "spConfigClient_secret": "",
            "spConfigUrl": "http://localhost:18182/config",
            "systemName": "system1",
            "systemShortName": "S1",
            "clients": [{"clientId": "clientsystem11"}],
            "clientRoles": [{"spClientRoleId": "test1", "spClientRoleName": "test1", "spClientRoleDescription": "test1"},{"spClientRoleId": "toCreate", "spClientRoleName": "toCreate", "spClientRoleDescription": "toCreate"}],
            "state": "present",
            "force": False
        },
        {
            "spUrl": "http://localhost:18081",
            "spUsername": "admin",
            "spPassword": "admin",
            "spRealm": "master",
            "spConfigClient_id": "admin-cli", 
            "spConfigClient_secret": "",
            "spConfigUrl": "http://localhost:18182/config",
            "systemName": "system2",
            "systemShortName": "S3",
            "clients": [{"clientId": "clientsystem21"}],
            "clientRoles": [{"spClientRoleId": "test2", "spClientRoleName": "test2", "spClientRoleDescription": "test2"},{"spClientRoleId": "toremoveChange", "spClientRoleName": "toremoveChange", "spClientRoleDescription": "toremoveChange"}],
            "state": "present",
            "force": False
        }    
    ]
    habilitationsEchus = [
        {
            "username": "user1",
            "clientRoles": [{"clientId": "clientsystem11","roles": ["test1"]}],
            "dateEcheance": "2019-01-01",
            "spConfigUrl": "http://localhost:18182/config"
        },
        {
            "username": "user4",
            "clientRoles": [{"clientId": "clientsystem21","roles": ["test2"]}],
            "dateEcheance": "2019-02-01",
            "spConfigUrl": "http://localhost:18182/config"
        }
    ]
    userIndex = {}
    clientIndex = {}
    expiredHabilitationsIndex = []
    
    def setUp(self):
        super(Sx5HabilitationTestCase, self).setUp()
        self.userIndex = {}
        self.clientIndex = {}
        self.expiredHabilitationsIndex = []
        toCreateClient = self.clientTemplate.copy()
        self.module = keycloak_client
        for theClient in self.clientsToCreate:
            toCreateClient["clientId"] = theClient["clientId"]
            toCreateClient["name"] = theClient["name"]
            toCreateClient["roles"] = theClient["roles"]
            set_module_args(toCreateClient)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
            self.clientIndex[theClient["clientId"]] = results.exception.args[0]["end_state"]["id"]
        self.module = keycloak_user
        for theUser in self.testUsers:
            createdUser = {}
            set_module_args(theUser)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
            createdUser["id"] = results.exception.args[0]["user"]["id"]
            # Obtenir ses roles de realm
            headers = loginAndSetHeaders("http://localhost:18081", theUser["realm"], theUser["auth_username"], theUser["auth_password"], "admin-cli", "")
            roleMappingsUrl = theUser["auth_keycloak_url"]+"/admin/realms/"+theUser["realm"]+"/users/"+results.exception.args[0]["user"]["id"]+"/role-mappings"
            roleMappings=json.load(open_url(roleMappingsUrl,headers=headers,method='GET'))
            createdUser["roles"] = roleMappings
            self.userIndex[theUser["username"]] = createdUser
        for systemToCreate in self.systemsToCreate:
            system(systemToCreate)
        for habilitation in self.habilitationsEchus:
            userId = self.userIndex[habilitation["username"]]["id"]
            listeDesRoles = []
            if "realmRoles" in habilitation:
                for roleToExpire in habilitation["realmRoles"]:
                    for userRole in self.userIndex[habilitation["username"]]["roles"]["realmMappings"]:
                        if userRole["name"] == roleToExpire:
                            listeDesRoles.append(userRole["id"])
            if "clientRoles" in habilitation:
                for client in habilitation["clientRoles"]:
                    for roleToExpire in client["roles"]:
                        if client["clientId"] in self.userIndex[habilitation["username"]]["roles"]["clientMappings"]:
                            for userRole in self.userIndex[habilitation["username"]]["roles"]["clientMappings"][client["clientId"]]["mappings"]:
                                if userRole["name"] == roleToExpire:
                                    listeDesRoles.append(userRole["id"])
            dateEcheance = habilitation["dateEcheance"]
            for roleToExpire in listeDesRoles:
                newHabilitation={"idUtilisateur": userId,"idRole": roleToExpire,"dateEcheance": dateEcheance}
                try:
                    open_url(habilitation["spConfigUrl"]+"/habilitations/",headers=headers,data=json.dumps(newHabilitation),method='POST')
                    self.expiredHabilitationsIndex.append(newHabilitation)
                except Exception as e:
                    print(str(e))
    
            
    def tearDown(self):
        toCreateClient = self.clientTemplate.copy()
        for expiredHabilitation in self.expiredHabilitationsIndex:
            try:
                headers = loginAndSetHeaders("http://localhost:18081", "master", "admin", "admin", "admin-cli", "")
                url = "http://localhost:18182/config/habilitations/utilisateurs/"+expiredHabilitation["idUtilisateur"]+"/roles/"+expiredHabilitation["idRole"]
                open_url(
                    url=url,
                    headers=headers,
                    method='DELETE')
            except HTTPError as e:
                if e.code != 404:
                    print(str(e))
            except Exception as e:
                print(str(e))
            
        for systemToCreate in self.systemsToCreate:
            systemToDelete = systemToCreate.copy()
            systemToDelete["state"] = "absent"
            system(systemToCreate)
        self.module = keycloak_user
        for theUser in self.testUsers:
            userToDelete = theUser.copy()
            userToDelete["state"] = "absent"
            set_module_args(userToDelete)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
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
        toList = {}
        toList["auth_keycloak_url"] = "http://localhost:18081/auth"
        toList["auth_username"] = "admin"
        toList["auth_password"] = "admin"
        toList["realm"] = "master"
        toList["spConfigUrl"] = "http://localhost:18182/config"
        toList["spConfigClient_id"] = "admin-cli"
        toList["spConfigClient_secret"] = ""
        toList["operation"] = "list"
        self.module = sx5_habilitation
        set_module_args(toList)
        with self.assertRaises(AnsibleExitJson) as results1:
            self.module.main()
        self.assertEqual(results1.exception.args[0]["habilitation"]["ExpiredHabilitations"],self.expiredHabilitationsIndex,"operation = list : mismatch ExpiredHabilitations")

    def test_operation_remove(self):
        toRemove = {}
        toRemove["auth_keycloak_url"] = "http://localhost:18081/auth"
        toRemove["auth_username"] = "admin"
        toRemove["auth_password"] = "admin"
        toRemove["realm"] = "master"
        toRemove["spConfigUrl"] = "http://localhost:18182/config"
        toRemove["spConfigClient_id"] = "admin-cli"
        toRemove["spConfigClient_secret"] = ""
        toRemove["operation"] = "remove"
        self.module = sx5_habilitation
        set_module_args(toRemove)
        with self.assertRaises(AnsibleExitJson) as results1:
            self.module.main()
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitations"],self.expiredHabilitationsIndex,"operation = list : mismatch deleteExpiredHabilitations")
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitationsInKc"],self.expiredHabilitationsIndex,"operation = list : mismatch deleteExpiredHabilitationsInKc")

    def test_operation_remove_with_deleted_user(self):
        userToDelete = self.testUsers[0].copy()
        userToDelete["state"] = "absent"
        self.module = keycloak_user
        set_module_args(userToDelete)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        toRemove = {}
        toRemove["auth_keycloak_url"] = "http://localhost:18081/auth"
        toRemove["auth_username"] = "admin"
        toRemove["auth_password"] = "admin"
        toRemove["realm"] = "master"
        toRemove["spConfigUrl"] = "http://localhost:18182/config"
        toRemove["spConfigClient_id"] = "admin-cli"
        toRemove["spConfigClient_secret"] = ""
        toRemove["operation"] = "remove"
        self.module = sx5_habilitation
        set_module_args(toRemove)
        with self.assertRaises(AnsibleExitJson) as results1:
            self.module.main()
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitations"],self.expiredHabilitationsIndex,"operation = remove : mismatch deleteExpiredHabilitations")
        deleteExpiredHabilitationsInKc = []
        deleteExpiredHabilitationsInKc.append(self.expiredHabilitationsIndex[1])
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitationsInKc"],deleteExpiredHabilitationsInKc,"operation = remove : mismatch deleteExpiredHabilitationsInKc")

    def test_operation_remove_with_deleted_user_client_role(self):
        userToUpdate = self.testUsers[0].copy()
        userToUpdate["clientRoles"] = [{"clientId": "clientsystem11","roles": []}]
        self.module = keycloak_user
        set_module_args(userToUpdate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        toRemove = {}
        toRemove["auth_keycloak_url"] = "http://localhost:18081/auth"
        toRemove["auth_username"] = "admin"
        toRemove["auth_password"] = "admin"
        toRemove["realm"] = "master"
        toRemove["spConfigUrl"] = "http://localhost:18182/config"
        toRemove["spConfigClient_id"] = "admin-cli"
        toRemove["spConfigClient_secret"] = ""
        toRemove["operation"] = "remove"
        self.module = sx5_habilitation
        set_module_args(toRemove)
        with self.assertRaises(AnsibleExitJson) as results1:
            self.module.main()
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitations"],self.expiredHabilitationsIndex,"operation = list : mismatch deleteExpiredHabilitations")
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitationsInKc"],self.expiredHabilitationsIndex,"operation = list : mismatch deleteExpiredHabilitationsInKc")

    def test_operation_remove_with_deleted_client(self):
        clientToDelete = self.clientsToCreate[0].copy()
        for key in self.clientTemplate.keys():
            clientToDelete[key] = self.clientTemplate[key]
        clientToDelete["state"] = "absent"
        self.module = keycloak_client
        set_module_args(clientToDelete)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        toRemove = {}
        toRemove["auth_keycloak_url"] = "http://localhost:18081/auth"
        toRemove["auth_username"] = "admin"
        toRemove["auth_password"] = "admin"
        toRemove["realm"] = "master"
        toRemove["spConfigUrl"] = "http://localhost:18182/config"
        toRemove["spConfigClient_id"] = "admin-cli"
        toRemove["spConfigClient_secret"] = ""
        toRemove["operation"] = "remove"
        self.module = sx5_habilitation
        set_module_args(toRemove)
        with self.assertRaises(AnsibleExitJson) as results1:
            self.module.main()
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitations"],self.expiredHabilitationsIndex,"operation = remove : mismatch deleteExpiredHabilitations")
        deleteExpiredHabilitationsInKc = []
        deleteExpiredHabilitationsInKc.append(self.expiredHabilitationsIndex[1])
        self.assertEqual(results1.exception.args[0]["habilitation"]["deleteExpiredHabilitationsInKc"],deleteExpiredHabilitationsInKc,"operation = remove : mismatch deleteExpiredHabilitationsInKc")

    def test_operation_expend(self):
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

        #toList = {}
        #toList["auth_keycloak_url"] = "http://localhost:18081/auth"
        #toList["auth_username"] = "admin"
        #toList["auth_password"] = "admin"
        #toList["realm"] = "master"
        #toList["spConfigUrl"] = "http://localhost:18182/config"
        #toList["spConfigClient_id"] = "admin-cli"
        #toList["spConfigClient_secret"] = ""
        #toList["operation"] = "list"
        ExpiredHabilitations = []
        for habilitation in self.expiredHabilitationsIndex:
            hab = {}
            newdate_extension = datetime.datetime.strptime(habilitation["dateEcheance"], '%Y-%m-%d')
            newdate_extension = newdate_extension + datetime.timedelta(days=toExpend["duration"])
            hab["dateEcheance"] = datetime.datetime.strftime(newdate_extension, '%Y-%m-%d')
            hab["idUtilisateur"] = habilitation["idUtilisateur"]  
            hab["idRole"] = habilitation["idRole"]
            ExpiredHabilitations.append(hab)
        self.module = sx5_habilitation
        set_module_args(toExpend)
        with self.assertRaises(AnsibleExitJson) as results2:
            self.module.main()
        #print results2.exception.args[0]
        self.assertNotEqual(results2.exception.args[0]["habilitation"]["extExpiredHabilitations"],self.expiredHabilitationsIndex,"operation = extend : ExpiredHabilitations not extended")
        self.assertEqual(results2.exception.args[0]["habilitation"]["extExpiredHabilitations"],ExpiredHabilitations,"operation = extend : mismatch extend ExpiredHabilitations")

        #toListAfter = toList
        #self.module = sx5_habilitation
        #set_module_args(toListAfter)
        #with self.assertRaises(AnsibleExitJson) as results3:
        #    self.module.main()
        #print results3.exception.args[0]
        #self.assertNotEqual(results3.exception.args[0]["habilitation"]["extExpiredHabilitations"],results2.exception.args[0]["habilitation"]["extExpiredHabilitations"],"operation = extend : mismatch ExpiredHabilitations")
        #self.assertEqual(results3.exception.args[0]["habilitation"]["ExpiredHabilitations"],[],"operation = extend : mismatch ExpiredHabilitations")
        
