"""Test target identification, iteration and inclusion/exclusion."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections
import os
import re
import errno
import itertools
import abc

from lib.util import (
    ApplicationError,
    display,
    read_lines_without_comments,
    is_subdir,
    to_text,
    to_bytes,
)

from lib.data import (
    data_context,
)

MODULE_EXTENSIONS = '.py', '.ps1'


def find_target_completion(target_func, prefix):
    """
    :type target_func: () -> collections.Iterable[CompletionTarget]
    :type prefix: unicode
    :rtype: list[str]
    """
    try:
        targets = target_func()
        short = os.environ.get('COMP_TYPE') == '63'  # double tab completion from bash
        matches = walk_completion_targets(targets, prefix, short)
        return matches
    except Exception as ex:  # pylint: disable=locally-disabled, broad-except
        return [u'%s' % ex]


def walk_completion_targets(targets, prefix, short=False):
    """
    :type targets: collections.Iterable[CompletionTarget]
    :type prefix: str
    :type short: bool
    :rtype: tuple[str]
    """
    aliases = set(alias for target in targets for alias in target.aliases)

    if prefix.endswith('/') and prefix in aliases:
        aliases.remove(prefix)

    matches = [alias for alias in aliases if alias.startswith(prefix) and '/' not in alias[len(prefix):-1]]

    if short:
        offset = len(os.path.dirname(prefix))
        if offset:
            offset += 1
            relative_matches = [match[offset:] for match in matches if len(match) > offset]
            if len(relative_matches) > 1:
                matches = relative_matches

    return tuple(sorted(matches))


def walk_internal_targets(targets, includes=None, excludes=None, requires=None):
    """
    :type targets: collections.Iterable[T <= CompletionTarget]
    :type includes: list[str]
    :type excludes: list[str]
    :type requires: list[str]
    :rtype: tuple[T <= CompletionTarget]
    """
    targets = tuple(targets)

    include_targets = sorted(filter_targets(targets, includes, errors=True, directories=False), key=lambda t: t.name)

    if requires:
        require_targets = set(filter_targets(targets, requires, errors=True, directories=False))
        include_targets = [target for target in include_targets if target in require_targets]

    if excludes:
        list(filter_targets(targets, excludes, errors=True, include=False, directories=False))

    internal_targets = set(filter_targets(include_targets, excludes, errors=False, include=False, directories=False))
    return tuple(sorted(internal_targets, key=lambda t: t.name))


def filter_targets(targets, patterns, include=True, directories=True, errors=True):
    """
    :type targets: collections.Iterable[CompletionTarget]
    :type patterns: list[str]
    :type include: bool
    :type directories: bool
    :type errors: bool
    :rtype: collections.Iterable[CompletionTarget]
    """
    unmatched = set(patterns or ())
    compiled_patterns = dict((p, re.compile('^%s$' % p)) for p in patterns) if patterns else None

    for target in targets:
        matched_directories = set()
        match = False

        if patterns:
            for alias in target.aliases:
                for pattern in patterns:
                    if compiled_patterns[pattern].match(alias):
                        match = True

                        try:
                            unmatched.remove(pattern)
                        except KeyError:
                            pass

                        if alias.endswith('/'):
                            if target.base_path and len(target.base_path) > len(alias):
                                matched_directories.add(target.base_path)
                            else:
                                matched_directories.add(alias)
        elif include:
            match = True
            if not target.base_path:
                matched_directories.add('.')
            for alias in target.aliases:
                if alias.endswith('/'):
                    if target.base_path and len(target.base_path) > len(alias):
                        matched_directories.add(target.base_path)
                    else:
                        matched_directories.add(alias)

        if match != include:
            continue

        if directories and matched_directories:
            yield DirectoryTarget(sorted(matched_directories, key=len)[0], target.modules)
        else:
            yield target

    if errors:
        if unmatched:
            raise TargetPatternsNotMatched(unmatched)


def walk_module_targets():
    """
    :rtype: collections.Iterable[TestTarget]
    """
    for target in walk_test_targets(path=data_context().content.module_path, module_path=data_context().content.module_path, extensions=MODULE_EXTENSIONS):
        if not target.module:
            continue

        yield target


def walk_units_targets():
    """
    :rtype: collections.Iterable[TestTarget]
    """
    return walk_test_targets(path=data_context().content.unit_path, module_path=data_context().content.unit_module_path, extensions=('.py',), prefix='test_')


def walk_compile_targets():
    """
    :rtype: collections.Iterable[TestTarget]
    """
    return walk_test_targets(module_path=data_context().content.module_path, extensions=('.py',), extra_dirs=('bin',))


def walk_sanity_targets():
    """
    :rtype: collections.Iterable[TestTarget]
    """
    return walk_test_targets(module_path=data_context().content.module_path)


def walk_posix_integration_targets(include_hidden=False):
    """
    :type include_hidden: bool
    :rtype: collections.Iterable[IntegrationTarget]
    """
    for target in walk_integration_targets():
        if 'posix/' in target.aliases or (include_hidden and 'hidden/posix/' in target.aliases):
            yield target


def walk_network_integration_targets(include_hidden=False):
    """
    :type include_hidden: bool
    :rtype: collections.Iterable[IntegrationTarget]
    """
    for target in walk_integration_targets():
        if 'network/' in target.aliases or (include_hidden and 'hidden/network/' in target.aliases):
            yield target


def walk_windows_integration_targets(include_hidden=False):
    """
    :type include_hidden: bool
    :rtype: collections.Iterable[IntegrationTarget]
    """
    for target in walk_integration_targets():
        if 'windows/' in target.aliases or (include_hidden and 'hidden/windows/' in target.aliases):
            yield target


def walk_integration_targets():
    """
    :rtype: collections.Iterable[IntegrationTarget]
    """
    path = 'test/integration/targets'
    modules = frozenset(target.module for target in walk_module_targets())
    paths = data_context().content.get_dirs(path)
    prefixes = load_integration_prefixes()

    for path in paths:
        yield IntegrationTarget(path, modules, prefixes)


def load_integration_prefixes():
    """
    :rtype: dict[str, str]
    """
    path = 'test/integration'
    file_paths = sorted(f for f in data_context().content.get_files(path) if os.path.splitext(os.path.basename(f))[0] == 'target-prefixes')
    prefixes = {}

    for file_path in file_paths:
        prefix = os.path.splitext(file_path)[1][1:]
        with open(file_path, 'r') as prefix_fd:
            prefixes.update(dict((k, prefix) for k in prefix_fd.read().splitlines()))

    return prefixes


def walk_test_targets(path=None, module_path=None, extensions=None, prefix=None, extra_dirs=None):
    """
    :type path: str | None
    :type module_path: str | None
    :type extensions: tuple[str] | None
    :type prefix: str | None
    :type extra_dirs: tuple[str] | None
    :rtype: collections.Iterable[TestTarget]
    """
    if path:
        file_paths = data_context().content.walk_files(path)
    else:
        file_paths = data_context().content.all_files()

    for file_path in file_paths:
        name, ext = os.path.splitext(os.path.basename(file_path))

        if extensions and ext not in extensions:
            continue

        if prefix and not name.startswith(prefix):
            continue

        if os.path.islink(to_bytes(file_path)):
            # special case to allow a symlink of ansible_release.py -> ../release.py
            if file_path != 'lib/ansible/module_utils/ansible_release.py':
                continue

        yield TestTarget(file_path, module_path, prefix, path)

    file_paths = []

    if extra_dirs:
        for extra_dir in extra_dirs:
            for file_path in data_context().content.get_files(extra_dir):
                file_paths.append(file_path)

    for file_path in file_paths:
        if os.path.islink(to_bytes(file_path)):
            continue

        yield TestTarget(file_path, module_path, prefix, path)


def analyze_integration_target_dependencies(integration_targets):
    """
    :type integration_targets: list[IntegrationTarget]
    :rtype: dict[str,set[str]]
    """
    real_target_root = os.path.realpath('test/integration/targets') + '/'

    role_targets = [target for target in integration_targets if target.type == 'role']
    hidden_role_target_names = set(target.name for target in role_targets if 'hidden/' in target.aliases)

    dependencies = collections.defaultdict(set)

    # handle setup dependencies
    for target in integration_targets:
        for setup_target_name in target.setup_always + target.setup_once:
            dependencies[setup_target_name].add(target.name)

    # handle target dependencies
    for target in integration_targets:
        for need_target in target.needs_target:
            dependencies[need_target].add(target.name)

    # handle symlink dependencies between targets
    # this use case is supported, but discouraged
    for target in integration_targets:
        for path in data_context().content.walk_files(target.path):
            if not os.path.islink(path):
                continue

            real_link_path = os.path.realpath(path)

            if not real_link_path.startswith(real_target_root):
                continue

            link_target = real_link_path[len(real_target_root):].split('/')[0]

            if link_target == target.name:
                continue

            dependencies[link_target].add(target.name)

    # intentionally primitive analysis of role meta to avoid a dependency on pyyaml
    # script based targets are scanned as they may execute a playbook with role dependencies
    for target in integration_targets:
        meta_dir = os.path.join(target.path, 'meta')

        if not os.path.isdir(meta_dir):
            continue

        meta_paths = data_context().content.get_files(meta_dir)

        for meta_path in meta_paths:
            if os.path.exists(meta_path):
                with open(meta_path, 'rb') as meta_fd:
                    # try and decode the file as a utf-8 string, skip if it contains invalid chars (binary file)
                    try:
                        meta_lines = to_text(meta_fd.read()).splitlines()
                    except UnicodeDecodeError:
                        continue

                for meta_line in meta_lines:
                    if re.search(r'^ *#.*$', meta_line):
                        continue

                    if not meta_line.strip():
                        continue

                    for hidden_target_name in hidden_role_target_names:
                        if hidden_target_name in meta_line:
                            dependencies[hidden_target_name].add(target.name)

    while True:
        changes = 0

        for dummy, dependent_target_names in dependencies.items():
            for dependent_target_name in list(dependent_target_names):
                new_target_names = dependencies.get(dependent_target_name)

                if new_target_names:
                    for new_target_name in new_target_names:
                        if new_target_name not in dependent_target_names:
                            dependent_target_names.add(new_target_name)
                            changes += 1

        if not changes:
            break

    for target_name in sorted(dependencies):
        consumers = dependencies[target_name]

        if not consumers:
            continue

        display.info('%s:' % target_name, verbosity=4)

        for consumer in sorted(consumers):
            display.info('  %s' % consumer, verbosity=4)

    return dependencies


class CompletionTarget:
    """Command-line argument completion target base class."""
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.name = None
        self.path = None
        self.base_path = None
        self.modules = tuple()
        self.aliases = tuple()

    def __eq__(self, other):
        if isinstance(other, CompletionTarget):
            return self.__repr__() == other.__repr__()

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.name.__lt__(other.name)

    def __gt__(self, other):
        return self.name.__gt__(other.name)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        if self.modules:
            return '%s (%s)' % (self.name, ', '.join(self.modules))

        return self.name


class DirectoryTarget(CompletionTarget):
    """Directory target."""
    def __init__(self, path, modules):
        """
        :type path: str
        :type modules: tuple[str]
        """
        super(DirectoryTarget, self).__init__()

        self.name = path
        self.path = path
        self.modules = modules


class TestTarget(CompletionTarget):
    """Generic test target."""
    def __init__(self, path, module_path, module_prefix, base_path):
        """
        :type path: str
        :type module_path: str | None
        :type module_prefix: str | None
        :type base_path: str
        """
        super(TestTarget, self).__init__()

        self.name = path
        self.path = path
        self.base_path = base_path + '/' if base_path else None

        name, ext = os.path.splitext(os.path.basename(self.path))

        if module_path and is_subdir(path, module_path) and name != '__init__' and ext in MODULE_EXTENSIONS:
            self.module = name[len(module_prefix or ''):].lstrip('_')
            self.modules = (self.module,)
        else:
            self.module = None
            self.modules = tuple()

        aliases = [self.path, self.module]
        parts = self.path.split('/')

        for i in range(1, len(parts)):
            alias = '%s/' % '/'.join(parts[:i])
            aliases.append(alias)

        aliases = [a for a in aliases if a]

        self.aliases = tuple(sorted(aliases))


class IntegrationTarget(CompletionTarget):
    """Integration test target."""
    non_posix = frozenset((
        'network',
        'windows',
    ))

    categories = frozenset(non_posix | frozenset((
        'posix',
        'module',
        'needs',
        'skip',
    )))

    def __init__(self, path, modules, prefixes):
        """
        :type path: str
        :type modules: frozenset[str]
        :type prefixes: dict[str, str]
        """
        super(IntegrationTarget, self).__init__()

        self.name = os.path.basename(path)
        self.path = path

        # script_path and type

        contents = [os.path.basename(p) for p in data_context().content.get_files(path)]

        runme_files = tuple(c for c in contents if os.path.splitext(c)[0] == 'runme')
        test_files = tuple(c for c in contents if os.path.splitext(c)[0] == 'test')

        self.script_path = None

        if runme_files:
            self.type = 'script'
            self.script_path = os.path.join(path, runme_files[0])
        elif test_files:
            self.type = 'special'
        elif os.path.isdir(os.path.join(path, 'tasks')) or os.path.isdir(os.path.join(path, 'defaults')):
            self.type = 'role'
        else:
            self.type = 'role'  # ansible will consider these empty roles, so ansible-test should as well

        # static_aliases

        try:
            aliases_path = os.path.join(path, 'aliases')
            static_aliases = tuple(read_lines_without_comments(aliases_path, remove_blank_lines=True))
        except IOError as ex:
            if ex.errno != errno.ENOENT:
                raise
            static_aliases = tuple()

        # modules

        if self.name in modules:
            module_name = self.name
        elif self.name.startswith('win_') and self.name[4:] in modules:
            module_name = self.name[4:]
        else:
            module_name = None

        self.modules = tuple(sorted(a for a in static_aliases + tuple([module_name]) if a in modules))

        # groups

        groups = [self.type]
        groups += [a for a in static_aliases if a not in modules]
        groups += ['module/%s' % m for m in self.modules]

        if not self.modules:
            groups.append('non_module')

        if 'destructive' not in groups:
            groups.append('non_destructive')

        if '_' in self.name:
            prefix = self.name[:self.name.find('_')]
        else:
            prefix = None

        if prefix in prefixes:
            group = prefixes[prefix]

            if group != prefix:
                group = '%s/%s' % (group, prefix)

            groups.append(group)

        if self.name.startswith('win_'):
            groups.append('windows')

        if self.name.startswith('connection_'):
            groups.append('connection')

        if self.name.startswith('setup_') or self.name.startswith('prepare_'):
            groups.append('hidden')

        if self.type not in ('script', 'role'):
            groups.append('hidden')

        # Collect file paths before group expansion to avoid including the directories.
        # Ignore references to test targets, as those must be defined using `needs/target/*` or other target references.
        self.needs_file = tuple(sorted(set('/'.join(g.split('/')[2:]) for g in groups if
                                           g.startswith('needs/file/') and not g.startswith('needs/file/test/integration/targets/'))))

        for group in itertools.islice(groups, 0, len(groups)):
            if '/' in group:
                parts = group.split('/')
                for i in range(1, len(parts)):
                    groups.append('/'.join(parts[:i]))

        if not any(g in self.non_posix for g in groups):
            groups.append('posix')

        # aliases

        aliases = [self.name] + \
                  ['%s/' % g for g in groups] + \
                  ['%s/%s' % (g, self.name) for g in groups if g not in self.categories]

        if 'hidden/' in aliases:
            aliases = ['hidden/'] + ['hidden/%s' % a for a in aliases if not a.startswith('hidden/')]

        self.aliases = tuple(sorted(set(aliases)))

        # configuration

        self.setup_once = tuple(sorted(set(g.split('/')[2] for g in groups if g.startswith('setup/once/'))))
        self.setup_always = tuple(sorted(set(g.split('/')[2] for g in groups if g.startswith('setup/always/'))))
        self.needs_target = tuple(sorted(set(g.split('/')[2] for g in groups if g.startswith('needs/target/'))))


class TargetPatternsNotMatched(ApplicationError):
    """One or more targets were not matched when a match was required."""
    def __init__(self, patterns):
        """
        :type patterns: set[str]
        """
        self.patterns = sorted(patterns)

        if len(patterns) > 1:
            message = 'Target patterns not matched:\n%s' % '\n'.join(self.patterns)
        else:
            message = 'Target pattern not matched: %s' % self.patterns[0]

        super(TargetPatternsNotMatched, self).__init__(message)
