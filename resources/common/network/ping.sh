#!/bin/sh
ping -c"$1" 1.1.1.1 | tail -n 1
