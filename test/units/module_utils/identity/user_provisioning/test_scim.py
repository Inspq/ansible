from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

#import pytest
import unittest
import json
from ansible.module_utils.identity.user_provisioning.scim import SCIMClient, User
from ansible.module_utils.identity.keycloak.keycloak import get_token

class SCIMTestCase(unittest.TestCase):
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
        }
    ]        
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.access_token = get_token(
            base_url='http://inspq-6673.inspq.qc.ca:18081/auth',
            validate_certs=False,
            auth_realm="msss",
            client_id="sx5idmlocal",
            auth_username="sx5approvisionneur",
            auth_password="appr0sx5!",
            client_secret=None)
        for json_user in self.testUsers:
            SCIMClient(base_url="http://inspq-6673.inspq.qc.ca:14102/scim/v2", access_token=self.access_token).createUser(User.from_json(json.dumps(json_user)))

    def tearDown(self):
        for json_user in self.testUsers:
            SCIMClient(base_url="http://inspq-6673.inspq.qc.ca:14102/scim/v2", access_token=self.access_token).deleteUser(User.from_json(json.dumps(json_user)))
        unittest.TestCase.tearDown(self)

    def testSearchUser(self):
        userToSearch = "test02"
        scimClient = SCIMClient(base_url="http://inspq-6673.inspq.qc.ca:14102/scim/v2", access_token=self.access_token)
        scimuser = scimClient.searchUserByUserName(userToSearch)
        self.assertEqual(scimuser.userName, userToSearch, scimuser.userName + " is not " + userToSearch)
        
    def testGetUserById(self):
        userToGet = "test02"
        scimClient = SCIMClient(base_url="http://inspq-6673.inspq.qc.ca:14102/scim/v2", access_token=self.access_token)
        scimuser = scimClient.getUserById(userToGet)
        self.assertEqual(scimuser.userName, userToGet, scimuser.userName + " is not " + userToGet)

    def testCreateUser(self):
        userToCreate = User.from_json(json.dumps(self.userToAdd))
        scimClient = SCIMClient(base_url="http://inspq-6673.inspq.qc.ca:14102/scim/v2", access_token=self.access_token)
        scimuser = scimClient.createUser(userToCreate)
        self.assertEqual(scimuser.userName, userToCreate.userName, scimuser.userName + " is not " + userToCreate.userName)
        
    def testDeleteUser(self):
        userToDelete = User.from_json(json.dumps(self.testUsers[0]))
        scimClient = SCIMClient(base_url="http://inspq-6673.inspq.qc.ca:14102/scim/v2", access_token=self.access_token)
        response = scimClient.deleteUser(userToDelete)
        self.assertEqual(response.code, 204, "Create response code incorrect: " + str(response.code))

    def testUpdateUser(self):
        userToUpdate = User.from_json(json.dumps(self.testUsers[1]))
        userToUpdate.displayName = "Test 02"
        scimClient = SCIMClient(base_url="http://inspq-6673.inspq.qc.ca:14102/scim/v2", access_token=self.access_token)
        scimuser = scimClient.updateUser(userToUpdate)
        self.assertEqual(scimuser.userName, userToUpdate.userName, scimuser.userName + " is not " + userToUpdate.userName)

if __name__ == '__main__':
    unittest.main()