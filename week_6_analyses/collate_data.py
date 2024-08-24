import os
import pandas as pd
import numpy as np

# Define base paths
base_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results"
matchmaking_log_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/matchmaking_log.csv"

# Load the matchmaking log
matchmaking_log = pd.read_csv(matchmaking_log_file)

# Generate unique IDs for each agent
unique_agents = pd.concat([matchmaking_log['Agent1'], matchmaking_log['Agent2']]).unique()
agent_id_mapping = {agent: f"Agent_{i+1}" for i, agent in enumerate(unique_agents)}

# Add unique ID and original name columns to the matchmaking log
matchmaking_log['Agent1_ID'] = matchmaking_log['Agent1'].map(agent_id_mapping)
matchmaking_log['Agent2_ID'] = matchmaking_log['Agent2'].map(agent_id_mapping)
matchmaking_log['Agent1_Name'] = matchmaking_log['Agent1']
matchmaking_log['Agent2_Name'] = matchmaking_log['Agent2']

# Initialize a list to collect all the data
all_data = []

# Loop through each experimental round
for round_num in range(1, 6):
    round_folder = os.path.join(base_folder, f"Experimental_round_0{round_num}")
    
    # Loop through each experiment in the round
    for experiment_num in range(1, 11):
        if experiment_num < 10:
            experiment_folder = os.path.join(round_folder, f"experiment_0{experiment_num}", "data_files")
        else:
            experiment_folder = os.path.join(round_folder, f"experiment_{experiment_num}", "data_files")
        
        # Match the pair ID to the correct agents from the matchmaking log
        pair_info = matchmaking_log[(matchmaking_log['Round'] == round_num) & 
                                    (matchmaking_log['Pair'] == experiment_num)]
        
        if pair_info.empty:
            continue
        
        agent1_id = pair_info['Agent1_ID'].values[0]
        agent2_id = pair_info['Agent2_ID'].values[0]
        agent1_name = pair_info['Agent1_Name'].values[0]
        agent2_name = pair_info['Agent2_Name'].values[0]
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
                data['Experiment_Round'] = round_num
                data['Agent1_ID'] = agent1_id
                data['Agent2_ID'] = agent2_id
                data['Agent1_Name'] = agent1_name
                data['Agent2_Name'] = agent2_name
                data['Pair_ID'] = pair_id
                data['Distance'] = distance  # Use the extracted distance
                
                # Rename columns to distinguish between Agent1 and Agent2
                data.columns = ['Agent1_Frequencies', 'Agent2_Frequencies', 'Agent1_Velocities', 
                                'Agent2_Velocities', 'Agent1_Amplitudes', 'Agent2_Amplitudes', 
                                'Experiment_Round', 'Agent1_ID', 'Agent2_ID', 'Agent1_Name', 
                                'Agent2_Name', 'Pair_ID', 'Distance']
                
                # Append data to the list
                all_data.append(data)

# Concatenate all data into a single DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Save the final DataFrame to a CSV file
output_file = os.path.join(base_folder, "combined_experiment_data_with_names.csv")
final_df.to_csv(output_file, index=False)

print(f"Data successfully collated and saved to {output_file}")