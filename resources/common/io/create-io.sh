#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

generate() {
    local name=$1
    local amount=$2
    
    mkdir -p $DIR/$name
    for (( I=1; I<=amount; I++ ))
    do
        cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 2048 | head -n 1 > $DIR/$name/$I.txt
        progress=$((I*100/amount))
        echo -ne "Generating $name ($progress %)\r"
    done
    echo ""
    
    cd $DIR && tar -cf $name.tar $name
}

generate xs 10
generate sm 100
generate md 1000
generate lg 10000
# generate xl 100000

echo "Done"
