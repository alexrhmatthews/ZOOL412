import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Load the combined experiment data
combined_data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
df = pd.read_csv(combined_data_file)
print("shape", df.shape)

# Filter the data to only include the rows for Round 1 and Distance of 2 meters
df_round1_2m = df[(df['Experiment_Round'] == 1) & (df['Distance'] == 2.0)].copy()

# Determine which agent beeped higher at 2 meters in Round 1 and create a mapping
high_at_2m_map = {}
for _, row in tqdm(df_round1_2m.iterrows(), total=df_round1_2m.shape[0], desc="Processing 2m Data"):
    if row['Agent1_Frequencies'] > row['Agent2_Frequencies']:
        high_at_2m_map[row['Agent1_ID']] = 'high'
        high_at_2m_map[row['Agent2_ID']] = 'low'
    else:
        high_at_2m_map[row['Agent2_ID']] = 'high'
        high_at_2m_map[row['Agent1_ID']] = 'low'

# Create a DataFrame to store the probability of beeping high or low in subsequent trials
probability_data = {'Agent_ID': [], 'Probability': [], 'Group': []}

# Loop through each row in the full DataFrame (for all rounds and distances) to calculate probabilities
for agent_id in tqdm(high_at_2m_map.keys(), desc="Calculating Probabilities"):
    agent_data = df[(df['Agent1_ID'] == agent_id) | (df['Agent2_ID'] == agent_id)]
    
    total_trials = len(agent_data)
    if total_trials == 0:
        continue
    
    high_count = 0
    for _, row in agent_data.iterrows():
        if (row['Agent1_ID'] == agent_id and row['Agent1_Frequencies'] > row['Agent2_Frequencies']) or \
           (row['Agent2_ID'] == agent_id and row['Agent2_Frequencies'] > row['Agent1_Frequencies']):
            high_count += 1
    
    probability = high_count / total_trials
    group = high_at_2m_map[agent_id]
    
    probability_data['Agent_ID'].append(agent_id)
    probability_data['Probability'].append(probability)
    probability_data['Group'].append(group)

# Convert the probability data into a DataFrame
df_probability = pd.DataFrame(probability_data)

# Plotting box-and-whisker plots for high and low groups
plt.figure(figsize=(10, 6))
sns.boxplot(x='Group', y='Probability', data=df_probability)
plt.title('Probability of Beeping High in Subsequent Trials\nBased on 2m Distance in Round 1')
plt.xlabel('Group (High or Low at 2m in Round 1)')
plt.ylabel('Probability of Beeping High in Subsequent Trials')
plt.grid(True)

# Save the plot
plt.savefig('/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/PROBABILITY_BEEP_HIGH_LOW_box_2m_round1.PNG')
plt.show()
