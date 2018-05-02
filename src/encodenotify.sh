#!/bin/bash

# requires inotify-tools be installed

echo "ENCODENOTIFY: starting"

inotifywait -m -e close_write "/transcode/encode/" | while read cPATH cPARMS cFILE
do
    echo "ENCODENOTIFY: inotify: $cPATH  $cFILE"
    # inotify has the following format in file creating 3 arguments for cut.py instad of 1
    # <path to file> triggers <filename.ext>
    python3 encode.py "$cPATH" "$cPARMS" "$cFILE" < /dev/null
done

echo "ENCODENOTIFY: ending"
