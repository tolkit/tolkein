#!/usr/bin/env bash

git stash -k -u

# run tests and generate coverage report
echo "py.test --ignore viewer --cov-config .coveragerc --doctest-modules --cov=src/tolkein --cov-report term-missing" &&
py.test --ignore viewer --cov-config .coveragerc --doctest-modules --cov=src/tolkein --cov-report term-missing

git stash pop
