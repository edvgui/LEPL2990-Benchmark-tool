#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
LOG_FILE="${DIR}/build.log"

build() {
  local folder=$1
  
  lxc image list | grep ${folder} &> /dev/null
  if [ $(echo $?) -eq 0 ]; then
    echo "INFO: ${folder}: Deleting previous build"
    lxc image delete ${folder} >> ${LOG_FILE}
  fi

  echo "INFO: ${folder}: Building"
  ${DIR}/${folder}/build.sh ${folder} &>> ${LOG_FILE}
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
