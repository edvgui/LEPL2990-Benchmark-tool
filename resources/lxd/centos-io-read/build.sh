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

lxc file push "${DIR}/../../common/io/${SIZE}.tar" ${CONTAINER}/root/source.tar
lxc exec ${CONTAINER} -- tar -xf source.tar
lxc exec ${CONTAINER} -- rm /root/source.tar
lxc file push "${DIR}/../../common/io/read.c" ${CONTAINER}/root/read.c
lxc exec ${CONTAINER} -- yum -y install gcc
lxc exec ${CONTAINER} -- gcc -o /root/read /root/read.c

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $TAG
lxc stop --force ${CONTAINER}
