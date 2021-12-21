# -*- coding: utf-8 -*-
import mock
import json
from ansible.modules.identity.user_provisioning import scim_user
from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args
from ansible.module_utils.identity.user_provisioning.scim import SCIMClient, User
from ansible.module_utils.identity.user_provisioning.mock_scim_server import mocked_scim_requests
from ansible.module_utils.identity.keycloak.keycloak import isDictEquals

class ScimUserTestCase(ModuleTestCase):
    testUsers = [
        {
            "scim_server_url": "http://scim.server.url/scim/v2",
            "access_token": "eyasdasfasd",
            "userName": "test01",
            "name": {
                "familyName":"Test1",
                "givenName":"Test1",
                "middleName":None
                },
            "roles":[
                {
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "state": "present",
            "force": False
            },
        {
            "scim_server_url": "http://scim.server.url/scim/v2",
            "access_token": "eyasdasfasd",
            "userName": "test02",
            "name": {
                "familyName":"Test2",
                "givenName":"Test2",
                "middleName":None
                },
            "roles":[
                {
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "state": "present",
            "force": False
            },
        {
            "scim_server_url": "http://scim.server.url/scim/v2",
            "access_token": "eyasdasfasd",
            "userName": "test03",
            "name": {
                "familyName":"Test3",
                "givenName":"Test3",
                "middleName":None
                },
            "roles":[
                {
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "state": "present",
            "force": False
            }
        
        ]
    def setUp(self):
        super(ScimUserTestCase, self).setUp()
        self.module = scim_user

    def tearDown(self):
        super(ScimUserTestCase, self).tearDown()

    def userToSCIMUser(self, user):
        scimUser = user.copy()
        del(scimUser['scim_server_url'])
        del(scimUser['access_token'])
        del(scimUser['state'])
        del(scimUser['force'])
        return(User(scimUser))
        
    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testCreateNewUser(self, open_url):
        user = self.testUsers[2].copy()
        set_module_args(user)
        scimUser = self.userToSCIMUser(user)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(json.loads(scimUser.to_json()), json.loads(User(results.exception.args[0]['user']).to_json()), exclude=["_ansible_keep_remote_files","scim_server_url","access_token","_ansible_remote_tmp"]), "User :" + str(results.exception.args[0]['user']) + " is not " + scimUser.to_json())
        self.assertTrue("externalId" in json.loads(User(results.exception.args[0]['user']).to_json()), User(results.exception.args[0]['user']).to_json() + " does not have externalId")
        
    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testUserNotChanged(self, open_url):
        user = self.testUsers[1].copy()
        set_module_args(user)
        scimUser = self.userToSCIMUser(user)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertFalse(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(json.loads(scimUser.to_json()), json.loads(User(results.exception.args[0]['user']).to_json()), exclude=["_ansible_keep_remote_files","scim_server_url","access_token","_ansible_remote_tmp"]), "User :" + str(results.exception.args[0]['user']) + " is not " + scimUser.to_json())

    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testUserChanged(self, open_url):
        user = self.testUsers[1].copy()
        user["displayName"] = "Test 02"
        set_module_args(user)
        scimUser = self.userToSCIMUser(user)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue(isDictEquals(json.loads(scimUser.to_json()), json.loads(User(results.exception.args[0]['user']).to_json()), exclude=["_ansible_keep_remote_files","scim_server_url","access_token","_ansible_remote_tmp"]), "User :" + str(results.exception.args[0]['user']) + " is not " + scimUser.to_json())

    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testDeleteUser(self, open_url):
        user = self.testUsers[0].copy()
        user["state"] = "absent"
        set_module_args(user)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'deleted', 'User not deleted')

