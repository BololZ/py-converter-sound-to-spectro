"""
This application provides functionality for converting audio files using the librosa library.
It includes functions for loading audio files, displaying waveforms,
and other audio processing tasks.
"""

import tkinter as tk
from tkinter import filedialog, ttk
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


CURRENT_FILE_PATH = ""

def audio_to_spectrogram(file_path, cmap):
    """Convertit un fichier audio en spectrogramme."""
    # Charger le fichier audio
    y, sr = librosa.load(file_path)

    # Calculer le spectrogramme
    d = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

        # Get the current size of the canvas
    canvas_width = canvas.get_tk_widget().winfo_width()
    canvas_height = canvas.get_tk_widget().winfo_height()

    # Calculate the figsize based on the canvas size
    figsize = (canvas_width / 100, canvas_height / 100)

    # Afficher le spectrogramme
    plt.figure(figsize=figsize)
    librosa.display.specshow(d, sr=sr, x_axis='time', y_axis='log', cmap=cmap)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogramme')
    plt.tight_layout()

    return plt.gcf()

def load_audio_file():
    """Charge un fichier audio et met à jour le spectrogramme."""
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
    if file_path:
        global CURRENT_FILE_PATH
        CURRENT_FILE_PATH = file_path
        file_name_label.config(text=f"Fichier chargé: {file_path.split('/')[-1]}")
        update_spectrogram(cmap='viridis')

def update_spectrogram(cmap='viridis'):
    """Met à jour le spectrogramme avec les paramètres actuels."""
    if globals().get('CURRENT_FILE_PATH'):
        fig = audio_to_spectrogram(CURRENT_FILE_PATH, cmap)
        canvas.figure = fig
        canvas.draw()

def save_spectrogram():
    """Enregistre le spectrogramme dans un fichier PNG."""
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if file_path:
        canvas.figure.savefig(file_path)

def on_closing():
    """Fonction appelée lorsque la fenêtre est fermée."""
    root.quit()
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Spectrogramme Audio")

# Create the root theme for the widgets
style = ttk.Style(root)
style.theme_use("vista")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to 75% of screen dimensions
window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)
root.geometry(f"{window_width}x{window_height}")

# Set the protocol for closing the window
root.protocol("WM_DELETE_WINDOW", on_closing)

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Charger un fichier audio", command=load_audio_file)
file_menu.add_command(label="Enregistrer le spectrogramme", command=save_spectrogram)
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=on_closing)
colormap_menu = tk.Menu(menu_bar, tearoff=0)
for colormap in plt.colormaps():
    colormap_menu.add_command(label=colormap,
                              command=lambda cmap=colormap: update_spectrogram(cmap))
menu_bar.add_cascade(label="Fichier", menu=file_menu)
menu_bar.add_cascade(label="Colormap", menu=colormap_menu)
root.config(menu=menu_bar)

# Create the main frame
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, rowspan=4, columnspan=6, sticky=(tk.N, tk.S, tk.E, tk.W))

file_name_label = ttk.Label(main_frame, text="Aucun fichier chargé")
file_name_label.grid(row=2, column=3)

# Create the figure and canvas for the spectrogram
fig, ax = plt.subplots(figsize=(12, 8))
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.get_tk_widget().grid(row=0, column=0, rowspan=2, columnspan=6,
                            sticky=(tk.N, tk.S, tk.E, tk.W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=3)
main_frame.columnconfigure(1, weight=3)
main_frame.columnconfigure(2, weight=3)
main_frame.columnconfigure(3, weight=1)
main_frame.columnconfigure(4, weight=1)
main_frame.rowconfigure(1, weight=1)
canvas.get_tk_widget().rowconfigure(0, weight=1)
canvas.get_tk_widget().columnconfigure(0, weight=3)
canvas.get_tk_widget().columnconfigure(1, weight=3)
canvas.get_tk_widget().columnconfigure(2, weight=3)
canvas.get_tk_widget().columnconfigure(3, weight=1)
canvas.get_tk_widget().columnconfigure(4, weight=1)

if __name__ == "__main__":
    root.mainloop()
