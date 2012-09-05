#!/usr/bin/python

"""
This script is the entry point for generating music on the server.
"""

import argparse
import datetime
import tempfile
import os
import shutil

from sleepmusicalization import controller

kunquat_export = os.path.expanduser("~/kunquat/bin/kunquat-export")

lame = "/usr/bin/lame"


def main():
    parser = argparse.ArgumentParser(description="Read Beddit sleep data and compose music.")
    parser.add_argument("-r", "--result", required=True)
    parser.add_argument("-s", "--sleep", required=True)
    parser.add_argument("output")
    
    arguments = parser.parse_args()
    
    date = datetime.datetime.strptime(arguments.date, "%Y-%m-%d").date()
    username = arguments.username
    token = arguments.token
    
    tempdir = tempfile.mkdtemp()
    print "Creating temporary directory", tempdir
    os.chdir(tempdir)
    
    print "Reading sleep data"
    with open(arguments.sleep) as sleep_file:
        sleep_data_json_string = sleep_file.read()
    with open(arguments.result) as result_file:
        result_data_json_string = result_file.read()
    
    print "Generating music"
    controller.composeSong(result_data_json_string, sleep_data_json_string)
    
    print "Exporting"
    os.system(kunquat_export + " -o sleep.wav kqtc00/")
    
    print "Converting to mp3"
    os.system(lame + " sleep.wav " + arguments.output)
    
    print "Removing temporary directory"
    shutil.rmtree(tempdir)


if __name__ == "__main__":
    main()
    