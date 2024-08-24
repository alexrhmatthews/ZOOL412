import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# Calculate the mean and confidence intervals for each distance for both high and low groups
high_group_stats = high_group.groupby('Distance')['Frequency'].agg(['mean', 'std', 'count'])
low_group_stats = low_group.groupby('Distance')['Frequency'].agg(['mean', 'std', 'count'])

high_group_stats['ci'] = 1.96 * high_group_stats['std'] / np.sqrt(high_group_stats['count'])
low_group_stats['ci'] = 1.96 * low_group_stats['std'] / np.sqrt(low_group_stats['count'])

# Plotting the data
plt.figure(figsize=(12, 8))
plt.errorbar(high_group_stats.index, high_group_stats['mean'], yerr=high_group_stats['ci'], fmt='-o', label='High Group', color='green')
plt.errorbar(low_group_stats.index, low_group_stats['mean'], yerr=low_group_stats['ci'], fmt='-o', label='Low Group', color='blue')

# Customize the plot
plt.xlabel('Distance (m)')
plt.ylabel('Average Frequency (Hz)')
plt.title('Average Frequency by Distance with 95% Confidence Intervals for High and Low Groups')
plt.legend(title='Group')
plt.grid(True)

# Save the plot
output_file = os.path.join(output_folder, 'grouped_avg_frequency_with_ci_lineplot.png')
plt.savefig(output_file)

print(f"Plot saved to {output_file}")
