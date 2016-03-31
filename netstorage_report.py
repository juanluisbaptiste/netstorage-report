import sys
import os
import json
import time
import datetime
import logging
import tempfile
import pytest
import ntplib
import netstoragekit as ns
import math
import smtplib
from email.mime.text import MIMEText

VERSION = "0.1"
# Configure the logging level and stream to stdout to see the logs.
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s[%(name)s.%(funcName)s:%(lineno)s] %(message)s",
                    stream=sys.stdout)

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

def get_subdirs_sizes(subdirs):
    for f in subdirs:
        if f['type'] == 'dir' :
          dir_size = int(get_dir_size(f['name']))
          dir_sizes[f['name']] = dir_size
    return dir_sizes

def get_subdirs(path):
    request = ns.api.Request(test_credentials['key_name'], test_credentials['key'],
                             test_credentials['cpcode'], test_credentials['host'],
                             timestamp=timestamp, unique_id=unique_id)

    data, r = request.dir(path)
    #print data
    return data.stat['file']

def get_formatted_subdirs_sizes(sizes):
    f = ""
    for key, value in sizes.iteritems():
        f += "%-20s: %-20s\n" % (key,human_size(value))
    return f

def get_program_header():
    return "----- ------ --------- ------ -------\n\
Cache Simple NetStorage Report Program\n\
----- ------ --------- ------ -------\n\n"

def calculate_total_size():
    return sum(dir_sizes.values())

def get_report_date():
    d = datetime.date.today()
    previous_month = d.month - 1
    previous_month_date = datetime.datetime(d.year,previous_month,d.day)
    return previous_month_date.strftime('%B') + " " + str(d.year)

def save_report(subdirs_sizes):
    data = ""
    data += get_program_header()
    data += get_formatted_subdirs_sizes(subdirs_sizes)
    data += "%-21s: %-20s\n" % ("\nTotal", human_size(calculate_total_size()))
    data += "\n--\nProgram version: %s\n" % VERSION
    save_report_file(data)

def save_report_file(data):
    f = open('reports/' + get_report_date() + '.txt', 'w')
    f.write(data)
    f.close

def send_email():
    fp = open('reports/' + get_report_date() + '.txt', 'rb')
    # Create a text/plain message
    msg = MIMEText(fp.read())
    fp.close()
    from_ = 'nsreport@cachesimple.com'
    dest = 'juan.baptiste@gmail.com'
    msg['Subject'] = 'Cache Simple NetStorage Report for %s' % get_report_date()
    msg['From'] = from_
    msg['To'] = dest
    s = smtplib.SMTP('localhost')
    s.sendmail(from_, dest, msg.as_string())
    s.quit()

def run():
    #print get_report_date()
    subdirs = get_subdirs('/')
    subdirs_sizes = get_subdirs_sizes(subdirs)
    save_report(subdirs_sizes)
    send_email()
    print get_program_header()
    print get_formatted_subdirs_sizes(subdirs_sizes)
    print "%-21s: %-20s" % ("Total", human_size(calculate_total_size()))

if __name__ == "__main__":
  run()
