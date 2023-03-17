# code adapted from https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python

import pyaudio
import numpy as np
import tkinter as tk


class SineWaveGenerator:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def generate_sine(self, frequency, duration, volume):
        sampling_rate = 44100

        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(sampling_rate * duration) * frequency / sampling_rate)).astype(
            np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = self.audio.open(format=pyaudio.paFloat32,
                                 channels=1,
                                 rate=sampling_rate,
                                 output=True)

        # play. May repeat with different volume values (if done interactively)
        stream.write(volume * samples)

        stream.stop_stream()
        stream.close()


def main():
    # Initialize Tkinter object.
    root = tk.Tk()
    root.title("Sound :)")

    # Initialize sine wave generator object.
    sine_gen = SineWaveGenerator()

    # Initialize Tkinter variables.
    freq_var = tk.StringVar(value="400")
    freq_label = tk.Label(root, text="f (Hz): ")
    freq_label.pack(side='left')
    freq_entry = tk.Entry(root, textvariable=freq_var, bd=5)
    freq_entry.pack(side='right')

    # Make Tkinter buttons.
    button = tk.Button(root, text='Click me !', bd='5', command=lambda: sine_gen.generate_sine(int(freq_var.get()), 2, 0.75))
    button.pack(side='top')
    root.mainloop()


if __name__ == "__main__":
    main()
