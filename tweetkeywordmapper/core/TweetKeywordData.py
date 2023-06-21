"""

@Name: TweetKeywordData.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Contains most functions that are imperative to running the program. This includes
              the algorithm used to determine the state of origin of each Tweet result, 
              as well as the csv_interact() function.
@Requirements: tweepy, pandas, numpy

"""


# import libraries
import pandas as pd
import numpy as np
import csv
import os
import time
import re


"""
# define get_states_from_results() function - uses search results to populate places list with
# full name of the state that each of the tweets with geolocation info was tweeted from
"""
def get_states_ids_from_results(results, api, states, cities, num):
    # initialize tweet ids list to store ids of tweets
    tweet_ids = []
    
    # intialize places list to store locations of tweets
    places = []
    
    # initialize counter
    count = 0
    
    # iterate through each result
    for tweet in results:
        # create status dict of tweet data
        status = tweet.__dict__
        
        # get tweet id and screen name
        tweet_id = status['_json']['id']
        screen_name = status['_json']['user']['screen_name']
        
        print(f'Tweet ID: {tweet_id}\n')
        #print(f'Screen Name: {screen_name}')
        
        # try to get status data using the tweet id
        # try to get user data using the screen name
        try:
            stat = api.get_status(tweet_id)
            user = api.get_user(screen_name=f'{screen_name}')
        except Exception:
            # tell user when data can't be pulled for either the status or the user
            print(f'Data for {tweet_id} cannot be pulled at this time.\n')
            time.sleep(1.5)   # pause program for a second
        else:
            # get the state from which the tweet was sent
            place = get_state(stat, user, states, cities)

            print(f'State: {place}\n')
        
            # append to places list if the place value is a key or value in states dict
            if (place != '') and ((place in states) or (place in states.values())):
                # append the tweet id to tweet_ids list
                tweet_ids.append(tweet_id)
                
                # when place value is a key in states dict, get its value and add to places list
                if place in states:
                    places.append(states[place])
                # when place value is a value in states dict, add that value to places list
                else:
                    places.append(place)
            
                # add 1 to counter
                count += 1
                print(f'{count}\n')
        
            # break from the loop once the user-inputted results number is reached
            if count == num:
                break
    
    # return places list to parent function
    return places, tweet_ids


"""
# define get_state() function - extracts the state from each tweet using either the Status or User model
"""
def get_state(s, u, states, cities):
    # run this code if there is a place object in status model for the tweet
    if s.place is not None:
        # set variable to place object of status model
        pl = s.place
        
        # return empty string if the country is not the USA
        if pl.country != 'United States':
            return ''
            
        # if the tweet was from the USA, use full name of locality
        else:
            place = pl.full_name
            print(f'Place: {place}\n')
            
            # if pl value hasn't been returned and is not blank or a space, set pl to the original place value
            # if it is blank or a space then return an empty string
            if place == '' or place == ' ':
                return ''
            else:
                pl = place
            
    # run this if there is no place object, but the user allows twitter to access their location
    elif (s.place is None) and (u.geo_enabled == True):
        # get the location that the user has on their profile,
        # then split the value using the comma as the delimiter, and store all words
        place = u.location
        print(f'Place: {place}\n')
        try_split = place.split(', ')
        
        # if pl value hasn't been returned and is not blank or a space, set pl to the original place value
        # if it is blank then return an empty string
        if place == '' or place == ' ':
            return ''
        else:
            pl = place
            
    # if none of these situations are the case for the tweet, return an empty string
    else:
        return ''
    
    # when the found place has a value, try to extract the state from the value
    if pl.find('via') == -1 and pl.find('from') == -1:
        return find_state_in_place_value(pl, states, cities)
    elif pl.find('via') != -1:
        return find_state_in_place_value(pl, states, cities, word='via')
    else:
        return find_state_in_place_value(pl, states, cities, word='from')


"""
# define search_for_state() function - looks for instance of a state abbreviation or name of a city
# within the place value and returns an object if an instance is found
# CREDIT: Hugh Bothwell
# https://stackoverflow.com/questions/5319922/check-if-a-word-is-in-a-string-in-python
"""
def search_for_state_city(p):
    return re.compile(r'\b({0})\b'.format(p), flags=re.IGNORECASE).search


