#!/bin/sh
ping -c"$1" www.google.com | tail -n 1
