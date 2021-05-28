"""Combine code coverage files."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json

from ... import types as t

from ...target import (
    walk_compile_targets,
    walk_powershell_targets,
)

from ...io import (
    read_text_file,
)

from ...util import (
    ANSIBLE_TEST_DATA_ROOT,
    display,
    ApplicationError,
)

from ...util_common import (
    ResultType,
    run_command,
    write_json_file,
    write_json_test_results,
)

from ...executor import (
    Delegate,
)

from ...data import (
    data_context,
)

from . import (
    enumerate_python_arcs,
    enumerate_powershell_lines,
    get_collection_path_regexes,
    get_all_coverage_files,
    get_python_coverage_files,
    get_python_modules,
    get_powershell_coverage_files,
    initialize_coverage,
    COVERAGE_OUTPUT_FILE_NAME,
    COVERAGE_GROUPS,
    CoverageConfig,
    PathChecker,
)


def command_coverage_combine(args):
    """Patch paths in coverage files and merge into a single file.
    :type args: CoverageCombineConfig
    :rtype: list[str]
    """
    if args.delegate:
        if args.docker or args.remote:
            paths = get_all_coverage_files()
            exported_paths = [path for path in paths if os.path.basename(path).split('=')[-1].split('.')[:2] == ['coverage', 'combined']]

            if not exported_paths:
                raise ExportedCoverageDataNotFound()

            pairs = [(path, os.path.relpath(path, data_context().content.root)) for path in exported_paths]

            def coverage_callback(files):  # type: (t.List[t.Tuple[str, str]]) -> None
                """Add the coverage files to the payload file list."""
                display.info('Including %d exported coverage file(s) in payload.' % len(pairs), verbosity=1)
                files.extend(pairs)

            data_context().register_payload_callback(coverage_callback)

        raise Delegate()

    paths = _command_coverage_combine_powershell(args) + _command_coverage_combine_python(args)

    for path in paths:
        display.info('Generated combined output: %s' % path, verbosity=1)

    return paths


class ExportedCoverageDataNotFound(ApplicationError):
    """Exception when no combined coverage data is present yet is required."""
    def __init__(self):
        super(ExportedCoverageDataNotFound, self).__init__(
            'Coverage data must be exported before processing with the `--docker` or `--remote` option.\n'
            'Export coverage with `ansible-test coverage combine` using the `--export` option.\n'
            'The exported files must be in the directory: %s/' % ResultType.COVERAGE.relative_path)


def _command_coverage_combine_python(args):
    """
    :type args: CoverageCombineConfig
    :rtype: list[str]
    """
    coverage = initialize_coverage(args)

    modules = get_python_modules()

    coverage_files = get_python_coverage_files()

    counter = 0
    sources = _get_coverage_targets(args, walk_compile_targets)
    groups = _build_stub_groups(args, sources, lambda s: dict((name, set()) for name in s))

    collection_search_re, collection_sub_re = get_collection_path_regexes()

    for coverage_file in coverage_files:
        counter += 1
        display.info('[%4d/%4d] %s' % (counter, len(coverage_files), coverage_file), verbosity=2)

        group = get_coverage_group(args, coverage_file)

        if group is None:
            display.warning('Unexpected name for coverage file: %s' % coverage_file)
            continue

        for filename, arcs in enumerate_python_arcs(coverage_file, coverage, modules, collection_search_re, collection_sub_re):
            if args.export:
                filename = os.path.relpath(filename)  # exported paths must be relative since absolute paths may differ between systems

            if group not in groups:
                groups[group] = {}

            arc_data = groups[group]

            if filename not in arc_data:
                arc_data[filename] = set()

            arc_data[filename].update(arcs)

    output_files = []

    if args.export:
        coverage_file = os.path.join(args.export, '')
        suffix = '=coverage.combined'
    else:
        coverage_file = os.path.join(ResultType.COVERAGE.path, COVERAGE_OUTPUT_FILE_NAME)
        suffix = ''

    path_checker = PathChecker(args, collection_search_re)

    for group in sorted(groups):
        arc_data = groups[group]

        updated = coverage.CoverageData()

        for filename in arc_data:
            if not path_checker.check_path(filename):
                continue

            updated.add_arcs({filename: list(arc_data[filename])})

        if args.all:
            updated.add_arcs(dict((source[0], []) for source in sources))

        if not args.explain:
            output_file = coverage_file + group + suffix
            updated.write_file(output_file)  # always write files to make sure stale files do not exist

            if updated:
                # only report files which are non-empty to prevent coverage from reporting errors
                output_files.append(output_file)

    path_checker.report()

    return sorted(output_files)


def _command_coverage_combine_powershell(args):
    """
    :type args: CoverageCombineConfig
    :rtype: list[str]
    """
    coverage_files = get_powershell_coverage_files()

    def _default_stub_value(source_paths):
        cmd = ['pwsh', os.path.join(ANSIBLE_TEST_DATA_ROOT, 'coverage_stub.ps1')]
        cmd.extend(source_paths)

        stubs = json.loads(run_command(args, cmd, capture=True, always=True)[0])

        return dict((d['Path'], dict((line, 0) for line in d['Lines'])) for d in stubs)

    counter = 0
    sources = _get_coverage_targets(args, walk_powershell_targets)
    groups = _build_stub_groups(args, sources, _default_stub_value)

    collection_search_re, collection_sub_re = get_collection_path_regexes()

    for coverage_file in coverage_files:
        counter += 1
        display.info('[%4d/%4d] %s' % (counter, len(coverage_files), coverage_file), verbosity=2)

        group = get_coverage_group(args, coverage_file)

        if group is None:
            display.warning('Unexpected name for coverage file: %s' % coverage_file)
            continue

        for filename, hits in enumerate_powershell_lines(coverage_file, collection_search_re, collection_sub_re):
            if args.export:
                filename = os.path.relpath(filename)  # exported paths must be relative since absolute paths may differ between systems

            if group not in groups:
                groups[group] = {}

            coverage_data = groups[group]

            if filename not in coverage_data:
                coverage_data[filename] = {}

            file_coverage = coverage_data[filename]

            for line_no, hit_count in hits.items():
                file_coverage[line_no] = file_coverage.get(line_no, 0) + hit_count

    output_files = []

    path_checker = PathChecker(args)

    for group in sorted(groups):
        coverage_data = dict((filename, data) for filename, data in groups[group].items() if path_checker.check_path(filename))

        if args.all:
            # Add 0 line entries for files not in coverage_data
            for source, source_line_count in sources:
                if source in coverage_data:
                    continue

                coverage_data[source] = _default_stub_value(source_line_count)

        if not args.explain:
            if args.export:
                output_file = os.path.join(args.export, group + '=coverage.combined')
                write_json_file(output_file, coverage_data, formatted=False)
                output_files.append(output_file)
                continue

            output_file = COVERAGE_OUTPUT_FILE_NAME + group + '-powershell'

            write_json_test_results(ResultType.COVERAGE, output_file, coverage_data, formatted=False)

            output_files.append(os.path.join(ResultType.COVERAGE.path, output_file))

    path_checker.report()

    return sorted(output_files)


def _get_coverage_targets(args, walk_func):
    """
    :type args: CoverageCombineConfig
    :type walk_func: Func
    :rtype: list[tuple[str, int]]
    """
    sources = []

    if args.all or args.stub:
        # excludes symlinks of regular files to avoid reporting on the same file multiple times
        # in the future it would be nice to merge any coverage for symlinks into the real files
        for target in walk_func(include_symlinks=False):
            target_path = os.path.abspath(target.path)

            target_lines = len(read_text_file(target_path).splitlines())

            sources.append((target_path, target_lines))

        sources.sort()

    return sources


def _build_stub_groups(args, sources, default_stub_value):
    """
    :type args: CoverageCombineConfig
    :type sources: List[tuple[str, int]]
    :type default_stub_value: Func[List[str]]
    :rtype: dict
    """
    groups = {}

    if args.stub:
        stub_group = []
        stub_groups = [stub_group]
        stub_line_limit = 500000
        stub_line_count = 0

        for source, source_line_count in sources:
            stub_group.append(source)
            stub_line_count += source_line_count

            if stub_line_count > stub_line_limit:
                stub_line_count = 0
                stub_group = []
                stub_groups.append(stub_group)

        for stub_index, stub_group in enumerate(stub_groups):
            if not stub_group:
                continue

            groups['=stub-%02d' % (stub_index + 1)] = default_stub_value(stub_group)

    return groups


def get_coverage_group(args, coverage_file):
    """
    :type args: CoverageCombineConfig
    :type coverage_file: str
    :rtype: str
    """
    parts = os.path.basename(coverage_file).split('=', 4)

    # noinspection PyTypeChecker
    if len(parts) != 5 or not parts[4].startswith('coverage.'):
        return None

    names = dict(
        command=parts[0],
        target=parts[1],
        environment=parts[2],
        version=parts[3],
    )

    export_names = dict(
        version=parts[3],
    )

    group = ''

    for part in COVERAGE_GROUPS:
        if part in args.group_by:
            group += '=%s' % names[part]
        elif args.export:
            group += '=%s' % export_names.get(part, 'various')

    if args.export:
        group = group.lstrip('=')

    return group


class CoverageCombineConfig(CoverageConfig):
    """Configuration for the coverage combine command."""
    def __init__(self, args):  # type: (t.Any) -> None
        super(CoverageCombineConfig, self).__init__(args)

        self.group_by = frozenset(args.group_by) if args.group_by else frozenset()  # type: t.FrozenSet[str]
        self.all = args.all  # type: bool
        self.stub = args.stub  # type: bool

        # only available to coverage combine
        self.export = args.export if 'export' in args else False  # type: str
