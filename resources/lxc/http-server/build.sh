#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"
NAME="alpine-http-server"

lxc image list | grep ${NAME} > /dev/null
if [ $(echo $?) -eq 0 ]; then
  echo "Deleting previous build"
  lxc image delete ${NAME}
fi

lxc launch -e ${BASE} ${CONTAINER}

lxc exec ${CONTAINER} -- apk update
lxc exec ${CONTAINER} -- apk add lighttpd
lxc exec ${CONTAINER} -- rc-update add lighttpd default
lxc file push "${DIR}/../../common/http-server/index.html" ${CONTAINER}/var/www/localhost/htdocs/index.html

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias ${NAME}
lxc stop ${CONTAINER}