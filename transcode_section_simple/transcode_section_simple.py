# simple program for transcoding portions of a video
# where ffmpeg is called to do the actual transcoding
import sys
import argparse
import os
import subprocess
import string

# checking if all arguments are given
if len(sys.argv) != 4:
    print("Usage : transcode.py input_filename startinsec endinsec")
    sys.exit()

input_filepath = str(sys.argv[1])
startinsec = int(sys.argv[2])
endinsec = int(sys.argv[3])

assert ((endinsec - startinsec) >= 0)

input_filename = input_filepath.split("/")[-1]
output_filename = "out_" + input_filename

cmd = ["ffmpeg", "-ss", str(startinsec), "-t", str(endinsec - startinsec), "-i", input_filepath, "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-strict", "experimental", "out.mp4"]
proc = subprocess.Popen(cmd)
proc.communicate()

retcode = proc.returncode
if not retcode == 0:
    raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))
