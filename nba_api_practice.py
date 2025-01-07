
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
import time
import pandas as pd

# Get a list of all active NBA players
active_players = players.get_active_players()

# # Convert active_players variable to a DataFrame for easier export
# active_players_df = pd.DataFrame(active_players)

# # Write a CSV file that contains all active players
# active_players_df.to_csv('active_nba_players.csv', index=False)

# print("CSV file created: active_nba_players.csv")

# Get a list of all active NBA players season IDs 
player_ids = [player['id'] for player in active_players]

#Ensuring no player data was lost
print(f" Number of player IDs: {len(player_ids)}")



# Initializing an empty dataframe to store the player data
player_dict = {}

# Iterate over each player ID
for i in player_ids:
    # Get current player info
    current_player_info = commonplayerinfo.CommonPlayerInfo(player_id=i)
    
    # Extract the dataframe of player info
    player_info_df = current_player_info.get_data_frames()[0]
    
    #Create a temp dictionary that has both player ID and experance
    temp_player_dict = dict(zip(player_info_df['PERSON_ID'], player_info_df['SEASON_EXP']))

    # If the dictionary is empty do not append 
    if len(player_dict) == 0:
        player_dict = temp_player_dict
    else:
        player_dict.update(temp_player_dict)
    
    print(f"Wokring on player: {i}")
    # Pause for 2 seconds before the next iteration
    time.sleep(2)



import csv
with open('active_player_experance.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Player ID', 'Season Experience'])
    for key, value in player_dict.items():
        writer.writerow([key, value])

print("Exported player experance data as a csv")
