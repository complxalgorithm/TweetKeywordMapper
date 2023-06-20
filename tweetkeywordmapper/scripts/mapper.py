"""

@Name: mapper.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Gives user the option to map the Tweet count data using ArcGIS Pro or GeoPandas for each US state.
@Requirements: Python3

"""


# import modules
import os
import platform
import importlib
import shutil
import time

try:
    from tweetkeywordmapper.core import TweetKeywordMapServices as maps
except:
    from core import TweetKeywordMapServices as maps


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
def TweetKeywordMapper(ws, state_counts, keyword):
    # ask user if they would like to map the results
    ifMap = input('Would you like to map the results? (Y or N) ')

    # validate that ifMap input is valid
    while ifMap.title() not in ('Yes', 'No') and ifMap.upper() not in ('Y', 'N'):
        # display error
        print(f'{ifMap} is not a valid option.')

        # ask user again if they would like to map the results using ArcGIS Pro
        ifMap = input('Would you like to map the results? (Y or N) ')

    # map data if the user signalled that they want to
    if ifMap.title() == 'Yes' or ifMap.upper() == 'Y':
        # get the platform the user would like to map with
        map_service = get_map_service()
        
        # try loading the geopandas module to check if it's installed
        geopandas_loader = importlib.util.find_spec('geopandas')
    
        # check to see if a path to the ArcGIS Pro executable is present on the system
        pro = shutil.which('ArcGISPro')

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
