# Object recognition module test

import object_rec
import chat_model

# ret, frame = object_rec.captureFrame()

# modelresults = object_rec.model(frame)

# detected_obj = object_rec.returnFoundObjects(modelresults)

# modified_img = object_rec.modifyImage(modelresults, frame)

# object_rec.displayWindow(modified_img)

# Chat module + object recongition module test

print("Capturing frame")

ret, frame = object_rec.captureFrame()

print("frame captured")
print("creating model")

modelresults = object_rec.model(frame)

print("model created")
print("finding objects")

detected_obj = object_rec.returnFoundObjects(modelresults)

print("objects found")

print(detected_obj)

modified_img = object_rec.modifyImage(modelresults, frame)

object_rec.displayWindow(modified_img)

print(chat_model.gen_story(detected_obj))