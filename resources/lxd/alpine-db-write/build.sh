#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

NETWORK="lxdbr0"
BASE="images:alpine/3.11/amd64"
CONTAINER="tmp"
SNAPSHOT="export"

TAG=$1
SIZE=$2

set -e

lxc launch -e -n ${NETWORK} ${BASE} ${CONTAINER}

sleep 10

lxc exec ${CONTAINER} -- apk update
lxc exec ${CONTAINER} -- apk add sqlite
lxc exec ${CONTAINER} -- mkdir /root/src
lxc file push "${DIR}/../../common/sqlite/tpcc-${SIZE}.db" ${CONTAINER}/root/tpcc.db
lxc file push "${DIR}/../../common/sqlite/write.sqlite" ${CONTAINER}/root/write.sqlite
lxc file push "${DIR}/../../common/sqlite/sqlite.sh" ${CONTAINER}/root/sqlite.sh
lxc exec ${CONTAINER} -- chmod +x /root/sqlite.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $TAG
lxc stop ${CONTAINER}
