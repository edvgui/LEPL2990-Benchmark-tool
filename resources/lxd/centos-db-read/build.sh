#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

NETWORK="lxdbr0"
BASE="images:centos/7/amd64"
CONTAINER="tmp"
SNAPSHOT="export"

TAG=$1
SIZE=$2

lxc launch -e -n ${NETWORK} ${BASE} ${CONTAINER}

sleep 10

lxc exec ${CONTAINER} -- yum -y install glibc.i686 zlib.i686
lxc exec ${CONTAINER} -- rm -rf /usr/bin/sqlite3

lxc file push "${DIR}/../../common/sqlite/sqlite3" ${CONTAINER}/usr/bin/sqlite3

lxc file push "${DIR}/../../common/sqlite/tpcc-${SIZE}.db" ${CONTAINER}/root/tpcc.db
lxc file push "${DIR}/../../common/sqlite/read.sqlite" ${CONTAINER}/root/read.sqlite
lxc file push "${DIR}/../../common/sqlite/sqlite.sh" ${CONTAINER}/root/sqlite.sh
lxc exec ${CONTAINER} -- chmod +x /root/sqlite.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $TAG
lxc stop ${CONTAINER}
