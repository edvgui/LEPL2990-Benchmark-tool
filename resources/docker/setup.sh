#!/usr/bin/env bash

err=$(docker info 2>&1)
result=$(echo $?)

# Check that docker is installed
if [ $result -eq 127 ]; then
    echo "INFO: Docker is missing"
    echo "INFO: Installing Docker"
    
    sudo -E apt-get -y install apt-transport-https ca-certificates software-properties-common > /dev/null
    curl -sL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    arch=$(dpkg --print-architecture)
    sudo -E add-apt-repository "deb [arch=${arch}] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /dev/null
    sudo -E apt-get update > /dev/null
    sudo -E apt-get -y install docker-ce > /dev/null
    sudo usermod -aG docker $USER
    docker --version
    echo "INFO: You neet to logout and log back in"
elif [ $result -eq 1 ]; then
    echo "INFO: Adding current user to docker group"
    sudo usermod -aG docker $USER
    echo "INFO: You neet to logout and log back in"
elif [ $result -eq 0 ]; then
    echo "INFO: Docker is correctly setup"
else
    1>&2 echo "ERROR: Unknown error code $result"
    1>&2 echo "ERROR: ${err}"
fi
