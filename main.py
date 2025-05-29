# Imports
import tkinter as tk # Tkinter
from PIL import Image, ImageTk # Import image modules from PIL (Python Imaging Library)
import os


# web_scraper.py, webbrowser module, time module
import web_scraper; import webbrowser; import time

# Function for starting a timer
def timer():
    pass

win = tk.Tk() # Create a window
win.geometry("1000x1000") # Make the window 1000 x 1000 px
win.configure(bg = "purple") # Give it a purple background
win.title("Daily Drum Rudiments") # Give it a title of "Daily Drum Rudiments"

# We store the result in the daily_rudiment variable to ensure it's only called once
daily_rudiment = web_scraper.get_rudiment() # Call the get_rudiment function from web_scraper.py

# Create labels using the dictionary named retrieved from get_rudiment (the function returns a dictionary)
rudiment_label = tk.Label(win, text = daily_rudiment["name"], fg = "white")

# Bind an event listener to the rudiment_url that calls the lambda function to open the url on a left click
rudiment_label.bind("<Button-1>", lambda _: webbrowser.open_new(daily_rudiment["url"]))

timer = tk.Button(win, text = "Start timer", command = timer) # Create a button that calls the timer function when clicked
rudiment_label.pack() # Add the rudiment label to the window

def open_image(filename):
    if not filename or not os.path.exists(filename) or os.path.getsize(filename) == 0:
        print("Image does not exist or is empty")
        return None

    img = Image.open(filename)
    print("Image mode:", img.mode, "size:", img.size)
    return ImageTk.PhotoImage(img)

video = web_scraper.get_video(daily_rudiment) # Call the get_video() function from web_scraper.py with the rudiment passed to it
thumbnail_file = web_scraper.get_thumbnail(video)

# Store the PhotoImage object to prevent garbage collection
thumbnail_img = open_image(thumbnail_file)
video_label = tk.Label(win, image=thumbnail_img)
video_label.bind("<Button-1>", lambda _: webbrowser.open_new(video))
video_label.pack() # Add the link label to the window

timer.pack()

def delete_image_data(event):
    if event.widget == win and thumbnail_file:
        with open(thumbnail_file, "wb") as file:
            file.seek(0)
            file.truncate()
            print("File emptied successfully!")

win.bind("<Destroy>", delete_image_data)
win.mainloop()