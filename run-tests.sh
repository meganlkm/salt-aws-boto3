#!/usr/bin/env bash

export BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pip install -r requirements-test.pip


export TEST_PACKAGE="aws_boto3"

with_rednose="--rednose --force-color"
with_coverage="--cover-html-dir=${BASE_DIR}/htmlcov --with-coverage --cover-html --cover-package=${TEST_PACKAGE} --cover-erase --cover-branches"
with_doctest="--with-doctest"
test -z $1 || dotests="--tests=${1}"

exec nosetests ${with_rednose} -s -v ${with_doctest} ${with_coverage} --where ${BASE_DIR}/tests ${dotests}
