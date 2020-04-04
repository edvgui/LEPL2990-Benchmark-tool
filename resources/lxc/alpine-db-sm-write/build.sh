#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"

lxc launch -e ${BASE} ${CONTAINER}

lxc exec ${CONTAINER} -- apk update
lxc exec ${CONTAINER} -- apk add sqlite
lxc exec ${CONTAINER} -- mkdir /root/src
lxc file push "${DIR}/../../common/sqlite/tpcc-sm.db" ${CONTAINER}/root/tpcc.db
lxc file push "${DIR}/../../common/sqlite/write.sqlite" ${CONTAINER}/root/write.sqlite
lxc file push "${DIR}/../../common/sqlite/sqlite.sh" ${CONTAINER}/root/sqlite.sh
lxc exec ${CONTAINER} -- chmod +x /root/sqlite.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $1
lxc stop ${CONTAINER}
