import collections
import os
import unittest

from ansible.module_utils.sx5_utils import isDictEquals


class sx5IsDictEqualsTestCase(unittest.TestCase):

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
    
    def test_trivial(self):
        self.assertTrue(isDictEquals(self.dict1,self.dict1))

    def test_equals_with_dict2_bigger_than_dict1(self):
        self.assertTrue(isDictEquals(self.dict1,self.dict2))

    def test_not_equals_with_dict2_bigger_than_dict1(self):
        self.assertFalse(isDictEquals(self.dict2,self.dict1))

    def test_not_equals_with_dict1_different_than_dict3(self):
        self.assertFalse(isDictEquals(self.dict1,self.dict3))
