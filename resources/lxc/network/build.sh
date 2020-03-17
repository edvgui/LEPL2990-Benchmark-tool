#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
LOG_FILE="${DIR}/build.log"

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"
NAME="alpine-network"

lxc launch ${BASE} ${CONTAINER}

lxc file push "${DIR}/../../common/network/ping.sh" ${CONTAINER}/root/ping.sh
lxc exec ${CONTAINER} -- chmod +x /root/ping.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias ${NAME}
lxc stop ${CONTAINER}
lxc delete ${CONTAINER}