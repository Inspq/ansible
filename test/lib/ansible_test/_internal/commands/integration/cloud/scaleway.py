"""Scaleway plugin for integration tests."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ....util import (
    ConfigParser,
    display,
)

from ....config import (
    IntegrationConfig,
)

from . import (
    CloudEnvironment,
    CloudEnvironmentConfig,
    CloudProvider,
)


class ScalewayCloudProvider(CloudProvider):
    """Checks if a configuration file has been passed or fixtures are going to be used for testing"""
    def __init__(self, args):  # type: (IntegrationConfig) -> None
        super(ScalewayCloudProvider, self).__init__(args)

        self.uses_config = True

    def setup(self):  # type: () -> None
        """Setup the cloud resource before delegation and register a cleanup callback."""
        super(ScalewayCloudProvider, self).setup()

        self._use_static_config()


class ScalewayCloudEnvironment(CloudEnvironment):
    """Updates integration test environment after delegation. Will setup the config file as parameter."""
    def get_environment_config(self):  # type: () -> CloudEnvironmentConfig
        """Return environment configuration for use in the test environment after delegation."""
        parser = ConfigParser()
        parser.read(self.config_path)

        env_vars = dict(
            SCW_API_KEY=parser.get('default', 'key'),
            SCW_ORG=parser.get('default', 'org')
        )

        display.sensitive.add(env_vars['SCW_API_KEY'])

        ansible_vars = dict(
            scw_org=parser.get('default', 'org'),
        )

        return CloudEnvironmentConfig(
            env_vars=env_vars,
            ansible_vars=ansible_vars,
        )
