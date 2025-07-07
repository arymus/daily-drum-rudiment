import os
import metronome_rs

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets") # Get the directory of the current file and concatenate it with the assets folder (because main.py is inside src, the directory is src)

def play(bpm, root):
    event_id = root.after(bpm / 60, lambda: metronome_rs.py_start_simple_metronome(120.0))
    return event_id

def stop(event_id, root):
    root.after_cancel(event_id)
    metronome_rs.py_stop_global_metronome()