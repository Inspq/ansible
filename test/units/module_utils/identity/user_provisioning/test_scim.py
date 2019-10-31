from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import mock

from unittest import TestCase
import json

from ansible.module_utils.identity.user_provisioning.scim import SCIMClient, User
from ansible.module_utils.identity.user_provisioning.mock_scim_server import mocked_scim_requests


class SCIMTestCase(TestCase):
    access_token = ""
    userToAdd = {
        "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id":"test03",
        "externalId":"5e771101-e3cd-4a77-851b-54f3f2668846",
        "meta":{
            "resourceType": None,
            "created":"2019-10-29T04:00:00.000+0000",
            "lastModified":None,
            "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test03",
            "version":None
        },
        "userName":"test03",
        "name":{
            "formatted":None,
            "familyName":"Test3",
            "givenName":"Test3",
            "middleName":None,
            "honorificPrefix":None,
            "honorificSuffix":None
        },
        "displayName":None,
        "nickName":None,
        "profileUrl":None,
        "title":None,
        "userType":None,
        "preferredLanguage":None,
        "locale":None,
        "timezone":None,
        "active":None,
        "password":None,
        "emails":[
            {
                "value":"test.test3@test.test",
                "display":None,
                "type":None,
                "primary":None
            }
        ],
        "phoneNumbers":None,
        "ims":None,
        "photos":None,
        "addresses":None,
        "groups":None,
        "entitlements":None,
        "roles":[
            {
                "value":"100",
                "display":"FA-SAISIE",
                "type":None,
                "primary":None
            }
        ],
        "x509Certificates":None
    }
    testUsers = [
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test01",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test01",
                "version":None
            },
            "userName":"test01",
            "name":{
                "formatted":None,
                "familyName":"Test1",
                "givenName":"Test1",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test1@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },
        {
            "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id":"test02",
            "externalId":"5e771101-e3cd-4a77-851b-54f5f2668846",
            "meta":{
                "resourceType": None,
                "created":"2019-10-29T04:00:00.000+0000",
                "lastModified":None,
                "location":"http://inspq-6673.inspq.qc.ca:14102/scim/v2/Users/test02",
                "version":None
            },
            "userName":"test02",
            "name":{
                "formatted":None,
                "familyName":"Test2",
                "givenName":"Test2",
                "middleName":None,
                "honorificPrefix":None,
                "honorificSuffix":None
            },
            "displayName":None,
            "nickName":None,
            "profileUrl":None,
            "title":None,
            "userType":None,
            "preferredLanguage":None,
            "locale":None,
            "timezone":None,
            "active":None,
            "password":None,
            "emails":[
                {
                    "value":"test2@test.test",
                    "display":None,
                    "type":None,
                    "primary":None
                }
            ],
            "phoneNumbers":None,
            "ims":None,
            "photos":None,
            "addresses":None,
            "groups":None,
            "entitlements":None,
            "roles":[
                {
                    "value":"100",
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ],
            "x509Certificates":None
        },
        {
           "userName":"testes01",
           "displayName":None,
           "name":{
              "middleName":None,
              "givenName":"Test",
              "familyName":"Test"
           },
           "roles":[
              {
                 "display":"FA-SAISIE",
                 "primary":False
              }
           ],
           "id":"testes01",
           "schemas":[
              "urn:ietf:params:scim:schemas:core:2.0:User"
           ]
        }
    ]        
    
    def setUp(self):
        TestCase.setUp(self)

    def tearDown(self):
        TestCase.tearDown(self)


    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testSearchUser(self, open_url):
        userToSearch = "test02"
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.searchUserByUserName(userToSearch)
        self.assertEqual(scimuser.userName, userToSearch, scimuser.userName + " is not " + userToSearch)
        
    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testSearchNonExistingUser(self, open_url):
        userToSearch = "test05"
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.searchUserByUserName(userToSearch)
        self.assertIs(scimuser, None, userToSearch + " is not supposed to be found")

    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testGetUserById(self, open_url):
        userToGet = "test02"
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.getUserById(userToGet)
        self.assertEqual(scimuser.userName, userToGet, scimuser.userName + " is not " + userToGet)

    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testCreateUser(self, open_url):
        userToCreate = User.from_json(json.dumps(self.userToAdd))
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.createUser(userToCreate)
        self.assertEqual(scimuser.userName, userToCreate.userName, scimuser.userName + " is not " + userToCreate.userName)
        
    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testDeleteUser(self, open_url):
        userToDelete = User.from_json(json.dumps(self.testUsers[0]))
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        response = scimClient.deleteUser(userToDelete)
        self.assertEqual(response.code, 204, "Delete response code incorrect: " + str(response.code))

    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testUpdateUser(self, open_url):
        userToUpdate = User.from_json(json.dumps(self.testUsers[1]))
        userToUpdate.displayName = "Test 02"
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.updateUser(userToUpdate)
        self.assertEqual(scimuser.userName, userToUpdate.userName, scimuser.userName + " is not " + userToUpdate.userName)

    @mock.patch('ansible.module_utils.identity.user_provisioning.scim.open_url', side_effect=mocked_scim_requests)
    def testCreateUserWithoutExternalId(self, open_url):
        userToCreate = User.from_json(json.dumps(self.testUsers[2]))
        scimClient = SCIMClient(base_url="http://scim.server.url/scim/v2", access_token=self.access_token)
        scimuser = scimClient.createUser(userToCreate)
        self.assertDictContainsSubset(json.loads(scimuser.to_json()), json.loads(userToCreate.to_json()), scimuser.to_json() + " is not " + userToCreate.to_json())
        self.assertTrue("externalId" in json.loads(scimuser.to_json()), scimuser.to_json() + " does not have externalId")