"""
# define find_state_in_place_value() function - searches for any mention of a state or city and returns the state value
# that is most likely to be the state of origin of the Tweet
"""
def find_state_in_place_value(place, states, cities, word=''):
    # initialize num_found_states variable to keep track of how many states could be pulled
    # from the place value
    num_found_states = 0
    
    # initialize found_states_indexes dictionary to store found states and where
    # they are located within the place value string
    found_states_indexes = {}
    
    # iterate through each city in the cities dictionary
    for c in cities:
        # run this code if a city mention is within the place value
        if search_for_state_city(c)(place.upper()) is not None or search_for_state_city(c)(place.title()) is not None:
            # do this if mention of city is found within uppercased version of place value
            if search_for_state_city(c)(place.upper()) is not None:
                # attempt to get index/location of mention within place value
                try:
                    place.upper().index(c)
                
                # move on if nothing was found
                except ValueError:
                    pass
                
                # run this if index/location of mention within place value was found
                else:
                    # display the city value that was found
                    # this could also include other names or abbreviations of states
                    print(f'City Found: {c}')
                    
                    # get result object of value that was found
                    result = search_for_state_city(c)(place)
                    
                    # make sure the result is not a common word
                    if result.group(1) not in ('la', 'La'):
                        # only add to found states counter if it isn't in the found_states_indexes dictionary
                        if cities[c] not in found_states_indexes:
                            num_found_states += 1
            
                        else:
                            print(f'{cities[c]} has already been found.')
                        
                        # add the state and its index within the place value to the found_states_indexes dictionary
                        # if the index is not already in the dictionary
                        if place.upper().index(c) not in found_states_indexes.values():
                            found_states_indexes[cities[c]] = place.upper().index(c)
                    
                        else:
                            print(f'A state has already been found at {place.title().index(c)}.')
                    
                    # tell user if the result may be a common word, and don't include it
                    else:
                        print('Probably doesn\'t refer to a city.')
            
            # move on if this fails
            else:
                pass
            
            # do this if mention of city is found within titled version of place value
            if search_for_state_city(c)(place.title()) is not None:
                # attempt to get index/location of mention within place value
                try:
                    place.title().index(c)
                
                # move on if nothing was found
                except ValueError:
                    pass
                
                # run this if index/location of mention within place value was found
                else:
                    # display the city value that was found
                    # this could also include other names or abbreviations for states
                    print(f'City Found: {c}')
                    
                    # get result object of value that was found
                    result = search_for_state_city(c)(place)
                    
                    # make sure the result is not a common word
                    if result.group(1) not in ('la', 'La'):
                        # only add to found states counter if it isn't in the found_states_indexes dictionary
                        if cities[c] not in found_states_indexes:
                            num_found_states += 1
            
                        else:
                            print(f'{cities[c]} has already been found.')
                        
                        # add the state and its index within the place value to the found_states_indexes dictionary
                        # if the index is not already in the dictionary
                        if place.title().index(c) not in found_states_indexes.values():
                            found_states_indexes[cities[c]] = place.title().index(c)
                    
                        else:
                            print(f'A state has already been found at {place.title().index(c)}.')
                    
                    # tell user if the result may be a common word, and don't include it
                    else:
                        print('Probably doesn\'t refer to a city.')
            
            # move on if this fails
            else:
                pass
        
        # move on if a city could not be found
        else:
            pass
    
    # iterate through each state in the states dictionary
    for s in states:
        # run this code if a state mention is within the place value
        if search_for_state_city(s)(place.upper()) is not None or search_for_state_city(states[s])(place.title()) is not None:
            # do this if mention of state's abbreviation is found within uppercased version of place value
            if search_for_state_city(s)(place.upper()) is not None:
                # display the state abbreviation that was found
                print(f'State Found: {s}')

                # attempt to find the index of a mention of the current state in a uppercased version of the place value
                try:
                    place.upper().index(s)

                # move on if nothing was found
                except ValueError:
                    pass

                # the index/location of a mention of the state was found in the place value
                else:
                    # set the resulting search object to result variable
                    result = search_for_state_city(s)(place)
                    
                    # trying to fix issue where a place value of 'LA' returns Louisiana
                    # this is almost always referring to Los Angeles, California
                    if place == 'LA':
                        print('Probably should be California.\n')

                        found_states_indexes['California'] = place.upper().index('LA')

                    # make sure the result is not a common word
                    if result.group(1) not in ('in', 'In', 'me', 'Me', 'de', 'la', 'La', 'or', 'Or', 'Ca', 'Mt', 'Co', 'co', 'oh', 'Oh'):
                        # only add to found states counter if it isn't in the found_states_indexes dictionary
                        if states[s] not in found_states_indexes:
                            num_found_states += 1

                        else:
                            # trying to fix LA/California issue
                            if result.group(1) == 'LA':
                                print('California has already been found.')
                            else:
                                print(f'{states[s]} has already been found.')
                        
                        # add the state and its index within the place value to the found_states_indexes dictionary
                        # if the index is not already in the dictionary
                        if place.upper().index(s) not in found_states_indexes.values():
                            found_states_indexes[states[s]] = place.upper().index(s)
                            
                        else:
                            print(f'A state has already been found at {place.upper().index(s)}.')
                        

                    # run if the result is not a common word
                    else:
                        # had to add this because I was getting the location of the foreign place that had 'Ca' in the name
                        # and was preceded by 'Au'
                        if (search_for_state_city('AU')(place.upper()) is None) and (result.group(1) not in ('in', 'In', 'me', 'Me', 'de', 'la', 'La', 'or', 'Or', 'Mt', 'Co', 'co', 'oh', 'Oh')):
                            # only add to found states counter if it isn't in the found_states_indexes dictionary
                            if states[s] not in found_states_indexes:
                                num_found_states += 1
                            
                            else:
                                print(f'{states[s]} has already been found.')
                            
                            # add the state and its index within the place value to the found_states_indexes dictionary
                            # if the index is not already in the dictionary
                            if place.upper().index(s) not in found_states_indexes.values():
                                found_states_indexes[states[s]] = place.upper().index(s)

                            # tell user when a state has already been found at that index
                            else:
                                print(f'A state has already been found at {place.upper().index(s)}.')

                        # tell user when the found result may not refer to a state
                        else:
                            print(f'Probably doesn\'t refer to a state.\n')

            # do this if mention of state's name is found within titled version of place value
            elif search_for_state_city(states[s])(place.title()) is not None:
                # display the state name that was found
                print(f'State Found: {states[s]}')

                # attempt to find the index of a mention of the current state in a titled version of the place value
                try:
                    place.title().index(states[s])
                
                # move on if nothing was found
                except ValueError:
                    pass
                
                # the index/location of a mention of the state was found in the place value
                else:
                    # only add to found states counter if it isn't in the found_states_indexes dictionary
                    if states[s] not in found_states_indexes:
                        num_found_states += 1

                    else:
                        print(f'{states[s]} has already been found.')
                    
                    # add the state and its index within the place value to the found_states_indexes dictionary
                    # if the index is not already in the dictionary
                    if place.title().index(states[s]) not in found_states_indexes.values():
                        found_states_indexes[states[s]] = place.title().index(states[s])
                    
                    else:
                        print(f'A state has already been found at {place.title().index(states[s])}.')
                    

            # move on if a state abbreviation or name could not be found
            else:
                pass
        
        # move on if a state abbreviation or name could not be found
        else:
            pass
    
    # display the number of states found and which states were found and the location
    # of each found state
    print(f'Number of Found States: {num_found_states}')
    print(f'States and Locations in Place: {found_states_indexes}\n')
    time.sleep(0.5)     # pause program for half a second
    
    # return an empty string if no states could be extracted from the place value
    if num_found_states == 0 or len(list(found_states_indexes.keys())) == 0:
        return ''
    else:
        # get list of found states
        found = list(found_states_indexes.keys())
        
        # get list of found indexes
        indexes = list(found_states_indexes.values())
        
        # sort index values from first to last
        sorted_values = np.argsort(indexes)
        
        # recreate sorted found_states_indexes dictionary
        found_states_indexes = {found[s]: indexes[s] for s in sorted_values}
        
        # return the first state that was found if the place value contains 'via' or 'from'
        # as long as there was more than 1 state found
        if word == 'via' or word == 'from':
            if num_found_states > 1:
                return found[indexes.index(min(found_states_indexes.values()))]
            
            else:
                return found[0]
        
        # return the last state that was found if the place value doesn't contain 'via' or 'from'
        # as long as there was more than 1 state found
        else:
            if num_found_states > 1:
                return found[indexes.index(max(found_states_indexes.values()))]
            
            else:
                return found[0]


