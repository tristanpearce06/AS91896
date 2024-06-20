from ultralytics import YOLO
import cv2
import std_func as sdf

# Decide on model and import a list of possible objects detected by chosen model

model = YOLO("./OBJRECModel/yolov9c.pt")

