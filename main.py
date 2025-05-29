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

timer_button = tk.Button(win, text = "Start timer", command = timer) # Create a button that calls the timer function when clicked
rudiment_label.pack() # Add the rudiment label to the window

# Function to get the image as a TK PhotoImage using PIL
def open_image(filename):

    # If filename doesn't exist or it's path isn't found or it's byte size is -
    if not filename or not os.path.exists(filename) or os.path.getsize(filename) == 0:
        print("Image does not exist or is empty") # Print error message
        return None # Return none

    img = Image.open(filename) # Open the file as an image
    print("Image mode:", img.mode, "size:", img.size) # Print image data (mode: the colors it uses, size: the size in bytes)
    return ImageTk.PhotoImage(img) # Return the image as a TK PhotoImage

video = web_scraper.get_video(daily_rudiment) # Call the get_video() function from web_scraper.py with the rudiment passed to it
thumbnail_file = web_scraper.get_thumbnail(video) # Call the get_thumbnail() function from web_scraper.py with the video passed to it

thumbnail_img = open_image(thumbnail_file) # Store the thumbnail inside a variable so it doesn't get garbage collected
video_label = tk.Label(win, image = thumbnail_img) # Create a label that displays the video
video_label.bind("<Button-1>", lambda _: webbrowser.open_new(video)) # Bind an event listener to the label that opens the video in the browser on left click
video_label.pack() # Add the label to the window

timer_button.pack() # Add the timer button to the window

# Function to delete image data with an event passed to it
def delete_image_data(event):

    # If the selected widget is window and thumbnail_file exists
    if event.widget == win and thumbnail_file:

        # Open thumbnail_file and write binary to it with an alias of file
        with open(thumbnail_file, "wb") as file:
            file.seek(0) # Move to the start of the file by moving the cursor to 0, aka the start
            file.truncate() # Delete all data from the current position to the end
            print("File emptied successfully!") # Print a success message

win.bind("<Destroy>", delete_image_data) # Bind an event listener that invokes delete_image_data with _ as the event when the window is deleted
win.mainloop() # Run the main loop so that the window appears