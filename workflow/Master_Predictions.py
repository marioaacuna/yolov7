import os
from functions.script_02__run_predictions import run_detection
from functions.script_03__process_withdrawal_frames import process_detection_blocks
import tkinter as tk
from tkinter import filedialog

def main():
    # Ask the user for the folder containing videos
    def select_folder():
        root = tk.Tk()
        root.withdraw()  # Hide the main window.
        folder_path = filedialog.askdirectory()  # Show the dialog and return the selected folder path.
        return folder_path
    

    # Ask the user to select the file containing the weights with a title
    def select_weights_file():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path
    
    # Get the weights file
    print('Select the weights file to use for detection.')
    weights_file = select_weights_file()
    print(f"Selected weights file: {weights_file}")

    # Get video folder
    print('Select the folder containing the videos to process.')
    video_folder = select_folder()
    print(f"Selected folder: {video_folder}")

    # Get the classes for this project located in the same folder as the weights file
    classes_file_path = os.path.join(os.path.dirname(weights_file), 'classes.txt')

    # Master folder for all outputs
    # check if it's a macOS or windows path
    if os.name == 'posix':
        master_output_folder = '/Users/Shared/master_output_YOLO_v7_folder'
    else:
        master_output_folder = 'D:/master_output_YOLO_v7_folder'

    os.makedirs(master_output_folder, exist_ok=True)

    # Parameters for processing detection blocks
    # set variables for the detection
    frame_rate = 30
    min_consecutive_frames = frame_rate * 0.10  # 0.1 second worth of frames
    min_gap_between_blocks = frame_rate * 20  # 20 seconds worth of frames
    withdraw_frames = int(frame_rate * 0.07)  # 70 ms before end of block

    # Iterate through the videos in the provided folder
    for video_name in os.listdir(video_folder):
        if video_name.endswith('.mp4'):  # or other video formats as needed
            video_path = os.path.join(video_folder, video_name)
            
            # Define the project folder for the current video
            project_folder = os.path.join(master_output_folder,  'runs/detect', os.path.splitext(video_name)[0])
            os.makedirs(project_folder, exist_ok=True)
            
            # Define the folder containing the labels
            labels_folder = os.path.join(project_folder,video_name, 'labels')
            if os.path.exists(labels_folder):
                print(f"Labels folder already exists for {video_name}. Skipping detection.")
                continue
            
            # Define the output CSV path
            output_csv_path = os.path.join(project_folder, 'blocks_with_withdrawal_frames.csv')
            
             
            # Run detection on the video
            print(f"\n{'*'*50}\n")
            print(f"Running detection on {video_name}...")
            run_detection(video_name=video_name, 
                          source_path=video_folder, 
                          project_folder=project_folder,
                          weights=weights_file, 
                          device='0')  # Add other parameters as needed

            # Process the detection blocks
            print(f"Processing detection blocks for {video_name}...")
            process_detection_blocks(labels_folder=labels_folder, 
                                     classes_file_path=classes_file_path, 
                                     output_csv_path=output_csv_path, 
                                     min_consecutive_frames = min_consecutive_frames,
                                     min_gap_between_blocks=min_gap_between_blocks,
                                     withdraw_frames=withdraw_frames
                                     )

if __name__ == '__main__':
    main()
