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

#player_ids_df = pd.DataFrame(unique_playerids, columns=['Player ID'])
#player_ids_df.to_csv("all_players_from_2015-2024.csv")


player_team_data = pd.DataFrame(columns=['Player ID', 'Season', 'Team ID'])

# # Getting player_id, season_id, and team_id 
# for i in unique_playerids:  
#     # Getting player team data
#     team_df = get_player_team_data(player_ids=[i], save_to_csv=False)
#     # Adding team data to a csv
#     player_team_data = pd.concat([player_team_data, team_df], ignore_index= True)
# #Removing 2024-25 season
# player_team_data = player_team_data.loc[player_team_data['Season ID'] != '2024-25']       
# player_team_data = player_team_data[['Player ID', 'Season ID', 'Team ID', 'Team Abbreviation']]

# #Saving temp progress
# player_team_data.to_csv("player_team_data_temp_checj_point.csv", index= False)

#Intialize empty df
player_exper_data = pd.DataFrame(columns=['Player ID', 'Season ID', 'Experience'])
# Getting player experance 
for i in unique_playerids: 
    print(f"Working on player id: {i}")
    for j in seasons_of_interest:
        # Get current player experance
        current_player = get_player_experience(player_ids= [i], season_ids= [j], save_to_csv= False)
        player_exper_data = pd.concat([player_exper_data, current_player], ignore_index= True)
# Save progress        
player_exper_data.to_csv("experance_data_checkpoint.csv", index= False)

# Merging experance and team history 
#merged_df = pd.merge(player_team_data, player_exper_data, on=['Player ID', 'Season ID'], how='left')

#merged_df.to_csv("Player Team and Experance 2014-2024.csv", index= False)
#print("Player Team and Experance 2014-2024.csv has been printed!")





