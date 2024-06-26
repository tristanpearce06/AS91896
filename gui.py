import tkinter
from tkinter import CENTER
import tkinter.messagebox
import customtkinter as tk

tk.set_appearance_mode("system")
tk.set_default_color_theme("blue")

class app(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Photo Story")
        self.geometry("600x360")

        self.container = tk.CTkFrame(self)
        self.container.pack(anchor=CENTER, expand=True)

        self.frames = {}

        for Fr in (HomePage, PrivacyPage):
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

        self.mainTitle = tk.CTkLabel(self, text="One Click Story", font=tk.CTkFont("Segoe", 80, "normal"))
        self.startButton = tk.CTkButton(self, text="Start", font=tk.CTkFont("Segoe", 35, "normal"))
        self.privacyButton = tk.CTkButton(self, text="Privacy", font=tk.CTkFont("Segoe", 35, "normal"), command=lambda:controller.show_frame("PrivacyPage"))
        self.exitButton = tk.CTkButton(self, text="Exit", font=tk.CTkFont("Segoe", 35, "normal"), command=self.quit)

        self.mainTitle.grid(row=0, column=0,)
        self.startButton.grid(row=1, column=0, pady=5)
        self.privacyButton.grid(row=2, column=0, pady=5)
        self.exitButton.grid(row=3, column=0, pady=5)


class PrivacyPage(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        self.mainTitle = tk.CTkLabel(self, text="One Click Story", font=tk.CTkFont("Segoe", 80, "normal"))
        self.backButton = tk.CTkButton(self, text="Back", font=tk.CTkFont("Segoe", 35, "normal"), command=lambda:controller.show_frame("HomePage"))
        self.exitButton = tk.CTkButton(self, text="Exit", font=tk.CTkFont("Segoe", 35, "normal"), command=self.quit)

        self.mainTitle.grid(row=0, column=0)
        self.backButton.grid(row=1, column=0, pady=5)
        self.exitButton.grid(row=2, column=0, pady=5)


app().mainloop()