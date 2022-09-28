#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The module provides logic for doing interesting things.


* for some subreddits
*   for some submissions
*     get the comments and metadata
*     combine data into table
*     prepare text for run with spacy model

"""

import sys
from pathlib import Path

sys.path.append(Path('config').absolute().as_posix() )
from _constants import (
    config,
    logger
)

from graphipy.graphipy import GraphiPy
import datetime
import pandas as pd
import numpy as np


"""
def search_reddits(reddit):
    "DOCSTRING"
    keyword = "projectmanagement"
    # However, it also returns the graph modified so you can assign it to other variables like so:
    subreddits_name = reddit.fetch_subreddits_by_name(
                                graphipy.create_graph(), 
                                keyword, 
                                limit=5)
    subreddit_df['created_local'] = subreddit_df['created_utc'].map(lambda x: datetime.datetime.fromtimestamp( np.float(x) ).isoformat() )
    subreddit_df[['Label','subscribers','created_local','lang']]
"""




class Reddit:
    """
    TODO:
    * am I combining all submissions and comments or losing some?
    * how do I mod to get more data?
    * how to combine graphs of multiple sub_reddits?

    Review results:
    df = pd.read_pickle('./data/reddit.serial')
    
    """

    dtypes = np.dtype([
            ('type', str),
            ('sub_reddit', str),
            ('sub_redditId', str),
            ('submissionLabel', str),
            ('submissionId', str),
            ('Id', int),
            ('Label', str),
            ('created_utc', str),
            ('author', str),
            ('ups', int),
            ('body', str),
            ('depth', int),
            ('downs', int),
            ('likes', int),
            ])

    def __init__(self, reddit_api_credentials, sub_reddits):
        """Initialize the object"""
        self.__reddit_api_credentials = reddit_api_credentials
        # create GraphiPy object (default to Pandas)
        self.graphipy = GraphiPy()
        # create the reddit object
        self.reddit = self.graphipy.get_reddit(reddit_api_credentials)
        self.sub_reddits = sub_reddits
        # maintain dataframes
        data = np.empty(0, dtype=self.dtypes)
        self.exportDf = pd.DataFrame(data)

    def get_text(self):
        """Get text from source"""
        # Call the appropriate function
        for sub_reddit in self.sub_reddits:
            subreddit_submissions = self.reddit.fetch_subreddit_submissions(
                                            self.graphipy.create_graph(), 
                                            subreddit_name=sub_reddit, 
                                            limit=100)
            # Get all the node dataframes available from the query
            ss_nodes = subreddit_submissions.get_nodes()
            submissionsDf = ss_nodes["submission"][['Id','Label','created_utc','author','ups','title','selftext','downs','num_comments']]
            logger.info( ss_nodes["submission"].shape )

            # Get comments from submision
            for submission_id in ss_nodes["submission"].Id:
                sub = submissionsDf.loc[submissionsDf.Id == submission_id,].reset_index(drop=True).copy(deep=True)
                sub['type'] = 'submission'
                sub['body'] = sub.title[0] + ' | ' + sub.selftext[0]
                sub['depth'] = np.nan
                sub['likes'] = sub.num_comments[0]
                sub_mod = sub[['type','Id','Label','created_utc','author','ups','body','depth','downs','likes']]

                try:
                    submission_comments = self.reddit.fetch_submission_comments(
                                            self.graphipy.create_graph(), 
                                            submission_id, 
                                            limit=100)
                except:
                    logger.error("Error in call")
                else:
                    sc_nodes = submission_comments.get_nodes()
                    if "comment" in sc_nodes.keys():
                        tmpDf1 = sc_nodes["comment"][['Id','Label','created_utc','author','ups','body','depth','downs','likes']].copy(deep=True)
                        tmpDf1['type'] = 'comment'
                        tmpDf2 = tmpDf1.append(sub_mod, ignore_index=True).copy(deep=True)

                        tmpDf2['sub_reddit'] = sub_reddit
                        tmpDf2['sub_redditId'] = np.nan
                        tmpDf2['submissionLabel'] = sub.Label[0]
                        tmpDf2['submissionId'] = sub.Id[0]
                        
                        self.exportDf = pd.concat([self.exportDf, tmpDf2], ignore_index=True)
                        logger.info(f"added {tmpDf2.shape[0]} rows to `exportDf` ")

        #tmpDf.to_csv(config.config['DATA_EXPORT'], index=False)
        self.exportDf.to_pickle(config['data_export'] )
        logger.info("reddit data complete")