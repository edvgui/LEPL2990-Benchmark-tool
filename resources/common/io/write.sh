#!/bin/sh

SRC=$1      # Full path
DEST=$2     # Full path

cd $DEST && tar -xf $SRC

echo "Done"
