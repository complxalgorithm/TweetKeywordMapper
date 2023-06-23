"""

@Name: counts.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Counts the total for each unique attribute value of a specified field within a CSV/Excel file
              Also determines percentages of total for each attribute value
@Requirements: Python3, pandas, numpy

"""


# import libraries
import pandas as pd
import numpy as np
import os
import time

try:
    from tweetkeywordmapper.core import data
    from tweetkeywordmapper.core import stats
    from tweetkeywordmapper.core import constants as cons
except:
    from core import data
    from core import stats
    from core import constants as cons


"""
# define TweetKeywordCount() function - outputs counts and percentage of total for each unique value
# of user specified field in CSV/Excel file
"""
def TweetKeywordCount(ws, default_file, states):
    # get file and its extension from user
    user_file, file_type = data.get_user_file(default_file)

    # get list of unique atrribution values, keyword field, and contents df from file
    values, field, contents = data.file_interact([], user_file, file_type, ws, mode='r', function='counts')
    
    # get dictionary of keyword counts and list of unique keywords
    counts = stats.get_counts(values, states, df=contents, field=field, function='counts')
    
    # get percents dictionary
    percents = stats.get_count_percentages(counts, len(contents), states, function='counts')
    
    time.sleep(1.5)     # pause program for a second and a half
    
    # display the count and percent of all data for each keyword in descending order
    print('{:<25s}{:<10s}{:<6s}'.format('VALUE', 'COUNT', 'PERCENT'))
    print('------------------------------------------')
    for value, count in counts.items():
        print('{:<25s}{:<10}{:<6}'.format(value, count, percents[value]))