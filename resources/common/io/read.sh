#!/bin/sh

FOLDER=$1

for file in $(cd $FOLDER && ls)
do
    cat $FOLDER/$file > /dev/null
done

echo "Done"
