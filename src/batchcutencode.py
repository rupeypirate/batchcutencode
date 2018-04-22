#!/usr/bin/env python3

# ---------------------------------------------------------------------------
#
# Batchcutencode.py
#
# Requires the following packages to be installed:
#          ffmpeg
#          HandBrakeCLI
#
#
# ---------------------------------------------------------------------------

import os
import time
import sys
import subprocess
import fnmatch
import re
import atexit


cutdir="/transcode/cut"
encodedir="/transcode/encode"
completedir="/transcode/complete"
filefilter= ['*.mp4', '*.MP4', '*.mkv', '*.MKV', '*.avi', '*.AVI"']

ffmpeg = "/usr/bin/ffmpeg"
ffprobe = "/usr/bin/ffprobe"
handbrake = "/usr/bin/HandBrakeCLI"

def debugprint( key, value ):
   print ("DEBUG: " +key+ ":" + str(value))
   return


# Is Script already running?
pid = str(os.getpid())
pidfile = "/tmp/batchcutencode.pid"

if os.path.isfile(pidfile):
    print (pidfile + " already exists, exiting")
    sys.exit()

f= open(pidfile, 'w')
f.write(pid)
f.close()

def exit_handler(removefile):
        print ('Program exiting, Removing lock file')
        if os.path.isfile(removefile):
                os.unlink(removefile)

atexit.register(exit_handler, pidfile)

#----------------------------------------------------------------------------
#---                                                                      ---
#---    Cut 5 seconds off fron and end of files in $cutfile directory     ---
#---                                                                      ---
#----------------------------------------------------------------------------

# transform glob patterns to regular expressions for file filter
filefilter = r'|'.join([fnmatch.translate(x) for x in filefilter])


for root, dirs, filenames in os.walk(cutdir):
        #apply file filter
        #filenames = [os.path.join(root, h) for h in filenames] #turning this on addes full path to filenames, but will break code below since it is based on filename only
        filenames = [h for h in filenames if re.match(filefilter, h)]
        for f in filenames:
                debugprint("CUT: root", root)
                debugprint("CUT:file", f)
                ff=os.path.join(root, f)
                debugprint("CUT: full file path", ff)

                # Call ffprobe to get the duration to cut off the end.
                avcommand= ffprobe + " -i \"" + ff + "\" -show_entries format=duration -v quiet -of csv=\"p=0\""
                debugprint("CUT:ffprobe command", avcommand)
                avprocess = subprocess.Popen(avcommand, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = avprocess.communicate()
                exitcode = avprocess.returncode
                debugprint("CUT: exitcode", str(exitcode))
                #  Check error code, continue loop it not 0
                if str(exitcode) != "0":
                        continue

                duration_seconds = output
                #print(output)
                #print(error)
                debugprint("CUT: duration_seconds", duration_seconds)

        #this calculated the total video time with 5 seconds cut off the front
        # and 5 seconds cut off the back
                endcut= float(duration_seconds) - 10.0
                debugprint("CUT: endcut", str(endcut))

                # subtract the time off the total durection to get to the end time
        # in ffmpeg -t is time from current cut postition (or -ss position)
        # -to is from the begining
        # -t overrides -to
                encodefilename = encodedir + "/" + f
                debugprint("CUT: encodefilename", str(encodefilename))
                avcommand= ffmpeg + " -y -ss 00:00:05 -t "+ str(endcut) + " -i \"" + ff + "\" -acodec copy -vcodec copy -async 1 \"" + encodefilename + "\""
                debugprint("CUT:ffmpeg command", avcommand)
                avprocess = subprocess.Popen(avcommand, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = avprocess.communicate()
                exitcode = avprocess.returncode
                debugprint("CUT: exitcode", str(exitcode))

                #  Check error code, continue loop it not 0 - does not delete original file
                if str(exitcode) != "0":
                        continue

                #Remove original file in cut directory
                os.remove(ff)
                debugprint("CUT: deleted file", str(ff))

#----------------------------------------------------------------------------
#---                                                                      ---
#---    encode files in the encodefile directory                          ---
#---                                                                      ---
#----------------------------------------------------------------------------

for root, dirs, filenames in os.walk(encodedir):
        #apply file filter
        #filenames = [os.path.join(root, h) for h in filenames] #turning this on addes full path to filenames, but will break code below since it is based on filename only
        filenames = [h for h in filenames if re.match(filefilter, h)]
        for f in filenames:
                debugprint("ENCODE: root", root)
                debugprint("ENCODE:file", f)
                ff=os.path.join(root, f)
                debugprint("ENCODE: full file path", ff)

            # Use HandbrakeCLI to encode all files in the encode directory
                completefilename = (completedir + "/" + f).rsplit(".", 1)[0] + '.mp4'
                debugprint("ENCODE: completefilename", str(completefilename))

                #$HANDBRAKECLI -i "$file" -o "$completedir/$filename" --preset="Normal"
                avcommand= handbrake + " -i \"" + ff + "\" -o \"" + completefilename + "\" --preset=\"Normal\""
                debugprint("ENCODE:handbrake command", avcommand)

                avprocess = subprocess.Popen(avcommand, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = avprocess.communicate()
                exitcode = avprocess.returncode
                debugprint("ENCODE: exitcode", str(exitcode))

                #  Check error code, continue loop it not 0 - does not delete original file
                if str(exitcode) != "0":
                        continue

                #Remove original file in cut directory
                os.remove(ff)
                debugprint("ENCODE: deleted file", str(ff))

