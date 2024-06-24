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

        self.mainmenu = tk.CTkFrame(self)
        self.mainmenu.grid_columnconfigure(0, weight=1)

        self.mainTitle = tk.CTkLabel(self.mainmenu, text="One Click Story", font=tk.CTkFont("Segoe", 80, "normal"))
        self.startButton = tk.CTkButton(self.mainmenu, text="Start", font=tk.CTkFont("Segoe", 35, "normal"))
        self.privacyButton = tk.CTkButton(self.mainmenu, text="Privacy", font=tk.CTkFont("Segoe", 35, "normal"))
        self.exitButton = tk.CTkButton(self.mainmenu, text="Exit", font=tk.CTkFont("Segoe", 35, "normal"), command=self.mainmenu.quit)

        self.mainTitle.grid(row=0, column=0)
        self.startButton.grid(row=1, column=0, pady=5)
        self.privacyButton.grid(row=2, column=0, pady=5)
        self.exitButton.grid(row=3, column=0, pady=5)

        self.mainmenu.pack(anchor=CENTER, expand=True)

app().mainloop()