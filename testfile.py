import object_rec

ret, frame = object_rec.captureFrame()

modelresults = object_rec.model(frame)

detected_obj = object_rec.returnFoundObjects(modelresults)

modified_img = object_rec.modifyImage(modelresults, frame)

object_rec.displayWindow(modified_img)

