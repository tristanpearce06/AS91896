# First time running?
# Through either the command prompt or the VS code terminal, run the command: pip install -r requirements.txt
# Then you're good to go!

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

# Set appearance and light/dark mode based on system settings
tk.set_appearance_mode("system")
tk.set_default_color_theme("blue")

# Placeholder privacy text
privacyText = "Placeholder privacy text lol real is this real chat what lol seriously yo thats actually crazy what???"

# Main application class
class app(tk.CTk):
    """
    The main application class that inherits from tk.CTk.
    This class is responsible for initializing the application window,
    creating and managing different frames (pages), and handling the
    navigation between these frames.
    """
    def __init__(self):
        super().__init__()

        # Set the title of the application window
        self.title("Photo Story")
        # Set the initial size of the application window
        self.geometry("550x650")

        # Create a container frame to hold all the pages
        self.container = tk.CTkFrame(self)
        self.container.pack(anchor=CENTER, expand=True)

        # Initialize attributes to hold images and other data
        self.uploadedImage = None
        self.generatedImage = None
        self.detectedImage = None
        self.objectsDict = None
        self.genStory = None

        # Dictionary to hold instances of all the frames
        self.frames = {}

        # Create instances of all the pages and store them in the frames dictionary
        for Fr in (HomePage, PrivacyPage, ImageInputPage, CameraInputPage, InputSelect, ObjectRecPage, StoryGenerator, ImageGenerator, FinalPage):
            PageName = Fr.__name__
            # Create an instance of the frame
            frame = Fr(parent=self.container, controller=self)
            # Store the frame instance in the dictionary with the frame name as the key
            self.frames[PageName] = frame
            # Place all frames in the same location; the one on the top will be visible
            frame.grid(row=0, column=0, sticky="nsew")

        # Display the home page initially
        self.show_frame("HomePage")

    def show_frame(self, pName):
            # Get the frame instance from the dictionary
            frame = self.frames[pName]
            
            # Update specific frames with the necessary data before displaying them
            if pName == "ObjectRecPage" and self.uploadedImage:
                # Update the ObjectRecPage with the uploaded image
                frame.update_image(self.uploadedImage)
            elif pName == "StoryGenerator" and self.objectsDict:
                # Update the StoryGenerator with the objects dictionary
                frame.updateObjList(self.objectsDict)
            elif pName == "ImageGenerator":
                # Set the window size to 1050x650 for the ImageGenerator page
                self.geometry("1050x650")
                # Create the story frame for the ImageGenerator page
                frame.createStoryFrame()
            elif pName == "FinalPage":
                # Create the second column for the FinalPage
                frame.createSecondColumn()

            # Raise the selected frame to the top of the stack (displaying the frame)
            frame.tkraise()

class HomePage(tk.CTkFrame):
    """
    HomePage class that inherits from tk.CTkFrame.
    This class represents the home page of the application.
    It contains buttons to navigate to other pages and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)

        # Store the controller for navigation
        self.controller = controller

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create and place the main title label
        self.mainTitle = tk.CTkLabel(self, text="One Click Story", font=tk.CTkFont("Segoe", 60, "normal"))
        
        # Create a frame to hold the buttons
        self.centerFrame = tk.CTkFrame(self, border_width=1, height=700)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        # Create a 'Start' button to navigate to the InputSelect page
        self.startButton = tk.CTkButton(self.centerFrame, text="Start", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("InputSelect"))
        
        # Create a 'Privacy' button to navigate to the PrivacyPage
        self.privacyButton = tk.CTkButton(self.centerFrame, text="Privacy", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("PrivacyPage"))
        
        # Create an 'Exit' button to quit the application
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        # Place the main title at the top center of the window
        self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)

        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)
        self.startButton.pack(padx=15, pady=(15, 5))
        self.privacyButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

class PrivacyPage(tk.CTkFrame):
    """
    PrivacyPage class that inherits from tk.CTkFrame.
    This class represents the privacy policy page of the application.
    It contains a text widget to display the privacy policy, a back button to return to the home page,
    and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)
        self.controller = controller

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create and place the main title label
        self.mainTitle = tk.CTkLabel(self, text="One Click Story", font=tk.CTkFont("Segoe", 60, "normal"))

        # Create a frame to hold the privacy policy text and buttons
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        # Create a text widget to display the privacy policy
        self.privacyPolicy = tk.CTkTextbox(self.centerFrame, font=tk.CTkFont("Segoe", 15, "normal"), width=500)
        # Insert the privacy policy text into the text widget
        self.privacyPolicy.insert("0.0", privacyText * 50)

        # Create a 'Back' button to return to the HomePage
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda: controller.show_frame("HomePage"))

        # Create an 'Exit' button to quit the application
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        # Place the main title at the top center of the window
        self.mainTitle.place(relx=0.5, rely=0.075, anchor=CENTER)

        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)
        self.privacyPolicy.pack(padx=15, pady=(15, 5))
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

