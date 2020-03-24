#!/usr/bin/env bash

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"

lxc launch -e ${BASE} ${CONTAINER}
lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $1
lxc stop ${CONTAINER}
