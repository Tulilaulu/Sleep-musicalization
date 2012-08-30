#!/usr/bin/python

"""
This script is the entry point for generating music on the server.
"""

import argparse
import datetime
import tempfile
import os
import shutil
import requests

from sleepmusicalization import controller

server = "https://api.beddit.com"

kunquat_export = os.path.expanduser("~/kunquat/bin/kunquat-export")

lame = "/usr/bin/lame"


def make_api_request(server, api_selector, username, date, token):
    "Make an API request and return the resulting JSON document as a string"
    
    sleep_url = server + "/api2/user/%s/%d/%02d/%02d/%s?access_token=%s" % (username, date.year, date.month, date.day, api_selector, token)
    response = requests.get(sleep_url)
    response.raise_for_status()
    
    serialized_json_document = response.text
    
    return serialized_json_document


def main():
    parser = argparse.ArgumentParser(description="Fetch Beddit sleep data and compose music.")
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("-d", "--date", required=True)
    parser.add_argument("-t", "--token", required=True)
    parser.add_argument("output")
    
    arguments = parser.parse_args()
    
    date = datetime.datetime.strptime(arguments.date, "%Y-%m-%d").date()
    username = arguments.username
    token = arguments.token
    
    tempdir = tempfile.mkdtemp()
    print "Creating temporary directory", tempdir
    os.chdir(tempdir)
    
    print "Fetching sleep data"
    sleep_data_json_string = make_api_request(server, "sleep", username, date, token)
    result_data_json_string = make_api_request(server, "results", username, date, token)
    
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
    