"""
# define get_counts() function - uses places list to count total number of tweets from
# each state in the search results
#   - df       -> default to None
#   - field    -> default to empty string
#   - function -> default to empty string
"""
def get_counts(values, states, df=None, field='', function=''):
    # run this if counts called this function
    if function == 'counts':
        # initialize counts list
        counts = []
        
        # iterate through each unique value in values list
        for v in values:
            # get rows that contain the field value
            field_contents = df[df[field] == v]

            # count how many rows there are with that value
            count = len(field_contents)

            # add this count to the counts list
            counts.append(count)
        
        # create dictionary of counts for each available unique field value
        value_counts = dict(zip(values, counts))

        # sort counts from highest to lowest
        sorted_counts = reversed(np.argsort(counts))

        # created sorted value_counts dictionary
        value_counts = {values[k]: counts[k] for k in sorted_counts}
        
        # return value_counts dictionary to parent function
        return value_counts
    
    # run this code if another script called this function
    else:
        # initialize counts dictionary
        counts = {}
    
        # iterate over the keys in states dict
        for s in states:
            # initialize counter to 0
            count = 0
            
            # iterate through each place in values list
            for p in values:
                # if the place is equal to the current states dict value, add 1 to the counter
                if p == states[s]:
                    count += 1

            # add current state's abbreviation key and its count as the next key/value combo in counts dict
            counts[s] = count
        
        # return counts dict to parent function
        return counts


