#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
LOG_FILE="${DIR}/build.log"

build() {
  local folder=$1

  docker images | grep ${folder} > /dev/null
  if [ $(echo $?) -eq 1 ]; then
    echo "ERROR: ${folder}: not found in docker images"
    return 1
  fi

  podman images | grep ${folder} > /dev/null
  if [ $(echo $?) -eq 0 ]; then
    echo "INFO: ${folder}: Deleting previous build"
    podman rmi ${foldername} &>> "${LOG_FILE}"
  fi

  echo "INFO: ${folder}: Pulling"
  podman pull "docker-daemon:${folder}:latest" &>> "${LOG_FILE}"
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
