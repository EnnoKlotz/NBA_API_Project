
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import time
import csv


def nba_playerid_by_season(season='2023-24', output_to_csv= False):
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

    # Save the filtered data to a CSV file if scpecified 
    if output_to_csv == True:
        active_players.to_csv(output_csv, index=False)
        print(f"Filtered CSV file created: {output_csv}")
    else:
        # Extract player IDs for the given season
        player_ids = active_players['PERSON_ID'].tolist()
        print(f"Number of player IDs for season {season}: {len(player_ids)}")

    return player_ids



def get_player_experience(player_ids, season_ids, save_to_csv= False, output_csv= 'player_experience.csv'):
    """
    Fetch the experience data for a list of NBA players for specific seasons and save it as a CSV.

    Parameters:
        player_ids (list): List of player IDs to process.
        season_ids (list): List of season IDs to calculate experience for (e.g., ['2022-23', '2021-22']).
        save_to_csv (bool): Save results as a CSV file.
        output_csv (str): File name for the output CSV. Default is 'player_experience.csv'.

    Returns:
        DataFrame: A pandas DataFrame containing player IDs and their experience for each season.
    """
    # List to store the experience data
    player_experience_list = []

    # Iterate over each player ID
    for player_id in player_ids:
        # Fetch career stats for the player
        career_stats = playercareerstats.PlayerCareerStats(player_id= player_id)
        stats_df = career_stats.get_data_frames()[0]

        # Iterate over each season ID
        for season_id in season_ids:
            # Filter the DataFrame for seasons before or equal to the given season
            filtered_df = stats_df[stats_df['SEASON_ID'] <= season_id]

            # Calculate the experience as the number of rows (seasons) in the filtered DataFrame
            experience = len(filtered_df.drop_duplicates(subset=['PLAYER_ID', 'SEASON_ID']))

            # Skip players with 0 experience
            if experience == 0:
                print(f"Skipping Player ID: {player_id} due to 0 experience in Season: {season_id}")
                break

            # Append the data to the list
            player_experience_list.append({
                'Player ID': player_id,
                'Season ID': season_id,
                'Experience': experience
            })

            print(f"Processed Player ID: {player_id} for Season: {season_id} with Experience: {experience}")
            time.sleep(2)  # Pause to avoid API rate limits

    # Convert the list to a DataFrame
    player_experience_df = pd.DataFrame(player_experience_list)

    if save_to_csv:
        # Save the DataFrame to a CSV file
        player_experience_df.to_csv(output_csv, index= False)
        print(f"Exported player experience data to {output_csv}")

    return player_experience_df



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





def get_player_team_data(player_ids, save_to_csv = False, output_csv='player_team_data.csv'):
    """
    Fetch team data (SEASON_ID, TEAM_ID, TEAM_ABBREVIATION) for a list of NBA players and save it as a CSV.

    Parameters:
        player_ids (list): List of player IDs to process.
        output_csv (str): File name for the output CSV. Default is 'player_team_data.csv'.
        save_to_csv (Bool): Saving the result in a csv

    Returns:
        dict: A dictionary containing player IDs as keys and their season team data as values.
    """
    # Initialize a dictionary to store player data
    player_team_data = {}

    # Create a list to store data for the CSV export
    csv_data = []

    # Iterate over each player ID
    for player_id in player_ids:
        try:
            # Fetch career stats for the current player
            career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
            stats_df = career_stats.get_data_frames()[0]

            # Iterate over rows in the DataFrame and extract relevant information
            for _, row in stats_df.iterrows():
                season_id = row['SEASON_ID']
                team_id = row['TEAM_ID']
                team_abbr = row['TEAM_ABBREVIATION']

                # Add the data to the dictionary
                if player_id not in player_team_data:
                    player_team_data[player_id] = []
                player_team_data[player_id].append({
                    'SEASON_ID': season_id,
                    'TEAM_ID': team_id,
                    'TEAM_ABBREVIATION': team_abbr
                })

                # Append the data for the CSV
                csv_data.append([player_id, season_id, team_id, team_abbr])

            print(f"Processed player ID: {player_id}")
        except Exception as e:
            print(f"Error processing player ID {player_id}: {e}")

        # Pause for 2 seconds to avoid rate-limiting
        time.sleep(2)

    # Convert csv_data into a DataFrame
    csv_df = pd.DataFrame(csv_data, columns=['Player ID', 'Season ID', 'Team ID', 'Team Abbreviation'])

    # Group by 'Player ID' and 'Season ID', and count unique teams per group
    csv_df['Team Count'] = csv_df.groupby(['Player ID', 'Season ID'])['Team ID'].transform('nunique')

    # Update rows for players with multiple teams in a season
    csv_df.loc[csv_df['Team Count'] > 1, ['Team ID', 'Team Abbreviation']] = [0, 'TOT']

    #Drop the temp column
    csv_df.drop(columns=['Team Count'], inplace=True)

    # Drop duplicate rows based on 'Player ID' and 'Season ID'
    csv_df = csv_df.drop_duplicates(subset=['Player ID', 'Season ID'])

    if save_to_csv == True: 
        # Export data to CSV
        csv_df.to_csv(output_csv, index=False)
        print(f"Exported player team data to {output_csv}")
    else:
        return csv_df
