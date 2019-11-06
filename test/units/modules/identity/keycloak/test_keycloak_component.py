# -*- coding: utf-8 -*-
# This unit test class need a Keycloak server running on localhost using port 18081.
# An admin user must exist and his password need to be admin.
# It also need a 389-ds server running on port 10389 with the following OU:
# Users: ou=People,dc=example,dc=com
# Groups: ou=Groups,dc=example,dc=com
# The admin bind DN must be cn=Directory Manager
# The password must be Admin123
# Use the following command to create a compliant Docker container:
# docker run -d --rm --name testldap -p 10389:389 minkwe/389ds:latest
# Use the following command to run a Keycloak server with Docker:
# docker run -d --rm --name testkc -p 18081:8080 --link testldap:testldap -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin jboss/keycloak:latest

from ansible.modules.identity.keycloak import keycloak_component
from units.modules.utils import AnsibleExitJson, ModuleTestCase, set_module_args

class KeycloakComponentTestCase(ModuleTestCase):
    testComponents = [
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "absent",
            "name": "test_create_component_ldap_user_storage_provider",
            "parentId": "master",
            "providerId": "ldap",
            "providerType": "org.keycloak.storage.UserStorageProvider",
            "config": {
                "vendor": ["ad"],
                "usernameLDAPAttribute": ["sAMAccountName"],
                "rdnLDAPAttribute": ["cn"],
                "uuidLDAPAttribute": ["objectGUID"],
                "userObjectClasses":["person, organizationalPerson, user"],
                "connectionUrl":["ldap://ldap.server.com:389"],
                "usersDn":["OU=users,DC=ldap,DC=server,DC=com"],
                "authType":["simple"],
                "bindDn":["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
                "bindCredential":["LeTresLongMotDePasse"]
            },
            "subComponents": {
                "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [{
                        "name": "groupMapper",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=newgroups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    },
                    {
                        "name": "groupMapper2",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=groups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    }
                ]
            },
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "name": "test_modify_component_ldap_user_storage_provider",
            "providerId": "ldap",
            "providerType": "org.keycloak.storage.UserStorageProvider",
            "config": {
                "vendor": ["ad"],
                "usernameLDAPAttribute": ["sAMAccountName"],
                "rdnLDAPAttribute": ["cn"],
                "uuidLDAPAttribute": ["objectGUID"],
                "userObjectClasses": ["person, organizationalPerson, user"],
                "connectionUrl": ["ldap://ldap.server.com:389"],
                "usersDn": ["OU=users,DC=ldap,DC=server,DC=com"],
                "authType":["simple"],
                "bindDn":["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
                "bindCredential": ["LeTresLongMotDePasse"]
            },
            "subComponents": {
                "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [
                    {
                        "name": "groupMapper",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=groups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    }
                ]
            },
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "name":"test_do_not_modify_component_ldap_user_storage_provider",
            "providerId": "ldap",
            "providerType": "org.keycloak.storage.UserStorageProvider",
            "config": {
                "vendor": ["ad"],
                "usernameLDAPAttribute": ["sAMAccountName"],
                "rdnLDAPAttribute": ["cn"],
                "uuidLDAPAttribute": ["objectGUID"],
                "userObjectClasses": ["person, organizationalPerson, user"],
                "connectionUrl": ["ldap://ldap.server.com:389"],
                "usersDn": ["OU=users,DC=ldap,DC=server,DC=com"],
                "authType": ["simple"],
                "bindDn": ["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
                "bindCredential": ["LeTresLongMotDePasse"]
            },
            "subComponents": {
                "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [
                    {
                        "name": "groupMapper",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=newgroups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    },
                    {
                        "name": "groupMapper2",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=groups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    }
                ]
            },
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "name":"test_modify_component_ldap_user_storage_provider_force",
            "providerId": "ldap",
            "providerType": "org.keycloak.storage.UserStorageProvider",
            "config": {
                "vendor": ["ad"],
                "usernameLDAPAttribute": ["sAMAccountName"],
                "rdnLDAPAttribute": ["cn"],
                "uuidLDAPAttribute": ["objectGUID"],
                "userObjectClasses": ["person, organizationalPerson, user"],
                "connectionUrl": ["ldap://ldap.server.com:389"],
                "usersDn": ["OU=users,DC=ldap,DC=server,DC=com"],
                "authType": ["simple"],
                "bindDn": ["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
                "bindCredential": ["LeTresLongMotDePasse"]
            },
            "subComponents": {
                "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [
                    {
                        "name": "groupMapper",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=newgroups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    },
                    {
                        "name": "groupMapper2",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=groups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    }
                ]
            },
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "name": "test_delete_component_ldap_user_storage_provider",
            "providerId": "ldap",
            "providerType": "org.keycloak.storage.UserStorageProvider",
            "config": {
                "vendor": ["ad"],
                "usernameLDAPAttribute": ["sAMAccountName"],
                "rdnLDAPAttribute": ["cn"],
                "uuidLDAPAttribute": ["objectGUID"],
                "userObjectClasses": ["person, organizationalPerson, user"],
                "connectionUrl": ["ldap://ldap.server.com:389"],
                "usersDn": ["OU=users,DC=ldap,DC=server,DC=com"],
                "authType": ["simple"],
                "bindDn": ["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
                "bindCredential": ["LeTresLongMotDePasse"]
            },
            "subComponents": {
                "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [
                    {
                        "name": "groupMapper",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=newgroups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    },
                    {
                        "name": "groupMapper2",
                        "providerId": "group-ldap-mapper",
                        "config": {
                            "mode": ["READ_ONLY"],
                            "membership.attribute.type": ["DN"],
                            "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                            "group.name.ldap.attribute": ["cn"],
                            "membership.ldap.attribute": ["member"],
                            "preserve.group.inheritance": ["true"],
                            "membership.user.ldap.attribute": ["uid"],
                            "group.object.classes": ["groupOfNames"],
                            "groups.dn": ["cn=groups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                            "drop.non.existing.groups.during.sync": ["false"]
                        }
                    }
                ]
            },
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "name": "forSyncUnitTests",
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
                "connectionUrl": ["ldap://testldap:389"],
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
            "force": False,
            "state": "absent"
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "name": "test_modify_component_add_two_mappers_same_providerId",
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
                "connectionUrl": ["ldap://testldap:389"],
                "usersDn": ["ou=People,dc=example,dc=com"],
                "authType": ["simple"],
                "bindDn": ["cn=Directory Manager"],
                "bindCredential": ["Admin123"]
            },
            "subComponents": {
                "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [
                    {
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
                    }
                ]
            },
            "force": False
        }
    ]

    def setUp(self):
        super(KeycloakComponentTestCase, self).setUp()
        self.module = keycloak_component
        for component in self.testComponents:
            set_module_args(component)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
 
    def tearDown(self):
        self.module = keycloak_component
        for component in self.testComponents:
            toDeleteComponent = component.copy()
            toDeleteComponent["state"] = "absent"
            set_module_args(toDeleteComponent)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
        super(KeycloakComponentTestCase, self).tearDown()
 
    def test_create_component_ldap_user_storage_provider(self):
        toCreate = self.testComponents[0].copy()
        toCreate["state"] = "present"
        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue("component" in results.exception.args[0] and results.exception.args[0]['component'] is not None)
        self.assertEquals(results.exception.args[0]['component']['name'],toCreate["name"],"name: " + results.exception.args[0]['component']['name'])
        
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0],toCreate["config"]["vendor"][0],"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])
        subComponentFound = False
        
    def test_modify_component_ldap_user_storage_provider(self):
        toModify = self.testComponents[1].copy()
        toModify["config"]["connectionUrl"][0] = "TestURL"
        toModify["subComponents"] = {
            "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [{
                    "name": "groupMapper",
                    "providerId": "group-ldap-mapper",
                    "config": {
                        "mode": ["READ_ONLY"],
                        "membership.attribute.type": ["DN"],
                        "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                        "group.name.ldap.attribute": ["cn"],
                        "membership.ldap.attribute": ["member"],
                        "preserve.group.inheritance": ["true"],
                        "membership.user.ldap.attribute": ["uid"],
                        "group.object.classes": ["groupOfNames"],
                        "groups.dn": ["cn=newgroups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                        "drop.non.existing.groups.during.sync": ["false"]
                    }
                },
                {
                    "name": "groupMapper2",
                    "providerId": "group-ldap-mapper",
                    "config": {
                        "mode": ["READ_ONLY"],
                        "membership.attribute.type": ["DN"],
                        "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
                        "group.name.ldap.attribute": ["cn"],
                        "membership.ldap.attribute": ["member"],
                        "preserve.group.inheritance": ["true"],
                        "membership.user.ldap.attribute": ["uid"],
                        "group.object.classes": ["groupOfNames"],
                        "groups.dn": ["cn=groups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                        "drop.non.existing.groups.during.sync": ["false"]
                    }
                },
                {
                    "name": "attributeMapper1",
                    "providerId": "user-attribute-ldap-mapper",
                    "config": {
                        "user.model.attribute": ["mobilePhoneNumber"],
                        "ldap.attribute": ["mobile"],
                        "is.mandatory.in.ldap": ["false"],
                        "always.read.value.from.ldap": ["false"],
                        "read.only": ["false"]
                    }
                },
                {
                    "name": "attributeMapper2",
                    "providerId": "user-attribute-ldap-mapper",
                    "config": {
                        "user.model.attribute": ["phoneNumber"],
                        "ldap.attribute": ["telephoneNumber"],
                        "is.mandatory.in.ldap": ["false"],
                        "always.read.value.from.ldap": ["false"],
                        "read.only": ["false"]
                    }
                }
            ]
        }
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
    
        self.assertEquals(results.exception.args[0]['component']['name'], toModify["name"] ,"name: " + results.exception.args[0]['component']['name'])
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0], toModify['config']['vendor'][0] ,"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
        self.assertEquals(results.exception.args[0]['component']['config']['connectionUrl'][0],toModify['config']['connectionUrl'][0], "connectionUrl: " + results.exception.args[0]['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][2]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["user.model.attribute"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][2]["config"]["user.model.attribute"][0],
                     "user.model.attribute: " + subComponent["config"]["user.model.attribute"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][2]["config"]["user.model.attribute"][0])
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][3]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["user.model.attribute"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][3]["config"]["user.model.attribute"][0],
                     "user.model.attribute: " + subComponent["config"]["user.model.attribute"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][3]["config"]["user.model.attribute"][0])

    def test_do_not_modify_component_ldap_user_storage_provider(self):
        toModify = self.testComponents[2].copy()
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertFalse(results.exception.args[0]['changed'])
    
        self.assertEquals(results.exception.args[0]['component']['name'], toModify['name'],"name: " + results.exception.args[0]['component']['name'])
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0], toModify['config']['vendor'][0] ,"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
        self.assertEquals(results.exception.args[0]['component']['config']['connectionUrl'][0], toModify['config']['connectionUrl'][0], "connectionUrl: " + results.exception.args[0]['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])

    def test_modify_component_ldap_user_storage_provider_force(self):
        toModify = self.testComponents[3].copy()
        toModify['force'] = True
        
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
    
        self.assertEquals(results.exception.args[0]['component']['name'], toModify['name'],"name: " + results.exception.args[0]['component']['name'])
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0], toModify['config']['vendor'][0] ,"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
        self.assertEquals(results.exception.args[0]['component']['config']['connectionUrl'][0], toModify['config']['connectionUrl'][0], "connectionUrl: " + results.exception.args[0]['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])

    def test_delete_component_ldap_user_storage_provider(self):
        toDelete = self.testComponents[4].copy()
        toDelete["state"] = "absent"
        set_module_args(toDelete)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'deleted', 'component not deleted')

    def test_sync_ldap_user_storage_provider(self):
        toModify = self.testComponents[5].copy()
        toModify["syncLdapMappers"] = "fedToKeycloak"
        toModify["syncUserStorage"] = "triggerFullSync"
        toModify["state"] = "present"
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])

    def test_modify_component_add_two_mappers_same_provider_id(self):
        toModify = self.testComponents[6].copy()
        toModify["subComponents"] = {
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
                },
                {
                    "name": "mobilePhoneMapper",
                    "providerId": "user-attribute-ldap-mapper",
                    "config": {
                        "user.model.attribute": ["mobilePhoneNumber"],
                        "ldap.attribute": ["mobile"],
                        "is.mandatory.in.ldap": ["false"],
                        "always.read.value.from.ldap": ["false"],
                        "read.only": ["false"]
                    }
                },
                {
                    "name": "phoneMapper",
                    "providerId": "user-attribute-ldap-mapper",
                    "config": {
                        "user.model.attribute": ["phoneNumber"],
                        "ldap.attribute": ["telephoneNumber"],
                        "is.mandatory.in.ldap": ["false"],
                        "always.read.value.from.ldap": ["false"],
                        "read.only": ["false"]
                    }
                },
                {
                    "name": "organisation",
                    "providerId": "user-attribute-ldap-mapper",
                    "config": { 
                        "user.model.attribute": ["company"],
                        "ldap.attribute": ["o"],
                        "is.mandatory.in.ldap": ["false"],
                        "always.read.value.from.ldap": ["false"],
                        "read.only": ["false"]
                    }
                }
            ]
        }
        toModify["syncUserStorage"] = "triggerFullSync"
        toModify["syncLdapMappers"] = "fedToKeycloak"
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
    
        self.assertEquals(results.exception.args[0]['component']['name'], toModify["name"] ,"name: " + results.exception.args[0]['component']['name'])
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0], toModify['config']['vendor'][0] ,"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
        self.assertEquals(results.exception.args[0]['component']['config']['connectionUrl'][0],toModify['config']['connectionUrl'][0], "connectionUrl: " + results.exception.args[0]['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][2]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["user.model.attribute"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][2]["config"]["user.model.attribute"][0],
                     "user.model.attribute: " + subComponent["config"]["user.model.attribute"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][2]["config"]["user.model.attribute"][0])
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][3]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["user.model.attribute"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][3]["config"]["user.model.attribute"][0],
                     "user.model.attribute: " + subComponent["config"]["user.model.attribute"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][3]["config"]["user.model.attribute"][0])
