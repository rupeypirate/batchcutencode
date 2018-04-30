#!/usr/bin/env python3

# ---------------------------------------------------------------------------
#
# cut.py
#
# Requires the following packages to be installed:  ffmpeg
#         
# This takes command line inputs that are meant to work with inotify
#
# ---------------------------------------------------------------------------

import os
import time
import sys
import subprocess
import fnmatch
import re
import atexit


#cutdir="/transcode/cut"
encodedir="/transcode/encode"

filefilter= ('.mp4', '.mkv', '.avi', '.ts')

ffmpeg = "/usr/bin/ffmpeg"
ffprobe = "/usr/bin/ffprobe"

print ("CUT: Initiating script: " + str(sys.argv[0]))
print ("CUT: Number of arguments: " + str(len(sys.argv)))
print ("CUT: The arguments are: " + str(sys.argv))

if len(sys.argv) != 6:
	print ("CUT: " + sys.argv[0] + " has wrong number of arguments, exiting")
	print ("CUT: There should be 6 arguements")
	print ("CUT: " + str(sys.argv))
	sys.exit(1)

# inotify puts out a single FILE perameter that looks like 3 parameters:	/home/eric/test/ CLOSE_WRITE,CLOSE midseason1.mp4
# sys.argv[0] application file name (this app)
# sys.argv[1] directory the video file is in
# sys.argv[2] triggers
# sys.argv[3] video file name
# sys.argv[4] seconds to cut off beginning of video
# sys.argv[5] seconds to cut off end of video

cutfiledirectory = sys.argv[1]
cutfiletrigger = sys.argv[2]
cutfilename = sys.argv[3]
frontcutseconds = int(sys.argv[4])
endcutseconds = int(sys.argv[5])



# Due to inotify passing this in, we can process sub directories also.    
ff=os.path.join(cutfiledirectory, cutfilename)
print("CUT: full file path: " + ff)

if not os.path.isfile(ff) :
	print ("CUT: file does not exist, exiting: " + cutfilename)
	sys.exit(1)

if not cutfilename.lower().endswith(filefilter):
	print ("CUT: file is not correct type, exiting: " + cutfilename)
	sys.exit(1)


# Call ffprobe to get the duration to cut off the end.
avcommand= ffprobe + " -i \"" + ff + "\" -show_entries format=duration -v quiet -of csv=\"p=0\""
print("CUT:ffprobe command: " + avcommand)
avprocess = subprocess.Popen(avcommand, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = avprocess.communicate()
exitcode = avprocess.returncode
print("CUT: exitcode: " + str(exitcode))
#  Check error code, continue loop it not 0
if str(exitcode) != "0":
	sys.exit(1)

duration_seconds = output
#print(output)
#print(error)
print("CUT: duration_seconds: " + duration_seconds)

#this calculated the total video time with frontcutseconds seconds cut off the front
# and endcutseconds seconds cut off the back
endcut= float(duration_seconds) - float(frontcutseconds) - float(endcutseconds)
print("CUT: endcut: " + str(endcut))

if endcut <= 0:
	print("CUT: cut time is bigger than the length of the video: " + str(endcut))
	sys.exit(1)


# in ffmpeg -t is time from current cut postition (or -ss position)
# -to is from the begining
# -t overrides -to

encodefilename = encodedir + "/" + cutfilename 
print("CUT: encodefilename: " + str(encodefilename))
sstime = time.strftime('%H:%M:%S', time.gmtime(frontcutseconds))
avcommand= ffmpeg + " -y -ss " + sstime + " -t "+ str(endcut) + " -i \"" + ff + "\" -acodec copy -vcodec copy -async 1 \"" + encodefilename + "\""
print("CUT:ffmpeg command: " + avcommand)
avprocess = subprocess.Popen(avcommand, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = avprocess.communicate()
exitcode = avprocess.returncode
print("CUT: exitcode: " + str(exitcode))

#  Check error code, continue loop it not 0 - does not delete original file
if str(exitcode) != "0":
	sys.exit(exitcode)

#Remove original file in cut directory
os.remove(ff)
print("CUT: deleted file: " + str(ff))
