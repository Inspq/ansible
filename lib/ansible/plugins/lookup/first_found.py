# (c) 2013, seth vidal <skvidal@fedoraproject.org> red hat, inc
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: first_found
    author: Seth Vidal (!UNKNOWN) <skvidal@fedoraproject.org>
    version_added: historical
    short_description: return first file found from list
    description:
      - This lookup checks a list of files and paths and returns the full path to the first combination found.
      - As all lookups, when fed relative paths it will try use the current task's location first and go up the chain
        to the containing locations of role / play / include and so on.
      - The list of files has precedence over the paths searched.
        For example, A task in a role has a 'file1' in the play's relative path, this will be used, 'file2' in role's relative path will not.
      - Either a list of files C(_terms) or a key `files` with a list of files is required for this plugin to operate.
    notes:
      - This lookup can be used in 'dual mode', either passing a list of file names or a dictionary that has C(files) and C(paths).
    options:
      _terms:
        description: A list of file names.
      files:
        description: A list of file names.
        type: list
        default: []
      paths:
        description: A list of paths in which to look for the files.
        type: list
        default: []
      skip:
        type: boolean
        default: False
        description: Return an empty list if no file is found, instead of an error.
"""

EXAMPLES = """
- name: show first existing file or ignore if none do
  debug:
    msg: "{{ lookup('first_found', findme, errors='ignore') }}"
  vars:
    findme:
      - /path/to/foo.txt
      - bar.txt  # will be looked in files/ dir relative to role and/or play
      - /path/to/biz.txt

- name: include tasks only if files exist.
  include_tasks:
    file: "{{ query('first_found', params) }}"
  vars:
    params:
      files:
        - path/tasks.yaml
        - path/other_tasks.yaml

- name: |
        copy first existing file found to /some/file,
        looking in relative directories from where the task is defined and
        including any play objects that contain it
  copy:
    src: "{{ lookup('first_found', findme) }}"
    dest: /some/file
  vars:
    findme:
      - foo
      - "{{ inventory_hostname }}"
      - bar

- name: same copy but specific paths
  copy:
    src: "{{ lookup('first_found', params) }}"
    dest: /some/file
  vars:
    params:
      files:
        - foo
        - "{{ inventory_hostname }}"
        - bar
      paths:
        - /tmp/production
        - /tmp/staging

- name: INTERFACES | Create Ansible header for /etc/network/interfaces
  template:
    src: "{{ lookup('first_found', findme) }}"
    dest: "/etc/foo.conf"
  vars:
    findme:
      - "{{ ansible_virtualization_type }}_foo.conf"
      - "default_foo.conf"

- name: read vars from first file found, use 'vars/' relative subdir
  include_vars: "{{ lookup('first_found', params) }}"
  vars:
    params:
      files:
        - '{{ ansible_distribution }}.yml'
        - '{{ ansible_os_family }}.yml'
        - default.yml
      paths:
        - 'vars'
"""

RETURN = """
  _raw:
    description:
      - path to file found
    type: list
    elements: path
"""
import os

from jinja2.exceptions import UndefinedError

from ansible.errors import AnsibleLookupError, AnsibleUndefinedVariable
from ansible.module_utils.common._collections_compat import Mapping, Sequence
from ansible.module_utils.six import string_types
from ansible.plugins.lookup import LookupBase


def _split_on(terms, spliters=','):

    # TODO: fix as it does not allow spaces in names
    termlist = []
    if isinstance(terms, string_types):
        for spliter in spliters:
            terms = terms.replace(spliter, ' ')
        termlist = terms.split(' ')
    else:
        # added since options will already listify
        for t in terms:
            termlist.extend(_split_on(t, spliters))

    return termlist


class LookupModule(LookupBase):

    def _process_terms(self, terms, variables, kwargs):

        total_search = []
        skip = False

        # can use a dict instead of list item to pass inline config
        for term in terms:
            if isinstance(term, Mapping):
                self.set_options(var_options=variables, direct=term)
            elif isinstance(term, string_types):
                self.set_options(var_options=variables, direct=kwargs)
            elif isinstance(term, Sequence):
                partial, skip = self._process_terms(term, variables, kwargs)
                total_search.extend(partial)
                continue
            else:
                raise AnsibleLookupError("Invalid term supplied, can handle string, mapping or list of strings but got: %s for %s" % (type(term), term))

            files = self.get_option('files')
            paths = self.get_option('paths')

            # NOTE: this is used as 'global' but  can be set many times?!?!?
            skip = self.get_option('skip')

            # magic extra spliting to create lists
            filelist = _split_on(files, ',;')
            pathlist = _split_on(paths, ',:;')

            # create search structure
            if pathlist:
                for path in pathlist:
                    for fn in filelist:
                        f = os.path.join(path, fn)
                        total_search.append(f)
            elif filelist:
                # NOTE: this seems wrong, should be 'extend' as any option/entry can clobber all
                total_search = filelist
            else:
                total_search.append(term)

        return total_search, skip

    def run(self, terms, variables, **kwargs):

        total_search, skip = self._process_terms(terms, variables, kwargs)

        # NOTE: during refactor noticed that the 'using a dict' as term
        # is designed to only work with 'one' otherwise inconsistencies will appear.
        # see other notes below.

        # actually search
        subdir = getattr(self, '_subdir', 'files')

        path = None
        for fn in total_search:

            try:
                fn = self._templar.template(fn)
            except (AnsibleUndefinedVariable, UndefinedError):
                continue

            # get subdir if set by task executor, default to files otherwise
            path = self.find_file_in_search_path(variables, subdir, fn, ignore_missing=True)

            # exit if we find one!
            if path is not None:
                return [path]

        # if we get here, no file was found
        if skip:
            # NOTE: global skip wont matter, only last 'skip' value in dict term
            return []
        raise AnsibleLookupError("No file was found when using first_found. Use errors='ignore' to allow this task to be skipped if no files are found")
