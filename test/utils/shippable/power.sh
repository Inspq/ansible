#!/usr/bin/env bash

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

platform="${args[1]}"
version="${args[2]}"

if [ "${#args[@]}" -gt 3 ]; then
    target="shippable/posix/group${args[3]}/"
else
    target="shippable/posix/"
fi

stage="${S:-prod}"
provider="${P:-default}"

# shellcheck disable=SC2086
ansible-test integration --color -v --retry-on-error "${target}" ${COVERAGE:+"$COVERAGE"} ${CHANGED:+"$CHANGED"} ${UNSTABLE:+"$UNSTABLE"} \
    --remote "power/${platform}/${version}" --remote-terminate always --remote-stage "${stage}" --remote-provider "${provider}"
