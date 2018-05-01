#!/bin/bash

# requires inotify-tools be installed

echo "encodenotify.sh starting"

#inotifywait -m -e close_write "/home/eric/test/" | while read FILE
inotifywait -m -e close_write "/transcode/encode/" | while read FILE
do
    echo "inotify: $FILE"
    # inotify has the following format in file creating 3 arguments for cut.py instad of 1
    # <path to file> triggers <filename.ext>
    python3 encode.py $FILE
done

echo "encodenotify.sh ending"