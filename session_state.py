import streamlit as st

def init_session_state():
    defaults = {
        'all_games_list': None,
        'rapid_games_list': None,
        'blitz_games_list': None,
        'bullet_games_list': None,
        'daily_games_list': None,
        'all_games': None,
        'rapid_games': None,
        'blitz_games': None,
        'bullet_games': None,
        'daily_games': None,
        'username': None,
        'go_to_data': False,
        'selected_df': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value