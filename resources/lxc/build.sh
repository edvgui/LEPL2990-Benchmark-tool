#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
LOG_FILE="${DIR}/build.log"

build() {
  local folder=$1
  local name="alpine-${folder}"

  echo "INFO: ${name}: Building"
  "${DIR}/${folder}/build.sh" &>> "${LOG_FILE}"
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