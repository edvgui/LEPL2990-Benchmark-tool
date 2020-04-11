#!/usr/bin/env bash

# Install benchmark dependencies
sudo apt install -y \
  python3-pip \
  python3-dev \
  libcurl4-openssl-dev \
  libssl-dev

cd /opt || exit
sudo git clone https://github.com/geverartsdev/LEPL2990-Benchmark-tool.git
sudo chmod -R 777 LEPL2990-Benchmark-tool

cd LEPL2990-Benchmark-tool || exit
sudo python3 setup.py install
