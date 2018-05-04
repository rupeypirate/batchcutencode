#!/usr/bin/env python3

# ---------------------------------------------------------------------------
#
# encode.py
#
# Requires the following packages to be installed:  HandBrakeCLI
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


encodedir="/transcode/encode"
completedir="/transcode/complete"
filefilter= ('.mp4', '.mkv', '.avi', '.ts')

handbrake = "/usr/bin/HandBrakeCLI"

print ("ENCODE: Initiating script: " + str(sys.argv[0]))
print ("ENCODE: Number of arguments: " + str(len(sys.argv)))
print ("ENCODE: The arguments are: " + str(sys.argv))

if len(sys.argv) != 4:
	print ("ENCODE: " + sys.argv[0] + " has wrong number of arguments, exiting")
	print ("ENCODE: There should be 4 arguements")
	print ("ENCODE: " + str(sys.argv))
	sys.exit(1)

# inotify puts out a single FILE perameter that looks like 3 parameters:	/home/eric/test/ CLOSE_WRITE,CLOSE midseason1.mp4
# sys.argv[0] application file name (this app)
# sys.argv[1] directory the video file is in
# sys.argv[2] triggers
# sys.argv[3] video file name


encodefiledirectory = sys.argv[1]
encodefiletrigger = sys.argv[2]
encodefilename = sys.argv[3]
encodeprofile = sys.argv[4]

# Due to inotify passing this in, we can process sub directories also.    
ff=os.path.join(encodefiledirectory, encodefilename)
print("ENCODE: full file path: " + ff)

if not os.path.isfile(ff) :
	print ("ENCODE: file does not exist, exiting: " + encodefilename)
	sys.exit(1)

if not encodefilename.lower().endswith(filefilter):
	print ("ENCODE: file is not correct type, exiting: " + encodefilename)
	sys.exit(1)

#HandbrakeCLI will encode to mp4, so need to set the completedir target with filename have an mp4 extension	
completefilename = (completedir + "/" + encodefilename).rsplit(".", 1)[0] + '.mp4'
print("ENCODE: completefilename: " + str(completefilename))

if encodeprofile = "" :
	encodeprofile = "Fast 1080p30"

print("ENCODE: encodeprofile: " + str(encodeprofile))

# Use HandbrakeCLI to encode files in the encode directory
#$HANDBRAKECLI -i "$file" -o "$completedir/$filename" --preset="Normal"
#avcommand= handbrake + " -i \"" + ff + "\" -o \"" + completefilename + "\" --preset=\"Normal\""
avcommand= handbrake + " -i \"" + ff + "\" -o \"" + completefilename + "\" --preset=\"" + encodeprofile + "\""
print("ENCODE:handbrake command: " + avcommand)

avprocess = subprocess.Popen(avcommand, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = avprocess.communicate()
exitcode = avprocess.returncode
print("ENCODE: exitcode: " + str(exitcode))

# Check error code
if str(exitcode) != "0":
	sys.exit(exitcode)

#Remove original file in cut directory
os.remove(ff)
print("ENCODE: deleted file: " + str(ff))

