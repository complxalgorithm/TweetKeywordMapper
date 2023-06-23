"""

@Name: search.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Searches Twitter using a specfied keyword and extracts the US state of origin for
              a user specified number of results, then writes data for each result to CSV/Excel file
@Requirements: Python3, pandas, tweepy

"""

# import modules
import tweepy
from tweepy import OAuthHandler
import time

try:
    from tweetkeywordmapper.core import extract_place as ex
    from tweetkeywordmapper.core import data
    from tweetkeywordmapper.core import stats
    from tweetkeywordmapper.core import constants as cons
except:
    from core import extract_place as ex
    from core import data
    from core import stats
    from core import constants as cons


"""
# define ifWrite() function - allow user to signal whether or not they want to write search results
# to a CSV or XLSX file
"""
def ifWrite():
    # ask user for input
    answer = input('Would you like to write Tweet data to a CSV/Excel file? (Y or N): ')
    
    # validate input
    while answer.capitalize() != 'Yes' and answer.upper() != 'Y' and answer.capitalize() != 'No' and answer.upper() != 'N':
        # display error
        print(f'{answer} is not valid. Please try again.')
        
        # ask user for input again
        answer = input('Would you like to write Tweet ID and State data to a CSV/Excel file? (Y or N): ')
    
    # return answer to parent function
    return answer


"""
# define TweetKeywordSearch() function - searches for Tweets using a specified keyword and
# returns the found states, the Tweet IDs, state counts, and keyword used.
"""
def TweetKeywordSearch(ws, default_file, states, cities):
    """
    # authorize access to Twitter API by using your project's key, tokens, and secrets
    # these tokens/secrets/key can be found on your project on your Twitter Developer Portal
    """
    
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
    api = tweepy.API(auth, wait_on_rate_limit=True)

    """
    # get data directly from a search query using Twitter's API
    # the data will be a list of states, and list of Tweet IDs, a dictionary of Tweet counts per state, and the keyword
    """
    
    # ask user to enter a keyword of interest
    keyword = input('Enter the keyword: ')

    # ask user how many results they would like
    num_res = input('How many results would you like to get? ')
    
    # validate that num_res is an integer
    while not num_res.isdigit():
        # tell user their input is not an integer
        print(f'{num_res} is not an integer.')
        
        # ask user again how many results they would like
        num_res = input('How many results would you like to get? ')

    # convert valid input to an integer
    num_res = int(num_res)
    
    # new line
    print()
    
    # create a search query using user keyword
    query = keyword + ' -filter:retweets lang:en' # exclude retweets and only include english tweets

    # get 100 search results using query
    search_results = tweepy.Cursor(api.search_tweets, q=query, count=100).items()
            
    # get lists of places and tweet ids from search results
    places, ids = ex.get_states_ids_from_results(search_results, api, states, cities, num_res)
            
    # get dictionary of counts for each state
    state_counts = stats.get_counts(places, states=states)
        
    # get number of tweets that were returned
    num_results = len(ids)
        
    # only ask user if they want to write to a file if there were search results for keyword
    if num_results == 0:
        # display there were no search results returned
        print(f'Searching for {keyword} returned no results.')
    else:
        # display number of search results returned
        print(f'Searching for {keyword} returned {num_results} results\n.')
            
        # ask user if they want to write results to file
        if_write = ifWrite()
            
        # run this if user signaled that they want to write results to file
        if if_write.capitalize() == 'Yes' or if_write.upper() == 'Y':
            # get file and its type to write to from user
            user_file, file_type = data.get_user_file(default_file)
            
            # get locations of data Tweet IDs, states, and keywords in the file using their indexes
            # in the user's file, and as well as a dictionary of Tweet data comprising the ids and places
            # also get a list of Tweet IDs that are already in the user's file
            # data parameter populated with ids and places lists
            tweets, tweet_data, state_index, id_index, keyword_index = data.file_interact([ids, places, ''], user_file, file_type,
                                                                                             ws, mode='r', function='search')
                
            # new line
            print()

            time.sleep(1.5)     # pause program for a second and a half
            
            # create empty written_data list to be used to store each Tweet result's data
            # to be used to write to file - allow for three places in list
            written_data = [None] * 3

            # iterate through tweet_data dict to write each tweet to the file
            for tweet_id in tweet_data:
                # append Tweet data to file if the Tweet ID is not already in the file
                if tweet_id not in tweets:
                    # add the relevant data to the correct index in the data list to write it to new line in user's file
                    written_data[state_index] = tweet_data[tweet_id]
                    written_data[id_index] = tweet_id
                    written_data[keyword_index] = keyword

                    # append this data to file
                    data.file_interact(written_data, user_file, file_type, ws)

                    # tell user data was successfully written to file
                    print(f'{written_data} was added to {user_file}')

                # inform user when data for a Tweet is already within the file
                else:
                    print(f'Data for {tweet_id} is already in {user_file}.')
    
    # return places, ids, state_counts, keyword, and num_results to parent function
    return places, ids, state_counts, keyword, num_results