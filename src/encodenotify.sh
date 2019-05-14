#!/bin/bash

# requires inotify-tools be installed

echo "ENCODENOTIFY: starting"

inotifywait -m -e close_write "/transcode/encode/" | while read cPATH cPARMS cFILE
do
	if [[ -f /transcode/defaultsettings.txt ]]; then
			echo "defaultsettings.txt file exists.  Using Override."
			source /transcode/defaultsettings.txt
	fi
	
	# Remove Windows special characters
	ENCODE_PROFILE=`echo "$ENCODE_PROFILE" | tr -cd "[:print:]\n"`
	
	if ! [[ $ENCODE_PROFILE  ]] ; then
			echo "ENCODE_PROFILE did not exist, using default of Fast 1080p30"
			ENCODE_PROFILE="Fast 1080p30"
	fi
    echo "ENCODENOTIFY: inotify: $cPATH  $cFILE $ENCODE_PROFILE"
    # inotify has the following format in file creating 3 arguments for cut.py instad of 1
    # <path to file> triggers <filename.ext>
    python3 encode.py "$cPATH" "$cPARMS" "$cFILE" "$ENCODE_PROFILE"  < /dev/null
done

echo "ENCODENOTIFY: ending"
