#!/usr/bin/env bash

DEVICE=/dev/sdb1

read -rs -p 'Enter target sudo password: ' PASSWORD
echo ""

mkdir -p logs

# Deploy benchmark tool
echo -ne "[$(date)] Deploying benchmark tool... "
ansible-playbook -i target.ini deploy-playbooks/deploy-benchmark.playbook.yaml \
  --extra-vars "ansible_become_pass=$PASSWORD" > logs/cgroupv1-lxd.log
if [ "$?" -eq "0" ]; then
  echo "OK"
else
  echo ""
  exit 1
fi

###
# Podman tests
for runtime in crun; do
  for driver in btrfs overlay vfs; do
    logfile="logs/podman-${runtime}-${driver}.log"
    echo -ne "[$(date)] Podman $runtime $driver... "

    ansible-playbook -i target.ini config-playbooks/podman-${runtime}-${driver}.playbook.yaml \
      --extra-vars "ansible_become_pass=$PASSWORD" \
      -e device=$DEVICE > $logfile
    if [ $? -eq 0 ]; then
      echo -ne "CONF_OK... "
      for image in alpine; do
        ansible-playbook -i target.ini run-playbooks/run-benchmark.playbook.yaml \
          --extra-vars "ansible_become_pass=$PASSWORD" \
          -e tests="--all" \
          -e solution=podman \
          -e image=${image} \
          -e runtime=${runtime} \
          -e tag=${driver} >> $logfile
      done
      if [ $? -eq 0 ]; then
        echo -ne "RUN_OK... "
      else
        echo -ne "RUN_ERR... "
      fi
    else
      echo -ne "CONF_ERR... "
    fi

    ansible-playbook -i target.ini cleanup-playbooks/podman-${driver}.playbook.yaml \
      --extra-vars "ansible_become_pass=$PASSWORD" >> $logfile
    if [ $? -eq 0 ]; then
      echo "CLEAN_OK"
    else
      echo "CLEAN_ERR"
    fi
  done
done