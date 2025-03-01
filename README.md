[![Pylint](https://github.com/BololZ/py-converter-sound-to-spectro/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/BololZ/py-converter-sound-to-spectro/actions/workflows/pylint.yml)


# py-converter-sound-to-spectro

## Description
This project is a Python application that converts sound files into spectrograms. It uses the `librosa` library to process the audio files and `matplotlib` to generate the spectrograms. The application is designed to be user-friendly and can handle various audio formats.

## Features
- Convert sound files to spectrograms.
- Support for multiple audio formats (e.g., WAV, MP3).
- Customizable spectrogram settings (e.g., color map).
- Save the generated spectrograms as image files (e.g., PNG).

## Requirements
- Python 3.12 or higher.
- `librosa` library.
- `matplotlib` library.
- `numpy` library.

## Installation

1. Clone the repository: `git clone https://github.com/BololZ/py-converter-sound-to-spectro.git`

2. Navigate to the project directory: `cd py-converter-sound-to-spectro`

3. Install dependencies: `poetry install --no-root --without dev`

## Usage

To use the application, run the following command in the project directory: `poetry run python py_converter_s_to_s/converter.py`