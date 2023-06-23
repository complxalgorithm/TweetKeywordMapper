<h1 align="center">Tweet Keyword Mapper</h1>

Search Twitter for Tweets containing a particular keyword from the command line, then write results to a CSV or XLSX file and/or map the results using ArcGIS Pro or GeoPandas.

[![asciicast](https://asciinema.org/a/lueHvB8fK4EX5wpFPOzvHHzDS.svg)](https://asciinema.org/a/lueHvB8fK4EX5wpFPOzvHHzDS)

Tweet data can be imported from a CSV or XLSX file, which will then be used for counting the number of Tweets from each state. You can pull data for multiple keywords from the file.

[![asciicast](https://asciinema.org/a/592490.svg)](https://asciinema.org/a/592490)

It is also possible to display a count and percentage of the total for all unique field values within a CSV or XLSX file. An example use is displaying the aforementioned statistics for all unique keywords that are present within a CSV or XLSX file.

[![asciicast](https://asciinema.org/a/RK8sRi71azh9PniNo73hD83C4.svg)](https://asciinema.org/a/RK8sRi71azh9PniNo73hD83C4)

Count results can be appended to shapefiles (ArcGIS Pro & GeoPandas) or feature classes within geodatabases (ArcGIS Pro).

If your default file does not exist within the project directory, the program will create the file for you using Tweet_ID, Keyword, and State as default field names. It is best to create a file in this manner.

The program can be ran as the <em>tweetkeywordmapper</em> package, or by using the <em>tkm</em> shell script.

## Requirements
1. Python 3
2. Tweepy
3. Pandas
4. GeoPandas
5. Matplotlib 
6. Numpy
7. ArcPy - learn how to download and install ArcGIS Pro [here](https://pro.arcgis.com/en/pro-app/latest/get-started/download-arcgis-pro.htm).
    - This is only required if you want to map your results using ArcGIS Pro.
    - The only way to install this library is by purchasing an ArcGIS Pro license and installed the software onto your machine.

If you are installing Pandas manually, it is ideal to install all of its dependencies.
```
pip3 install pandas[all]
```

## Set Up & Run
In order to run this program to its fullest extent, you will first need to download the repository onto your machine and install the requirements. You will then need to add appropriate constants values within the TweetKeywordConstants_TEMP.py file, and then remove "_TEMP" from the file name. Using the Tweepy library requires setting up a Twitter Developer account, and then creating a new project. Using ArcGIS Pro requires the Windows operating system and a paid license to use.

### Download & Install
You can download the program in a couple ways. Download a zip file of this repository by clicking [this link](https://github.com/complxalgorithm/TweetKeywordMapper/archive/refs/heads/master.zip).

You can also use git to clone the repo by running the following in your terminal:
```
git clone https://github.com/complxalgorithm/TweetKeywordMapper.git
```
Next, set the workspace of your project (i.e., your ArcGIS Pro project) within the TweetKeywordConstants_TEMP.py file. Your workspace can either be within the TweetKeywordMapper directory that you downloaded, or in a different directory. You then need to set the name of the default csv file. This file should be located within the TweetKeywordMapper directory. If no file with the set name exists, the program will create a blank csv file with the appropriate fields.

#### Install Requirements
You can install all modules other than ArcPy by running the following command within the TweetKeywordMapper directory:
```
pip3 install -r requirements.txt
```
You can then download ArcGIS Pro if you have a Windows machine, and that will automatically install the latest version of ArcPy.

### Using Twitter API
1. Set up a Twitter Developer account [here](https://developer.twitter.com).
2. Create a Project on your account.
3. Navigate to "Projects & Apps," then click on your name under the relevant project.
4. At the top of your screen, click on "Keys and tokens".
5. Generate all necessary keys, then copy <em>all of them</em> down making sure you know which is which:
    - API Key and Secret
    - Bearer Token
    - Access Token and Secret
6. Add each key, token, and secret to its respective variable in the TweetKeywordConstants_TEMP.py file.
7. Change the above file name to TweetKeywordConstants.py.

### Using ArcGIS Pro
1. Assuming you are on Windows, purchase a use license [here](https://www.esri.com/en-us/arcgis/products/arcgis-pro/buy#for-individuals).
2. Follow the instructions that are on Esri's website on how to successfully install the software.

<em>You will need to create a new ArcGIS Pro project using the map template before running the program.</em>
<em>Additionally, ArcGIS Pro **cannot** be open at the same time that you execute the program.</em>

### Run
Once the program is downloaded onto your machine and all of the requirements are met, you can now run the program. Support is available to run the program as the <em>tweetkeywordmapper</em> Python package, or by using the <em>tkm</em> shell script. Both of these support four argument/parameter options.

#### Python
The program runs as the <em>tweetkeywordmapper</em> package.
```
username ^ TweetKeywordMapper => python3 tweetkeywordmapper -h
usage: python3 tweetkeywordmapper [-h] [-s] [-r] [-c]

Search/Import Tweet data from US states with a keyword, then map the count results

optional arguments:
  -h, --help    show this help message and exit
  -s, --search  search Twitter for Tweets containing a specific keyword, then map results
  -r, --read    import Tweet data from a CSV/XLSX file, then map results
  -c, --counts  tally the total for each unique value of a specified field from a CSV/XLSX file
```
The program accepts a single argument with one of four options: search, read, counts, or help.

#### Shell
You can also use the <em>tkm</em> shell script to execute the program.

Make the script executable by running the following command within the TweetKeywordMapper directory:
```
chmod +x tkm
```

After making the script executable, you can simply run the main program by entering:
```
./tkm
```

The script accepts a single parameter with the same options as the Python program.
```
username ^ TweetKeywordMapper => ./tkm help
usage: ./tkm <parameter>

Search/Import Tweet data from US states with a keyword, then map the count results

optional parameters:
search:  search Twitter for Tweets containing a specific keyword, then map results
read:    import Tweet data from a CSV/XLSX file, then map results
counts:  tally the total for each unique value of a specified field from a CSV/XLSX file
help:    displays help information for this script

- search and read will run mapper.py to map the results after state counts are determined.
```

## Disclaimers
This program is not an official Twitter or Esri project. This is a project that I made for a college course and is not affiliated <em>in any way</em> with Twitter/X Corp. or Esri. If you represent either of these companies and have an issue with this project, feel free to reach out to me at any time. Regardless, please do not sue me.

Sometimes, a Tweet will be missed that should have been counted. I tried to limit as many mistakes as possible. To me, it is better to exclude Tweets that should have been included than it is to include Tweets that should have been excluded. There still may be times where a Tweet is counted that should not have been. That is still rarer than Tweets not getting counted that should have been.

There may be times when you specify a higher number of expected results, but the program doesn't reach it. That is because Twitter has a set limit of 100 results for each search query. This program will only count Tweets from which it is able to extract a state of origin towards your specified number of search results.

If you decide to map your results using ArcGIS Pro and you have mapped results for the same keyword using ArcGIS Pro, the program will overwrite field names and their attribution values that are already on the target US states shapefile (i.e., there will not be duplicate fields of the same name). The full field name should be added to ArcGIS Pro, as well. Mapping using GeoPandas will <em>not</em> overwrite duplicate fields, and will simply create a new field with a number appended to it. The field names in this case will have a limit of ten (10) characters, so the full name of the field will not appear (i.e., "Tweet_Count" would be "Tweet_Coun").

Unfortunately, due to how the code is written, you may run into issues with CSV files that have more than three fields. The program will add the data that was found by searching Twitter using the field indexes of the Tweet IDs, states, and keywords fields. I do not know if it will still work successfully with CSV files that contain more than three (3) fields.

Upon adding support for XLSX files, I kept getting a UnicodeDecodeError or ParserError when running the <em>counts</em> functionality on a preexisting CSV file. After setting my default file to a non-existent CSV file and having the program create it for me, the program was able to run without issues. This is either a bug in my code, in Pandas's code, and/or the CSV files with which I was attempting to run the program were corrupted.

## To-Do List
- [X] Clean up state extraction algorithm
- [X] Find instance of a state's name in place values like "New York and the World" and return the appropriate state value.
- [X] Get state from Tweet where user's location has something like "NY -> FL".
- [X] Get state from Tweet where user's location has something like "Florida via New York"
- [ ] If place value from a Tweet is a set of X,Y coordinates, use those to determine state.
- [ ] Identify area codes in place value and use them to determine state of origin.
- [X] When writing data to a csv, organize each row's data based on the location of their respective field in the file.
- [X] Handle situations like when shapefiles can't be found in the user specified directory.
- [X] Allow user to interact with Excel files.
- [ ] Add support for mapping using PyQGIS.
- [X] Add support for mapping using GeoPandas.
- [ ] Allow user to search Tweets in other languages.
- [ ] Allow user to search Tweets from different countries.

## Contributing
Contributions to this program are more than welcome. Simply make a pull request for my review. If there are any issues with or any suggestions for the program that you have, create an issue for my review.

My only requirement is that you thoroughly comment your code so that others and I can follow along with what you are doing, and can learn from what you added.

## Copyright
&copy; 2023 [Stephen C. Sanders](https://stephensanders.me). Licensed under the <a href="https://github.com/complxalgorithm/TweetKeywordMapper/blob/master/LICENSE">MIT License</a>. Credit would be appreciated.
