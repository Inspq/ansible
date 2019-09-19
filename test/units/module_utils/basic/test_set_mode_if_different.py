# -*- coding: utf-8 -*-
# (c) 2016, Toshio Kuratomi <tkuratomi@ansible.com>
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
from itertools import product

import pytest


SYNONYMS_0660 = (
    0o660,
    '0o660',
    '660',
    'u+rw-x,g+rw-x,o-rwx',
    'u=rw,g=rw,o-rwx',
)


@pytest.fixture
def mock_stats(mocker):
    mock_stat1 = mocker.MagicMock()
    mock_stat1.st_mode = 0o444
    mock_stat2 = mocker.MagicMock()
    mock_stat2.st_mode = 0o660
    yield {"before": mock_stat1, "after": mock_stat2}


@pytest.fixture
def am_check_mode(am):
    am.check_mode = True
    yield am
    am.check_mode = False


@pytest.fixture
def mock_lchmod(mocker):
    m_lchmod = mocker.patch('ansible.module_utils.basic.os.lchmod', return_value=None, create=True)
    yield m_lchmod


@pytest.mark.parametrize('previous_changes, check_mode, exists, stdin',
                         product((True, False), (True, False), (True, False), ({},)),
                         indirect=['stdin'])
def test_no_mode_given_returns_previous_changes(am, mock_stats, mock_lchmod, mocker, previous_changes, check_mode, exists):
    am.check_mode = check_mode
    mocker.patch('os.lstat', side_effect=[mock_stats['before']])
    m_lchmod = mocker.patch('os.lchmod', return_value=None, create=True)
    m_path_exists = mocker.patch('os.path.exists', return_value=exists)

    assert am.set_mode_if_different('/path/to/file', None, previous_changes) == previous_changes
    assert not m_lchmod.called
    assert not m_path_exists.called


@pytest.mark.parametrize('mode, check_mode, stdin',
                         product(SYNONYMS_0660, (True, False), ({},)),
                         indirect=['stdin'])
def test_mode_changed_to_0660(am, mock_stats, mocker, mode, check_mode):
    # Note: This is for checking that all the different ways of specifying
    # 0660 mode work.  It cannot be used to check that setting a mode that is
    # not equivalent to 0660 works.
    am.check_mode = check_mode
    mocker.patch('os.lstat', side_effect=[mock_stats['before'], mock_stats['after'], mock_stats['after']])
    m_lchmod = mocker.patch('os.lchmod', return_value=None, create=True)
    mocker.patch('os.path.exists', return_value=True)

    assert am.set_mode_if_different('/path/to/file', mode, False)
    if check_mode:
        assert not m_lchmod.called
    else:
        m_lchmod.assert_called_with(b'/path/to/file', 0o660)


@pytest.mark.parametrize('mode, check_mode, stdin',
                         product(SYNONYMS_0660, (True, False), ({},)),
                         indirect=['stdin'])
def test_mode_unchanged_when_already_0660(am, mock_stats, mocker, mode, check_mode):
    # Note: This is for checking that all the different ways of specifying
    # 0660 mode work.  It cannot be used to check that setting a mode that is
    # not equivalent to 0660 works.
    am.check_mode = check_mode
    mocker.patch('os.lstat', side_effect=[mock_stats['after'], mock_stats['after'], mock_stats['after']])
    m_lchmod = mocker.patch('os.lchmod', return_value=None, create=True)
    mocker.patch('os.path.exists', return_value=True)

    assert not am.set_mode_if_different('/path/to/file', mode, False)
    assert not m_lchmod.called


@pytest.mark.parametrize('check_mode, stdin',
                         product((True, False), ({},)),
                         indirect=['stdin'])
def test_missing_lchmod_is_not_link(am, mock_stats, mocker, monkeypatch, check_mode):
    """Some platforms have lchmod (*BSD) others do not (Linux)"""

    am.check_mode = check_mode
    original_hasattr = hasattr

    monkeypatch.delattr(os, 'lchmod', raising=False)

    mocker.patch('os.lstat', side_effect=[mock_stats['before'], mock_stats['after']])
    mocker.patch('os.path.islink', return_value=False)
    mocker.patch('os.path.exists', return_value=True)
    m_chmod = mocker.patch('os.chmod', return_value=None)

    assert am.set_mode_if_different('/path/to/file/no_lchmod', 0o660, False)
    if check_mode:
        assert not m_chmod.called
    else:
        m_chmod.assert_called_with(b'/path/to/file/no_lchmod', 0o660)


@pytest.mark.parametrize('check_mode, stdin',
                         product((True, False), ({},)),
                         indirect=['stdin'])
def test_missing_lchmod_is_link(am, mock_stats, mocker, monkeypatch, check_mode):
    """Some platforms have lchmod (*BSD) others do not (Linux)"""

    am.check_mode = check_mode
    original_hasattr = hasattr

    monkeypatch.delattr(os, 'lchmod', raising=False)

    mocker.patch('os.lstat', side_effect=[mock_stats['before'], mock_stats['after']])
    mocker.patch('os.path.islink', return_value=True)
    mocker.patch('os.path.exists', return_value=True)
    m_chmod = mocker.patch('os.chmod', return_value=None)
    mocker.patch('os.stat', return_value=mock_stats['after'])

    assert am.set_mode_if_different('/path/to/file/no_lchmod', 0o660, False)
    if check_mode:
        assert not m_chmod.called
    else:
        m_chmod.assert_called_with(b'/path/to/file/no_lchmod', 0o660)

    mocker.resetall()
    mocker.stopall()
