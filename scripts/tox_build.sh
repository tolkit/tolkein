#!/usr/bin/env bash

set -eux
if [[ -n ${WHEEL_MANYLINUX1:-} ]]; then
  docker run --rm --user $UID -itv $(pwd):/code ionelmc/manylinux $WHEEL_MANYLINUX1
  tox --installpkg $WHEEL_PATH/*.whl -v
else
  tox -v
fi
if [ "$1" == "PyPI" ]; then
  if [[ -n ${WHEEL_PATH:-} ]]; then
    twine upload --repository-url https://pypi.org/legacy/ --skip-existing $WHEEL_PATH/*.whl
  fi
fi
