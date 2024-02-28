# read frames and get distibution of confidence
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

def main():

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
            conf = float(max_confidence_line.strip().split()[5])

        return label, conf

    
    def extract_frame_number(filename):
        """Extract and return the frame number from the filename."""
        parts = filename.split('_')
        return int(parts[-1].split('.')[0])


    labels_folder = r'D:\master_output_YOLO_v7_folder\runs\detect\CNO_injection_546\CNO_injection_546.mp4\labels'
    classes_file_path = r'H:\YOLO_v7_weights\classes.txt'


    # get the labels and confidences
    labels = []
    confidences = []

    text_files = sorted(glob.glob(os.path.join(labels_folder, '*.txt')), key=extract_frame_number)
    for txt_file in text_files:
        file_path = os.path.join(txt_file)
        label, conf = read_detections(file_path)
        labels.append(label)
        confidences.append(conf)

    # print the distribution of confidences in a csv
    with open('confidence_distribution.csv', 'w') as f:
        f.write('label,confidence\n')
        for label, confidence in zip(labels, confidences):
            f.write(f'{label},{confidence}\n')
    

    
    # plot the distribution of confidences per label
    plt.figure(figsize=(10, 5))
    plt.scatter(labels, confidences, s=1)
    plt.xlabel('Label')
    plt.ylabel('Confidence')
    plt.title('Confidence per label')
    
    
   # read classes
    with open(classes_file_path, 'r') as f:
        classes = f.readlines()


    # plot the distribution of confidences
    plt.figure(figsize=(10, 5))
    plt.hist(confidences, bins=100)
    plt.xlabel('Confidence')
    plt.ylabel('Frequency')
    plt.title('Distribution of confidences')
    

    # plot distribution of confidences per label in subplots
    plt.figure(figsize=(10, 5))
    # set the color for each class
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
         
    for i in range(1, 8):
        plt.subplot(2, 4, i)
       # plot the distribution of confidences for each class with a different color
        plt.hist([confidences[j] for j in range(len(confidences)) if labels[j] == i-1], bins=100, color=colors[i-1])
        # title corresponding class
        plt.xlabel('Confidence')
        plt.ylabel('Frequency')
        plt.title(classes[i-1])
    plt.show()

    
   
if __name__ == '__main__':
    main()


    

    