class ImageInputPage(tk.CTkFrame):
    """
    ImageInputPage class that inherits from tk.CTkFrame.
    This class represents the page for uploading an image from the PC.
    It contains a frame to hold the uploaded image, a button to upload an image,
    a 'Continue' button to proceed to the ObjectRecPage, and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)
        self.controller = controller

        # Flag to check if an image has been uploaded
        self.uploaded = False

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create a frame to hold the image and buttons
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        # Create a frame to hold the uploaded image
        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.uploadedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        # Create a button to upload an image
        self.imageButton = tk.CTkButton(self.centerFrame, text="Upload Image", font=tk.CTkFont("Segoe", 20, "normal"), command=self.imageUpload)
        
        # Create a 'Continue' button to proceed to the ObjectRecPage, initially disabled
        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ObjectRecPage"), state="disabled") # Default state is disable to ensure that user does not continue without an uploaded image
        
        # Create an 'Exit' button to quit the application
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)
        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.uploadedImage.pack(expand=True, fill="both")

        # Pack the buttons in the center frame
        self.imageButton.pack(padx=15, pady=(15, 5))
        self.continueButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def imageUpload(self):
        # Function to handle image upload
        f_type_list = [("Image files", "*,jpg;*.png;*.jpeg")] # Creates the little "allowed file extensions" list for windows explorer
        path = tk.filedialog.askopenfilename(filetypes=f_type_list)

        if len(path):
            # Open and resize the image
            pic = Image.open(path)
            pic = pic.resize((400, 300)) # Format uploaded images to the optimal size for object recognition
            self.controller.uploadedImage = pic
            # Update the label to display the uploaded image
            self.uploadedImage.configure(image = tk.CTkImage(pic, size=(400,400)))
            # Activate the continue button once an image is uploaded
            self.continueButton.configure(state="normal")
        else:
            return(False)
        
class CameraInputPage(tk.CTkFrame):
    """
    CameraInputPage class that inherits from tk.CTkFrame.
    This class represents the page for capturing an image using the camera.
    It contains a frame to hold the camera feed, a button to start the camera,
    a 'Capture' button to capture an image from the camera feed, and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)
        self.controller = controller

        # Flags and variables to manage camera state and images
        self.uploaded = False
        self.cameraActive = False
        self.currentImage = None
        self.nakedImage = None

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create a frame to hold the camera feed and buttons
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        # Create a frame to hold the captured image
        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.uploadedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        # Create a button to start/stop the camera and capture an image
        self.imageButton = tk.CTkButton(self.centerFrame, text="Capture Picture", font=tk.CTkFont("Segoe", 20, "normal"), command=self.cameraUpload)
        
        # Create a 'Continue' button to proceed to the ObjectRecPage, initially disabled
        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ObjectRecPage"), state="disabled") # Default state is disable to ensure that user does not continue without an uploaded image
        
        # Create an 'Exit' button to quit the application
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)
        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.uploadedImage.pack(expand=True, fill="both")

        # Pack the buttons in the center frame
        self.imageButton.pack(padx=15, pady=(15, 5))
        self.continueButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def cameraUpload(self):
        # Function to handle camera start/stop and image capture
        if self.cameraActive:
            # Stop the camera and capture the image
            self.cameraActive = False
            self.imageButton.configure(text="Capture Picture")
            self.continueButton.configure(state="normal")
            self.after_cancel(self.update_job)
            self.controller.uploadedImage = self.nakedImage
            self.cap.release()
            cv2.destroyAllWindows()
        else:
            # Start the camera
            self.cameraActive = True
            self.imageButton.configure(text="Stop Camera")
            self.continueButton.configure(state="disabled")
            self.cap = cv2.VideoCapture(0)
            self.displayWebcam()

    def displayWebcam(self):
        # Function to display the camera feed
        if self.cameraActive:
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to RGB and resize it
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (400, 400))
                img = Image.fromarray(frame)
                self.nakedImage = img
                self.currentImage = tk.CTkImage(img, size=(400,400))
                self.uploadedImage.configure(image=self.currentImage)
            # Schedule the next frame update
            self.update_job = self.after(10, self.displayWebcam)
                    
