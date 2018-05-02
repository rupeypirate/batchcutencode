#!/bin/bash

# requires inotify-tools be installed

echo "CUTNOTIFY: starting"

inotifywait -mr -e close_write "/transcode/cut/" | while read cPATH cOPTIONS cFILE
do
    echo "CUTNOTIFY: inotify: close_write: $cPATH  $cFILE"
    # inotify has the following format in file creating 3 arguments for cut.py instad of 1
    # <path to file> triggers <filename.ext> 
    python3 cut.py "$cPATH" "$cOPTIONS" "$cFILE" 5 5 < /dev/null
done

echo "CUTNOTIFY: exiting"
