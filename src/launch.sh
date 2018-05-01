#!/bin/bash

echo "launch.sh starting"
/app/cutnotify.sh &
/app/encodenotify.sh &

echo "launch.sh exiting"