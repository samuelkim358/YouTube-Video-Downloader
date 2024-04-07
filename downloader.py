# import all the libraries
import customtkinter as ctk
import yt_dlp
import threading
import re
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the paths to ffmpeg.exe and icon.ico relative to the script directory
ffmpeg_path = os.path.join(script_dir, "ffmpeg.exe")
icon_path = os.path.join(script_dir, "icon.ico")

# function to get the download percentage
def progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = d['_percent_str']
        match = re.search(r'(\d+\.\d+)%', percent_str)
        percentage = float(match.group(1)) / 100 if match else 0
        progress_label.configure(text=f"Progress: {percentage * 100:.2f}%")
        progress_bar.set(percentage)

# function to download video
def download_video():
    # get resolution for the video
    url = entry_url.get()
    resolution = resolution_var.get()

    # update the UI to show the progress of the download
    progress_label.configure(text="Progress: 0%")
    progress_label.pack(pady=(10, 5))
    progress_bar.set(0)
    progress_bar.pack(pady=(10, 5))
    status_label.configure(text="")
    status_label.pack(pady=(10, 5))

    # specify the format of the video and include ffmpeg
    try:
        ydl_opts = {
            'format': f'bv[height<={resolution}]+ba/b[height<={resolution}]',
            'progress_hooks': [progress_hook],
            'ffmpeg_location': ffmpeg_path
        }
        
        # download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            status_label.configure(text="Video Downloaded!")

    # if error print error
    except Exception as e:
        status_label.configure(text=e)


# set the GUI of the app
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root.title("Youtube Downloader")
root.iconbitmap(icon_path)
root.geometry("720x480")
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# URL input 
url_label = ctk.CTkLabel(content_frame, text="↓↓↓ Enter the YouTube video link here ↓↓↓")
entry_url = ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=(10,5))
entry_url.pack(pady=(10.5))

# download button
download_button = ctk.CTkButton(content_frame, text="Download", command=lambda:threading.Thread(target=download_video).start())
download_button.pack(pady=(10, 5))

# resolutions available and combobox
resolutions = ["2160", "1440", "1080", "720", "480", "360", "240", "144"]
resolution_var = ctk.StringVar()
resolution_combobox = ctk.CTkComboBox(content_frame, values=resolutions, variable=resolution_var)
resolution_combobox.pack(pady=(10, 5))
resolution_combobox.set("720")

# declare progress UI elements
progress_label = ctk.CTkLabel(content_frame)
progress_bar = ctk.CTkProgressBar(content_frame, width=400)
status_label = ctk.CTkLabel(content_frame)

# change the appearance of the GUI
light_mode_button = ctk.CTkButton(content_frame, text="Light mode", command=lambda:ctk.set_appearance_mode("light"))
light_mode_button.place(relx=0.29, rely=0.9, anchor="s")
system_mode_button = ctk.CTkButton(content_frame, text="Same as system", command=lambda:ctk.set_appearance_mode("system"))
system_mode_button.place(relx=0.5, rely=0.9, anchor="s")
dark_mode_button = ctk.CTkButton(content_frame, text="Dark mode", command=lambda:ctk.set_appearance_mode("dark"))
dark_mode_button.place(relx=0.71, rely=0.9, anchor="s")

# run the app
root.mainloop()
