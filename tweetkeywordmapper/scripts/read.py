"""

@Name: read.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Imports Tweet data from CSV/Excel file
@Requirements: Python3

"""

# import module
import time

try:
    from tweetkeywordmapper.core import data
    from tweetkeywordmapper.core import stats
except:
    from core import data
    from core import stats


"""
# define TweetKeywordRead() function - read Tweet data from a CSV/Excel file and return
# lists of states and Tweet IDS, state_counts dictionary, keyword, and number of results
"""
def TweetKeywordRead(ws, default_file, states):
    # ask user for file, and use default file if input is left blank
    user_file, file_type = data.get_user_file(default_file)
    
    # extract states, tweet ids, and filtered keywords from file
    places, ids, keywords = data.file_interact([], user_file, file_type, ws, mode='r', checkKeyword=True, function='')

    # get Tweet counts for each state using data
    state_counts = stats.get_counts(places, states=states)

    # get number of tweets that were returned
    num_results = len(ids)
        
    # set keyword value using keywords list
    keyword = ' '.join(keywords)
    
    # display how many search results were returned
    if num_results == 0:
        print(f'Reading from {user_file} returned no results.\n')
        
        time.sleep(1) # pause program for a second

    # display results if any were found
    else:
        print(f'Reading from {user_file} returned {num_results} results.\n')

        time.sleep(1) # pause program for a second
    
    # return places & tweet ids lists, state_counts dictionary, keyword, and num_results to parent function
    return places, ids, state_counts, keyword, num_results