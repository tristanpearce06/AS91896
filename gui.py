import tkinter
from tkinter import CENTER
import tkinter.messagebox
import customtkinter as tk
from PIL import Image
import threading # Used to multithread tasks which use an extended period to process so that the GUI does not freeze during processing
import cv2 # Used to display webcam feed on the Camera Input page

import std_func as sdf
import object_rec
import chat_model
import image_model

tk.set_appearance_mode("system")
tk.set_default_color_theme("blue")

privacyText = "Placeholder privacy text lol real is this real chat what lol seriously yo thats actually crazy what???"

class app(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Photo Story")
        self.geometry("550x650")

        self.container = tk.CTkFrame(self)
        self.container.pack(anchor=CENTER, expand=True)

        self.uploadedImage = None
        self.generatedImage = None
        self.detectedImage = None
        self.objectsDict = None
        self.genStory = None

        self.frames = {}

        for Fr in (HomePage, PrivacyPage, ImageInputPage, CameraInputPage, InputSelect, ObjectRecPage, StoryGenerator, ImageGenerator, FinalPage):
            PageName = Fr.__name__
            frame = Fr(parent=self.container, controller=self)
            self.frames[PageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, pName):
        frame = self.frames[pName]
        if pName == "ObjectRecPage" and self.uploadedImage:
            frame.update_image(self.uploadedImage)
        elif pName == "StoryGenerator" and self.objectsDict:
            frame.updateObjList(self.objectsDict)
        elif pName == "ImageGenerator":
            self.geometry("1050x650")
            frame.createStoryFrame()
        elif pName == "FinalPage":
            frame.createSecondColumn()

        frame.tkraise()

class HomePage(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.mainTitle = tk.CTkLabel(self, text="One Click Story", font=tk.CTkFont("Segoe", 60, "normal"))
        
        self.centerFrame = tk.CTkFrame(self, border_width=1, height=700)
        self.centerFrame.grid_columnconfigure(0, weight=1)
        self.startButton = tk.CTkButton(self.centerFrame, text="Start", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("InputSelect"))
        self.privacyButton = tk.CTkButton(self.centerFrame, text="Privacy", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("PrivacyPage"))
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.centerFrame.grid(row=2, column=0)
        self.startButton.pack(padx=15, pady=(15, 5))
        self.privacyButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

class PrivacyPage(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.mainTitle = tk.CTkLabel(self, text="One Click Story", font=tk.CTkFont("Segoe", 60, "normal"))

        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)
        self.privacyPolicy = tk.CTkTextbox(self.centerFrame, font=tk.CTkFont("Segoe", 15, "normal"), width=500)
        self.privacyPolicy.insert("0.0", privacyText*50)
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("HomePage"))
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        self.mainTitle.place(relx=0.5, rely=0.075, anchor=CENTER)

        self.centerFrame.grid(row=2, column=0)
        self.privacyPolicy.pack(padx=15, pady=(15, 5))
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

class ImageInputPage(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.uploaded = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #self.mainTitle = tk.CTkLabel(self, text="Image Input", font=tk.CTkFont("Segoe", 120, "normal"))

        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.uploadedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        self.imageButton = tk.CTkButton(self.centerFrame, text="Upload Image", font=tk.CTkFont("Segoe", 20, "normal"), command=self.imageUpload)
        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ObjectRecPage"), state="disabled") # Default state is disable to ensure that user does not continue without an uploaded image
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)
        
        #self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.centerFrame.grid(row=2, column=0)
        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.uploadedImage.pack(expand=True, fill="both")

        self.imageButton.pack(padx=15, pady=(15, 5))
        self.continueButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def imageUpload(self):
        f_type_list = [("Image files", "*,jpg;*.png;*.jpeg")] # Creates the little "allowed file extensions" list for windows explorer
        path = tk.filedialog.askopenfilename(filetypes=f_type_list)

        if len(path):
            pic = Image.open(path)
            pic = pic.resize((400, 300)) # Format uploaded images to the optimal size for object recognition
            self.controller.uploadedImage = pic
            self.uploadedImage.configure(image = tk.CTkImage(pic, size=(400,400)))
            self.continueButton.configure(state="normal") # Activate the continue button once an image is uploaded
        else:
            return(False)
        
class CameraInputPage(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.uploaded = False
        self.cameraActive = False
        self.currentImage = None
        self.nakedImage = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #self.mainTitle = tk.CTkLabel(self, text="Image Input", font=tk.CTkFont("Segoe", 120, "normal"))

        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.uploadedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        self.imageButton = tk.CTkButton(self.centerFrame, text="Capture Picture", font=tk.CTkFont("Segoe", 20, "normal"), command=self.cameraUpload)
        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ObjectRecPage"), state="disabled") # Default state is disable to ensure that user does not continue without an uploaded image
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)
        
        #self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.centerFrame.grid(row=2, column=0)
        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.uploadedImage.pack(expand=True, fill="both")

        self.imageButton.pack(padx=15, pady=(15, 5))
        self.continueButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def cameraUpload(self):
        if self.cameraActive:
            self.cameraActive = False
            self.imageButton.configure(text="Capture Picture")
            self.continueButton.configure(state="normal")
            self.after_cancel(self.update_job)
            self.controller.uploadedImage = self.nakedImage
            self.cap.release()
            cv2.destroyAllWindows()
        else:
            self.cameraActive = True
            self.imageButton.configure(text="Stop Camera")
            self.continueButton.configure(state="disabled")
            self.cap = cv2.VideoCapture(0)
            self.displayWebcam()

    def displayWebcam(self):
        if self.cameraActive:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (400, 400))
                img = Image.fromarray(frame)
                self.nakedImage = img
                self.currentImage = tk.CTkImage(img, size=(400,400))
                self.uploadedImage.configure(image=self.currentImage)
            self.update_job = self.after(10, self.displayWebcam)
                    
