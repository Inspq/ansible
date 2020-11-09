# (c) 2014, Brian Coca, Josh Drake, et al
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.cache import BaseCacheModule

DOCUMENTATION = '''
    cache: none
    short_description: write-only cache (no cache)
    description:
        - No caching at all
    version_added: historical
    author: core team (@ansible-core)
    options:
      _timeout:
        default: 86400
        description: Expiration timeout for the cache plugin data
        env:
          - name: ANSIBLE_CACHE_PLUGIN_TIMEOUT
        ini:
          - key: fact_caching_timeout
            section: defaults
        type: integer
'''


class CacheModule(BaseCacheModule):
    def __init__(self, *args, **kwargs):
        super(CacheModule, self).__init__(*args, **kwargs)
        self.empty = {}
        self._timeout = self.get_option('_timeout')

    def get(self, key):
        return self.empty.get(key)

    def set(self, key, value):
        return value

    def keys(self):
        return self.empty.keys()

    def contains(self, key):
        return key in self.empty

    def delete(self, key):
        del self.emtpy[key]

    def flush(self):
        self.empty = {}

    def copy(self):
        return self.empty.copy()

    def __getstate__(self):
        return self.copy()

    def __setstate__(self, data):
        self.empty = data
