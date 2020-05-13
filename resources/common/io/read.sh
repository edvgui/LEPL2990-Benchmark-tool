#!/bin/sh

FOLDER=$1

for file in $(cd $FOLDER && ls)
do
    tmp=$(<$FOLDER/$file)
done

echo "Done"
