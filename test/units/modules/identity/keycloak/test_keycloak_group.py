import collections
import os
import unittest
import socket
from ansible.modules.identity.keycloak.keycloak_group import *
from ansible.modules.identity.keycloak.keycloak_component import *
from ansible.module_utils.keycloak_utils import isDictEquals

class KeycloakGroupTestCase(unittest.TestCase):
    userStorageComponent = {
        "url": "http://localhost:18081",
        "username": "admin",
        "password": "admin",
        "realm": "master",
        "state": "present",
        "name": "forGroupUnitTests",
        "parentId": "master",
        "providerId": "ldap",
        "providerType": "org.keycloak.storage.UserStorageProvider",
        "config": {
            "vendor": ["rhds"],
            "usernameLDAPAttribute": ["uid"],
            "rdnLDAPAttribute": ["uid"],
            "uuidLDAPAttribute": ["nsuniqueid"],
            "userObjectClasses": [
                "inetOrgPerson",
                "organizationalPerson"
                ],
            "connectionUrl": ["ldap://localhost:10389"],
            "usersDn": ["ou=People,dc=example,dc=com"],
            "authType": ["simple"],
            "bindDn": ["cn=Directory Manager"],
            "bindCredential": ["Admin123"]
        },
        "subComponents": {
            "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [{
                "name": "groupMapper",
                "providerId": "group-ldap-mapper",
                "config": {
                    "mode": ["LDAP_ONLY"],
                    "membership.attribute.type": ["DN"],
                    "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                    "group.name.ldap.attribute": ["cn"],
                    "membership.ldap.attribute": ["member"],
                    "preserve.group.inheritance": ["true"],
                    "membership.user.ldap.attribute": ["cn"],
                    "group.object.classes": ["groupOfNames"],
                    "groups.dn": ["ou=Groups,dc=example,dc=com"],
                    "drop.non.existing.groups.during.sync": ["false"]
                }
            }],
        },
        "force": False
    }

    def setUp(self):
        localhostname = socket.getfqdn()
        self.userStorageComponent["config"]["connectionUrl"] = ["ldap://" + localhostname + ":10389"]
        component(self.userStorageComponent)
 
    def test_create_group_with_attibutes_dict(self):
        toCreate = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test1",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "realmRoles": [
                "uma_authorization"
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users",
                    "view-identity-providers"
                    ]
                }
            ],
            "state":"present",
            "force":False
        }

        results = group(toCreate)
        print (str(results))
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toCreate["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toCreate["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], toCreate["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toCreate["attributes"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toCreate["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toCreate["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toCreate["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toCreate["realmRoles"]))
        
    def test_create_group_with_attributes_list(self):
        toCreate = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test11",
            "attributes_list": [
                {
                    "name":"attr1",
                    "value":["value1"]
                    },
                {
                    "name": "attr2",
                    "value":["value2"]
                    }
            ], 
            "realmRoles": [
                "uma_authorization"
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users",
                    "view-identity-providers"
                    ]
                }
            ], 
            "state":"present",
            "force":False
        }
        attributes_dict = {
                "attr1":["value1"],
                "attr2":["value2"]
            }
        
        results = group(toCreate)
        print (str(results))
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toCreate["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toCreate["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], attributes_dict), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(attributes_dict))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toCreate["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toCreate["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toCreate["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toCreate["realmRoles"]))

    def test_create_group_with_attributes_dict_and_attributes_list(self):
        toCreate = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test12",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "attributes_list": [
                {
                    "name":"attr3",
                    "value":["value3"]
                    },
                {
                    "name": "attr4",
                    "value":["value4"]
                    }
            ], 
            "realmRoles": [
                "uma_authorization"
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users",
                    "view-identity-providers"
                    ]
                }
            ], 
            "state":"present",
            "force":False
        }
        attributes_dict = {
                "attr1":["value1"],
                "attr2":["value2"],
                "attr3":["value3"],
                "attr4":["value4"]
            }
        
        results = group(toCreate)
        print (str(results))
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toCreate["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toCreate["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], attributes_dict), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(attributes_dict))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toCreate["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toCreate["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toCreate["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toCreate["realmRoles"]))

    def test_create_group_with_user_storage_sync(self):
        toCreate = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test10",
            "syncLdapMappers": True, 
            "state":"present",
            "force":False
        }
        results = group(toCreate)
        print (str(results))
        self.assertTrue(results['changed'])

    def test_group_not_changed(self):
        toDoNotChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test2",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "realmRoles": [
                "uma_authorization"
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users"
                    ]
                }
            ], 
            "state":"present",
            "force":False
        }

        group(toDoNotChange)
        results = group(toDoNotChange)
        
        self.assertFalse(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toDoNotChange["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toDoNotChange["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], toDoNotChange["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toDoNotChange["attributes"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toDoNotChange["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toDoNotChange["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toDoNotChange["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toDoNotChange["realmRoles"]))

    def test_group_modify_force(self):
        toDoNotChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test3",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "realmRoles": [
                "uma_authorization"
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users"
                    ]
                }
            ], 
            "state":"present",
            "force":False
        }

        group(toDoNotChange)
        toDoNotChange["force"] = True
        results = group(toDoNotChange)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toDoNotChange["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toDoNotChange["name"])
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["attributes"], toDoNotChange["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toDoNotChange["attributes"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["clientRoles"], toDoNotChange["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toDoNotChange["clientRoles"]))
        self.assertTrue(isDictEquals(results["ansible_facts"]["group"]["realmRoles"], toDoNotChange["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toDoNotChange["realmRoles"]))

    def test_modify_group(self):
        toChange = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test4",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "realmRoles": [
                "uma_authorization",
            ], 
            "clientRoles": [{
                "clientid": "master-realm",
                "roles": [
                    "manage-users",
                    "view-identity-providers"
                    ]
                }
            ],
            "state":"present",
            "force":False
        }
        group(toChange)
        newToChange = toChange.copy()
        newToChange["attributes"] = {
            "attr3":["value3"]
            }
        newToChange["realmRoles"] = [
                "uma_authorization",
                "offline_access"
            ]

        newToChange["clientRoles"] = [{
            "clientid": "master-realm",
            "roles": [
                "view-clients",
                "query-realms",
                "view-users"
                ]
            },{
            "clientid": "account",
            "roles": [
                "manage-account-links",
                "view-profile",
                "manage-account"
                ]
            }
        ]
        results = group(newToChange)
        self.assertTrue(results['changed'])
        self.assertEquals(results["ansible_facts"]["group"]["name"], toChange["name"], "name: " + results["ansible_facts"]["group"]["name"] + " : " + toChange["name"])
        self.assertTrue(isDictEquals(toChange["attributes"],results["ansible_facts"]["group"]["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toChange["attributes"]))
        self.assertTrue(isDictEquals(newToChange["attributes"], results["ansible_facts"]["group"]["attributes"]), "attributes: " + str(results["ansible_facts"]["group"]["attributes"]) + " : " + str(toChange["attributes"]))
        self.assertTrue(isDictEquals(newToChange["clientRoles"], results["ansible_facts"]["group"]["clientRoles"]), "clientRoles: " + str(results["ansible_facts"]["group"]["clientRoles"]) + " : " + str(toChange["clientRoles"]))
        self.assertTrue(isDictEquals(newToChange["realmRoles"], results["ansible_facts"]["group"]["realmRoles"]), "realmRoles: " + str(results["ansible_facts"]["group"]["realmRoles"]) + " : " + str(toChange["realmRoles"]))

        
    def test_delete_group(self):
        toDelete = {
            "username":"admin", 
            "password":"admin",
            "realm":"master",
            "url":"http://localhost:18081",
            "name":"test5",
            "attributes": {
                "attr1":["value1"],
                "attr2":["value2"]
            }, 
            "state":"present",
            "force":False
        }

        group(toDelete)
        toDelete["state"] = "absent"
        results = group(toDelete)
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'group has been deleted')