class InputSelect(tk.CTkFrame):
    """
    InputSelect class that inherits from tk.CTkFrame.
    This class represents the page where the user can select the input method for the image.
    It contains buttons to choose between uploading an image from the PC or capturing an image using the camera,
    and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)
        self.controller = controller

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create and place the main title label
        self.mainTitle = tk.CTkLabel(self, text="Input Selection", font=tk.CTkFont("Segoe", 60, "normal"))
        
        # Create a frame to hold the input method buttons and other controls
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        # Create a button to navigate to the ImageInputPage for uploading an image from the PC
        self.imageInput = tk.CTkButton(self.centerFrame, text="Add From PC", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ImageInputPage"))
        
        # Create a button to navigate to the CameraInputPage for capturing an image using the camera
        self.cameraInput = tk.CTkButton(self.centerFrame, text="Add From Camera", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("CameraInputPage"))
        
        # Create a 'Back' button to return to the HomePage
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("HomePage"))
        
        # Create an 'Exit' button to quit the application
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        # Place the main title at the top center of the window
        self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)
        self.imageInput.pack(padx=15, pady=(15, 5))
        self.cameraInput.pack(padx=15, pady=5)
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

class ObjectRecPage(tk.CTkFrame):
    """
    ObjectRecPage class that inherits from tk.CTkFrame.
    This class represents the page for object recognition.
    It contains a frame to display the image with recognized objects,
    a button to start the object recognition process, and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)
        self.controller = controller

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create a frame to hold the image and buttons
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        # Create a frame to hold the displayed image
        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.displayedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        # Create a button to start the object recognition process
        self.detectButton = tk.CTkButton(self.centerFrame, text="Detect Objects", font=tk.CTkFont("Segoe", 20, "normal"), command=self.startObjectRecThread)
        
        # Create a 'Continue' button to proceed to the StoryGenerator page, initially disabled
        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("StoryGenerator"), state="disabled")
        
        # Create a 'Back' button to return to the InputSelect page
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("InputSelect"))
        
        # Create an 'Exit' button to quit the application
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        # Create a progress bar to show the progress of the object recognition process
        self.progressBar = tk.CTkProgressBar(self.centerFrame, orientation="horizontal", mode="determinate", determinate_speed=0.15)
        self.progressBar.set(0)
        
        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)
        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.displayedImage.pack(expand=True, fill="both")

        # Pack the progress bar and buttons in the center frame
        self.progressBar.pack(padx=15, pady=(15,5))
        self.detectButton.pack(padx=15, pady=5)
        self.continueButton.pack(padx=15, pady=5)
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def update_image(self, image):
        # Update the displayed image with the given image
        self.displayedImage.configure(image=tk.CTkImage(image, size=(400,400)))
        self.displayedImage.image = image

    def startObjectRecThread(self):
        # Start a new thread to run the object recognition process
        thr = threading.Thread(target=self.objectRec)
        thr.start()

    def objectRec(self):
        # Configure and start the progress bar
        self.progressBar.configure(progress_color = "#0C955A")
        self.progressBar.start()

        # Perform object recognition on the uploaded image
        modelresults = object_rec.captureFrame(2, self.controller.uploadedImage)
        detected_obj = object_rec.returnFoundObjects(modelresults)
        self.controller.objectsDict = detected_obj
        print(self.controller.objectsDict)
        self.progressBar.step()

        # Modify the image to highlight the recognized objects
        modified_img = object_rec.modifyImage(modelresults, self.controller.uploadedImage)

        # Convert the modified image to a format suitable for (openCV uses BGR and tkinter uses RGB RAAGHHHHH)
        formatted_img = Image.fromarray(modified_img)
        self.controller.detectedImage = formatted_img
        self.displayedImage.configure(image=tk.CTkImage(formatted_img, size=(400,400)))

        # Stop the progress bar and enable the continue button
        self.progressBar.stop()
        self.progressBar.set(1)
        self.continueButton.configure(state="normal")

