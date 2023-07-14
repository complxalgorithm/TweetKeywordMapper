"""

@Name: extract_place.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: State extraction algorithm used to determine US state of origin of Tweets that were pulled
              by Tweepy search cursor.
@Requirements: numpy, geopy

"""


# import modules
from geopy.geocoders import Nominatim
import numpy as np
import re
import time


"""
# define get_states_from_results() function - uses search results to populate places list with
# full name of the state that each of the tweets with geolocation info was tweeted from
"""
def get_states_ids_from_results(results, api, states, cities, areas, num):
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
        
        # display Tweet ID
        print(f'Tweet ID: {tweet_id}\n')
        
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
            place = get_state(stat, user, states, cities, areas)

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
def get_state(s, u, states, cities, areas):
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
        
        # if pl value hasn't been returned and is not blank or a space, set pl to the original place value
        # if it is blank then return an empty string
        if place == '' or place == ' ':
            return ''
        
        else:
            pl = place
            
    # if none of these situations are the case for the tweet, return an empty string
    else:
        return ''
    
    """
    # when the found place has a value, try to extract the state from the value
    # depending on the type
    """
    
    # remove dash from value in the event that it is a set of coordinates in the western hemisphere or south of the equator
    temp_pl = re.sub('\-', '', pl)
    
    # create list of elements using this temp value
    if len(temp_pl.split(', ')) > 1:
        elements = temp_pl.split(', ')
    
    elif len(temp_pl.split(',')) > 1:
        elements = temp_pl.split(',')
    
    elif len(temp_pl.split(' ')) > 1:
        elements = temp_pl.split(' ')
    
    else:
        elements = []
    
    # depending on what the place value is, try to determine state of origin
    if (pl.find('ÜT: ') != -1 or pl.find('°') != -1) or (len(elements) == 2 and ('.' in elements[0] and elements[0].replace('.', '').isnumeric()) and ('.' in elements[1] and elements[1].replace('.', '').isnumeric())):
        return determine_state_from_coordinates(pl, states)
    
    elif pl.find('via') != -1 or pl.find('from') != -1:
        return find_state_in_place_value(pl, states, cities, areas, word='via')
    
    else: 
        return find_state_in_place_value(pl, states, cities, areas)


"""
# define determine_state_from_coordinates() function - will use potential coordinates from place value
# to determine state of origin
"""
def determine_state_from_coordinates(pl, states):
    # intialize Nominatim API
    geolocator = Nominatim(user_agent='Tweet Keyword Mapper')
    
    # run this if ÜT is not in place value
    if pl.find('ÜT: ') != -1:
        # remove ÜT from place value
        pl = re.sub('\ÜT: ', '', pl)
        
        # get x,y coordinates from place value
        elements = pl.split(',')
    
    # run this in every other situation
    else:
        # try splitting value by a comma space
        if (len(pl.split(', '))) > 1:
            elements = pl.split(', ')
        
        # try splitting value by a comma
        elif (len(pl.split(','))) > 1:
            elements = pl.split(',')

        # try splitting value by a space
        elif (len(pl.split(' '))) > 1:
            elements = pl.split(' ')

        # return empty string if all fails
        else:
            return ''
        
    # create coordinates string
    coordinates = ' , '.join(elements)
    
    print(coordinates)

    # get location using coordinates
    location = geolocator.reverse(coordinates)

    # get city, state, country address from location
    address = location.raw['address']

    # when an address can't be determined, return an empty string
    if address is None:
        print('Could not use coordinates provided in {pl}\n')

        return ''

    # use the address values to try to determine state
    else:
        # get state from the address when it comes from the United States,
        # then return the state
        if address['country'] == 'United States':
            state = address['state']

            print(f'State Found from Coordinates: {state}\n')

            return state

        # return empty string when tweet came from a different country
        else:
            print('Not from the United States.')

            return ''


"""
# define search_for_state() function - looks for instance of a state abbreviation or name of a city
# within the place value and returns an object if an instance is found
# CREDIT: Hugh Bothwell -> https://stackoverflow.com/questions/5319922/check-if-a-word-is-in-a-string-in-python
"""
def search_for_state_city(p):
    return re.compile(r'\b({0})\b'.format(p), flags=re.IGNORECASE).search


