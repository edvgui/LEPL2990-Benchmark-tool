#!/usr/bin/env bash

DEVICE1=/dev/sdb1
DEVICE2=/dev/sdb2

read -rs -p 'Enter target sudo password: ' PASSWORD
echo ""

mkdir -p logs

# Deploy benchmark tool
echo -ne "[$(date)] Deploying benchmark tool... "
ansible-playbook -i target.ini deploy-playbooks/deploy-benchmark.playbook.yaml \
  --extra-vars "ansible_become_pass=$PASSWORD" > logs/cgroupv1-docker.log
if [ "$?" -eq "0" ]; then
  echo "OK"
else
  echo ""
  exit 1
fi

###
# Docker tests
for runtime in runc crun qemu; do
  for driver in aufs btrfs overlay vfs zfs; do
    logfile="logs/docker-${runtime}-${driver}.log"
    echo -ne "[$(date)] Docker $runtime $driver... "

    ansible-playbook -i target.ini config-playbooks/docker-${runtime}-${driver}.playbook.yaml \
      --extra-vars "ansible_become_pass=$PASSWORD" \
      -e device=$DEVICE1 > $logfile
    if [ $? -eq 0 ]; then
      echo -ne "CONF_OK... "
      for image in alpine centos; do
        ansible-playbook -i target.ini run-playbooks/run-benchmark.playbook.yaml \
          --extra-vars "ansible_become_pass=$PASSWORD" \
          -e tests="--all" \
          -e solution=docker \
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

    ansible-playbook -i target.ini cleanup-playbooks/docker-${driver}.playbook.yaml \
      --extra-vars "ansible_become_pass=$PASSWORD" >> $logfile
    if [ $? -eq 0 ]; then
      echo "CLEAN_OK"
    else
      echo "CLEAN_ERR"
    fi
  done
done

for runtime in runc crun qemu firecracker; do
  driver="devicemapper"
  logfile="logs/docker-${runtime}-${driver}.log"
  echo -ne "[$(date)] Docker $runtime $driver... "

  ansible-playbook -i target.ini config-playbooks/docker-${runtime}-${driver}.playbook.yaml \
    --extra-vars "ansible_become_pass=$PASSWORD" \
    -e device=$DEVICE1 \
    -e lvm_device=$DEVICE2 > $logfile
  if [ $? -eq 0 ]; then
    echo -ne "CONF_OK... "
    for image in alpine centos; do
      ansible-playbook -i target.ini run-playbooks/run-benchmark.playbook.yaml \
        --extra-vars "ansible_become_pass=$PASSWORD" \
        -e tests="--all" \
        -e solution=docker \
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

  ansible-playbook -i target.ini cleanup-playbooks/docker-${driver}.playbook.yaml \
    --extra-vars "ansible_become_pass=$PASSWORD" >> $logfile
  if [ $? -eq 0 ]; then
    echo "CLEAN_OK"
  else
    echo "CLEAN_ERR"
  fi
done
