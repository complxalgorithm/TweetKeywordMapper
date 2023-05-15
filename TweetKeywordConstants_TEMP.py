"""

@Name: TweetKeywordConstants.py
@Author: Stephen Sanders <https://stephensanders.me>
@Description: Holds authorization key/tokens/secrets, as well as the workspace and default_csv values.

"""

bearer_token = '<ADD BEARER TOKEN HERE>'
consumer_key = "<ADD CONSUMER KEY HERE>"
consumer_secret = "<ADD CONSUMER SECRET HERE>"
access_token = "<ADD ACCESS TOKEN HERE>"
access_secret = "<ADD ACCESS SECRET HERE>"

# set path to workspace
workspace = r'<ADD WORKSPACE HERE>'

# set default csv file
default_csv = '<ADD CSV FILE NAME HERE>'

# create states dictionary that stores states using abbrev as key
states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District of Columbia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}

# make sure certain populous US cities (and DC) are included directly
# initialize a cities dict with city names as keys and their respective state as the values
# I had to include the other spelling of Hawaii (i.e., Hawai'i) here after running into a case
cities = {
    'NYC': 'New York',
    'New York City': 'New York',
    'Calif': 'California',
    'LA': 'California',
    'L.A.': 'California',
    'Los Angeles': 'California',
    'SD': 'California',
    'S.D.': 'California',
    'San Diego': 'California',
    'San Jose': 'California',
    'San Francisco': 'California',
    'San Fran': 'California',
    'Bay Area': 'California',
    'SoCal': 'California',
    'Chicago': 'Illinois',
    'Chi': 'Illinois',
    'Houston': 'Texas',
    'SA': 'Texas',
    'S.A.': 'Texas',
    'San Antonio': 'Texas',
    'Dallas': 'Texas',
    'Phoenix': 'Arizona',
    'Philly': 'Pennsylvania',
    'Philadelphia': 'Pennsylvania',
    'Washington DC': 'District of Columbia',
    'D.C.': 'District of Columbia',
    'DC.': 'District of Columbia',
    'Honolulu': 'Hawaii',
    'Hawai\'i': 'Hawaii',
    'Hawaiian': 'Hawaii',
    'Baltimore': 'Maryland',
    'Atlanta': 'Georgia',
    'ATL': 'Georgia',
    'Boston': 'Massachusetts',
    'Seattle': 'Washington',
    'Miami': 'Florida',
    'Orlando': 'Florida',
    'New Orleans': 'Louisiana',
    'Minneapolis': 'Minnesota'
}