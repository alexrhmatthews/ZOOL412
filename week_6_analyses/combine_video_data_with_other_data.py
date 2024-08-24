import pandas as pd

# Your file paths
experiment_data_path = '/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv'
video_analysis_path = '/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/experiment_video_analysis.csv'

# Load the two datasets
data_with_names_df = pd.read_csv(experiment_data_path)
video_ana_df = pd.read_csv(video_analysis_path)

# Convert the 'Distance' column to match the format in both DataFrames
video_ana_df['distance'] = video_ana_df['distance'].astype(float)
data_with_names_df['Distance'] = data_with_names_df['Distance'].astype(float)

# Create new columns for brightness in the main dataframe, initialized with NaN
data_with_names_df['Agent1_left_brightness'] = pd.NA
data_with_names_df['Agent1_right_brightness'] = pd.NA
data_with_names_df['Agent2_left_brightness'] = pd.NA
data_with_names_df['Agent2_right_brightness'] = pd.NA

# Iterate through the video analysis data and add brightness data to the correct rows in the main DataFrame
for _, row in video_ana_df.iterrows():
    # Extract relevant information from the row
    exp_round = row['Experiment_Round']
    pair_id = row['Pair_ID']
    distance = row['distance']
    agent_num = row['agent_number']
    left_brightness = row['left_brightness']
    right_brightness = row['right_brightness']
    
    # Find the matching row in the main DataFrame
    mask = (
        (data_with_names_df['Experiment_Round'] == exp_round) & 
        (data_with_names_df['Pair_ID'] == pair_id) & 
        (data_with_names_df['Distance'] == distance)
    )
    
    if agent_num == 1:
        data_with_names_df.loc[mask, 'Agent1_left_brightness'] = left_brightness
        data_with_names_df.loc[mask, 'Agent1_right_brightness'] = right_brightness
    elif agent_num == 2:
        data_with_names_df.loc[mask, 'Agent2_left_brightness'] = left_brightness
        data_with_names_df.loc[mask, 'Agent2_right_brightness'] = right_brightness

# Save the merged DataFrame to a new CSV file
output_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names_with_videodata.csv"
data_with_names_df.to_csv(output_file, index=False)

print(f"Merged data saved to {output_file}")
