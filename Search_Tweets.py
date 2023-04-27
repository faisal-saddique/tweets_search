import tweepy
import streamlit as st
# import logging
import sys
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

if "duplicates" not in st.session_state:
    st.session_state["duplicates"] = []

sys.setrecursionlimit(15000)
# logging.basicConfig(level=logging.DEBUG)

# bearer_token = config['bearer_token']
bearer_token = st.secrets['bearer_token']

@st.cache_data
def search_tweets(query,count):
    response_tweets = client.search_recent_tweets(
        query=f"#{query} -is:retweet", max_results=count, expansions=["author_id"])
    return response_tweets

@st.cache_data
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

st.session_state["hashtag"] = st.text_input("Please enter the hashtag you wanna search (without #):")
max_results = st.number_input("Number of results you wanna fetch (between 10 and 100):",min_value=10,max_value=100,value=10)

if st.button("Proceed"):

    st.session_state["response_tweets"] = search_tweets(st.session_state["hashtag"], max_results)
    st.session_state["response_count"] = search_tweets_counts(st.session_state["hashtag"])

    st.session_state["proceed"] = True
    switch_page("View & Export")