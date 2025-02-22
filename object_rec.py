from ultralytics import YOLO
import cv2
import std_func as sdf
import numpy

# Decide on model and import a list of possible objects detected by chosen model

model = YOLO("./OBJRECModel/yolov9c.pt")
# Create list of possible objects which can be detected by model

# Capture a single frame from the user's camera / Capture all usable data from an image

def captureFrame(type, image):
    if type == 1:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        results = model(frame)
        return results
    elif type == 2:
        opencvImage = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        results = model(opencvImage)
        return results

# def captureFromImage(image):
#     opencvImage = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
#     results = model(opencvImage)
#     return results

# Creates a dictionary with all detected objects in format {key:num}

def returnFoundObjects(results):
    detected = {}
    for result in results:
        for box in result.boxes:
            sdf.std_dict_addition(detected, model.names[int(box.cls[0])])
    return detected

# Modifies the source image to include confidence score and bounding boxes of objects

def modifyImage(results, image):
    frames = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    for result in results:
        for box in result.boxes:
                # Extract bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                class_id = box.cls[0]
                label = model.names[int(class_id)]

                # Draw bounding box and label on the frame
                cv2.rectangle(frames, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frames, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frames

# Create a window to display modified image (debug)

def displayWindow(modifiedimg):
    cv2.imshow("Image", modifiedimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()