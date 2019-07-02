from ansible.modules.identity.keycloak import keycloak_user, keycloak_group, keycloak_role
from ansible.modules.identity.sx5 import sx5_habilitation
from ansible.module_utils.keycloak import isDictEquals
from units.modules.utils import ModuleTestCase
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
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1","testUserRole2"],
            "state":"absent",
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
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1","testUserRole2"],
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
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1","testUserRole2"],
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
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1"],
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
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["uma_authorization","offline_access"],
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
            "clientRoles": [{"clientId": "master-realm","roles": ["manage-clients"]}],
            "realmRoles": ["testUserRole1","testUserRole2"],
            "state":"absent",
            "force":"no"
        }                
    ]
    
    # def setUp(self):
    #     super(KeycloakUserTestCase, self).setUp()
    #     self.module = keycloak_user
    #     for theUser in self.testUsers:
    #         set_module_args(theUser)
    #         with self.assertRaises(AnsibleExitJson) as results:
    #             self.module.main()
    # def tearDown(self):
    #     self.module = keycloak_user
    #     for user in self.testUsers:
    #         theUser = user.copy()
    #         theUser["state"] = "absent"
    #         set_module_args(theUser)
    #         with self.assertRaises(AnsibleExitJson) as results:
    #             self.module.main()
    #     super(KeycloakUserTestCase, self).tearDown()           
 
    def test_operation_list(self):
        
        self.module = keycloak_user
        for theUser in self.testUsers:
            set_module_args(theUser)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
            newHabilitation={"idUtilisateur": results.exception.args[0]["user"]["id"],"idRole": expiredHabilitation["idRole"],"dateEcheance": newdate_extension}
            print results

        # newdate_extepirationn = datetime.datetime.strptime(datetime.date.today(), '%y/%m/%d')
        # newHabilitation={"idUtilisateur": expiredHabilitation["idUtilisateur"],"idRole": expiredHabilitation["idRole"],"dateEcheance": newdate_extension}

        # headers = loginAndSetHeaders(toCreate1["spUrl"], toCreate1["spRealm"], toCreate1["spUsername"], toCreate1["spPassword"], toCreate1["spConfigClient_id"], toCreate1["spConfigClient_secret"])
        # getResponse = requests.get(toCreate1["spConfigUrl"]+"/habilitations/"+toCreate1["systemShortName"], headers=headers)
        # dataResponse = getResponse.json()

        # toList:{}
        # toList["auth_keycloak_url"] = "http://localhost:8080/auth"
        # toList["auth_sername"]: "admin"
        # toList["auth_password"]: "password"
        # toList["realm"] = "master"
        # toList["spConfigUrl"] = "http://localhost:8089/config"
        # toList["spConfigClient_id"] = "sx5spconfig"
        # toList["spConfigClient_secret"] = "client_string"
        # toList["operation"] = "list"

        # results = system(toCreate)

    # def test_operation_remove(self):
    #     toRemove:{}
    #     toRemove["auth_keycloak_url"] = "http://localhost:8080/auth"
    #     toRemove["auth_sername"]: "admin"
    #     toRemove["auth_password"]: "password"
    #     toRemove["realm"] = "master"
    #     toRemove["spConfigUrl"] = "http://localhost:8089/config"
    #     toRemove["spConfigClient_id"] = "sx5spconfig"
    #     toRemove["spConfigClient_secret"] = "client_string"
    #     toRemove["operation"] = "remove"


    # def test_operation_expend(self):
    #     toExpend:{}
    #     toExpend["auth_keycloak_url"] = "http://localhost:8080/auth"
    #     toExpend["auth_sername"]: "admin"
    #     toExpend["auth_password"]: "password"
    #     toExpend["realm"] = "master"
    #     toExpend["spConfigUrl"] = "http://localhost:8089/config"
    #     toExpend["spConfigClient_id"] = "sx5spconfig"
    #     toExpend["spConfigClient_secret"] = "client_string"
    #     toExpend["operation"] = "extend"
    #     toExpend["duration"] = "1"

        

    #     toListAfter:{}
    #     toListAfter["auth_keycloak_url"] = "http://localhost:8080/auth"
    #     toListAfter["auth_sername"]: "admin"
    #     toListAfter["auth_password"]: "password"
    #     toListAfter["realm"] = "master"
    #     toListAfter["spConfigUrl"] = "http://localhost:8089/config"
    #     toListAfter["spConfigClient_id"] = "sx5spconfig"
    #     toListAfter["spConfigClient_secret"] = "client_string"
    #     toListAfter["operation"] = "list"

