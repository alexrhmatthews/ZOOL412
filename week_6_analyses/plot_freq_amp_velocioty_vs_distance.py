import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define file paths
data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
output_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/plots"

# Load the data
df = pd.read_csv(data_file)

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Combine Agent1 and Agent2 data into a single DataFrame for plotting
df_combined = pd.DataFrame({
    'Distance': pd.concat([df['Distance'], df['Distance']]),
    'Frequency': pd.concat([df['Agent1_Frequencies'], df['Agent2_Frequencies']]),
    'Amplitude': pd.concat([df['Agent1_Amplitudes'], df['Agent2_Amplitudes']]),
    'Velocity': pd.concat([df['Agent1_Velocities'], df['Agent2_Velocities']])
})

# Remove rows where Amplitude is 0
df_combined = df_combined[df_combined['Amplitude'] != 0]

# Create subplots for Amplitude, Frequency, and Velocity against Distance
fig, axs = plt.subplots(3, 1, figsize=(12, 18))

# Plot Frequency vs Distance
sns.boxplot(x='Distance', y='Frequency', data=df_combined, ax=axs[0])
axs[0].set_xlabel('Distance (Categorical)')
axs[0].set_ylabel('Frequency (Hz)')
axs[0].set_title('Frequency vs Distance')

# Plot Amplitude vs Distance
sns.boxplot(x='Distance', y='Amplitude', data=df_combined, ax=axs[1])
axs[1].set_xlabel('Distance (Categorical)')
axs[1].set_ylabel('Amplitude')
axs[1].set_title('Amplitude vs Distance')

# Plot Velocity vs Distance
sns.boxplot(x='Distance', y='Velocity', data=df_combined, ax=axs[2])
axs[2].set_xlabel('Distance (Categorical)')
axs[2].set_ylabel('Velocity')
axs[2].set_title('Velocity vs Distance')

# Adjust layout and save the plot
plt.tight_layout()
output_file = os.path.join(output_folder, 'distance_vs_metrics_boxplot.png')
plt.savefig(output_file)

print(f"Plots saved to {output_file}")
