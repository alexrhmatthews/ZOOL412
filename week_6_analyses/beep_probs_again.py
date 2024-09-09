import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Load the combined experiment data
combined_data_file = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/combined_experiment_data_with_names.csv"
df = pd.read_csv(combined_data_file)
print("shape", df.shape)

# Sort the DataFrame by Agent_ID and Pair_ID to ensure sequential order of trials
df = df.sort_values(by=['Agent1_ID', 'Agent2_ID', 'Pair_ID', 'Distance']).reset_index(drop=True)

# Create lists to store the probabilities
prob_higher_given_higher = []
prob_higher_given_lower = []

# Iterate through the data to calculate probabilities
for agent_id in df['Agent1_ID'].unique():
    agent_data = df[(df['Agent1_ID'] == agent_id) | (df['Agent2_ID'] == agent_id)].reset_index(drop=True)
    total_trials = len(agent_data)
    
    if total_trials < 2:
        continue  # Skip agents with less than 2 trials

    for i in range(total_trials - 1):
        current_trial = agent_data.iloc[i]
        next_trial = agent_data.iloc[i + 1]

        current_beep_higher = (current_trial['Agent1_ID'] == agent_id and current_trial['Agent1_Frequencies'] > current_trial['Agent2_Frequencies']) or \
                              (current_trial['Agent2_ID'] == agent_id and current_trial['Agent2_Frequencies'] > current_trial['Agent1_Frequencies'])

        next_beep_higher = (next_trial['Agent1_ID'] == agent_id and next_trial['Agent1_Frequencies'] > next_trial['Agent2_Frequencies']) or \
                           (next_trial['Agent2_ID'] == agent_id and next_trial['Agent2_Frequencies'] > next_trial['Agent1_Frequencies'])

        if current_beep_higher:
            prob_higher_given_higher.append(1 if next_beep_higher else 0)
        else:
            prob_higher_given_lower.append(1 if next_beep_higher else 0)

# Convert to DataFrame for plotting
df_probabilities = pd.DataFrame({
    'Probability': prob_higher_given_higher + prob_higher_given_lower,
    'Condition': ['Beeped Higher in Current Trial'] * len(prob_higher_given_higher) + ['Beeped Lower in Current Trial'] * len(prob_higher_given_lower)
})

# Plotting box-and-whisker plots
plt.figure(figsize=(10, 6))
sns.boxplot(x='Condition', y='Probability', data=df_probabilities)
plt.title('Probability of Beeping Higher in the Next Trial\nBased on Current Trial Outcome')
plt.xlabel('Current Trial Outcome')
plt.ylabel('Probability of Beeping Higher in Next Trial')
plt.grid(True)

# Save the plot
plt.savefig('/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results/PROBABILITY_NEXT_TRIAL_BEEP_HIGHER.PNG')
plt.show()
