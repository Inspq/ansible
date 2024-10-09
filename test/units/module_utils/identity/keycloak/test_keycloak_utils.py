import collections
import os
import unittest

from ansible.module_utils.identity.keycloak.keycloak import isDictEquals, remove_arguments_with_value_none
from ansible.module_utils.keycloak_utils import ansible2keycloakClientRoles
from ansible.module_utils.keycloak_utils import keycloak2ansibleClientRoles

class KeycloakIsDictEqualsTestCase(unittest.TestCase):

    dict1 = dict(
        test1 = 'test1',
        test2 = dict(
            test1='test1',
            test2='test2'
            ),
        test3 = ['test1',dict(test='test1',test2='test2')]         
        )
    dict2 = dict(
        test1 = 'test1',
        test2 = dict(
            test1='test1',
            test2='test2',
            test3='test3'
            ),
        test3 = ['test1',dict(test='test1',test2='test2'),'test3'],
        test4 = 'test4'         
        )
    dict3 = dict(
        test1 = 'test1',
        test2 = dict(
            test1='test1',
            test2='test23',
            test3='test3'
            ),
        test3 = ['test1',dict(test='test1',test2='test23'),'test3'],
        test4 = 'test4'         
        )

    dict5 = dict(
        test1 = 'test1',
        test2 = dict(
            test1=True,
            test2='test23',
            test3='test3'
            ),
        test3 = ['test1',dict(test='test1',test2='test23'),'test3'],
        test4 = 'test4'         
        )

    dict6 = dict(
        test1 = 'test1',
        test2 = dict(
            test1='true',
            test2='test23',
            test3='test3'
            ),
        test3 = ['test1',dict(test='test1',test2='test23'),'test3'],
        test4 = 'test4'         
        )
    dict7 = [{'roles': ['view-clients', 'view-identity-providers', 'view-users', 'query-realms', 'manage-users'], 'clientid': 'master-realm'}, {'roles': ['manage-account', 'view-profile', 'manage-account-links'], 'clientid': 'account'}]
    dict8 = [{'roles': ['view-clients', 'query-realms', 'view-users'], 'clientid': 'master-realm'}, {'roles': ['manage-account-links', 'view-profile', 'manage-account'], 'clientid': 'account'}]

    def test_trivial(self):
        self.assertTrue(isDictEquals(self.dict1,self.dict1))

    def test_equals_with_dict2_bigger_than_dict1(self):
        self.assertTrue(isDictEquals(self.dict1,self.dict2))

    def test_not_equals_with_dict2_bigger_than_dict1(self):
        self.assertFalse(isDictEquals(self.dict2,self.dict1))

    def test_not_equals_with_dict1_different_than_dict3(self):
        self.assertFalse(isDictEquals(self.dict1,self.dict3))

    def test_equals_with_dict5_contain_bool_and_dict6_contain_true_string(self):
        self.assertFalse(isDictEquals(self.dict5,self.dict6))
        self.assertFalse(isDictEquals(self.dict6,self.dict5))

    def test_not_equals_dict7_dict8_compare_dict7_with_list_bigger_than_dict8_but_reverse_equals(self):
        self.assertFalse(isDictEquals(self.dict7,self.dict8))
        self.assertTrue(isDictEquals(self.dict8,self.dict7))
        
class KeycloakAnsibleClientRolesTestCase(unittest.TestCase):
    ansibleClientRoles = [
        {
            'clientid': 'test1',
            'roles': [
                'role1',
                'role2'
                ]
            },
        {
            'clientid': 'test2',
            'roles': [
                'role3',
                'role4'
                ]
            }        
        ]
    keycloakClientRoles = {
        'test1':[
            'role1',
            'role2'
            ],
        'test2':[
            'role3',
            'role4'
            ]
        }
    
    def testAnsible2KeycloakClientRoles(self):
        self.assertEqual(ansible2keycloakClientRoles(self.ansibleClientRoles), self.keycloakClientRoles, str(ansible2keycloakClientRoles(self.ansibleClientRoles)) + ' is not ' + str(self.keycloakClientRoles))
        
    def testKeycloak2AnsibleClientRoles(self):
        self.assertEqual(keycloak2ansibleClientRoles(self.keycloakClientRoles), self.ansibleClientRoles, str(keycloak2ansibleClientRoles(self.keycloakClientRoles)) + ' is not ' + str(self.ansibleClientRoles))

class KeycloakRemoveNoneValuesFromDictTest(unittest.TestCase):
    test1 = {
        "key1": "value1",
        "key2": None
        }
    expected1 = {
        "key1": "value1"
    }
    test2 = {
        "key1": "value1",
        "list1": [{
            "list1key1": None,
            "list1key2": "list1value2"
            }
        ]
    }
    expected2 = {
        "key1": "value1",
        "list1": [{
            "list1key2": "list1value2"
            }
        ]
    }
    test3 = {
        "key1": "value1",
        "list1": [{
            "list1key1": None,
            "list1key2": "list1value2",
            "list1list1": [{
                "list1list1key1": "list1list1value1",
                "list1list1key2": None
                }]
            },
            "list1value1",
            None
        ],
        "dict1": {
            "dict1key1": "dict1value1",
            "dict1key2": None,
            "dict1dict1": [{
                "dict1dict1key1": None,
                "dict1dict1key2": "dict1dict1Value2"
            }]
        }
    }
    expected3 = {
        "key1": "value1",
        "list1": [{
            "list1key2": "list1value2",
            "list1list1": [{
                "list1list1key1": "list1list1value1"
                }]
            },
            "list1value1",
        ],
        "dict1": {
            "dict1key1": "dict1value1",
            "dict1dict1": [{
                "dict1dict1key2": "dict1dict1Value2"
            }]
        }
    }
    def testSimpleDictWithOneNoneValue(self):
        result1 = remove_arguments_with_value_none(self.test1)
        self.assertDictEqual(result1, self.expected1, str(result1))

    def testDictWithListContainingOneNoneValue(self):
        result2 = remove_arguments_with_value_none(self.test2)
        self.assertDictEqual(result2, self.expected2, str(result2))

    def testDictWithListAndDictThreeLevel(self):
        result3 = remove_arguments_with_value_none(self.test3)
        self.assertDictEqual(result3, self.expected3, str(result3))
