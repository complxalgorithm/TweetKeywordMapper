#!/usr/bin/env python3
# coding: utf-8

"""

@Name: TweetKeywordMapper.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Allows user to either search Twitter for Tweets that meet a specified keyword, or
              import Tweet data from a csv file using a keyword. The state and ID for each Tweet will be identified
              and collected, and then the number of Tweets that appear in each state will be tallied. The results
              will then be displayed and the user will have the option to map the data using ArcGIS Pro.
@Requirements: Python3, pandas, geopandas, tweepy, matplotlib, numpy, arcpy

"""


# import modules/libraries
import os
import platform
import importlib
import shutil
import time
from tweetkeywordmapper.core import TweetKeywordConstants as cons
from tweetkeywordmapper.core import TweetKeywordData as data
from tweetkeywordmapper.core import TweetKeywordMapServices as maps
from tweetkeywordmapper.scripts import counts


"""
# define get_map_service() function - allows user to specify which mapping service they'd like to use
# in order to map their results
"""
def get_map_service():
    # set services list populated with name of each supported mapping service
    services = ['ArcPro', 'GeoPandas']
    
    # display menu of mapping options
    print()
    for s in services:
        print(s)
    print()
    
    # ask user for service they'd like to use
    user_service = input('Which service would you like to map your results with? ')
    
    # validate that the option is in the services list
    while user_service not in services:
        # display an error
        print('That is not an available service.')
        
        # ask user again for service they'd like to use
        user_service = input('Which service would you like to map your results with? ')
    
    # return service to parent function
    return user_service
    

"""
# define TweetKeywordMapper() function - main function that will get results and allow user to
# map them if results were found
"""
def TweetKeywordMapper():
    # set workspace from TweetKeywordConstants module
    ws = cons.workspace

    # set default csv file from TweetKeywordConstants module
    default_csv = cons.default_csv

    # get states and cities dictionary from TweetKeywordConstants module
    states = cons.states
    cities = cons.cities
    
    # try loading the tweepy module as a way to check if it's installed
    tweepy_loader = importlib.util.find_spec('tweepy')
    
    # try loading the geopandas module to check if it's installed
    geopandas_loader = importlib.util.find_spec('geopandas')
    
    # check to see if a path to the ArcGIS Pro executable is present on the system
    pro = shutil.which('ArcGISPro')
    
    # create the default csv file if it does not already exist within the workspace
    # add first row to file containing headers Tweet_ID, Keyword, and State
    if not os.path.exists(default_csv):
        data.csv_interact(('Tweet_ID', 'Keyword', 'State'), default_csv, ws)

        # display that default file was successfully create
        print(f'Default file created called: {default_csv}')

        # pause program for a second
        time.sleep(1)

    # ask if user would like to import data from a csv file or search directly
    where = data.where_data()
    
    # when the user chooses to search the Twitter API, make sure they have Tweepy installed
    if where == '1' and tweepy_loader is not None:
        places, tweet_ids, state_counts, keyword = data.TweetKeywordSearch(ws, default_csv, states, cities)
        
        # get number of tweets that were returned
        num_results = len(tweet_ids)
        
        time.sleep(1) # pause program for a second
        
        # display results if any were found
        if num_results > 0:
            print(f'\nKeyword: {keyword}\n\nIDs: {tweet_ids}\n\nPlaces: {places}\n\nCounts: {state_counts}\n')

    # run this code if the use wants to count total for each unique field value of a field from a csv file
    elif where == '3':
        # set number of results to 0
        num_results = 0
        
        # run counts program
        counts.main()
    
    # run this code when the user either chooses to import Tweet data from csv
    # or the Tweepy and/or Numpy libraries are not installed on their machine
    else:
        # display that Tweepy is not installed if either or both is the case
        if where == '1' and tweepy_loader is None:
            if tweepy_loader is None:
                print('Tweepy is not downloaded onto your machine.')
            
            print('You will have to import from a csv.')

        # ask user for file, and use default file if input is left blank
        user_file = data.get_user_csv_file(default_csv)

        # extract state data and fields from csv file
        places, tweet_ids, keywords = data.csv_interact((), user_file, ws, mode='r', checkKeyword=True)

        # get Tweet counts for each state using data
        state_counts = data.get_state_counts(places, states)

        # get number of tweets that were returned
        num_results = len(tweet_ids)
        
        # set keyword value using keywords list
        keyword = ' '.join(keywords)
        
        # display how many search results were returned
        if num_results == 0:
            print(f'Reading from {user_file} returned no results.')
            time.sleep(1) # pause program for a second
        
        # display results if any were found
        else:
            print(f'Reading from {user_file} returned {num_results} results.\n')
            
            time.sleep(1) # pause program for a second

            # display results if any were found
            print(f'\nKeywords: {keyword}\n\nIDs: {tweet_ids}\n\nPlaces: {places}\n\nCounts: {state_counts}\n')
    
    time.sleep(1)   # pause program for a second
    
    # run mapping functionality if results were found
    if num_results > 0:
        # get what percentage of the total number of results came from each state
        # will only include the states that have Tweets
        state_counts_percents = data.get_count_percentages(state_counts, num_results, states)

        # display the percentages
        print('Percent of Tweets That Came From Each State')
        print('-------------------------------------------')
        for state, percent in state_counts_percents.items():
            print('{:<30s} {:<6}'.format(state + ':', percent))
        print()

        time.sleep(1)   # pause program for a second
        
        # ask user if they would like to map the results
        ifMap = input('Would you like to map the results? (Y or N) ')

        # validate that ifMap input is valid
        while ifMap.title() != 'Yes' and ifMap.upper() != 'Y' and ifMap.title() != 'No' and ifMap.upper() != 'N':
            # display error
            print(f'{ifMap} is not a valid option.')

            # ask user again if they would like to map the results using ArcGIS Pro
            ifMap = input('Would you like to map the results? (Y or N) ')

        # map data if the user signalled that they want to
        if ifMap.title() == 'Yes' or ifMap.upper() == 'Y':
            # get the platform the user would like to map with
            map_service = get_map_service()

            # run code if user wants to use ArcGIS Pro
            if map_service == 'ArcPro':
                # make sure user is using Windows and that ArcGIS Pro is installed before mapping data
                if platform.system() != 'Windows':
                    # tell user that they can't map since they are not using Windows
                    print('You are not using Windows, so you can not map your data using ArcGIS Pro.')

                elif platform.system() == 'Windows' and pro is None:
                    # tell user they can't map because ArcGIS Pro is not installed
                    print('You are using Windows, but ArcGIS Pro is not installed.')
                    print('Please install ArcGIS Pro if you would like to map using ArcGIS Pro.')

                else:
                    # run TweetKeywordArcPro function in order to map state Tweet counts
                    # if user is using Windows and ArcGIS Pro is installed
                    maps.TweetKeywordArcPro(ws, state_counts, keyword)

            # run code if user wants to use GeoPandas
            else:
                # map results using GeoPandas if it is installed on user's machine
                if geopandas_loader is not None:
                    # map results using GeoPandas
                    maps.TweetKeywordGeoPandas(ws, state_counts, keyword)
                
                # tell user they cannot map using GeoPandas if it isn't installed on their machine
                else:
                    print('GeoPandas is not installed on your machine, so you cannot map your results using GeoPandas.')

    # display goodbye after the full program has executed
    print('\nThank you for using Tweet Keyword Mapper!')


"""
# execute the program
"""
if __name__ == '__main__':
    TweetKeywordMapper()
