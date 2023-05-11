import TweetKeywordData as data
import TweetKeywordConstants as cons

ws = cons.workspace
states = cons.states
default_csv = cons.default_csv

places, ids, keyword = data.csv_interact((), default_csv, ws, mode='r', checkKeyword=True)

state_counts = data.get_state_counts(places, states)

print(f'\nKeyword: {keyword}\n\nIDS: {ids}\n\nPlaces: {places}\n\nCounts: {state_counts}')