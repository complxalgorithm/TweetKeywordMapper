"""
# import modules
"""
import argparse
import os
import sys
import time
import warnings as warn

try:
    from tweetkeywordmapper.core.data import create_file
    from tweetkeywordmapper.core import constants as cons
    from tweetkeywordmapper.scripts import mapper as tkm
    from tweetkeywordmapper.scripts import search as tks
    from tweetkeywordmapper.scripts import read as tkr
    from tweetkeywordmapper.scripts import counts as cnts
except:
    from core.data import create_file
    from core import constants as cons
    from scripts import mapper as tkm
    from scripts import search as tks
    from scripts import read as tkr
    from scripts import counts as cnts
    
# ignore all warnings that GeoPandas may output
warn.filterwarnings('ignore')


"""
# initialize constants
"""
# set workspace
WS = cons.workspace

# set default file and its extention
DEFAULT_FILE = cons.default_file
DEFAULT_FILE_TYPE = DEFAULT_FILE.split('.')[-1]

# set states, cities, and area codes dictionaries
STATES = cons.states
CITIES = cons.cities
AREA_CODES = cons.area_codes


"""
# define get_args() function - set valid arguments and return arguments parser
"""
def get_args() -> argparse.Namespace:
    # import textwrap module to be used in argument parser
    import textwrap
    
    # create ArgumentParser instance
    parser = argparse.ArgumentParser(prog='python3 tweetkeywordmapper',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                        Search/Import Tweet data from US states with a keyword, then map the count results.
                                        - search and read will run mapper.py to map the results after state counts are totaled.
                                        - if you want to use two parameters, -f must be one of them.
                                        '''),
                                     add_help=False)
    
    # add argument options to parser
    parser.add_argument('-s', '--search', action='store_true',
                         help='search Twitter for Tweets containing a specific keyword, then map results')
    parser.add_argument('-r', '--read', action='store_true',
                         help='import Tweet data from a CSV/XLSX file, then map results')
    parser.add_argument('-c', '--counts', action='store_true',
                         help='tally the count for each unique value of a specified field from a CSV/XLSX file')
    parser.add_argument('-f', '--create', action='store_true',
                       help='create a CSV or XLSX file to use for writing and importing Tweet data')
    parser.add_argument('-h', '--help', action='help',
                       help='display usage information')
    
    # return parser
    return parser.parse_args()

        
"""
# define display_results() function - displays results of the search or import
"""
def display_results(count_percents, state_counts, places, ids, keyword, states):
    # display keyword(s), and tweet ids and places lists if any were found
    print(f'\nKeywords: {keyword}\n')
    time.sleep(1.5)                 # pause program for a second and a half
    print(f'IDs: {ids}\n')
    time.sleep(1.5)                 # pause program for a second and a half
    print(f'Places: {places}\n')
    time.sleep(1.5)                 # pause program for a second and a half
    
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
    
    # get number of arguments minus package name
    num_args = (len(sys.argv)-1)
    
    """
    # handle arguments, or lack thereof
    """
    
    # display an error if no additional arguments are entered after package name, then quit program
    # NOTES: usage information will be displayed by default if more than 1 additional argument is entered
    #        a default error will be displayed if an invalid argument is entered
    #        if help is used along with another argument, the program will only display usage information
    if num_args == 0:
        print('ERROR - No argument provided. Use -h or --help for usage information.')
        
        return
    
    # display an error if more than two additional arguments are entered after package name
    elif num_args > 2:
        print('ERROR - Too many arguments. Use -h or --help for usage information.')
        
        return
    
    # make sure createfile is one of the arguments if two arguments are entered after package name
    elif num_args == 2 and not args.create:
        print('ERROR - f/create flag must be used when using 2 arguments. Use -h or --help for usage information.')
        
        return
    
    # only 1 argument was entered
    else:
        # display welcome message
        print('Welcome to Tweet Keyword Mapper!\n')
        
        time.sleep(1)   # pause program for a second

        # run create_file function if createfile is an argument
        if args.create:
            print('Create a CSV or XLSX File\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            # create file
            create_file(DEFAULT_FILE, WS)

        # run the search.py script if search is an argument
        if args.search:
            print('Search Twitter for Tweets Containing a Keyword\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            places, ids, state_counts, keyword, num_results = tks.TweetKeywordSearch(WS, DEFAULT_FILE, STATES, CITIES, AREA_CODES)

        # run the read.py script if read is an argument
        elif args.read:
            print('Import Tweet Data from a CSV or XLSX File\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            places, ids, state_counts, keyword, num_results = tkr.TweetKeywordRead(WS, DEFAULT_FILE, STATES)

        # run the counts.py script if counts is an argument
        elif args.counts:
            print('Count Instances of Each Unique Value of a Field in a CSV or XLSX File\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            cnts.TweetKeywordCount(WS, DEFAULT_FILE, STATES)

        # run this code if search or import were an argument
        if args.search or args.read:
            # run this code if results were found
            if num_results > 0:
                # import stats module
                try:
                    from tweetkeywordmapper.core.stats import get_count_percentages
                except:
                    from core.stats import get_count_percentages
                
                # get what percentage of the total number of results came from each state
                # will only include the states that have Tweets
                state_count_percents = get_count_percentages(state_counts, num_results, STATES)

                time.sleep(1)   # pause program for a second

                # display the results
                display_results(state_count_percents, state_counts, places, ids, keyword, STATES)

                time.sleep(1)   # pause program for a second

                # run mapping functionality
                tkm.TweetKeywordMapper(WS, state_counts, keyword)
        
        # display goodbye after the program has executed
        print('\nThank you for using Tweet Keyword Mapper!')


# execute program
if __name__ == '__main__':
    main()