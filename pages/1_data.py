import streamlit as st
from utils import extract_games, extract_pgn_data 
from session_state import init_session_state

st.set_page_config(layout="wide")

init_session_state()

# pages/1_Data.py - already handles this
if st.session_state.all_games_list is None:
    st.warning("Please fetch data first.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

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


