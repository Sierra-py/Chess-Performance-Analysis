# Chess Performance Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chess-performance-analysis.streamlit.app)

This project is the my learning journey of basics Data Analysis, learning the libraries like pandas, numpy, and matplotlib.

Analyzes chess.com game data to find performance patterns and insights.

## Features
- Fetches games via Chess.com API
- Separates analysis by time format (rapid, blitz, bullet, daily)
- Analyzes win rates, streaks, and performance vs opponent strength
- Visualizes rating progression over time

## Requirements
- Python 3.7+
- pandas
- numpy
- matplotlib
- requests

## Usage
1. Run the Jupyter notebook
2. Enter your chess.com username when prompted (It's case sensitive)
3. Specify the year and month to analyze (format: yyyy for year and mm for month)
4. View your performance insights and visualizations

## Key Findings Example
- Win rate by color (White vs Black)
- Performance against different opponent strengths
- Rating progression and streak analysis

## A Sample of Analysis

![Sample of analysis](<Sample of analysis.png>)
![Sample of visualization](<Sample of visualization.png>)

---

## Streamlit Web App

The analysis has also been converted into a deployed multipage Streamlit web app with interactive Plotly charts. [Link to App](https://chess-performance-analysis.streamlit.app/)

### Additional Features
- Multipage layout — Home, Data, and Analysis pages
- Interactive Plotly charts for all visualizations
- Game type selector — analyze Rapid, Blitz, Bullet, or Daily games separately
- Identifies your most successful openings
- Tracks Elo trends with peak and lowest rating annotations

### Additional Requirements
- streamlit
- plotly
- regex

### Installation

```bash
git clone https://github.com/Sierra-py/Chess-Performance-Analysis.git
cd Chess-Performance-Analysis
pip install -r requirements.txt
streamlit run app.py
```

### App Usage

**Page 1 — Home**
- Enter your Chess.com username (case sensitive)
- Enter the year and month to analyze
- Click Fetch Data

**Page 2 — Data**
- Click Extract All Games to process your game data
- View dataframes for each game format — All, Rapid, Blitz, Bullet, Daily

**Page 3 — Analysis**
- Select a game format to analyze
- View performance metrics and interactive charts

### Project Structure

```
Chess-Performance-Analysis/
│
├── app.py                  # Home page — input and data fetch
├── utils.py                # All data processing functions
├── session_state.py        # Session state initialization
├── pages/
│   ├── 1_Data.py           # Game extraction and dataframe display
│   └── 2_Analysis.py       # Analysis metrics and Plotly charts
└── requirements.txt
```