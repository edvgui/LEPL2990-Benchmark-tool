#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

BASE="images:centos/7/amd64"
CONTAINER="tmp"
SNAPSHOT="export"

lxc launch -e ${BASE} ${CONTAINER}

lxc file push "${DIR}/../../common/network/ping.sh" ${CONTAINER}/root/ping.sh
lxc exec ${CONTAINER} -- chmod +x /root/ping.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $1
lxc stop --force ${CONTAINER}
