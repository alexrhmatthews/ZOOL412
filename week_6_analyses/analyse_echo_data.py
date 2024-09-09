import os
import pandas as pd
import numpy as np

# Define base paths
base_folder = "/home/alexmatthews/Downloads/Experiment_Results(1)/Experiment_Results"
matchmaking_log_file = '/home/alexmatthews/Downloads/Experiment_Results(1)/Experiment_Results/matchmaking_log_echo.csv'

# Load the matchmaking log
matchmaking_log = pd.read_csv(matchmaking_log_file)

# Filter to include only the relevant rounds where actual pairings with Echo start
relevant_matchmaking_log = matchmaking_log.dropna(subset=['Echo_Last_Frequency'])

# Generate unique IDs for each animal, considering Echo as a unique ID
unique_animals = pd.concat([relevant_matchmaking_log['Animal1'], relevant_matchmaking_log['Animal2']]).unique()
animal_id_mapping = {animal: f"Animal_{i+1}" for i, animal in enumerate(unique_animals)}

# Add unique ID and original name columns to the matchmaking log
relevant_matchmaking_log['Animal1_ID'] = relevant_matchmaking_log['Animal1'].map(animal_id_mapping)
relevant_matchmaking_log['Animal2_ID'] = relevant_matchmaking_log['Animal2'].map(animal_id_mapping)
relevant_matchmaking_log['Animal1_Name'] = relevant_matchmaking_log['Animal1']
relevant_matchmaking_log['Animal2_Name'] = relevant_matchmaking_log['Animal2']

# Initialize a list to collect all the data
all_data = []

# List of new experimental rounds
echo_rounds = ['Echo_round_01', 'Echo_round_02']

# Loop through each new experimental round
for echo_round in echo_rounds:
    round_folder = os.path.join(base_folder, echo_round)
    
    # Loop through each experiment in the round
    for experiment_num in range(1, 11):
        if experiment_num < 10:
            experiment_folder = os.path.join(round_folder, f"experiment_0{experiment_num}", "data_files")
        else:
            experiment_folder = os.path.join(round_folder, f"experiment_{experiment_num}", "data_files")
        
        # Match the pair ID to the correct animals from the matchmaking log
        pair_info = relevant_matchmaking_log[(relevant_matchmaking_log['Round'] == int(echo_round.split('_')[-1])) & 
                                             (relevant_matchmaking_log['Pair'] == experiment_num)]
        
        if pair_info.empty:
            continue
        
        animal1_id = pair_info['Animal1_ID'].values[0]
        animal2_id = pair_info['Animal2_ID'].values[0]
        animal1_name = pair_info['Animal1_Name'].values[0]
        animal2_name = pair_info['Animal2_Name'].values[0]
        pair_id = pair_info['Pair'].values[0]
        
        # Loop through all CSV files in the data_files folder
        for csv_file in os.listdir(experiment_folder):
            if csv_file.endswith(".csv") and "data_distance" in csv_file:
                data = pd.read_csv(os.path.join(experiment_folder, csv_file))
                
                # Extract the distance value from the file name
                try:
                    distance_str = csv_file.split('_')[2].replace('m.csv', '')
                    distance = float(distance_str)
                except ValueError:
                    print(f"Error parsing distance from file name: {csv_file}")
                    continue
                
                # Add metadata columns
                data['Experiment_Round'] = echo_round
                data['Animal1_ID'] = animal1_id
                data['Animal2_ID'] = animal2_id
                data['Animal1_Name'] = animal1_name
                data['Animal2_Name'] = animal2_name
                data['Pair_ID'] = pair_id
                data['Distance'] = distance  # Use the extracted distance
                
                # Rename columns to distinguish between Animal1 and Animal2
                data.columns = ['Animal1_Frequencies', 'Animal2_Frequencies', 'Animal1_Velocities', 
                                'Animal2_Velocities', 'Animal1_Amplitudes', 'Animal2_Amplitudes', 
                                'Experiment_Round', 'Animal1_ID', 'Animal2_ID', 'Animal1_Name', 
                                'Animal2_Name', 'Pair_ID', 'Distance']
                
                # Append data to the list
                all_data.append(data)

# Concatenate all data into a single DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Save the final DataFrame to a CSV file
output_file = os.path.join(base_folder, "combined_experiment_data_echo_rounds.csv")
final_df.to_csv(output_file, index=False)

print(f"Data successfully collated and saved to {output_file}")
