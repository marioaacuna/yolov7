import os
import glob
import csv

# Constants
labels_folder = 'D:/_test_YOLOv7/eval_vids/runs/detect/exp/labels'
frame_rate = 30
min_consecutive_frames = frame_rate * 0.10  # 1 second worth of frames
min_gap_between_blocks = frame_rate * 20  # 20 seconds worth of frames
withdraw_frames = int(frame_rate * 0.07)  # 500 ms worth of frames
output_csv_path = 'blocks_with_withdrawal_frames.csv'
classes_file_path = 'C:/Users/acuna/Repositories/yolov7/classes.txt'

# Helper functions
def extract_frame_number(filename):
    """Extract and return the frame number from a filename."""
    parts = filename.split('_')
    return int(parts[-1].split('.')[0])

def read_detections(file_path):
    """Read detections from a file and return the label."""
    with open(file_path, 'r') as f:
        return int(f.readline().strip().split()[0])

# Read class names from classes.txt
with open(classes_file_path, 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# Process detections into blocks
blocks = {}
text_files = sorted(glob.glob(os.path.join(labels_folder, '*.txt')), key=extract_frame_number)
for txt_file in text_files:
    frame_number = extract_frame_number(os.path.basename(txt_file))
    label = read_detections(txt_file)
    
    if label not in blocks:
        blocks[label] = []
    
    # Check if the frame is consecutive or if a new block should start
    if blocks[label] and frame_number - blocks[label][-1][-1] <= 1:
        blocks[label][-1].append(frame_number)
    else:
        # Start a new block if enough time has passed
        if not blocks[label] or frame_number - blocks[label][-1][-1] >= min_gap_between_blocks:
            blocks[label].append([frame_number])

# Filter out blocks that don't last at least 1 second
blocks = {label: [block for block in blocks_list if len(block) >= min_consecutive_frames] for label, blocks_list in blocks.items()}

# Before writing to CSV, collect all rows in a list
output_rows = []
for label, blocks_list in blocks.items():
    for block in blocks_list:
        withdrawal_frame = block[-1] - withdraw_frames if (block[-1] - block[0] > withdraw_frames) else block[0]
        # Use the class name instead of the label index
        class_name = class_names[label] if label < len(class_names) else f"Unknown label {label}"
        output_rows.append({
            'Label': class_name,
            'Block_Start': block[0],
            'Block_End': block[-1],
            'Withdrawal_Frame': withdrawal_frame
        })

# Sort the rows by Block_Start frame number, then write to CSV as before
output_rows.sort(key=lambda x: x['Block_Start'])

with open(output_csv_path, 'w', newline='') as csvfile:
    fieldnames = ['Label', 'Block_Start', 'Block_End', 'Withdrawal_Frame']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in output_rows:
        writer.writerow(row)

print(f"Results saved to {output_csv_path}")