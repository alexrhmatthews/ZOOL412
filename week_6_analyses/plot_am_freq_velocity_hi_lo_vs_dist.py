import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Define file paths
data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
output_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/plots"

# Load the data
df = pd.read_csv(data_file)

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to group animals based on a specified distance
def group_animals(df, group_distance=20.0):
    # Filter the data for the specified distance
    df_group = df[df['Distance'] == group_distance]
    
    # Initialize columns to classify High and Low for the specified distance
    df['Group_High_Low_Frequency'] = 'Low'
    df['Group_High_Low_Amplitude'] = 'Low'
    df['Group_High_Low_Velocity'] = 'Low'
    
    # Use tqdm to add a progress bar for the loop
    for index, row in tqdm(df_group.iterrows(), total=df_group.shape[0], desc="Grouping animals"):
        if row['Agent1_Frequencies'] > row['Agent2_Frequencies']:
            df.loc[(df['Agent1_ID'] == row['Agent1_ID']) & (df['Agent2_ID'] == row['Agent2_ID']), 'Group_High_Low_Frequency'] = 'High'
            df.loc[(df['Agent2_ID'] == row['Agent2_ID']) & (df['Agent1_ID'] == row['Agent1_ID']), 'Group_High_Low_Frequency'] = 'Low'
        else:
            df.loc[(df['Agent1_ID'] == row['Agent1_ID']) & (df['Agent2_ID'] == row['Agent2_ID']), 'Group_High_Low_Frequency'] = 'Low'
            df.loc[(df['Agent2_ID'] == row['Agent2_ID']) & (df['Agent1_ID'] == row['Agent1_ID']), 'Group_High_Low_Frequency'] = 'High'
        
        if row['Agent1_Amplitudes'] > row['Agent2_Amplitudes']:
            df.loc[(df['Agent1_ID'] == row['Agent1_ID']) & (df['Agent2_ID'] == row['Agent2_ID']), 'Group_High_Low_Amplitude'] = 'High'
            df.loc[(df['Agent2_ID'] == row['Agent2_ID']) & (df['Agent1_ID'] == row['Agent1_ID']), 'Group_High_Low_Amplitude'] = 'Low'
        else:
            df.loc[(df['Agent1_ID'] == row['Agent1_ID']) & (df['Agent2_ID'] == row['Agent2_ID']), 'Group_High_Low_Amplitude'] = 'Low'
            df.loc[(df['Agent2_ID'] == row['Agent2_ID']) & (df['Agent1_ID'] == row['Agent1_ID']), 'Group_High_Low_Amplitude'] = 'High'
        
        if row['Agent1_Velocities'] > row['Agent2_Velocities']:
            df.loc[(df['Agent1_ID'] == row['Agent1_ID']) & (df['Agent2_ID'] == row['Agent2_ID']), 'Group_High_Low_Velocity'] = 'High'
            df.loc[(df['Agent2_ID'] == row['Agent2_ID']) & (df['Agent1_ID'] == row['Agent1_ID']), 'Group_High_Low_Velocity'] = 'Low'
        else:
            df.loc[(df['Agent1_ID'] == row['Agent1_ID']) & (df['Agent2_ID'] == row['Agent2_ID']), 'Group_High_Low_Velocity'] = 'Low'
            df.loc[(df['Agent2_ID'] == row['Agent2_ID']) & (df['Agent1_ID'] == row['Agent1_ID']), 'Group_High_Low_Velocity'] = 'High'
    
    return df

# Apply the grouping function with a default distance of 20m
group_distance = 20.0
df_grouped = group_animals(df, group_distance=group_distance)

# Combine data for plotting
df_combined_frequency = pd.DataFrame({
    'Distance': pd.concat([df_grouped['Distance'], df_grouped['Distance']]),
    'Frequency': pd.concat([df_grouped['Agent1_Frequencies'], df_grouped['Agent2_Frequencies']]),
    'Group': pd.concat([df_grouped['Group_High_Low_Frequency'], df_grouped['Group_High_Low_Frequency']])
})

df_combined_amplitude = pd.DataFrame({
    'Distance': pd.concat([df_grouped['Distance'], df_grouped['Distance']]),
    'Amplitude': pd.concat([df_grouped['Agent1_Amplitudes'], df_grouped['Agent2_Amplitudes']]),
    'Group': pd.concat([df_grouped['Group_High_Low_Amplitude'], df_grouped['Group_High_Low_Amplitude']])
})

df_combined_velocity = pd.DataFrame({
    'Distance': pd.concat([df_grouped['Distance'], df_grouped['Distance']]),
    'Velocity': pd.concat([df_grouped['Agent1_Velocities'], df_grouped['Agent2_Velocities']]),
    'Group': pd.concat([df_grouped['Group_High_Low_Velocity'], df_grouped['Group_High_Low_Velocity']])
})

# Plotting grouped data for Frequency, Amplitude, and Velocity
fig, axs = plt.subplots(3, 1, figsize=(12, 18))

# Frequency plot
sns.boxplot(x='Distance', y='Frequency', hue='Group', data=df_combined_frequency, ax=axs[0])
axs[0].set_xlabel('Distance (Categorical)')
axs[0].set_ylabel('Frequency (Hz)')
axs[0].set_title('Frequency vs Distance Grouped by High/Low at {}m'.format(group_distance))

# Amplitude plot
sns.boxplot(x='Distance', y='Amplitude', hue='Group', data=df_combined_amplitude, ax=axs[1])
axs[1].set_xlabel('Distance (Categorical)')
axs[1].set_ylabel('Amplitude')
axs[1].set_title('Amplitude vs Distance Grouped by High/Low at {}m'.format(group_distance))

# Velocity plot
sns.boxplot(x='Distance', y='Velocity', hue='Group', data=df_combined_velocity, ax=axs[2])
axs[2].set_xlabel('Distance (Categorical)')
axs[2].set_ylabel('Velocity')
axs[2].set_title('Velocity vs Distance Grouped by High/Low at {}m'.format(group_distance))

# Adjust layout and save the plots
plt.tight_layout()
output_file = os.path.join(output_folder, 'grouped_metrics_vs_distance_{}.png'.format(int(group_distance)))
plt.savefig(output_file)

print(f"Plots saved to {output_file}")
