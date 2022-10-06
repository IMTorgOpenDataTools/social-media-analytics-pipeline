#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The module provides logic for working with Reddit API data.

"""

from asyncore import read
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
import spacy


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


def prepare_data_for_labeling(read_data_or_file=None, csv_out_file=None):
    """Prepare data for upload to labeling app (doccano) in jsonl format.

    - one sentence per record
    - metadata for re-combine after labeling
    - columns: 'id', 'body'
    
    """
    def splitter(x, nlp):
        """Nested function to split text into sentences."""
        doc = nlp(x["text"])
        a = [sent.text for sent in doc.sents]
        b = len(a)
        dictionary = {"Id": np.repeat(x["Id"],b), "sentence_nr": list(range(1, b+1)), "sentence": a}
        dictionaries = [{key : value[i] for key, value in dictionary.items()} for i in range(b)]
        for dictionary in dictionaries:
            rows_list.append(dictionary)

    if read_data_or_file==None:
        read_data_or_file = './data/reddit.serial'

    if csv_out_file==None:
        csv_out_file = './data/reddit.jsonl'

    df = pd.read_pickle(read_data_or_file)
    out = df[['body','Id']]
    out.rename(columns={'body':'text'}, inplace=True)

    nlp = spacy.load("en_core_web_sm")
    rows_list = []

    out.apply(lambda x: splitter(x, nlp), axis = 1)
    new_df = pd.DataFrame(rows_list, columns=['Id', 'sentence_nr','sentence'])
    new_df['label'] = ''

    with open(csv_out_file, 'w') as f:
        print(new_df.to_json(orient='records', lines=True), file=f, flush=False)
    
    return new_df




class Reddit:
    """Class to manage data API pulls from Reddit.

    * for some subreddits
    *   for n submissions
    *     get the comments and metadata
    *     combine data into table
    *     prepare text for run with spacy model

    Review results:

    
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
        self.subreddits = sub_reddits
        # maintain dataframes
        data = np.empty(0, dtype=self.dtypes)
        self.exportDf = pd.DataFrame(data)


    def get_text_bodies_from_subreddits(self, subreddits=None, submissions_limit=100, comments_limit=100):
        """Get text bodies (up to specified limits) from list of subreddits.
        
        """

        if subreddits == None:
            subreddits = self.subreddits

        for sub_reddit in subreddits:
            try:
                subreddit_submissions = self.reddit.fetch_subreddit_submissions(
                                                self.graphipy.create_graph(), 
                                                subreddit_name=sub_reddit, 
                                                limit= submissions_limit)
                # Get all the node dataframes available from the query
                ss_nodes = subreddit_submissions.get_nodes()
                submissionsDf = ss_nodes["submission"][['Id','Label','created_utc','author','ups','title','selftext','downs','num_comments']]
                logger.info( ss_nodes["submission"].shape )
            except:
                continue

            # Get comments from submision
            for submission_id in ss_nodes["submission"].Id:
                sub = submissionsDf.loc[submissionsDf.Id == submission_id,].reset_index(drop=True).copy(deep=True)
                sub['type'] = 'submission'
                sub['body'] = sub.title[0] + ' | ' + sub.selftext[0]
                sub['depth'] = np.nan
                sub['likes'] = sub.num_comments[0]
                sub_mod = sub[['type','Id','Label','created_utc','author','ups','body','depth','downs','likes']]

                sub_mod['sub_reddit'] = sub_reddit
                sub_mod['sub_redditId'] = np.nan
                sub_mod['submissionLabel'] = sub.Label[0]
                sub_mod['submissionId'] = sub.Id[0]
                self.exportDf = pd.concat([self.exportDf, sub_mod], ignore_index=True)

                if comments_limit > 0:
                    try:
                        #check-1: call can fail
                        submission_comments = self.reddit.fetch_submission_comments(
                                                self.graphipy.create_graph(), 
                                                submission_id, 
                                                limit= comments_limit)
                    except:
                        logger.error("Error in call")

                    else:
                        sc_nodes = submission_comments.get_nodes()
                        #check-2: call may not return comment
                        if "comment" in sc_nodes.keys():
                            tmpDf1 = sc_nodes["comment"][['Id','Label','created_utc','author','ups','body','depth','downs','likes']].copy(deep=True)
                            tmpDf1['type'] = 'comment'
                            #tmpDf2 = tmpDf1.append(sub_mod, ignore_index=True).copy(deep=True)
                            tmpDf2 = tmpDf1

                            tmpDf2['sub_reddit'] = sub_reddit
                            tmpDf2['sub_redditId'] = np.nan
                            tmpDf2['submissionLabel'] = sub.Label[0]
                            tmpDf2['submissionId'] = sub.Id[0]

                            self.exportDf = pd.concat([self.exportDf, tmpDf2], ignore_index=True)
                            logger.info(f"added {tmpDf2.shape[0]} rows to `exportDf` ")

        logger.info("reddit data complete")
        return self.exportDf


    def export_records_to_file(self, type='serial'):
        """Export records to file."""
        file_path = Path(config['data_export'])
        mode = 'w+'
        match type:
            case 'serial':
                file_name = file_path.with_suffix('.serial')
                self.exportDf.to_pickle(file_name)
                return file_name
            case 'csv':
                file_name = file_path.with_suffix('.csv')
                self.exportDf.to_csv(file_name, mode=mode)
                return file_name
            case _:
                return f'The arg {type} is not allowed.'