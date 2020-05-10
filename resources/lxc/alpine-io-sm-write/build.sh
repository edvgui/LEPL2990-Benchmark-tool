#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"

lxc launch -e ${BASE} ${CONTAINER}

lxc file push "${DIR}/../../common/io/sm.tar" ${CONTAINER}/root/sm.tar
lxc file push "${DIR}/../../common/io/write.sh" ${CONTAINER}/root/write.sh
lxc exec ${CONTAINER} -- chmod +x /root/write.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $1
lxc stop ${CONTAINER}
