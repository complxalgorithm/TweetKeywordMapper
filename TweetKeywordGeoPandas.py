"""

@Name: TweetKeywordGeoPandas.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Maps the Tweet data using GeoPandas.
              Can only work with shapefiles.
@Requirements: geopandas, matplotlib

"""


# import libraries
import TweetKeywordData as data
import os
import warnings


"""
# define TweetKeywordGeoPandas.py function - maps the state counts using the GeoPandas library
"""
def TweetKeywordGeoPandas(ws, counts, keyword):
    # ignore all warnings that GeoPandas may output
    warnings.filterwarnings("ignore")
    
    # import libraries/modules
    import pandas as pd
    import geopandas as gpd
    import matplotlib.pyplot as plt
    
    # get US states shapefile
    states_shp, shp_dir = data.get_shapefile(ws)
    
    # read shapefile
    states_df = gpd.read_file(states_shp)
    
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
    
    # set name of the field to be created in states feature class
    new_field = data.set_new_field(keyword)
	
    # go through each value in the states abbreviations field in the states shapefile
    for num, state in states_df[user_field].items():
        # iterate through each state and count value in counts dict
        for st, count in counts.items():
            # when it reaches the current state, add counts value for the current state
            # as its new_field value
            if st == state:
                states_df.loc[states_df[user_field] == state, new_field] = int(count)
        
    # join shp_dir with states_shp name in order to generate new shapefile
    shp_path = os.path.join(shp_dir, states_shp)
    
    # generate updated shapefile with new count field and respective count values
    states_df.to_file(shp_path)
    
    # read updated US states shapefile
    states_df = gpd.read_file(shp_path)
    
    # get list of all fields
    fields_list = states_df.head()
    
    # display field options found in shapefile
    print()
    for f in fields_list:
        print(f)
    print()
    
    # ask user which field holds the Tweet count values
    plot_field = input('Choose the Tweet count field that was generated to plot it: ')

    # validate that user_field is in the field_names list
    while plot_field not in fields_list:
        # display an error
        print(f'{plot_field} is not a field. Please try again.')

        # ask user again to specify which field holds the Tweet count
        plot_field = input('Which field has the abbreviations of the states? ')
    
    """
    # generate map of the states shapefile using the plot_field as the column to plot
    # sets axes using layer from gpd naturalearth_lowres
    """
    
    # set title of map using the keyword
    if keyword == '':
        map_title = 'Tweet Count'
    else:
        map_title = f'{keyword} Tweet Count'
    
    # get low resolution map of world from datasets
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    # filter all countries except for the USA
    usa = world[world.name == 'United States of America']
    
    # get axes of USA dataset
    ax = usa.plot()
    
    # plot states shapefiles using above axes and plot_field, setting color scheme to red
    # and including a legend	
    states_df.plot(ax=ax, column=plot_field, cmap='OrRd', legend=True)
    
    # get min/max x and min/max y values from usa dataset
    minx, miny, maxx, maxy = usa.total_bounds
    
    # set x and y limits using above values
    ax.set_xlim(minx-5, maxx+5)
    ax.set_ylim(miny-5, maxy+5)
    
    # set title of plot using map_title value
    ax.set_title(map_title)
    
    # show map in new window
    plt.show()
    
    # return to parent function
    return
