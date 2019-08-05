"""Fallback source provider when no other provider matches the content root."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

import lib.types as t

from lib.constants import (
    TIMEOUT_PATH,
)

from . import (
    SourceProvider,
)


class UnversionedSource(SourceProvider):
    """Fallback source provider when no other provider matches the content root."""
    sequence = 0  # disable automatic detection

    @staticmethod
    def is_content_root(path):  # type: (str) -> bool
        """Return True if the given path is a content root for this provider."""
        return False

    def get_paths(self, path):  # type: (str) -> t.List[str]
        """Return the list of available content paths under the given path."""
        paths = []

        kill_any_dir = (
            '.idea',
            '.pytest_cache',
            '__pycache__',
            'ansible.egg-info',
        )

        kill_sub_dir = {
            'test/runner': (
                '.tox',
            ),
            'test': (
                'results',
                'cache',
            ),
            'docs/docsite': (
                '_build',
            ),
        }

        kill_sub_file = {
            '': (
                TIMEOUT_PATH,
            ),
        }

        kill_extensions = (
            '.pyc',
            '.retry',
        )

        for root, dir_names, file_names in os.walk(path):
            rel_root = os.path.relpath(root, path)

            if rel_root == '.':
                rel_root = ''

            for kill in kill_any_dir + kill_sub_dir.get(rel_root, ()):
                if kill in dir_names:
                    dir_names.remove(kill)

            kill_files = kill_sub_file.get(rel_root, ())

            paths.extend([os.path.join(rel_root, file_name) for file_name in file_names
                          if not os.path.splitext(file_name)[1] in kill_extensions and file_name not in kill_files])

        return paths
