import glob
import os
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
        """Extract and return the frame number from the filename."""
        parts = filename.split('_')
        return int(parts[-1].split('.')[0])

    def read_detections(file_path):
        """Read detections from a file and return the label with the highest confidence along with the frame number."""
        with open(file_path, 'r') as f:
            lines = f.readlines()
            max_confidence = 0
            max_confidence_line = None
            for line in lines:
                confidence = float(line.split()[5])
                if confidence > max_confidence:
                    max_confidence = confidence
                    max_confidence_line = line
            label = int(max_confidence_line.strip().split()[0])
        return label

    def process_files(labels_folder):
        """Process all text files in the given folder and return a list of (label, frame_id) pairs."""
        label_frame_pairs = []
        text_files = sorted(glob.glob(os.path.join(labels_folder, '*.txt')), key=extract_frame_number)
        for txt_file in text_files:
            frame_number = extract_frame_number(os.path.basename(txt_file))
            label = read_detections(txt_file)
            label_frame_pairs.append((label, frame_number))
        return label_frame_pairs


    def correct_consecutive_glitches_with_removal(label_frame_pairs, gap_threshold=600, no_label_id=0):
        """
        Correct glitches that span 2 or 3 consecutive frames and remove isolated labels in the sequence of label-frame pairs.

        Args:
        - label_frame_pairs: A list of tuples (label, frame_id).
        - gap_threshold: The minimum frame gap considered as a valid separation between blocks.
        - no_label_id: The label ID used for frames with no label (assumed to be 0).

        Returns:
        - A list of corrected label-frame pairs with isolated labels removed.
        """
        corrected_pairs = []
        n = len(label_frame_pairs)
        
        # Initialize pointers for scanning through the label-frame pairs
        i = 0
        while i < n:
            current_label, current_frame = label_frame_pairs[i]

            # Check for previous and next labels, considering the boundaries of the list
            prev_label = label_frame_pairs[i-1][0] if i > 0 else no_label_id
            next_label = label_frame_pairs[i+1][0] if i < n - 1 else no_label_id

            # Identify if the current label is isolated
            if current_label != no_label_id and prev_label == no_label_id and next_label == no_label_id:
                # Skip this label to effectively remove it from the sequence
                i += 1
                continue

            # Rest of the logic for correcting glitches remains the same
            # Check for a glitch in 2 or 3 consecutive frames
            is_glitch = False
            if i < n - 2:
                # If next two frames are the same and different from current
                is_glitch = (label_frame_pairs[i+1][0] == label_frame_pairs[i+2][0] and current_label != label_frame_pairs[i+1][0])
            if i < n - 3 and not is_glitch:
                # If next three frames are the same and different from current
                is_glitch = (label_frame_pairs[i+1][0] == label_frame_pairs[i+2][0] == label_frame_pairs[i+3][0] and current_label != label_frame_pairs[i+1][0])

            if is_glitch:
                # Correct the glitch to the label that occurs in the next 2 or 3 frames
                corrected_label = label_frame_pairs[i+1][0]
                corrected_pairs.append((corrected_label, current_frame))
            else:
                # If no glitch is detected, append the current label-frame pair
                corrected_pairs.append((current_label, current_frame))

            i += 1

        return corrected_pairs



    def process_blocks(corrected_label_frame_pairs, min_consecutive_frames=12, withdraw_frames=1, min_gap_between_blocks=600, classes_file_path='classes.txt'):
        # Sort the list by frame number
        corrected_label_frame_pairs.sort(key=lambda pair: pair[1])
        
        # Initialize blocks list
        blocks = []
        current_block = []

        # Process corrected_label_frame_pairs into blocks
        for label, frame_number in corrected_label_frame_pairs:
            if not current_block:
                # Start a new block if current_block is empty
                current_block = [label, frame_number, frame_number]  # label, start, end
            else:
                # Check if current frame continues the last block or starts a new block
                if label == current_block[0] and frame_number - current_block[2] == 1:
                    # Continue the block
                    current_block[2] = frame_number  # Update the end of the current block
                else:
                    # Check if the last block was long enough to be considered a block and had a sufficient gap
                    if (current_block[2] - current_block[1] + 1) >= min_consecutive_frames:
                        # Check if there is a sufficient gap from the next block
                        if not blocks or frame_number - blocks[-1][2] >= min_gap_between_blocks:
                            blocks.append(current_block)
                    # Start a new block
                    current_block = [label, frame_number, frame_number]

        # Check the last block
        if current_block and (current_block[2] - current_block[1] + 1) >= min_consecutive_frames:
            blocks.append(current_block)

        
        # Read class names from classes.txt
        with open(classes_file_path, 'r') as f:
            class_names = [line.strip() for line in f.readlines()]


        
        # Prepare output rows for CSV
        output_rows = []
        for block in blocks:
            label, start, end = block
            withdrawal_frame = end - withdraw_frames if (end - start + 1) > withdraw_frames else start
            # Get the class name using the label
            class_name = class_names[label] if label < len(class_names) else f"Unknown label {label}"
            output_rows.append({
                'Label': class_name,
                'Block_Start': start,
                'Block_End': end,
                'Withdrawal_Frame': withdrawal_frame
            })

        return output_rows

    # Process the label-frame pairs
    print('Running process_files...%s' % labels_folder)
    label_frame_pairs = process_files(labels_folder)

    # Apply the correction for consecutive glitches
    corrected_label_frame_pairs = correct_consecutive_glitches_with_removal(label_frame_pairs, gap_threshold=min_gap_between_blocks)

    # Process the corrected label-frame pairs into blocks
    output_rows = process_blocks(corrected_label_frame_pairs, min_consecutive_frames, withdraw_frames, min_gap_between_blocks, classes_file_path)

    # Write to CSV
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
    min_consecutive_frames = frame_rate * 0.4  # 0.4 second worth of frames
    min_gap_between_blocks = frame_rate * 20  # 20 seconds worth of frames
    withdraw_frames = int(frame_rate * 0.07)  # 70 ms before end of block
    output_csv_path = os.path.join(labels_folder, 'blocks_with_withdrawal_frames.csv')

    process_detection_blocks(labels_folder, 
                             classes_file_path,
                             min_consecutive_frames,
                             min_gap_between_blocks,
                             withdraw_frames,
                             output_csv_path)


"""
## Debugging
import matplotlib.pyplot as plt

# Extract frame IDs and labels from the original and corrected sequences
original_labels, original_frames = zip(*label_frame_pairs)
corrected_labels, corrected_frames = zip(*corrected_label_frame_pairs)

# Create the plot
plt.figure(figsize=(20, 6))  # Adjust the size for better visibility

# Plot original sequence
#plt.plot(original_frames, original_labels, color='red', alpha=0.7, label='Original Labels', marker='o', linestyle='-', markersize=2)

# Plot corrected sequence
plt.plot(corrected_frames, corrected_labels, color='green', alpha=0.7, label='Corrected Labels', marker='x', linestyle='-', markersize=2)

# Enhancements for better understanding
plt.title('Original vs. Corrected Label Sequences Over Time')
plt.xlabel('Frame ID')
plt.ylabel('Label')
plt.legend()

# Set the y-axis to show the label range
plt.ylim(0, 6)

# Show grid for better visibility
plt.grid(True)

# Display the plot
plt.show()



# The label_frame_pairs list now contains (label, frame_id) pairs for further processing.
"""