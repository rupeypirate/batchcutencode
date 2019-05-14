#!/bin/bash

# requires inotify-tools be installed

echo "CUTNOTIFY: starting"



inotifywait -mr -e close_write "/transcode/cut/" | while read cPATH cOPTIONS cFILE
do
	if [[ -f /transcode/defaultsettings.txt ]]; then
			echo "defaultsettings.txt file exists.  Using Override."
			source /transcode/defaultsettings.txt
	fi
	
	re='^[0-9]+$'
	if ! [[ $SECONDS_FRONT =~ $re ]] ; then
			echo "SECONDS_FRONT did not exist, using default of 5 SECONDS"
			SECONDS_FRONT=5
	fi
	if ! [[ $SECONDS_END =~ $re ]] ; then
		echo "SECONDS_END did not exist, using default of 5 SECONDS"
			SECONDS_END=5
	fi
	
    echo "CUTNOTIFY: inotify: close_write: $cPATH  $cFILE ${SECONDS_FRONT} ${SECONDS_END}"
    # inotify has the following format in file creating 3 arguments for cut.py instad of 1
    # <path to file> triggers <filename.ext> 
    python3 cut.py "$cPATH" "$cOPTIONS" "$cFILE" ${SECONDS_FRONT} ${SECONDS_END} < /dev/null
done

echo "CUTNOTIFY: exiting"
