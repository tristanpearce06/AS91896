import tkinter
from tkinter import CENTER
import tkinter.messagebox
import customtkinter as tk
from PIL import Image

import object_rec

tk.set_appearance_mode("system")
tk.set_default_color_theme("blue")

privacyText = "Placeholder privacy text lol real is this real chat what lol seriously yo thats actually crazy what???"

class app(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Photo Story")
        self.geometry("800x550")

        self.container = tk.CTkFrame(self)
        self.container.pack(anchor=CENTER, expand=True)

        self.uploadedImage = None

        self.frames = {}

        for Fr in (HomePage, PrivacyPage, ImageInputPage, InputSelect, ObjectRecPage):
            PageName = Fr.__name__
            frame = Fr(parent=self.container, controller=self)
            self.frames[PageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, pName):
        frame = self.frames[pName]
        if pName == "ObjectRecPage" and self.uploadedImage:
            frame.update_image(self.uploadedImage)
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
        self.cameraInput = tk.CTkButton(self.centerFrame, text="Add From Camera", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)
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

        self.mainTitle = tk.CTkLabel(self, text="Object Recognition", font=tk.CTkFont("Segoe", 60, "normal"))
        
        self.centerFrame = tk.CTkFrame(self, border_width=1)
        self.centerFrame.grid_columnconfigure(0, weight=1)

        self.imageHolder = tk.CTkFrame(self.centerFrame, width=400, height=400)
        self.displayedImage = tk.CTkLabel(self.imageHolder, width=400, height=400, text="")

        self.continueButton = tk.CTkButton(self.centerFrame, text="Continue", font=tk.CTkFont("Segoe", 20, "normal"), command=self.objectRec)
        self.backButton = tk.CTkButton(self.centerFrame, text="Back", font=tk.CTkFont("Segoe", 20, "normal"), command=lambda:controller.show_frame("ImageInputPage"))
        self.exitButton = tk.CTkButton(self.centerFrame, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)

        self.mainTitle.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.centerFrame.grid(row=2, column=0)
        self.imageHolder.pack(padx=15, pady=(15, 5))
        self.displayedImage.pack(expand=True, fill="both")

        self.continueButton.pack(padx=15, pady=(15, 5))
        self.backButton.pack(padx=15, pady=5)
        self.exitButton.pack(padx=15, pady=(5, 15))

    def update_image(self, image):
        self.displayedImage.configure(image=tk.CTkImage(image, size=(400,400)))
        self.displayedImage.image = image

    def objectRec(self):
        # Convert PIL image to CV2 for input :(
        modelresults = object_rec.captureFrame(2, self.controller.uploadedImage)

        detected_obj = object_rec.returnFoundObjects(modelresults)
        print(detected_obj)

        modified_img = object_rec.modifyImage(modelresults, self.controller.uploadedImage)
        print(modified_img)
        formatted_img = Image.fromarray(modified_img)
        self.displayedImage.configure(image=tk.CTkImage(formatted_img, size=(400,400)))

app().mainloop()