import detect

# set weights to use
weights = 'yolov7.pt'

# set confidence threshold (0-1)
conf = 0.25

# set image size same as training
img_size = 1280

# set source to video file
source = 'yourvideo.mp4'

# detect video
def detect_video(weights, conf, img_size, source):
    detect.detect(weights, conf, img_size, source)

detect_video(weights, conf, img_size, source)
