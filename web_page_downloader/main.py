import socket
import tkinter as tk
import threading
import pathlib
curr_path = pathlib.Path(__file__).parent.resolve()
class Downloader:
    def __init__(self, url):
        self.url = url
        self.host = self.get_host()
        self.path = self.get_path()

    def get_host(self):
        # Extract the host name from the URL
        return self.url.split('/')[2]

    def get_path(self):
        # Extract the path from the URL
        return '/' + '/'.join(self.url.split('/')[3:])

    def download(self):
        # Open a TCP socket connection to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {self.host}...")     
        s.connect((self.host, 80))
        print(f"Connected to {self.host}.")

        # Send an HTTP GET request to the server
        request = f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\nAccept:text/html\r\n\r\n"
        s.send(request.encode())

        # Receive the response from the server
        response = ''
        while True:
            data = s.recv(1024)
            if not data:
                break
            print(data)
            response += data.decode('utf-8', errors='replace')

        # Close the socket connection
        s.close()

        # Save the response to a file
        try:
            print(curr_path)
            with open("tst.html", "w" , encoding="utf-8") as f:
                content = response.split('\r\n\r\n')[1]
                print(f"Writing {len(content)} bytes to file...")
                f.write(content)
                print("File write completed successfully!")
        except Exception as e:
            print(f"Error writing file: {e}")

        

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x100")
        self.root.title("Web Page Downloader")
        self.root.configure(bg="green")

        self.url_label = tk.Label(self.root, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()

        self.download_button = tk.Button(self.root, text="Download", command=self.download, bg="black", fg="white")
        self.download_button.pack()

        self.root.mainloop()

    def download(self):
        url = self.url_entry.get()
        downloader = Downloader(url)
        t = threading.Thread(target=downloader.download)
        t.start()

if __name__ == '__main__':
    gui = GUI()