"""
# define get_count_percentages() function - calculates for each state/unique field value the percent
# of the total number of Tweets and adds each value and the percent to the percents dictionary
# then returns that dictionary to the parent function
#   - function -> default to mapper
"""
def get_count_percentages(counts, num_res, states, function='mapper'):
    # initialize percents dictionary
    percents = {}
    
    # iterate through each state and its count
    for value, count in counts.items():
        # run this if counts script is calling this function
        if function == 'counts':
            # add unique value and its percentage of total to percents dictionary
            percents[value] = '{:.2%}'.format(count / num_res)
        
        # run this if other scripts are calling this function
        else:
            # only do this for states that have results
            if count > 0:
                # add full name of state as key and percent of total results as value
                # to percents dictionary
                percents[states[value]] = '{:.2%}'.format(count / num_res)
    
    # return percents dictionary to the parent function
    return percents


"""
# define get_user_csv_file() function - get a csv file from the user, then return valid file
"""
def get_user_csv_file(default):
    # ask user to enter their file, or use the default csv file
    user_file = input('Enter csv file from your current directory, or hit enter to use default file: ') or default
    
    # automatically return value if the input is the same as the default csv file
    if user_file == default:
        return default
    
    # get extension of input file
    file_ext = user_file.split('.')[-1]
    
    # validate that file exists and that the file is a csv file
    while os.path.exists(user_file) == False or file_ext != 'csv':
        # display error if input doesn't exist
        if os.path.exists(user_file) == False:
            print(f'{user_file} does not exist in your current directory.')
        # display error if input isn't a csv file
        elif file_ext != 'csv':
            print(f'{user_file} is not a csv file.')
            
        # ask user for file again, and use default file if input is left blank
        user_file = input('Enter file from your current directory, or hit enter to use default file: ') or default
        
        # get extension of new input file
        file_ext = user_file.split('.')[-1]
    
    # return the file to the parent function
    return user_file


