#!/bin/bash

# requires inotify-tools be installed

echo "ENCODENOTIFY: starting"

if ! [[ $ENCODE_PROFILE  ]] ; then
        ENCODE_PROFILE="Fast 1080p30"
fi


inotifywait -m -e close_write "/transcode/encode/" | while read cPATH cPARMS cFILE
do
    echo "ENCODENOTIFY: inotify: $cPATH  $cFILE $ENCODE_PROFILE"
    # inotify has the following format in file creating 3 arguments for cut.py instad of 1
    # <path to file> triggers <filename.ext>
    python3 encode.py "$cPATH" "$cPARMS" "$cFILE" "$ENCODE_PROFILE"  < /dev/null
done

echo "ENCODENOTIFY: ending"
