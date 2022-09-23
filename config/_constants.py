#!/usr/bin/env python3
"""
Constants used throughout app.
"""

import os
import sys
from pathlib import Path
import logzero
from logzero import logger
from collections import namedtuple
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

sys.path.append(Path('..').absolute().as_posix() )
#from output import Output




# system variables
config = {}
config['data_export'] = './data/reddit.serial'
config['logging_dir'] = './data/process.log'
"""
emails_file = './config/emails.csv'
email_network_drive = r'\\hqfiles01\sec_edgar$\cbdc_tracker'

report_dir = './downloads'
report_copy_dir = './downloads'
"""
sub_reddits=["banks"]


# logging
logzero.loglevel(logzero.INFO)                                           #set a minimum log level: debug, info, warning, error
logzero.logfile(config['logging_dir'], maxBytes=1000000, backupCount=3)            #set rotating log file
logger.info('logger created, constants initialized')


# dotenv
reddit_api_credentials = {
    "client_id": os.getenv('CLIENT_ID'),
    "client_secret": os.getenv('CLIENT_SECRET'),
    "user_agent": os.getenv('USER_AGENT'),
    "username": os.getenv('USERNAME'),
    "password": os.getenv('PASSWORD')
}