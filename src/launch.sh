#!/bin/bash

echo "launch.sh starting"

# Launch in background
/app/cutnotify.sh &

# launch in forground... this must stay running of docer will stop
/app/encodenotify.sh 

echo "launch.sh exiting"
