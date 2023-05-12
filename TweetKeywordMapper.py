"""

@Name: TweetKeywordMapper.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Allows user to either search Twitter for Tweets that meet a specified keyword, or
              import Tweet data from a csv file. The state and ID for each Tweet will be identified and collected,
              and then the number of Tweets that appear in each state will be tallied. The results will then
              be displayed and the user will have the option to map the data using ArcGIS Pro.
@Requirements: Python3, TweetKeywordConstants, TweetKeywordData, TweetKeywordArcPro

"""

# import modules/libraries
import TweetKeywordConstants as cons
import TweetKeywordData as data
import TweetKeywordArcPro as arc
import importlib
import os
import time
import platform
import shutil

# set workspace
ws = cons.workspace

# set default csv file
default_csv = cons.default_csv

# get states and cities dictionary from TweetKeywordConstants module
states = cons.states
cities = cons.cities


# define TweetKeywordMapper() function - main function
def TweetKeywordMapper(ws, states):
    # determine if tweepy is downloaded
    tweepy_loader = importlib.util.find_spec('tweepy')

    # check to see if a path to the ArcGIS Pro executable is present on the system
    pro = shutil.which('ArcGISPro')

    # create the default csv file if it does not already exist within the workspace
    # add first row to file containing headers Tweet_ID and State
    if not os.path.exists(default_csv):
        data.csv_interact(('Tweet_ID', 'Keyword', 'State'), default_csv)

        # display that default file was successfully create
        print(f'Default file created called: {default_csv}')

        # pause program for a second
        time.sleep(1)

    # ask if user would like to import data from a csv file or search directly
    where = data.where_data()
    
    # when the user chooses to search the Twitter API, make sure they have Tweepy installed
    if where == '1' and tweepy_loader is not None:
        places, tweet_ids, state_counts, keyword = data.TweetKeywordSearch(ws, default_csv, states, cities)

    # run this code when the user either chooses to import Tweet data from csv
    # or the Tweepy library is not installed on their machine
    else:
        # display that Tweepy is not installed if that is the case
        if where == '1' and tweepy_loader is None:
            print('Tweepy is not downloaded onto your machine, so you will have to import from a csv.')

        # ask user for file, and use default file if input is left blank
        user_file = data.get_user_csv_file(default_csv)

        # extract state data and fields from csv file
        places, tweet_ids, keyword = data.csv_interact((), user_file, ws, mode='r', checkKeyword=True)

        # get Tweet counts for each state using data
        state_counts = data.get_state_counts(places, states)

        # get number of tweets that were returned
        num_results = len(tweet_ids)

        # display how many search results were returned
        if num_results == 0:
            print(f'Reading from {user_file} returned no results.')
        else:
            print(f'Reading from {user_file} returned {num_results} results.\n')

    # display results
    print(f'\nKeyword: {keyword}\n\nIDS: {tweet_ids}\n\nPlaces: {places}\n\nCounts: {state_counts}\n')

    # ask user if they would like to map the results using ArcGIS Pro
    ifMap = input('Would you like to map the results using ArcGIS Pro? (Y or N) ')

    # validate that ifMap input is valid
    while ifMap.title() != 'Yes' and ifMap.upper() != 'Y' and ifMap.title() != 'No' and ifMap.upper() != 'N':
        # display error
        print(f'{ifMap} is not a valid option.')

        # ask user again if they would like to map the results using ArcGIS Pro
        ifMap = input('Would you like to map the results using ArcGIS Pro? (Y or N) ')

    # map data if the user signalled that they want to
    if ifMap.title() == 'Yes' or ifMap.upper() == 'Y':
        # make sure user is using Windows and that ArcGIS Pro is installed before mapping data
        if platform.system() != 'Windows':
            # tell user that they can't map since they are not using Windows
            print('You are not using Windows, so you can not map your data.')
        elif platform.system() == 'Windows' and pro is None:
            # tell user they can't map because ArcGIS Pro is not installed
            print('You are using Windows, but ArcGIS Pro is not installed.')
            print('Please install ArcGIS Pro if you would like to map.')
        else:
            # run TweetKeywordArcPro function in order to map state Tweet counts
            # if user is using Windows and ArcGIS Pro is installed
            arc.TweetKeywordArcPro(ws, state_counts, keyword)

    # display goodbye
    print('Thank you for using Tweet Keyword Mapper!')


# run the program
if __name__ == '__main__':
    TweetKeywordMapper(ws, states)
