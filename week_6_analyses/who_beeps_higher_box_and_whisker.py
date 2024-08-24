import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define file paths
data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
output_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/plots"

# Load the data
df = pd.read_csv(data_file)

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Calculate the overall average frequency for each agent across all distances within each experimental run
df['Agent1_Overall_Avg_Frequency'] = df.groupby(['Experiment_Round', 'Agent1_ID'])['Agent1_Frequencies'].transform('mean')
df['Agent2_Overall_Avg_Frequency'] = df.groupby(['Experiment_Round', 'Agent2_ID'])['Agent2_Frequencies'].transform('mean')

# Assign agents to high and low groups based on overall average frequency
df['Agent1_Group'] = np.where(df['Agent1_Overall_Avg_Frequency'] >= df['Agent1_Overall_Avg_Frequency'].median(), 'High', 'Low')
df['Agent2_Group'] = np.where(df['Agent2_Overall_Avg_Frequency'] >= df['Agent2_Overall_Avg_Frequency'].median(), 'High', 'Low')

# Prepare the data for plotting
high_group = pd.concat([
    df[df['Agent1_Group'] == 'High'][['Distance', 'Agent1_Frequencies']].rename(columns={'Agent1_Frequencies': 'Frequency'}),
    df[df['Agent2_Group'] == 'High'][['Distance', 'Agent2_Frequencies']].rename(columns={'Agent2_Frequencies': 'Frequency'})
])

low_group = pd.concat([
    df[df['Agent1_Group'] == 'Low'][['Distance', 'Agent1_Frequencies']].rename(columns={'Agent1_Frequencies': 'Frequency'}),
    df[df['Agent2_Group'] == 'Low'][['Distance', 'Agent2_Frequencies']].rename(columns={'Agent2_Frequencies': 'Frequency'})
])

# Initialize the figure
plt.figure(figsize=(12, 8))

# Define the positions for the boxplots
distances = df['Distance'].unique()
distances.sort()
positions_low = np.arange(len(distances)) - 0.15
positions_high = np.arange(len(distances)) + 0.15

# Create box and whisker plots for each distance for both high and low groups
plt.boxplot([low_group[low_group['Distance'] == d]['Frequency'] for d in distances],
            positions=positions_low, widths=0.3, patch_artist=True,
            boxprops=dict(facecolor='skyblue'), medianprops=dict(color='black'),
            showfliers=True, flierprops=dict(markerfacecolor='red', marker='o'))

plt.boxplot([high_group[high_group['Distance'] == d]['Frequency'] for d in distances],
            positions=positions_high, widths=0.3, patch_artist=True,
            boxprops=dict(facecolor='lightgreen'), medianprops=dict(color='black'),
            showfliers=True, flierprops=dict(markerfacecolor='red', marker='o'))

# Customize the plot
plt.xticks(np.arange(len(distances)), labels=[f"{d:.2f}" for d in distances])
plt.xlabel('Distance (m)')
plt.ylabel('Frequency (Hz)')
plt.title('Box and Whisker Plot of Agent Frequencies by Distance for High and Low Groups')

# Add custom legend
import matplotlib.patches as mpatches
low_patch = mpatches.Patch(color='skyblue', label='Low Group')
high_patch = mpatches.Patch(color='lightgreen', label='High Group')
plt.legend(handles=[low_patch, high_patch], title='Group', loc='upper right')

# Save the plot
output_file = os.path.join(output_folder, 'frequency_variability_boxplot_by_distance.png')
plt.savefig(output_file)

print(f"Plot saved to {output_file}")
