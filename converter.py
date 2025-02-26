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


_current_file_path = ""

def audio_to_spectrogram(file_path, colormap):
    """Convertit un fichier audio en spectrogramme."""
    # Charger le fichier audio
    y, sr = librosa.load(file_path)

    # Calculer le spectrogramme
    d = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    # Afficher le spectrogramme
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(d, sr=sr, x_axis='time', y_axis='log', cmap=colormap)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogramme')
    plt.tight_layout()

    return plt.gcf()

def load_audio_file():
    """Charge un fichier audio et met à jour le spectrogramme."""
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
    if file_path:
        global _current_file_path
        _current_file_path = file_path
        file_name_label.config(text=f"Fichier chargé: {file_path.split('/')[-1]}")
        update_spectrogram()

def update_spectrogram():
    """Met à jour le spectrogramme avec les paramètres actuels."""
    if '_current_file_path' in globals():
        colormap = colormap_var.get()
        fig = audio_to_spectrogram(_current_file_path, colormap)
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

# Configuration de l'interface graphique
root = tk.Tk()
root.title("Spectrogramme Audio")
root.protocol("WM_DELETE_WINDOW", on_closing)

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

load_button = ttk.Button(main_frame, text="Charger un fichier audio", command=load_audio_file)
load_button.grid(row=0, column=0, pady=5)

file_name_label = ttk.Label(main_frame, text="Aucun fichier chargé")
file_name_label.grid(row=1, column=0, pady=5)

colormap_label = ttk.Label(main_frame, text="Choisir la colormap:")
colormap_label.grid(row=2, column=0, pady=5)

colormap_var = tk.StringVar()
colormap_combobox = ttk.Combobox(main_frame, textvariable=colormap_var)
colormap_combobox['values'] = plt.colormaps()
colormap_combobox.current(0)
colormap_combobox.grid(row=3, column=0, pady=5)
colormap_combobox.bind("<<ComboboxSelected>>", lambda _: update_spectrogram())

save_button = ttk.Button(main_frame, text="Enregistrer l'image", command=save_spectrogram)
save_button.grid(row=4, column=0, pady=5)

fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.get_tk_widget().grid(row=5, column=0, pady=10)

root.mainloop()
