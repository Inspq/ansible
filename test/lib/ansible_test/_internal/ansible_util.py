"""Miscellaneous utility functions and classes specific to ansible cli tools."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os

from . import types as t

from .constants import (
    SOFT_RLIMIT_NOFILE,
)

from .util import (
    common_environment,
    display,
    find_python,
    ApplicationError,
    ANSIBLE_LIB_ROOT,
    ANSIBLE_TEST_DATA_ROOT,
    ANSIBLE_BIN_PATH,
    ANSIBLE_SOURCE_ROOT,
)

from .util_common import (
    create_temp_dir,
    run_command,
    ResultType,
)

from .config import (
    IntegrationConfig,
    PosixIntegrationConfig,
    EnvironmentConfig,
    CommonConfig,
)

from .data import (
    data_context,
)

CHECK_YAML_VERSIONS = {}


def ansible_environment(args, color=True, ansible_config=None):
    """
    :type args: CommonConfig
    :type color: bool
    :type ansible_config: str | None
    :rtype: dict[str, str]
    """
    env = common_environment()
    path = env['PATH']

    if not path.startswith(ANSIBLE_BIN_PATH + os.path.pathsep):
        path = ANSIBLE_BIN_PATH + os.path.pathsep + path

    if not ansible_config:
        # use the default empty configuration unless one has been provided
        ansible_config = args.get_ansible_config()

    if not args.explain and not os.path.exists(ansible_config):
        raise ApplicationError('Configuration not found: %s' % ansible_config)

    ansible = dict(
        ANSIBLE_PYTHON_MODULE_RLIMIT_NOFILE=str(SOFT_RLIMIT_NOFILE),
        ANSIBLE_FORCE_COLOR='%s' % 'true' if args.color and color else 'false',
        ANSIBLE_FORCE_HANDLERS='true',  # allow cleanup handlers to run when tests fail
        ANSIBLE_HOST_PATTERN_MISMATCH='error',  # prevent tests from unintentionally passing when hosts are not found
        ANSIBLE_INVENTORY='/dev/null',  # force tests to provide inventory
        ANSIBLE_DEPRECATION_WARNINGS='false',
        ANSIBLE_HOST_KEY_CHECKING='false',
        ANSIBLE_RETRY_FILES_ENABLED='false',
        ANSIBLE_CONFIG=ansible_config,
        ANSIBLE_LIBRARY='/dev/null',
        ANSIBLE_DEVEL_WARNING='false',  # Don't show warnings that CI is running devel
        PYTHONPATH=get_ansible_python_path(),
        PAGER='/bin/cat',
        PATH=path,
        # give TQM worker processes time to report code coverage results
        # without this the last task in a play may write no coverage file, an empty file, or an incomplete file
        # enabled even when not using code coverage to surface warnings when worker processes do not exit cleanly
        ANSIBLE_WORKER_SHUTDOWN_POLL_COUNT='100',
        ANSIBLE_WORKER_SHUTDOWN_POLL_DELAY='0.1',
    )

    if isinstance(args, IntegrationConfig) and args.coverage:
        # standard path injection is not effective for ansible-connection, instead the location must be configured
        # ansible-connection only requires the injector for code coverage
        # the correct python interpreter is already selected using the sys.executable used to invoke ansible
        ansible.update(dict(
            ANSIBLE_CONNECTION_PATH=os.path.join(ANSIBLE_TEST_DATA_ROOT, 'injector', 'ansible-connection'),
        ))

    if isinstance(args, PosixIntegrationConfig):
        ansible.update(dict(
            ANSIBLE_PYTHON_INTERPRETER='/set/ansible_python_interpreter/in/inventory',  # force tests to set ansible_python_interpreter in inventory
        ))

    env.update(ansible)

    if args.debug:
        env.update(dict(
            ANSIBLE_DEBUG='true',
            ANSIBLE_LOG_PATH=os.path.join(ResultType.LOGS.name, 'debug.log'),
        ))

    if data_context().content.collection:
        env.update(dict(
            ANSIBLE_COLLECTIONS_PATHS=data_context().content.collection.root,
        ))

    if data_context().content.is_ansible:
        env.update(configure_plugin_paths(args))

    return env


def configure_plugin_paths(args):  # type: (CommonConfig) -> t.Dict[str, str]
    """Return environment variables with paths to plugins relevant for the current command."""
    if not isinstance(args, IntegrationConfig):
        return {}

    support_path = os.path.join(ANSIBLE_SOURCE_ROOT, 'test', 'support', args.command)

    # provide private copies of collections for integration tests
    collection_root = os.path.join(support_path, 'collections')

    env = dict(
        ANSIBLE_COLLECTIONS_PATHS=collection_root,
    )

    # provide private copies of plugins for integration tests
    plugin_root = os.path.join(support_path, 'plugins')

    plugin_list = [
        'action',
        'become',
        'cache',
        'callback',
        'cliconf',
        'connection',
        'filter',
        'httpapi',
        'inventory',
        'lookup',
        'netconf',
        # 'shell' is not configurable
        'strategy',
        'terminal',
        'test',
        'vars',
    ]

    # most plugins follow a standard naming convention
    plugin_map = dict(('%s_plugins' % name, name) for name in plugin_list)

    # these plugins do not follow the standard naming convention
    plugin_map.update(
        doc_fragment='doc_fragments',
        library='modules',
        module_utils='module_utils',
    )

    env.update(dict(('ANSIBLE_%s' % key.upper(), os.path.join(plugin_root, value)) for key, value in plugin_map.items()))

    # only configure directories which exist
    env = dict((key, value) for key, value in env.items() if os.path.isdir(value))

    return env


def get_ansible_python_path():  # type: () -> str
    """
    Return a directory usable for PYTHONPATH, containing only the ansible package.
    If a temporary directory is required, it will be cached for the lifetime of the process and cleaned up at exit.
    """
    if ANSIBLE_SOURCE_ROOT:
        # when running from source there is no need for a temporary directory to isolate the ansible package
        return os.path.dirname(ANSIBLE_LIB_ROOT)

    try:
        return get_ansible_python_path.python_path
    except AttributeError:
        pass

    python_path = create_temp_dir(prefix='ansible-test-')
    get_ansible_python_path.python_path = python_path

    os.symlink(ANSIBLE_LIB_ROOT, os.path.join(python_path, 'ansible'))

    return python_path


def check_pyyaml(args, version):
    """
    :type args: EnvironmentConfig
    :type version: str
    """
    try:
        return CHECK_YAML_VERSIONS[version]
    except KeyError:
        pass

    python = find_python(version)
    stdout, _dummy = run_command(args, [python, os.path.join(ANSIBLE_TEST_DATA_ROOT, 'yamlcheck.py')],
                                 capture=True, always=True)

    CHECK_YAML_VERSIONS[version] = result = json.loads(stdout)

    yaml = result['yaml']
    cloader = result['cloader']

    if not yaml:
        display.warning('PyYAML is not installed for interpreter: %s' % python)
    elif not cloader:
        display.warning('PyYAML will be slow due to installation without libyaml support for interpreter: %s' % python)

    return result
