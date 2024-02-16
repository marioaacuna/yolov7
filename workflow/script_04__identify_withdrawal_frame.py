import os
import glob
import csv
from itertools import groupby

# Constants
labels_folder = 'D:/_test_YOLOv7/eval_vids/runs/detect/exp/labels'
frame_rate = 30
min_consecutive_frames = frame_rate * 0.5  # 1 second worth of frames
withdraw_frames = int(frame_rate * 0.5)  # 500 ms worth of frames
output_csv_path = 'D:/_test_YOLOv7/eval_vids/runs/detect/exp/blocks_with_withdrawal_frames.csv'

# Helper function to read detections from a file
def read_detections(file_path):
    with open(file_path, 'r') as f:
        return [int(line.strip().split()[0]) for line in f]

# Process detections into blocks
blocks = {}
for txt_file in glob.glob(os.path.join(labels_folder, '*.txt')):
    base_name = os.path.basename(txt_file)
    video_name, frame_number = base_name.rsplit('_', 1)
    frame_number = int(frame_number.split('.')[0])

    label = read_detections(txt_file)[0]
    if label not in blocks:
        blocks[label] = []

    # Add frame to the corresponding label block if it's consecutive
    if blocks[label] and frame_number - blocks[label][-1][-1] == 1:
        blocks[label][-1].append(frame_number)
    else:
        blocks[label].append([frame_number])

# Filter out blocks that don't last at least 1 second
blocks = {label: [block for block in blocks_list if len(block) >= min_consecutive_frames]
          for label, blocks_list in blocks.items()}

# Determine the withdrawal frame for each block
withdrawal_frames = {label: [block[-withdraw_frames] for block in blocks_list]
                     for label, blocks_list in blocks.items()}

# Write the results to a CSV file
with open(output_csv_path, 'w', newline='') as csvfile:
    fieldnames = ['Label', 'Block_Start', 'Block_End', 'Withdrawal_Frame']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for label, blocks_list in blocks.items():
        for block in blocks_list:
            writer.writerow({
                'Label': label,
                'Block_Start': block[0],
                'Block_End': block[-1],
                'Withdrawal_Frame': block[-withdraw_frames]
            })

print(f"Results saved to {output_csv_path}")
