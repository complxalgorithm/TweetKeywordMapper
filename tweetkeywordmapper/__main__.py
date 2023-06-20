# import modules
import sys
import time
from scripts import mapper as tkm
from scripts import counts as cnts

# define helpFunc() function - display usage information
def helpFunc():
    print('Usage: python3 tweetkeywordmapper <argument>')
    print('Argument Options: mapper, counts, help\n')
    print('mapper:\tmapper.py - main Twitter search, CSV import, and counts program')
    print('counts:\tcounts.py - tallies a total for each unique value of a specified field from a CSV file')
    print('help:\tdisplays help information for this script\n')
    print('If you do not enter an argument, mapper.py will run by default.\n')


# define main() function - handles arguments and runs appropriate functionality
def main():
    # set name of package
    pkg = 'tweetkeywordmapper'
    
    # initialize list of available arguments
    avail_args = ['mapper', 'counts', 'help']

    # get last argument
    arg = sys.argv[-1]

    # get number of arguments except for name of program
    num_args = (len(sys.argv)-1)
    
    ""
    # handle arguments, or lack thereof
    ""
    
    # run this if only the package name is entered or the package name and a valid argument are entered
    if (num_args == 0 and arg == pkg) or (num_args == 1 and arg in avail_args):
        # display welcome message
        print('Welcome to Tweet Keyword Mapper!\n')
        
        time.sleep(1)   # pause program for a second

        # do this when package name is the only argument
        if num_args == 0 and arg == pkg:
            # run the mapper.py script
            tkm.TweetKeywordMapper()

        # do this if there is 1 additional argument that is in the avail_args list
        else:
            # run the mapper.py script if mapper is the argument
            if arg == 'mapper':
                tkm.TweetKeywordMapper()

            # run the counts.py script if counts is the argument
            elif arg == 'counts':
                cnts.main()

            # display usage information if help is the argument
            else:
                helpFunc()

        time.sleep(1)   # pause program for a second

        # display goodbye after the program has executed
        print('\nThank you for using Tweet Keyword Mapper!')

    # handle when more than 1 argument or an invalid argument is entered
    else:
        # display too many arguments error
        if num_args > 1:
            print('ERROR - Too many arguments. Only 1 is allowed at most.\n')
        
        # display invalid argument value error
        else:
            print(f'ERROR - {arg} is not a valid argument value.\n')
        
        # display usage information
        helpFunc()


# execute program
main()