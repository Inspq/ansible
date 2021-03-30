#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2017, INSPQ Team SX5
#
# This file is not part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: sx5_sp_config_system
short_description: Configure a system application in SX5 SP DB
description:
    - This module creates, create or update system application in SX5 SP DB.
version_added: "2.3"
options:
    spUrl:
        description:
            - The url of the Keycloak server. used to check the presence of the client in services provider
        required: true
        type: str
    spUsername:
        description:
            - The username to logon in Keycloak.
        required: true
        type: str
    spPassword:
        description:
            - The password for the user to logon in Keycloak.
        required: true
        type: str
    spAuthRealm:
        description:
            - The Realm for the user to logon in Keycloak.
        required: false
        default: master
        type: str
    spRealm:
        description:
            - The name of the Keycloak realm in which is the client.
        required: true
        type: str
    spConfigUrl:
        description:
            - sx5-config DB REST services URL.
        required: true
        type: str
    spConfigClient_id:
        description:
            - Sx5-sp-Config Client ID.
        required: true
        type: str
    spConfigClient_secret:
        description:
            - Sx5-sp-Config Client Secret.
        required: false
        type: str
    spHabilitationShortName:
        description:
            - System Habilitation Short Name acronym without espace.
        required: false
        default: sx5habilitation
        type: str
    systemShortName:
        description:
            - System Short Name acronym without espace.
        required: true
        type: str
    systemName:
        description:
            - System name of Client ID.
        required: true
        type: str
    clients:
        description:
            - list of OIDC Client ID for the client in Keycloak.
        required: false
        type: list
        elements: dict
    clientRoles:
        description:
            - list of role in keycloak.
        type: list
        required: false
        elements: dict
    sadu_principal:
        description:
            - Principal provisioning services URL.
        type: str
        required: false
    sadu_secondary:
        description:
            - list of secondary provisioning services URL.
        type: list
        required: false
        elements: dict
    clientRoles_mapper:
        description:
            - list of role correspondance between keycloak roles end SADU roles.
        required: false
        type: list
        elements: dict
    pilotRoles:
        description:
            - list of piloting roles in keycloak.
        type: list
        required: false
        elements: dict
    pilotRole:
        description:
            - Name for the piloting role in sx5-habilitation.
            - The value sx5-pilote-{{ systemShortName }} will be assigned
            - to this role if this parameter is not defined
        required: false
        type: str
    pilotSaduRoles:
        description:
            - List of client roles to assign for pilots to be able to provision
            - users when assigning habilitations using SADU.
        required: false
        type: list
        elements : dict
        suboptions:
            id:
                description:
                    - Client ID for SADU.
                type: str
            name:
                description:
                    - The name of the role for SADU provisioning.
                type: str
    force:
        default: "no"
        description:
            - If yes, allows to remove client and recreate it.
        required: false
        type: bool
    graylog_host:
        description:
            - Url for Graylog support.
        required: false
        type: str
    graylog_port_udp:
        default: 12300
        description:
            - UDP port for Graylog support.
        required: false
        type: int
    state:
        description:
            - Control if the client must exists or not
        choices: [ "present", "absent" ]
        default: present
        required: false
        type: str
notes:
    - module does not modify clientId in keycloak.
author:
    - INSPQ SX5 Team (@moi8407)
