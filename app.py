import os
import tkinter as tk
from pathlib import Path
import qrcode

# Fonts
title_styles = {"font": ("Trebuchet MS Bold", 50),
                "background": "#C0C0C0",
                "foreground": "#000000"}
subtitle_styles = {"font": ("Trebuchet MS Bold", 25),
                   "background": "#C0C0C0",
                   "foreground": "#000000"}
body_styles = {"font": ("Trebuchet MS Bold", 18),
               "background": "#C0C0C0",
               "foreground": "#000000"}


class QRApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('QR App')
        self._frame = None
        self.switch_frame(QRGenerator)

    def switch_frame(self, frame_class):
        """ Method for switching Frames """
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class QRGenerator(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Main Frame (Window)
        main_frame = tk.Frame(self, bg="#C0C0C0",height=200, width=400)
        main_frame.pack_propagate(False)
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Tittle
        label_title = tk.Label(main_frame, title_styles, text="QR Generator")
        label_title.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Content Frame
        self.content_frame = tk.Frame(self, bg="#C0C0C0", height=300, width=600)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(fill="both", expand=True)
        
        # Canvas and QR
        self.canvas = None
        self.qr = None

        # Label file_name
        self.fileName_label = tk.Label( self.content_frame, body_styles, text="Name: ")
        self.fileName_label.grid(row=0, column=0, pady=5)
        # Entry file_name
        self.file_name = tk.Entry( self.content_frame)
        self.file_name.grid(row=0, column=1, pady=1)
        
        # Canvas
        self.canvas = tk.Canvas(self.content_frame, bg="#C0C0C0", height=290, width=290)
        self.canvas.grid(row=0, column=3, rowspan=2, padx=30)

        # Label URL
        self.url_label = tk.Label(self.content_frame, body_styles, text="URL: ")
        self.url_label.grid(row=1, column=0, pady=5)
        # Entry URL
        self.url = tk.Entry(self.content_frame)
        self.url.grid(row=1, column=1, pady=1)
        
        # Messages
        self.message = tk.Label(self.content_frame, text='', bg="#C0C0C0")
        self.message.grid(row=3, column=0, columnspan=2, pady=5)

        # Create QR Code Button
        button_create = tk.Button(self.content_frame, subtitle_styles, text="Generate", bg="#C0C0C0",command=lambda: self.generatorQR())
        button_create.grid(row=4, column=0, sticky=tk.E + tk.W, padx=10, pady=10, columnspan=2)

    def generatorQR(self):
        """ QR Code Generator and Displayer """
        if self.url.index("end") == 0 or self.file_name.index("end") == 0:
            self.message['text'] = 'ERROR! The Name and the URL are requiered.'
            self.message['fg'] = 'red'
        else:
            url = self.url.get()
            file_name = self.file_name.get()
            file_path = f"./img/{file_name}.jpg"

            if not os.path.isfile(file_path):
                img = qrcode.make(url)
                img.save(file_path)
                # Image
                self.qr = tk.PhotoImage(file=file_path)
                self.canvas.create_image(150, 150, image=self.qr)
                # Message
                self.message['text'] = 'The QR Code was succesfully created.'
                self.message['fg'] = 'green'
                # Download Button
                button_download = tk.Button(self.content_frame, subtitle_styles, text="Download", bg="#C0C0C0", command=lambda: self.downloadQR(file_path, file_name))
                button_download.grid(row=4, column=2, sticky=tk.E + tk.W, padx=10, pady=10, columnspan=2)
            else:
                # Mensaje
                self.message['text'] = 'ERROR! The QR Code name already exist.'
                self.message['fg'] = 'red'

    def downloadQR(self, file_path=None, file_name=None):
        """ Download the generated QR Code """
        # Download Path
        downloads_path = str(Path.home() / "Downloads")
        try:
            # Download
            os.rename(file_path, downloads_path + f'/{file_name}.jpg')
            # Message
            self.message['text'] = 'QR Code succesfully downloaded'
            self.message['fg'] = 'green'
        except FileNotFoundError:
            
            # Message
            self.message['text'] = 'QR Code File not found.'
            self.message['fg'] = 'red'
        except NameError:
            # Message
            self.message['text'] = 'QR Code Name not found.'
            self.message['fg'] = 'red'
        except Exception as e:
            # Message
            self.message['text'] = e
            self.message['fg'] = 'red'


if __name__ == "__main__":
    app = QRApp()
    app.mainloop()
    