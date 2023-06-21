"""

@Name: counts.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: 
@Requirements: Python3, pandas, numpy

"""


# import libraries
import pandas as pd
import numpy as np
import os
import time

try:
    from tweetkeywordmapper.core import TweetKeywordData as data
    from tweetkeywordmapper.core import TweetKeywordConstants as cons
except:
    from core import TweetKeywordData as data
    from core import TweetKeywordConstants as cons


"""
# define get_values() function - get unique values of selected field, and return list of unique values
# and the selected field
"""
def get_unique_values(contents):
    # get fields from contents
    fields = [f for f in contents]

    # display menu of fields that were found in csv file
    print()
    for i, field in enumerate(fields, start=1):
        print(f'{i}. {field}')
    print()

    # initialize empty lists of unique keywords from csv file and counts of each unique keyword in keywords list
    values = []
    counts = []

    # ask user to identify the keywords field from the menu
    field = input('Enter the field you would like to tally from the menu: ')

    # validate that field is in fields list
    while field not in fields:
        # tell user that field doesn't exist, then pause program for a second
        print(f'{field} field does not exist.')
        time.sleep(1)

        # ask user again for keyword field
        field = input('Enter the field you would like to tally from the menu: ')
    
    print()
    
    # initialize list to store keyword values object containing values from keyword_field
    data = []

    # add data values/object of keyword_field to keyword_data list
    data.append(contents[field])

    # iterate through each keyword result object and add unique values to keyword list
    for ob in data:
        for word in ob:
            # add keyword to keywords list if it isn't already in it
            if word not in values:
                values.append(word)
    
    # return list of values and field lists to parent function
    return values, field


"""
# define TweetKeywordCount() function - outputs counts and percentage of total for each unique value
# of user specified field in csv file
"""
def TweetKeywordCount(states):
    # set default csv file
    default_csv = cons.default_csv

    # get csv file from user
    user_csv = data.get_user_csv_file(default_csv)

    # extract contents of csv file
    contents = pd.read_csv(user_csv, header=0)
    
    # get list of unique keywords and keyword field from csv file
    values, field = get_unique_values(contents)
    
    # get dictionary of keyword counts and list of unique keywords
    counts = data.get_counts(values, states, df=contents, field=field, function='counts')
    
    # get percents dictionary
    percents = data.get_count_percentages(counts, len(contents), states, function='counts')
    
    time.sleep(1.5)     # pause program for a second and a half
    
    # display the count and percent of all data for each keyword in descending order
    print('{:<25s}{:<10s}{:<6s}'.format('VALUE', 'COUNT', 'PERCENT'))
    print('------------------------------------------')
    for value, count in counts.items():
        print('{:<25s}{:<10}{:<6}'.format(value, count, percents[value]))