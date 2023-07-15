# import modules
import time

try:
    from tweetkeywordmapper.core import data
    from tweetkeywordmapper.core import constants as cons
except:
    from core import data
    from core import constants as cons


"""
# define delete_us_territories() function - remove US territories from US state boundaries shapefile
"""
def delete_us_territories(ws):
    import os
    import pandas as pd
    import geopandas as gpd
    
    # initialize list of abbreviations of US territories
    territories = ['AS', 'GU', 'MP', 'PR', 'VI']
    
    # get shapefile and shp's parent directory
    shp_file, shp_dir = data.get_shapefile(ws)
    
    # read shapefile
    states_df = gpd.read_file(shp_file)
    
    # get list of all fields
    fields_list = states_df.head()
    
    # display field options found in shapefile
    print()
    for f in fields_list:
        print(f)
    print()
    
    # ask user which field holds the abbreviations of the states
    user_field = input('Which field has the abbreviations of the states? ')

    # validate that user_field is in the field_names list
    while user_field not in fields_list:
        # display an error
        print(f'{user_field} is not a field. Please try again.')

        # ask user again to specify the state abbreviations field
        user_field = input('Which field has the abbreviations of the states? ')
    
    # initialize dropped_territories list
    dropped_territories = []
    
    # iterate through each row of the us states shapefile
    for num, state in states_df[user_field].items():
        # if the abbreviation is in the territories list, remove it from the dataframe
        # and add it to the dropped_territories list
        if state in territories:
            states_df.drop(states_df[states_df[user_field] == state].index, inplace=True)
            
            dropped_territories.append(state)
        
    # join shp_dir with states_shp name in order to generate new shapefile
    shp_path = os.path.join(shp_dir, shp_file)
    
    # generate updated shapefile with new count field and respective count values
    states_df.to_file(shp_path)
    
    time.sleep(1)   # pause program for a second
    
    # display which territories were dropped
    if len(dropped_territories) > 0:
        dropped = ', '.join(dropped_territories)
        
        print(f'{dropped} were removed from {shp_file}\n')
    
    else:
        print(f'No territories were in {shp_file}\n')
    
    time.sleep(0.5) # pause program for half a second