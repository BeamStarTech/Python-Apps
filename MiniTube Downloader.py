import tkinter as tk
from tkinter import Entry, Button, Listbox, Scrollbar, Label, messagebox, END
from youtubesearchpython import VideosSearch
from pytube import YouTube
import pygame
import os
import platform
import threading

# Function to get the appropriate music folder path based on the operating system
def get_music_folder():
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.path.expanduser("~"), "Music")
    elif system == 'Darwin':  # macOS
        return os.path.join(os.path.expanduser("~"), "Music")
    elif system == 'Linux':
        return os.path.join(os.path.expanduser("~"), "Music")
    else:
        return os.path.join(os.path.expanduser("~"), "Downloads")

def get_video_folder():
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.path.expanduser("~"), "Videos")  # Change "Videos" to your preferred folder name
    elif system == 'Darwin':  # macOS
        return os.path.join(os.path.expanduser("~"), "Videos")
    elif system == 'Linux':
        return os.path.join(os.path.expanduser("~"), "Videos")
    else:
        return os.path.join(os.path.expanduser("~"), "Downloads")

def search_music():
    query = entry.get()
    videos_search = VideosSearch(query, limit=10)
    results = videos_search.result()

    listbox.delete(0, tk.END)
    for result in results['result']:
        title = result['title']
        video_id = result['id']
        listbox.insert(tk.END, title)
        video_urls[title] = f"https://www.youtube.com/watch?v={video_id}"

def download_audio_and_play():
    download_audio()

def download_audio():
    selected_item = listbox.curselection()
    if selected_item:
        title = listbox.get(selected_item)
        url = video_urls.get(title, '')
        if url:
            show_downloading_message()
            download_thread = threading.Thread(target=download_audio_file, args=(url,))
            download_thread.start()

def download_video_and_convert_to_mp4():
    download_video()

def download_video():
    selected_item = listbox.curselection()
    if selected_item:
        title = listbox.get(selected_item)
        url = video_urls.get(title, '')
        if url:
            show_downloading_message()
            download_thread = threading.Thread(target=download_video_file, args=(url,))
            download_thread.start()

def download_audio_file(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        music_folder = get_music_folder()
        download_path = os.path.join(music_folder, yt.title + ".mp3")
        stream.download(output_path=music_folder, filename=yt.title + ".mp3")

        show_download_message(download_path)

    except Exception as e:
        print(f"Error downloading audio: {e}")

def download_video_file(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_folder = get_video_folder()  # Use the video folder path
        download_path = os.path.join(video_folder, yt.title + ".mp4")  # Save to the "Video" folder
        stream.download(output_path=video_folder, filename=yt.title + ".mp4")

        show_download_message(download_path)

    except Exception as e:
        print(f"Error downloading video: {e}")

def show_downloading_message():
    message_label.config(text="Downloading... Please do not close the window.")

def show_download_message(download_path):
    message_label.config(text=f"The file has been saved to the Music/Video folder:\n{download_path}")

app = tk.Tk()
app.title("MiniTube Music & Video Downloader")

# Create and pack a title label
title_label = Label(app, text="MiniTube Music & Video Downloader", font=("Arial", 16))
title_label.pack(pady=10)

# Create and pack an entry field
entry = Entry(app, font=("Arial", 12), width=40)
entry.pack(pady=5)

# Create and pack a search button
search_button = Button(app, text="Search", font=("Arial", 12), command=search_music)
search_button.pack(pady=5)

# Create and pack a listbox
listbox = Listbox(app, selectmode=tk.SINGLE, font=("Arial", 12), height=10, width=50)
listbox.pack()

# Create and pack a scrollbar for the listbox
scrollbar = Scrollbar(app)
scrollbar.pack()
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Create and pack a download audio button
download_audio_button = Button(app, text="Download Audio", font=("Arial", 12), command=download_audio_and_play)
download_audio_button.pack(pady=5)

# Create and pack a download video button
download_video_button = Button(app, text="Download Video", font=("Arial", 12), command=download_video_and_convert_to_mp4)
download_video_button.pack(pady=5)

# Create a Label for status messages
message_label = Label(app, text="", font=("Arial", 12))
message_label.pack(pady=10)

video_urls = {}

app.mainloop()
