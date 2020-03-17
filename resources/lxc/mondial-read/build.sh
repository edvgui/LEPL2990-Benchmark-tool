#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
LOG_FILE="${DIR}/build.log"

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"
NAME="alpine-mondial-read"

lxc launch ${BASE} ${CONTAINER}

lxc exec ${CONTAINER} -- apk update
lxc exec ${CONTAINER} -- apk add sqlite
lxc exec ${CONTAINER} -- mkdir /root/src
lxc file push "${DIR}/../../common/sqlite/mondial-orig.db" ${CONTAINER}/root/src/mondial-orig.db
lxc file push "${DIR}/../../common/sqlite/read.sqlite" ${CONTAINER}/root/src/read.sqlite
lxc file push "${DIR}/../../common/sqlite/read.sh" ${CONTAINER}/root/read.sh
lxc exec ${CONTAINER} -- chmod +x /root/read.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias ${NAME}
lxc stop ${CONTAINER}
lxc delete ${CONTAINER}