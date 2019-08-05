"""Enable unit testing of Ansible collections."""
from __future__ import (absolute_import, division, print_function)


import os
import sys

# set by ansible-test to a single directory, rather than a list of directories as supported by Ansible itself
ANSIBLE_COLLECTIONS_PATH = os.path.join(os.environ['ANSIBLE_COLLECTIONS_PATHS'], 'ansible_collections')


def collection_pypkgpath(self):
    for parent in self.parts(reverse=True):
        if str(parent) == ANSIBLE_COLLECTIONS_PATH:
            return parent

    raise Exception('File "%s" not found in collection path "%s".' % (self.strpath, ANSIBLE_COLLECTIONS_PATH))


def pytest_configure():
    from ansible.utils.collection_loader import AnsibleCollectionLoader

    # allow unit tests to import code from collections
    sys.meta_path.insert(0, AnsibleCollectionLoader())

    import py._path.local

    # force collections unit tests to be loaded with the ansible_collections namespace
    # original idea from https://stackoverflow.com/questions/50174130/how-do-i-pytest-a-project-using-pep-420-namespace-packages/50175552#50175552
    py._path.local.LocalPath.pypkgpath = collection_pypkgpath
