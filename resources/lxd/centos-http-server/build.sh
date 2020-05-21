#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

NETWORK="lxdbr0"
BASE="images:centos/7/amd64"
CONTAINER="tmp"
SNAPSHOT="export"


lxc launch -e -n ${NETWORK} ${BASE} ${CONTAINER}

sleep 10

lxc exec ${CONTAINER} -- yum -y install epel-release
lxc exec ${CONTAINER} -- yum -y install lighttpd
lxc exec ${CONTAINER} -- rm -rf /var/cash/apk/*
lxc exec ${CONTAINER} -- sed -i 's/server.use-ipv6 = "enable"/server.use-ipv6 = "disable"/' /etc/lighttpd/lighttpd.conf
lxc file push "${DIR}/../../common/http-server/index.html" ${CONTAINER}/var/www/lighttpd/index.html

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $1
lxc stop --force ${CONTAINER}
