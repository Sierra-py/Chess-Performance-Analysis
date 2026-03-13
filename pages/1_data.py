import streamlit as st
from utils import extract_games, extract_pgn_data 
from session_state import init_session_state


init_session_state()

# pages/1_Data.py - already handles this
if st.session_state.all_games_list is None:
    st.warning("Please fetch data first.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

# Button to extract game data of different formats into dataframe
if st.button("Extract All games.", shortcut='Enter', type='primary'):

    all_games = extract_games(st.session_state.all_games_list, st.session_state.username)
    st.session_state.all_games = all_games
    st.write(f'Total {len(all_games)} games extracted')

    rapid_games = extract_games(st.session_state.rapid_games_list, st.session_state.username)
    st.session_state.rapid_games = rapid_games
    st.write(f'{len(rapid_games)} rapid games')

    blitz_games = extract_games(st.session_state.blitz_games_list, st.session_state.username)
    st.session_state.blitz_games = blitz_games
    st.write(f'{len(blitz_games)} blitz games')

    daily_games = extract_games(st.session_state.daily_games_list, st.session_state.username)
    st.session_state.daily_games = daily_games
    st.write(f'{len(daily_games)} daily games')

    bullet_games = extract_games(st.session_state.bullet_games_list, st.session_state.username)
    st.session_state.bullet_games = bullet_games
    st.write(f'{len(bullet_games)} bullet games')

if st.session_state.all_games is not None:
    if st.button("Go to Analysis →"):
        st.switch_page("pages/2_analysis.py")


# Session state to track which df to show
if 'selected_df' not in st.session_state:
    st.session_state.selected_df = None

# Buttons side by side
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("All Games"):
        st.session_state.selected_df = 'all'
with col2:
    if st.button("Rapid"):
        st.session_state.selected_df = 'rapid'
with col3:
    if st.button("Bullet"):
        st.session_state.selected_df = 'bullet'
with col4:
    if st.button("Blitz"):
        st.session_state.selected_df = 'blitz'
with col5:
    if st.button("Daily"):
        st.session_state.selected_df = 'daily'

# Dataframe renders full width OUTSIDE columns
df_map = {
    'all': st.session_state.all_games,
    'rapid': st.session_state.rapid_games,
    'bullet': st.session_state.bullet_games,
    'blitz': st.session_state.blitz_games,
    'daily': st.session_state.daily_games
}

if st.session_state.selected_df is not None:
    df = df_map[st.session_state.selected_df]
    if df is not None:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No games of this type found.")


