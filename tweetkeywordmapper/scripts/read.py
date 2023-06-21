"""

@Name: read.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Imports Tweet data from CSV file
@Requirements: Python3

"""

# import module
import time

try:
    from tweetkeywordmapper.core import TweetKeywordData as data
except:
    from core import TweetKeywordData as data


"""
# define TweetKeywordImport() function - read Tweet data from a CSV file and return
# lists of states and Tweet IDS, state_counts dictionary, keyword, and number of results
"""
def TweetKeywordImport(ws, default, states):
    # ask user for file, and use default file if input is left blank
    user_file = data.get_user_csv_file(default)

    # extract states, tweet ids, and filtered keywords from csv file
    places, ids, keywords = data.csv_interact([], user_file, ws, mode='r', checkKeyword=True)

    # get Tweet counts for each state using data
    state_counts = data.get_state_counts(places, states)

    # get number of tweets that were returned
    num_results = len(ids)
        
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
    
    # return places & tweet ids lists, state_counts dictionary, keyword, and num_results to parent function
    return places, ids, state_counts, keyword, num_results