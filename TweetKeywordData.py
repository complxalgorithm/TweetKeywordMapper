"""

@Name: TweetKeywordData.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Contains most functions that are imperative to running the program. This includes
              the algorithm used to determine the state of origin of each Tweet result, 
              as well as the csv_interact() and TweetKeywordSearch() functions.
@Requirements: tweepy, pandas, geopy

"""
# import libraries
import pandas as pd
import csv
import os
import time
import TweetKeywordConstants as cons
##from geopy.geocoders import Nominatim
##from sys import platform
##import random

"""
# define set_path_to_file() function - 
def set_path_to_file(ws, file):
    # set path depending on operating system
    if platform == 'win32':
        path_to_file = ws + '\\' + file
    else:
        path_to_file = ws + '/' + file
    
    # return path to file to parent function
    return path_to_file
"""


# define where_data() function - 
def where_data():
    # create options dict to display
    options = {'1': 'Search Twitter', '2': 'Import from CSV'}
    
    # display menu of options
    for o in options:
        print(f'{o}: {options[o]}')
    
    # ask where user would like to get data from
    where = input('Choose how you would like to get Tweet count data using the option\'s number: ')
    
    # validate input
    while where not in options:
        # display an error
        print('That is not a valid option. Please try again.')
        
        # ask where user would like to get data from
        where = input('Choose how you would like to get Tweet count data using the option\'s number: ')
    
    # return key value to main() function
    return where


# define ifWrite() function - allow user to signal whether or not they want to write search results
# to a csv file
def ifWrite():
    # ask user for input
    answer = input('Would you like to write Tweet ID and State data to a CSV file? (Y or N): ')
    
    # validate input
    while answer.capitalize() != 'Yes' and answer.upper() != 'Y' and answer.capitalize() != 'No' and answer.upper() != 'N':
        # display error
        print(f'{answer} is not valid. Please try again.')
        
        # ask user for input again
        answer = input('Would you like to write Tweet ID and State data to a CSV file? (Y or N): ')
    
    # return answer to main() function
    return answer


# define get_states_from_results() function - uses search results to populate places list with
# full name of the state that each of the tweets with geolocation info was tweeted from
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
        
        # get status data using the tweet id
        # get user data using the screen name
        try:
            stat = api.get_status(tweet_id)
            user = api.get_user(screen_name=f'{screen_name}')
        except Exception:
            place = ''
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
                print(count)
        
            # break from the loop once the user-inputted results number is reached
            if count == num:
                break
    
    # return places list to main() function
    return places, tweet_ids


