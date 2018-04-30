#!/bin/bash

# requires inotify-tools be installed

#inotifywait -m -e close_write "/home/eric/test/" | while read FILE
inotifywait -mr -e close_write "/transcode/cut/" | while read FILE
do
    echo "inotify: close_write: $FILE"
    # inotify has the following format in file creating 3 arguments for cut.py instad of 1
    # <path to file> triggers <filename.ext> 
    python3 cut.py $FILE 5 5
done

