# -*- coding: utf-8 -*-
# This unit test class need a Keycloak server running on localhost using port 18081.
# An admin user must exist and his password need to be admin.
# Use the following command to run a Keycloak server with Docker:
# docker run -d --rm --name testkc -p 18081:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin jboss/keycloak:latest

from ansible.modules.identity.keycloak import keycloak_client
from units.modules.utils import AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args


class KeycloakClientTestCase(ModuleTestCase):
    testClientRoles = [
        {
            "name":"test1",
            "description": "test1",
            "composite": False
            },
        {
            "name":"test2",
            "description": "test2",
            "composite": False
        }
    ]
    testClients = [
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "clientId": "basetest",
            "rootUrl": "http://test.com:8080",
            "name": "basetestname",
            "description": "Base testing",
            "publicClient": False,
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "clientId": "test_modify_client",
            "rootUrl": "http://test3.com:8080",
            "name": "Modify client test",
            "description": "This client will be modified",
            "adminUrl": "http://test3.com:8080/admin",
            "baseUrl": "http://test3.com:8080",
            "enabled": True,
            "clientAuthenticatorType": "client-secret",
            "redirectUris": ["http://test3.com:8080/secure"],
            "webOrigins": ["http://test3.com:8080/secure"],
            "consentRequired": False,   
            "standardFlowEnabled": True,
            "implicitFlowEnabled": True,
            "directAccessGrantsEnabled": True,
            "serviceAccountsEnabled": True,
            "fullScopeAllowed": True,
            "protocol": "openid-connect",
            "bearerOnly": False,
            "publicClient": False,
            "roles": [
                {
                    "name":"test1",
                    "description": "test1",
                    "composite": False
                },
                {
                    "name":"test2",
                    "description": "test2",
                    "composite": True,
                    "composites": []
                }
            ],
            "protocolMappers": [
                {
                    "name": "test1Mapper",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": False,
                        "user.attribute": "test1",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test1",
                        "jsonType.label": "String"
                    }
                },
                {
                    "name": "test2Mapper",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": 'true',
                        "user.attribute": "test2",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test2",
                        "jsonType.label": "String"
                    }
                }
            ]
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "clientId": "test_add_client_composite_roles",
            "rootUrl": "http://test5.com:8080",
            "name": "Add composites role to this client",
            "description": "Composites role should be added to this client",
            "adminUrl": "http://test5.com:8080/admin",
            "baseUrl": "http://test5.com:8080",
            "enabled": True,
            "clientAuthenticatorType": "client-secret",
            "redirectUris": ["http://test5.com:8080/secure"],
            "webOrigins": ["http://test5.com:8080/secure"],
            "consentRequired": False,   
            "standardFlowEnabled": True,
            "implicitFlowEnabled": True,
            "directAccessGrantsEnabled": True,
            "fullScopeAllowed": True,
            "serviceAccountsEnabled": True,
            "protocol": "openid-connect",
            "bearerOnly": False,
            "publicClient": False,
            "roles":  [
                {
                    "name":"test1",
                    "description": "test1",
                    "composite": False
                    },
                {
                    "name":"test2",
                    "description": "test2",
                    "composite": True,
                    "composites": []
                }
            ],
            "protocolMappers": [
                {
                    "name": "test1Mapper",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": False,
                        "user.attribute": "test1",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test1",
                        "jsonType.label": "String"}
                },
                {
                    "name": "test2Mapper",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": 'true',
                        "user.attribute": "test2",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test2",
                        "jsonType.label": "String"
                    }
                }
            ]
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "clientId": "test_remove_mapper_from_client",
            "rootUrl": "http://test.com:8080",
            "name": "Test remove mapper",
            "description": "Client from which we remove a mapper",
            "publicClient": False,
            "protocolMappers": [
                {
                    "name": "thismapperstays",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": False,
                        "user.attribute": "test1",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test1",
                        "jsonType.label": "String"}
                },
                {
                    "name": "thismappermustbedeleted",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": 'true',
                        "user.attribute": "test2",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test2",
                        "jsonType.label": "String"
                    }
                }
            ],
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "clientId": "test_remove_role_from_client",
            "rootUrl": "http://test.com:8080",
            "name": "Test remove role",
            "description": "Client from which we remove a role",
            "publicClient": False,
            "roles": [
                {
                    "name":"thisrolestays",
                    "description": "This role must stay after the test",
                    "composite": False,
                    "state": "present"
                    },
                {
                    "name":"thisrolemustbedeleted",
                    "description": "This role mus be deleted by the module",
                    "composite": False,
                    "state": "present"
                }
            ],
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "clientId": "test_delete_client",
            "name": "Client to delete",
            "description": "this client should have been deleted",
            "rootUrl": "http://test.com:8080",
            "name": "basetestname",
            "description": "Base testing",
            "publicClient": False,
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "absent",
            "clientId": "test_create_client",
            "rootUrl": "http://test.com:8080",
            "name": "Create client test",
            "description": "This client should be created",
            "adminUrl": "http://test.com:8080/admin",
            "baseUrl": "http://test.com:8080",
            "enabled": True,
            "clientAuthenticatorType": "client-secret",
            "redirectUris": ["http://test.com:8080/secure","http://test1.com:8080/secure"],
            "webOrigins": ["*"],
            "consentRequired": False,   
            "standardFlowEnabled": True,
            "implicitFlowEnabled": True,
            "directAccessGrantsEnabled": True,
            "serviceAccountsEnabled": True,
            "protocol": "openid-connect",
            "fullScopeAllowed": True,
            "bearerOnly": False,
            "roles": [
                {
                    "name":"test1",
                    "description": "test1",
                    "composite": False
                },
                {
                    "name":"toCreate",
                    "description": "toCreate",
                    "composite": True,
                    "composites": [
                        {
                            "name": "admin"
                        }
                    ]
                }
            ],
            "protocolMappers": [
                {
                    "name": "test1Mapper",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": 'true',
                        "user.attribute": "test1",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test1",
                        "jsonType.label": "String"
                    }
                },
                {
                    "name": "test2Mapper",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": 'true',
                        "user.attribute": "test2",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test2",
                        "jsonType.label": "String"
                    }
                }
            ],
            "publicClient": False,
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "absent",
            "clientId": "test_create_client_inexisting_client_role",
            "rootUrl": "http://test.com:8080",
            "name": "Create client test",
            "description": "This client should generate an error",
            "adminUrl": "http://test.com:8080/admin",
            "baseUrl": "http://test.com:8080",
            "enabled": True,
            "clientAuthenticatorType": "client-secret",
            "redirectUris": ["http://test.com:8080/secure","http://test1.com:8080/secure"],
            "webOrigins": ["*"],
            "consentRequired": False,   
            "standardFlowEnabled": True,
            "implicitFlowEnabled": True,
            "directAccessGrantsEnabled": True,
            "serviceAccountsEnabled": True,
            "protocol": "openid-connect",
            "fullScopeAllowed": True,
            "bearerOnly": False,
            "roles": [
                {
                    "name":"test1",
                    "description": "test1",
                    "composite": False
                },
                {
                    "name":"toCreate",
                    "description": "toCreate",
                    "composite": True,
                    "composites": [
                        {
                            "name": "admin"
                        },
                        {
                            "id": "non_existing_client",
                            "name": "non_existing_role"
                        }
                    ]
                }
            ],
            "protocolMappers": [
                {
                    "name": "test1Mapper",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": 'true',
                        "user.attribute": "test1",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test1",
                        "jsonType.label": "String"
                    }
                },
                {
                    "name": "test2Mapper",
                    "protocol": "openid-connect",
                    "protocolMapper": "oidc-usermodel-attribute-mapper",
                    "consentRequired": False,
                    "config": { 
                        "multivalued": 'false',
                        "userinfo.token.claim": 'true',
                        "user.attribute": "test2",
                        "id.token.claim": 'true',
                        "access.token.claim": 'true',
                        "claim.name": "test2",
                        "jsonType.label": "String"
                    }
                }
            ],
            "publicClient": False,
            "force": False
        },
        {
            "auth_keycloak_url": "http://localhost:18081/auth",
            "auth_username": "admin",
            "auth_password": "admin",
            "realm": "master",
            "state": "present",
            "clientId": "test_add_client_scope_mappings",
            "rootUrl": "http://test6.com:8080",
            "name": "Add scope mappings to this client",
            "description": "scope mappings should be added to this client",
            "adminUrl": "http://test6.com:8080/admin",
            "baseUrl": "http://test6.com:8080",
            "enabled": True,
            "clientAuthenticatorType": "client-secret",
            "redirectUris": ["http://test6.com:8080/secure"],
            "webOrigins": ["http://test6.com:8080/secure"],
            "fullScopeAllowed": False,
            "serviceAccountsEnabled": True,
            "protocol": "openid-connect",
            "bearerOnly": False,
            "publicClient": False
        }
    ]

    def setUp(self):
        super(KeycloakClientTestCase, self).setUp()
        self.module = keycloak_client
        for client in self.testClients:
            if client["clientId"] == "basetest":
                client["roles"] = self.testClientRoles
            elif client["clientId"] in ["test_modify_client", "test_add_client_composite_roles", "test_create_client"]:
                client['roles'][1]['composites'].append({'id': self.testClients[0]['clientId'],"name": self.testClientRoles[0]['name']})
            set_module_args(client)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()

    def tearDown(self):
        for client in self.testClients:
            toDelete = client.copy()
            toDelete["state"] = "absent"
            set_module_args(toDelete)
            with self.assertRaises(AnsibleExitJson) as results:
                self.module.main()
        super(KeycloakClientTestCase, self).tearDown()
 
    def test_create_client(self):
        toCreate = self.testClients[6].copy()
        toCreate["state"] = "present"
        set_module_args(toCreate)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['end_state']['enabled'])
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertTrue('clientSecret' in results.exception.args[0])
        OrderdRoles = sorted(results.exception.args[0]['end_state']['clientRoles'], key=lambda k: k['name'])
        self.assertEqual(OrderdRoles[0]['name'], toCreate["roles"][0]['name'], "roles : " + OrderdRoles[0]['name'])
        self.assertEqual(OrderdRoles[1]['name'], toCreate["roles"][1]['name'], "roles : " + OrderdRoles[1]['name'])
        for newComposite in toCreate["roles"][1]['composites']:
            compositeFound = False
            for createdComposite in OrderdRoles[1]['composites']:
                if "id" in newComposite and newComposite["id"] == createdComposite['id'] and newComposite["name"] == createdComposite['name']:
                    compositeFound = True
                elif newComposite["name"] == createdComposite['name']:
                    compositeFound = True
            if "id" in newComposite:
                message = "Composite: id:" + newComposite["id"] + " name:" + newComposite["name"] + " not found"
            else:
                message = "Composite: name:" + newComposite["name"] + " not found"
            self.assertTrue(compositeFound, message)
            
        self.assertEqual(results.exception.args[0]['end_state']['redirectUris'].sort(),toCreate["redirectUris"].sort(),"redirectUris: " + str(results.exception.args[0]['end_state']['redirectUris'].sort()))
        for toCreateMapper in toCreate["protocolMappers"]:
            mapperFound = False
            for mapper in results.exception.args[0]['end_state']['protocolMappers']:
                if mapper["name"] == toCreateMapper["name"]:
                    mapperFound = True
                    break
            self.assertTrue(mapperFound, "no mapper found: " + toCreateMapper["name"])
            if mapperFound:
                self.assertEqual(mapper["config"]["claim.name"], toCreateMapper["config"]["claim.name"], "claim.name: " + toCreateMapper["config"]["claim.name"] + ": " + mapper["config"]["claim.name"])
                self.assertEqual(mapper["config"]["user.attribute"], toCreateMapper["config"]["user.attribute"], "user.attribute: " + mapper["config"]["user.attribute"] + ": " + mapper["config"]["user.attribute"])

    def test_client_not_changed(self):
        set_module_args(self.testClients[0])
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertFalse(results.exception.args[0]['changed'])


    def test_modify_client(self):
        toModifyClient = self.testClients[1].copy()
        toModifyClient["name"] = "test_modify_client_modified"
        toModifyClient["description"] = "This client should have been modified"
        toModifyClient["protocolMappers"] = [{"name": "test1Mapper",
                                        "protocol": "openid-connect",
                                        "protocolMapper": "oidc-usermodel-attribute-mapper",
                                        "consentRequired": False,
                                        "config": { 
                                            "multivalued": 'false',
                                            "userinfo.token.claim": 'false',
                                            "user.attribute": "modifiedattribute",
                                            "id.token.claim": 'true',
                                            "access.token.claim": 'true',
                                            "claim.name": "modifiedclaim",
                                            "jsonType.label": "String"}}]
        set_module_args(toModifyClient)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['end_state']['enabled'])
        self.assertTrue(results.exception.args[0]['changed'])
        
        self.assertEqual(results.exception.args[0]['end_state']['name'], toModifyClient["name"], "name: " + results.exception.args[0]['end_state']['name'])
        self.assertEqual(results.exception.args[0]['end_state']['description'], toModifyClient["description"], 'description: ' + results.exception.args[0]['end_state']['description'])
        self.assertEqual(results.exception.args[0]['end_state']['redirectUris'].sort(),toModifyClient["redirectUris"].sort(),"redirectUris: " + str(results.exception.args[0]['end_state']['redirectUris'].sort()))
        for toChangeMapper in toModifyClient["protocolMappers"]:
            mapperFound = False
            for mapper in results.exception.args[0]['end_state']['protocolMappers']:
                if mapper["name"] == toChangeMapper["name"]:
                    mapperFound = True
                    break
            self.assertTrue(mapperFound, "no mapper found: " + toChangeMapper["name"])
            if mapperFound:
                self.assertEqual(mapper["config"]["claim.name"], toChangeMapper["config"]["claim.name"], "claim.name: " + toChangeMapper["config"]["claim.name"] + ": " + mapper["config"]["claim.name"])
                self.assertEqual(mapper["config"]["user.attribute"], toChangeMapper["config"]["user.attribute"], "user.attribute: " + toChangeMapper["config"]["user.attribute"] + ": " + mapper["config"]["user.attribute"])
        OrderdRoles = sorted(results.exception.args[0]['end_state']['clientRoles'], key=lambda k: k['name'])
        self.assertEqual(OrderdRoles[0]['name'], toModifyClient["roles"][0]['name'], "roles : " + OrderdRoles[0]['name'])
        self.assertEqual(OrderdRoles[1]['name'], toModifyClient["roles"][1]['name'], "roles : " + OrderdRoles[1]['name'])
 
    def test_add_client_composite_roles(self):
        newClientRoles = [
            {
                "name":"test1",
                "description": "test1",
                "composite": False
                },
            {
                "name":"test2",
                "description": "test2",
                "composite": True,
                "composites": [
                    {
                        "id": self.testClients[0]['clientId'],
                        "name": self.testClientRoles[0]['name']
                    },
                    {
                        "id": self.testClients[0]['clientId'],
                        "name": self.testClientRoles[1]['name']
                    },
                    {
                        "name": "admin"
                    }
                ]
            }
        ]
        toAddCompositesForClientRole = self.testClients[2].copy()
        toAddCompositesForClientRole["roles"] = newClientRoles
        set_module_args(toAddCompositesForClientRole)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['end_state']['enabled'])
        self.assertTrue(results.exception.args[0]['changed'])
        OrderdRoles = sorted(results.exception.args[0]['end_state']['clientRoles'], key=lambda k: k['name'])
        self.assertEqual(OrderdRoles[0]['name'], newClientRoles[0]['name'], "roles : " + OrderdRoles[0]['name'])
        self.assertEqual(OrderdRoles[1]['name'], newClientRoles[1]['name'], "roles : " + OrderdRoles[1]['name'])
        #self.assertEqual(len(OrderdRoles[1]['composites']), len(newClientRoles[1]['composites']), 'Composite length: ' + len(OrderdRoles[1]['composites']) + ' : ' + len(newClientRoles[1]['composites']))
        OrderedComposites = sorted(OrderdRoles[1]['composites'], key=lambda k:['name]'])
        for index, composite in enumerate(OrderedComposites):
            compositeFound = False
            for toChangeComposite in newClientRoles[1]['composites']:
                if toChangeComposite['name'] == composite['name']:
                    compositeFound = True
                    break
            self.assertTrue(compositeFound, 'Composite ' + composite['name'] + ' not found')
    
    def test_remove_mapper_from_client(self):
        toRemoveMapperFromClient = self.testClients[3].copy()
        toRemoveMapperFromClient["protocolMappers"][1]["state"] = "absent"
        set_module_args(toRemoveMapperFromClient)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        mapperFound = False
        for mapper in results.exception.args[0]['end_state']['protocolMappers']:
            if mapper["name"] == toRemoveMapperFromClient["protocolMappers"][1]["name"]:
                mapperFound = True
                break
        self.assertFalse(mapperFound, "Mapper " + toRemoveMapperFromClient["protocolMappers"][1]["name"] + " has not been deleted")
         
    def test_remove_role_from_client(self):
        toRemoveRoleFromClient = self.testClients[4].copy()
        toRemoveRoleFromClient["roles"][1]["state"] = "absent"
        set_module_args(toRemoveRoleFromClient)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        roleFound = False
        for role in results.exception.args[0]['end_state']['clientRoles']:
            if role["name"] == toRemoveRoleFromClient["roles"][1]["name"]:
                roleFound = True
                break
        self.assertFalse(roleFound, "Role " + toRemoveRoleFromClient["roles"][1]["name"] + " has not been deleted")

    def test_delete_client(self):
        toDeleteClient = self.testClients[5].copy()
        toDeleteClient["state"] = "absent"
        set_module_args(toDeleteClient)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'deleted', 'client not deleted')

    def test_create_client_with_non_existing_client_composite_role(self):
        toErrorClient = self.testClients[7].copy()
        toErrorClient["state"] = "present"
        set_module_args(toErrorClient)
        with self.assertRaises(AnsibleFailJson) as results:
            self.module.main()
        self.assertRegexpMatches(results.exception.args[0]['msg'], 'client ' + toErrorClient["roles"][1]["composites"][1]["id"] + ' does not exist', 'error not generated')

    def test_add_client_scope_mappings_roles(self):
        toAddnewClientScopeMappings = self.testClients[8].copy()
        newClientScopeMappings = {
                "realm": [
                    {"name": "admin", "state": "present"},
                    {"name": "offline_access","state": "present"}
                ],
                "clients": [
                    {
                        "id": "master-realm",
                        "roles": [{"name": "view-events"},{"name": "manage-clients"}]
                    },
                    {
                        "id": "master-realm",
                        "roles": [{"name": "view-clients","state": "present"},{"name": "view-realm"}]
                    }
                ]
            }
        toAddnewClientScopeMappings["scope_mappings"] = newClientScopeMappings
        set_module_args(toAddnewClientScopeMappings)
        with self.assertRaises(AnsibleExitJson) as results: 
            self.module.main()
        self.assertTrue(results.exception.args[0]['changed'])