class StoryGenerator(tk.CTkFrame):
    """
    StoryGenerator class that inherits from tk.CTkFrame.
    This class represents the page for generating a story based on recognized objects.
    It contains a frame to display the generated story, a button to generate the story,
    and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)
        self.controller = controller

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create and place the main title label
        self.mainTitle = tk.CTkLabel(self, text="Story Generator", font=tk.CTkFont("Segoe", 60, "normal"))

        # Create a frame to hold the story and buttons
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)
        
        # Create a label to display the list of recognized objects
        self.objectList = tk.CTkLabel(self.centerFrame, text="Objects List:", font=tk.CTkFont("Segoe", 20, "normal"))
        
        # Create a text box to display the generated story
        self.generatedStory = tk.CTkTextbox(self.centerFrame, font=tk.CTkFont("Segoe", 15, "normal"), width=500)

        # Create a progress bar to show the progress of the story generation process
        self.progressBar = tk.CTkProgressBar(self.centerFrame, orientation="horizontal", mode="determinate", determinate_speed=0.15)
        self.progressBar.set(0)

        # Create a button to start the story generation process
        self.generateButton = tk.CTkButton(self.centerFrame, text="Generate Story", font=tk.CTkFont("Segoe", 20, "normal"), command=self.startStoryGenThread)
        
        # Create a 'Continue' button to proceed to the ImageGenerator page
        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ImageGenerator"))
        
        # Create a 'Back' button to return to the ObjectRecPage
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ObjectRecPage"))
        
        # Create an 'Exit' button to quit the application
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        # Place the main title at the top center of the window
        self.mainTitle.place(relx=0.5, rely=0.075, anchor=CENTER)

        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)
        self.objectList.pack(padx=15, pady=(15,5))
        self.generatedStory.pack(padx=15, pady=5)
        self.progressBar.pack(padx=15, pady=5)
        self.generateButton.pack(padx=15, pady=5)
        self.continueButton.pack(padx=15, pady=5)
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def updateObjList(self, text):
        # Update the object list label with the given text
        finalString = sdf.std_return_dict_as_single_string(text)
        self.objectList.configure(text=finalString.title())
        self.objectList._text = text

    def startStoryGenThread(self):
        # Start a new thread to run the story generation process
        thr = threading.Thread(target=self.generateStory)
        thr.start()

    def generateStory(self):
        # Clear the text box and start the progress bar
        self.generatedStory.delete(1.0, tk.END)
        self.progressBar.configure(progress_color = "#0C955A")
        self.progressBar.start()

        # Generate the story based on the recognized objects
        storyReturn = chat_model.gen_story(self.controller.objectsDict)
        self.controller.genStory = storyReturn
        print(storyReturn)

        # Stop the progress bar and display the generated story
        self.progressBar.stop()
        self.progressBar.set(1)
        self.generatedStory.insert(0.0, storyReturn)

class ImageGenerator(tk.CTkFrame):
    """
    ImageGenerator class that inherits from tk.CTkFrame.
    This class represents the page for generating images based on the generated story.
    It contains a frame to display the generated image, a button to start the image generation process,
    and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)
        self.controller = controller

        # Flag to check if an image has been uploaded
        self.uploaded = False

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create a frame to hold the image and buttons
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        # Create a frame to hold the generated image
        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.uploadedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        # Create a button to start the image generation process
        self.imageButton = tk.CTkButton(self.centerFrame, text="Generate Image", font=tk.CTkFont("Segoe", 20, "normal"), command=self.startImageGenThread)
        
        # Create a 'Finish' button to proceed to the FinalPage, initially disabled
        self.continueButton = tk.CTkButton(self.centerFrame, text="Finish", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("FinalPage"), state="disabled") # Default state is disable to ensure that user does not continue without a generated image
        
        # Create an 'Exit' button to quit the application
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)
    
        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)

        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.uploadedImage.pack(expand=True, fill="both")

        # Create a progress bar to show the progress of the image generation process
        self.progressBar = tk.CTkProgressBar(self.centerFrame, orientation="horizontal", mode="determinate", determinate_speed=0.15)
        self.progressBar.set(0)

        # Pack the progress bar and buttons in the center frame
        self.progressBar.pack(padx=15, pady=(15, 5))
        self.imageButton.pack(padx=15, pady=5)
        self.continueButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def createStoryFrame(self):
        # Create a frame to display the generated story
        self.storyFrame = tk.CTkFrame(self, border_width=1)
        self.storyFrame.grid_columnconfigure(0, weight=1)
        self.generatedStory = tk.CTkTextbox(self.storyFrame, font=tk.CTkFont("Segoe", 20, "normal"), width=500)
        self.storyFrame.grid(row=2, column=1)
        self.generatedStory.pack(padx=15, pady=5)
        
        # Insert the generated story into the text box
        self.generatedStory.insert(0.0, self.controller.genStory)

    def startImageGenThread(self):
        # Start a new thread to run the image generation process
        thr = threading.Thread(target=self.generateImage)
        thr.start()

    def generateImage(self):
        # Configure and start the progress bar
        self.progressBar.configure(progress_color = "#0C955A")
        self.progressBar.start()

        # Generate the image based on the generated story
        genImage = image_model.generate_image_from_text(self.controller.genStory)
        self.controller.generatedImage = genImage

        # Update the label to display the generated image
        self.uploadedImage.configure(image=tk.CTkImage(genImage, size=(400,400)))

        # Stop the progress bar and enable the continue button
        self.progressBar.stop()
        self.progressBar.set(1)
        self.continueButton.configure(state="normal")

