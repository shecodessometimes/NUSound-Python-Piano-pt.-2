# code adapted from https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python
# and from https://stackoverflow.com/questions/51783787/python-3-x-tkinter-buttons-of-specific-shapes-or-button-overlay

import pyaudio
import numpy as np
import tkinter as tk
#from pynput.keyboard iamport Key, Listener
import keyboard  # using module keyboard



class SineWaveGenerator:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def generate_semitone(self, base_f, semitones):
        freq = base_f * pow(2, (semitones/12))
        self.generate_sine(freq, 1, 1)

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

    keyboard.wait("a")
    print("A Key Pressed")

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

    def key_pressed(sine_generator, color, num):
        semitones_white = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]
        semitones_black = [1, 3, 0, 6, 8, 10, 0, 13, 15]
        if color == 'White':
            sine_generator.generate_semitone(200, semitones_white[num])
            print(color + ': ' + str(num))
        if color == 'Black':
            sine_generator.generate_semitone(200, semitones_black[num])
            print(color + ': ' + str(num))

    root = tk.Tk()

    root.geometry("500x200")

    white_keys = 10
    black_keys = [1, 1, 0, 1, 1, 1, 0, 1, 1]

    for i in range(white_keys):
        tk.Button(root, bg='white', activebackground='gray87', command=lambda i=i: key_pressed(sine_gen, 'White', i)).grid(row=0,
                                                                                                             column=i * 3,
                                                                                                             rowspan=2,
                                                                                                             columnspan=3,
                                                                                                             sticky='nsew')

    for i in range(white_keys - 1):
        if black_keys[i]:
            tk.Button(root, bg='black', activebackground='gray30', command=lambda i=i: key_pressed(sine_gen,'Black', i)).grid(
                row=0, column=(i * 3) + 2, rowspan=1, columnspan=2, sticky='nsew')

    for i in range(white_keys * 3):
        root.columnconfigure(i, weight=1)

    for i in range(2):
        root.rowconfigure(i, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
