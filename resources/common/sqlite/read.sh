#!/bin/sh
sqlite3 src/mondial-orig.db < src/read.sqlite > /dev/null
echo 'Done'
