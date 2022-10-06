import os
import sys
from pathlib import Path

sys.path.append(Path('..').absolute().as_posix() ) 

from analytics_pipeline.reddit import (
    Reddit,
    prepare_data_for_labeling 
)
from config._constants import (
    config,
    reddit_api_credentials,
    subreddits
)




data = Reddit(reddit_api_credentials, subreddits)

def test_Reddit_Submissions_get_text_bodies():
    textDf = data.get_text_bodies_from_subreddits(subreddits=['banks', 'stocks'],
                                                    submissions_limit=10,
                                                    comments_limit=0
                                                    )
    number_of_submissions = textDf[textDf['type']=='submission'].shape[0]
    assert number_of_submissions == 23

def test_Reddit_Comments_get_text_bodies():
    textDf = data.get_text_bodies_from_subreddits(subreddits=['banks'],
                                                    submissions_limit=1,
                                                    comments_limit=10
                                                    )
    number_of_submissions = textDf[textDf['type']=='submission'].shape[0]
    assert number_of_submissions == 2

def test_Reddit_export():
    file_name = data.export_records_to_file(type='serial')
    check = Path(file_name).is_file()
    assert check == True

def test_prepare_data_for_labeling():
    jsonlDf = prepare_data_for_labeling()
    lines = jsonlDf.shape[0]
    assert lines == 207