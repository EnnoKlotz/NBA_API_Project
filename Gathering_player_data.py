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

#Calling the player_id function for all seasons of interest
list_of_ids = []
for i in seasons_of_interest: 
    player_ids = nba_playerid_by_season(season=i, output_to_csv=False)
    #Make one big list with all data 
    list_of_ids.extend(player_ids)

# Only keep unique player_ids 
unique_playerids = set(list_of_ids)





#player_experience = get_player_experience(player_ids, seasons_of_interest)

#calling the home & away games function 
# home_games_df, away_games_df = get_home_and_away_games(
#     player_ids, 
#     save_csv=True, 
#     home_csv="all_home_games.csv", 
#     away_csv="all_away_games.csv"
#)

