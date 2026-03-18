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
st.set_page_config(layout="centered", page_title="Chess Analysis", initial_sidebar_state="collapsed")


# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Text Input fields */
    div[data-testid="stTextInput"] input {
        background-color: rgba(22, 27, 34, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(76, 175, 80, 0.5) !important;
        border-radius: 6px !important;
        padding: 10px !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        background-color: rgba(22, 27, 34, 0.8) !important;
        border: 1px solid rgba(88, 166, 255, 0.8) !important;
        box-shadow: 0 0 0 1px rgba(88, 166, 255, 0.5) !important;
    }
    
    /* Selectbox (dropdown) fields */
    div[data-testid="stSelectbox"] > div > div {
        background-color: rgba(22, 27, 34, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(76, 175, 80, 0.5) !important;
        border-radius: 6px !important;
    }
    
    div[data-testid="stSelectbox"] > div > div:hover {
        border: 1px solid rgba(76, 175, 80, 0.5) !important;
    }
    
    /* Dropdown menu options */
    div[role="listbox"] {
        background-color: rgba(22, 27, 34, 0.8) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    div[role="option"] {
        color: #ffffff !important;
    }
    
    div[role="option"]:hover {
        border: 1px solid rgba(76, 175, 80, 0.5) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: rgba(22, 27, 34, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(76, 175, 80, 0.5) !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stButton > button:hover {
        background-color: rgba(22, 27, 34, 0.8) !important;
        border: 1px solid rgba(76, 175, 80, 0.5) !important;
    }
    
    /* Labels for input fields */
    label {
        color: #c9d1d9 !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)


if st.session_state.go_to_data:
    st.session_state.go_to_data = False
    st.switch_page("pages/1_Data.py")
    
# Getting information of user 
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"]

username = st.text_input("Enter your Chess.com\'s username: ", placeholder='Enter Your Username.')
year = st.text_input('Enter Year: ', placeholder='Enter Year (YYYY)')
month = st.selectbox(label="Select Month", options=months, index=None, placeholder='Select a Month')

st.session_state.username = username
st.session_state.year = year
st.session_state.month = month

# Button to fetch Data by calling API
button = st.button("Fetch data", type='primary')
if button:
    if not username or not year or not month:
        st.write("Please fill all fields.")
    else:
        result = import_data(username, year, month)
        if not result:
            st.error("Invalid Username, Year, or month.")
            st.stop()
        st.spinner("Data Fetched Successfully.")

        data = result.json()

        st.session_state.all_games_list = data['games']
        if len(st.session_state.all_games_list) > 0:
            st.write(f'You played {len(st.session_state.all_games_list)} games in {st.session_state.month} {st.session_state.year}.\n\n')

            bullet_games_list, blitz_games_list, rapid_games_list, daily_games_list, other_games_list = game_type(st.session_state.all_games_list)
            st.session_state.rapid_games_list = rapid_games_list
            st.session_state.blitz_games_list = blitz_games_list
            st.session_state.bullet_games_list = bullet_games_list
            st.session_state.daily_games_list = daily_games_list

            # if st.button("Extract All games.", shortcut='Enter', type='primary'):

            all_games = extract_games(st.session_state.all_games_list, st.session_state.username)
            st.session_state.all_games = all_games

            rapid_games = extract_games(st.session_state.rapid_games_list, st.session_state.username)
            st.session_state.rapid_games = rapid_games

            blitz_games = extract_games(st.session_state.blitz_games_list, st.session_state.username)
            st.session_state.blitz_games = blitz_games

            daily_games = extract_games(st.session_state.daily_games_list, st.session_state.username)
            st.session_state.daily_games = daily_games

            bullet_games = extract_games(st.session_state.bullet_games_list, st.session_state.username)
            st.session_state.bullet_games = bullet_games
            data={'Total Games' : len(all_games),
                               'Rapid Games' : len(rapid_games),
                               'Blitz Games' : len(blitz_games),
                               'Bullet Games' : len(bullet_games),
                               'Daily Games' : len(daily_games)}
            data = pd.Series(data= data.values(), index = data.keys(), name='No of Games')
            data.index.set_names(['Game Type'], inplace=True)
            st.table(data=data,  width='content')

            # Session state to track which df to show
            if 'selected_df' not in st.session_state:
                st.session_state.selected_df = None




        else:
            st.write(f'No games found for this month.')
            st.stop()
if st.session_state.all_games is not None:
    if st.button("Go to Analysis →", icon='📈'):
        st.switch_page("pages/2_analysis.py")

if st.session_state.all_games_list is not None:
    if st.button("Go to Data →", icon='📊'):
        st.switch_page("pages/1_data.py")
