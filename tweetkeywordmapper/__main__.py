"""
# import modules and ignore warnings
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
    from tweetkeywordmapper.utils.delete_us_territories import delete_us_territories
    from tweetkeywordmapper.utils.download_shp import download_shp
except:
    from core.data import create_file
    from core import constants as cons
    from scripts import mapper as tkm
    from scripts import search as tks
    from scripts import read as tkr
    from scripts import counts as cnts
    from utils.delete_us_territories import delete_us_territories
    from utils.download_shp import download_shp

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
                                        - if you want to use two parameters, -f, -d, or -p must be one of them.
                                        - to use three parameters, two of -f, -d, or -p must be used.
                                        '''),
                                     add_help=False)
    
    # add argument options to parser
    parser.add_argument('-s', '--search', action='store_true',
                        help='search Twitter for Tweets containing a specific keyword, then map results')
    parser.add_argument('-r', '--read', action='store_true',
                        help='import Tweet data from a CSV/XLSX file, then map results')
    parser.add_argument('-c', '--counts', action='store_true',
                        help='tally the count for each unique value of a field from a CSV/XLSX file')
    parser.add_argument('-m', '--map_field', action='store_true',
                        help='map previous results field from shapefile using GeoPandas')
    parser.add_argument('-f', '--create_file', action='store_true',
                        help='create a CSV or XLSX file to use for writing and importing Tweet data')
    parser.add_argument('-d', '--delete_terrs', action='store_true',
                        help='delete US territories from US state boundaries shapefile')
    parser.add_argument('-p', '--download_shp', action='store_true',
                        help='download US State boundaries shapefile from US Census Bureau website')
    parser.add_argument('-h', '--help', action='help',
                        help='display usage information')
    
    # return parser
    return parser.parse_args()

        
"""
# define display_results() function - displays results of the search or import
"""
def display_results(count_percents, state_counts, places, ids, keyword, states):
    # get number of states that Tweets came from
    num_states = len(set(count_percents.keys()))
    
    # number of results
    num_results = len(ids)
    
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
    print('=============================================')
    # display number of states of origin and number of results
    print('{:<30s} {:<6}'.format(f'{num_states} states', f'{num_results} results'))
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
    # NOTES: usage information will be displayed by default if more than 3 arguments are entered
    #        a default error will be displayed if an invalid argument is entered
    #        if help is used along with another argument, the program will only display usage information
    if num_args == 0:
        print('ERROR - No argument provided. Use -h or --help for usage information.')
        
        return
    
    # display an error if more than two additional arguments are entered after package name
    elif num_args > 3:
        print('ERROR - Too many arguments. Use -h or --help for usage information.')
        
        return
    
    # make sure create_file or delete_terrs is one of the arguments if two arguments are entered after package name
    elif (num_args == 2) and (not args.create_file and not args.delete_terrs and not args.download_shp):
        print('ERROR - f/create_file, d/delete_terrs, and/or p/download_shp must be used when using 2 arguments.\nUse -h or --help for usage information.')
        
        return
    
    # make sure both create_file and delete_terrs are arguments if three arguments are entered after package name
    elif (num_args == 3) and ((args.search and args.read) or (args.search and args.counts) or (args.read and args.counts) or (args.search and args.map_field) or (args.read and args.map_field) or (args.counts and args.map_field)):
        print('ERROR - Two of f/create_file, d/delete_terrs, and/or p/download_shp must be used when using 3 arguments.\nUse -h or --help for usage information.')
    
    # valid argument or argument combination
    else:
        # display welcome message
        print('Welcome to Tweet Keyword Mapper!\n')
        
        time.sleep(1)   # pause program for a second

        # run create_file function if create_file is an argument
        if args.create_file:
            print('Create a CSV or XLSX File\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            # create file
            create_file(DEFAULT_FILE, WS)
        
        # run download_shapefile function if download_shp is an argument
        if args.download_shp:
            print('Download US State boundaries shapefile from US Census Bureau Website\n')
            
            time.sleep(0.5)   # pause program for half a second
            
            # download US states shapefile from US Census Bureau website
            download_shp(WS)
        
        # run remove_us_territories.py if remove_territories is an argument
        if args.delete_terrs:
            print('Remove US Territories from US States Shapefile')
            
            time.sleep(0.5)   # pause program for half a second
            
            # delete US territories from shapefile
            delete_us_territories(WS)

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
        
        # run map_field function of TweetKeywordGeoPandas() method if map_field is an argument
        elif args.map_field:
            # import TweetKeywordGeoPandas method
            try:
                from tweetkeywordmapper.core.map_services import TweetKeywordGeoPandas
            except:
                from core.map_services import TweetKeywordGeoPandas
            
            print('Map Previous Results from Shapefile Field Using GeoPandas')
            
            time.sleep(0.5)   # pause program for half a second
            
            # run map_field functionality
            TweetKeywordGeoPandas(WS, {}, '', function='map_field')

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