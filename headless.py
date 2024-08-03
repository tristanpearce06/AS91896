# Object recognition module test

import object_rec
import chat_model
import image_model

# ret, frame = object_rec.captureFrame()

# modelresults = object_rec.model(frame)

# detected_obj = object_rec.returnFoundObjects(modelresults)

# modified_img = object_rec.modifyImage(modelresults, frame)

# object_rec.displayWindow(modified_img)

# Chat module + object recongition module test

print("Capturing frame")


modelresults = object_rec.captureFrame(1, None)

print("model created")
print("finding objects")

detected_obj = object_rec.returnFoundObjects(modelresults)

print("objects found")

print(detected_obj)

#modified_img = object_rec.modifyImage(modelresults, frame)

#object_rec.displayWindow(modified_img)

print("Generating story")

story = chat_model.gen_story(detected_obj)
print(story)

# Test with image generation

print("Generating image")

image = image_model.generate_image_from_text(story)

image.show()