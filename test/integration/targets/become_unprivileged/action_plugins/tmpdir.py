# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        result.update(self._execute_module('ping', task_vars=task_vars))
        result['tmpdir'] = self._connection._shell.tmpdir
        return result
