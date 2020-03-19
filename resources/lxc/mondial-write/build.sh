#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"
NAME="alpine-mondial-write"

lxc image list | grep ${NAME} > /dev/null
if [ $(echo $?) -eq 0 ]; then
  echo "Deleting previous build"
  lxc image delete ${NAME}
fi

lxc launch -e ${BASE} ${CONTAINER}

lxc exec ${CONTAINER} -- apk update
lxc exec ${CONTAINER} -- apk add sqlite
lxc exec ${CONTAINER} -- mkdir /root/src
lxc file push "${DIR}/../../common/sqlite/mondial-orig.db" ${CONTAINER}/root/mondial-orig.db
lxc file push "${DIR}/../../common/sqlite/write.sqlite" ${CONTAINER}/root/write.sqlite
lxc file push "${DIR}/../../common/sqlite/sqlite.sh" ${CONTAINER}/root/sqlite.sh
lxc exec ${CONTAINER} -- chmod +x /root/sqlite.sh

lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias ${NAME}
lxc stop ${CONTAINER}