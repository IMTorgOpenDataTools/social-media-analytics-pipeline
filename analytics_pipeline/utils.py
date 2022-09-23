#!/usr/bin/env python3
"""
Utility functions
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"



import sys
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter, Retry
import datetime as dt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

sys.path.append(Path('config').absolute().as_posix() )
from _constants import (
    logger
)






def get_reddit():
    """Get the data file from web page.
    Return dict of lists (records).
    """
    pass