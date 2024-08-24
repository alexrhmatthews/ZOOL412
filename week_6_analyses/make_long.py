import pandas as pd

# Assuming your data is in a CSV file
df = pd.read_csv('/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names_with_videodata.csv')

# Reshape the DataFrame to long format
df_long = pd.melt(df, 
                  id_vars=['Experiment_Round', 'Pair_ID', 'Distance'], 
                  value_vars=['Agent1_Frequencies', 'Agent2_Frequencies', 
                              'Agent1_Velocities', 'Agent2_Velocities', 
                              'Agent1_Amplitudes', 'Agent2_Amplitudes', 
                              'Agent1_ID', 'Agent2_ID', 
                              'Agent1_Name', 'Agent2_Name', 
                              'Agent1_left_brightness', 'Agent1_right_brightness', 
                              'Agent2_left_brightness', 'Agent2_right_brightness'],
                  var_name='Attribute', 
                  value_name='Value')

# Extract Agent information (1 or 2) and clean up column names
df_long['Agent_Number'] = df_long['Attribute'].str.extract(r'Agent(\d)_')
df_long['Attribute'] = df_long['Attribute'].str.replace(r'Agent\d_', '')

# Pivot table to create a cleaner long format
df_long = df_long.pivot_table(index=['Experiment_Round', 'Pair_ID', 'Distance', 'Agent_Number'], 
                              columns='Attribute', 
                              values='Value',
                              aggfunc='first').reset_index()

# Save the reshaped DataFrame to a new CSV file
df_long.to_csv('combined_long_data.csv', index=False)

print(df_long.head())
