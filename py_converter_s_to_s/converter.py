# py_converter_s_to_s/converter.py
"""This application provides functionality for converting audio files using the librosa library.
It includes functions for loading audio files, displaying waveforms, and saving in various formats.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QAction
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

CURRENT_FILE_PATH = ""
FILE_NAME_LABEL = None
CANVAS = None
FIG = None

def audio_to_spectrogram(file_path, cmap):
    """Convertit un fichier audio en spectrogramme."""
    # Charger le fichier audio
    y, sr = librosa.load(file_path)

    # Calculer le spectrogramme
    d = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    # Caclul taille du spectrogramme
    canvas_width, canvas_height = CANVAS.get_width_height()

    # Afficher le spectrogramme
    plt.figure(figsize=(canvas_height/100, canvas_width/100))
    librosa.display.specshow(d, sr=sr, x_axis='time', y_axis='log', cmap=cmap)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogramme')
    plt.tight_layout()

    return plt.gcf()

def load_audio_file():
    """Charge un fichier audio et met à jour le spectrogramme."""
    file_path, _ = QFileDialog.getOpenFileName(None, "Open Audio File", "",
                                               "Audio Files (*.wav *.mp3 *.flac)")
    if file_path:
        global CURRENT_FILE_PATH
        CURRENT_FILE_PATH = file_path
        FILE_NAME_LABEL.setText(f"Fichier chargé : {file_path.split('/')[-1]}")
        update_spectrogram(cmap='viridis')

def update_spectrogram(cmap='viridis'):
    """Met à jour le spectrogramme avec les paramètres actuels."""
    if globals().get('CURRENT_FILE_PATH'):
        global FIG
        FIG = audio_to_spectrogram(CURRENT_FILE_PATH, cmap)
        CANVAS.figure = FIG
        CANVAS.draw()

def save_spectrogram():
    """Enregistre le spectrogramme dans un fichier PNG."""
    file_path, _ = QFileDialog.getSaveFileName(None, "Save Spectrogram", "", "PNG files (*.png)")
    if file_path:
        CANVAS.figure.saveFIG(file_path)

def on_closing():
    """Fonction appelée lorsque la fenêtre est fermée."""
    QApplication.quit()

class MainWindow(QMainWindow):
    """Classe principale pour la fenêtre de l'application."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spectrogramme Audio")
        # Get screen dimensions
        screen_width = self.screen().size().width()
        screen_height = self.screen().size().height()

        # Set window size to 75% of screen dimensions
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)
        self.setGeometry(100, 100, window_width, window_height)

        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur."""
        global FILE_NAME_LABEL, CANVAS, FIG

        # Create the main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Create the file name label
        FILE_NAME_LABEL = QLabel("Aucun fichier chargé")
        layout.addWidget(FILE_NAME_LABEL)

        # Create the figure and CANVAS for the spectrogram
        FIG, _ = plt.subplots()
        CANVAS = FigureCanvas(FIG)
        layout.addWidget(CANVAS)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Create the menu bar
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Fichier")
        load_action = QAction("Charger un fichier audio", self)
        load_action.triggered.connect(load_audio_file)
        file_menu.addAction(load_action)

        save_action = QAction("Enregistrer le spectrogramme", self)
        save_action.triggered.connect(save_spectrogram)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(on_closing)
        file_menu.addAction(quit_action)

        colormap_menu = menu_bar.addMenu("Colormap")
        for colormap in plt.colormaps():
            colormap_action = QAction(colormap, self)
            colormap_action.triggered.connect(lambda checked,
                                        cmap=colormap: update_spectrogram(cmap))
            colormap_menu.addAction(colormap_action)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
