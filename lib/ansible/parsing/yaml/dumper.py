# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
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

import yaml

from ansible.module_utils.six import PY3, text_type, binary_type
from ansible.module_utils.common.yaml import SafeDumper
from ansible.parsing.yaml.objects import AnsibleUnicode, AnsibleSequence, AnsibleMapping, AnsibleVaultEncryptedUnicode
from ansible.utils.unsafe_proxy import AnsibleUnsafeText, AnsibleUnsafeBytes
from ansible.vars.hostvars import HostVars, HostVarsVars


class AnsibleDumper(SafeDumper):
    '''
    A simple stub class that allows us to add representers
    for our overridden object types.
    '''


def represent_hostvars(self, data):
    return self.represent_dict(dict(data))


# Note: only want to represent the encrypted data
def represent_vault_encrypted_unicode(self, data):
    return self.represent_scalar(u'!vault', data._ciphertext.decode(), style='|')


if PY3:
    def represent_unicode(self, data):
        return yaml.representer.SafeRepresenter.represent_str(self, text_type(data))

    def represent_binary(self, data):
        return yaml.representer.SafeRepresenter.represent_binary(self, binary_type(data))
else:
    def represent_unicode(self, data):
        return yaml.representer.SafeRepresenter.represent_unicode(self, text_type(data))

    def represent_binary(self, data):
        return yaml.representer.SafeRepresenter.represent_str(self, binary_type(data))


AnsibleDumper.add_representer(
    AnsibleUnicode,
    represent_unicode,
)

AnsibleDumper.add_representer(
    AnsibleUnsafeText,
    represent_unicode,
)

AnsibleDumper.add_representer(
    AnsibleUnsafeBytes,
    represent_binary,
)

AnsibleDumper.add_representer(
    HostVars,
    represent_hostvars,
)

AnsibleDumper.add_representer(
    HostVarsVars,
    represent_hostvars,
)

AnsibleDumper.add_representer(
    AnsibleSequence,
    yaml.representer.SafeRepresenter.represent_list,
)

AnsibleDumper.add_representer(
    AnsibleMapping,
    yaml.representer.SafeRepresenter.represent_dict,
)

AnsibleDumper.add_representer(
    AnsibleVaultEncryptedUnicode,
    represent_vault_encrypted_unicode,
)
