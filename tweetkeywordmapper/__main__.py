"""
# import modules
"""
import argparse
import os
import sys
import time

try:
    from tweetkeywordmapper.core import TweetKeywordData as data
    from tweetkeywordmapper.core import TweetKeywordConstants as cons
    from tweetkeywordmapper.scripts import mapper as tkm
    from tweetkeywordmapper.scripts import search as tks
    from tweetkeywordmapper.scripts import read as tkr
    from tweetkeywordmapper.scripts import counts as cnts
except:
    from core import TweetKeywordData as data
    from core import TweetKeywordConstants as cons
    from scripts import mapper as tkm
    from scripts import search as tks
    from scripts import read as tkr
    from scripts import counts as cnts

"""
# initialize constants
"""
# set workspace
WS = cons.workspace

# set default csv file
DEFAULT_CSV = cons.default_csv

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
                         help='import Tweet data from a CSV file, then map results')
    parser.add_argument('-c', '--counts', action='store_true',
                         help='tally the total for each unique value of a specified field from a CSV file')
    
    # return parser
    return parser.parse_args()


"""
# define create_default_csv() function - create the default csv file if it does not already exist
# within the workspace by adding first row to file containing headers Tweet_ID, Keyword, and State
"""
def create_default_csv(default, ws):
    if not os.path.exists(default):
        data.csv_interact(('Tweet_ID', 'Keyword', 'State'), default, ws)

        # display that default file was successfully create
        print(f'Default file created called: {DEFAULT_CSV}')

        # pause program for a second
        time.sleep(1)

        
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

        # create default csv if it doesn't already exist
        create_default_csv(DEFAULT_CSV, WS)

        # run the search.py script if search is the argument
        if args.search:
            print('Search Twitter for Tweets Containing a Keyword\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            places, ids, state_counts, keyword, num_results = tks.TweetKeywordSearch(WS, DEFAULT_CSV, STATES, CITIES)

        # run the read.py script if import is the argument
        elif args.read:
            print('Import Tweet Data from a CSV File\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            places, ids, state_counts, keyword, num_results = tkr.TweetKeywordImport(WS, DEFAULT_CSV, STATES)

        # run the counts.py script if counts is the argument
        elif args.counts:
            print('Count Instances of Each Unique Value of a Field in a CSV File\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            cnts.TweetKeywordCount()
        
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
                state_count_percents = data.get_count_percentages(state_counts, num_results, STATES)

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