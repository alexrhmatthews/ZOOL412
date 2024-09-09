import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

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

# Calculate regression line
slope, intercept, r_value, p_value, std_err = stats.linregress(df_combined['Velocity'], df_combined['Frequency'])

# Print out the y-intercept and regression equation
print(f"Y-Intercept: {intercept}")
print(f"Regression Equation: Frequency = {slope} * Velocity + {intercept}")

# Predict frequencies based on the regression line
df_combined['Predicted_Frequency'] = intercept + slope * df_combined['Velocity']

# Calculate the confidence interval for the regression line
# Standard error of the estimate
se = np.sqrt(np.sum((df_combined['Frequency'] - df_combined['Predicted_Frequency'])**2) / (len(df_combined) - 2))

# Confidence interval range
confidence_interval = 1.96 * se * np.sqrt(1/len(df_combined) + (df_combined['Velocity'] - df_combined['Velocity'].mean())**2 / np.sum((df_combined['Velocity'] - df_combined['Velocity'].mean())**2))

# Plotting frequency versus velocity with regression line and confidence interval
plt.figure(figsize=(12, 8))
plt.plot(df_combined['Velocity'], df_combined['Predicted_Frequency'], color='red', label='Regression Line')

# Add transparent blue shaded area for the confidence interval
plt.fill_between(df_combined['Velocity'], 
                 df_combined['Predicted_Frequency'] - confidence_interval, 
                 df_combined['Predicted_Frequency'] + confidence_interval, 
                 color='blue', alpha=0.3, label='95% Confidence Interval')

# Customize the plot
plt.xlabel('Velocity')
plt.ylabel('Frequency (Hz)')
plt.title('Frequency vs Velocity with Regression Line and Confidence Interval')
plt.grid(True)
plt.legend()

# Save the plot
output_file = os.path.join(output_folder, 'frequency_vs_velocity_regression_with_ci.png')
plt.savefig(output_file)

print(f"Plot saved to {output_file}")
