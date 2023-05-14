import tkinter as tk


class ServerView:
    def __init__(self, start_callback, stop_callback):
        self.root = tk.Tk()
        self.start_callback = start_callback
        self.stop_callback = stop_callback

        self.root.title("Server")
        self.root.geometry("400x200")
        self.root.configure(bg="green")
        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_callback, bg="black", fg="white")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Server", command=self.stop_callback, state=tk.DISABLED,  bg="black", fg="white")
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Not Running")
        self.status_label.pack(pady=10)

    def set_status(self, status):
        self.status_label.config(text=status)

    def set_start_button_state(self, state):
        self.start_button.config(state=state)

    def set_stop_button_state(self, state):
        self.stop_button.config(state=state)
