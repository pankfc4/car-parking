import argparse
import yaml
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from colors import *
import logging
import numpy as np
import cv2
import time

def main():
    
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    image_file = args.image_file
    data_file = args.data_file
    start_frame = args.start_frame
    
    if image_file is not None:
            with open(data_file, "w+") as points:
                generator = CoordinatesGenerator(image_file, points, COLOR_RED)
                generator.generate()
    
    while(1>0) :
        
        capture_duration = 10
        
        cap = cv2.VideoCapture(1)
        
        start_time = time.time()

        if(cap.isOpened()== False):
            print("error")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('videos/output.mp4', -1, 20.0, (640,480))
        
        while(int(time.time() - start_time) < capture_duration):
            ret, frame = cap.read()
            if ret == True:
                out.write(frame)
                cv2.imshow('Frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
          
        

        with open(data_file, "r") as data:
            points = yaml.load(data,Loader=yaml.FullLoader)
            
            #CALL MotionDetector from motion_detector.py
            detector = MotionDetector(args.video_file, points, int(start_frame))
            detector.detect_motion()
                
def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--image",
                        dest="image_file",
                        required=True,
                        help="Image file to generate coordinates on")
    parser.add_argument("--data",
                        dest="data_file",
                        required=True,
                        help="Data file to be used with OpenCV")
    parser.add_argument("--video",
                        dest="video_file",
                        required=True,
                        help="Video file to detect motion on")
    parser.add_argument("--start-frame",
                        dest="start_frame",
                        required=True,
                        default=1,
                        help="Starting frame on the video")

    return parser.parse_args()


if __name__ == '__main__':
    main()

