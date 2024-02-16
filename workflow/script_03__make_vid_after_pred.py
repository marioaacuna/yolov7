import cv2
import os
import glob

# Define the paths
labels_folder = 'D:/_test_YOLOv7/eval_vids/runs/detect/exp/labels'
video_folder = 'D:/_test_YOLOv7/eval_vids'
classes_file_path = 'C:/Users/acuna/Repositories/yolov7/classes.txt'

# Read class names from classes.txt
with open(classes_file_path, 'r') as file:
    classes = [line.strip() for line in file.readlines()]

# Function to extract video name and frame number from the text file name
def extract_info_from_filename(filename):
    parts = filename.split('_')
    frame_number = int(parts[-1].split('.')[0])
    video_name = '_'.join(parts[:-1])
    return video_name, frame_number

# Get the list of text files with detections
text_files = glob.glob(os.path.join(labels_folder, '*.txt'))
# Sort the text files by frame number to process in order
text_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

# Assuming there is only one source video
video_name = extract_info_from_filename(os.path.basename(text_files[0]))[0]
source_video_path = os.path.join(video_folder, f"{video_name}.mp4")

# Read the source video
cap = cv2.VideoCapture(source_video_path)
if not cap.isOpened():
    raise Exception(f"Failed to open video: {source_video_path}")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Set up the output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_video_path = os.path.join(video_folder, f"{video_name}_output.mp4")
out = cv2.VideoWriter(out_video_path, fourcc, fps, (width, height))

# Process each text file and frame
for txt_file in text_files:
    _, frame_number = extract_info_from_filename(os.path.basename(txt_file))
    
    # Move to the specific frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)

    # Read the frame
    ret, frame = cap.read()
    if not ret:
        print(f"Failed to get frame number {frame_number} from video {source_video_path}")
        continue

    # Read detection from the text file
    with open(txt_file, 'r') as f:
        detection = f.readline().strip()
        label, x_center, y_center, bbox_width, bbox_height, prob = map(float, detection.split())

        # Convert from relative to absolute coordinates
        x = int((x_center - bbox_width / 2) * width)
        y = int((y_center - bbox_height / 2) * height)
        w = int(bbox_width * width)
        h = int(bbox_height * height)

        # Draw the bounding box and label on the frame
        label_text = f"{classes[int(label)]} {prob:.2f}"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label_text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the frame to the output video
    out.write(frame)

# Release the video capture and writer
cap.release()
out.release()

print('Video processing completed.')
