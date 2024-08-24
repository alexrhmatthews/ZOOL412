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
    'Frequency': pd.concat([df['Agent1_Frequencies'], df['Agent2_Frequencies']]),
    'Velocity': pd.concat([df['Agent1_Velocities'], df['Agent2_Velocities']])
})

# Remove rows where velocity is 0
df_combined = df_combined[df_combined['Velocity'] != 0]

# Plotting frequency versus velocity
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Velocity', y='Frequency', data=df_combined, alpha=0.7)

# Customize the plot
plt.xlabel('Velocity')
plt.ylabel('Frequency (Hz)')
plt.title('Frequency vs Velocity')
plt.grid(True)

# Save the plot
output_file = os.path.join(output_folder, 'frequency_vs_velocity_scatterplot.png')
plt.savefig(output_file)

print(f"Plot saved to {output_file}")
