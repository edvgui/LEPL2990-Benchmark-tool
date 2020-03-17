#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
LOG_FILE="${DIR}/build.log"

build() {
  local folder=$1
  local name="alpine-${folder}"

  docker images | grep ${name} > /dev/null
  if [ $(echo $?) -eq 1 ]; then
    echo "ERROR: ${name}: not found in docker images"
    return 1
  fi

  podman images | grep ${name} > /dev/null
  if [ $(echo $?) -eq 0 ]; then
    echo "INFO: ${name}: Deleting previous build"
    podman rmi ${name} &>> "${LOG_FILE}"
  fi

  echo "INFO: ${name}: Pulling"
  podman pull "docker-daemon:${name}:latest" &>> "${LOG_FILE}"
}

echo "" > "${LOG_FILE}"
for arg in "$@"
do
  case ${arg} in
    -a| --all)
      for folder in $(cd ${DIR} && ls -d */ | cut -f1 -d'/')
      do
        build "${folder}"
      done
      ;;
    *)
      build "${arg}"
      ;;
  esac
done
echo "Done"