# import modules
import sys
from scripts import mapper as tkm
from scripts import counts as cnts

# define helpFunc() function - display usage information
def helpFunc():
    print('')
    print('Usage: python3 tweetkeywordmapper <argument>')
    print('Argument Options: mapper, counts, help\n')
    print('mapper:\tmapper.py - main Twitter search, CSV import, and counts program')
    print('counts:\tcounts.py - tallies a total for each unique value of a specified field from a CSV file')
    print('help:\tdisplays help information for this script')
    print('')
    print('If you do not enter an argument, mapper.py will run by default.\n')

# get last argument
arg = sys.argv[-1]

# get number of arguments except for name of program
num_args = (len(sys.argv)-1)

# handle when there are no other arguments other than the program name
if num_args == 0:
    # run the mapper.py script
    tkm.TweetKeywordMapper()

# handle when there is only one argument outside of the program name
elif num_args == 1:
    # run the mapper.py script if mapper is the argument
    if arg == 'mapper':
        tkm.TweetKeywordMapper()
    
    # run the counts.py script if counts is the argument
    elif arg == 'counts':
        cnts.main()
    
    # display help information if help is the argument
    elif arg == 'help':
        helpFunc()
    
    # for any other argument value, display error and then help information
    else:
        print(f'ERROR - {arg} is not a valid argument value.')
        helpFunc()

# handle when more than 1 argument is entered
else:
    # display an error and then help information
    print('ERROR - Too many arguments. Only 1 is allowed at most.')
    helpFunc()