# define get_state() function - extracts the state from each tweet using either the Status or User model
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
            
            # split the name using a comma as the delimiter and store words in list
            try_split = place.split(', ')
            
            # iterate through each element and attempt to get that from the states dict
            for wrd in try_split:
                if wrd in states:
                    return states[wrd]
                elif wrd in states.values():
                    return wrd
            
            # if pl value hasn't been returned and is not blank, set pl to the original place value
            # if it is blank then return an empty string
            if place != '':
                pl = place
                print(f'Place: {pl}\n')
            else:
                return ''
            
    # run this if there is no place object, but the user allows twitter to access their location
    elif (s.place is None) and (u.geo_enabled == True):
        # get the location that the user has on their profile,
        # then split the value using the comma as the delimiter, and store all words
        place = u.location
        try_split = place.split(', ')
        
        # iterate through each word in resulting list
        for wrd in try_split:
            # check to see if each word is in the states dict as a key or value
            # if it is, return the respective value
            if wrd in states:
                # if a key in states dict, return respective value
                return states[wrd]
        
            # if a value in states dict, return try_split value
            elif wrd in states.values():
                return wrd
        
        # if pl value hasn't been returned and is not blank, set pl to the original place value
        # if it is blank then return an empty string
        if place != '':
            pl = place
            print(f'Place: {pl}\n')
        else:
            return ''
            
    # if none of these situations are the case for the tweet, return an empty string
    else:
        return ''
    
    """
    # if the pl value has not been returned to its parent function, then there are other situations
    # that will need to be handled. it will first be compared to the below cities dict. if it is not
    # within the cities dict as a key, then the program will attempt to split the pl value using a
    # space, a / symbol, a | symbol, or a • symbol as a delimiter. it will then iterate through each
    # resulting word of each delimited string and compare them to many different string alterations involving
    # the pl value (e.g., pl.upper(), pl.title(), etc.). if these all fail, it will return an empty string.
    """
    
    # return its respective value in the cities dict if it shows up as a key
    if pl in cities:
        return cities[pl]
    
    # return value if its titled version shows up as a key in cities dict
    elif pl.title() in cities:
        return cities[pl.title()]
    
    # return titled version of value if it shows up as a value in states dict
    elif pl.title() in states.values():
        return pl.title()
    
    # run this code if pl value is not a key/value in states dict, nor is it in cities dict
    elif (pl not in states) and (pl not in states.values()):
        # split pl value by four different delimiters: a space, a /, a |, and a •
        elements_space = pl.split(' ')
        elements_slash = pl.split('/')
        elements_bar = pl.split('|')
        elements_dot = pl.split('•')
        
        # display the results of splitting the string
        print(f'Split by Space: {elements_space}')
        print(f'Split by /: {elements_slash}')
        print(f'Split by |: {elements_bar}')
        print(f'Split by Dot: {elements_dot}\n')
        
        """
        # check the length of each resulting list.
        # if any of them have more than 1 element, iterate through multiple tests and return the state
        # if any of the elements (using string methods) are in the states dictionary or cities dictionary.
        # return an empty string if the place value doesn't pass any of these tests.
        """
        # split by space
        if len(elements_space) > 1:
            for wrd in elements_space:
                if wrd in states: # not upper(), since 2-letter words between spaces are typically words (e.g., me, in)
                    return states[wrd]
                elif wrd in states.values():
                    return wrd
                elif wrd.capitalize() in states.values():
                    return wrd.capitalize()
                elif wrd.title() in states.values():
                    return wrd.title()
                elif wrd in cities:
                    return cities[wrd]
                elif wrd.title() in cities:
                    return cities[wrd.title()]
                elif wrd.upper() in cities:
                    return cities[wrd.upper()]
            
            # return empty string if state value hasn't been returned
            return ''
        
        # split by /
        elif len(elements_slash) > 1:
            for wrd in elements_slash:
                if wrd.upper() in states:
                    return states[wrd.upper()]
                elif wrd in states.values():
                    return wrd
                elif wrd.capitalize() in states.values():
                    return wrd.capitalize()
                elif wrd.title() in states.values():
                    return wrd.title()
                elif wrd in cities:
                    return cities[wrd]
                elif wrd.title() in cities:
                    return cities[wrd.title()]
                elif wrd.upper() in cities:
                    return cities[wrd.upper()]
            
            # return empty string if state value hasn't been returned
            return ''
        
        # split by |
        elif len(elements_bar) > 1:
            for wrd in elements_bar:
                if wrd.upper() in states:
                    return states[wrd.upper()]
                elif wrd in states.values():
                    return wrd
                elif wrd.capitalize() in states.values():
                    return wrd.capitalize()
                elif wrd.title() in states.values():
                    return wrd.title()
                elif wrd in cities:
                    return cities[wrd]
                elif wrd.title() in cities:
                    return cities[wrd.title()]
                elif wrd.upper() in cities:
                    return cities[wrd.upper()]
            
            # return empty string if state value hasn't been returned
            return ''
        
        # split by •
        elif len(elements_dot) > 1:
            for wrd in elements_dot:
                if wrd.upper() in states:
                    return states[wrd.upper()]
                elif wrd in states.values():
                    return wrd
                elif wrd.capitalize() in states.values():
                    return wrd.capitalize()
                elif wrd.title() in states.values():
                    return wrd.title()
                elif wrd in cities:
                    return cities[wrd]
                elif wrd.title() in cities:
                    return cities[wrd.title()]
                elif wrd.upper() in cities:
                    return cities[wrd.upper()]
            
            # return empty string if state value hasn't been returned
            return ''
        
        # return an empty string after going through each element
        else:
            return ''
                
    # return an empty string when all other checks fail
    else:
        return ''

    
