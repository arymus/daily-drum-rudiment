# Imports
import tkinter as tk # Tkinter
from PIL import Image, ImageTk # Import image modules from PIL (Python Imaging Library)
import web_scraper; import webbrowser; # Import web_scraper.py and webbrowser module
timer_label = None # Initialize timer_label as None

# Function for starting a timer with a set amount of seconds
def start_timer(seconds):
    global timer_label # Define timer_label as a global variable

    # If timer_label is None (doesn't exist)
    if timer_label == None:
        timer_label = tk.Label(win) # Create a tkinter label containing the amount of time left on the timer
        timer_label.pack() # Add the timer to the window
    # ^ If else, don't do anything

    # Function to call every second the timer runs
    def update_timer(remaining):

        print(remaining)

        # If the remaining time is greater or equal to 0
        if remaining >= 0:
            from math import ceil # Import ceil from the math module which rounds numbers up

            # If the remaining time is greater than or equal to 60, 
            # set the display message to display the remaining amount of minutes by rounding up the amount of seconds divided by 60
            if remaining >= 60: display = f"There are {ceil(remaining / 60)} minutes left."
            else: display = f"There are {remaining} seconds left." # If else (seconds are less than 60), display the amount of seconds

            timer_label.config(text = display) # Configure the timer label to contain the display message
            win.after(1000, update_timer, remaining - 1) # After 1000 millliseconds, the function calls itself and decreases remaining by 1

        # If else (the timer is 0), change the text of the label to "Time's up!"
        else: timer_label.config(text="Time's up!")

    update_timer(seconds) # Call the update_timer function with the amount of seconds passed to it

# Function to get the image as a TK PhotoImage using PIL
def open_image(filename):
    import os # Import the os module for running operating system dependent functions

    # If filename doesn't exist or it's path isn't found or it's byte size is -
    if not filename or not os.path.exists(filename) or os.path.getsize(filename) == 0:
        print("Image does not exist or is empty") # Print error message
        return None # Return none

    img = Image.open(filename) # Open the file as an image
    img = img.resize((800, 500))
    print("Image mode:", img.mode, "size:", img.size) # Print image data (mode: the colors it uses, size: the size in bytes)
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
win.configure(bg = "purple") # Give it a purple background
win.title("Daily Drum Rudiments") # Give it a title of "Daily Drum Rudiments"

# We store the result in the daily_rudiment variable to ensure it's only called once
daily_rudiment = web_scraper.get_rudiment() # Call the get_rudiment function from web_scraper.py

rudiment_label = tk.Label(win, text = daily_rudiment["name"], fg = "white") # Create labels using the rudiment name retrieved from the dictionary get_rudiment returns
rudiment_label.bind("<Button-1>", lambda _: webbrowser.open_new(daily_rudiment["url"])) # Bind an event listener to the rudiment_url that opens the URL in the browser on a left click
rudiment_label.pack() # Add the rudiment label to the window

timer_button = tk.Button(win, text = "Start timer", command = lambda: start_timer(3600)) # Create a button that calls the timer function when clicked
timer_button.pack() # Add the timer button to the window

video = web_scraper.get_video(daily_rudiment) # Call the get_video() function from web_scraper.py with the rudiment passed to it
thumbnail_file = web_scraper.get_thumbnail(video) # Call the get_thumbnail() function from web_scraper.py with the video passed to it

thumbnail_img = open_image(thumbnail_file) # Store the thumbnail inside a variable so it doesn't get garbage collected
video_label = tk.Label(win, image = thumbnail_img) # Create a label that displays the video
video_label.bind("<Button-1>", lambda _: webbrowser.open_new(video)) # Bind an event listener to the label that opens the video in the browser on left click
video_label.pack() # Add the label to the window

win.bind("<Destroy>", delete_image_data) # Bind an event listener that invokes delete_image_data with _ as the event when the window is deleted
win.mainloop() # Run the main loop so that the window appears