'''

EXAMPLES = '''
    - name: Create a system system1 with default settings.
      sx5_sp_config_system:
        spUrl: http://localhost:8080/auth
        spUsername: admin
        spPassword: admin
        spAuthRealm: master
        spRealm: master
        graylog_host: tcn00qubc02216.isn.rtss.qc.ca
        graylog_port_udp: 12300
        spConfigUrl: http://localhost:8089/config
        spConfigClient_id: sx5spconfig
        spConfigClient_secret: client_string
        spHabilitationShortName: sx5habilitation
        systemName: system1
        systemShortName: S1
        sadu_principal: http://localhost:8088/sadu1
        sadu_secondary:
        - adresse: http://localhost:8088/sadu2
        - adresse: http://localhost:8088/sadu3
        clients:
        - clientId: client1
        - clientId: client2
        clientRoles_mapper:
        - spClientRole: roleInSp1
          eq_sadu_role: roleSadu1
        - spClientRole: roleInSp2
          eq_sadu_role: roleSadu2
        clientRoles:
        - spClientRoleId: roleId1
          spClientRoleName: roleName1
          spClientRoleDescription: roleDescription1
        - spClientRoleId: roleId2
          spClientRoleName: roleName2
          spClientRoleDescription: roleDescription2
        pilotRoles:
        - habilitationClientId: habilitationClient1
          roles:
          - name: "rolesName"
            description: "Role1"
            composite: true
            composites:
              - id: existinqClient
                name: role1ofclient
            state: present
        - habilitationClientId: habilitationClient2
          roles:
          - name: "rolesName"
            description: "Role2"
            composite: true
            composites:
              - id: existinqClient
                name: role1ofclient
            state: present
        state: present

    - name: Re-create a system system1 with default settings.
      sx5_sp_config_system:
        spUrl: http://localhost:8080/auth
        spUsername: admin
        spPassword: admin
        spRealm: Master
        spConfigUrl: http://localhost:8089/config
        spConfigClient_id: sx5spconfig
        spConfigClient_secret: client_string
        systemName: system1
        systemShortName: S1
        sadu_principal: http://localhost:8088/sadu1
        sadu_secondary:
        - adresse: http://localhost:8088/sadu2
        - adresse: http://localhost:8088/sadu3
        clients:
        - clientId: client1
        - clientId: client2
        clientRoles_mapper:
        - spClientRole: roleInSp1
          eq_sadu_role: roleSadu1
        - spClientRole: roleInSp2
          eq_sadu_role: roleSadu2
        clientRoles:
        - spClientRoleId: roleId1
          spClientRoleName: roleName1
          spClientRoleDescription: roleDescription1
        - spClientRoleId: roleId2
          spClientRoleName: roleName2
          spClientRoleDescription: roleDescription2
        pilotRole: pilote-system1
        pilotSaduRoles:
        - id: sadu_clientid 
          name: sadu_client_role
        state: present
        force: yes

    - name: Remove system1.
      sx5_sp_config_system:
        spUrl: http://localhost:8080/auth
        spUsername: admin
        spPassword: admin
        spRealm: Master
        spConfigUrl: http://localhost:8089/config
        spConfigClient_id: sx5spconfig
        spConfigClient_secret: client_string
        systemName: system1
        systemShortName: S1
        sadu_principal: http://localhost:8088/sadu1
        state: absent
'''
RETURN = '''
ansible_facts:
  description: JSON representation for the system.
  returned: on success
  type: dict
stderr:
  description: Error message if it is the case
  returned: on error
  type: str
rc:
  description: return code, 0 if success, 1 otherwise.
  returned: always
  type: bool
changed:
  description: Return True if the operation changed the system on the SX5 DB, false otherwise.
  returned: always
  type: bool
