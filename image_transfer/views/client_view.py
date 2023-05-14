import tkinter as tk
from tkinter import filedialog

class ClientView:
    def __init__(self, select_image_callback, send_image_callback):
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.geometry("400x200")
        self.root.configure(bg="green")
        self.select_button = tk.Button(self.root, text="Select Image", command=select_image_callback, bg="black", fg="white")
        self.select_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Select an image",  bg="black", fg="white")
        self.status_label.pack(pady=10)

        self.send_button = tk.Button(self.root, text="Send Image", command=send_image_callback, state=tk.DISABLED,  bg="black",fg="white")
        self.send_button.pack(pady=10)


    def set_status_label(self, text):
        self.status_label.config(text=text)

    def enable_send_button(self):
        self.send_button.config(state=tk.NORMAL)

    def disable_send_button(self):
        self.send_button.config(state=tk.DISABLED)

    def get_file_path(self):
        return filedialog.askopenfilename(initialdir="./", title="Select Image",
                                          filetypes=[("PNG Image", "*.png"),("JPEG Image","*.jpg")])
