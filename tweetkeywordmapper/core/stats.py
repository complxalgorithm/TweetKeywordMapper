# import module
import numpy as np

"""
# define get_counts() function - uses lists of unique values and states to count
# total number of Tweets from each state in the search results
#   - states   -> default to empty dictionary
#   - df       -> default to None
#   - field    -> default to empty string
#   - function -> default to empty string
"""
def get_counts(values, states={}, df=None, field='', function=''):
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
#   - function -> default to empty string
"""
def get_count_percentages(counts, num_res, states, function=''):
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