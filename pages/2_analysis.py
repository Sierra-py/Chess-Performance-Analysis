import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import analysis_report
from session_state import init_session_state
import base64

init_session_state()

st.set_page_config(layout="wide", page_title="Chess Analysis", initial_sidebar_state="collapsed")

#bg image

def get_base64_image(image_path):
    """Convert local image to base64 string"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_background_image(image_path):
    """Set background image with overlay"""
    try:
        img_base64 = get_base64_image(image_path)
        
        st.markdown(f"""
            <style>
            /* Main app background with image */
            .stApp {{
                background: linear-gradient(rgba(13, 17, 23, 0.85), rgba(13, 17, 23, 0.85)),
                            url("data:image/png;base64,{img_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            /* Sidebar background with image */
            section[data-testid="stSidebar"] {{
                background: linear-gradient(rgba(13, 17, 23, 0.95), rgba(13, 17, 23, 0.95)),
                            url("data:image/png;base64,{img_base64}");
                background-size: cover;
                background-position: center;
            }}
            
            /* Additional styling for better visibility */
            div[data-testid="stMetric"] {{
                background-color: rgba(22, 27, 34, 0.7);
                backdrop-filter: blur(10px);
                padding: 15px;
                border-radius: 8px;
                border: 1px solid rgba(48, 54, 61, 0.7);
            }}
            
            div[data-testid="stPlotlyChart"] {{
                background-color: rgba(22, 27, 34, 0.7);
                backdrop-filter: blur(8px);
                border-radius: 8px;
                padding: 10px;
                border: 1px solid rgba(48, 54, 61, 0.7);
            }}
            
            div[data-testid="stDataFrame"] {{
                background-color: rgba(22, 27, 34, 0.7);
                backdrop-filter: blur(10px);
                border-radius: 8px;
                border: 1px solid rgba(48, 54, 61, 0.7);
            }}
            /* Plot containers - more translucent */
            div[data-testid="stPlotlyChart"] {{
                background-color: rgba(22, 27, 34, 0.7);
                backdrop-filter: blur(5px);
                border-radius: 8px;
                padding: 10px;
                border: 1px solid rgba(48, 54, 61, 0.7);
            }}
            
            /* Dataframe containers - more translucent */
            div[data-testid="stDataFrame"] {{
                background-color: rgba(22, 27, 34, 0.7);
                backdrop-filter: blur(8px);
                border-radius: 8px;
                border: 1px solid rgba(48, 54, 61, 0.7);
            }}
            
            /* Make dataframe cells also translucent */
            div[data-testid="stDataFrame"] table {{
                background-color: transparent !important;
            }}
            
            div[data-testid="stDataFrame"] tbody tr {{
                background-color: rgba(22, 27, 34, 0.7) !important;
            }}
            
            div[data-testid="stDataFrame"] tbody tr:hover {{
                background-color: rgba(48, 54, 61, 0.7) !important;
            }}
            
            div[data-testid="stDataFrame"] thead {{
                background-color: rgba(22, 27, 34, 0.7) !important;
            }}
                        
            h1 {{
                color: #ffffff;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            }}
            
            h3 {{
                color: #c9d1d9;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
            }}
            </style>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error(f"Image file '{image_path}' not found! Make sure it's in the same folder as your script.")

set_background_image("bg.jpg")  

##############

# If data is not fetched
if st.session_state.all_games_list is None:
    st.warning("Please fetch data first.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

# Welcome message
st.title(f"Welcome, {st.session_state.username}", width='stretch', text_alignment="center")

# Create a dictionary to map the dropdown labels to the actual dataframes in session state
game_type_options = {
    "All Games": st.session_state.all_games,
    "Rapid": st.session_state.rapid_games,
    "Blitz": st.session_state.blitz_games,
    "Bullet": st.session_state.bullet_games,
    "Daily": st.session_state.daily_games
}

# Use a selectbox to let the user choose
selected_type = st.selectbox("Select Game Type for Analysis:", list(game_type_options.keys()), index=1)

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
    
    analysis_report(df, selected_type, st.session_state.username)

    col1, col2 = st.columns([3,2])
    with col1:
        # First chart.

        fig1 = go.Figure()

        fig1.add_trace(
            go.Scatter(
                x=df["Game Number:"],
                y=df["My Elo:"],
                mode="lines+markers",
                name="Elo",
                line=dict(color="#f39c12"),
                hovertemplate='<b>Game %{x}</b><br>Rating: %{y}<extra></extra>'
            )
        )
        
        
        fig1.add_hline(y=df["My Elo:"].min(), line_dash="dash", line_color="red", annotation={'text':'Lowest', 'x':0.1, 'arrowhead': 2})
        fig1.add_hline(y=df["My Elo:"].max(), line_dash="dash", line_color="green", annotation={'text':'Highest', 'x':0.1, 'arrowhead': 2})
        fig1.add_hline(y=df["My Elo:"].mean(), line_dash="dash", line_color="grey", annotation={'text':'Average', 'x':0.1, 'arrowhead': 2})

        max_index = df["My Elo:"].idxmax()
        min_index = df["My Elo:"].idxmin()

        fig1.add_annotation(
            x=df["Game Number:"][max_index],
            y=df["My Elo:"][max_index],
            text=f"Peak Elo: {df['My Elo:'][max_index]}",
            showarrow=True,
            arrowhead=5,
            font=dict(color="green")
        )

        fig1.add_annotation(
            x=df["Game Number:"][min_index],
            y=df["My Elo:"][min_index],
            text=f"Lowest Elo: {df['My Elo:'][min_index]}",
            showarrow=True,
            arrowhead=2,
            font=dict(color="red"),
            ax=10,
            ay=50
        )

        fig1.update_layout(
            title="Rating for this month",
            xaxis_title=f"Game Number ({len(df)} games)",
            yaxis_title="Elo",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                    showgrid=False, 
                    gridcolor="#464646",
                    color='#FAF9F6',
                    title='Game Number',
                    title_font=dict(size=18)
                ),
            yaxis=dict(
                    showgrid=True, 
                    gridcolor='#21262d',
                    color='#FAF9F6',
                    title='ELO Rating',
                    title_font=dict(size=18, color="#FAF9F6")
                ),
                showlegend=False,
                hovermode='x unified'
        )
        st.plotly_chart(fig1, use_container_width=True, key='trend')

        # Progressive win rate chart
        st.markdown("### Win Rate Progression")
        fig_wr = go.Figure()
        fig_wr.add_trace(go.Scatter(
            x=df['Game Number:'],
            y=df['running_win_rate'],
            mode='lines',
            line=dict(color='#3fb950', width=2.5),
            fill='tozeroy',
            fillcolor='rgba(63, 185, 80, 0.5)',
            hovertemplate='<b>Game %{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>'
        ))
        fig_wr.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=10, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='#21262d',
                color='#FAF9F6',
                title='Game Number',
                title_font=dict(size=18)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#21262d',
                color='#FAF9F6',
                title='Win Rate %',
                title_font=dict(size=18),
                range=[0, 100]  # Fixed Y-axis range
            ),
            showlegend=False,
            hovermode='x unified'
        )
        st.plotly_chart(fig_wr, use_container_width=True, key="winrate")

    
    with col2:


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
            yaxis_title="Games",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                    showgrid=False, 
                    gridcolor="#464646",
                    color='#FAF9F6',
                    title='Termination Type',
                    title_font=dict(size=18)
                ),
            yaxis=dict(
                    showgrid=True, 
                    gridcolor='#21262d',
                    color='#FAF9F6',
                    title='Games',
                    title_font=dict(size=18, color="#FAF9F6")
                ),

        )   
        st.plotly_chart(fig3)

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
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Number of Wins",
            template="plotly_dark",            
        )


        st.plotly_chart(fig4, key=4)
