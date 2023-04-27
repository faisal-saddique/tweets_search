# Tweets Search Streamlit App

This app allows users to search for tweets on a particular hashtag. Users can enter the hashtag they are interested in searching and the maximum number of results they want to fetch.

The app then makes API calls to the Twitter API using the Tweepy library to search for recent tweets containing that hashtag and retrieve count data for the number of tweets over the past 7 days.

It displays the tweet count chart and up to the specified number of recent tweets containing that hashtag. It shows the username and tweet text for each result.

Users can adjust the number of results and search for different hashtags to explore different topics on Twitter. This app streamlines searching and analyzing trends on Twitter hashtags.

## Instructions

1.	Install Python 3: If you don't already have Python 3 installed on your machine, you can download the latest version from the official Python website: https://www.python.org/downloads/windows/. Once you download the installer, run it and follow the prompts to install Python on your machine. Make sure to add Python to your system's PATH variable during the installation process.
2.	Download the tweets_search repository: Go to the repository's GitHub page (https://github.com/faisal-saddique/tweets_search) and click on the green "Code" button. Then select "Download ZIP" and save the ZIP file to a location on your computer.
3.	Extract the ZIP file: Navigate to the location where you saved the ZIP file and extract its contents. You should now have a folder called tweets_search-master.
4.	Install the required Python packages: Open a command prompt and navigate to the tweets_search-master folder. Then run the following command to install the required Python packages:
`pip install -r requirements.txt` 
5.	Set up your Twitter API credentials: To use the app, you need to have Twitter API credentials. If you don't already have them, you can apply for a Twitter Developer account and create an app to get your API credentials. You can follow the instructions here to create a developer account and app: https://developer.twitter.com/en/docs/apps/overview.
6.	Update the Twitter API credentials: Once you have your Twitter API credentials, open the .streamlit/secrets.toml file in the tweets_search folder and add the bearer token value.
7.	Start the app: To start the app, run the following command in the command prompt while you are still in the tweets_search-master directory:
`streamlit run Search_Tweets.py`

This will start the app in your default web browser. You can now use the app to search for tweets and save them locally.