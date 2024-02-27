# script_03__process_withdrawal_frames.py

import os
import glob
import csv

def process_detection_blocks(labels_folder, classes_file_path, min_consecutive_frames=3, min_gap_between_blocks=600, withdraw_frames=2, output_csv_path='blocks_with_withdrawal_frames.csv'):
    """
    Processes detection blocks to identify withdrawal frames.
    
    :param labels_folder: Directory containing detection label files.
    :param classes_file_path: Path to the file containing class names.
    :param min_consecutive_frames: Minimum number of consecutive frames for a valid block.
    :param min_gap_between_blocks: Minimum gap between blocks, in frames.
    :param withdraw_frames: Number of frames before the last detection to mark as withdrawal.
    :param output_csv_path: Path to save the CSV output.
    """
    def extract_frame_number(filename):
        parts = filename.split('_')
        return int(parts[-1].split('.')[0])

    def read_detections(file_path):
        with open(file_path, 'r') as f:
            # read the row with max confidence (6th column)
            lines = f.readlines()
            # check if lines > 1 

            max_confidence = 0
            for line in lines:
                confidence = float(line.split()[5])
                if confidence > max_confidence:
                    max_confidence = confidence
                    max_confidence_line = line
            
            if len(lines) > 1:
                print(max_confidence_line)
                #exit()

            return int(max_confidence_line.strip().split()[0])
       
            

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
        
        if blocks[label] and frame_number - blocks[label][-1][-1] <= 1:
            blocks[label][-1].append(frame_number)
        else:
            if not blocks[label] or frame_number - blocks[label][-1][-1] >= min_gap_between_blocks:
                blocks[label].append([frame_number])

    # Filter out blocks that don't last at least the minimum consecutive frames
    blocks = {label: [block for block in blocks_list if len(block) >= min_consecutive_frames] for label, blocks_list in blocks.items()}

    # Prepare output rows
    output_rows = []
    for label, blocks_list in blocks.items():
        for block in blocks_list:
            withdrawal_frame = block[-1] - withdraw_frames if (block[-1] - block[0] > withdraw_frames) else block[0]
            class_name = class_names[label] if label < len(class_names) else f"Unknown label {label}"
            output_rows.append({
                'Label': class_name,
                'Block_Start': block[0],
                'Block_End': block[-1],
                'Withdrawal_Frame': withdrawal_frame
            })

    # Sort and write to CSV
    output_rows.sort(key=lambda x: x['Block_Start'])
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Label', 'Block_Start', 'Block_End', 'Withdrawal_Frame']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow(row)

    print(f"Results saved to {output_csv_path}")

if __name__ == '__main__':
    # Example usage
    labels_folder = 'H:/Mario/YOLOv7_postdetection/CNO_injection_548/labels'
    classes_file_path = 'H:/YOLO_v7_weights/classes.txt'
    frame_rate = 30
    min_consecutive_frames = frame_rate * 0.10  # 0.1 second worth of frames
    min_gap_between_blocks = frame_rate * 20  # 20 seconds worth of frames
    withdraw_frames = int(frame_rate * 0.07)  # 70 ms before end of block

    process_detection_blocks(labels_folder, 
                             classes_file_path,
                             min_consecutive_frames,
                             min_gap_between_blocks,
                             withdraw_frames)
