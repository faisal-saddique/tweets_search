import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import regex as re
import os
from Search_Tweets import search_tweets

if "is_refreshed" not in st.session_state:
    st.session_state['is_refreshed'] = False

if ("proceed" in st.session_state and st.session_state["proceed"]):

    # st.subheader(f"Number of tweets for #{st.session_state['hashtag']} the past 7 days:")
    # st.dataframe(st.session_state["response_count"], use_container_width=True)

    # st.write("---")

    # st.title(st.session_state["file_path"])
    
    # st.divider()

    st.subheader(f"Tweets:")

    if st.button("Refresh",use_container_width=True):

        old_tweets = st.session_state["response_tweets"].data
        new_tweets = search_tweets(st.session_state["hashtag"], st.session_state["max_results"], int(st.session_state["hours"]))
        st.session_state["response_tweets"] = new_tweets
        new_users = new_tweets.includes['users']
        new_tweets = new_tweets.data
        
        # Create a new dataframe with only the new tweets
        data = []
        with st.expander("Expand fetched tweets"):
            for i, (tweet, user) in enumerate(zip(new_tweets, new_users)):
                if tweet not in old_tweets:
                    data.append({
                        'author': user,
                        'tweet': tweet.text,
                        'include': False
                    })

                    st.write(f"**Author:** {user}")
                    st.write(f"**Tweet:** {tweet.text}")
                    st.write("---")

        df_new = pd.DataFrame(data, columns=['author', 'tweet', 'include'])

        # Append the new dataframe to the existing dataframe
        # df = pd.concat([st.session_state["df"], df_new], ignore_index=True)

        # Update the session state variable
        st.session_state["df"] = df_new
        st.session_state['is_refreshed'] = True

    if not st.session_state['is_refreshed']:
        tweets = st.session_state["response_tweets"].data

        usernames = st.session_state["response_tweets"].includes['users']

        data = []

        with st.expander("Expand fetched tweets"):
            for i, (tweet, user) in enumerate(zip(tweets, usernames)):
                data.append({
                    'author': user,
                    'tweet': tweet.text,
                    'include': False
                })
                st.write(f"**Author:** {user}")
                st.write(f"**Tweet:** {tweet.text}")
                st.write("---")

        # st.write("**NOTE:** Please uncheck the 'include' value for the tweet you don't want to include in the final result.")
        st.session_state['df'] = pd.DataFrame(data, columns=['author', 'tweet', 'include'])

    st.write("**NOTE:** Please uncheck the 'include' value for the tweet you don't want to include in the final result.")
    updated_df = st.experimental_data_editor(st.session_state['df'], use_container_width=True)

    # Drop rows where 'include' is False
    # final_df = updated_df.drop(updated_df[updated_df['include'] == False].index)

    # st.dataframe(updated_df,use_container_width=True)

    # Cache the conversion to prevent computation on every rerun
    @st.cache_data
    def convert_df(df):
        # Drop any unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.drop('include', axis=1)
        return df.to_csv(index=False).encode('utf-8')

    # csv = convert_df(final_df)

    # if (st.button("Save locally")):

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear file contents",use_container_width=True):
            open(st.session_state["file_path"], 'w').close()
    with col2:
        if st.button("Delete file",use_container_width=True):
            os.remove(f"{st.session_state['file_path']}")

    def update_file(df):
        # Write data to file
        try:
            fr = None  # Define fr with a default value
            with open(st.session_state["file_path"], 'a', encoding='utf-8-sig') as f:
                for index, row in df.iterrows():
                    if row['include']:
                        # st.success(row['author'])
                        if (row['author'] not in st.session_state["duplicates"]):
                            st.session_state["duplicates"].append(f"{row['author']}")
                            user = row['author']
                            tweet = row['tweet']
                            # Remove emojis
                            tweet = re.sub(r'\p{Emoji}', '', tweet)
                            # Remove newline characters
                            tweet = tweet.replace('\n', '')
                            f.write(f"{user}@\n{tweet}\n")
                        else:
                            st.warning("Entry duplicated, ignoring it.")
                    else:
                        with open(st.session_state["file_path"], 'r', encoding='utf-8-sig') as fr:
                            lines = fr.readlines()
                        tweet_lines = [i for i in range(len(lines)) if f"{row['author']}@" in lines[i]]
                        if tweet_lines:
                            lines.pop(tweet_lines[0])
                            if tweet_lines[0] < len(lines):
                                lines.pop(tweet_lines[0])
                            with open(st.session_state["file_path"], 'w', encoding='utf-8-sig') as f_sec:
                                f_sec.writelines(lines)
                                f_sec.close()

            # Close the file objects (f and fr) outside the loop
            if fr is not None:
                fr.close()
            f.close()
            st.success("Tweets file saved successfully!")
        except Exception as e:
            st.error(f"Error saving tweets file: {e}")

    update_file(updated_df)


        # st.download_button(
        #     label="Download results as CSV",
        #     data=csv,
        #     file_name='tweets.csv',
        #     mime='text/csv',
        # )

else:
    switch_page("Search Tweets")