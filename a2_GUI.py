# a2_GUI.py

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from a2_Function import apply_filter

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter App")

        self.file_path_label = tk.Label(self.root, text="")
        self.file_path_label.pack()

        self.file_path = None
        self.image = None
        self.filtered_image = None

        self.create_widgets()

    def create_widgets(self):
        self.open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        self.open_button.pack(pady=10)

        self.filter_type_label = tk.Label(self.root, text="Filter Type:")
        self.filter_type_label.pack()
        self.filter_type_var = tk.StringVar()
        self.filter_type_var.set("Low Pass")
        self.filter_type_menu = tk.OptionMenu(self.root, self.filter_type_var, "Low Pass", "High Pass")
        self.filter_type_menu.pack()

        self.cutoff_label = tk.Label(self.root, text="Cutoff Frequency:")
        self.cutoff_label.pack()
        self.cutoff_scale = tk.Scale(self.root, from_=0, to=200, orient='horizontal')
        self.cutoff_scale.pack()

        self.filter_button = tk.Button(self.root, text="Apply Filter", command=self.apply_filter)
        self.filter_button.pack(pady=10)

        self.img_label = tk.Label(self.root)
        self.img_label.pack()

    def open_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.file_path:
         self.file_path_label.config(text="File Path: " + self.file_path)
        self.image = cv2.imread(self.file_path)
        if self.image is not None:
            self.image = cv2.resize(self.image, (800, 600))  # Resize the image
            self.update_image()

    def apply_filter(self):
        if self.image is not None:
            filter_type = self.filter_type_var.get().lower().replace(" ", "_")
            cutoff_frequency = self.cutoff_scale.get() / 100.0
            self.filtered_image = apply_filter(self.image, filter_type=filter_type, cutoff_frequency=cutoff_frequency)
            self.update_image()

    def update_image(self):
        if self.image is not None:
            img = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            img = ImageTk.PhotoImage(img)
            self.img_label.config(image=img)
            self.img_label.image = img

            if self.filtered_image is not None:
                filtered_img = Image.fromarray(cv2.cvtColor(self.filtered_image, cv2.COLOR_BGR2RGB))
                filtered_img = ImageTk.PhotoImage(filtered_img)
                self.img_label.config(image=filtered_img)
                self.img_label.image = filtered_img

root = tk.Tk()
app = ImageFilterApp(root)
root.mainloop()