# define get_state_counts() function - uses places list to count total number of tweets from
# each state in the search results
def get_state_counts(places, states):
    # initialize counts dictionary
    counts = {}
    
    # iterate over the keys in states dict
    for key in states:
        # initialize counter to 0
        count = 0
        
        # go through each value in places list
        for p in places:
            # if the place is equal to the current states dict value, add 1 to the counter
            if p == states[key]:
                count += 1
        
        # add current state key and its count as the next key/value combo in counts dict
        counts[key] = count
    
    # return counts dict to main() function
    return counts


# define get_user_csv_file() function - get a csv file from the user
def get_user_csv_file(default):
    # ask user to enter their file, or use the default csv file
    user_file = input('Enter csv file from your current directory, or hit enter to use default file: ') or default
    
    # automatically return value if the input is the same as the default csv file
    if user_file == default:
        return user_file
    
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


# define csv_interact() function - 
# optional parameters:
#   - mode         -> default to append
#   - checkKeyword -> default to False
def csv_interact(data, file, workspace, mode='a', checkKeyword=False):
    # write to or append data to file using csv module
    if mode == 'a' or mode == 'w':
        # this code makes sure that a file in append mode will append the first line to a newline
        # CREDIT: tdelaney from stack overflow
        # -> <https://stackoverflow.com/questions/64921222/csv-writer-adds-the-first-line-to-the-last-cell>
        if mode == 'a':
            with open(file, 'a+b') as f:
                f.seek(-1, 2)
                
                if f.read(1) != b"\n":
                    f.write(b"\r\n")
        
        # write data to the file, separating each field value with a comma
        with open(file, mode=mode, newline='') as csv_write:
            csvwriter = csv.writer(csv_write, delimiter=',')
            csvwriter.writerow(data)

        #
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
        
        # tell user to enter the state and tweet id fields from the menu
        state_field = input('Enter the field that contains names of states: ')
        id_field = input('Enter the field that contains Tweet IDs: ')
        
        # validate that both fields are in fields list
        while state_field not in fields or id_field not in fields:
            # display an error, then pause program for half a second
            print('One of those fields does not exist. Please try again.')
            time.sleep(0.5)
            
            # tell user to enter the fields again
            state_field = input('Enter the field that contains the names of states: ')
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
                keyword_field = input('Enter the field that contains keywords from menu: ')
            
                # validate that field is in fields list
                while keyword_field not in fields or keyword_field == state_field or keyword_field == id_field:
                    if keyword_field == state_field:
                        # display that the keyword field is the same as the state field, then pause program for half a second
                        print('That is the same as your state field. Please try again.')
                        time.sleep(0.5)
                    elif keyword_field == id_field:
                        # display that the keyword field is the same as the id field, then pause program for half a second
                        print('That is the same as your id field. Please try again.')
                    else:
                        # display that the field does not exist, then pause program for half a second
                        print('That field does not exist. Please try again.')
                        time.sleep(0.5)
            
                    # ask user again for keyword field
                    keyword_field = input('Enter the field that contains keywords from menu: ')
            
                # initialize list to store keyword values object containing values from keyword_field
                keyword_data = []
            
                # add data values/object of keyword_field to keyword_data list
                keyword_data.append(contents[keyword_field])
            
                # iterate through each keyword result object and add unique values to keyword list
                for ob in keyword_data:
                    for word in ob:
                        if word not in keywords:
                            keywords.append(word)
            
                # display menu of fields that were found in csv file
                print()
                for i, keyword in enumerate(keywords, start=1):
                    print(f'{i}. {keyword}')
                print()
            
                # ask user to enter an available keyword from the menu
                user_keyword = input('Enter a keyword from the menu: ')
            
                # validate that the keyword is an option
                while user_keyword not in keywords:
                    # display error
                    print(f'{user_keyword} is not an option. Please try again')
                
                    # ask user again to enter an available keyword from the menu
                    user_keyword = input('Enter a keyword from the menu: ')
            
                # filter contents using user specified keyword
                keyword_contents = contents[contents[keyword_field] == user_keyword]
                print(f'Results For - {user_keyword}:\n{keyword_contents}')
            
                # add data values/object of state_field and id_field (after keyword filtering) to respective list
                state_data.append(keyword_contents[state_field])
                id_data.append(keyword_contents[id_field])
            
            # run this code if user indicated that they do not want to filter csv data using a keyword
            else:
                # add data values/object of state_field and id_field (without keyword filtering) to respective list
                state_data.append(contents[state_field])
                id_data.append(contents[id_field])

                #
                user_keyword = ''
        
        # run this code if function parameters indicates to not consider keyword
        else:
            # add data values/object of state_field and id_field (without keyword filtering) to respective list
            state_data.append(contents[state_field])
            id_data.append(contents[id_field])

            #
            user_keyword = ''
            
        # iterate through each state result object and add the state value to the states list
        for ob in state_data:
            for state in ob:
                states.append(state)
            
        # iterate through each id result object and add the id value to the ids list
        for ob in id_data:
            for tweet in ob:
                ids.append(tweet)
        
        # return states and ids to parent function
        return states, ids, user_keyword