"""
# define get_shp_directory() function - asks user to specify which directory within workspace contains shapefile
"""
def get_shp_directory(ws):
    # create empty dirs_list to hold all directories in project
    dirs_list = []
    
    # go through every file/dir that is within the workspace
    for file in os.listdir(ws):
        # set path to current file/dir
        path = os.path.join(ws, file)
        
        # try to split the path using a period in order to identify which ones have a file extension
        try_dir = path.split('.')
        
        # run this if file path was not split
        if len(try_dir) == 1:
            # make sure file is a directory
            if os.path.isdir(path) == True:
                # make sure directory doesn't end with an underscore
                if path[-1] != '_':
                    # add this path to dirs_list
                    dirs_list.append(path)
    
    # append workspace to dirs_list
    dirs_list.append(ws)
    
    # generate key values for each dir in dir_list to add to dirs dict
    nums = [str(i) for i in range(1, len(dirs_list)+1)]
    
    # create dictionary of keyed directory values
    dirs = dict(zip(nums, dirs_list))
    
    # display menu of possible directories
    print()
    for d in dirs:
        print(f'{d}: {dirs[d]}')
    print()
    
    # ask user to choose which directory their US states shapefile is in
    user_dir = input('Choose which directory your shapefile is in using its number: ')
    
    # validate that user_dir exists
    while user_dir not in dirs:
        # display an error, then pause program for half a second
        print('That is not a directory in your project.')
        time.sleep(0.5)
        
        # ask user again to choose which directory their US states shapefile is in
        user_dir = input('Choose which directory your shapefile is in using its number: ')
    
    # return directory to parent function
    return dirs[user_dir]


"""
# define get_shapefile() function - returns shapefile to be used by GeoPandas to map each state's Tweet counts
"""
def get_shapefile(ws):
    # get directory that contains US states shapefile
    user_dir = get_shp_directory(ws)
    
    # create empty shp_list to hold all shapefiles in user_dir
    shp_list = []
    
    # go through every file/dir that is within user_dir
    for file in os.listdir(user_dir):
        # set path to current file/dir
        path = os.path.join(user_dir, file)
        
        # append current file to shp_list if file has a .shp extension
        if file.split('.')[-1] == 'shp':
            shp_list.append(path)
    
    # validate that the directory contains shapefiles
    while len(shp_list) == 0:
        # tell user the directory they picked doesn't have any shapefiles,
        # then pause program for half a second
        print(f'{user_dir} has no shapefiles. Please choose a different directory.')
        time.sleep(0.5)
        
        # ask user for another directory
        user_dir = get_shp_directory(ws)
        
        # create empty shp_list to hold all shapefiles in user_dir
        shp_list = []
    
        # go through every file/dir that is within user_dir
        for file in os.listdir(user_dir):
            # set path to current file/dir
            path = os.path.join(user_dir, file)
        
            # append current file to shp_list if file has a .shp extension
            if file.split('.')[-1] == 'shp':
                shp_list.append(path)
    
    # generate key values for each shp in shp_list to add to dirs dict
    nums = [str(i) for i in range(1, len(shp_list)+1)]
    
    # create dictionary of keyed shapefile values
    shps = dict(zip(nums, shp_list))
    
    # display menu of shapefiles
    print()
    for s in shps:
        print(f'{s}: {shps[s]}')
    print()
    
    # ask user to choose which directory their US states shapefile is in
    user_shp = input('Choose your US states shapefile using its number: ')
    
    # validate that user_dir exists
    while user_shp not in shps:
        # display an error
        print(f'{user_shp} is not a shapefile.')
        
        # ask user again to choose which directory their US states shapefile is in
        user_shp = input('Choose your US states shapefile using its number: ')
    
    # return the shapefile and directory to the parent function
    return shps[user_shp], user_dir


