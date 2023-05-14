import socket
import threading
from tkinter import filedialog, messagebox
from PIL import Image
from views.server_view import ServerView


class ServerController:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.receive_thread = None
        self.host = 'localhost'
        self.port = 5000
        self.connected = False
        self.view = ServerView(self.start_server, self.stop_server)
        self.view.root.mainloop()
    def start_server(self):
        self.view.set_start_button_state("disabled")
        self.view.set_stop_button_state("normal")

        self.server_thread = threading.Thread(target=self.start_server_thread)
        self.server_thread.start()

    def start_server_thread(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.connected = True
            self.view.set_status(f"Server running on {self.host}:{self.port}")
            while self.connected:
                self.client_socket, client_address = self.server_socket.accept()
                self.receive_thread = threading.Thread(target=self.receive_image, args=(self.client_socket,))
                self.receive_thread.start()
        except Exception as e:
            self.view.set_status(f"Error: {e}")
            self.stop_server()

    def stop_server(self):
        self.connected = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join()
        self.view.set_status("Not Running")
        self.view.set_start_button_state("normal")
        self.view.set_stop_button_state("disabled")

    def receive_image(self, client_socket):
        try:
            # Receive the filename from the client
            filename = client_socket.recv(1024).decode()

            # Show a save dialog to select the path to save the image
            save_path = filedialog.asksaveasfilename(initialdir="./", title="Save Image As", initialfile=filename,
                                                     filetypes=[("PNG Image", "*.png"),("JPEG Image","*.jpg")])

            # If the user cancelled the save dialog, send a cancel message to the client and return
            if not save_path:
                client_socket.sendall(b"cancel")
                return

            # If the user selected a valid save path, send an "ok" message to the client
            client_socket.sendall(b"ok")

            # Receive the image data from the client and save it to the selected file path
            with open(save_path, "wb") as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)

            # Show a success message and open the saved image in a new window
            self.view.set_status(f"Image received and saved as {save_path}")
            self.view.set_status(save_path)

        except Exception as e:
            # Show an error message if the image reception failed
            self.view.show_error(f"Failed to receive image: {e}")

        finally:
            # Close the client socket
            client_socket.close()