class FinalPage(tk.CTkFrame):
    """
    FinalPage class that inherits from tk.CTkFrame.
    This class represents the final page of the application.
    It contains a frame to display the final generated image and story,
    and an exit button to quit the application.
    """
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.CTkFrame)
        super().__init__(parent)
        self.controller = controller

        # Configure the grid layout for the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create a frame to hold the uploaded image
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        # Create a frame to hold the uploaded image
        self.uploadedImageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.uploadedImage = tk.CTkLabel(self.uploadedImageHolder, width=400, height=400, text="")

        # Configure the layout of the center frame
        self.centerFrame.grid(row=2, column=0)

        self.uploadedImageHolder.pack(padx=15, pady=15)
        self.uploadedImage.pack(expand=True, fill="both")

    def createSecondColumn(self):
        # Create a frame to hold the generated image and story
        self.storyFrame = tk.CTkFrame(self, border_width=1)
        self.storyFrame.grid_columnconfigure(0, weight=1)
        
        # Configure the layout of the story frame
        self.storyFrame.grid(row=2, column=1)

        # Create a frame to hold the generated image
        self.generatedImageHolder = tk.CTkFrame(self.storyFrame, width=400, height=400)
        self.generatedImageHolder.pack(padx=15, pady=15)
        self.generatedImage = tk.CTkLabel(self.generatedImageHolder, width=400, height=400, text="")
        self.generatedImage.pack(expand=True, fill="both")

        # Create a frame to hold the generated story and exit button
        self.bottomFrame = tk.CTkFrame(self, width=600, height=50)
        self.bottomFrame.grid(row=3, column=0, columnspan=2)
        self.generatedStory = tk.CTkTextbox(self.bottomFrame, font=tk.CTkFont("Segoe", 15, "normal"), width=500, height=100)
        self.generatedStory.pack(padx=15, pady=5)
        
        # Insert the generated story into the text box
        self.generatedStory.insert(0.0, self.controller.genStory)

        # Create an exit button to quit the application
        self.exitButton = tk.CTkButton(self.bottomFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)
        self.exitButton.pack(padx=15, pady=(5, 15))

        # Update the labels to display the uploaded and generated images
        self.generatedImage.configure(image=tk.CTkImage(self.controller.generatedImage, size=(400,400)))
        self.uploadedImage.configure(image=tk.CTkImage(self.controller.detectedImage, size=(400,400)))

app().mainloop()