#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"

lxc launch -e ${BASE} ${CONTAINER}

lxc file push "${DIR}/../../common/io/xs.tar" ${CONTAINER}/root/xs.tar
lxc exec ${CONTAINER} -- tar -xf xs.tar
lxc file push "${DIR}/../../common/io/read.sh" ${CONTAINER}/root/read.sh
lxc exec ${CONTAINER} -- chmod +x /root/read.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $1
lxc stop ${CONTAINER}