# define TweetKeywordSearch() function - searches for Tweet result using a specified keyword and
# returns the found states, the Tweet IDs, state counts, and keyword used.
def TweetKeywordSearch(ws, default, states, cities):
    # import necessary Tweepy library and OAuthHandler
    import tweepy
    from tweepy import OAuthHandler

    # authorization to access Twitter API
    client = tweepy.Client(cons.bearer_token)
    consumer_key = cons.consumer_key
    consumer_secret = cons.consumer_secret
    access_token = cons.access_token
    access_secret = cons.access_secret

    # create OAuthHandler instance using relevant keys,
    # then set access token in order to access Twitter API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # create Tweepy API instance
    api = tweepy.API(auth)

    """
    # get data directly from a search using Twitter's API
    """
    
    # ask user to enter a keyword of interest
    keyword = input('Enter the keyword: ')

    # ask user how many results they would like
    num_res = int(input('How many results would you like to get? '))

    # create a search query using user keyword
    query = keyword + ' -filter:retweets lang:en' # exclude retweets and only include english tweets

    # get 100 search results using query
    search_results = tweepy.Cursor(api.search_tweets, q=query, count=100).items()
            
    # get lists of places and tweet ids that tweets in search results came from
    places, ids = get_states_ids_from_results(search_results, api, states, cities, num_res)
            
    # get dictionary of counts for each state
    state_counts = get_state_counts(places, states)
        
    # get number of tweets that were returned
    num_results = len(ids)
        
    # only ask user if they want to write to a csv if there were search results for keyword
    if num_results == 0:
        # display there were no search results returned
        print(f'Searching for {keyword} returned no results.')
    else:
        # display number of search results returned
        print(f'Searching for {keyword} returned {num_results} results\n.')
            
        # ask user if they want to write results to default csv file
        if_write = ifWrite()
            
        # run this if user signaled that they want to write results to csv file
        if if_write.capitalize() == 'Yes' or if_write.upper() == 'Y':
            # get csv file to write to from user
            user_file = get_user_csv_file(default)
            
            # create tweet_data dict using ids and places lists
            tweet_data = dict(zip(ids, places))
            
            # read contents of user_file for use in making sure duplicate Tweets aren't written to the file
            # reading a file necessitates setting 2 variables; if it didn't, then this would just be ids
            locations, tweets, word = csv_interact((), user_file, ws, mode='r')
            
            # iterate through tweet_data dict to write each tweet to the csv file
            for tweet_id in tweet_data:
                # append Tweet data to file if the Tweet ID is not already in the file
                if tweet_id not in tweets:
                    # create data set for each tweet
                    data = (tweet_id, keyword, tweet_data[tweet_id])
        
                    # append this data to default csv file
                    csv_interact(data, user_file, ws)
                
                    # tell user data was successfully written to csv file
                    print(f'{data} was added to {user_file}')
                # inform user when data for a Tweet is already within the csv file
                else:
                    print(f'Data for {tweet_id} is already in {user_file}.')
    
    # return ids, places, and state_counts results
    return places, ids, state_counts, keyword
