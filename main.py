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

def open_image():
    if not os.path.exists("rudiment_thumbnail.png") or os.path.getsize("rudiment_thumbnail.png") == 0:
        print("Image does not exist or is empty")
        return None

    img = Image.open("rudiment_thumbnail.png")
    print("Image mode:", img.mode, "size:", img.size)
    return ImageTk.PhotoImage(img)

video = web_scraper.get_video(daily_rudiment) # Call the get_video() function from web_scraper.py with the rudiment passed to it
thumbnail = web_scraper.get_thumbnail(video) # Call the get_thumbnail() function from web_scraper.py with the video URL passed to it

video_label = tk.Label(win, image = open_image()) # Create a label that has the the thumbnail of the video
video_label.bind("<Button-1>", lambda _: webbrowser.open_new(video)) # Bind an event listener to to open the url in the lambda function on a left click
video_label.pack() # Add the link label to the window

timer.pack()

def delete_image_data(event):
    if event.widget == win:
        with open("rudiment_thumbnail.png", "wb") as file:
            file.seek(0)
            file.truncate()
            print("File emptied successfully!")

win.bind("<Destroy>", delete_image_data)
win.mainloop()