#!/bin/bash

T=${1:-tests}
shift

. enable_matlab.sh
py.test --regtest-reset $T $*

. disable_matlab.sh
py.test --regtest-reset $T $*

. enable_matlab.sh
