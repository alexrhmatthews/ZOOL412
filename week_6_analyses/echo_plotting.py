import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Load the combined experiment data
combined_data_file = "/home/alexmatthews/Downloads/Experiment_Results(1)/Experiment_Results/combined_experiment_data_echo_rounds.csv"
data = pd.read_csv(combined_data_file)

# Calculate the absolute difference between Animal1 and Animal2 frequencies
data['Absolute_Difference'] = np.abs(data['Animal1_Frequencies'] - data['Animal2_Frequencies'])

# Group by distance and calculate the mean and confidence interval for the absolute difference
mean_diff = data.groupby('Distance')['Absolute_Difference'].mean()
ci_diff = data.groupby('Distance')['Absolute_Difference'].apply(lambda x: stats.sem(x) * stats.t.ppf((1 + 0.95) / 2., len(x)))

# Plotting
plt.figure(figsize=(10, 6))
plt.errorbar(mean_diff.index, mean_diff, yerr=ci_diff, fmt='-o', capsize=5, label='Mean Absolute Difference ± 95% CI')
plt.xlabel('Distance (m)')
plt.ylabel('Mean Absolute Frequency Difference')
plt.title('Mean Absolute Frequency Difference Between Animal1 and Echo Across All Trials and Distances')
plt.legend()
plt.grid(True)
import os
output_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/plots"
output_file = os.path.join(output_folder, 'echo_difference_freq.png')
plt.savefig(output_file)

print(f"Plot saved to {output_file}")
