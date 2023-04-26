import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.subheader(f"Number of tweets for #{st.session_state['hashtag']} the past 7 days:")
st.dataframe(st.session_state["response_count"], use_container_width=True)

st.write("---")

st.subheader(f"Tweets:")

tweets = st.session_state["response_tweets"].data

usernames = st.session_state["response_tweets"].includes['users']

data = []
with st.expander("Expand fetched tweets"):
    for i, (tweet, user) in enumerate(zip(tweets, usernames)):
        data.append({
            'author': user,
            'tweet': tweet.text,
            'include': True
        })
        st.write(f"**Author:** {user}")
        st.write(f"**Tweet:** {tweet.text}")
        st.write("---")

df = pd.DataFrame(data, columns=['author', 'tweet', 'include'])
updated_df = st.experimental_data_editor(df, use_container_width=True)

st.dataframe(updated_df,use_container_width=True)