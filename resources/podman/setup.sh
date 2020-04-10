#!/usr/bin/env bash

err=$(podman info 2>&1)
result=$(echo $?)

# Check that docker is installed
if [ $result -eq 127 ]; then
    echo "INFO: Podman is missing"
    echo "INFO: Installing Podman"
    
    source /etc/os-release > /dev/null
    sudo sh -c "echo 'deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"
    curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key | sudo apt-key add -
    sudo apt-get update -qq > /dev/null
    sudo apt-get -qq -y install podman > /dev/null
elif [ $result -eq 0 ]; then
    echo "INFO: Podman is correctly setup"
else
    1>&2 echo "ERROR: Unknown error code $result"
    1>&2 echo "ERROR: ${err}"
fi
