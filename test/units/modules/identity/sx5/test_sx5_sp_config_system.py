#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# Pour exécuter ce test, les composants Keycloak et sx5_sp_config doivent être fonctionnel.
# Utiliser les commandes suivantes pour les lancer avec Docker
# Lancer le LDAP (optionnel pour ce test)
docker pull minkwe/389ds:latest
docker run -d --rm --name testldap -p 10389:389 minkwe/389ds:latest
# Lancer un serveur Keycloak
docker pull jboss/keycloak:latest
docker run -d --rm --name testkc -p 18081:8080 --link testldap:testldap -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -e KEYCLOAK_CONFIG=standalone-test.xml jboss/keycloak:latest
# Lancer sx5_sp_config
docker pull nexus3.inspq.qc.ca:5000/inspq/sx5-sp-config:latest
docker run -d --rm --name sx5spconfig -p 18182:8080 --link testkc:testkc -e KEYCLOAK_URL=http://testkc:8080 -e KEYCLOAK_ENABLED=false nexus3.inspq.qc.ca:5000/inspq/sx5-sp-config:latest
### sx5_sp_config peut aussi être lancé en mode debug et journaliser dans Graylog avec les options suivantes
-e DEBUG_PORT=*:8001
-e GRAYLOG_HOST_BASE=sx5spconfig
-e LOG4J2_GRAYLOG_PORT_GELF_UDP=12231
-e LOG4J2_GRAYLOG_URL=172.17.0.1

