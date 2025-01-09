
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd
import time
import csv


def export_active_nba_players(output_csv='active_nba_players.csv'):
    """
    Fetches the list of all active NBA players, saves it as a CSV file, 
    and returns a list of their player IDs.

    Parameters:
        output_csv (str): File name for the output CSV. Default is 'active_nba_players.csv'.

    Returns:
        list: A list of player IDs for all active NBA players.
    """
    # Get a list of all active NBA players
    active_players = players.get_active_players()

    # Convert the active_players variable to a DataFrame for easier export
    active_players_df = pd.DataFrame(active_players)

    # Write a CSV file that contains all active players
    active_players_df.to_csv(output_csv, index=False)
    print(f"CSV file created: {output_csv}")

    # Get a list of all active NBA players' season IDs
    player_ids = [player['id'] for player in active_players]

    # Ensuring no player data was lost
    print(f"Number of player IDs: {len(player_ids)}")

    return player_ids

#Calling the player_id function 
player_ids = export_active_nba_players(output_csv='nba_active_players.csv')
print(player_ids)


def get_player_experience(player_ids, output_csv='active_player_experience.csv'):
    """
    Fetch the experience data (SEASON_EXP) for a list of NBA players and save it as a CSV.

    Parameters:
        player_ids (list): List of player IDs to process.
        output_csv (str): File name for the output CSV. Default is 'active_player_experience.csv'.

    Returns:
        dict: A dictionary containing player IDs as keys and their season experience as values.
    """
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

    #Exporting player experance as csv 

    with open('active_player_experance.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Player ID', 'Season Experience'])
        for key, value in player_dict.items():
            writer.writerow([key, value])

    print("Exported player experance data as a csv")
    return player_dict

# Calling the player experance function 
player_experience = get_player_experience(player_ids)



# Getting all the home and away games 
def get_home_and_away_games(player_ids, season="2023-24", save_csv=False, output_dir="output"):
    """
    Retrieves home and away game logs for a list of NBA player IDs for a given season
    and optionally saves them as separate CSV files.

    Parameters:
        player_ids (list): List of player IDs to retrieve game logs for.
        season (str): NBA season in "YYYY-YY" format. Default is "2023-24".
        save_csv (bool): If True, saves the home and away game DataFrames as CSV files. Default is False.
        output_dir (str): Directory where CSV files will be saved. Default is "output".

    Returns:
        tuple: Two lists containing DataFrames:
               - home_games: List of DataFrames for home games for each player.
               - away_games: List of DataFrames for away games for each player.
    """
    import os

    # Create output directory if saving CSVs
    if save_csv and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    home_games = []
    away_games = []

    for i in player_ids:
        # Get game log data for the player
        player_game_log = playergamelog.PlayerGameLog(player_id=i, season=season)

        # Convert to a DataFrame
        game_log_df = player_game_log.get_data_frames()[0]

        # Filter for away games
        temp_away_games_df = game_log_df[game_log_df['MATCHUP'].str.contains('@')]

        # Filter for home games
        temp_home_games_df = game_log_df[~game_log_df['MATCHUP'].str.contains('@')]

        # Append to the respective lists
        away_games.append(temp_away_games_df)
        home_games.append(temp_home_games_df)

        # Save to CSV if required
        if save_csv:
            away_csv_path = os.path.join(output_dir, f"player_{i}_away_games.csv")
            home_csv_path = os.path.join(output_dir, f"player_{i}_home_games.csv")

            temp_away_games_df.to_csv(away_csv_path, index=False)
            temp_home_games_df.to_csv(home_csv_path, index=False)

            print(f"Saved CSVs for Player ID {i}: {away_csv_path}, {home_csv_path}")

        # Print progress
        print(f"Player ID {i}: {len(temp_away_games_df)} away games, {len(temp_home_games_df)} home games.")
        time.sleep(2)  # Pause between API requests to avoid rate limits

    return home_games, away_games

#calling the home & away games function 
home_games, away_games = get_home_and_away_games(player_ids[:5], save_csv=True, output_dir="game_logs")







