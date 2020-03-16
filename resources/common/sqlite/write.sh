#!/bin/sh
sqlite3 src/mondial-orig.db < src/write.sqlite > /dev/null
echo 'Done'