"""
# define set_new_field() function - sets name of new field using the keyword and returns it
# to the parent function
"""
def set_new_field(keyword):
    # name if results were not filtered using a keyword
    if keyword == '':
        new_field = 'Tweet_Count'
    
    # name fi results were filtered using a keyword
    else:
        # split the keyword using a space
        words = keyword.split(' ')

        # name if results were filtered using a keyword
        if len(words) > 1:
            # name if keyword had more than 1 word
            new_field = '_'.join(words)   # join the separate words with a _ in between each word
            new_field = f'{new_field}_Tweet_Count'

        # name if the keyword only had one word    
        else:
            new_field = f'{keyword}_Tweet_Count'
    
    # return new field name value to parent function
    return new_field


"""
# define csv_interact() function - appends, writes, or reads contents of user's csv file
# optional parameters:
#   - mode         -> default to append
#   - checkKeyword -> default to False
"""
def csv_interact(data, file, workspace, mode='a', checkKeyword=False):
    # write to or append data to file using csv module
    if mode == 'a' or mode == 'w':
        # this code makes sure that a file in append mode will append the first line to a newline
        # it will only run if the csv file already exists
        # CREDIT: tdelaney from stack overflow
        # -> <https://stackoverflow.com/questions/64921222/csv-writer-adds-the-first-line-to-the-last-cell>
        if mode == 'a' and os.path.exists(file):
            with open(file, 'a+b') as f:
                f.seek(-1, 2)
                
                if f.read(1) != b"\n":
                    f.write(b"\r\n")
        
        # write data to the file, separating each field value with a comma
        with open(file, mode=mode, newline='') as csv_write:
            csvwriter = csv.writer(csv_write, delimiter=',')
            csvwriter.writerow(data)

        # return to the parent function
        return
    
    # read contents of csv file using pandas module
    else:
        # initialize states and ids lists to store states and Tweet IDs from csv file
        states = []
        ids = []
        
        # extract contents of csv file
        contents = pd.read_csv(file, header=0)
        
        # get fields from contents
        fields = [f for f in contents]
        
        # display menu of fields that were found in csv file
        print()
        for i, field in enumerate(fields, start=1):
            print(f'{i}. {field}')
        print()
        
        # ask user to enter the state and tweet id fields from the menu
        state_field = input('Enter the field that contains names of states: ')
        
        # validate that the state field is in the fields list
        while state_field not in fields:
            print(f'{state_field} does not exist.')
            
            # ask user to enter the state field again
            state_field = input('Enter the field that contains names of states: ')
        
        # ask user to enter the tweet id field from the menu
        id_field = input('Enter the field that contains Tweet IDs: ')
        
        # validate that the id field is in the fields list
        while id_field not in fields or id_field == state_field:
            # tell user that the field is not in the fields list
            if id_field not in fields:
                print(f'{id_field} does not exist.')
            
            # tell user that their id field is the same as their states field
            elif id_field == state_field:
                print(f'{id_field} is the same as your states field.')
            
            # tell user to enter the id field again
            id_field = input('Enter the field that contains Tweet IDs: ')
        
        # intialize state_data and id_data lists to store values of state_field and id_field
        state_data = []
        id_data = []
        
        # run keyword filtering related code if function parameter indicates to do so
        if checkKeyword == True:
            # ask user if they'd like to only map tweets that have a certain keyword
            if_keyword = input('Would you like to import Tweets that have a certain keyword? (Y or N) ')
        
            # validate that input is Yes/Y or No/N
            while if_keyword.title() != 'Yes' and if_keyword.upper() != 'Y' and if_keyword.title() != 'No' and if_keyword.upper() != 'N':
                # display error if input isn't Yes/Y or No/N
                print(f'{if_keyword} is not a valid answer. Please try again.')
            
                # ask user again
                if_keyword = input('Would you like to import Tweets that have a certain keyword? (Y or N) ')
        
            # run this code if the user wants to only include Tweets with a certain keyword from the csv file
            if if_keyword.title() == 'Yes' or if_keyword.upper() == 'Y':
                # initialize empty list of unique keywords from csv file
                keywords = []
            
                # ask user to identify the keywords field from the menu
                keyword_field = input('Enter the field that contains keywords: ')
            
                # validate that field is in fields list
                while keyword_field not in fields or keyword_field == state_field or keyword_field == id_field:
                    # display that the keyword field is the same as the state field, then pause program for half a second
                    if keyword_field == state_field:
                        print(f'{keyword_field} is the same as your state field.')
                        time.sleep(0.5)
                    
                    # display that the keyword field is the same as the id field, then pause program for half a second
                    elif keyword_field == id_field:
                        print(f'{keyword_field} is the same as your id field.')
                        time.sleep(0.5)
                    
                    # display that the field does not exist, then pause program for half a second
                    else:
                        print(f'{keyword_field} field does not exist.')
                        time.sleep(0.5)
            
                    # ask user again for keyword field
                    keyword_field = input('Enter the field that contains keywords: ')
            
                # initialize list to store keyword values object containing values from keyword_field
                keyword_data = []
            
                # add data values/object of keyword_field to keyword_data list
                keyword_data.append(contents[keyword_field])
            
                # iterate through each keyword result object and add unique values to keyword list
                for ob in keyword_data:
                    for word in ob:
                        # add keyword to keywords list if it isn't already in it
                        if word not in keywords:
                            keywords.append(word)
            
                # handle empty csv files
                if len(keywords) == 0:
                    print('No keywords were found.')
                    
                    # return empty states, ids, and user_keywords lists to parent function
                    return [], [], []
                
                # run this code if data is in the csv file
                else:
                    # display menu of fields that were found in csv file
                    print()
                    print('Available Keywords')
                    print('------------------')
                    for i, keyword in enumerate(keywords, start=1):
                        print(f'{i}. {keyword}')
                    print()

                    time.sleep(1)   # pause program for a second

                    # determine how many keywords are available
                    total_keywords = len(keywords)

                    # initialize user_keywords list to store keywords user wants to pull data for
                    user_keywords = []

                    # initialize valid_number bool to False to use in below validation loop
                    valid_number = False

                    # validate the input is an integer and smaller than the total number of available keywords
                    while valid_number == False:
                        # ask user how many keywords they want to pull data for
                        num_keywords = input('How many keywords would you like to pull data for? ')

                        # tell user if input is not an integer
                        if not num_keywords.isdigit():
                            print(f'{num_keywords} is not an integer.')
                            
                            time.sleep(0.5)     # pause program for half a second

                        # tell user if input is larger than total number of available keywords
                        elif int(num_keywords) > total_keywords:
                            print(f'{num_keywords} is larger than the amount of available keywords: {total_keywords}.')
                            
                            time.sleep(0.5)     # pause program for half a second

                        # tell user if input equals the total number of available keywords
                        elif int(num_keywords) == total_keywords:
                            print(f'{num_keywords} is the same as the total number of available keywords: {total_keywords}.')
                            
                            time.sleep(0.5)     # pause program for half a second

                        # tell user if input is equal to 0
                        elif int(num_keywords) == 0:
                            print(f'You need to use at least 1 keyword.')
                            
                            time.sleep(0.5)     # pause program for half a second

                        # the input passed both validation tests
                        else:
                            # convert valid input to integer
                            num_keywords = int(num_keywords)

                            # signal that a valid input has been entered
                            valid_number = True

                    # new line
                    print()

                    # initialize counter
                    counter = 0

                    # get data for as many keywords as user wants
                    while counter < num_keywords:
                        # ask user to enter an available keyword from the menu
                        user_keyword = input(f'Enter keyword #{counter+1} from the menu: ')

                        # validate that the keyword is an option
                        while user_keyword not in keywords or user_keyword in user_keywords:
                            # tell user if keyword is not in keywords list
                            if user_keyword not in keywords:
                                print(f'{user_keyword} is not an option. Please try again')

                                time.sleep(0.5)     # pause program for half a second

                            # tell user if data for keyword has already been pulled
                            else:
                                print(f'Data for {user_keyword} has already been pulled.')

                                time.sleep(0.5)     # pause program for half a second

                            # new line
                            print()

                            # ask user again to enter an available keyword from the menu
                            user_keyword = input(f'Enter keyword #{counter+1} from the menu: ')

                        # new line
                        print()
                        
                        # add keyword to user_keywords list
                        user_keywords.append(user_keyword)

                        # filter contents using user specified keyword
                        keyword_contents = contents[contents[keyword_field] == user_keyword]

                        # get number of results pulled
                        num_results = len(keyword_contents)

                        # display results
                        if num_keywords > 1:
                            print(f'\nPulling data for {user_keyword} returned {num_results} results.\n')
                        
                        time.sleep(1)   # pause program for a second
                        print(f'Results For - {user_keyword}:\n{keyword_contents}\n')

                        # add data values/object of state_field and id_field (after keyword filtering) to respective list
                        state_data.append(keyword_contents[state_field])
                        id_data.append(keyword_contents[id_field])

                        # add 1 to the counter
                        counter += 1
            
            # run this code if user indicated that they do not want to filter csv data using a keyword
            else:
                # add data values/object of state_field and id_field (without keyword filtering) to respective list
                state_data.append(contents[state_field])
                id_data.append(contents[id_field])

                # set user keyword to an empty list
                user_keywords = []
        
        # run this code if function parameters indicate to not filter by keyword
        else:
            # add data values/object of state_field and id_field (without keyword filtering) to respective list
            state_data.append(contents[state_field])
            id_data.append(contents[id_field])

            # set user keyword to an empty list
            user_keywords = []
            
        # iterate through each state result object and add the state value to the states list
        for ob in state_data:
            for state in ob:
                states.append(state)
            
        # iterate through each id result object and add the id value to the ids list
        for ob in id_data:
            for tweet in ob:
                ids.append(tweet)
        
        # return states, ids, and user_keyword to parent function
        return states, ids, user_keywords


