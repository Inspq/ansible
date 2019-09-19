#!/usr/bin/env python


import sys
from collections import namedtuple
import rpmfluff


RPM = namedtuple('RPM', ['name', 'version', 'release', 'epoch', 'recommends'])


SPECS = [
    RPM('dinginessentail', '1.0', '1', None, None),
    RPM('dinginessentail', '1.0', '2', '1', None),
    RPM('dinginessentail', '1.1', '1', '1', None),
    RPM('dinginessentail-olive', '1.0', '1', None, None),
    RPM('dinginessentail-olive', '1.1', '1', None, None),
    RPM('landsidescalping', '1.0', '1', None, None),
    RPM('landsidescalping', '1.1', '1', None, None),
    RPM('dinginessentail-with-weak-dep', '1.0', '1', None, ['dinginessentail-weak-dep']),
    RPM('dinginessentail-weak-dep', '1.0', '1', None, None),
]


def main():
    try:
        arch = sys.argv[1]
    except IndexError:
        arch = 'x86_64'

    pkgs = []
    for spec in SPECS:
        pkg = rpmfluff.SimpleRpmBuild(spec.name, spec.version, spec.release, [arch])
        pkg.epoch = spec.epoch

        if spec.recommends:
            # Skip packages that require weak deps but an older version of RPM is being used
            if not hasattr(rpmfluff, "can_use_rpm_weak_deps") or not rpmfluff.can_use_rpm_weak_deps():
                continue

            for recommend in spec.recommends:
                pkg.add_recommends(recommend)

        pkgs.append(pkg)

    repo = rpmfluff.YumRepoBuild(pkgs)
    repo.make(arch)

    for pkg in pkgs:
        pkg.clean()

    print(repo.repoDir)


if __name__ == "__main__":
    main()
