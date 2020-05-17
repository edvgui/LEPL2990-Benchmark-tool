#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

NETWORK="lxdbr0"
BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"


lxc launch -e -n ${NETWORK} ${BASE} ${CONTAINER}

lxc exec ${CONTAINER} -- apk update
lxc exec ${CONTAINER} -- apk add lighttpd
lxc file push "${DIR}/../../common/http-server/index.html" ${CONTAINER}/var/www/localhost/htdocs/index.html

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias $1
lxc stop ${CONTAINER}
