<h1 align="center">Tweet Keyword Mapper</h1>

Search Twitter for Tweets containing a particular keyword from the command line, then write results to a CSV or XLSX file and/or map the count results using ArcGIS Pro or GeoPandas.

[![asciicast](https://asciinema.org/a/599643.svg)](https://asciinema.org/a/599643)

Import Tweet data from a CSV or XLSX file. Pull all data or data for one or more keyword from the file, then map the count results.

[![asciicast](https://asciinema.org/a/599644.svg)](https://asciinema.org/a/599644)

Display a count and percentage of the total for all unique field values within a CSV or XLSX file. An example use is displaying the aforementioned statistics for all unique keywords that are present within a CSV or XLSX file.

[![asciicast](https://asciinema.org/a/599645.svg)](https://asciinema.org/a/599645)

Mapping can be done on count results from the same session through searching Twitter or reading from a CSV/XLSX file, or on count results that were mapped in a previous session by specifying the relevant field within your US State boundaries shapefile. Below is an example map that was generated using GeoPandas:

<img src="./sample/sample_map.png" alt="sample geopandas map showing results Tweets that contained either of 4 keywords" />

## Other Features
- Create a file using default fields <em>Tweet_ID</em>, <em>Keyword</em>, and <em>State</em>.
    - Used if your default file does not already exist, or if you just want to create another file.
    - It is best to create a file used by this program in this manner.
- Download a US State boundaries shapefile from the [US Census Bureau](https://www.census.gov) website.
- Easily remove US territories from US State boundaries shapefile.
- Count results can be appended to shapefiles (ArcPy & GeoPandas) or feature classes within geodatabases (ArcPy).

<b>The program can be ran as the <em>tweetkeywordmapper</em> Python3 package, or by using the <em>tkm</em> shell script.</b>

## Requirements
1. python3
2. pip
3. tweepy
4. pandas / geopandas
5. geopy
6. matplotlib 
7. numpy
8. openpyxl
9. arcpy

In order to install ArcPy and ArcGIS Pro, you must have a Windows machine. <b>You can still run the program without ArcPy installed</b>, you will just have to map your results using GeoPandas.

## Set Up & Run
In order to run this program to its fullest extent, you will first need to download the repository onto your machine and install the requirements. You will then need to add appropriate constants values within the <em>constants_TEMP.py</em> file, and then remove "_TEMP" from the file name. Using the Tweepy library requires setting up a Twitter Developer account, and then creating a new project. Using ArcGIS Pro requires the Windows operating system and a paid license to use.

### Download & Install
You can download the program in a couple ways. Download a zip file of this repository by clicking [this link](https://github.com/complxalgorithm/TweetKeywordMapper/archive/refs/heads/master.zip).

You can also use git to clone the repo by running the following in your terminal:
```
$ git clone https://github.com/complxalgorithm/TweetKeywordMapper.git
```
Next, set the workspace of your project (i.e., your ArcGIS Pro project) within the <em>constants_TEMP.py</em> file. Your workspace can either be within the TweetKeywordMapper directory that you downloaded, or in a different directory.

You then need to set the name of the default CSV/XLSX file. This file should be located within the TweetKeywordMapper directory, but it doesn't have to be. You can use either of the sample files that are included to get started.

#### Install Requirements
You can install all modules other than ArcPy by running the following command within the TweetKeywordMapper directory:
```
$ pip3 install -r requirements.txt
```
You can then download ArcGIS Pro if you have a Windows machine, and that will automatically install the latest version of ArcPy.

#### Configure Shell Scripts
In order to run the <em>tkm</em> and <em>test</em> shell scripts, you will first need to make them executable. You can do this by running the following in the project directory:
```
$ python3 -m tweetkeywordmapper.utils.sh_exec_config
```
Bourne or C shell variants can run these scripts. They will not work if you use PowerShell, for instance.

### Using Twitter API
1. Set up a Twitter Developer account [here](https://developer.twitter.com).
2. Create a Project on your account.
3. Navigate to "Projects & Apps," then click on your name under the relevant project.
4. At the top of your screen, click on "Keys and tokens".
5. Generate all necessary keys, then copy <em>all of them</em> down making sure you know which is which:
    - API Key and Secret
    - Bearer Token
    - Access Token and Secret
6. Add each key, token, and secret to its respective variable in the <em>constants_TEMP.py</em> file.
7. Change the above file name to <em>constants.py</em>.

<b>This application now requires paid API access to use the Search functionality. Prepare to spend at least $100 per month if you would like to pull Tweet data.</b>

### Using ArcGIS Pro
1. Assuming you are on Windows, purchase a use license [here](https://www.esri.com/en-us/arcgis/products/arcgis-pro/buy#for-individuals).
2. Follow the instructions that are on Esri's website on how to successfully install the software.

<em>You will need to create a new ArcGIS Pro project using the map template before running the program.</em>
<em>Additionally, ArcGIS Pro **cannot** be open at the same time that you execute the program.</em>

### Getting US States Boundaries Shapefile
You can get a US states polygon shapefile from many places. Here are a few:
1. [United States Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)
2. [National Weather Service](https://www.weather.gov/gis/USStates)
3. [Data.gov](https://catalog.data.gov/dataset/tiger-line-shapefile-2017-nation-u-s-current-state-and-equivalent-national)

The program has functionality that allows you to download a US state boundaries shapefile from the US Census Bureau website. You can also download the shapefile manually.

It is recommended that you remove all territories (including Puerto Rico) from the shapefile because only results from a US <em>state</em> will be counted. The program has functionality that allows you to do that very easily (currently only available if you are using a shapefile).

This shapefile can be anywhere within the workspace that you specified in the <em>constants</em> module. It can be directly within your root workspace directory or within a subdirectory of the workspace directory.

### Run
Once the program is downloaded onto your machine and all of the requirements are met, you can now run the program. Support is available to run the program as the <em>tweetkeywordmapper</em> Python package, or by using the <em>tkm</em> shell script. Both of these support seven argument/parameter options.

#### Python
The program runs as the <em>tweetkeywordmapper</em> package. The program accepts up to three arguments with eight options: search, read, counts, map_field, create_file, delete_terrs, download_shp, or help.
```
$ python3 tweetkeywordmapper -h
usage: python3 tweetkeywordmapper [-s] [-r] [-c] [-m] [-f] [-d] [-p] [-h]

Search/Import Tweet data from US states with a keyword, then map the count results.
- search and read will run mapper.py to map the results after state counts are totaled.
- if you want to use two parameters, -f, -d, or -p must be one of them.
- to use three parameters, two of -f, -d, or -p must be used.

optional arguments:
  -s, --search        search Twitter for Tweets containing a specific keyword, then map results
  -r, --read          import Tweet data from a CSV/XLSX file, then map results
  -c, --counts        tally the count for each unique value of a field from a CSV/XLSX file
  -m, --map_field     map previous results field from shapefile using GeoPandas
  -f, --create_file   create a CSV or XLSX file to use for writing and importing Tweet data
  -d, --delete_terrs  delete US territories from US state boundaries shapefile
  -p, --download_shp  download US State boundaries shapefile from US Census Bureau website
  -h, --help          display usage information
```

#### Shell
The <em>tkm</em> shell script can be used to execute the program. This script acts as an execution wrapper for the <em>tweetkeywordmapper</em> package and executes the appropriate command depending on the parameter value(s).

You can run the script after making it executable. The script accepts up to three parameters with the same options and conditions as the Python execution.
```
$ ./tkm help
usage: ./tkm [search] [read] [counts] [map_field] [create_file] [delete_terrs] [download_shp] [help]

Search/Import Tweet data from US states with a keyword, then map the count results.
- search and read will run mapper.py to map the results after state counts are totaled.
- if you want to use two parameters, create_file, delete_terrs or download_shp must be one of them.
- to use three parameters, two of create_file, delete_terrs, and download_shp must be used.

optional parameters:
search:          search Twitter for Tweets containing a specific keyword, then map results
read:            import Tweet data from a CSV/XLSX file, then map results
counts:          tally the count for each unique value of a field from a CSV/XLSX file
map_field:       map previous results field from shapefile using GeoPandas
create_file:     create a CSV or XLSX file to use for writing and importing Tweet data
delete_terrs:    delete US territories from US state boundaries shapefile
download_shp:    download US State boundaries shapefile from US Census Bureau website
help:            display usage information
```

#### Optional: Set Alias
If you would like to run the program without having to be in the TweetKeywordMapper directory, you can set an alias pointing to the <em>tweetkeywordmapper</em> Python package or the <em>tkm</em> shell script by adding one of the following to your shell's config file (e.g., .zshrc):
```
alias tkm="python3 /path/to/TweetKeywordMapper/tweetkeywordmapper"

alias tkm="./path/to/TweetKeywordMapper/tkm"
```

## Testing
There are a few test scripts within the <em>tests</em> directory. You can use the <em>test</em> shell script to run them.
```
$ ./test help
usage: ./test [extract] [contents] [map_field] [help]

Test tweetkeywordmapper functionality

optional parameters:
extract:         test coordinates and find state in value functions from extract_place module
contents:        test get_file_contents_fields() function from data module
map_field:       test map_field functionality of TweetKeywordGeoPandas() method
help:            display usage information
```
You could also test them manually using Python3:
```
$ python3 -m tweetkeywordmapper.tests.test_extract_place

$ python3 -m tweetkeywordmapper.tests.test_file_contents_fields

$ python3 -m tweetkeywordmapper.tests.test_map_field
```

## Disclaimers
This program is not an official Twitter or Esri project. This is a project that I made for a college course and is not affiliated <em>in any way</em> with Twitter/X Corp. or Esri. If you represent either of these companies and have an issue with this project, feel free to reach out to me at any time. Regardless, please do not sue me.

Sometimes, a Tweet will be missed that should have been counted. I tried to limit as many mistakes as possible. To me, it is better to exclude Tweets that should have been included than it is to include Tweets that should have been excluded. There still may be times where a Tweet is counted that should not have been. That is still rarer than Tweets not getting counted that should have been.

Currently, the delete_terrs argument/parameter only works on shapefiles. The ability to use this functionality on feature classes within geodatabases will be added in the future.

There may be times when you specify a higher number of expected results, but the program doesn't reach it. That is because Twitter has a set limit of 100 results for each search query. This program will only count Tweets from which it is able to extract a state of origin towards your specified number of search results.

If you decide to map your results using ArcGIS Pro and you have mapped results for the same keyword using ArcGIS Pro, the program will overwrite field names and their attribution values that are already on the target US states shapefile (i.e., there will not be duplicate fields of the same name). The full field name should be added to ArcGIS Pro, as well. Mapping using GeoPandas will <em>not</em> overwrite duplicate fields, and will simply create a new field with a number appended to it. The field names in this case will have a limit of ten (10) characters, so the full name of the field will not appear (i.e., "Tweet_Count" would be "Tweet_Coun").

Unfortunately, due to how the code is written, you may run into issues with CSV/XLSX files that have more than three (3) fields. The program will add the data that was found by searching Twitter using the field indexes of the Tweet IDs, states, and keywords fields. I do not know if it will still work successfully with CSV/XLSX files that contain more than three (3) fields.

### Privacy
The data in the sample files contain Tweet IDs, the searched keyword that was found in each Tweet, and each Tweet's extracted state of origin. Twitter necessitates the screen name in order to view the Tweets on Twitter. The URL structure is as such:
```
https://twitter.com/SCREEN_NAME/status/TWEET_ID
```
While this program has to use the screen name in order to pull data about the user in the state extraction algorithm, it does not - nor will it ever - allow you to save the screen name affiliated with any Tweet to your CSV/XLSX file. If you append any of the Tweet IDs to the <em>twitter.com</em> domain, you will get an error saying that the account does not exist. It is because of this that you will not be able to view any of the Tweets on Twitter. This is by design.

## To-Do
See the [TODO](TODO.md) list to view features that will be added in the future.

## Contributing
Contributions are more than welcome. Simply make a pull request for my review. If there are any issues with, or any suggestions for, the program that you may have, create an issue for my review.

My only requirement is that you thoroughly comment your code so that others and I can follow along with what you are doing, and can learn from what you added.

## Copyright
&copy; 2023 [Stephen C. Sanders](https://stephensanders.me). Licensed under the <a href="https://github.com/complxalgorithm/TweetKeywordMapper/blob/master/LICENSE">MIT License</a>. Credit would be appreciated.
