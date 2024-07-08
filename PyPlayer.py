import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("PyPlayer")
        self.music_files = []
        self.mixer = pygame.mixer
        self.mixer.init()  # Initialize Pygame mixer
        self.mixer.music.set_volume(0.7)
        self.is_playing = False
        self.paused_at = 0
        self.music_length = 0

        self.create_gui()

    def create_gui(self):
        # Create frames and widgets
        self.library_frame = tk.Frame(self.root)
        self.library_frame.pack()

        self.listbox = tk.Listbox(self.library_frame, width=30, height=10, selectmode=tk.MULTIPLE)
        self.listbox.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.library_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack()

        self.start_button = tk.Button(self.buttons_frame, text="Start", command=self.play_music)
        self.start_button.pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(self.buttons_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(side=tk.LEFT)

        self.play_pause_button = tk.Button(self.buttons_frame, text="Play/Pause", command=self.toggle_playback)
        self.play_pause_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.buttons_frame, text="Stop", command=self.stop_music)
        self.stop_button.pack(side=tk.LEFT)

        self.add_remove_frame = tk.Frame(self.root)
        self.add_remove_frame.pack()

        self.add_button = tk.Button(self.add_remove_frame, text="Add", command=self.add_music)
        self.add_button.pack(side=tk.LEFT)

        self.remove_button = tk.Button(self.add_remove_frame, text="Remove", command=self.remove_music)
        self.remove_button.pack(side=tk.LEFT)

    def add_music(self):
        music_files_temp = filedialog.askopenfilenames(initialdir="/", title="Select Music File", filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")))
        if music_files_temp:
            for file in music_files_temp:
                filename = os.path.basename(file)  # Extract filename
                self.listbox.insert(tk.END, filename)
                self.music_files.append(file)  # Store the full path

    def remove_music(self):
        try:
            selected_indices = self.listbox.curselection()
            for index in sorted(selected_indices, reverse=True):
                self.listbox.delete(index)
                self.music_files.pop(index)
        except Exception as e:
            print(f"Error: {e}")

    def play_music(self):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            for index in selected_indices:
                file = self.listbox.get(index)
                filepath = self.music_files[index]
                if filepath:
                    self.mixer.music.load(filepath)
                    if self.paused_at > 0:
                        self.mixer.music.play(start=self.paused_at)
                    else:
                        self.mixer.music.play()
                    self.is_playing = True
                    self.music_length = self.mixer.Sound(filepath).get_length()
                    self.update_progress_bar()
        else:
            messagebox.showinfo("Error", "Choose a song then press 'Start'")

    def toggle_playback(self):
        if self.is_playing:
            self.paused_at = self.mixer.music.get_pos() / 1000
            self.mixer.music.pause()
            self.is_playing = False
            self.root.after_cancel(self.update_progress_bar)  # Stop the progress bar update
            self.play_pause_button.config(text="Resume")
        else:
            if self.paused_at > 0:
                self.mixer.music.unpause()
                self.mixer.music.set_pos(self.paused_at)
                self.is_playing = True
                self.update_progress_bar()
                self.play_pause_button.config(text="Pause")
            elif self.listbox.size() > 0:
                self.play_music()
                self.play_pause_button.config(text="Pause")
            else:
                messagebox.showinfo("Error", "Choose a song then press 'Start'")

    def stop_music(self):
        self.mixer.music.stop()
        self.is_playing = False
        self.paused_at = 0
        self.play_pause_button.config(text="Play/Pause")

    def update_progress_bar(self):
        if self.is_playing:
            current_position = self.mixer.music.get_pos() / 1000
            self.progress_bar["value"] = int(current_position / self.music_length * 100)
            self.root.after(100, self.update_progress_bar)  # Use root.after instead of

if __name__ == "__main__":
    pygame.init()  # Initialize Pygame
    root = tk.Tk()
    music_player = MusicPlayer(root)

    # Define the on_closing function
    def on_closing(root):
        pygame.quit()  # Quit Pygame
        root.destroy()  # Close the Tkinter window

    # Add a protocol to quit Pygame when the window is closed
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    root.mainloop()