"""
# define get_field_indexes_tweet_ids() function - determines the location of each relevant field using the user's input
# also generates a list of Tweet IDs that are in the csv file to make sure duplicate Tweets aren't being added to the file
# returns the list of Tweet IDs and the indexes of the state, tweet_id, and keyword fields
"""
def get_field_indexes_tweet_ids(contents):
    # get fields from csv file
    fields = [f for f in contents]

    # display menu of fields that were found in csv file
    print()
    for i, field in enumerate(fields, start=1):
        print(f'{i}. {field}')
    print()
    
    # ask user to enter field that has states
    state_field = input('Enter the field that contains names of states: ')
    
    # validate that specified state field is in fields list
    while state_field not in fields:
        # tell user that state field isn't in the fields list
        print(f'{state_field} does not exist.')

        # tell user to enter the states field again
        state_field = input('Enter the field that contains the names of states: ')
    
    # ask user to enter field that has Tweet IDs
    id_field = input('Enter the field that contains Tweet IDs: ')
    
    # validate that specified ids field is in fields list and is not the same as states field
    while id_field not in fields or id_field == state_field:
        # tell user if field does not exist
        if id_field not in fields:
            print(f'{id_field} does not exist.')
        
        # tell user if field is the same as state field
        if id_field == state_field:
            print(f'That is the same as {state_field}.')
        
        # tell user to enter the ids field again
        id_field = input('Enter the field that contains Tweet IDs: ')
    
    # ask user to enter field that contains keywords
    keyword_field = input('Enter the field that contains keywords: ')
    
    # validate that specified keywords field is in fields list and is not the same as states or ids fields
    while keyword_field not in fields or keyword_field == state_field or keyword_field == id_field:
        # tell user if field does not exist
        if keyword_field not in fields:
            print(f'{keyword_field} does not exist.')
        
        # tell user if field is the same as state field
        if keyword_field == state_field:
            print(f'That is the same as {state_field}.')
        
        # tell user if field is the same as id field
        if keyword_field == id_field:
            print(f'That is the same as {id_field}.')
        
        # tell user to enter the ids field again
        keyword_field = input('Enter the field that contains keywords: ')
    
    # get list of tweet ids from csv file using user id_field
    tweets = contents[id_field].tolist()
    
    # determine indexes of each of the specified fields in the fields list
    state_index = fields.index(state_field)
    id_index = fields.index(id_field)
    keyword_index = fields.index(keyword_field)
    
    # return Tweet IDs list and indexes to parent function
    return tweets, state_index, id_index, keyword_index