#!/usr/bin/env bash

sudo apt-get install -y lxd zfsutils-linux > /dev/null
sudo usermod -aG lxd $USER
lxd init
