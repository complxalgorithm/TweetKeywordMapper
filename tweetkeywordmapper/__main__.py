"""
# import modules
"""
import argparse
import os
import sys
import time
import pandas as pd
import warnings as warn

# ignore all warnings that GeoPandas may output
warn.filterwarnings('ignore')

try:
    from tweetkeywordmapper.core import data
    from tweetkeywordmapper.core import stats
    from tweetkeywordmapper.core import constants as cons
    from tweetkeywordmapper.scripts import mapper as tkm
    from tweetkeywordmapper.scripts import search as tks
    from tweetkeywordmapper.scripts import read as tkr
    from tweetkeywordmapper.scripts import counts as cnts
except:
    from core import data
    from core import stats
    from core import constants as cons
    from scripts import mapper as tkm
    from scripts import search as tks
    from scripts import read as tkr
    from scripts import counts as cnts   

"""
# initialize constants
"""
# set workspace
WS = cons.workspace

# set default file and its extention
DEFAULT_FILE = cons.default_file
DEFAULT_FILE_TYPE = DEFAULT_FILE.split('.')[-1]

# set states and cities dictionaries
STATES = cons.states
CITIES = cons.cities


"""
# define get_args() function - set valid arguments and return arguments parser
"""
def get_args() -> argparse.Namespace:
    # create ArgumentParser instance
    parser = argparse.ArgumentParser(prog='python3 tweetkeywordmapper',
                                     description='Search/Import Tweet data from US states with a keyword, then map the count results',
                                     add_help=True)
    
    # add argument options to parser
    parser.add_argument('-s', '--search', action='store_true',
                         help='search Twitter for Tweets containing a specific keyword, then map results')
    parser.add_argument('-r', '--read', action='store_true',
                         help='import Tweet data from a CSV/XLSX file, then map results')
    parser.add_argument('-c', '--counts', action='store_true',
                         help='tally the total for each unique value of a specified field from a CSV/XLSX file')
    
    # return parser
    return parser.parse_args()


"""
# define create_default_file() function - create the default file if it does not already exist
# within the workspace by adding first row to file containing headers Tweet_ID, Keyword, and State
"""
def create_default_file(default, ws, file_type):
    # create default file if it doesn't already exist
    if not os.path.exists(default):
        # create default file if it's a CSV or XLSX file
        if file_type == 'csv' or file_type == 'xlsx':
            data.file_interact(['Tweet_ID', 'Keyword', 'State'], default, file_type, ws)

            # display that default file was successfully create
            print(f'Default file created called: {default}\n')
        
        # display error if file is not a CSV or XLSX file
        else:
            print(f'Could not create default file {default} because it is not a CSV or XLSX file.')

        # pause program for a second
        time.sleep(1)
        
        # return to parent function
        return

        
"""
# define display_results() function - displays results of the search or import
"""
def display_results(count_percents, state_counts, places, ids, keyword, states):
    # display keyword(s), and tweet ids and places lists if any were found
    print(f'\nKeywords: {keyword}\n')
    time.sleep(1.5)   # pause program for a second and a half
    print(f'IDs: {ids}\n')
    time.sleep(1.5)   # pause program for a second and a half
    print(f'Places: {places}\n')
    time.sleep(1.5)   # pause program for a second and a half
    
    # display the count and percentage of total for each state
    print('Total Tweets/Percent of Total From Each State')
    print('---------------------------------------------')
    print('{:<30s} {:<6} {:<6}'.format('STATE', 'COUNT', 'PERCENT'))
    print('---------------------------------------------')
    for state, percent in count_percents.items():
        # get count for state from state_counts dictionary
        count = state_counts[list(states.keys())[list(states.values()).index(state)]]

        # display result for state
        print('{:<30s} {:<6} {:<6}'.format(state + ':', count, percent))

    # new line
    print()
    

"""
# define main() function - handles arguments and runs appropriate functionality
"""
def main():
    # get arguments
    args = get_args()
    
    # set name of package
    pkg = 'tweetkeywordmapper'
    
    # get last argument
    arg = sys.argv[-1]
    
    # get number of arguments except for name of program
    num_args = (len(sys.argv)-1)
    
    ""
    # handle arguments, or lack thereof
    ""
    
    # display an error if no additional arguments are entered after tweetkeywordmapper, then quit program
    # NOTE: usage information will be displayed if more than 1 additional argument is entered
    #       and a default error will be displayed if an invalid argument is entered
    if num_args == 0:
        print('ERROR - No argument provided. Use -h or --help for usage information.')
        
        return
    
    # run this code if no errors in argumentation are present
    else:
        # display welcome message
        print('Welcome to Tweet Keyword Mapper!\n')
        
        time.sleep(1)   # pause program for a second

        # create default file if it doesn't already exist
        create_default_file(DEFAULT_FILE, WS, DEFAULT_FILE_TYPE)

        # run the search.py script if search is the argument
        if args.search:
            print('Search Twitter for Tweets Containing a Keyword\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            places, ids, state_counts, keyword, num_results = tks.TweetKeywordSearch(WS, DEFAULT_FILE, STATES, CITIES)

        # run the read.py script if import is the argument
        elif args.read:
            print('Import Tweet Data from a CSV/Excel File\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            places, ids, state_counts, keyword, num_results = tkr.TweetKeywordRead(WS, DEFAULT_FILE, STATES)

        # run the counts.py script if counts is the argument
        elif args.counts:
            print('Count Instances of Each Unique Value of a Field in a CSV/Excel File\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            cnts.TweetKeywordCount(WS, DEFAULT_FILE, STATES)
        
        # display invalid argument error if any other arguments are entered, then quit program
        else:
            print('ERROR - Invalid argument. Use -h or --help for usage information.')
            
            return

        # run this code if search or import were the arguments
        if args.search or args.read:
            # run this code if results were found
            if num_results > 0:
                # get what percentage of the total number of results came from each state
                # will only include the states that have Tweets
                state_count_percents = stats.get_count_percentages(state_counts, num_results, STATES)

                time.sleep(1)   # pause program for a second

                # display the results
                display_results(state_count_percents, state_counts, places, ids, keyword, STATES)

                time.sleep(1)   # pause program for a second

                # run mapping functionality
                tkm.TweetKeywordMapper(WS, state_counts, keyword)

        # display goodbye after the program has executed
        if arg != pkg:
            time.sleep(1)   # pause program for a second
            
            print('\nThank you for using Tweet Keyword Mapper!')


# execute program
if __name__ == '__main__':
    main()