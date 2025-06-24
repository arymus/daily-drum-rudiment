# Imports
import tkinter as tk # Tkinter
from PIL import Image, ImageTk # Import image modules from PIL (Python Imaging Library)
from tkdial import Dial # Import the Dial from tkdial
import web_scraper; import metronome; import timer_functions # Import web_scraper.py and metronome.py
import webbrowser # Import webbrowser to interact with the user's browser

# Function to get the image as a TK PhotoImage using PIL
def open_image(filename):
    import os # Import the os module for running operating system dependent functions

    # If filename doesn't exist or it's path isn't found or it's byte size is -
    if not filename or not os.path.exists(filename) or os.path.getsize(filename) == 0:
        print("Image does not exist or is empty") # Print error message
        return None # Return none

    img = Image.open(filename) # Open the file as an image
    img = img.resize((800, 500)) # Resize the image to be 800x500
    return ImageTk.PhotoImage(img) # Return the image as a TK PhotoImage

# Function to delete image data with an event passed to it
def delete_image_data(event):

    # If the selected widget is window and thumbnail_file exists
    if event.widget == win and thumbnail_file:

        # Open thumbnail_file and write binary to it with an alias of file
        with open(thumbnail_file, "wb") as file:
            file.seek(0) # Move to the start of the file by moving the cursor to 0, aka the start
            file.truncate() # Delete all data from the current position to the end
            print("File emptied successfully!") # Print a success message

        global timer_label # Define timer_label as a global variable
        timer_label = None # Set timer_label back to None

win = tk.Tk() # Create a window
win.geometry("1000x1000") # Make the window 1000 x 1000 px
win.configure(bg = "#8b0909") # Give it a purple background
win.title("Daily Drum Rudiments") # Give it a title of "Daily Drum Rudiments"

# We store the result in the daily_rudiment variable to ensure it's only called once
daily_rudiment = web_scraper.get_rudiment() # Call the get_rudiment function from web_scraper.py
print(daily_rudiment["name"])

rudiment_label = tk.Label(win, text = daily_rudiment["name"], font = ("Arial", 20, "bold"), fg = "#806350") # Create labels using the rudiment name retrieved from the dictionary get_rudiment returns and display them using the Impact font in bold, size 20px
rudiment_label.bind("<Button-1>", lambda _: webbrowser.open_new(daily_rudiment["url"])) # Bind an event listener to the rudiment_url that opens the URL in the browser on a left click
rudiment_label.pack(padx = 20, pady = 20, ipadx = 10, ipady = 10) # Add the rudiment label to the window with internal and external padding (10px and 20px respectively)

video = web_scraper.get_video(daily_rudiment) # Call the get_video() function from web_scraper.py with the rudiment passed to it
thumbnail_file = web_scraper.get_thumbnail(video) # Call the get_thumbnail() function from web_scraper.py with the video passed to it

thumbnail_img = open_image(thumbnail_file) # Store the thumbnail inside a variable so it doesn't get garbage collected
video_label = tk.Label(win, image = thumbnail_img) # Create a label that displays the video
video_label.bind("<Button-1>", lambda _: webbrowser.open_new(video)) # Bind an event listener to the label that opens the video in the browser on left click
video_label.pack() # Add the label to the window

timer_button = tk.Button(win, text = "Start timer", command = lambda: timer_functions.start_timer(30, win, timer_button), bg = "#806350", fg = "#EDD9CC", font = ("Arial", 15, "bold")) # Create a button that calls the timer function from timer_functions.py when clicked with colors and fonts applied
timer_button.pack(padx = 10, pady = 10, ipadx = 10, ipady = 10) # Add the timer button to the window with internal and external padding

win.bind("<Destroy>", delete_image_data) # Bind an event listener that invokes delete_image_data with _ as the event when the window is deleted
win.mainloop() # Run the main loop so that the window appears