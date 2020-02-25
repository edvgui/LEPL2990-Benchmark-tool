#!/bin/sh
sqlite3 src/mondial-orig.db < src/queries.sql > /dev/nul
echo 'Done'
