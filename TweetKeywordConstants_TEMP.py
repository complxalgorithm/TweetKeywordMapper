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
# I had to include many state name and abbreviation variations here as well
cities = {
    'NYC': 'New York',
    'New York City': 'New York',
    'Brooklyn': 'New York',
    'Manhattan': 'New York',
    'Buffalo': 'New York',
    'WNY': 'New York',
    'Calif': 'California',
    'Cali': 'California',
    'Cal': 'California',
    'L.A': 'California',
    'Los Angeles': 'California',
    'San Diego': 'California',
    'San Jose': 'California',
    'San Francisco': 'California',
    'San Fran': 'California',
    'SoCal': 'California',
    'Sacramento': 'California',
    'Long Beach': 'California',
    'Oakland': 'California',
    'Chicago': 'Illinois',
    'Chi': 'Illinois',
    'Chitown': 'Illinois',
    'Houston': 'Texas',
    'SA': 'Texas',
    'S.A': 'Texas',
    'San Antonio': 'Texas',
    'Dallas': 'Texas',
    'Frisco': 'Texas',
    'Phoenix': 'Arizona',
    'Tuscon': 'Arizona',
    'Philly': 'Pennsylvania',
    'Philadelphia': 'Pennsylvania',
    'Pittsburgh': 'Pennsylvania',
    'Washington DC': 'District of Columbia',
    'Washington D.C': 'District of Columbia',
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
    'Sea': 'Washington',
    'Miami': 'Florida',
    'Orlando': 'Florida',
    'Tampa Bay': 'Florida',
    'Tallahassee': 'Florida',
    'New Orleans': 'Louisiana',
    'LA Gulf Coast': 'Louisiana',
    'Minneapolis': 'Minnesota',
    'Omaha': 'Nebraska',
    'Las Vegas': 'Nevada',
    'L.V': 'Nevada',
    'LV': 'Nevada',
    'Sin City': 'Nevada',
    'Reno': 'Nevada',
    'Charlotte': 'North Carolina',
    'Tuscaloosa': 'Alabama',
    'Milwaukee': 'Wisconsin',
    'Memphis': 'Tennessee',
    'Louisville': 'Kentucky',
    'Cleveland': 'Ohio',
    'Albuquerque': 'New Mexico',
    'Denver': 'Colorado',
    'Detroit': 'Michigan',
    'A.L': 'Alabama',
    'A.K': 'Alaska',
    'A.Z': 'Arizona',
    'A.R': 'Arkansas',
    'C.A': 'California',
    'C.O': 'Colorado',
    'C.T': 'Connecticut',
    'D.E': 'Delaware',
    'D.C': 'District of Columbia',
    'F.L': 'Florida',
    'G.A': 'Georgia',
    'H.I': 'Hawaii',
    'I.D': 'Idaho',
    'I.L': 'Illinois',
    'I.N': 'Indiana',
    'I.A': 'Iowa',
    'K.S': 'Kansas',
    'K.Y': 'Kentucky',
    #'L.A': 'Louisiana',
    'M.E': 'Maine',
    'M.D': 'Maryland',
    'M.A': 'Massachusetts',
    'M.I': 'Michigan',
    'M.N': 'Minnesota',
    'M.S': 'Mississippi',
    'M.O': 'Missouri',
    'M.T': 'Montana',
    'N.E': 'Nebraska',
    'N.V': 'Nevada',
    'N.H': 'New Hampshire',
    'N.J': 'New Jersey',
    'N.M': 'New Mexico',
    'N.Y': 'New York',
    'N.C': 'North Carolina',
    'N.D': 'North Dakota',
    'O.H': 'Ohio',
    'O.K': 'Oklahoma',
    'O.R': 'Oregon',
    'P.A': 'Pennsylvania',
    'R.I': 'Rhode Island',
    'S.C': 'South Carolina',
    'S.D': 'South Dakota',
    'T.N': 'Tennessee',
    'T.X': 'Texas',
    'U.T': 'Utah',
    'V.T': 'Vermont',
    'V.A': 'Virginia',
    'W.A': 'Washington',
    'W.V': 'West Virginia',
    'W.I': 'Wisconsin',
    'W.Y': 'Wyoming'
}