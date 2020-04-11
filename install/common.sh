#!/usr/bin/env bash

# Install benchmark dependencies
sudo apt-get install -y \
  python3-pip \
  python3-dev \
  libcurl4-openssl-dev \
  libssl-dev

cd /opt/LEPL2990-Benchmark-tool || exit
sudo python3 setup.py install

# Generate databases
sudo apt-get install -y \
  mysql-client \
  sqlite3 \
  unzip
cd resources/common/sqlite || exit
chmod +x create-db.sh
./create-db.sh