import tkinter as tk
from tkinter import ttk
import winsound
from tkinter import messagebox

# Create main window
window = tk.Tk()
window.title("Virtual Piano")

# Create piano keyboard frame
keyboard_frame = ttk.Frame(window)
keyboard_frame.pack(pady=20)

# Define MIDI note numbers
midi_notes = {
    "a": 261.63,  # C4
    "s": 293.66,  # D4
    "d": 329.63,  # E4
    "f": 349.23,  # F4
    "g": 392.00,  # G4
    "h": 440.00,  # A4
    "j": 493.88,  # B4
    "k": 523.25,  # C5
    "l": 587.33,  # D5
    ";": 659.26,  # E5
    "'": 698.46,  # F5
}

# Define key binding functions
def play_midi(event, key):
    if key in midi_notes:
        winsound.Beep(int(midi_notes[key]), 500)  # Play MIDI note for 500ms

def play_midi_held(event, key):
    if key in midi_notes:
        winsound.Beep(int(midi_notes[key]), 0)  # Play MIDI note indefinitely

def stop_midi(event, key):
    if key in midi_notes:
        winsound.Beep(0, 0)  # Stop any currently playing sound

# Create keyboard keys
key_labels = ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'"]
for i, label in enumerate(key_labels):
    key_button = ttk.Button(keyboard_frame, text=label, width=5)
    key_button.grid(row=0, column=i, padx=5)
    if label == ";":
        key_button.bind("<Button-1>", lambda event, key=";": play_midi_held(event, key))
        key_button.bind("<ButtonRelease-1>", lambda event, key=";": stop_midi(event, key))
    elif label == "'":
        key_button.bind("<Button-1>", lambda event, key="'": play_midi_held(event, key))
        key_button.bind("<ButtonRelease-1>", lambda event, key="'": stop_midi(event, key))
    else:
        key_button.bind("<Button-1>", lambda event, key=label.lower(): play_midi_held(event, key))
        key_button.bind("<ButtonRelease-1>", lambda event, key=label.lower(): stop_midi(event, key))

# Bind all corresponding keyboard keys
keyboard_keys = {
    "a": "<a>",
    "s": "s",
    "d": "<d>",
    "f": "<f>",
    "g": "<g>",
    "h": "<h>",
    "j": "<j>",
    "k": "<k>",
    "l": "<l>",
    ";": ";",
    "'": "'",
}

for key, binding in keyboard_keys.items():
    window.bind(binding, lambda event, key=key: play_midi(event, key))
    window.bind(f"{binding}+Release", lambda event, key=key: stop_midi(event, key))

# Create pitch buttons
pitch_buttons_frame = ttk.Frame(window)
pitch_buttons_frame.pack(pady=20)

def increase_pitch():
    global midi_notes
    new_midi_notes = {
        key: midi_notes[key] * 1.059463094 for key in midi_notes}
    if 37 <= min(new_midi_notes.values()) and max(new_midi_notes.values()) <= 32767:
        midi_notes = new_midi_notes
    else:
        messagebox.showerror("Error", "Pitch is out of range. Please adjust the pitch.")

def decrease_pitch():
    global midi_notes
    new_midi_notes = {
        key: midi_notes[key] / 1.059463094 for key in midi_notes}
    if 37 <= min(new_midi_notes.values()) and max(new_midi_notes.values()) <= 32767:
        midi_notes = new_midi_notes
    else:
        messagebox.showerror("Error", "Pitch is out of range. Please adjust the pitch.")

increase_pitch_button = ttk.Button(pitch_buttons_frame, text="Increase Pitch", command=increase_pitch)
increase_pitch_button.grid(row=0, column=0, padx=5)

decrease_pitch_button = ttk.Button(pitch_buttons_frame, text="Decrease Pitch", command=decrease_pitch)
decrease_pitch_button.grid(row=0, column=1, padx=5)

window.mainloop()
