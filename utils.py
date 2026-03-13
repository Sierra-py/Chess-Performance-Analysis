import pandas as pd
import numpy as np
import requests
import regex as re
import streamlit as st

# Function to call Chess.com's API and fetch data
@st.cache_data
def import_data(username, year, month):

    header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0'
    }
    response = requests.get(f"https://api.chess.com/pub/player/{username}/games/{year}/{month}", headers= header)
    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        return None
    else:
        return None

# Function to separate data into game types.
def game_type(all_games_list):
    bullet_games_list = []
    blitz_games_list = []
    rapid_games_list = []
    daily_games_list = []
    other_games_list = []
    for i in range(len(all_games_list)):

        if ('TimeControl "600"' in all_games_list[i]['pgn'] or 
            'TimeControl "900+10"' in all_games_list[i]['pgn'] or 
            'TimeControl "1800"' in all_games_list[i]['pgn'] or 
            'TimeControl "600+5"' in all_games_list[i]['pgn'] or 
            'TimeControl "1200"' in all_games_list[i]['pgn'] or 
            'TimeControl "3600"' in all_games_list[i]['pgn']):

            rapid_games_list.append(all_games_list[i])

        elif ('TimeControl "180"' in all_games_list[i]['pgn'] or 
              'TimeControl "180+2"' in all_games_list[i]['pgn'] or
              'TimeControl "300"' in all_games_list[i]['pgn'] or 
              'TimeControl "300+2"' in all_games_list[i]['pgn'] or 
              'TimeControl "300+5"' in all_games_list[i]['pgn']):

            blitz_games_list.append(all_games_list[i])

        elif ('TimeControl "60"' in all_games_list[i]['pgn'] or 
              'TimeControl "60+1"' in all_games_list[i]['pgn'] or 
              'TimeControl "120+1"' in all_games_list[i]['pgn']):

            bullet_games_list.append(all_games_list[i])

        elif 'TimeControl "1/' in all_games_list[i]['pgn']:

            daily_games_list.append(all_games_list[i])

        else:
            other_games_list.append(all_games_list[i])

    return bullet_games_list, blitz_games_list, rapid_games_list, daily_games_list, other_games_list

# Function to extract game info from game pgn file.
def extract_pgn_data(pgn):
    list_pgn = pgn.split('\n')
    game_info = {}
    

    for line in list_pgn:
        if 'White ' in line:
            White = line.split('"')[1]
            game_info['White username:'] = White
        elif 'Black ' in line:
            Black = line.split('"')[1]
            game_info['Black username:'] = Black
        elif 'WhiteElo' in line:
            WhiteElo = line.split('"')[1]
            game_info['White\'s Elo:'] = WhiteElo
        elif 'BlackElo' in line:
            BlackElo = line.split('"')[1]
            game_info['Black\'s Elo:'] = BlackElo
        elif 'Result ' in line:
            result = line.split('"')[1]
            game_info['Result:'] = result
        elif 'Date' in line:
            Date = line.split('"')[1]
            game_info['Date:'] = Date
        elif 'ECOUrl' in line and 'EndDate' not in line and 'UTCDate' not in line:
            Opening_url = line.split('"')[1]
            Opening = Opening_url.split('/')[4]
            Opening_simplified = re.split(r'-\d+', Opening)[0]
            game_info['Opening:'] = Opening_simplified
        elif 'Termination' in line:
            Termination = line.split('"')[1]
            Termination = Termination.split(" ")[-1]
            game_info['Termination:'] = Termination
    
    return game_info

