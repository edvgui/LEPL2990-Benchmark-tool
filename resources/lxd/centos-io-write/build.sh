#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

BASE="images:centos/7/amd64"
CONTAINER="tmp"
SNAPSHOT="export"

TAG=$1
SIZE=$2

lxc launch -e ${BASE} ${CONTAINER}

lxc file push "${DIR}/../../common/io/${SIZE}.tar" ${CONTAINER}/root/source.tar
lxc file push "${DIR}/../../common/io/write.sh" ${CONTAINER}/root/write.sh
lxc exec ${CONTAINER} -- chmod +x /root/write.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $TAG
lxc stop --force ${CONTAINER}
