import streamlit as st
import json
from streamlit_extras.switch_page_button import switch_page
st.title("Settings")

# load existing JSON file or create new file if it doesn't exist
try:
    with open('settings.json', 'r') as file:
            st.write("Settings found.")
            data = json.load(file)
            
except (FileNotFoundError, json.JSONDecodeError):
            st.write("Settings not found")

st.write("---")

try:
    filepath = st.text_input("Enter the file path: ",value=data['filepath'])
except:
    filepath = st.text_input("Enter the file path: ")

try:
    hashtag_value = st.text_input("Please enter the hashtag you wanna search (without #):",value=data['hashtag'])
except:
    hashtag_value = st.text_input("Please enter the hashtag you wanna search (without #):")

try:
    hours_input = st.number_input("Fetch the tweets for last (hours only):",value=int(data['hours_range']),min_value=1,max_value=168)
except:
    hours_input = st.number_input("Fetch the tweets for last (hours only):",value=24,min_value=1,max_value=168)

if st.button("Save") and hashtag_value and filepath and hours_input:
    # load existing JSON file or create new file if it doesn't exist
    try:
        with open('settings.json', 'r') as file:
                data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
            data = {}

    # update JSON data with hashtag and path value
    data['hashtag'] = hashtag_value
    data['filepath'] = filepath
    data['hours_range'] = hours_input

    # write updated JSON data to file
    with open("settings.json", 'w') as file:
        json.dump(data, file, indent=4)
        if "file_path" in st.session_state:
            del st.session_state["file_path"]
        if "hashtag" in st.session_state:
            del st.session_state["hashtag"]
        if "hours" in st.session_state:
            del st.session_state["hours"]
        st.success("JSON data written to file successfully. Go to Search Tweets page.")