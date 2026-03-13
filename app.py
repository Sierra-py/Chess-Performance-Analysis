# Import Required libraries.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import requests
import regex as re
import streamlit as st
from utils import import_data, game_type, extract_games, extract_pgn_data
from session_state import init_session_state


init_session_state()
# st.set_page_config(layout="wide")
st.set_page_config(layout="wide", page_title="Chess Analysis", initial_sidebar_state="collapsed")




if st.session_state.go_to_data:
    st.session_state.go_to_data = False
    st.switch_page("pages/1_Data.py")
    
# Getting information of user 
username = st.text_input("Enter your Chess.com\'s username: ")
year = st.text_input('Enter Year: ')
month = st.text_input('Enter month number in two digits: ')
st.session_state.username = username

# Button to fetch Data by calling API
button = st.button("Fetch data", type='primary', shortcut='Enter')
if button:
    if not username or not year or not month:
        st.write("Please fill all fields.")
    else:
        result = import_data(username, year, month)
        if not result:
            st.error("Invalid Username, Year, or month.")
            st.stop()
        st.success("Data Fetched Successfully.")

        data = result.json()

        st.session_state.all_games_list = data['games']
        all_games_list =  st.session_state.all_games_list # A list that contains values of games key in the data dict.
        if len(all_games_list) > 0:
            st.write(f'Data found for {len(all_games_list)} games.\n\n')

            bullet_games_list, blitz_games_list, rapid_games_list, daily_games_list, other_games_list = game_type(st.session_state.all_games_list)
            st.session_state.rapid_games_list = rapid_games_list
            st.session_state.blitz_games_list = blitz_games_list
            st.session_state.bullet_games_list = bullet_games_list
            st.session_state.daily_games_list = daily_games_list




        else:
            st.write(f'No games found for this month.')
            st.stop()

if st.session_state.all_games_list is not None:
    if st.button("Go to Data →"):
        st.switch_page("pages/1_data.py")
