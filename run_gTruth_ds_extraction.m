% this script will evaluate the YoloX network in data from videos already
% concatenated. 
clc
clear
close all
global GC
% GC = general_configs();
%% set the version
version = 'X';
rootpath = GC.repo_path; 
% if ispc
%     root_path = 'C:\Users\acuna\OneDrive - Universitaet Bern\Coding_playground\Anna_playground\';
% else
%     keyboard
% end

addpath(genpath('Object_detection_scripts\utilities'))

% load the ground truths
gt_path = 'D:\stimulus_labeler';
% gt_path = 'H:\Mario\BioMed_students_2023\Anna\Playground\YOLO_paincohort';
% check how many *.mat files are in the folder
files = dir(fullfile(gt_path, '*.mat'));
n_files = length(files);

% Load the GT
% load(fullfile(gt_path, ['gTruth_', num2str(i), '.mat']));
load(fullfile(gt_path, ['gTruth_conc_2.mat']));
% Set where to save the images
write_loc = fullfile(gt_path, 'Yolov7', 'images');
if ~exist(write_loc, 'dir')
    mkdir(write_loc)
end

% Make training data
[imds, bxds] = objectDetectorTrainingData(gTruth, 'WriteLocation', ...
    write_loc); % Unique WriteLocation for each

% Ensure the 'labels' folder exists; if not, create it
labels_folder = fullfile(gt_path, 'Yolov7', 'labels');

if ~exist(labels_folder, 'dir')
    mkdir(labels_folder)
end
% crete the labels

class_names = {'vF_purple', 'cold', 'hot', 'vF_blue', 'vF_green', 'pinprick'};
fileID = fopen(fullfile(labels_folder,'classes.txt'),'w');
fprintf(fileID,'%s\n', class_names{:});
fclose(fileID);


%%
% Iterate over each entry in the boxLabelDatastore
for i = 1:size(bxds.LabelData, 1)
    % Extract the file name and use it to name the label file
    [~, name, ~] = fileparts(imds.Files{i});
    labelFileName = fullfile(labels_folder, [name '.txt']);
    
    % Open the file for writing
    fileID = fopen(labelFileName, 'w');
    
    % Retrieve bounding box and class label for the current image
    bboxes = bxds.LabelData{i, 1}; % Bounding boxes
    labels = bxds.LabelData{i, 2}; % Class labels
    j = i;
    % for j = 1:size(bboxes, 1)
        % Find the index of the current label in class_names
        classIndex = find(strcmp(class_names, char(labels)));
        
        % Convert bounding box from [x y width height] to the desired format
        % Here, you might need to adjust the format based on your specific requirements
        % For YOLO, it's typically [center_x center_y width height] normalized by image dimensions
        bbox = bboxes;
        [imgHeight, imgWidth, ~] = size(imread(imds.Files{i}));
        centerX = (bbox(1) + bbox(3) / 2) / imgWidth;
        centerY = (bbox(2) + bbox(4) / 2) / imgHeight;
        width = bbox(3) / imgWidth;
        height = bbox(4) / imgHeight;
        
        % Write to file: classIndex, centerX, centerY, width, height
        fprintf(fileID, '%d %.6f %.6f %.6f %.6f\n', classIndex-1, centerX, centerY, width, height);
    % end
    
    % Close the file
    fclose(fileID);
end