'''

from ansible.module_utils.identity.keycloak.keycloak import (KeycloakAPI,
                                                             get_token,
                                                             isDictEquals)
from ansible.module_utils.basic import AnsibleModule
import requests
import sys
import os
import logging
import json
import copy


try:
    from pygelf import GelfUdpHandler
    gelf = True
except ImportError:
    gelf = False
logger = logging.getLogger('sx5-sp-config-system')

ROLES = {
    'PILOTE_HABILITATION': {
        'NAME': 'sx5-pilote-sx5habilitation',
        'DESC': 'Pilote de système de Gestion des habilitations'
    },
    'SUPERADMIN_HABILITATION': {
        'NAME': 'sx5-habilitation-superadmin',
        'DESC': 'Super administrateur de Gestion des habilitations'
    },
    'UTILISATEUR_HABILITATION': {
        'NAME': 'sx5-habilitation-utilisateur'
    },
    'SYSTEM_HABILITATION': {
        'DESC': 'Rôle de pilotage {sysname}'
    }
}


def main():
    pilot_sadu_roles_options = dict(
        id=dict(type='str'),
        name=dict(type='str'))
    module = AnsibleModule(
        argument_spec=dict(
            spUrl=dict(type='str', required=True),
            spUsername=dict(type='str', required=True),
            spPassword=dict(required=True),
            spAuthRealm=dict(type='str', required=False, default='master'),
            spRealm=dict(type='str', required=True),
            spConfigUrl=dict(type='str', required=True),
            spConfigClient_id=dict(type='str', required=True),
            spConfigClient_secret=dict(type='str', required=False),
            spHabilitationShortName=dict(
                type='str', required=False, default='sx5habilitation'),
            systemName=dict(type='str', required=True),
            systemShortName=dict(type='str', required=True),
            sadu_principal=dict(type='str', required=False),
            sadu_secondary=dict(type='list', elements='dict', default=[]),
            clients=dict(type='list', elements='dict', default=[]),
            clientRoles=dict(type='list', elements='dict', default=[]),
            pilotRoles=dict(type='list', elements='dict', default=[]),
            pilotRole=dict(type='str', required=False),
            clientRoles_mapper=dict(type='list', elements='dict', default=[]),
            pilotSaduRoles=dict(type='list', elements='dict', default=[], options=pilot_sadu_roles_options),
            force=dict(type='bool', default=False),
            state=dict(choices=["absent", "present"], default='present'),
            graylog_host=dict(type='str', default=''),
            graylog_port_udp=dict(type='int', default=12300)
        ),
        supports_check_mode=True,
    )

    try:
        params = completParams(module)
        if os.name == 'nt':
            logging.basicConfig(level=logging.DEBUG)
        elif module._verbosity == 4:
            logging.basicConfig(level=logging.DEBUG)
        elif module._verbosity in [2, 3]:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)
        logger.addFilter(JsonFilter())
        if gelf and params['graylog_host'] != '':
            logger.addHandler(
                GelfUdpHandler(
                    host=params['graylog_host'],
                    port=params['graylog_port_udp'],
                    debug=True,
                    include_extra_fields=True))
            logger.warning(
                'Allo gelf from sx5-sp-config-system, logging lvl : %s',
                logger.getEffectiveLevel())
        spConfig = SpConfigSystem(params)
        result = spConfig.run()
    except Exception as e:
        result = dict(
            stderr=str(e),
            rc=1,
            changed=False
        )
        logger.exception(e)

    if result['rc'] != 0:
        module.fail_json(msg='non-zero return code', **result)
    else:
        module.exit_json(**result)


def completParams(module):
    params = module.params.copy()
    params['spUrl'] = params['spUrl'].rstrip('/')
    params['spConfigUrl'] = params['spConfigUrl'].rstrip('/')
    params['force'] = module.boolean(module.params['force'])
    if not ('spAuthRealm' in params):
        params['spAuthRealm'] = params["spRealm"]
    if not (
            "spConfigClient_secret" in params) or params['spConfigClient_secret'] is None:
        params['spConfigClient_secret'] = ''
    if 'pilotRole' not in params or params['pilotRole'] is None or params['pilotRole'] == '':
        params['pilotRole'] = 'sx5-pilote-' + params["systemShortName"]
    if 'spHabilitationShortName' not in params or params['spHabilitationShortName'] is None or len(
            params['spHabilitationShortName']) == 0:
        params['spHabilitationShortName'] = 'sx5habilitation'
    return params


class SpConfigSystemError(Exception):
    pass


class JsonFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, dict) or isinstance(record.msg, list):
            try:
                record.msg = json.dumps(record.msg, indent=2)
            except BaseException:
                pass
        return True


class MockModule(object):
    def __init__(self, params):
        self.params = dict()
        self.params['auth_keycloak_url'] = params['spUrl'] + "/auth"
        self.params['validate_certs'] = True
        self.params['auth_realm'] = params['spRealm']
        self.params['auth_client_id'] = params['spConfigClient_id']
        self.params['auth_username'] = params['spUsername']
        self.params['auth_password'] = params['spPassword']
        self.params['auth_client_secret'] = params['spConfigClient_secret']

    def fail_json(self, msg, **kwargs):
        raise SpConfigSystemError(msg)


class SpConfigSystem(object):
    def __init__(self, params):
        self.params = params

    def systemDBRepresentation(self):
        params = self.params
        # Creer un representation du system pour BD SP config
        newSystemDBRepresentation = {}
        if "spRealm" in params and params["spRealm"] is not None:
            if sys.version_info.major == 3:
                newSystemDBRepresentation["spRealm"] = params['spRealm']
            else:
                newSystemDBRepresentation["spRealm"] = params['spRealm'].decode(
                    "utf-8")
        if sys.version_info.major == 3:
            newSystemDBRepresentation["systemName"] = params['systemName']
            newSystemDBRepresentation["spConfigUrl"] = params['spConfigUrl']
        else:
            newSystemDBRepresentation["systemName"] = params['systemName'].decode(
                "utf-8")
            newSystemDBRepresentation["spConfigUrl"] = params['spConfigUrl'].decode(
                "utf-8")
        if "systemShortName" in params and params['systemShortName'] is not None:
            newSystemDBRepresentation["systemShortName"] = params['systemShortName']
        if "sadu_principal" in params and params['sadu_principal'] is not None:
            if sys.version_info.major == 3:
                newSystemDBRepresentation["sadu_principal"] = params['sadu_principal']
            else:
                newSystemDBRepresentation["sadu_principal"] = params['sadu_principal'].decode(
                    "utf-8")
        if "sadu_secondary" in params and params['sadu_secondary'] is not None:
            newSystemDBRepresentation["sadu_secondary"] = params['sadu_secondary']
        if "clients" in params and params['clients'] is not None:
            newSystemDBRepresentation["clients"] = params['clients']
        if "clientRoles_mapper" in params and params['clientRoles_mapper'] is not None:
            newSystemDBRepresentation["clientRoles_mapper"] = params['clientRoles_mapper']
        if "clientRoles" in params and params['clientRoles'] is not None:
            newSystemDBRepresentation["clientRoles"] = params['clientRoles']
        if "pilotRoles" in params and params['pilotRoles'] is not None:
            newSystemDBRepresentation["pilotRoles"] = params['pilotRoles']
        if 'pilotRole' not in params or params['pilotRole'] is None or params['pilotRole'] == '':
            newSystemDBRepresentation['pilotRole'] = 'sx5-pilote-' + \
                params["systemShortName"]
        else:
            newSystemDBRepresentation["pilotRole"] = params['pilotRole']
        if 'pilotSaduRoles' in params:
            newSystemDBRepresentation['pilotSaduRoles'] = params['pilotSaduRoles']
        return newSystemDBRepresentation

    def addDiff(self, title, dict1, dict2, result):
        result['changed'] = True
        if 'diff' in result:
            diff = result['diff']
        else:
            diff = {
                'before': {},
                'after': {}
            }
            result['diff'] = diff

        diff['before'][title] = dict2
        diff['after'][title] = dict1

    def addDeprecation(self, msg, result):
        if 'deprecations' in result:
            deprecations = result['deprecations']
        else:
            deprecations = []
            result['deprecations'] = deprecations
        deprecations.append(
            {
                'msg': msg,
                'version:': 'v2.9.4-keycloak-sx5-1'
            }
        )

    def getSystemSpConfig(self, systemShortName):
        if systemShortName == '':
            raise SpConfigSystemError(
                "getSystemSpConfig systemShortName ne peut pas etre vide")
        getResponse = requests.get(
            self.params['spConfigUrl'] + "/systemes/" + systemShortName,
            headers=self.headers
        )
        if getResponse.status_code == 200:
            dataResponse = getResponse.json()
        elif getResponse.status_code == 404:
            dataResponse = None
        else:
            raise SpConfigSystemError(
                "getSystemSpConfig code {code} : {token}".format(
                    code=getResponse.status_code,
                    token=self.headers['Authorization']))
        return dataResponse

    def getKeycloakClient(self, clientId):
        # le client dans kc doit avoir ete cree/modife par une task dans la
        # playbook avant
        clientKc = self.kc.get_client_by_clientid(
            clientId, self.params['spRealm'])
        if clientKc is None:
            raise SpConfigSystemError(
                "getKeycloakClient client absent {clientid}@{realm} : {token}".format(
                    clientid=clientId,
                    realm=self.params['spRealm'],
                    token=self.headers['Authorization']))
        return clientKc

    def addSystemSpConfig(self, result):
        if self.params['force']:
            self.delSystemSpConfig(result, self.params)

        self.addSystemSpConfigBody(result, self.params)
        # il faut creer la representation json des role pour habilitation avant
        # les manipulations pour Kc qui vont changer le clientid pour l'id Kc
        # dans les composantes mais apres l'ajout du systeme, au cas ou le
        # systeme serait habiltation lui-meme
        roleHabilitationRepresentations = self.roleHabilitationRepresentation(
            result)
        if roleHabilitationRepresentations is None:
            roleHabilitationRepresentations = self.roleHabilitationSystemShortName(
                result)
        self.addSystemKeycloakPilotage(result, self.params)
        self.addSystemSpConfigPilotageHabilitation(
            result, roleHabilitationRepresentations)

    def addSystemSpConfigPilotageHabilitation(
            self, result, roleHabilitationRepresentations):
        if roleHabilitationRepresentations is not None:
            self.addSystemSpConfigBody(result, roleHabilitationRepresentations)

    def roleHabilitationSystemShortName(self, result):
        logger.info(
            'Creation representation system pour pilotage par la variable SystemShortName')
        system = self.getSystemSpConfig(self.params['spHabilitationShortName'])
        if system is None:
            raise SpConfigSystemError(
                "System Habilitation({shortname}) absent du realm: {realm}, prerequis, playbook sx5-habilitation".format(
                    shortname=self.params['spHabilitationShortName'],
                    realm=self.params['spRealm']))
        paramHabilitations = self.roleHabilitationSystemRepresentation(system)
        self.roleHabilitationSystemShortNameKeycloak(
            system, paramHabilitations, result)
        self.roleHabilitationSystemShortNameSpConfig(
            system, paramHabilitations, result)
        return paramHabilitations

    def roleHabilitationSystemShortNameKeycloak(
            self, system, paramHabilitations, result):
        if self.params['spHabilitationShortName'] == self.systemRepresentation['systemShortName']:
            self.roleHabilitationSystemShortNameKeycloakHabilitation(
                system, paramHabilitations, result)
        else:
            self.roleHabilitationSystemShortNameKeycloakAutre(
                system, paramHabilitations, result)

    def roleHabilitationSystemShortNameKeycloakHabilitation(
            self, system, paramHabilitations, result):
        logger.info(
            'Generer json pour API KC, client Habilitation: %s',
            self.systemRepresentation['systemShortName'])
        pilotRoles = self.params['pilotRoles']
        for composant in system['composants']:
            roles = []
            rolePilot = {
                'state': 'present',
                'name': ROLES['PILOTE_HABILITATION']['NAME'],
                'description': ROLES['PILOTE_HABILITATION']['DESC']
            }
            
            roleSuperAdmin = {
                'name': ROLES['SUPERADMIN_HABILITATION']['NAME'],
                'description': ROLES['SUPERADMIN_HABILITATION']['DESC'],
                'composite': True,
                'composites': [
                    {
                        'id': composant['clientId'],
                        'name': ROLES['PILOTE_HABILITATION']['NAME']
                    }
                ]
            }
            roles.append(rolePilot)            
            roles.append(roleSuperAdmin)
            pilotRoles.append(
                {
                    'habilitationClientId': composant['clientId'],
                    'roles': roles
                }
            )

    def roleHabilitationSystemShortNameKeycloakAutre(
            self, system, paramHabilitations, result):
        logger.info('Generer json pour API KC: %s',
                    self.systemRepresentation['systemShortName'])
        pilotRoles = self.params['pilotRoles']
        for composant in system['composants']:
            clientRolesForComposant =[]
            rolePiloteSysteme = {
                'description': ROLES['SYSTEM_HABILITATION']['DESC'].format(sysname=self.systemRepresentation['systemName']),
                'name': self.params['pilotRole'],
                'composite': True,
                'composites': [
                    {
                        'id': composant['clientId'],
                        'name': ROLES['UTILISATEUR_HABILITATION']['NAME']
                    }
                ]
            }
            # Si on a des rôles du sadu à attribuer aux roles de pilotages
            if 'pilotSaduRoles' in self.params and self.params['pilotSaduRoles'] is not None:
                for pilotSaduRole in self.params['pilotSaduRoles']:
                    rolePiloteSysteme['composites'].append(pilotSaduRole)
            clientRolesForComposant.append(rolePiloteSysteme)
            roleSuperAdmin = {
                "description": ROLES['SUPERADMIN_HABILITATION']['DESC'],
                "name": ROLES['SUPERADMIN_HABILITATION']['NAME'],
                "composite": True,
                "composites": [
                    {
                        "id": composant['clientId'],
                        "name": self.params['pilotRole']
                    }
                ]
            }
            clientRolesForComposant.append(roleSuperAdmin)
            
            pilotRoles.append(
                {
                    'habilitationClientId': composant['clientId'],
                    'roles': clientRolesForComposant
                }
            )

    def roleHabilitationSystemShortNameSpConfig(
            self, system, paramHabilitations, result):
        # Dans sp-config, tous les clients du systeme habilitation sont
        # identiques, on peut donc prendre le premier pour fusionner les roles,
        # ca change rien
        logger.info('Generer role pour sp-config: %s',
                    self.systemRepresentation['systemShortName'])
        composant = system['composants'][0]
        roles = []
        rolePiloteHabilitation = {
            'state': 'present',
            'name': ROLES['PILOTE_HABILITATION']['NAME'],
            'description': ROLES['PILOTE_HABILITATION']['DESC']
        }
        rolePiloteSysteme = {
            'state': 'present',
            'name': self.params['pilotRole'],
            'description': ROLES['SYSTEM_HABILITATION']['DESC'].format(sysname=self.systemRepresentation['systemName'])
        }
        roleSuperAdmin = {
            'state': 'present',
            'name': ROLES['SUPERADMIN_HABILITATION']['NAME'],
            'description': ROLES['SUPERADMIN_HABILITATION']['DESC']
        }
        roles.append(rolePiloteHabilitation)
        roles.append(roleSuperAdmin)
        # le comportement est different si on creer le system sx5habilitation
        # vs tous les autres
        if self.params['spHabilitationShortName'] != self.systemRepresentation['systemShortName']:
            roles.append(rolePiloteSysteme)

        clientRoles = paramHabilitations['clientRoles']
        self.fusionnerRole(clientRoles, composant['roles'], roles)

    # il faut utilise la reponse de sp-config et la modifer en
    # "ajoutant/mettre a jour" avec le parametre ansible
    def roleHabilitationRepresentation(self, result):
        logger.info('Creation representation system pour pilotage')
        if 'pilotRoles' not in self.systemRepresentation or len(
                self.systemRepresentation['pilotRoles']) == 0:
            logger.info(
                'Aucun representation system pour pilotage, pilotRoles est vide ou absent')
            return None

        self.addDeprecation(
            "**Deprecated**: le parametre 'pilotRoles' est obselet, voir 'pilotRole' pour changer le nom par defaut du role pilote dans habilitation",
            result)

        system = self.getSystemSpConfig(self.params['spHabilitationShortName'])
        if system is None:
            raise SpConfigSystemError(
                "System Habilitation({shortname}) absent {realm}, prerequis, playbook sx5-habilitation".format(
                    shortname=self.params['spHabilitationShortName'],
                    realm=self.params['spRealm']))

        paramHabilitations = self.roleHabilitationSystemRepresentation(system)
        clientRoles = paramHabilitations['clientRoles']
        # Dans sp-config, tous les clients du systeme habilitation sont
        # identiques, on peut donc prendre le premier pour fusionner les roles,
        # ca change rien
        composant = system['composants'][0]
        for pilotRole in self.systemRepresentation['pilotRoles']:
            self.fusionnerRole(
                clientRoles,
                composant['roles'],
                pilotRole['roles'])

        logger.debug(paramHabilitations)
        return paramHabilitations

    def fusionnerRole(self, roles, habilitationRoles, piloteRoles):

        for role in piloteRoles:
            if self.findRecord(roles, 'spClientRoleId', role['name']) is None:
                logger.debug(
                    'Fusion role pilotage via param : %s',
                    role['name'])
                roles.append(
                    {
                        "spClientRoleDescription": role['description'],
                        "spClientRoleId": role['name'],
                        "spClientRoleName": role['name']
                    }
                )

        for role in habilitationRoles:
            if self.findRecord(roles, 'spClientRoleId', role['nom']) is None:
                logger.debug(
                    'Fusion role pilotage via sp-config : %s',
                    role['nom'])
                roles.append(
                    {
                        "spClientRoleDescription": role['description'],
                        "spClientRoleId": role['nom'],
                        "spClientRoleName": role['nom']
                    }
                )

    # creer la representation json d'un system avec les info des roles pilot

    def roleHabilitationSystemRepresentation(self, system):
        # dans sp-config, les composantes sont des clients kc
        clients = []
        for composant in system['composants']:
            clients.append(
                {
                    'clientId': composant['clientId']
                }
            )
        paramHabilitations = {
            "systemName": system['nom'],
            "systemShortName": system['cleUnique'],
            "force": False,
            "clients": clients,
            "clientRoles": []
        }
        return paramHabilitations

    def findRecord(self, jsonArray, key, value):
        for o in jsonArray:
            if o[key] == value:
                return o
        return None

    def addSystemKeycloakPilotage(self, result, params):
        if not ("pilotRoles" in params) or params['pilotRoles'] is None:
            return
        for pilotRole in params["pilotRoles"]:
            # set roles in Keycloak
            self.createOrUpdateClientRoles(
                pilotRole["roles"],
                pilotRole['habilitationClientId'],
                result
            )

    def createOrUpdateClientRoles(
            self, pilotClientRoles, clientHabilitationId, result):
        if pilotClientRoles is None:
            return
        if len(pilotClientRoles) == 0:
            return
        logger.info('Ajoute system Keycloak client : %s', clientHabilitationId)
        logger.debug(pilotClientRoles)
        # Copier la liste des rôles clients dans une structure temporaire
        # car la méthode create_or_update_client_roles peut la polluer
        pilotClientRolesCopy = copy.deepcopy(pilotClientRoles)
        if self.kc.create_or_update_client_roles(
                clientHabilitationId, pilotClientRolesCopy, self.params['spRealm'], False):
            self.addDiff(
                'keycloak',
                'create_or_update_client_roles',
                '',
                result)
            result['changed'] = True

    def addSystemSpConfigBody(self, result, params):
        spConfigUrl = self.params['spConfigUrl']
        spConfigSystem = self.getSystemSpConfig(params['systemShortName'])

        clients = self.clientRepresentation(params, spConfigSystem)
        adresses = self.adresseRepresentation(params)
        rolemappers = self.rolemapperRepresentation(params)

        bodySystem = {
            "nom": params["systemName"],
            "cleUnique": params["systemShortName"],
            "composants": clients
        }
        # on cree/recree le system seulment s'il n'exists pas/plus
        if spConfigSystem is None:
            logger.info('Creation system sp-config : %s', bodySystem['nom'])
            logger.debug(bodySystem)
            self.addDiff('Creation-system-sp-config', bodySystem, None, result)
            spConfigSystem = self.inspectResponse(
                requests.post(
                    spConfigUrl + "/systemes/",
                    headers=self.headers,
                    json=bodySystem
                ), "post systeme", 201
            )
        elif not isDictEquals(bodySystem, spConfigSystem):
            # on met a jour
            logger.info('Mise a jour system sp-config: %s', bodySystem['nom'])
            logger.debug(bodySystem)
            self.addDiff(
                'Mise-a-jour-system-sp-config',
                bodySystem,
                spConfigSystem,
                result)
            spConfigSystem = self.inspectResponse(
                requests.put(
                    spConfigUrl + '/systemes/' + bodySystem['cleUnique'],
                    headers=self.headers,
                    json=bodySystem
                ), "put systeme", 200
            )

        if len(adresses) > 0:
            bodyAdrAppr = {
                "cleUnique": params["systemShortName"],
                "entreesAdressesApprovisionnement": adresses
            }
            spAdrAppr = self.inspectResponse(
                requests.get(
                    spConfigUrl + "/systemes/" +
                    spConfigSystem["cleUnique"] + "/adressesApprovisionnement",
                    headers=self.headers
                ), "get adressesApprovisionnement", 200, 201
            )
            if not isDictEquals(bodyAdrAppr, spAdrAppr):
                logger.info(
                    'Mise a jour adresse approvisionnement sp-config: %s',
                    bodyAdrAppr['cleUnique'])
                logger.debug(bodyAdrAppr)
                self.addDiff(
                    'Mise-a-jour-adresse-appro',
                    bodyAdrAppr,
                    spAdrAppr,
                    result)
                self.inspectResponse(
                    requests.put(
                        spConfigUrl + "/systemes/" +
                        spConfigSystem["cleUnique"] +
                        "/adressesApprovisionnement",
                        headers=self.headers,
                        json=bodyAdrAppr
                    ), "put adressesApprovisionnement", 200, 201
                )

        if len(rolemappers) > 0:
            bodyTableCorrespondance = {
                "cleUnique": params["systemShortName"],
                "entreesTableCorrespondance": rolemappers
            }
            spTableCorrespondance = self.inspectResponse(
                requests.get(
                    spConfigUrl + "/systemes/" +
                    spConfigSystem["cleUnique"] + "/tableCorrespondance",
                    headers=self.headers
                ), "get tableCorrespondance", 200, 201
            )
            if not isDictEquals(bodyTableCorrespondance,
                                spTableCorrespondance):
                logger.info(
                    'Mise a jour role mapper sp-config: %s',
                    bodyTableCorrespondance['cleUnique'])
                logger.debug(bodyTableCorrespondance)
                self.addDiff(
                    'Mise-a-jour-role-mapper',
                    bodyTableCorrespondance,
                    spTableCorrespondance,
                    result)
                self.inspectResponse(
                    requests.put(
                        spConfigUrl + "/systemes/" +
                        spConfigSystem["cleUnique"] + "/tableCorrespondance",
                        headers=self.headers,
                        json=bodyTableCorrespondance
                    ), "put tableCorrespondance", 200, 201
                )

    def inspectResponse(self, response, msg, *codes):
        status = response.status_code
        if status in codes:
            if response.text == '':
                return None
            return response.json()
        try:
            msg = msg + ' - ' + response.text
        except Exception as e:
            pass
        raise SpConfigSystemError("code {code} - {msg} : {token}".format(
            code=status, msg=msg, token=self.headers['Authorization']))

    def clientRepresentation(self, params, spConfigSystem):
        clients = []
        for clientKeycloak in params["clients"]:
            dataResponseKeycloak = self.getKeycloakClient(
                clientKeycloak['clientId'])
            clients.append(
                self.mergeKcClientWithSystemRepresentation(
                    dataResponseKeycloak, params))
        if spConfigSystem is not None:
            # si le system exist deja dans SpConfig, il faut ajouter les autres
            # clients(composants dans SpConfig) qui existaient deja, si non, ca
            # va les supprimer
            for clientSpConfig in spConfigSystem['composants']:
                if self.findRecord(clients, 'clientId',
                                   clientSpConfig['clientId']) is None:
                    clients.append(clientSpConfig)

        return clients

    def rolemapperRepresentation(self, params):
        rolemappers = []
        if "clientRoles_mapper" in params and params['clientRoles_mapper'] is not None:
            for clientRoles_mapper in params["clientRoles_mapper"]:
                role = {
                    "roleKeycloak": clientRoles_mapper["spClientRole"],
                    "roleSysteme": clientRoles_mapper["eq_sadu_role"]
                }
                rolemappers.append(role)
        return rolemappers

    def adresseRepresentation(self, params):
        adresses = []
        if "sadu_principal" in params and params['sadu_principal'] is not None:
            adresse = {
                "principale": True,
                "adresse": params["sadu_principal"]
            }
            adresses.append(adresse)
            if "sadu_secondary" in params and params['sadu_secondary'] is not None:
                for sadu_secondary in params["sadu_secondary"]:
                    adresse = {
                        "principale": False,
                        "adresse": sadu_secondary["adresse"]
                    }
                    adresses.append(adresse)
        return adresses

    def mergeKcClientWithSystemRepresentation(
            self, dataResponseKeycloak, params):
        dataResponseroles = dataResponseKeycloak['clientRoles']
        clientRoles = params["clientRoles"]
        roles = []
        for dataKeycloakrole in dataResponseroles:
            for clientRole in clientRoles:
                if dataKeycloakrole["name"] == clientRole["spClientRoleId"]:
                    role = {
                        "uuidRoleKeycloak": dataKeycloakrole["id"],
                        "nom": clientRole["spClientRoleId"],
                        "description": clientRole["spClientRoleDescription"]
                    }
                    roles.append(role)
        client = {
            "nom": dataResponseKeycloak["name"],
            "uuidKeycloak": dataResponseKeycloak["id"],
            "clientId": dataResponseKeycloak["clientId"],
            "description": dataResponseKeycloak["description"],
            "roles": roles
        }
        return client

    def delSystemSpConfig(self, result, params):
        spConfigSystem = self.getSystemSpConfig(params['systemShortName'])
        if spConfigSystem is not None:
            logger.info('Delete system : ' + params['systemShortName'])
            self.addDiff('Delete-system', None, spConfigSystem, result)
            self.inspectResponse(
                requests.delete(
                    self.params['spConfigUrl'] + "/systemes/" +
                    spConfigSystem["cleUnique"],
                    headers=self.headers
                ), "delSystemSpConfig", 204
            )

    def run(self):
        logger.info('Debug creation systeme sx5-sp-config')
        logger.debug(self.params)
        self.systemRepresentation = self.systemDBRepresentation()
        result = dict(
            ansible_facts=self.systemRepresentation,
            rc=0,
            changed=False
        )

        params = self.params
        auth_realm = params['spAuthRealm'] if 'spAuthRealm' in params else 'master'
        self.headers = get_token(
            base_url=params['spUrl'] + "/auth",
            validate_certs=True,
            auth_realm=auth_realm,
            client_id=params['spConfigClient_id'],
            auth_username=params['spUsername'],
            auth_password=params['spPassword'],
            client_secret=params['spConfigClient_secret']
        )
        logger.debug(self.headers['Authorization'])

        self.kc = KeycloakAPI(MockModule(params), self.headers)
        if params['state'] == 'present':
            self.addSystemSpConfig(result)
        else:
            self.delSystemSpConfig(result=result, params=params)

        logger.info('Fin creation systeme sx5-sp-config')
        logger.info(result)
        return result


if __name__ == '__main__':
    main()
