#!/usr/bin/env bash

# lint code in lib directory
echo "pylint --rcfile=.pylintrc src/tolkein -f parseable -r n" &&
pylint --rcfile=.pylintrc src/tolkein -f parseable -r n &&
# check codestyle
echo "pycodestyle src/tolkein --max-line-length=120" &&
pycodestyle src/tolkein --max-line-length=120 &&
# check docstyle
echo "pydocstyle src/tolkein" &&
pydocstyle src/tolkein
