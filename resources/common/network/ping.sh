#!/bin/sh

ping -c1 1.1.1.1 > output
if [ $(echo $?) -ne 0 ]; then
    cat output 1>&2
    exit 1
fi
cat output | tail -n 1
