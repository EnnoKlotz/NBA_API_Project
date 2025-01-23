from nba_api_functions import nba_playerid_by_season
from nba_api_functions import get_player_experience
from nba_api_functions import get_home_and_away_games
from nba_api_functions import get_player_team_data
import pandas as pd
import os 

# Setting working directory 
new_dir = "/Users/ennok./Documents/GitHub/NBA_API_Project" 
os.chdir(new_dir)

seasons_of_interest = ["2023-24", "2022-23", "2021-22", "2020-21", "2019-20", "2018-19", "2017-18", "2016-17", "2015-16"]

#Calling the player_id function 
player_ids = nba_playerid_by_season(season='2023-24', output_csv='nba_players_2023_24.csv')




player_experience = get_player_experience(player_ids, seasons_of_interest)

#calling the home & away games function 
# home_games_df, away_games_df = get_home_and_away_games(
#     player_ids, 
#     save_csv=True, 
#     home_csv="all_home_games.csv", 
#     away_csv="all_away_games.csv"
#)