# Pour arrêter et supprimer les conteneurs, lancer la commande docker suivante
docker stop sx5spconfig testkc testldap
"""

import requests
import os

from ansible.modules.identity.sx5 import sx5_sp_config_system
from ansible.modules.identity.keycloak import keycloak_client
from ansible.module_utils.sx5_sp_config_system_utils import loginAndSetHeaders
from units.modules.utils import AnsibleExitJson, ModuleTestCase, set_module_args

KC_URL = "http://localhost"
SP_URL = KC_URL
KC_PORT = int(os.environ['KC_PORT']) if 'KC_PORT' in os.environ else 18081
SP_PORT = int(os.environ['SP_PORT']) if 'SP_PORT' in os.environ else 18182
AUTH_URL = "{url}:{port}".format(url = KC_URL, port = KC_PORT)
SP_CONFIG_URL = "{url}:{port}/config".format(url = SP_URL, port = SP_PORT)

class Sx5SystemTestCase(ModuleTestCase):
    systemsToCreate = [
        {
            "spUrl": AUTH_URL,
            "spUsername": "admin",
            "spPassword": "admin",
            "spRealm": "master",
            "spConfigUrl": SP_CONFIG_URL,
            "systemName": "Gestion des habilitations",
            "systemShortName": "sx5habilitation",
            "clients": [
                {"clientId": "sx5habilitationservices"},
                {"clientId": "sx5habilitationui"}
            ],
            "clientRoles": [
                {
                    "spClientRoleId": "sx5-pilote-sx5habilitation",
                    "spClientRoleName": "sx5-pilote-sx5habilitation",
                    "spClientRoleDescription": "Pilote de système de Gestion des habilitations"
                    }
            ],
            "state": "present",
            "force": False
        },
        {
            "spUrl": AUTH_URL,
            "spUsername": "admin",
            "spPassword": "admin",
            "spRealm": "master",
            "spConfigClient_id": "sx5spconfig", 
            "spConfigClient_secret": "",
            "spConfigUrl": SP_CONFIG_URL,
            "systemName": "SystemeAReconfigurer",
            "systemShortName": "SAR",
            "clients": [
                {
                    "clientId": "clientasupprimer"
                }
            ],
            "sadu_principal": "http://sadu.system.a.reconfiguer",
            "sadu_secondary": [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}],
            "clientRoles_mapper": [
                {
                    "spClientRole": "roleInSp11",
                    "eq_sadu_role": "roleSadu11"
                },
                {
                    "spClientRole": "roleInSp12",
                    "eq_sadu_role": "roleSadu12"
                }
            ],
            "clientRoles": [
                {
                    "spClientRoleId": "test1",
                    "spClientRoleName": "test1",
                    "spClientRoleDescription": "test1"
                },
                {
                    "spClientRoleId": "toCreate",
                    "spClientRoleName": "toCreate",
                    "spClientRoleDescription": "toCreate"
                }
            ],
            "state": "present",
            "force": False
        }
    ]
    clientTemplate = {
        "auth_keycloak_url": AUTH_URL + "/auth",
        "auth_username": "admin",
        "auth_password": "admin",
        "realm": "master",
        "state": "present",
        "rootUrl": "http://test.com:18186",
        "description": "Ceci est un test",
        "adminUrl": "http://test.com:18186/admin",
        "enabled": True,
        "clientAuthenticatorType": "client-secret",
        "redirectUris": ["http://test.com:18186/secure","http://test1.com:18186/secure"],
        "webOrigins": ["*"],
        "bearerOnly": False,
        "publicClient": False,
        "force": False
        }
    spConfigClient = {
        "clientId": "sx5spconfig",
        "name": "sx5spconfig",
        "roles": [
            {"name":"sp-lecture","description": "Rôle de lecture pour sx5-sp-config","composite": "False"},
            {
                "name":"sp-configuration",
                "description": "Rôle de config pour sx5-sp-config",
                "composite": True,
                "composites": [{"id": "sx5spconfig","name": "sp-lecture"}]}
            ]
        }
    
    clientsToCreate = [
        {
            "clientId": "sx5habilitationui",
            "name": "IW de SX5-HABILITATION",
            "description": "Interface Web d'habilitation des utilisateurs de SX5",
            "roles": [
                {
                    "name":"sx5-habilitation-utilisateur",
                    "description": "Utilisateur de Gestion des habilitations",
                    "composite": "False"
                    },
                {
                    "name":"sx5-habilitation-superadmin",
                    "description": "Super administrateur de Gestion des habilitations",
                    "composite": True,
                    "composites": [
                        {
                            "id": "sx5habilitationui",
                            "name": "sx5-habilitation-utilisateur"
                            }
                        ]
                    },
                {
                    "name":"sx5-pilote-sx5habilitation",
                    "description": "Pilote de système de Gestion des habilitations",
                    "composite": True,
                    "composites": [
                        {
                            "id": "sx5habilitationui",
                            "name": "sx5-habilitation-utilisateur"
                            }
                        ]
                    }                
                ]
            },
        {
            "clientId": "sx5habilitationservices",
            "name": "API REST SX5-HABILITATION ",
            "description": "API rest d'habilitation des utilisateurs de SX5",
            "bearerOnly": True,
            "roles": [
                {
                    "name":"sx5-habilitation-utilisateur",
                    "description": "Utilisateur de Gestion des habilitations",
                    "composite": "False"
                    },
                {
                    "name":"sx5-habilitation-superadmin",
                    "description": "Super administrateur de Gestion des habilitations",
                    "composite": True,
                    "composites": [
                        {
                            "id": "sx5habilitationservices",
                            "name": "sx5-habilitation-utilisateur"
                            }
                        ]
                    },
                {
                    "name":"sx5-pilote-sx5habilitation",
                    "description": "Pilote de système de Gestion des habilitations",
                    "composite": True,
                    "composites": [
                        {
                            "id": "sx5habilitationservices",
                            "name": "sx5-habilitation-utilisateur"
                            }
                        ]
                    }                
                ]
            },
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
                         {"name":"toDoNotChange","description": "toDoNotChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystem31",
            "name": "clientsystem31",
            "roles": [{"name":"test31","description": "test31","composite": "False"},
                         {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystemChange31",
            "name": "clientsystemChange31",
            "roles": [{"name":"test31","description": "test31","composite": "False"},
                         {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystem32",
            "name": "clientsystem32",
            "roles": [{"name":"test32","description": "test32","composite": "False"},
                         {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystemChange32",
            "name": "clientsystemChange32",
            "roles": [{"name":"test32","description": "test32","composite": "False"},
                         {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystemNS1",
            "name": "clientsystemNS1",
            "roles": [{"name":"testNS1","description": "testNS1","composite": "False"},
                         {"name":"toCreate","description": "toCreate","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        
        {
            "clientId": "clientsystemNS21",
            "name": "clientsystemNS21",
            "roles": [{"name":"testNS2","description": "testNS2","composite": "False"},
                         {"name":"toDoNotChange","description": "toDoNotChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystemNS31",
            "name": "clientsystemNS31",
            "roles": [{"name":"testNS31","description": "testNS31","composite": "False"},
                         {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystemChangeNS31",
            "name": "clientsystemChangeNS31",
            "roles": [{"name":"testNS31","description": "testNS31","composite": "False"},
                         {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystemNS32",
            "name": "clientsystemNS32",
            "roles": [{"name":"testNS32","description": "testNS32","composite": "False"},
                         {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystemChangeNS32",
            "name": "clientsystemChangeNS32",
            "roles": [{"name":"testNS32","description": "testNS32","composite": "False"},
                         {"name":"toChange","description": "toChange","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientsystem41",
            "name": "clientsystem41",
            "roles": [{"name":"test4","description": "test4","composite": "False"},
                         {"name":"toDelete","description": "toDelete","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                         ]
            },
        {
            "clientId": "clientasupprimer",
            "name": "clientasupprimer",
            "roles": [{"name":"test1","description": "test1","composite": "False"}]
            },
        {
            "clientId": "clientarecreer",
            "name": "clientarecreer",
            "roles": [{"name":"test1","description": "test1","composite": "False"}]
            },
        {
            "clientId": "habilitationClient6",
            "name": "habilitationClient6",
            "roles": [{"name":"HPilot1","description": "HPilot1","composite": "False"},
                      {"name":"HPilot2","description": "HPilot2","composite": True,"composites": [{"id": "master-realm","name": "view-users"}]}
                ]
            }, 
        ]
    clientsToDelete = [
        {
            "clientId": "clientasupprimer"
        }
    ]
    def setUp(self):
        super(Sx5SystemTestCase, self).setUp()
        toCreateClient = self.clientTemplate.copy()
        module = keycloak_client
        # Créer le client pour spconfig
        toCreateClient['clientId'] = self.spConfigClient['clientId']
        toCreateClient["name"] = self.spConfigClient["name"]
        toCreateClient["roles"] = self.spConfigClient["roles"]
        set_module_args(toCreateClient)
        with self.assertRaises(AnsibleExitJson) as results:
            module.main()
        self.spConfigClient['clientSecret'] = results.exception.args[0]['clientSecret']['value']
        # Créer les autres clients
        for theClient in self.clientsToCreate:
            toCreateClient["clientId"] = theClient["clientId"]
            toCreateClient["name"] = theClient["name"]
            if 'bearerOnly' in theClient:
                toCreateClient['bearerOnly'] = theClient['bearerOnly']
            if 'description' in theClient:
                toCreateClient['description'] = theClient['description']
            toCreateClient["roles"] = theClient["roles"]
            set_module_args(toCreateClient)
            with self.assertRaises(AnsibleExitJson) as results:
                module.main()
        for systeme in self.systemsToCreate:
            self.system(systeme)
        toDeleteClient = self.clientTemplate.copy()
        toDeleteClient["state"] = "absent"
        for theClient in self.clientsToDelete:
            toDeleteClient["clientId"] = theClient["clientId"]
            set_module_args(toDeleteClient)
            with self.assertRaises(AnsibleExitJson) as results:
                module.main()

    def tearDown(self):
        for systeme in self.systemsToCreate:
            systemCleanup = systeme.copy()
            systemCleanup["state"] = "absent"
            self.system(systemCleanup)
        module = keycloak_client
        toDeleteClient = self.clientTemplate.copy()
        toDeleteClient["state"] = "absent"
        for theClient in self.clientsToCreate:
            toDeleteClient["clientId"] = theClient["clientId"]
            set_module_args(toDeleteClient)
            with self.assertRaises(AnsibleExitJson) as results:
                module.main()
        # Supprimer client spconfig
        toDeleteClient["clientId"] = self.spConfigClient['clientId']
        set_module_args(toDeleteClient)
        with self.assertRaises(AnsibleExitJson) as results:
            module.main()
            
        super(Sx5SystemTestCase, self).tearDown()

    def system(self, params):
        self.module = sx5_sp_config_system
        params['spConfigClient_id'] = self.spConfigClient['clientId']
        params['spConfigClient_secret'] = self.spConfigClient['clientSecret']
        set_module_args(params)
        with self.assertRaises(AnsibleExitJson) as results:
            self.module.main()
        return results.exception.args[0]
        #spConfigSystem = SpConfigSystem(params)
        #spConfigSystem.run()
                        
    def test_create_system(self):
        toCreate = {}
        toCreate["spUrl"] = AUTH_URL
        toCreate["spUsername"] = "admin"
        toCreate["spPassword"] = "admin"
        toCreate["spRealm"] = "master"
        toCreate["spConfigClient_id"] = "sx5spconfig" 
        toCreate["spConfigClient_secret"] = ""
        toCreate["spConfigUrl"] = SP_CONFIG_URL
        toCreate["systemName"] = "system1"
        toCreate["systemShortName"] = "S1"
        toCreate["clients"] = [{"clientId": "clientsystem11"}]
        toCreate["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toCreate["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toCreate["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toCreate["clientRoles"] = [{"spClientRoleId": "test1", "spClientRoleName": "test1", "spClientRoleDescription": "test1"},{"spClientRoleId": "toCreate", "spClientRoleName": "toCreate", "spClientRoleDescription": "toCreate"}]
        toCreate["pilotRoles"] = [{"habilitationClientId": "sx5habilitationservices", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        toCreate["state"] = "present"
        toCreate["force"] = False
    
        results = self.system(toCreate)
        self.assertTrue(results['changed'])
        self.assertEquals(results["diff"]["after"]["Creation-system-sp-config"]["nom"],
                          toCreate["systemName"],
                          "systemName: " + results["diff"]["after"]["Creation-system-sp-config"]["nom"] + " : " + toCreate["systemName"])
        
    def test_system_not_changed(self):
        toDoNotChange = {}
        toDoNotChange["spUrl"] = AUTH_URL
        toDoNotChange["spUsername"] = "admin"
        toDoNotChange["spPassword"] = "admin"
        toDoNotChange["spRealm"] = "master"
        toDoNotChange["spConfigClient_id"] = "sx5spconfig" 
        toDoNotChange["spConfigClient_secret"] = ""
        toDoNotChange["spConfigUrl"] = SP_CONFIG_URL
        toDoNotChange["systemName"] = "system2"
        toDoNotChange["systemShortName"] = "S2"
        toDoNotChange["clients"] = [{"clientId": "clientsystem21"}]
        toDoNotChange["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toDoNotChange["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toDoNotChange["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toDoNotChange["clientRoles"] = [{"spClientRoleId": "test2", "spClientRoleName": "test2", "spClientRoleDescription": "test2"},{"spClientRoleId": "toDoNotChange", "spClientRoleName": "toDoNotChange", "spClientRoleDescription": "toDoNotChange"}]
        toDoNotChange["pilotRoles"] = [{"habilitationClientId": "sx5habilitationservices", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem21", "name": "test2"}], "state": "present"}]}]
        toDoNotChange["state"] = "present"
        toDoNotChange["force"] = False

        self.system(toDoNotChange)
        results = self.system(toDoNotChange)
        self.assertFalse(results['changed'])

    def test_modify_system_no_pilotRoles(self):
        toChange1 = {}
        toChange1["spUrl"] = AUTH_URL
        toChange1["spUsername"] = "admin"
        toChange1["spPassword"] = "admin"
        toChange1["spRealm"] = "master"
        toChange1["spConfigClient_id"] = "admin-cli" 
        toChange1["spConfigClient_secret"] = ""
        toChange1["spConfigUrl"] = SP_CONFIG_URL
        toChange1["systemName"] = "system3"
        toChange1["systemShortName"] = "S3"
        toChange1["clients"] = [{"clientId": "clientsystem31"}]
        toChange1["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toChange1["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toChange1["clientRoles_mapper"] = [
            {
                "spClientRole": "test31",
                "eq_sadu_role": "roleSadu11"
                },
            {
                "spClientRole": "toChange", 
                "eq_sadu_role": "roleSadu12"
                }
        ]
        toChange1["clientRoles"] = [
            {
                "spClientRoleId": "test31", 
                "spClientRoleName": "test31", 
                "spClientRoleDescription": "test31"
                },
            {
                "spClientRoleId": "toChange", 
                "spClientRoleName": "toChange", 
                "spClientRoleDescription": "toChange"
                }
            ]
        toChange1["state"] = "present"
        toChange1["force"] = False

        self.system(toChange1)
        toChange1["sadu_principal"] = "http://localhost/test3"
        toChange1["clients"] = [{"clientId": "clientsystemChange31"}]
        NnClient=len(toChange1["clients"])+1
        results = self.system(toChange1)
        self.assertTrue(results['changed'])
        for adressesApprovisionnement in results["diff"]["after"]["Mise-a-jour-adresse-appro"]["entreesAdressesApprovisionnement"]:
            if adressesApprovisionnement["principale"]:
                self.assertEquals(adressesApprovisionnement["adresse"], toChange1["sadu_principal"], "sadu_principal: " + adressesApprovisionnement["adresse"] + " : " + toChange1["sadu_principal"])
        
        self.assertEquals(len(results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"]), 
                          NnClient, 
                          str(len(results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"])) + " : " + str(NnClient))

    def test_modify_system_with_pilotRoles(self):
        toChangep = {}
        toChangep["spUrl"] = AUTH_URL
        toChangep["spUsername"] = "admin"
        toChangep["spPassword"] = "admin"
        toChangep["spRealm"] = "master"
        toChangep["spConfigClient_id"] = "admin-cli" 
        toChangep["spConfigClient_secret"] = ""
        toChangep["spConfigUrl"] = SP_CONFIG_URL
        toChangep["systemName"] = "system3"
        toChangep["systemShortName"] = "S3"
        toChangep["clients"] = [{"clientId": "clientsystem31"}]
        toChangep["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toChangep["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toChangep["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toChangep["clientRoles"] = [{"spClientRoleId": "test31", "spClientRoleName": "test31", "spClientRoleDescription": "test31"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChangep["pilotRoles"] = [{"habilitationClientId": "sx5habilitationservices", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        toChangep["state"] = "present"
        toChangep["force"] = False

        self.system(toChangep)
        toChangep["sadu_principal"] = "http://localhost/test3"
        toChangep["clients"] = [{"clientId": "clientsystemChange31"}]
        NnClient=len(toChangep["clients"])+1
        results = self.system(toChangep)
        self.assertTrue(results['changed'])
        for adressesApprovisionnement in results["diff"]["after"]["Mise-a-jour-adresse-appro"]["entreesAdressesApprovisionnement"]:
            if adressesApprovisionnement["principale"]:
                self.assertEquals(adressesApprovisionnement["adresse"], toChangep["sadu_principal"], "sadu_principal: " + adressesApprovisionnement["adresse"] + " : " + toChangep["sadu_principal"])
        
        self.assertEquals(len(results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"]), 
                          NnClient, 
                          str(len(results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"])) + " : " + str(NnClient))

    def test_modify_system_add_clients(self):
        toChange2 = {}
        toChange2["spUrl"] = AUTH_URL
        toChange2["spUsername"] = "admin"
        toChange2["spPassword"] = "admin"
        toChange2["spRealm"] = "master"
        toChange2["spConfigClient_id"] = "admin-cli" 
        toChange2["spConfigClient_secret"] = ""
        toChange2["spConfigUrl"] = SP_CONFIG_URL
        toChange2["systemName"] = "test3"
        toChange2["systemShortName"] = "T3"
        toChange2["clients"] = [{"clientId": "clientsystem32"}]
        toChange2["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toChange2["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toChange2["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toChange2["clientRoles"] = [{"spClientRoleId": "test32", "spClientRoleName": "test32", "spClientRoleDescription": "test32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChange2["pilotRoles"] = [{"habilitationClientId": "sx5habilitationservices", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        toChange2["state"] = "present"
        toChange2["force"] = False

        self.system(toChange2)

        newToChange = {}
        newToChange["spUrl"] = AUTH_URL
        newToChange["spUsername"] = "admin"
        newToChange["spPassword"] = "admin"
        newToChange["spRealm"] = "master"
        newToChange["spConfigClient_id"] = "admin-cli" 
        newToChange["spConfigClient_secret"] = ""
        newToChange["spConfigUrl"] = SP_CONFIG_URL
        newToChange["systemName"] = "test3"
        newToChange["systemShortName"] = "T3"
        newToChange["clients"] = [{"clientId": "clientsystemChange32"}]
        newToChange["sadu_principal"] = "http://sadu_principal"
        newToChange["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        newToChange["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        newToChange["clientRoles"] = [{"spClientRoleId": "test32", "spClientRoleName": "test32", "spClientRoleDescription": "test32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        newToChange["pilotRoles"] = [{"habilitationClientId": "sx5habilitationservices", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "present"}]}]
        newToChange["state"] = "present"
        newToChange["force"] = False

        results = self.system(newToChange)
        self.assertTrue(results['changed'])
        systemClients = results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"]
        for toChangeClient in toChange2["clients"]:
            clientFound = False
            for systemClient in systemClients:
                if toChangeClient["clientId"] == systemClient["clientId"]:
                    clientFound = True
                    break
            self.assertTrue(clientFound, toChangeClient["clientId"] + " not found")
        for newToChangeClient in newToChange["clients"]:
            clientFound = False
            for systemClient in systemClients:
                if newToChangeClient["clientId"] == systemClient["clientId"]:
                    clientFound = True
                    break
            self.assertTrue(clientFound, newToChangeClient["clientId"] + " not found")
    
    def test_modify_system_habilitation_clients(self):
        toCreate1 = {}
        toCreate1["spUrl"] = AUTH_URL
        toCreate1["spUsername"] = "admin"
        toCreate1["spPassword"] = "admin"
        toCreate1["spRealm"] = "master"
        toCreate1['spConfigClient_id'] = self.spConfigClient['clientId']
        toCreate1['spConfigClient_secret'] = self.spConfigClient['clientSecret']
        toCreate1["spConfigUrl"] = SP_CONFIG_URL
        toCreate1["systemName"] = "testH"
        toCreate1["systemShortName"] = "TH"
        toCreate1["clients"] = [{"clientId": "habilitationClient6"}]
        toCreate1["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toCreate1["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toCreate1["clientRoles_mapper"] = [
            {
                "spClientRole": "HPilot1",
                "eq_sadu_role": "roleSadu11"
                }
            ]
        toCreate1["clientRoles"] = [
            {
                "spClientRoleId": "HPilot1",
                "spClientRoleName": "HPilot1",
                "spClientRoleDescription": "HPilot1"
                }
            ]
        NnClient=len(toCreate1["clientRoles"])
        toCreate1["pilotRoles"] = [
            {
                "habilitationClientId": "sx5habilitationservices", 
                "roles": [
                    {
                        "name": "pilot-system1",
                        "description": "Role1",
                        "composite": True,
                        "composites": [
                            {
                                "id": "clientsystem11", 
                                "name": "test1"}
                            ],
                        "state": "present"
                        }
                    ]
                }
            ]
        toCreate1["state"] = "present"
        toCreate1["force"] = False
        
        self.system(toCreate1)

        headers = loginAndSetHeaders(toCreate1["spUrl"], toCreate1["spRealm"], toCreate1["spUsername"], toCreate1["spPassword"], toCreate1["spConfigClient_id"], toCreate1["spConfigClient_secret"])
        getResponse = requests.get(toCreate1["spConfigUrl"]+"/systemes/"+toCreate1["systemShortName"], headers=headers)
        dataResponse = getResponse.json()
        self.assertEquals(len(dataResponse["composants"][0]["roles"]),NnClient,str(len(dataResponse["composants"][0]["roles"])) + " : " + str(NnClient))

        newRole = {
            "spClientRoleId": "HPilot2",
            "spClientRoleName": "HPilot2",
            "spClientRoleDescription": "HPilot2"
            }
        toCreate1["clientRoles"].append(newRole)
        NnClient=len(toCreate1["clientRoles"])
        self.system(toCreate1)

        headers = loginAndSetHeaders(toCreate1["spUrl"], toCreate1["spRealm"], toCreate1["spUsername"], toCreate1["spPassword"], toCreate1["spConfigClient_id"], toCreate1["spConfigClient_secret"])
        getResponse = requests.get(toCreate1["spConfigUrl"]+"/systemes/"+toCreate1["systemShortName"], headers=headers)
        dataResponse = getResponse.json()
        self.assertEquals(len(dataResponse["composants"][0]["roles"]),NnClient,str(len(dataResponse["composants"][0]["roles"])) + " : " + str(NnClient))


    def test_create_system_no_sadu(self):
        toCreate = {}
        toCreate["spUrl"] = AUTH_URL
        toCreate["spUsername"] = "admin"
        toCreate["spPassword"] = "admin"
        toCreate["spRealm"] = "master"
        toCreate["spConfigClient_id"] = "admin-cli" 
        toCreate["spConfigClient_secret"] = ""
        toCreate["spConfigUrl"] = SP_CONFIG_URL
        toCreate["systemName"] = "systemNS1"
        toCreate["systemShortName"] = "NS1"
        toCreate["clients"] = [{"clientId": "clientsystemNS1"}]
        toCreate["clientRoles"] = [{"spClientRoleId": "testNS1", "spClientRoleName": "testNS1", "spClientRoleDescription": "testNS1"},{"spClientRoleId": "toCreate", "spClientRoleName": "toCreate", "spClientRoleDescription": "toCreate"}]
        toCreate["state"] = "present"
        toCreate["force"] = False
    
        results = self.system(toCreate)
        self.assertTrue(results['changed'])
        self.assertEquals(results["diff"]["after"]["Creation-system-sp-config"]["nom"],
                          toCreate["systemName"],
                          "systemName: " + results["diff"]["after"]["Creation-system-sp-config"]["nom"] + " : " + toCreate["systemName"])

    def test_system_no_sadu_not_changed(self):
        toDoNotChange = {}
        toDoNotChange["spUrl"] = AUTH_URL
        toDoNotChange["spUsername"] = "admin"
        toDoNotChange["spPassword"] = "admin"
        toDoNotChange["spRealm"] = "master"
        toDoNotChange["spConfigClient_id"] = "admin-cli" 
        toDoNotChange["spConfigClient_secret"] = ""
        toDoNotChange["spConfigUrl"] = SP_CONFIG_URL
        toDoNotChange["systemName"] = "systemNS2"
        toDoNotChange["systemShortName"] = "SNS2"
        toDoNotChange["clients"] = [{"clientId": "clientsystemNS21"}]
        toDoNotChange["clientRoles"] = [{"spClientRoleId": "testNS2", "spClientRoleName": "testNS2", "spClientRoleDescription": "testNS2"},{"spClientRoleId": "toDoNotChange", "spClientRoleName": "toDoNotChange", "spClientRoleDescription": "toDoNotChange"}]
        toDoNotChange["state"] = "present"
        toDoNotChange["force"] = False

        self.system(toDoNotChange)
        results = self.system(toDoNotChange)
        self.assertFalse(results['changed'])

    def test_modify_system_no_sadu(self):
        toChange = {}
        toChange["spUrl"] = AUTH_URL
        toChange["spUsername"] = "admin"
        toChange["spPassword"] = "admin"
        toChange["spRealm"] = "master"
        toChange["spConfigClient_id"] = "admin-cli" 
        toChange["spConfigClient_secret"] = ""
        toChange["spConfigUrl"] = SP_CONFIG_URL
        toChange["systemName"] = "systemNS3"
        toChange["systemShortName"] = "SNS3"
        toChange["clients"] = [{"clientId": "clientsystemNS31"}]
        toChange["clientRoles"] = [{"spClientRoleId": "testNS31", "spClientRoleName": "testNS31", "spClientRoleDescription": "testNS31"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChange["state"] = "present"
        toChange["force"] = False

        self.system(toChange)
        toChange["clients"] = [{"clientId": "clientsystemChangeNS31"}]
        NnClient=len(toChange["clients"])+1
        results = self.system(toChange)
        self.assertTrue(results['changed'])
        self.assertEquals(len(results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"]), 
                          NnClient, 
                          str(len(results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"])) + " : " + str(NnClient))

    def test_modify_system_no_sadu_add_clients(self):
        toChange = {}
        toChange["spUrl"] = AUTH_URL
        toChange["spUsername"] = "admin"
        toChange["spPassword"] = "admin"
        toChange["spRealm"] = "master"
        toChange["spConfigClient_id"] = "admin-cli" 
        toChange["spConfigClient_secret"] = ""
        toChange["spConfigUrl"] = SP_CONFIG_URL
        toChange["systemName"] = "testNS3"
        toChange["systemShortName"] = "TNS3"
        toChange["clients"] = [{"clientId": "clientsystemNS32"}]
        toChange["clientRoles"] = [{"spClientRoleId": "testNS32", "spClientRoleName": "testNS32", "spClientRoleDescription": "testNS32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        toChange["state"] = "present"
        toChange["force"] = False

        self.system(toChange)

        newToChange = {}
        newToChange["spUrl"] = AUTH_URL
        newToChange["spUsername"] = "admin"
        newToChange["spPassword"] = "admin"
        newToChange["spRealm"] = "master"
        newToChange["spConfigClient_id"] = "admin-cli" 
        newToChange["spConfigClient_secret"] = ""
        newToChange["spConfigUrl"] = SP_CONFIG_URL
        newToChange["systemName"] = "testNS3"
        newToChange["systemShortName"] = "TNS3"
        newToChange["clients"] = [{"clientId": "clientsystemChangeNS32"}]
        newToChange["clientRoles"] = [{"spClientRoleId": "testNS32", "spClientRoleName": "testNS32", "spClientRoleDescription": "testNS32"},{"spClientRoleId": "toChange", "spClientRoleName": "toChange", "spClientRoleDescription": "toChange"}]
        newToChange["state"] = "present"
        newToChange["force"] = False

        results = self.system(newToChange)
        self.assertTrue(results['changed'])
        systemClients = results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"]
        for toChangeClient in toChange["clients"]:
            clientFound = False
            for systemClient in systemClients:
                if toChangeClient["clientId"] == systemClient["clientId"]:
                    clientFound = True
                    break
            self.assertTrue(clientFound, toChangeClient["clientId"] + " not found")
        for newToChangeClient in newToChange["clients"]:
            clientFound = False
            for systemClient in systemClients:
                if newToChangeClient["clientId"] == systemClient["clientId"]:
                    clientFound = True
                    break
            self.assertTrue(clientFound, newToChangeClient["clientId"] + " not found")
    def test_delete_system(self):
        toDelete = {}
        toDelete["spUrl"] = AUTH_URL
        toDelete["spUsername"] = "admin"
        toDelete["spPassword"] = "admin"
        toDelete["spRealm"] = "master"
        toDelete["spConfigClient_id"] = "admin-cli" 
        toDelete["spConfigClient_secret"] = ""
        toDelete["spConfigUrl"] = SP_CONFIG_URL
        toDelete["systemName"] = "system4"
        toDelete["systemShortName"] = "S4"
        toDelete["clients"] = [{"clientId": "clientsystem41"}]
        toDelete["sadu_principal"] = "http://sadu.dev.inspq.qc.ca"
        toDelete["sadu_secondary"] = [{"adresse": "http://sadu_secondary1"},{"adresse": "http://sadu_secondary2"}]
        toDelete["clientRoles_mapper"] = [{"spClientRole": "roleInSp11", "eq_sadu_role": "roleSadu11"},{"spClientRole": "roleInSp12", "eq_sadu_role": "roleSadu12"}]
        toDelete["clientRoles"] = [{"spClientRoleId": "test4", "spClientRoleName": "test4", "spClientRoleDescription": "test4"},{"spClientRoleId": "toDelete", "spClientRoleName": "toDelete", "spClientRoleDescription": "toDelete"}]
        toDelete["pilotRoles"] = [{"habilitationClientId": "sx5habilitationservices", "roles": [{"name": "pilot-system1", "description": "Role1", "composite": True, "composites": [{ "id": "clientsystem11", "name": "test1"}], "state": "absent"}]}]
        toDelete["state"] = "present"
        toDelete["force"] = False

        self.system(toDelete)
        toDelete["state"] = "absent"
        results = self.system(toDelete)
        self.assertTrue(results['changed'])
        self.assertTrue(results['diff']['after']['Delete-system'] is None, 'system has not been deleted: {}'.format(str(results['diff']['after']['Delete-system'])))
        
    def test_modify_system_clients_for_components(self):
        toModifySystem = self.systemsToCreate[1].copy()
        toModifySystem["clients"] = [
                {
                    "clientId": "clientarecreer"
                }
            ]
        results = self.system(toModifySystem)
        self.assertTrue(results['changed'])
        systemClients = results["diff"]["after"]["Mise-a-jour-system-sp-config"]["composants"]
        clientFound = False
        for client in systemClients:
            if client["clientId"] == toModifySystem["clients"][0]["clientId"]:
                clientFound = True
                break
        self.assertTrue(clientFound, "Le client " + toModifySystem["clients"][0]["clientId"] + " ne fait pas partie des composants")


