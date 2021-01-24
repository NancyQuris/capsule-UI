import cv2
import os

def frame_cutting(path):
    current_working_dir = os.getcwd()
    video_name = get_video_name(path)
    if not os.path.isdir(video_name) :
    	os.mkdir(video_name)
    video_capture = cv2.VideoCapture(path)
    success, image = video_capture.read()
    count = 0
    while success:
        cv2.imwrite(current_working_dir + "/" + video_name + "/%d.jpg" % count, image)
        success, image = video_capture.read()
        count += 1
    video_capture.release()
    print("frame cutting success")


def get_video_name(path):
	path_length = len(path)
	position_of_last_slash = 0
	for i in range(path_length - 1, -1, -1):
		current_char = path[i]
		if current_char == '/':
			position_of_last_slash = i + 1
			break
	return path[position_of_last_slash:]
