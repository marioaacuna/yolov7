# in case to be run from the command line, the following command should be used:
#! python train_aux.py --workers 8 --device 0 --batch-size 16 --data D:/YOLOv7_training/training_configs.yaml --img 704 --cfg cfg/training/yolov7-e6-custom.yaml --weights models/yolov7-e6_training.pt --name pain_and_anxiety --hyp data/hyp.scratch.p6_custom.yaml --epochs 100 --project, D:/YOLOv7_training

import subprocess
import os
from Utilities.get_conda_env import get_conda_env_path

# Set the working directory to the directory containing train_aux.py
working_directory = f'C:/Users/acuna/Repositories/yolov7/'

# Define the path to the Python interpreter in the env_Yolo7 Conda environment
# Adjust this path to the actual location of your Conda environment's Python interpreter

env_name = 'env_yolo7'
env_path = get_conda_env_path(env_name)
if env_path:
    env_python_path = os.path.join(env_path, 'python')
    #print(f'Python path for {env_name}: {env_python_path}')
else:
    print(f'Conda environment {env_name} not found.')
    KeyError( f'Conda environment {env_name} not found.')

# Set training variables
workers = 8
device = 0  #
batch_size = 16
data = 'D:/YOLOv7_training/training_configs.yaml'
img_size = 704  # Updated to the sizes given in your command
cfg = './cfg/training/yolov7-e6-custom.yaml'
weights = './models/yolov7-e6_training.pt'
#name = 'yolov7-e6-custom'  # Updated to match the name in your command
hyp = './data/hyp.scratch.p6_custom.yaml'  # Updated to the new hyp file
epochs = 100  # Updated to the number of epochs you want to train for
project_folder = 'D:/YOLOv7_training'  # Updated to the project folder you want to use
name = 'pain_and_anxiety'


############################################################################################################
# Train the model
# Then run the training script

# Command line arguments as a list of strings
args = [env_python_path, 'train_aux.py',
    '--workers', str(workers),
    '--device', str(device),
    '--batch-size', str(batch_size),
    '--data', data,
    '--img', str(img_size),
    '--cfg', cfg,
    '--weights', weights,
    '--name', name,
    '--hyp', hyp,
    '--epochs', str(epochs),
    '--project', project_folder
]
# Execute the subprocess with the constructed arguments
print('Running training...')
process = subprocess.Popen(args, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# Be aware of the cache in the training folder, if your training is not working, try to delete the cache folder in the training folder
# 


# Wait for the command to complete and capture the output
stdout, stderr = process.communicate()

# Print the outputs
print(stdout)
print(stderr)

# decorate the output with stars
print('*' * 80)
print('All done with training!')
