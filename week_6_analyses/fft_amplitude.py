import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import stats

# Define file paths
data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
output_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/plots"

# Load the data
df = pd.read_csv(data_file)

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Combine Agent1 and Agent2 data into a single DataFrame for analysis
df_combined = pd.DataFrame({
    'Frequency': pd.concat([df['Agent1_Frequencies'], df['Agent2_Frequencies']]),
    'Amplitude': pd.concat([df['Agent1_Amplitudes'], df['Agent2_Amplitudes']])
})

# Remove rows where Amplitude is 0
# df_combined = df_combined[df_combined['Amplitude'] != 0]
# df_combined = df_combined[df_combined['Frequency'] != 0]
# Sort by Frequency to align the data
df_combined = df_combined.sort_values(by='Frequency')

# Extract the amplitude and frequency as NumPy arrays
amplitude_array = df_combined['Amplitude'].to_numpy()
frequency_array = df_combined['Frequency'].to_numpy()

# Apply FFT to the amplitude data
fft_values = fft(amplitude_array)
fft_freq = np.fft.fftfreq(len(fft_values), d=(frequency_array[1] - frequency_array[0]))

# Only keep the positive frequencies
positive_freqs = fft_freq > 0
fft_values = np.abs(fft_values[positive_freqs])
fft_freq = fft_freq[positive_freqs]

# Plot the FFT results
plt.figure(figsize=(12, 8))
plt.plot(fft_freq, fft_values, label='FFT of Amplitude Data')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('FFT of Amplitude Data vs. Frequency')
plt.grid(True)

# Save the FFT plot
fft_plot_file = os.path.join(output_folder, 'fft_of_amplitude_data_vs_frequency.png')
plt.savefig(fft_plot_file)
plt.show()

print(f"FFT plot saved to {fft_plot_file}")

# Perform a statistical test to determine if noise is present
# Let's assume noise is present if there's significant variation in the higher frequencies

# Split frequencies into lower and higher bands for comparison
midpoint = len(fft_freq) // 2
low_freq_band = fft_values[:midpoint]
high_freq_band = fft_values[midpoint:]

# Perform a t-test to compare the mean amplitude between the low and high frequency bands
t_stat, p_value = stats.ttest_ind(low_freq_band, high_freq_band)

print(f"T-statistic: {t_stat}, P-value: {p_value}")

# Determine if noise is statistically significant
if p_value < 0.05:
    print("There is significant noise present in the amplitude data.")
else:
    print("No significant noise detected in the amplitude data.")
