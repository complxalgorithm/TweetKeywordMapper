"""

@Name: TweetKeywordArcPro.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Maps the Tweet data using ArcGIS Pro.
@Requirements: arcpy

"""

# import libraries
import os
import sys


# define TweetKeywordArcPro() function - maps the state counts using ArcGIS Pro
def TweetKeywordArcPro(ws, counts, keyword):
    # import arcpy library
    import arcpy
    
    # set workspace
    arcpy.env.workspace = ws
    arcpy.env.overwriteOutput = True

    # get list of feature classes from workspace
    fcs = arcpy.ListFeatureClasses()

    # display menu of available feature classes in the gdb
    print()
    for i, fc in enumerate(fcs):
        print(f'{i+1}: {fc}')
    print()

    # ask user to enter their state feature class or shapefile
    states_fc = input('Choose a feature class from the menu: ')

    # validate that the feature class exists
    while states_fc not in fcs:
        # display an error
        print(f'{states_fc} is not a feature class.')

        # ask user to enter states feature class name again
        states_fc = input('Choose a feature class from the menu: ')

    print(f'\n{states_fc} found in {ws}\n')

    # get fields from feature class
    fields = arcpy.ListFields(states_fc)

    # initialize field_names list
    field_names = []

    # go through each field object an add its name to field_names list
    for field in fields:
        print(field.name)
        field_names.append(field.name)

    # ask user which field holds the abbreviations of the states
    user_field = input('Which field has the abbreviations of the states? ')

    # validate that user_field is in the field_names list
    while user_field not in field_names:
        # display an error
        print(f'{user_field} is not a field. Please try again.')

        # ask user again to specify the state abbreviations field
        user_field = input('Which field has the abbreviations of the states? ')

    # set name of the field to be created in states feature class
    if keyword == '':
        # name if results were not filtered using a keyword
        new_field = 'Tweet_Count'
    else:
        # split the keyword using a space
        words = keyword.split(' ')

        # name if results were filtered using a keyword
        if len(words) > 1:
            # name if keyword had more than 1 word
            key_str = '_'.join(words)   # join the separate words with a _ in between each word
            new_field = key_str
            new_field = f'{new_field}_Tweet_Count'
            
        # name if the keyword only had one word    
        else:
            new_field = f'{keyword}_Tweet_Count'

    # create new field in states feature class, and display that it was successful
    arcpy.AddField_management(states_fc, new_field, "LONG", field_alias=new_field)
    print()

    # create update cursor of states feature class that pulls state abbrevs field and the created field
    update = arcpy.da.UpdateCursor(states_fc, [user_field, new_field])

    # go through each row of the update cursor
    for row in update:
        # iterate through each state key in counts dictionary
        for state in counts:
            # once state is reached, add its respective Tweet count value and then update the row
            if state == row[0]:
                row[1] = counts[state]
                update.updateRow(row)

        # display each state and its count
        print(f'{row[0]}: {row[1]}')

    # delete update cursor
    del update

    # tell user that the Tweet counts were successfully added to
    print(f'Tweet counts for each state successfully added to {new_field} in {states_fc}.')

    """
    # this code changes the symbology of the states_fc layer to graduated values using natural breaks
    # this code was configured based off of the code sample on the below link:
    # https://pro.arcgis.com/en/pro-app/latest/arcpy/mapping/graduatedsymbolsrenderer-class.htm
    """
    """
    # get current working directory
    path = os.path.dirname(sys.argv[0])

    #
    project = arcpy.mp.ArcGISProject(path + r"\GEG238_Project.aprx")
    mp = project.listMaps("Map")[0]
    states_layer = mp.listLayers(states_fc)[0]
    symb = states_layer.symbology

    #
    if hasattr(symb, 'renderer'):
        if symb.renderer.type == "GraduatedSymbolsRenderer":
            # modify graduated symbol renderer
            symb.renderer.classificationField = user_field
            symb.renderer.classificationMethod = 'NaturalBreaks'
            symb.renderer.colorRamp = project.listColorRamps("Blue to White")[0]

            #
            states_layer.symbology = symb
    """
