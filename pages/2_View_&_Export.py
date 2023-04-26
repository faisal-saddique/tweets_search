import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

if ("proceed" in st.session_state and st.session_state["proceed"]):

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

    st.write("NOTE: Please uncheck the 'include' value for the tweet you don't want to include in the final result.")
    df = pd.DataFrame(data, columns=['author', 'tweet', 'include'])
    updated_df = st.experimental_data_editor(df, use_container_width=True)

    # Drop rows where 'include' is False
    final_df = updated_df.drop(updated_df[updated_df['include'] == False].index)

    # st.dataframe(final_df,use_container_width=True)

    # Cache the conversion to prevent computation on every rerun
    @st.cache_data
    def convert_df(df):
        # Drop any unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.drop('include', axis=1)
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(final_df)

    st.subheader("Download Results")
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name='tweets.csv',
        mime='text/csv',
    )

else:
    switch_page("Search Tweets")