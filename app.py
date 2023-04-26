import tweepy
import streamlit as st
# import logging
import sys
import pandas as pd

sys.setrecursionlimit(15000)
# logging.basicConfig(level=logging.DEBUG)

# # read configs
# with open('config.json', 'r') as f:
#     config = json.load(f)

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

hashtag = st.text_input("Please enter the hashtag you wanna search (without #):")
max_results = st.number_input("Number of results you wanna fetch (between 10 and 100):",min_value=10,max_value=100,value=10)

if st.button("Proceed"):

    response_tweets = search_tweets(hashtag,max_results)
    response_count = search_tweets_counts(hashtag)

    st.subheader(f"Number of tweets for #{hashtag} the past 7 days:")
    st.dataframe(response_count, use_container_width=True)

    st.write("---")

    st.subheader(f"Tweets:")

    tweets = response_tweets.data

    usernames = response_tweets.includes['users']

    # Each Tweet object has default ID and text fields
    for (tweet,user) in zip(tweets,usernames):
        st.write(f"**Username:** {user}")
        st.write(f"**Tweet:** {tweet.text}")
        st.write("---")
