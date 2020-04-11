#!/usr/bin/env bash

ARCH=$(arch)
BRANCH="${BRANCH:-master}"
sudo sh -c "echo 'deb http://download.opensuse.org/repositories/home:/katacontainers:/releases:/${ARCH}:/${BRANCH}/xUbuntu_$(lsb_release -rs)/ /' > /etc/apt/sources.list.d/kata-containers.list"
curl -sL  http://download.opensuse.org/repositories/home:/katacontainers:/releases:/${ARCH}:/${BRANCH}/xUbuntu_$(lsb_release -rs)/Release.key | sudo apt-key add -
sudo -E apt-get update
sudo -E apt-get -y install kata-runtime kata-proxy kata-shim

sudo -E apt-get -y install apt-transport-https ca-certificates software-properties-common
curl -sL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
arch=$(dpkg --print-architecture)
sudo -E add-apt-repository "deb [arch=${arch}] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo -E apt-get update
sudo -E apt-get -y install docker-ce=18.06.3~ce~3-0~ubuntu

cd /tmp || exit
wget https://github.com/kata-containers/runtime/releases/download/1.5.0/kata-static-1.5.0-x86_64.tar.xz
sudo tar -xvf kata-static-1.5.0-x86_64.tar.xz -C /

sudo mkdir -p /etc/docker
printf '
{
  "runtimes": {
    "kata-fc": {
      "path": "/opt/kata/bin/kata-fc"
    },
    "kata-runtime": {
      "path": "/opt/kata/bin/kata-qemu"
    }
  },
  "storage-driver": "devicemapper"
}
' | sudo tee /etc/docker/daemon.json
sudo systemctl daemon-reload
sudo systemctl restart docker