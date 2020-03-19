#!/bin/sh
sqlite3 "$1" < "$2" > /dev/null
if [ $(echo $?) -eq 0 ]; then
  echo 'Done'
else
  echo 'Error'
fi
