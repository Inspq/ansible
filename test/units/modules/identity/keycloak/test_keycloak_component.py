import collections
import os
<<<<<<< HEAD
<<<<<<< HEAD

from ansible.modules.identity.keycloak import keycloak_component
from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args

class KeycloakComponentTestCase(ModuleTestCase):

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
=======
import unittest
=======
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.

from ansible.modules.identity.keycloak import keycloak_component
from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args

<<<<<<< HEAD
class KeycloakComponentTestCase(unittest.TestCase):
 
    def test_create_component_ldap_user_storage_provider(self):
        toCreate = {}
        toCreate["url"] = "http://localhost:18081"
        toCreate["username"] = "admin"
        toCreate["password"] = "admin"
        toCreate["realm"] = "master"
        toCreate["state"] = "present"
        toCreate["name"] = "test1"
        toCreate["parentId"] = "master"
        toCreate["providerId"] = "ldap"
        toCreate["providerType"] = "org.keycloak.storage.UserStorageProvider"
        toCreate["config"] = dict(
            vendor=["ad"],
            usernameLDAPAttribute=["sAMAccountName"],
            rdnLDAPAttribute=["cn"],
            uuidLDAPAttribute=["objectGUID"],
            userObjectClasses=["person, organizationalPerson, user"],
            connectionUrl=["ldap://ldap.server.com:389"],
            usersDn=["OU=users,DC=ldap,DC=server,DC=com"],
            authType=["simple"],
            bindDn=["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
            bindCredential=["LeTresLongMotDePasse"]
            )
        toCreate["subComponents"] = {
            "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [{
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
class KeycloakComponentTestCase(ModuleTestCase):

    modifyComponentLdapUserStorageProvider = {
        "url": "http://localhost:18081/auth",
        "username": "admin",
        "password": "admin",
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
        "url": "http://localhost:18081/auth",
        "username": "admin",
        "password": "admin",
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
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
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
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
        }
        toCreate["force"] = False

        results = component(toCreate)
        #print str(results)
    
        self.assertTrue("component" in results['ansible_facts'] and results['ansible_facts']['component'] is not None)
        self.assertEquals(results['ansible_facts']['component']['name'],toCreate["name"],"name: " + results['ansible_facts']['component']['name'])
        self.assertTrue(results['changed'])
        self.assertEquals(results['ansible_facts']['component']['config']['vendor'][0],toCreate["config"]["vendor"][0],"vendor: " + results['ansible_facts']['component']['config']['vendor'][0])
        subComponentFound = False
        for subComponent in results['ansible_facts']['subComponents']:
            if subComponent["name"] == toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results['ansible_facts']['subComponents']:
            if subComponent["name"] == toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])
        subComponentFound = False
        
    def test_modify_component_ldap_user_storage_provider(self):
        toModify = {}
        toModify["url"] = "http://localhost:18081"
        toModify["username"] = "admin"
        toModify["password"] = "admin"
        toModify["realm"] = "master"
        toModify["state"] = "present"
        toModify["name"] = "test2"
        toModify["providerId"] = "ldap"
        toModify["providerType"] = "org.keycloak.storage.UserStorageProvider"
        toModify["config"] = dict(
            vendor=["ad"],
            usernameLDAPAttribute=["sAMAccountName"],
            rdnLDAPAttribute=["cn"],
            uuidLDAPAttribute=["objectGUID"],
            userObjectClasses=["person, organizationalPerson, user"],
            connectionUrl=["ldap://ldap.server.com:389"],
            usersDn=["OU=users,DC=ldap,DC=server,DC=com"],
            authType=["simple"],
            bindDn=["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
            bindCredential=["LeTresLongMotDePasse"]
            )
        toModify["subComponents"] = {
                "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [{
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
        },
        "force": False
    }
    
    modifyComponentLdapUserStorageProviderForce = {
        "url": "http://localhost:18081/auth",
        "username": "admin",
        "password": "admin",
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
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
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
<<<<<<< HEAD
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
=======
                        "groups.dn": ["cn=groups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                        "drop.non.existing.groups.during.sync": ["false"]
                    }
                }]
            }
        toModify["force"] = False
        component(toModify)
        toModify["config"]["connectionUrl"][0] = "TestURL"
        toModify["subComponents"] = {
            "org.keycloak.storage.ldap.mappers.LDAPStorageMapper": [{
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
                        "groups.dn": ["cn=groups,OU=SEC,DC=SANTEPUBLIQUE,DC=RTSS,DC=QC,DC=CA"],
                        "drop.non.existing.groups.during.sync": ["false"]
                    }
                }
            ]
        },
        "force": False
    }

    deleteComponentLdapUserStorageProvider = {
        "url": "http://localhost:18081/auth",
        "username": "admin",
        "password": "admin",
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
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
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
<<<<<<< HEAD
<<<<<<< HEAD
        },
        "force": False
    }

    def setUp(self):
        super(KeycloakComponentTestCase, self).setUp()
        self.module = keycloak_component
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
        super(KeycloakComponentTestCase, self).tearDown()
 
    def test_create_component_ldap_user_storage_provider(self):
        toCreate = {}
        toCreate["auth_keycloak_url"] = "http://localhost:18081/auth"
        toCreate["auth_username"] = "admin"
        toCreate["auth_password"] = "admin"
        toCreate["realm"] = "master"
        toCreate["state"] = "present"
        toCreate["name"] = "test_create_component_ldap_user_storage_provider"
        toCreate["parentId"] = "master"
        toCreate["providerId"] = "ldap"
        toCreate["providerType"] = "org.keycloak.storage.UserStorageProvider"
        toCreate["config"] = dict(
=======
        }
        results = component(toModify)
        #print str(results)
    
        self.assertEquals(results['ansible_facts']['component']['name'],"test2","name: " + results['ansible_facts']['component']['name'])
        self.assertTrue(results['changed'])
        self.assertEquals(results['ansible_facts']['component']['config']['vendor'][0],"ad","vendor: " + results['ansible_facts']['component']['config']['vendor'][0])
        self.assertEquals(results['ansible_facts']['component']['config']['connectionUrl'][0],"TestURL","connectionUrl: " + results['ansible_facts']['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results['ansible_facts']['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results['ansible_facts']['subComponents']:
            if subComponent["name"] == toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
                     toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])

    def test_do_not_modify_component_ldap_user_storage_provider(self):
        toDoNotModify = {}
        toDoNotModify["url"] = "http://localhost:18081"
        toDoNotModify["username"] = "admin"
        toDoNotModify["password"] = "admin"
        toDoNotModify["realm"] = "master"
        toDoNotModify["state"] = "present"
        toDoNotModify["name"] = "test3"
        toDoNotModify["providerId"] = "ldap"
        toDoNotModify["providerType"] = "org.keycloak.storage.UserStorageProvider"
        toDoNotModify["config"] = dict(
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
        },
        "force": False
    }

    def setUp(self):
        super(KeycloakComponentTestCase, self).setUp()
        self.module = keycloak_component
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
        super(KeycloakComponentTestCase, self).tearDown()
 
    def test_create_component_ldap_user_storage_provider(self):
        toCreate = {}
        toCreate["url"] = "http://localhost:18081/auth"
        toCreate["username"] = "admin"
        toCreate["password"] = "admin"
        toCreate["realm"] = "master"
        toCreate["state"] = "present"
        toCreate["name"] = "test_create_component_ldap_user_storage_provider"
        toCreate["parentId"] = "master"
        toCreate["providerId"] = "ldap"
        toCreate["providerType"] = "org.keycloak.storage.UserStorageProvider"
        toCreate["config"] = dict(
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
            vendor=["ad"],
            usernameLDAPAttribute=["sAMAccountName"],
            rdnLDAPAttribute=["cn"],
            uuidLDAPAttribute=["objectGUID"],
            userObjectClasses=["person, organizationalPerson, user"],
            connectionUrl=["ldap://ldap.server.com:389"],
            usersDn=["OU=users,DC=ldap,DC=server,DC=com"],
            authType=["simple"],
            bindDn=["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
            bindCredential=["LeTresLongMotDePasse"]
            )
<<<<<<< HEAD
<<<<<<< HEAD
        toCreate["subComponents"] = {
=======
        toDoNotModify["subComponents"] = {
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
        toCreate["subComponents"] = {
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
        toCreate["force"] = False

        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue("component" in results.exception.args[0] and results.exception.args[0]['component'] is not None)
        self.assertEquals(results.exception.args[0]['component']['name'],toCreate["name"],"name: " + results.exception.args[0]['component']['name'])
        
        self.assertEquals(results.exception.args[0]['component']['config']['vendor'][0],toCreate["config"]["vendor"][0],"vendor: " + results.exception.args[0]['component']['config']['vendor'][0])
<<<<<<< HEAD
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
=======
        toDoNotModify["force"] = False
        component(toDoNotModify)
        results = component(toDoNotModify)
    
        self.assertEquals(results['ansible_facts']['component']['name'],"test3","name: " + results['ansible_facts']['component']['name'])
        self.assertFalse(results['changed'])
        self.assertEquals(results['ansible_facts']['component']['config']['vendor'][0],"ad","vendor: " + results['ansible_facts']['component']['config']['vendor'][0])
        self.assertEquals(results['ansible_facts']['component']['config']['connectionUrl'][0],"ldap://ldap.server.com:389","connectionUrl: " + results['ansible_facts']['component']['config']['connectionUrl'][0])
        subComponentFound = False
        for subComponent in results['ansible_facts']['subComponents']:
            if subComponent["name"] == toDoNotModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["name"]:
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
<<<<<<< HEAD
<<<<<<< HEAD
                     toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
=======
                     toDoNotModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toDoNotModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results['ansible_facts']['subComponents']:
            if subComponent["name"] == toDoNotModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
                     toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][0]["config"]["groups.dn"][0])
        subComponentFound = False
        for subComponent in results.exception.args[0]['subComponents']:
            if subComponent["name"] == toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["name"]:
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
                subComponentFound = True
                break
        self.assertTrue(subComponentFound,"Sub component not found in the sub components")
        self.assertEquals(subComponent["config"]["groups.dn"][0], 
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
                     toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toCreate["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])
        subComponentFound = False
        
    def test_modify_component_ldap_user_storage_provider(self):
        self.modifyComponentLdapUserStorageProvider["config"]["connectionUrl"][0] = "TestURL"
        self.modifyComponentLdapUserStorageProvider["subComponents"] = {
<<<<<<< HEAD
=======
                     toDoNotModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0],
                     "groups.dn: " + subComponent["config"]["groups.dn"][0] + ": " + toDoNotModify["subComponents"]["org.keycloak.storage.ldap.mappers.LDAPStorageMapper"][1]["config"]["groups.dn"][0])

    def test_delete_component_ldap_user_storage_provider(self):
        toDelete = {}
        toDelete["url"] = "http://localhost:18081"
        toDelete["username"] = "admin"
        toDelete["password"] = "admin"
        toDelete["realm"] = "master"
        toDelete["state"] = "present"
        toDelete["name"] = "test4"
        toDelete["providerId"] = "ldap"
        toDelete["providerType"] = "org.keycloak.storage.UserStorageProvider"
        toDelete["config"] = dict(
            vendor=["ad"],
            usernameLDAPAttribute=["sAMAccountName"],
            rdnLDAPAttribute=["cn"],
            uuidLDAPAttribute=["objectGUID"],
            userObjectClasses=["person, organizationalPerson, user"],
            connectionUrl=["ldap://ldap.server.com:389"],
            usersDn=["OU=users,DC=ldap,DC=server,DC=com"],
            authType=["simple"],
            bindDn=["CN=toto,OU=users,DC=ldap,DC=server,DC=com"],
            bindCredential=["LeTresLongMotDePasse"]
            )
        toDelete["subComponents"] = {
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
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
<<<<<<< HEAD
    
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
=======
        toDelete["force"] = False
        component(toDelete)
        toDelete["state"] = "absent"
        results = component(toDelete)
    
        self.assertTrue(results['changed'])
        self.assertEqual(results['stdout'], 'deleted', 'client has been deleted')
>>>>>>> SX5-868 Add role management to keycloak_group module. Add
=======
    
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
>>>>>>> SX5-868 Add keycloak_component module with non mock unit tests.
