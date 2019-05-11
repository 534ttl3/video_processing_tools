# This code reads an m3u file and
# sequentially calls ffmpeg with some options to transcode the given portions
# of source files given therein
# ------ before executing this script, one may do this -----
# $ find -name "* *" -type d | rename 's/ /_/g'
# ------ then one may execute the script -------
# Usage: $ python m3utranscode.py input_filepath
# ------ after executing the script, one may do this -----
# merge mp4 files together:
# first create an input.txt file like
# $ find . -name "*.mp4" > input.txt
# then make the input.txt file look like this
# file '/path/to/input1.mp4'
# file '/path/to/input2.mp4'
# file '/path/to/input3.mp4'
#
# without renaming them, one may use this command to accomplish
# the two above steps all in one command
# $ find . -name "*.mp4" | sort | sed "s/^/file '/;s/$/'/;s/\.\///" > input.txt
#
# to randomly shuffle lines in a text file, one may use
# $ shuf -o File.txt < File.txt
#
# to concatenate the source files listed in input.txt, one may do
# $ ffmpeg -f concat -i input.txt -c copy output.mp4
# $ shuf -o input.txt < input.txt && ffmpeg -f concat -i input.txt -c copy output$(echo $RANDOM).mp4
#
# all-in-one
# find . -name "*.mp4" | sort | sed "s/^/file '/;s/$/'/;s/\.\///" > input.txt && shuf -o input.txt < input.txt && ffmpeg -f concat -i input.txt -c copy output$(shuf -i 0-10000 -n 1).mp4

import sys
import argparse
import os
import subprocess
import string
import re  # regular expressions, extraction of data from file

def get_relative_dirpath_with_slash(relative_filepath):
    dirpath_pattern = re.compile(r".*\/")
    dirpath_list = dirpath_pattern.findall(relative_filepath)

    if isinstance(dirpath_list, list):
        if len(dirpath_list) > 0:
            return dirpath_list[0]
    return ""

def transcodevideo(filepath, startinsec, endinsec):
    assert ((endinsec - startinsec) >= 1 )

    # get filename from filepath
    if not os.path.exists(get_relative_dirpath_with_slash(filepath) + "/transcoded"):
        os.makedirs(get_relative_dirpath_with_slash(filepath) + "/transcoded")

    output_filename = ("z_out_" +
                      os.path.splitext(os.path.basename(filepath))[0] +
                      "_" + str(startinsec) + "_to_" + str(endinsec)
                      + "." + filepath.split(".")[-1])
    output_filepath = get_relative_dirpath_with_slash(filepath) + "transcoded/" + output_filename

    cmd = ["ffmpeg",
            "-ss", str(startinsec),
            "-t", str(endinsec - startinsec),
            "-i", filepath,
            "-c:v", "libx264",
            "-crf", "20",  # quality: 0: lossless, 50: worst
            "-c:a", "aac",
            "-strict", "experimental",
            output_filepath]
    proc = subprocess.Popen(cmd)
    proc.communicate()

    retcode = proc.returncode
    if not retcode == 0:
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

def main():
    # checking if all arguments are given
    if len(sys.argv) != 2:
        print("Usage : python m3utranscode.py input_filepath")
        sys.exit()

    m3u_filepath = str(sys.argv[1])
    with open(m3u_filepath, 'r') as myfile:
        data = myfile.read()

    pattern = re.compile(r'start-time=(\d+)[\W\n]+EXTVLCOPT\:stop-time=(\d+)[\W\n]+([^\s]+)',
                         re.DOTALL | re.MULTILINE)
    triples = pattern.findall(data)
    print("to transcode: \n", triples)

    sources_folderpath = get_relative_dirpath_with_slash(m3u_filepath)

    for startsec, endsec, fname in triples:
        transcodevideo(str(sources_folderpath + fname), int(startsec), int(endsec))

main()
