# Have a sound play at a specified interval
import simpleaudio as sa
import os

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets") # Get the directory of the current file and concatenate it with the assets folder (because main.py is inside src, the directory is src)
audio = sa.WaveObject.from_wave_file(ASSETS_PATH + "/click.wav") # Initialize a Wave Object with the click.wav path

# Function to play the audio
def play(bpm, root):

    audio_obj = audio.play() # Create an audio object variable so that we can call on it to stop the audio

    root.after(int(bpm / 60), lambda: play(int(bpm / 60), root)) # Make the root (a Tkinter window) play the sound every beat per second (bpm/60) by calling itself at that interval
    return audio_obj # Return the audio object

# Function to stop the audio
def stop(audio):
    audio.stop() # Stop the audio