# Function to make a dataframe from gamelist.
def extract_games(games_list, username, game_type = ''):
    games = []
    if games_list is  None:
        return None
    for i in range(len(games_list)):
        game_pgn = games_list[i]['pgn']
        games.append(extract_pgn_data(game_pgn))
    if not games:
        return games
    df = pd.DataFrame(games)
    df['My color:'] = np.where(df['White username:'] == username, 'White', 'Black')

    df['My result:'] = np.where(
        df['Result:'] == '1/2-1/2', 'Draw', 
        np.where(
            ((df['Result:'] == '1-0') & (df['My color:'] == 'White')) | 
            ((df['Result:'] == '0-1') & (df['My color:'] == 'Black')), 
            'Win', 'Loss'))
    # Extract your rating and opponent's rating
    df['My Elo:'] = np.where(df['White username:'] == username, df['White\'s Elo:'], df['Black\'s Elo:'])
    df['Opponent\'s Elo:'] = np.where(df['Black username:'] == username, df['White\'s Elo:'], df['Black\'s Elo:'])

    # Convert ratings to integers
    df['My Elo:'] = df['My Elo:'].astype('int64')
    df['White\'s Elo:'] = df['White\'s Elo:'].astype('int64')
    df['Black\'s Elo:'] = df['Black\'s Elo:'].astype('int64')
    df['Opponent\'s Elo:'] = df['Opponent\'s Elo:'].astype('int64')

    # Extract opponent's username
    df['Opponent\'s username:'] = np.where(df['My color:'] == 'White', df['Black username:'], df['White username:'])

    # Calculate rating difference 
    df['Elo Difference:'] = df['Opponent\'s Elo:'] - df['My Elo:'] # +ve number means opponent's rating is higher than you, -ve number means opponent's rating is lower than you

    # Create separate DataFrames for different results
    Wins = df[df['My result:'] == 'Win']
    Loss = df[df['My result:'] == 'Loss']
    Draw = df[df['My result:'] == 'Draw']

    # Add game tracking columns
    df['Game Number:'] = range(1, len(df)+1)
    df['cumulative_wins'] = (df['My result:'] == 'Win').cumsum()
    df['running_win_rate'] = (df['cumulative_wins'] / df['Game Number:'] * 100)

    df = df[[
    "Date:", 
    "Game Number:", 
    "Opponent's username:", 
    "Opponent's Elo:", 
    "My Elo:", 
    "Elo Difference:",
    "My color:", 
    "My result:", 
    "Opening:", 
    "Termination:", 
    "Result:", 
    "cumulative_wins", 
    "running_win_rate"
    ]]
    return df

def analysis_report(df, username):

    Wins = df[df['My result:'] == 'Win']
    Loss = df[df['My result:'] == 'Loss']
    Draw = df[df['My result:'] == 'Draw']

    st.write(f"=== Hello, {username} ===\n")
    st.write(f"Number of games played in the month: {df['My Elo:'].count()}\n")
    st.write(f"Your Average Elo of the month is: {df['My Elo:'].mean().__trunc__()}\n")
    st.write(f"Your Max Elo of the month is: {df['My Elo:'].max()}\n")
    st.write(f"Your Min Elo of the month is: {df['My Elo:'].min()}\n")


    idx = Wins["Opponent\'s Elo:"].idxmax()
    st.write(f"Your Best Win was against user: {Wins['Opponent\'s username:'][idx]} with the Elo of :{Wins['Opponent\'s Elo:'][idx]}\n")
    st.write(f"Rating change over this month: {df['My Elo:'].iloc[-1] - df['My Elo:'].iloc[0]}\n")

    st.write(f"Your Win rate: {len(Wins)/len(df):.2%}\n")

    color = df.groupby('My color:')['My result:'].apply(lambda x: (x == 'Win').mean())
    st.write(f'Win Rate with different colors: ')
    st.dataframe(color*100, width="content")

    df["Opponent\'s Strength:"] = pd.cut(df['Elo Difference:'], 
                                        bins=[-np.inf, -100, -20, 20, 100, np.inf], 
                                        labels=['Much Weaker', 'Weaker', 'Similar', 'Stronger', 'Much Stronger'])
    a = df.groupby("Opponent\'s Strength:", observed=True)['My result:'].apply(lambda x: (x =='Win').mean())


    st.write(f"Win Rate according to the opponent\'s strength: ")
    st.dataframe(a*100, width="content")




    # st.write(f"Longest Win streak: {max(win_streaks) if win_streaks else 0}")
    # st.write(f"Longest Loss streak: {max(loss_streaks) if loss_streaks else 0}")
    # st.write(f"Longest Draw streak: {max(draw_streaks) if draw_streaks else 0}")