class InputSelect(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.mainTitle = tk.CTkLabel(self, text="Input Selection", font=tk.CTkFont("Segoe", 60, "normal"))
        
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)
        self.imageInput = tk.CTkButton(self.centerFrame, text="Add From PC", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ImageInputPage"))
        self.cameraInput = tk.CTkButton(self.centerFrame, text="Add From Camera", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("CameraInputPage"))
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("HomePage"))
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.centerFrame.grid(row=2, column=0)
        self.imageInput.pack(padx=15, pady=(15, 5))
        self.cameraInput.pack(padx=15, pady=5)
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

class ObjectRecPage(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # self.mainTitle = tk.CTkLabel(self, text="Object Recognition", font=tk.CTkFont("Segoe", 60, "normal"))
        
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.displayedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        self.detectButton = tk.CTkButton(self.centerFrame, text="Detect Objects", font=tk.CTkFont("Segoe", 20, "normal"), command=self.startObjectRecThread)
        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("StoryGenerator"), state="disabled")
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("InputSelect"))
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        self.progressBar = tk.CTkProgressBar(self.centerFrame, orientation="horizontal", mode="determinate", determinate_speed=0.15)
        self.progressBar.set(0)
        # self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.centerFrame.grid(row=2, column=0)
        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.displayedImage.pack(expand=True, fill="both")

        self.progressBar.pack(padx=15, pady=(15,5))
        self.detectButton.pack(padx=15, pady=5)
        self.continueButton.pack(padx=15, pady=5)
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def update_image(self, image):
        self.displayedImage.configure(image=tk.CTkImage(image, size=(400,400)))
        self.displayedImage.image = image

    def startObjectRecThread(self):
        thr = threading.Thread(target=self.objectRec)
        thr.start()

    def objectRec(self):
        # Convert PIL image to CV2 for input :(
        self.progressBar.configure(progress_color = "#0C955A")
        self.progressBar.start()

        modelresults = object_rec.captureFrame(2, self.controller.uploadedImage)
        detected_obj = object_rec.returnFoundObjects(modelresults)
        self.controller.objectsDict = detected_obj
        print(self.controller.objectsDict)
        self.progressBar.step()

        modified_img = object_rec.modifyImage(modelresults, self.controller.uploadedImage)

        formatted_img = Image.fromarray(modified_img)
        self.controller.detectedImage = formatted_img
        self.displayedImage.configure(image=tk.CTkImage(formatted_img, size=(400,400)))

        self.progressBar.stop()
        self.progressBar.set(1)
        self.continueButton.configure(state="normal")

class StoryGenerator(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.mainTitle = tk.CTkLabel(self, text="Story Generator", font=tk.CTkFont("Segoe", 60, "normal"))

        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)
        
        self.objectList = tk.CTkLabel(self.centerFrame, text="Objects List:", font=tk.CTkFont("Segoe", 20, "normal"))
        
        self.generatedStory = tk.CTkTextbox(self.centerFrame, font=tk.CTkFont("Segoe", 15, "normal"), width=500)

        self.progressBar = tk.CTkProgressBar(self.centerFrame, orientation="horizontal", mode="determinate", determinate_speed=0.15)
        self.progressBar.set(0)

        self.generateButton = tk.CTkButton(self.centerFrame, text="Generate Story", font=tk.CTkFont("Segoe", 20, "normal"), command=self.startStoryGenThread)
        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ImageGenerator"))
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ObjectRecPage"))
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        self.mainTitle.place(relx=0.5, rely=0.075, anchor=CENTER)

        self.centerFrame.grid(row=2, column=0)
        self.objectList.pack(padx=15, pady=(15,5))
        self.generatedStory.pack(padx=15, pady=5)
        self.progressBar.pack(padx=15, pady=5)
        self.generateButton.pack(padx=15, pady=5)
        self.continueButton.pack(padx=15, pady=5)
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def updateObjList(self, text):
        finalString = sdf.std_return_dict_as_single_string(text)
        self.objectList.configure(text=finalString.title())
        self.objectList._text = text

    def startStoryGenThread(self):
        thr = threading.Thread(target=self.generateStory)
        thr.start()

    def generateStory(self):
        self.generatedStory.delete(1.0, tk.END)
        self.progressBar.configure(progress_color = "#0C955A")
        self.progressBar.start()
        storyReturn = chat_model.gen_story(self.controller.objectsDict)
        self.controller.genStory = storyReturn
        print(storyReturn)
        self.progressBar.stop()
        self.progressBar.set(1)
        self.generatedStory.insert(0.0, storyReturn)

