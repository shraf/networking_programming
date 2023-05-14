import socket
from tkinter import messagebox
from views.client_view import ClientView

class ClientController:
    def __init__(self):
        self.client_socket = None
        self.host = 'localhost'
        self.port = 5000
        self.gui = ClientView(select_image_callback=self.select_image, send_image_callback=self.send_image)
        print(self.gui)
        self.gui.root.mainloop()
        
    def select_image(self):
        print(self)
        file_path = self.gui.get_file_path()
        if file_path:
            self.file_path = file_path
            self.gui.set_status_label(f"Selected image: {file_path}")
            self.gui.enable_send_button()

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_file(self):
        try:
            # Send filename to server
            filename = self.file_path.split("/")[-1]
            self.client_socket.sendall(filename.encode())

            # Wait for server response
            response = self.client_socket.recv(1024).decode()

            # Check if transfer was cancelled
            if response == "cancel":
                self.gui.set_status_label("Image transfer cancelled")
                return

            # Send image data to server
            with open(self.file_path, "rb") as file:
                with self.client_socket.makefile("wb") as socket_file:
                    while True:
                        # Read data from file
                        data = file.read(1024)
                        if not data:
                            break

                        # Send data to server
                        socket_file.write(data)

            # Update status label
            self.gui.set_status_label("Image sent")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send image: {e}")

        finally:
            # Close socket connection
            if self.client_socket:
                self.client_socket.close()

    def send_image(self):
        # Connect to server
        self.connect_to_server()

        # Send file to server
        self.send_file()
