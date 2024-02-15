#from yolov7 import  train_aux
#from train_aux import train_aux
import subprocess

# Set the working directory to the directory containing train_aux.py
working_directory = f'C:/Users/acuna/Repositories/yolov7'


# Set training variables
workers = 8
device = 0  # Updated to device 0 as per your command
batch_size = 16
data = 'data/custom_01.yaml'
img_size = 704  # Updated to the sizes given in your command
cfg = 'cfg/training/yolov7-e6-custom.yaml'
weights = 'models/yolov7-e6_training.pt'
name = 'yolov7-e6-custom'  # Updated to match the name in your command
hyp = 'data/hyp.scratch.p6_custom.yaml'  # Updated to the new hyp file
epochs = 100  # Updated to the number of epochs you want to train for

# Command line arguments as a list of strings
args = [
    'conda', 'run', '-n', 'env_Yolo7', 'python', 'train_aux.py',
    '--workers', str(workers),
    '--device', str(device),
    '--batch-size', str(batch_size),
    '--data', data,
    '--img', str(img_size),
    '--cfg', cfg,
    '--weights', weights,
    '--name', name,
    '--hyp', hyp,
    '--epochs', str(epochs)
]

# Run the train_aux.py script with the specified arguments in the env_Yolo7 conda environment
subprocess.run(args, cwd=working_directory)
print('All done with training!')



'''
python train_aux.py --workers 8 --device 0 --batch-size 16 --data data/custom_01.yaml --img 1280 720 --cfg cfg/training/yolov7-e6-custom.yaml --weights 'models/yolov7-e6_training.pt' --name yolov7-w6-custom --hyp data/hyp.scratch.p6_custom.yaml
'''

''' From the bash script create a python function:
python export.py --weights yolov7-tiny.pt --grid --end2end --simplify \
        --topk-all 100 --iou-thres 0.65 --conf-thres 0.35 --img-size 640 640 --max-wh 640
        '''

""" import export

export_weights = 'yolov7-e6-custom.pt'
grid = True
end2end = True
simplify = True
topk_all = 100
iou_thres = 0.65
conf_thres = 0.35
#img_size = [640, 640]
max_wh = 640

export.export(export_weights,
              grid, 
              end2end, 
              simplify, 
              topk_all, 
              iou_thres, 
              conf_thres, 
              img_size, 
              max_wh)

 """