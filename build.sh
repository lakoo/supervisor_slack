#!/usr/bin/env bash

PWD=`pwd`
WD=`cd $(dirname "$0") && pwd -P`

cd "${WD}"

docker build -t supervisor-slack .

cd "${PWD}"