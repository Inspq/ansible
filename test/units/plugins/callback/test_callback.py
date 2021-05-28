# (c) 2012-2014, Chris Meyers <chris.meyers.fsu@gmail.com>
#
# This file is part of Ansible
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

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import re
import textwrap
import types

from units.compat import unittest
from units.compat.mock import MagicMock

from ansible.executor.task_result import TaskResult
from ansible.inventory.host import Host
from ansible.plugins.callback import CallbackBase


mock_task = MagicMock()
mock_task.delegate_to = None


class TestCallback(unittest.TestCase):
    # FIXME: This doesn't really test anything...
    def test_init(self):
        CallbackBase()

    def test_display(self):
        display_mock = MagicMock()
        display_mock.verbosity = 0
        cb = CallbackBase(display=display_mock)
        self.assertIs(cb._display, display_mock)

    def test_display_verbose(self):
        display_mock = MagicMock()
        display_mock.verbosity = 5
        cb = CallbackBase(display=display_mock)
        self.assertIs(cb._display, display_mock)

    def test_host_label(self):
        result = TaskResult(host=Host('host1'), task=mock_task, return_data={})

        self.assertEquals(CallbackBase.host_label(result), 'host1')

    def test_host_label_delegated(self):
        mock_task.delegate_to = 'host2'
        result = TaskResult(
            host=Host('host1'),
            task=mock_task,
            return_data={'_ansible_delegated_vars': {'ansible_host': 'host2'}},
        )
        self.assertEquals(CallbackBase.host_label(result), 'host1 -> host2')

    # TODO: import callback module so we can patch callback.cli/callback.C


class TestCallbackResults(unittest.TestCase):

    def test_get_item_label(self):
        cb = CallbackBase()
        results = {'item': 'some_item'}
        res = cb._get_item_label(results)
        self.assertEqual(res, 'some_item')

    def test_get_item_label_no_log(self):
        cb = CallbackBase()
        results = {'item': 'some_item', '_ansible_no_log': True}
        res = cb._get_item_label(results)
        self.assertEqual(res, "(censored due to no_log)")

        results = {'item': 'some_item', '_ansible_no_log': False}
        res = cb._get_item_label(results)
        self.assertEqual(res, "some_item")

    def test_clean_results_debug_task(self):
        cb = CallbackBase()
        result = {'item': 'some_item',
                  'invocation': 'foo --bar whatever [some_json]',
                  'a': 'a single a in result note letter a is in invocation',
                  'b': 'a single b in result note letter b is not in invocation',
                  'changed': True}

        cb._clean_results(result, 'debug')

        # See https://github.com/ansible/ansible/issues/33723
        self.assertTrue('a' in result)
        self.assertTrue('b' in result)
        self.assertFalse('invocation' in result)
        self.assertFalse('changed' in result)

    def test_clean_results_debug_task_no_invocation(self):
        cb = CallbackBase()
        result = {'item': 'some_item',
                  'a': 'a single a in result note letter a is in invocation',
                  'b': 'a single b in result note letter b is not in invocation',
                  'changed': True}

        cb._clean_results(result, 'debug')
        self.assertTrue('a' in result)
        self.assertTrue('b' in result)
        self.assertFalse('changed' in result)
        self.assertFalse('invocation' in result)

    def test_clean_results_debug_task_empty_results(self):
        cb = CallbackBase()
        result = {}
        cb._clean_results(result, 'debug')
        self.assertFalse('invocation' in result)
        self.assertEqual(len(result), 0)

    def test_clean_results(self):
        cb = CallbackBase()
        result = {'item': 'some_item',
                  'invocation': 'foo --bar whatever [some_json]',
                  'a': 'a single a in result note letter a is in invocation',
                  'b': 'a single b in result note letter b is not in invocation',
                  'changed': True}

        expected_result = result.copy()
        cb._clean_results(result, 'ebug')
        self.assertEqual(result, expected_result)


class TestCallbackDumpResults(object):
    def test_internal_keys(self):
        cb = CallbackBase()
        result = {'item': 'some_item',
                  '_ansible_some_var': 'SENTINEL',
                  'testing_ansible_out': 'should_be_left_in LEFTIN',
                  'invocation': 'foo --bar whatever [some_json]',
                  'some_dict_key': {'a_sub_dict_for_key': 'baz'},
                  'bad_dict_key': {'_ansible_internal_blah': 'SENTINEL'},
                  'changed': True}
        json_out = cb._dump_results(result)
        assert '"_ansible_' not in json_out
        assert 'SENTINEL' not in json_out
        assert 'LEFTIN' in json_out

    def test_exception(self):
        cb = CallbackBase()
        result = {'item': 'some_item LEFTIN',
                  'exception': ['frame1', 'SENTINEL']}
        json_out = cb._dump_results(result)
        assert 'SENTINEL' not in json_out
        assert 'exception' not in json_out
        assert 'LEFTIN' in json_out

    def test_verbose(self):
        cb = CallbackBase()
        result = {'item': 'some_item LEFTIN',
                  '_ansible_verbose_always': 'chicane'}
        json_out = cb._dump_results(result)
        assert 'SENTINEL' not in json_out
        assert 'LEFTIN' in json_out

    def test_diff(self):
        cb = CallbackBase()
        result = {'item': 'some_item LEFTIN',
                  'diff': ['remove stuff', 'added LEFTIN'],
                  '_ansible_verbose_always': 'chicane'}
        json_out = cb._dump_results(result)
        assert 'SENTINEL' not in json_out
        assert 'LEFTIN' in json_out

    def test_mixed_keys(self):
        cb = CallbackBase()
        result = {3: 'pi',
                  'tau': 6}
        json_out = cb._dump_results(result)
        round_trip_result = json.loads(json_out)
        assert len(round_trip_result) == 2
        assert '3' in round_trip_result
        assert 'tau' in round_trip_result
        assert round_trip_result['3'] == 'pi'
        assert round_trip_result['tau'] == 6


