import tweepy
import streamlit as st
# import logging
import sys
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import os
import json
import datetime

if "duplicates" not in st.session_state:
    st.session_state["duplicates"] = []


sys.setrecursionlimit(15000)
# logging.basicConfig(level=logging.DEBUG)

# bearer_token = config['bearer_token']
bearer_token = st.secrets['bearer_token']

# st.write(bearer_token)

# @st.cache_data
def search_tweets(query,count,hours_before):
    time_before_x_hours = datetime.datetime.utcnow() - datetime.timedelta(hours=hours_before)
    # format the time as a string in the desired format
    time_before_x_hours_str = time_before_x_hours.strftime('%Y-%m-%dT%H:%M:%SZ')

    response_tweets = client.search_recent_tweets(
        query=f"#{query} -is:retweet", max_results=count, expansions=["author_id"], start_time=time_before_x_hours_str, end_time=(datetime.datetime.utcnow() - datetime.timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%SZ'))
    return response_tweets

# @st.cache_data
def search_tweets_counts(query):
    response_count = client.get_recent_tweets_count(query=f"#{query} -is:retweet", granularity="day")
    data = []
    for i in response_count.data:
        data.append({
            'start': i['start'],
            'end': i['end'],
            'tweet_count': i['tweet_count']
        })
    df = pd.DataFrame(data)
    return df

@st.cache_resource
def create_client():
    return tweepy.Client(bearer_token)

client = create_client()

st.title("Twitter Scrapper")

# load existing JSON file or prompt user to set the credentials first
try:
    with open('settings.json', 'r') as file:
            # st.subheader("Previous settings")
            data = json.load(file)
            # st.json(data)

            st.session_state["hashtag"] = data['hashtag']
            st.session_state["hours"] = data["hours_range"]
            file_path = data['filepath']

            st.session_state["max_results"] = st.number_input("Number of results you wanna fetch (between 10 and 100):",min_value=10,max_value=100,value=10)

            if st.button("Proceed"):

                # Get file path from user input
                if "file_path" not in st.session_state:
                    st.session_state["file_path"] = file_path

                st.write(st.session_state["file_path"] )

                # Verify if the file path is valid
                if st.session_state["file_path"]:
                    try:
                        os.makedirs(os.path.dirname(st.session_state["file_path"]), exist_ok=True)
                        with open(st.session_state["file_path"], 'a', encoding='utf-8-sig') as f:
                            pass
                    except Exception as e:
                        st.error(f"Invalid file path: {e}")
                        st.stop()

                st.session_state["response_tweets"] = search_tweets(
                    st.session_state["hashtag"], st.session_state["max_results"] , int(st.session_state["hours"]))

                st.session_state["proceed"] = True
                switch_page("View & Export")
            
except (FileNotFoundError, json.JSONDecodeError):
            st.write("Settings file not found. Please go to settings tab, and update the file path and hashtag search string.")