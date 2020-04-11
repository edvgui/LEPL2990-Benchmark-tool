#!/usr/bin/env bash

sudo -E apt-get -y install apt-transport-https ca-certificates software-properties-common
curl -sL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
arch=$(dpkg --print-architecture)
sudo -E add-apt-repository "deb [arch=${arch}] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo -E apt-get update
sudo -E apt-get -y install docker-ce

sudo -E apt-get -y install \
  uidmap \
  golang-go

cd /tmp || exit
wget https://github.com/rootless-containers/rootlesskit/releases/download/v0.9.3/rootlesskit-x86_64.tar.gz
tar -xzf rootlesskit-x86_64.tar.gz
sudo mv rootlesskit /usr/bin/rootlesskit
sudo mv rootlessctl /usr/bin/rootlessctl

wget https://github.com/rootless-containers/slirp4netns/releases/download/v1.0.0/slirp4netns-x86_64
sudo mv slirp4netns-x86_64 /usr/bin/slirp4netns
sudo chmod +x /usr/bin/slirp4netns

echo "net.ipv4.ping_group_range=0 2000000" | sudo tee /etc/sysctl.d/10-ipv4-ping.conf