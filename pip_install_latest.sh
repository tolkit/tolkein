#!/bin/bash

# Build and install the latest tolkein version in the current environment

TOLKEIN_VERSION=$(
    grep current_version `dirname "$0"`/.bumpversion.cfg \
    | head -n 1 \
    | awk '{print $3}')

python3 setup.py sdist bdist_wheel \
&& echo y | pip uninstall tolkein \
&& pip install dist/tolkein-${TOLKEIN_VERSION}-py3-none-any.whl
