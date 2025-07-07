import os
import metronome_rs

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets") # Get the directory of the current file and concatenate it with the assets folder (because main.py is inside src, the directory is src)