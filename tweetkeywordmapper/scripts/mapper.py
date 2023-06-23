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
    from tweetkeywordmapper.core import map_services as maps
except:
    from core import map_services as maps


"""
# define get_map_service() function - allows user to specify which mapping service they'd like to use
# in order to map their results
"""
def get_map_service(services):
    # display menu of mapping options
    print()
    for s in services:
        print(s)
    print()
    
    # ask user for service they'd like to use
    user_service = input('Which service would you like to map your results with? ')
    
    # validate that the option is in the services list
    while user_service.lower() not in services:
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
    # set services list populated with name of each supported mapping service
    services = ['arcpro', 'geopandas']
    
    # initialize failed_services list to keep track of which services user failed to map with
    failed_services = []
    
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
        map_service = get_map_service(services)
        
        # try loading the geopandas module to check if it's installed
        geopandas_loader = importlib.util.find_spec('geopandas')
    
        # check to see if a path to the ArcGIS Pro executable is present on the system
        pro = shutil.which('ArcGISPro')

        # run code if user wants to use ArcGIS Pro
        if map_service.lower() == 'arcpro':
            # make sure user is using Windows and that ArcGIS Pro is installed before mapping data
            if platform.system() != 'Windows' or (platform.system() == 'Windows' and pro is None):
                if platform.system() != 'Windows':
                    # tell user that they can't map since they are not using Windows
                    print('\nYou are not using Windows, so you cannot map your data using ArcGIS Pro.\n')

                else:
                    # tell user they can't map because ArcGIS Pro is not installed
                    print('\nYou are using Windows, but ArcGIS Pro is not installed.')
                    print('Please install ArcGIS Pro if you would like to map using ArcGIS Pro.\n')
                
                # add arcpro to failed_services list
                failed_services.append('arcpro')
            
            # map results using ArcGIS Pro if user is on Windows and has ArcGIS Pro installed
            else:
                maps.TweetKeywordArcPro(ws, state_counts, keyword)
                
                # return to parent function
                return

        # run code if user wants to use GeoPandas
        else:
            # make sure user has geopandas installed
            if geopandas_loader is None:
                # tell user they cannot map using GeoPandas if it isn't installed on their machine
                print('GeoPandas is not installed on your machine, so you cannot map your results using GeoPandas.\n')
                
                # add geopandas to failed_services list
                failed_services.append('geopandas')

            # map results using GeoPandas if it is installed on user's machine
            else:
                maps.TweetKeywordGeoPandas(ws, state_counts, keyword)
                
                # return to parent function
                return
        
        time.sleep(1.5)     # pause program for a second and a half
        
        # see if user failed to map using either arcpro or geopandas, and try to map using the other service
        if len(failed_services) == 1:
            # run code if user couldn't map using ArcGIS Pro
            if 'arcpro' in failed_services:
                print('Trying to map using GeoPandas...')
                
                time.sleep(1.5)     # pause program for a second and a half
                
                # make sure user has geopandas installed
                if geopandas_loader is None:
                    # tell user they cannot map using GeoPandas if it isn't installed on their machine
                    print('GeoPandas is not installed on your machine, so you cannot map your results using GeoPandas.')

                # map results using GeoPandas if it is installed on user's machine
                else:
                    maps.TweetKeywordGeoPandas(ws, state_counts, keyword)
            
            # run code if user couldn't map using geopandas
            else:
                print('Trying to map using ArcGIS Pro...')
                
                time.sleep(1.5)     # paused program for a second and a half
                
                # make sure user is using Windows and that ArcGIS Pro is installed before mapping data
                if platform.system() != 'Windows' or (platform.system() == 'Windows' and pro is None):
                    if platform.system() != 'Windows':
                        # tell user that they can't map since they are not using Windows
                        print('\nYou are not using Windows, so you can not map your data using ArcGIS Pro.')

                    else:
                        # tell user they can't map because ArcGIS Pro is not installed
                        print('\nYou are using Windows, but ArcGIS Pro is not installed.')
                        print('Please install ArcGIS Pro if you would like to map using ArcGIS Pro.')

                # map results using ArcGIS Pro if user is on Windows and has ArcGIS Pro installed
                else:
                    maps.TweetKeywordArcPro(ws, state_counts, keyword)