"""
# define find_state_in_place_value() function - searches for any mention of a state or city and returns the state value
# that is most likely to be the state of origin of the Tweet
"""
def find_state_in_place_value(place, states, cities, areas, word=''):
    # initialize num_found_states variable to keep track of how many states could be pulled
    # from the place value
    num_found_states = 0
    
    # initialize found_states_indexes dictionary to store found states and where
    # they are located within the place value string
    found_states_indexes = {}
    
    # strip place value of certain characters: '?', '.', '!', ';', and ':'
    place = re.sub('\?|\.|\!|\;|\:', '', place)
    
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
                    print(f'City Found: {c} => {cities[c]}')
                    
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
                            print(f'A state has already been found at index {place.title().index(c)}.')
                    
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
                    print(f'City Found: {c} => {cities[c]}')
                    
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
                            print(f'A state has already been found at index {place.title().index(c)}.')
                    
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
        # handle Washington, DC situations separately
        if s == 'DC' and search_for_state_city(s)(place.upper()) is None:
            # attempt to find the index of a mention of the District of Columbia in place value
            try:
                place.upper().index(states[s].upper())

            # move on if nothing was found
            except ValueError:
                pass

            # the index/location of a mention of DC was found in the place value
            else:
                # display the state name that was found
                print(f'State Found: {states[s]}')

                # only add to found states counter if it isn't in the found_states_indexes dictionary
                # add the state and its index within the place value to the found_states_indexes dictionary
                # if the index is not already in the dictionary
                if (states[s] not in found_states_indexes) and (place.upper().index(states[s].upper()) not in found_states_indexes.values()):
                    num_found_states += 1

                    found_states_indexes[states[s]] = place.upper().index(states[s].upper())

                elif (states[s] not in found_states_indexes) and (place.upper().index(states[s].upper()) in found_states_indexes.values()):
                    print(f'A state has already been found at index {place.upper().index(states[s].upper())}.')

                else:
                    print(f'{states[s]} has already been found.')
        
        # run this code if a state mention is within the place value
        elif (search_for_state_city(s)(place.upper()) is not None) or (search_for_state_city(states[s])(place.title()) is not None):
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
                        # add the state and its index within the place value to the found_states_indexes dictionary
                        # if the index is not already in the dictionary
                        if (states[s] not in found_states_indexes) and (place.upper().index(s) not in found_states_indexes.values()):
                            num_found_states += 1
                            
                            found_states_indexes[states[s]] = place.upper().index(s)
                        
                        elif (states[s] not in found_states_indexes) and (place.upper().index(s) in found_states_indexes.values()):
                            print(f'A state has already been found at index {place.upper().index(s)}.')

                        else:
                            print(f'{states[s]} has already been found.')

                    # run if the result is not a common word
                    else:
                        # had to add this because I was getting the location of the foreign place that had 'Ca' in the name
                        # and was preceded by 'Au'
                        if (search_for_state_city('AU')(place.upper()) is None) and (result.group(1) not in ('in', 'In', 'me', 'Me', 'de', 'la', 'La', 'or', 'Or', 'Mt', 'Co', 'co', 'oh', 'Oh')):
                            # only add to found states counter if it isn't in the found_states_indexes dictionary
                            # add the state and its index within the place value to the found_states_indexes dictionary
                            # if the index is not already in the dictionary
                            if (states[s] not in found_states_indexes) and (place.upper().index(s) not in found_states_indexes.values()):
                                num_found_states += 1
                                
                                found_states_indexes[states[s]] = place.upper().index(s)
                            
                            elif (states[s] not in found_states_indexes) and (place.upper().index(s) in found_states_indexes.values()):
                                print(f'A state has already been found at index {place.upper().index(s)}.')
                            
                            else:
                                print(f'{states[s]} has already been found.')

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
                    # add the state and its index within the place value to the found_states_indexes dictionary
                    # if the index is not already in the dictionary
                    if (states[s] not in found_states_indexes) and (place.title().index(states[s]) not in found_states_indexes.values()):
                        # set the resulting search object to result variable
                        result = search_for_state_city(states[s])(place)
                        
                        # handle situation where Washington State is being added to found states when
                        # the place value is equal to Washington, D.C.
                        if (place.upper().find('WASHINGTON, DC') != -1 or (place.upper().find('WASHINGTON, DC') != -1) or place.upper().find('WASHINGTON, DISTRICT OF COLUMBIA') != -1) and (result.group(1) in ('Washington', 'washington')):
                            print('Washington refers to DC, not the separate state.')
                        
                        # handle situation where Virginia is being returned in cases where full West Virginia name is in place value
                        elif (place.upper().find('WEST VIRGINIA') != -1) and (result.group(1) in ('Virginia', 'virginia')):
                            print('Virginia is not referring to the separate state, but is part of West Virginia.')
                        
                        else:
                            num_found_states += 1
                            
                            found_states_indexes[states[s]] = place.title().index(states[s])

                    elif (states[s] not in found_states_indexes) and (place.title().index(states[s]) in found_states_indexes.values()):
                        print(f'A state has already been found at index {place.title().index(states[s])}.')

                    else:
                        print(f'{states[s]} has already been found.')

            # move on if a state abbreviation or name could not be found
            else:
                pass
        
        # move on if a state abbreviation or name could not be found
        else:
            pass
    
    # iterate through each area code in area_codes dictionary
    for code in areas:
        # run this if an area code was found in place value
        if search_for_state_city(code)(place) is not None:
            # display the area code that was found
            print(f'Area Code: {code} => {areas[code]}')
            
            # attempt to get index within place value of found area code
            try:
                place.index(code)
            
            # move on if an error occurred
            except ValueError:
                pass
            
            # an index was found successfully
            else:
                # account for full street addresses with house numbers
                if (place.upper().find('STREET') == -1) and (place.upper().find('DR') == -1) and (place.upper().find('DRIVE') == -1) and (place.upper().find('RD') == -1) and (place.upper().find('ROAD') == -1) and (place.upper().find('BLVD') == -1) and (place.upper().find('BOULEVARD') == -1):
                    # only add to found states counter if state isn't already in the found_states_indexes dictionary
                    # add the state and its index within the place value to the found_states_indexes dictionary
                    # if the index is not already in the dictionary
                    if (areas[code] not in found_states_indexes) and (place.index(code) not in found_states_indexes.values()):
                        num_found_states += 1

                        found_states_indexes[areas[code]] = place.index(code)

                    elif (areas[code] not in found_states_indexes) and (place.index(code) in found_states_indexes.values()):
                        print(f'A state has already been found at index {place.index(code)}.')

                    else:
                        print(f'{areas[code]} has already been found.')
                
                # tell user when the code is probably a house number in a full street address
                else:
                    print(f'{code} is probably the house number in an address.')
        
        # move on if area code could not be found in place value
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
    
    # run this if at least one state was extracted from Tweet
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