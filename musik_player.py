import os
import pygame
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, END

def add_songs():
    files = filedialog.askopenfilenames(filetypes=[("MP3 Dateien", "*.mp3")])
    for file in files:
        playlist.insert(END, file)

def play_song(event=None):
    selected = playlist.curselection()
    if selected:
        song = playlist.get(selected[0])
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        song_label.config(text=f"Aktuell: {os.path.basename(song)}")

def stop_song():
    pygame.mixer.music.stop()
    song_label.config(text="Kein Song läuft.")

def set_volume(val):
    volume = float(val)
    pygame.mixer.music.set_volume(volume)

def next_song():
    selected = playlist.curselection()
    if selected and selected[0] < playlist.size() - 1:
        playlist.selection_clear(0, END)
        playlist.selection_set(selected[0] + 1)
        play_song()

def prev_song():
    selected = playlist.curselection()
    if selected and selected[0] > 0:
        playlist.selection_clear(0, END)
        playlist.selection_set(selected[0] - 1)
        play_song()

# Initialisiere pygame
pygame.mixer.init()

# Erstelle das Fenster mit ttkbootstrap
root = ttk.Window(themename="cyborg")
root.title("🎵 Moderner Musikplayer")

# Nutze die klassische Tkinter-Listbox und style sie farbig
playlist = tk.Listbox(
    root,
    width=60,
    bg="#21252b",
    fg="#61dafb",
    font=("Segoe UI", 12),
    selectbackground="#61dafb",
    selectforeground="#21252b",
    borderwidth=0,
    highlightthickness=0
)
playlist.pack(padx=10, pady=10)

playlist.bind('<Double-1>', play_song)  # Doppelklick auf Song startet ihn

# Steuerungs-Buttons in einem Frame
controls_frame = ttk.Frame(root)
controls_frame.pack(pady=5)

add_btn = ttk.Button(controls_frame, text="Lieder hinzufügen", command=add_songs, bootstyle="info-outline")
add_btn.grid(row=0, column=0, padx=5)

play_btn = ttk.Button(controls_frame, text="Abspielen", command=play_song, bootstyle="success")
play_btn.grid(row=0, column=1, padx=5)

stop_btn = ttk.Button(controls_frame, text="Stopp", command=stop_song, bootstyle="danger")
stop_btn.grid(row=0, column=2, padx=5)

prev_btn = ttk.Button(controls_frame, text="<< Zurück", command=prev_song, bootstyle="secondary")
prev_btn.grid(row=0, column=3, padx=5)

next_btn = ttk.Button(controls_frame, text="Weiter >>", command=next_song, bootstyle="secondary")
next_btn.grid(row=0, column=4, padx=5)

# Song-Anzeige
song_label = ttk.Label(root, text="Kein Song läuft.", font=("Segoe UI", 12), bootstyle="inverse-dark")
song_label.pack(pady=10)

# Lautstärkeregler
volume_label = ttk.Label(root, text="Lautstärke", bootstyle="secondary")
volume_label.pack()
volume_slider = ttk.Scale(root, from_=0, to=1, orient="horizontal", command=set_volume, bootstyle="info")
volume_slider.set(0.5)
volume_slider.pack(pady=10)

root.mainloop()
