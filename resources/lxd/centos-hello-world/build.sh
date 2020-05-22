#!/usr/bin/env bash

BASE="images:centos/7/amd64"
CONTAINER="tmp"
SNAPSHOT="export"

set -e

lxc launch -e ${BASE} ${CONTAINER}
lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $1
lxc stop --force ${CONTAINER}
