import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Load the combined experiment data
combined_data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
df = pd.read_csv(combined_data_file)
print("shape", df.shape)

# Filter the data to only include the rows where Distance is 10 meters
df_10m = df[df['Distance'] == 10.0].copy()
print("len 10 =  ", len(df_10m))

# Determine which agent beeped higher at 10 meters and create a mapping
higher_at_10_map = {}
for _, row in tqdm(df_10m.iterrows(), total=df_10m.shape[0], desc="Processing 10m Data"):
    if row['Agent1_Frequencies'] > row['Agent2_Frequencies']:
        higher_at_10_map[row['Agent1_ID']] = 'higher'
        higher_at_10_map[row['Agent2_ID']] = 'lower'
    else:
        higher_at_10_map[row['Agent2_ID']] = 'higher'
        higher_at_10_map[row['Agent1_ID']] = 'lower'

print("len higher =  ", len(higher_at_10_map))
# Debugging: Print the mapping to check if it's populated correctly
print("Higher at 10m mapping (first 10):", list(higher_at_10_map.items())[:10])
print("Total in mapping:", len(higher_at_10_map))

# Create new DataFrames to classify each agent's data into the appropriate group
df_higher = pd.DataFrame(columns=['Agent_ID', 'Frequencies', 'Distance'])
df_lower = pd.DataFrame(columns=['Agent_ID', 'Frequencies', 'Distance'])

# Loop through each row in the DataFrame and classify into higher/lower groups
for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Classifying Data"):
    agent1_data = {'Agent_ID': row['Agent1_ID'], 'Frequencies': row['Agent1_Frequencies'], 'Distance': row['Distance']}
    agent2_data = {'Agent_ID': row['Agent2_ID'], 'Frequencies': row['Agent2_Frequencies'], 'Distance': row['Distance']}
    
    if higher_at_10_map.get(row['Agent1_ID']) == 'higher':
        df_higher = df_higher._append(agent1_data, ignore_index=True)
        df_lower = df_lower._append(agent2_data, ignore_index=True)
    else:
        df_higher = df_higher._append(agent2_data, ignore_index=True)
        df_lower = df_lower._append(agent1_data, ignore_index=True)

# Debugging: Print the sizes of the DataFrames to ensure they contain data
print("df_higher size:", df_higher.shape)
print("df_lower size:", df_lower.shape)

# Plotting two box-and-whisker plots: one for the "Higher" group and one for the "Lower" group
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 8), sharey=True)

# Plot for the "Higher" group
if not df_higher.empty:
    sns.boxplot(x='Distance', y='Frequencies', data=df_higher, ax=axes[0])
    axes[0].set_title('Frequency vs Distance for Higher Group')
    axes[0].set_ylabel('Frequency (Hz)')
    axes[0].set_xlabel('Distance (m)')
else:
    print("Warning: 'Higher' group is empty!")

# Plot for the "Lower" group
if not df_lower.empty:
    sns.boxplot(x='Distance', y='Frequencies', data=df_lower, ax=axes[1])
    axes[1].set_title('Frequency vs Distance for Lower Group')
    axes[1].set_xlabel('Distance (m)')
else:
    print("Warning: 'Lower' group is empty!")

# Save the plot
plt.savefig('/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/BEEP_FREQ_VS_DIST_GROUPED.PNG')
plt.show()
