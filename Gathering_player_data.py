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

unique_playerids = list(unique_playerids)

player_ids_df = pd.DataFrame(unique_playerids, columns=['Player ID'])

#player_ids_df.to_csv("all_players_from_2015-2024.csv")


player_team_data = pd.DataFrame(columns=['Player ID', 'Season', 'Team ID'])

# Getting player_id, season_id, and team_id
for i in seasons_of_interest[:2]:  
    # Getting the players for the given season 
    players = nba_playerid_by_season(season= i, output_to_csv= False)
    # Converting them to strings
    str_players = [str(x) for x in players]
    
    for j in str_players[:4]:  
        # Getting player team data
        team_df = get_player_team_data(player_ids=[j], save_to_csv=False)
        # Adding team data to a csv
        player_team_data = pd.concat([player_team_data, team_df], ignore_index= True)
        
player_team_data = player_team_data[['Player ID', 'Season ID', 'Team ID', 'Team Abbreviation']]

