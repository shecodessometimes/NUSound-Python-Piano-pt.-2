# code adapted from https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python
# and from https://stackoverflow.com/questions/51783787/python-3-x-tkinter-buttons-of-specific-shapes-or-button-overlay

import pyaudio
import numpy as np
import tkinter as tk
# from pynput.keyboard iamport Key, Listener
import keyboard  # using module keyboard


class SineWaveGenerator:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

    # Generate semitone.
    def generate_semitone(self, base_f, semitones):
        freq = base_f * pow(2, (semitones / 12))
        self.generate_sine(freq, 1, 1)

    # Generate sine wave with given parameters.
    def generate_sine(self, frequency, duration, volume):
        sampling_rate = 44100

        # Generate sine wave in form of float32 array.
        samples = (np.sin(2 * np.pi * np.arange(sampling_rate * duration) * frequency / sampling_rate)).astype(
            np.float32)

        # Place the sine wave into the stream. paFloat32 sample values must be in range [-1.0, 1.0].
        stream = self.audio.open(format=pyaudio.paFloat32, channels=1, rate=sampling_rate,output=True)

        # Play the note. May repeat with different volume values (if done interactively).
        stream.write(volume * samples)

        stream.stop_stream()
        stream.close()


def main():
    # Initialize Tkinter object.
    root = tk.Tk()
    root.title("Sound :)")
    root.geometry("500x200")

    # Initialize sine wave generator object.
    sine_gen = SineWaveGenerator()

    # Initialize the piano key info.
    white_keys = 10
    black_keys = [1, 1, 0, 1, 1, 1, 0, 1, 1]

    # Set up the rows.
    for i in range(2):
        root.rowconfigure(i, weight=1)

    # Set up the columns.
    for i in range(white_keys * 3):
        root.columnconfigure(i, weight=1)

    # Function called when piano key is pressed.
    def key_pressed(sine_generator, color, num):
        # Define how many semitones from first note depending on key.
        semitones_white = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]
        semitones_black = [1, 3, 0, 6, 8, 10, 0, 13, 15]

        # Generate actual sound, with given semitones.
        if color == 'White':
            sine_generator.generate_semitone(200, semitones_white[num])
        elif color == 'Black':
            sine_generator.generate_semitone(200, semitones_black[num])

    # Initialize the white piano keys.
    for i in range(white_keys):
        # Initialize the white keys.
        tk.Button(root, bg='white', activebackground='gray87',
                               command=lambda i=i: key_pressed(sine_gen, 'White', i)).grid(
            row=0, column=i * 3, rowspan=2, columnspan=3, sticky='nsew')

    # Initialize the black piano keys.
    for i in range(white_keys - 1):
        if black_keys[i]:
            tk.Button(root, bg='black', activebackground='gray30',
                      command=lambda i=i: key_pressed(sine_gen, 'Black', i)).grid(
                row=0, column=(i * 3) + 2, rowspan=1, columnspan=2, sticky='nsew')

    root.mainloop()


# Simply accesses the main function.
if __name__ == "__main__":
    main()
