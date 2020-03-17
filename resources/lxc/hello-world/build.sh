#!/usr/bin/env bash

BASE="images:alpine/3.11/i386"
CONTAINER="tmp"
SNAPSHOT="export"
NAME="alpine-hello-world"

lxc image list | grep ${NAME} > /dev/null
if [ $(echo $?) -eq 0 ]; then
  echo "Deleting previous build"
  lxc image delete ${NAME}
fi

lxc launch -e ${BASE} ${CONTAINER}
lxc snapshot ${CONTAINER} ${SNAPSHOT}
lxc publish ${CONTAINER}/${SNAPSHOT} --alias ${NAME}
lxc stop ${CONTAINER}