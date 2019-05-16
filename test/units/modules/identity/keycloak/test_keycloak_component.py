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
import collections
import os

from ansible.modules.identity.keycloak import keycloak_component
from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args

class KeycloakComponentTestCase(ModuleTestCase):
    createComponentLdapUserStorageProvider = {
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
    }
    userStorageComponentForSync = {
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
    }

    modifyComponentLdapUserStorageProvider = {
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
    }
    doNotModifyComponentLdapUserStorageProvider = {
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
    }
    
    modifyComponentLdapUserStorageProviderForce = {
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
    }

    deleteComponentLdapUserStorageProvider = {
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
    }

    def setUp(self):
        super(KeycloakComponentTestCase, self).setUp()
        self.module = keycloak_component
        set_module_args(self.createComponentLdapUserStorageProvider)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        set_module_args(self.userStorageComponentForSync)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        set_module_args(self.modifyComponentLdapUserStorageProvider)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        set_module_args(self.modifyComponentLdapUserStorageProviderForce)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        set_module_args(self.doNotModifyComponentLdapUserStorageProvider)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        set_module_args(self.deleteComponentLdapUserStorageProvider)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
 
    def tearDown(self):
        self.module = keycloak_component
        set_module_args(self.userStorageComponentForSync)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        super(KeycloakComponentTestCase, self).tearDown()
 
    def test_create_component_ldap_user_storage_provider(self):
        toCreate = self.createComponentLdapUserStorageProvider.copy()
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
        self.modifyComponentLdapUserStorageProvider["config"]["connectionUrl"][0] = "TestURL"
        self.modifyComponentLdapUserStorageProvider["subComponents"] = {
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
        }
        set_module_args(self.modifyComponentLdapUserStorageProvider)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
    
        self.assertEquals(results.exception.args[0]['component']['name'], self.modifyComponentLdapUserStorageProvider["name"] ,"name: " + results.exception.args[0]['component']['name'])
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0], self.modifyComponentLdapUserStorageProvider['config']['vendor'][0] ,"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
        self.assertEquals(results.exception.args[0]['component']['config']['connectionUrl'][0],self.modifyComponentLdapUserStorageProvider['config']['connectionUrl'][0], "connectionUrl: " + results.exception.args[0]['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == self.modifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     self.modifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + self.modifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == self.modifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     self.modifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + self.modifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])

    def test_do_not_modify_component_ldap_user_storage_provider(self):
        set_module_args(self.doNotModifyComponentLdapUserStorageProvider)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertFalse(results.exception.args[0]['changed'])
    
        self.assertEquals(results.exception.args[0]['component']['name'], self.doNotModifyComponentLdapUserStorageProvider['name'],"name: " + results.exception.args[0]['component']['name'])
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0], self.doNotModifyComponentLdapUserStorageProvider['config']['vendor'][0] ,"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
        self.assertEquals(results.exception.args[0]['component']['config']['connectionUrl'][0], self.doNotModifyComponentLdapUserStorageProvider['config']['connectionUrl'][0], "connectionUrl: " + results.exception.args[0]['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == self.doNotModifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     self.doNotModifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + self.doNotModifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == self.doNotModifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     self.doNotModifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + self.doNotModifyComponentLdapUserStorageProvider["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])

    def test_modify_component_ldap_user_storage_provider_force(self):
        self.modifyComponentLdapUserStorageProviderForce['force'] = True
        
        set_module_args(self.modifyComponentLdapUserStorageProviderForce)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
    
        self.assertEquals(results.exception.args[0]['component']['name'], self.modifyComponentLdapUserStorageProviderForce['name'],"name: " + results.exception.args[0]['component']['name'])
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0], self.modifyComponentLdapUserStorageProviderForce['config']['vendor'][0] ,"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
        self.assertEquals(results.exception.args[0]['component']['config']['connectionUrl'][0], self.modifyComponentLdapUserStorageProviderForce['config']['connectionUrl'][0], "connectionUrl: " + results.exception.args[0]['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == self.modifyComponentLdapUserStorageProviderForce["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     self.modifyComponentLdapUserStorageProviderForce["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + self.modifyComponentLdapUserStorageProviderForce["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == self.modifyComponentLdapUserStorageProviderForce["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     self.modifyComponentLdapUserStorageProviderForce["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + self.modifyComponentLdapUserStorageProviderForce["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])

    def test_delete_component_ldap_user_storage_provider(self):
        self.deleteComponentLdapUserStorageProvider["state"] = "absent"
        set_module_args(self.deleteComponentLdapUserStorageProvider)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'deleted', 'component not deleted')

    def test_sync_ldap_user_storage_provider(self):
        toModify = self.userStorageComponentForSync.copy()
        toModify["syncLdapMappers"] = "fedToKeycloak"
        toModify["syncUserStorage"] = "triggerFullSync"
        toModify["state"] = "present"
        set_module_args(toModify)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
