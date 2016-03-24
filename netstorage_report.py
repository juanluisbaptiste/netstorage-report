import sys
import os
import json
import time
import logging
import tempfile
import pytest
import ntplib
import netstoragekit as ns
import math

# Configure the logging level and stream to stdout to see the logs.
#logging.basicConfig(level=logging.DEBUG,
#                    format="%(levelname)s[%(name)s.%(funcName)s:%(lineno)s] %(message)s",
#                    stream=sys.stdout)

# Sample timestamp and unique_id to test
# expected responses against the aactual ones using the same data
timestamp = int(time.time())
unique_id = int(timestamp * 2.5)
dir_sizes = {}

def get_test_credentials():
    # This file is installed in the home dir as a .json.dist file
    # that the user should update in order for these tests to run
    file = '~/.netstoragekit_test_credentials.json'
    file = os.path.expanduser(file)
    if not os.path.exists(file):
        return None
    with open(file) as data:
        test_credentials = json.load(data)
    return test_credentials

test_credentials = get_test_credentials()

def human_size(nbytes):
  suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  try:
      rank = int((math.log10(nbytes)) / 3)
  except ValueError:
      rank = 0
  rank = min(rank, len(suffixes) - 1)
  human = nbytes / (1024.0 ** rank)
  f = ('%.2f' % human).rstrip('0').rstrip('.')
  return '%s %s' % (f, suffixes[rank])

def get_dir_size(path):
    request = ns.api.Request(test_credentials['key_name'], test_credentials['key'],
                             test_credentials['cpcode'], test_credentials['host'],
                             timestamp=timestamp, unique_id=unique_id)
    data, r = request.du(path)
    return data.du['du-info'].bytes

def get_subdirs(path):
    request = ns.api.Request(test_credentials['key_name'], test_credentials['key'],
                             test_credentials['cpcode'], test_credentials['host'],
                             timestamp=timestamp, unique_id=unique_id)

    data, r = request.dir(path)
    print data
    return data.stat['file']

def run():

    subdirs = get_subdirs('/')
    for f in subdirs:
        if f['type'] == 'dir' :
          dir_size = float(get_dir_size(f['name']))
          if dir_size > 0 :
            dir_sizes[f['name']] = dir_size
            print f['name'] + ': ' + human_size(dir_size)

if __name__ == "__main__":
  run()
