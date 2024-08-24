import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define file paths
data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
output_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/plots"

# Load the data
df = pd.read_csv(data_file)

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Calculate the median frequency (rounded) for each agent at each distance
df['Agent1_Median_Frequency'] = df.groupby(['Agent1_ID', 'Distance'])['Agent1_Frequencies'].transform(lambda x: round(x.median()))
df['Agent2_Median_Frequency'] = df.groupby(['Agent2_ID', 'Distance'])['Agent2_Frequencies'].transform(lambda x: round(x.median()))

# Identify which agent in the pair beeped at a higher or lower median frequency
df['Higher_Agent_Frequency'] = df[['Agent1_Median_Frequency', 'Agent2_Median_Frequency']].max(axis=1)
df['Lower_Agent_Frequency'] = df[['Agent1_Median_Frequency', 'Agent2_Median_Frequency']].min(axis=1)

# Prepare the data for plotting
distances = df['Distance'].unique()
distances.sort()

# Initialize the figure
plt.figure(figsize=(12, 8))

# Define the positions for the boxplots
positions_lower = np.arange(len(distances)) - 0.15
positions_higher = np.arange(len(distances)) + 0.15

# Create the boxplots
plt.boxplot([df[df['Distance'] == d]['Lower_Agent_Frequency'] for d in distances], positions=positions_lower, widths=0.3, patch_artist=True, boxprops=dict(facecolor='skyblue'), medianprops=dict(color='black'))
plt.boxplot([df[df['Distance'] == d]['Higher_Agent_Frequency'] for d in distances], positions=positions_higher, widths=0.3, patch_artist=True, boxprops=dict(facecolor='lightgreen'), medianprops=dict(color='black'))

# Customize the plot
plt.xticks(np.arange(len(distances)), labels=[f"{d:.2f}" for d in distances])
plt.xlabel('Distance (m)')
plt.ylabel('Frequency (Hz)')
plt.title('Box and Whisker Plot of Agent Frequencies by Distance')

# Add custom legend
import matplotlib.patches as mpatches
low_patch = mpatches.Patch(color='skyblue', label='Low Frequency')
high_patch = mpatches.Patch(color='lightgreen', label='High Frequency')
plt.legend(handles=[low_patch, high_patch], title='Frequency Category', loc='upper right')

# Save the plot
output_file = os.path.join(output_folder, 'offset_median_frequency_boxplot_by_distance.png')
plt.savefig(output_file)

print(f"Plot saved to {output_file}")
