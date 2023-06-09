import tkinter as tk
import pyaudio
import numpy as np
from PIL import Image, ImageTk
from collections import defaultdict

# Define the notes and their corresponding frequencies
NOTES = {
    'C': 261.63,
    'Db': 277.18,
    'D': 293.66,
    'Eb': 311.13,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'Ab': 415.30,
    'A': 440.00,
    'Bb': 466.16,
    'B': 493.88
}

# Define the octave range
OCTAVE_RANGE = 3  # Number of octaves to display

# Function to generate a sine wave for a given frequency and duration
def generate_tone(frequency, duration):
    sample_rate = 44100  # CD quality audio
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    return tone

# Function to play a note
def play_note(note):
    frequency = NOTES.get(note)
    if frequency:
        tone = generate_tone(frequency, 0.3)
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
        stream.write(tone.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Function to handle key press events
def on_key_press(event):
    key = event.char.upper()
    play_note(key)
    if key in key_buttons:
        key_buttons[key].config(relief=tk.SUNKEN)
        active_keys.add(key)

# Function to handle key release events
def on_key_release(event):
    key = event.char.upper()
    if key in key_buttons:
        key_buttons[key].config(relief=tk.RAISED)
        active_keys.discard(key)

# Function to handle octave selection
def on_octave_change(event):
    selected_octave = int(octave_var.get())
    start_index = selected_octave * 12
    end_index = start_index + 12
    for i, (note, _) in enumerate(NOTES.items()):
        if i >= start_index and i < end_index:
            key_buttons[note].grid(row=0, column=i-start_index, padx=(0, 2))
            label_buttons[note].grid(row=1, column=i-start_index)
        else:
            key_buttons[note].grid_forget()
            label_buttons[note].grid_forget()

# Function to handle recording
def start_recording():
    global recording
    recording = True
    recorded_notes.clear()

def stop_recording():
    global recording
    recording = False

def play_recorded_sequence():
    for note in recorded_notes:
        play_note(note)

# Create the main window
window = tk.Tk()
window.title("Piano App")
window.configure(bg="#f1f1f1")

# Load piano key images
white_key_image = ImageTk.PhotoImage(Image.open("white_key.png"))
black_key_image = ImageTk.PhotoImage(Image.open("black_key.png"))

# Create piano keys and labels
key_buttons = {}
label_buttons = {}
active_keys = set()
recording = False
recorded_notes = []

# Create piano keys and labels
for note, _ in NOTES.items():
    if note.endswith("#"):
        btn = tk.Button(window, image=black_key_image, width=30, height=120, bd=0, highlightthickness=0)
        lbl = tk.Label(window, text=note[:-1], fg='white', bg='black', font=('Arial', 12))
    else:
        btn = tk.Button(window, image=white_key_image, width=50, height=200, bd=0, highlightthickness=0)
        lbl = tk.Label(window, text=note, fg='black', bg='#f1f1f1', font=('Arial', 12))
    btn.config(command=lambda n=note: play_note(n))
    key_buttons[note] = btn
    label_buttons[note] = lbl

# Position the piano keys and labels
for i, (note, _) in enumerate(NOTES.items()):
    if i < OCTAVE_RANGE * 12:
        if NOTES[list(NOTES.keys())[i]].is_integer():
            key_buttons[note].grid(row=0, column=i, padx=(0, 2))
            label_buttons[note].grid(row=1, column=i)
        else:
            key_buttons[note].grid(row=0, column=i, padx=(5, 2))
            label_buttons[note].grid(row=1, column=i)

# Bind key press and release events to the main window
window.bind('<KeyPress>', on_key_press)
window.bind('<KeyRelease>', on_key_release)

# Octave selection
octave_var = tk.StringVar()
octave_var.set("0")
octave_var.trace('w', on_octave_change)
octave_label = tk.Label(window, text="Octave:", font=('Arial', 12), bg='#f1f1f1')
octave_dropdown = tk.OptionMenu(window, octave_var, *range(OCTAVE_RANGE), command=on_octave_change)
octave_label.grid(row=2, column=0, padx=(10, 0), pady=10)
octave_dropdown.grid(row=2, column=1, pady=10)

# Recording controls
record_button = tk.Button(window, text="Record", font=('Arial', 12), command=start_recording)
stop_button = tk.Button(window, text="Stop", font=('Arial', 12), command=stop_recording)
play_button = tk.Button(window, text="Play", font=('Arial', 12), command=play_recorded_sequence)
record_button.grid(row=2, column=2, padx=10, pady=10)
stop_button.grid(row=2, column=3, padx=10, pady=10)
play_button.grid(row=2, column=4, padx=10, pady=10)

# Function to handle key press events
def on_key_press(event):
    key = event.char.upper()
    play_note(key)
    if key in key_buttons:
        key_buttons[key].config(relief=tk.SUNKEN)
        active_keys.add(key)
        if recording:
            recorded_notes.append(key)

# Function to handle key release events
def on_key_release(event):
    key = event.char.upper()
    if key in key_buttons:
        key_buttons[key].config(relief=tk.RAISED)
        active_keys.discard(key)

# Bind key press and release events to the main window
window.bind('<KeyPress>', on_key_press)
window.bind('<KeyRelease>', on_key_release)

# Run the application
window.mainloop()
