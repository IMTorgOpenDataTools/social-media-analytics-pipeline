#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The module provides logic for doing interesting things.

"""
import sys
from pathlib import Path
import argparse

sys.path.append(Path('config').absolute().as_posix() )
from _constants import (
    logger,
    reddit_api_credentials,
    sub_reddits
)

from .reddit import Reddit




def parse_arguments():
    """Define and parse the script arguments."""
    parser = argparse.ArgumentParser()
    #parser.add_argument('notebook', help='Jupyter notebook filename')
    #parser.add_argument('--site-dir', required=True, help='path to hugo site directory')
    #parser.add_argument('--section', required=True, help='content section where to create markdown')
    args = parser.parse_args()
    return args


def main(args):
    data = Reddit(reddit_api_credentials, sub_reddits)
    text = data.get_text()
    return text




if __name__ == '__main__':
    args = parse_arguments()
    main(args)
    logger.info("Data extraction complete.")