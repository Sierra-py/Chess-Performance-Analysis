import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import analysis_report
from session_state import init_session_state


init_session_state()

# pages/1_Data.py - already handles this
if st.session_state.all_games_list is None:
    st.warning("Please fetch data first.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

# Create a dictionary to map the dropdown labels to the actual dataframes in session state
game_type_options = {
    "All Games": st.session_state.all_games,
    "Rapid": st.session_state.rapid_games,
    "Blitz": st.session_state.blitz_games,
    "Bullet": st.session_state.bullet_games,
    "Daily": st.session_state.daily_games
}

# Use a selectbox to let the user choose
selected_type = st.selectbox("Select Game Type for Analysis:", list(game_type_options.keys()))

# Get the selected dataframe based on the user's choice
df = game_type_options[selected_type]
if df is None or len(df) == 0:
    st.warning("No games for this type")

else:
    
    all_games = st.session_state.all_games
    
    rapid_games_list = st.session_state.rapid_games_list
    Wins = df[df['My result:'] == 'Win']
    Loss = df[df['My result:'] == 'Loss']
    Draw = df[df['My result:'] == 'Draw']

    analysis_report(df, st.session_state.username)
    # First chart.

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=df["Game Number:"],
            y=df["My Elo:"],
            mode="lines+markers",
            name="Elo",
            line=dict(color="#f39c12")
        )
    )

    fig1.add_hline(y=df["My Elo:"].min(), line_dash="dash", line_color="red")
    fig1.add_hline(y=df["My Elo:"].max(), line_dash="dash", line_color="green")
    fig1.add_hline(y=df["My Elo:"].mean(), line_dash="dash", line_color="black")

    max_index = df["My Elo:"].idxmax()
    min_index = df["My Elo:"].idxmin()

    fig1.add_annotation(
        x=df["Game Number:"][max_index],
        y=df["My Elo:"][max_index],
        text=f"Peak Elo: {df['My Elo:'][max_index]}",
        showarrow=True,
        arrowhead=2,
        font=dict(color="green")
    )

    fig1.add_annotation(
        x=df["Game Number:"][min_index],
        y=df["My Elo:"][min_index],
        text=f"Lowest Elo: {df['My Elo:'][min_index]}",
        showarrow=True,
        arrowhead=2,
        font=dict(color="red")
    )

    fig1.update_layout(
        title="Rating for this month",
        xaxis_title=f"Game Number ({len(df)} games)",
        yaxis_title="Elo",
        template="plotly_dark"
    )

    # Second Chart.

    col_func = df.groupby("My color:")["My result:"].apply(lambda x: (x == "Win").mean())

    fig2 = go.Figure(
        data=[
            go.Pie(
                labels=col_func.index,
                values=col_func.values,
                hole=0.2
            )
        ]
    )

    fig2.update_layout(
        title="% of Wins with Different Color",
        template="plotly_dark"
    )

    # Third Chart.


    termination_count = df.groupby(["Termination:"]).size()
    significant = termination_count[termination_count >= 5].index

    filtered_df = df[df["Termination:"].isin(significant)]
    filtered_df = filtered_df.groupby(["Termination:", "My result:"]).size().unstack(fill_value=0)

    fig3 = go.Figure()

    for col in filtered_df.columns:
        fig3.add_bar(
            x=filtered_df.index,
            y=filtered_df[col],
            name=col
        )

    fig3.update_layout(
        barmode="group",
        title="Termination Type Analysis",
        template="plotly_dark",
        xaxis_title="Termination Type",
        yaxis_title="Games"
    )   
    # Fourth Chart.

    a = Wins.groupby("Opening:").size()
    frequent_openings = a.nlargest(3)

    fig4 = go.Figure(
        go.Bar(
            x=frequent_openings.values,
            y=frequent_openings.index,
            orientation="h",
            marker_color="#f39c12"
        )
    )

    fig4.update_layout(
        title="Top 3 Most Successful Openings",
        xaxis_title="Number of Wins",
        template="plotly_dark"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)