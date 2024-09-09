import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File path to the merged data
merged_data_path = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names_with_videodata.csv"

# Load the merged data
merged_df = pd.read_csv(merged_data_path)

# Initialize the scaler
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

# Normalize brightness values for both agents
merged_df['Agent1_left_brightness'] = scaler.fit_transform(merged_df[['Agent1_left_brightness']])
merged_df['Agent1_right_brightness'] = scaler.fit_transform(merged_df[['Agent1_right_brightness']])
merged_df['Agent2_left_brightness'] = scaler.fit_transform(merged_df[['Agent2_left_brightness']])
merged_df['Agent2_right_brightness'] = scaler.fit_transform(merged_df[['Agent2_right_brightness']])

# Combine the brightness data for both agents
brightness_left = pd.concat([merged_df['Agent1_left_brightness'], merged_df['Agent2_left_brightness']])
brightness_right = pd.concat([merged_df['Agent1_right_brightness'], merged_df['Agent2_right_brightness']])
velocity = pd.concat([merged_df['Agent1_Velocities'], merged_df['Agent2_Velocities']])

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left Brightness vs Velocity
sns.regplot(x=velocity, y=brightness_left, ax=axes[0], ci=95, color='blue')
axes[0].set_title('Right Brightness vs. Velocity')
axes[0].set_xlabel('Velocity')
axes[0].set_ylabel('Normalized Brightness')

# Right Brightness vs Velocity
sns.regplot(x=velocity, y=brightness_right, ax=axes[1], ci=95, color='red')
axes[1].set_title('Left Brightness vs. Velocity')
axes[1].set_xlabel('Velocity')
axes[1].set_ylabel('Normalized Brightness')

# Adjust layout and show the plot
plt.tight_layout()
import os
output_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/plots"
output_file = os.path.join(output_folder, 'brightness_vs_velocity.png')
plt.savefig(output_file)

print(f"Plot saved to {output_file}")