class ImageGenerator(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.uploaded = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #self.mainTitle = tk.CTkLabel(self, text="Image Input", font=tk.CTkFont("Segoe", 120, "normal"))

        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.uploadedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        self.imageButton = tk.CTkButton(self.centerFrame, text="Generate Image", font=tk.CTkFont("Segoe", 20, "normal"), command=self.startImageGenThread)
        self.continueButton = tk.CTkButton(self.centerFrame, text="Finish", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("FinalPage"), state="disabled") # Default state is disable to ensure that user does not continue without a generated image
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)
        
        #self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.centerFrame.grid(row=2, column=0)

        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.uploadedImage.pack(expand=True, fill="both")

        self.progressBar = tk.CTkProgressBar(self.centerFrame, orientation="horizontal", mode="determinate", determinate_speed=0.15)
        self.progressBar.set(0)

        self.progressBar.pack(padx=15, pady=(15, 5))
        self.imageButton.pack(padx=15, pady=5)
        self.continueButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def createStoryFrame(self):
        self.storyFrame = tk.CTkFrame(self, border_width=1)
        self.storyFrame.grid_columnconfigure(0, weight=1)
        self.generatedStory = tk.CTkTextbox(self.storyFrame, font=tk.CTkFont("Segoe", 20, "normal"), width=500)
        self.storyFrame.grid(row=2, column=1)
        self.generatedStory.pack(padx=15, pady=5)
        
        self.generatedStory.insert(0.0, self.controller.genStory)

    def startImageGenThread(self):
        thr = threading.Thread(target=self.generateImage)
        thr.start()

    def generateImage(self):
        self.progressBar.configure(progress_color = "#0C955A")
        self.progressBar.start()
        genImage = image_model.generate_image_from_text(self.controller.genStory)
        self.controller.generatedImage = genImage
        self.uploadedImage.configure(image=tk.CTkImage(genImage, size=(400,400)))
        self.progressBar.stop()
        self.progressBar.set(1)
        self.continueButton.configure(state="normal")

class FinalPage(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.mainTitle = tk.CTkLabel(self, text="Final Output", font=tk.CTkFont("Segoe", 120, "normal"))

        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        self.uploadedImageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.uploadedImage = tk.CTkLabel(self.uploadedImageHolder, width=400, height=400, text="")
        
        self.mainTitle.place(relx=0.7, rely=0.1, anchor=CENTER)

        self.centerFrame.grid(row=2, column=0)

        self.uploadedImageHolder.pack(padx=15, pady=15)
        self.uploadedImage.pack(expand=True, fill="both")

    def createSecondColumn(self):
        self.storyFrame = tk.CTkFrame(self, border_width=1)
        self.storyFrame.grid_columnconfigure(0, weight=1)
        # self.generatedStory = tk.CTkTextbox(self.storyFrame, font=tk.CTkFont("Segoe", 20, "normal"), width=500)
        self.storyFrame.grid(row=2, column=1)
        # self.generatedStory.pack(padx=15, pady=5)
        
        # self.generatedStory.insert(0.0, self.controller.genStory)

        # Create holder frame and image for generated image

        self.generatedImageHolder = tk.CTkFrame(self.storyFrame, width=400, height=400)
        self.generatedImageHolder.pack(padx=15, pady=15)
        self.generatedImage = tk.CTkLabel(self.generatedImageHolder, width=400, height=400, text="")
        self.generatedImage.pack(expand=True, fill="both")

        self.bottomFrame = tk.CTkFrame(self, width=600, height=50)
        self.bottomFrame.grid(row=3, column=0, columnspan=2)
        self.generatedStory = tk.CTkTextbox(self.bottomFrame, font=tk.CTkFont("Segoe", 15, "normal"), width=500, height=100)
        self.generatedStory.pack(padx=15, pady=5)
        self.generatedStory.insert(0.0, self.controller.genStory)

        self.exitButton = tk.CTkButton(self.bottomFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)
        self.exitButton.pack(padx=15, pady=(5, 15))

        self.generatedImage.configure(image=tk.CTkImage(self.controller.generatedImage, size=(400,400)))
        self.uploadedImage.configure(image=tk.CTkImage(self.controller.detectedImage, size=(400,400)))

app().mainloop()