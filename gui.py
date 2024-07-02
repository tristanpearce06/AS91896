import tkinter
from tkinter import CENTER
import tkinter.messagebox
import customtkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

tk.set_appearance_mode("system")
tk.set_default_color_theme("blue")

privacyText = "Placeholder privacy text lol real is this real chat what lol seriously yo thats actually crazy what???"

# Create general functions before initializing the UI




class app(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Photo Story")
        self.geometry("800x500")

        self.container = tk.CTkFrame(self)
        self.container.pack(anchor=CENTER, expand=True)

        self.frames = {}

        for Fr in (HomePage, PrivacyPage, ImageInputPage, InputSelect):
            PageName = Fr.__name__
            frame = Fr(parent=self.container, controller=self)
            self.frames[PageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, pName):
        frame = self.frames[pName]
        frame.tkraise()

class HomePage(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.mainTitle = tk.CTkLabel(self, text="One Click Story", font=tk.CTkFont("Segoe", 60, "normal"))
        
        self.centerFrame = tk.CTkFrame(self, border_width=1)
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

        self.grid_columnconfigure(0, weight=1)

        self.mainTitle = tk.CTkLabel(self, text="Image Input", font=tk.CTkFont("Segoe", 60, "normal"))
        self.imageHolder = tk.CTkFrame(self, width=400, height=300)
        self.uploadedImage = tk.CTkLabel(self.imageHolder, width=400, height=300, text="")
        self.imageButton = tk.CTkButton(self, text="Upload Image", font=tk.CTkFont("Segoe", 20, "normal"), command=self.imageUpload)
        self.exitButton = tk.CTkButton(self, text="Exit", font=tk.CTkFont("Segoe", 20, "normal"), command=self.quit)
        
        self.mainTitle.grid(row=1, column=0)
        self.imageHolder.grid(row=2, column=0, pady=5)
        self.uploadedImage.pack(expand=True, fill="both")
        self.imageButton.grid(row=3, column=0, pady=5)
        self.exitButton.grid(row=4, column=0, pady=5)

    def imageUpload(self):
        f_type_list = [("Image files", "*,jpg;*.png;*.jpeg")] # Creates the little "allowed file extensions" list for windows explorer
        path = tk.filedialog.askopenfilename(filetypes=f_type_list)

        if len(path):
            pic = Image.open(path)
            pic = pic.resize((400, 300)) # Format uploaded images to the optimal size for object recognition
            self.uploadedImage.configure(image = tk.CTkImage(pic, size=(400,300)))
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

app().mainloop()