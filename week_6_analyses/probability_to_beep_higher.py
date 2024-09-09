import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined experiment data
combined_data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
df = pd.read_csv(combined_data_file)

# Create a column that determines which agent beeped at a higher frequency for each trial
df['Higher_Beep_Agent'] = df.apply(
    lambda row: 'Agent1' if row['Agent1_Frequencies'] > row['Agent2_Frequencies'] else 'Agent2',
    axis=1
)

# Create a column that indicates if Agent1 beeped higher (1) or lower (0)
df['Agent1_Higher'] = (df['Higher_Beep_Agent'] == 'Agent1').astype(int)

# Calculate the probability of each agent beeping higher across all trials and distances
probability_df_1 = df.groupby('Agent1_ID')['Agent1_Higher'].mean().reset_index()
probability_df_1.columns = ['Agent_ID', 'Probability_Higher']

# Add probabilities for Agent2 (1 - Agent1_Higher gives the probability for Agent2)
probability_df_2 = df.groupby('Agent2_ID')['Agent1_Higher'].apply(lambda x: 1 - x.mean()).reset_index()
probability_df_2.columns = ['Agent_ID', 'Probability_Higher']

# Combine the two probabilities
probability_df = pd.concat([probability_df_1, probability_df_2])

# Boxplot of the average probability for each individual agent to beep higher or lower across all trials and distances
plt.figure(figsize=(12, 8))
sns.boxplot(x='Agent_ID', y='Probability_Higher', data=probability_df)
plt.title('Probability of Agents Beeping Higher Across All Trials and Distances')
plt.ylabel('Probability of Beeping Higher')
plt.xlabel('Agent ID')
plt.xticks(rotation=45)
output_folder = "/media/alexmatthews/Alex_011/ZOOL412/week_6/plots"
output_file = os.path.join(output_folder, 'PROBABILITY_BEEP_HIGHER.png')
plt.savefig(output_file)

print(f"Plot saved to {output_file}")