class TestCallbackDiff(unittest.TestCase):

    def setUp(self):
        self.cb = CallbackBase()

    def _strip_color(self, s):
        return re.sub('\033\\[[^m]*m', '', s)

    def test_difflist(self):
        # TODO: split into smaller tests?
        difflist = [{'before': u'preface\nThe Before String\npostscript',
                     'after': u'preface\nThe After String\npostscript',
                     'before_header': u'just before',
                     'after_header': u'just after'
                     },
                    {'before': u'preface\nThe Before String\npostscript',
                     'after': u'preface\nThe After String\npostscript',
                     },
                    {'src_binary': 'chicane'},
                    {'dst_binary': 'chicanery'},
                    {'dst_larger': 1},
                    {'src_larger': 2},
                    {'prepared': u'what does prepared do?'},
                    {'before_header': u'just before'},
                    {'after_header': u'just after'}]

        res = self.cb._get_diff(difflist)

        self.assertIn(u'Before String', res)
        self.assertIn(u'After String', res)
        self.assertIn(u'just before', res)
        self.assertIn(u'just after', res)

    def test_simple_diff(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before_header': 'somefile.txt',
                'after_header': 'generated from template somefile.j2',
                'before': 'one\ntwo\nthree\n',
                'after': 'one\nthree\nfour\n',
            })),
            textwrap.dedent('''\
                --- before: somefile.txt
                +++ after: generated from template somefile.j2
                @@ -1,3 +1,3 @@
                 one
                -two
                 three
                +four

            '''))

    def test_new_file(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before_header': 'somefile.txt',
                'after_header': 'generated from template somefile.j2',
                'before': '',
                'after': 'one\ntwo\nthree\n',
            })),
            textwrap.dedent('''\
                --- before: somefile.txt
                +++ after: generated from template somefile.j2
                @@ -0,0 +1,3 @@
                +one
                +two
                +three

            '''))

    def test_clear_file(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before_header': 'somefile.txt',
                'after_header': 'generated from template somefile.j2',
                'before': 'one\ntwo\nthree\n',
                'after': '',
            })),
            textwrap.dedent('''\
                --- before: somefile.txt
                +++ after: generated from template somefile.j2
                @@ -1,3 +0,0 @@
                -one
                -two
                -three

            '''))

    def test_no_trailing_newline_before(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before_header': 'somefile.txt',
                'after_header': 'generated from template somefile.j2',
                'before': 'one\ntwo\nthree',
                'after': 'one\ntwo\nthree\n',
            })),
            textwrap.dedent('''\
                --- before: somefile.txt
                +++ after: generated from template somefile.j2
                @@ -1,3 +1,3 @@
                 one
                 two
                -three
                \\ No newline at end of file
                +three

            '''))

    def test_no_trailing_newline_after(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before_header': 'somefile.txt',
                'after_header': 'generated from template somefile.j2',
                'before': 'one\ntwo\nthree\n',
                'after': 'one\ntwo\nthree',
            })),
            textwrap.dedent('''\
                --- before: somefile.txt
                +++ after: generated from template somefile.j2
                @@ -1,3 +1,3 @@
                 one
                 two
                -three
                +three
                \\ No newline at end of file

            '''))

    def test_no_trailing_newline_both(self):
        self.assertMultiLineEqual(
            self.cb._get_diff({
                'before_header': 'somefile.txt',
                'after_header': 'generated from template somefile.j2',
                'before': 'one\ntwo\nthree',
                'after': 'one\ntwo\nthree',
            }),
            '')

    def test_no_trailing_newline_both_with_some_changes(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before_header': 'somefile.txt',
                'after_header': 'generated from template somefile.j2',
                'before': 'one\ntwo\nthree',
                'after': 'one\nfive\nthree',
            })),
            textwrap.dedent('''\
                --- before: somefile.txt
                +++ after: generated from template somefile.j2
                @@ -1,3 +1,3 @@
                 one
                -two
                +five
                 three
                \\ No newline at end of file

            '''))

    def test_diff_dicts(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before': dict(one=1, two=2, three=3),
                'after': dict(one=1, three=3, four=4),
            })),
            textwrap.dedent('''\
                --- before
                +++ after
                @@ -1,5 +1,5 @@
                 {
                +    "four": 4,
                     "one": 1,
                -    "three": 3,
                -    "two": 2
                +    "three": 3
                 }

            '''))

    def test_diff_before_none(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before': None,
                'after': 'one line\n',
            })),
            textwrap.dedent('''\
                --- before
                +++ after
                @@ -0,0 +1 @@
                +one line

            '''))

    def test_diff_after_none(self):
        self.assertMultiLineEqual(
            self._strip_color(self.cb._get_diff({
                'before': 'one line\n',
                'after': None,
            })),
            textwrap.dedent('''\
                --- before
                +++ after
                @@ -1 +0,0 @@
                -one line

            '''))


class TestCallbackOnMethods(unittest.TestCase):
    def _find_on_methods(self, callback):
        cb_dir = dir(callback)
        method_names = [x for x in cb_dir if '_on_' in x]
        methods = [getattr(callback, mn) for mn in method_names]
        return methods

    def test_are_methods(self):
        cb = CallbackBase()
        for method in self._find_on_methods(cb):
            self.assertIsInstance(method, types.MethodType)

    def test_on_any(self):
        cb = CallbackBase()
        cb.v2_on_any('whatever', some_keyword='blippy')
        cb.on_any('whatever', some_keyword='blippy')
