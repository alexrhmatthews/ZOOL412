import os
import json
from tqdm import tqdm

# Define the filepaths
input_folder = "/projects/sciences/zoology/geurten_lab/alex_stuff/ZOOL412/rot_learning"
output_folder = "/projects/sciences/zoology/geurten_lab/alex_stuff/ZOOL412/rot_learning_processed"
output_file = os.path.join(output_folder, "facing_within_5degrees_for_1_sec.json")

# Initialize a dictionary to store the processed data
processed_data = {}

# Function to process a single file
def process_file(filepath, n_degrees):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    # Clean lines from newline characters and empty lines
    lines = [line.strip() for line in lines if line.strip()]
    
    # Extract metadata
    animal_id = None
    trial_number = None
    learning_odour = None
    odour_positions = {}

    for line in lines:
        if line.startswith("Animal ID:"):
            animal_id = int(line.split(":")[1].strip())
        elif line.startswith("Trial Number:"):
            trial_number = int(line.split(":")[1].strip())
        elif line.startswith("Learning Odour:"):
            learning_odour = line.split(":")[1].strip()
        elif "Position:" in line:
            parts = line.split(",")
            odour_name = parts[0].split(":")[1].strip()
            odour_position = float(parts[1].split(":")[1].strip().replace("°", ""))
            odour_positions[odour_name] = odour_position

    if animal_id is None or trial_number is None or learning_odour is None:
        raise ValueError(f"Missing metadata in file: {filepath}")

    # Determine the learning odour angle
    if learning_odour == "None":
        learning_odour = "Air"
    learning_odour_angle = odour_positions[learning_odour]

    # Extract trajectory data
    trajectory_data_start = lines.index("Trajectory Data (Time, Angle)") + 1
    trajectory_data = []
    for line in lines[trajectory_data_start:]:
        if line.strip() and not line.startswith("----"):  # Skip empty lines and lines with dashes
            try:
                time, angle = map(float, line.split())
                trajectory_data.append((time, angle))
            except ValueError:
                continue
    
    # Find the first timestamp where the angle is within ±n degrees of the learning odour angle for 1 second
    start_time = None
    time_within_range = 0
    for time, angle in trajectory_data:
        if abs(angle - learning_odour_angle) <= n_degrees:
            if start_time is None:
                start_time = time
            time_within_range += 1 / 50  # Each frame is 1/50th of a second
        else:
            start_time = None
            time_within_range = 0

        if time_within_range >= 1:
            break

    if time_within_range < 1:
        # If no valid start time is found, use the latest timestamp
        start_time = trajectory_data[-1][0] if trajectory_data else None

    return {
        "animal_id": animal_id,
        "trial_number": trial_number,
        "learning_odour": learning_odour,
        "start_time": start_time
    }

# Function to process all files in the input folder
def process_all_files(input_folder, output_file, n_degrees):
    # Get a list of all files in the input folder
    files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]

    # Iterate over all files in the input folder with a progress bar
    for filename in tqdm(files, desc="Processing files", unit="file"):
        filepath = os.path.join(input_folder, filename)
        try:
            data = process_file(filepath, n_degrees)
            if data is not None:
                animal_id = data["animal_id"]
                trial_number = data["trial_number"]
                if animal_id not in processed_data:
                    processed_data[animal_id] = {}
                processed_data[animal_id][trial_number] = data
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

    # Save the processed data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(processed_data, json_file, indent=4)

    print(f"Processed data saved to {output_file}")

# Example usage:
# Define the angle (in degrees) for the angle to be within ±n degrees of the learning odour angle
user_defined_n_degrees = 5  # Change this value as needed
process_all_files(input_folder, output_file, user_defined_n_degrees)
