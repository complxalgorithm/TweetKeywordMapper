# Tweet Keyword Mapper
Search Twitter for Tweets containing a particular keyword or read Tweet data from a csv file, then write results to a csv file and/or map the results using ArcGIS Pro.

# Requirements
1. Python 3 - get the latest release [here](https://www.python.org/downloads).
2. Pandas - learn how to install [here](https://pandas.pydata.org/docs/getting_started/install.html).
3. Tweepy - learn how to install [here](https://docs.tweepy.org/en/stable/install.html).
    - This is only required if you do not want to use the search capabilities and instead already have a csv file containing Tweet data.
4. ArcPy - learn how to download and install ArcGIS Pro [here](https://pro.arcgis.com/en/pro-app/latest/get-started/download-arcgis-pro.htm).
    - This is only required if you want to map your results.

# Set Up & Run
In order to run this program to its fullest extent, you will need to install the Tweepy library and ArcGIS Pro. Using the Tweepy library requires setting up a Twitter Developer account. Using ArcGIS Pro requires the Windows operating system and a paid license to use.

## Using Twitter API
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

## Using ArcGIS Pro
1. Assuming you are on Windows, purchase a use license [here](https://www.esri.com/en-us/arcgis/products/arcgis-pro/buy#for-individuals).
2. Follow the instructions that are on Esri's website on how to successfully install the software.

<em>In order to run this program, ArcGIS Pro **cannot** be open at the same time that you execute the program.</em>

## Run
You can download the program in a couple ways. Download a zip file of this repository by clicking this link: https://github.com/complxalgorithm/TweetKeywordMapper/archive/refs/heads/master.zip

You can also use git to clone the repo by running the following in your terminal:
```
git clone https://github.com/complxalgorithm/TweetKeywordMapper.git
```

Once all of the requirements are met and the program is downloaded, you can run the code based on how your operating system runs Python scripts. In your terminal, change your current working directory to the TweetKeywordMapper directory, then run
```
py TweetKeywordMapper.py
```
Or, if on a non-Windows operating system, run
```
python3 TweetKeywordMapper.py
```

You can also run this program in an IDE, such as [PyCharm](https://www.jetbrains.com/pycharm/).

# Disclaimers
This program is not an official Twitter or Esri project. This is a project that I made for a college course and is not affiliated <em>in any way</em> with Twitter/X Corp. or Esri. If you represent either of these companies and have an issue with this project, feel free to reach out to me at any time. Regardless, please do not sue me.

Unfortunately, due to how the code is written, the program assumes a particular csv layout when writing data to a csv file. In order to get the most ideal outcome when writing your results to a csv file, your csv file should be organized so that there are only three (3) fields in this particular order:
```
Tweet IDS  |  Keyword  |  State
```

I will be updating the program in the future so that this is not the required layout (see To-Do List).

# To-Do List
- [ ] - When writing data to a csv file, organize each row's data based on the location of their respective field in the file.
- [ ] - Recognize coordinate location values and get state using them.
- [ ] - Organize the code into objects/classes.

# Contributing
Contributions to this program are more than welcome. Simply make a pull request for my review. If there are any issues with or any suggestions for the program that you have, create an issue for my review.

My only requirement is that you thoroughly comment your code so that others and I can follow along with what you are doing, and can learn from what you added.

# Copyright
&copy; 2023 [Stephen C. Sanders](https://stephensanders.me). Licensed under the <a href="https://github.com/complxalgorithm/TweetKeywordMapper/blob/master/LICENSE">MIT License</a>.
