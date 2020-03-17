#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
LOG_FILE="${DIR}/build.log"

build() {
  local folder=$1
  local name="centos-${folder}"

  docker images | grep ${name} > /dev/null
  if [ $(echo $?) -eq 0 ]; then
    echo "INFO: ${name}: Deleting previous build"
    docker rmi ${name} &>> "${LOG_FILE}"
  fi

  echo "INFO: ${name}: Building"
  docker build -t "${name}" -f "${DIR}/${folder}/Dockerfile" "${DIR}/../../" &>> "${LOG_FILE}"
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