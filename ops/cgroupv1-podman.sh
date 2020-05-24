#!/usr/bin/env bash

DEVICE1=/dev/sdb1
DEVICE2=/dev/sdb2

read -rs -p 'Enter target sudo password: ' PASSWORD
echo ""

mkdir -p logs

# Deploy benchmark tool
echo -ne "[$(date)] Deploying benchmark tool... "
ansible-playbook -i target.ini deploy-playbooks/deploy-benchmark.playbook.yaml \
  --extra-vars "ansible_become_pass=$PASSWORD" \
  -e skip_lxd_images=1 > logs/cgroupv1-podman.log
if [ "$?" -eq "0" ]; then
  echo "OK"
else
  echo ""
  exit 1
fi

###
# Podman tests
for runtime in runc; do
  for driver in aufs btrfs overlay vfs zfs; do
    logfile="logs/podman-${runtime}-${driver}.log"
    echo -ne "[$(date)] Podman $runtime $driver... "

    ansible-playbook -i target.ini config-playbooks/podman-${runtime}-${driver}.playbook.yaml \
      --extra-vars "ansible_become_pass=$PASSWORD" \
      -e benchmark_user='root' \
      -e benchmark_group='root' \
      -e device=$DEVICE1 > $logfile
    if [ $? -eq 0 ]; then
      echo -ne "CONF_OK... "
      for image in alpine centos; do
        ansible-playbook -i target.ini run-playbooks/run-benchmark.playbook.yaml \
          --extra-vars "ansible_become_pass=$PASSWORD" \
          -e benchmark_user='root' \
          -e benchmark_group='root' \
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
      --extra-vars "ansible_become_pass=$PASSWORD" \
      -e benchmark_user='root' >> $logfile
    if [ $? -eq 0 ]; then
      echo "CLEAN_OK"
    else
      echo "CLEAN_ERR"
    fi
  done
done