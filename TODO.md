## Completed
- [X] Clean up state extraction algorithm
- [X] Find instance of a state's name in place values like "New York and the World" and return the appropriate state value.
- [X] Get state from Tweet where user's location has something like "NY -> FL".
- [X] Get state from Tweet where user's location has something like "Florida via New York"
- [X] Identify area codes in place value and use them to determine state of origin.
- [X] When writing data to a csv, organize each row's data based on the location of their respective field in the file.
- [X] Allow user to interact with Excel files.
- [X] Allow user to extract data for multiple keywords from their file.
- [X] Add support for mapping using GeoPandas.
- [X] If place value from a Tweet is a set of X,Y coordinates, use those to determine state.
- [X] Account for full addresses so that a house number is not mistaken for an area code.

## Major
- [ ] Allow user to search Tweets in other languages.
- [ ] Allow user to search Tweets from different countries.
- [ ] If adding support for other languages and/or countries, start storing language/country data in file.

## Minor
- [ ] Ask user if they would like to set the name of the new field in the feature class and the name of the generated map.
- [ ] Extract time and date from Tweet and store this data in file.
- [ ] Allow user to save generated plot as a PNG before showing it.
- [ ] Add support for mapping using PyQGIS.