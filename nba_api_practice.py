
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import time
import csv


def nba_playerid_by_season(season='2023-24', output_csv='nba_players_by_season.csv'):
    """
    Fetches the list of all NBA players active during a given season, 
    saves it as a CSV file, and returns a list of their player IDs.

    Parameters:
        season (str): The NBA season in 'YYYY-YY' format. Default is '2023-24'.
        output_csv (str): File name for the output CSV. Default is 'nba_players_by_season.csv'.

    Returns:
        list: A list of player IDs for players active during the specified season.
    """
    # Convert season to numeric start year (e.g. '2023-24' -> 2023)
    season_start_year = int(season.split('-')[0])

    # Fetch all players (both historical and current)
    players_response = commonallplayers.CommonAllPlayers(
        # Fetch historical data as well
        is_only_current_season=0,  
        league_id='00',          
        season=season
    )
    # Converting to a DataFrame
    players_data = players_response.get_data_frames()[0]  

    # Ensure FROM_YEAR and TO_YEAR are integers
    players_data['FROM_YEAR'] = pd.to_numeric(players_data['FROM_YEAR'], errors='coerce')
    players_data['TO_YEAR'] = pd.to_numeric(players_data['TO_YEAR'], errors='coerce')

    # Filter players active during the specified season
    active_players = players_data[
        (players_data['FROM_YEAR'] <= season_start_year) &
        (players_data['TO_YEAR'] >= season_start_year) &
        # Only rostered players
        (players_data['ROSTERSTATUS'] == 1)  
    ]

    # Save the filtered data to a CSV file
    active_players.to_csv(output_csv, index=False)
    print(f"Filtered CSV file created: {output_csv}")

    # Extract player IDs for the given season
    player_ids = active_players['PERSON_ID'].tolist()
    print(f"Number of player IDs for season {season}: {len(player_ids)}")

    return player_ids


#Calling the player_id function 
player_ids = nba_playerid_by_season(season='2023-24', output_csv='nba_players_2023_24.csv')




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
#player_experience = get_player_experience(player_ids)



# Getting all the home and away games 
def get_home_and_away_games(player_ids, season="2023-24", save_csv=False, home_csv="home_games.csv", away_csv="away_games.csv"):
    """
    Retrieves home and away game logs for a list of NBA player IDs for a given season
    and optionally saves them as two separate CSV files.

    Parameters:
        player_ids (list): List of player IDs to retrieve game logs for.
        season (str): NBA season in "YYYY-YY" format. Default is "2023-24".
        save_csv (bool): If True, saves the combined home and away game DataFrames as CSV files. Default is False.
        home_csv (str): File path for the home games CSV. Default is "home_games.csv".
        away_csv (str): File path for the away games CSV. Default is "away_games.csv".

    Returns:
        tuple: Two DataFrames:
               - home_games_df: DataFrame of all home games for all players.
               - away_games_df: DataFrame of all away games for all players.
    """
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

        # Print progress
        print(f"Player ID {i}: {len(temp_away_games_df)} away games, {len(temp_home_games_df)} home games.")
        time.sleep(2)  # Pause between API requests to avoid rate limits

    # Combine all players' games into single DataFrames
    home_games_df = pd.concat(home_games, ignore_index=True)
    away_games_df = pd.concat(away_games, ignore_index=True)

    # Save to CSV if required
    if save_csv:
        home_games_df.to_csv(home_csv, index=False)
        away_games_df.to_csv(away_csv, index=False)
        print(f"Saved home games to {home_csv} and away games to {away_csv}.")

    return home_games_df, away_games_df


#calling the home & away games function 
# home_games_df, away_games_df = get_home_and_away_games(
#     player_ids, 
#     save_csv=True, 
#     home_csv="all_home_games.csv", 
#     away_csv="all_away_games.csv"
# )


#Using the above functions to gather all of the data needed 
seasons_of_interest = ["2023-24", "2022-23", "2021-22", "2020-21", "2019-20", "2018-19", "2017-18", "2016-17", "2015-16"]

#Get the player IDs for 




