import os
import cv2
import numpy as np
import csv
from tqdm import tqdm

def process_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    left_sum = 0
    right_sum = 0
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray_frame.shape
        left_half = gray_frame[:, :width//2]
        right_half = gray_frame[:, width//2:]

        left_sum += np.sum(left_half)
        right_sum += np.sum(right_half)
        frame_count += 1

    cap.release()

    # Calculate the average brightness
    left_brightness = left_sum / (frame_count * left_half.size)
    right_brightness = right_sum / (frame_count * right_half.size)

    return left_brightness, right_brightness

def main(root_dir, output_csv):
    video_files = []
    
    # Collect all video files
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".mp4"):
                video_files.append(os.path.join(root, file))

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Experiment_Round', 'Pair_ID', 'agent_number', 'distance', 'left_brightness', 'right_brightness'])

        # Add progress bar
        for video_path in tqdm(video_files, desc="Processing videos"):
            # Extract details from the path and filename
            path_parts = video_path.split(os.sep)
            experiment_round_str = path_parts[-4]
            experiment_number_str = path_parts[-3]
            filename_parts = os.path.basename(video_path).split('_')
            agent_number = filename_parts[2][-1]  # Extracts '1' or '2'
            distance = filename_parts[-1].split('.')[0]  # Extracts distance like '0.25m'

            # Convert round and experiment strings to numerical values
            experiment_round = int(experiment_round_str.split('_')[-1])
            pair_id = int(experiment_number_str.split('_')[-1])

            # Process the video to get brightness
            left_brightness, right_brightness = process_video(video_path)

            # Write the results to the CSV file
            writer.writerow([experiment_round, pair_id, agent_number, distance, left_brightness, right_brightness])

if __name__ == "__main__":
    root_directory = "/media/alexmatthews/Alex_011/ZOOL412/week_6/Experiment_Results"  # Update to the correct path
    output_csv_path = "experiment_video_analysis.csv"
    main(root_directory, output_csv_path)
