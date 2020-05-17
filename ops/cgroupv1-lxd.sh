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
# LXD tests
runtime="lxc"
for driver in btrfs dir lvm zfs; do
  logfile="logs/lxd-${runtime}-${driver}.log"
  echo -ne "[$(date)] LXD $runtime $driver... "

  ansible-playbook -i target.ini config-playbooks/lxd-${runtime}-${driver}.playbook.yaml \
    --extra-vars "ansible_become_pass=$PASSWORD" \
    -e device=$DEVICE > $logfile
  if [ $? -eq 0 ]; then
    echo -ne "CONF_OK... "
    for image in alpine; do
      ansible-playbook -i target.ini run-playbooks/run-benchmark.playbook.yaml \
        --extra-vars "ansible_become_pass=$PASSWORD" \
        -e tests="--all" \
        -e solution=lxd \
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

  ansible-playbook -i target.ini cleanup-playbooks/lxd-${driver}.playbook.yaml \
    --extra-vars "ansible_become_pass=$PASSWORD" >> $logfile
  if [ $? -eq 0 ]; then
    echo "CLEAN_OK"
  else
    echo "CLEAN_ERR"
  fi
done