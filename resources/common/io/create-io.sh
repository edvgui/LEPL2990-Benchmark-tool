#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )

generate() {
    local name=$1
    local amount=$2
    
    rm -rf $DIR/$name
    mkdir -p $DIR/$name

    for (( I=1; I<=amount; I++ ))
    do
        tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w 4095 | head -n 1 > $DIR/$name/$I.txt
        progress=$((I*100/amount))
        echo -ne "Generating $name ($progress %)\r"
    done
    echo ""
    
    cd $DIR && tar -cf $name.tar $name
}

echo "Compiling read executable"
gcc -o read read.c


generate xs 10
generate sm 100
generate md 1000
generate lg 10000
generate xl 100000

echo "Done"
