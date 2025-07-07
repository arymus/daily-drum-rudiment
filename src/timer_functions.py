import tkinter as tk # Tkinter
import metronome # Import metronome.py

timer_label = None # Initialize timer_label as None
pause_button = None # Initialize pause_button as None

# Function to pause the timer
def pause(button, time, timer, remaining, root, timer_button, event_id):
    root.after_cancel(timer) # Stop the timer
    if remaining >= 60: time.config(text = f"{remaining // 60}:{(remaining % 60):02d}") # If the remaining time is a minute or above, display the time in minutes:seconds
    else: time.config(text = f"There are {remaining} seconds left.") # If the remaining seconds are less than a minute, display only the seconds

    button.config(text = "Play", command = lambda: start_timer(remaining, root, timer_button)) # Change the text and function of the button
    metronome.stop(event_id, root) # Stop the metronome with the necessary data

# Function for starting a timer with a set amount of seconds
def start_timer(seconds, root, timer_button):
    global timer_label # Define timer_label as a global variable
    global pause_button # Define pause_button as a global variable

    timer_button.config(command = None, state = "disabled") # Set the button to be disabled so it can't be clicked again
    event_id = metronome.play(120, root) # Activate the metronome at 120bpm

    # If timer_label is None (doesn't exist)
    if timer_label == None:
        timer_label = tk.Label(root, bg = "#EDD9CC", fg = "#B20808", font = ("Arial", 15, "bold")) # Create a tkinter label containing the amount of time left on the timer
        timer_label.pack(ipadx = 10, ipady = 10, padx = 10, pady = 10) # Add the timer to the window

    # If the pause button is still None
    if pause_button == None:
        pause_button = tk.Button(root, text = "Pause", bg = "#B20808", fg = "#EDD9CC") # Create button
        pause_button.pack(ipadx = 10, ipady = 10, padx = 10, pady = 10) # Add the button to the window

    # If else, because when we call the function again on button click in pause(), the pause_button isn't None and therefore keeps the text of "Pause"
    else:
        pause_button.config(text = "Pause") # Edit the pause button to say pause

    # Function to call every second the timer runs
    def update_timer(remaining):

        # The win.after() is assigned to the variable so that we can cancel it when the timer ends using it
        timer = root.after(1000, update_timer, remaining - 1) # After 1000 millliseconds, the function calls itself and decreases remaining by 1
        pause_button.config(command = lambda: pause(pause_button, timer_label, timer, remaining, root, timer_button)) # Add the function to pause the timer onto the button as a command

        # If the remaining time is greater or equal to 0
        if remaining >= 0:

            # If the remaining time is greater than or equal to 60, 
            # set the display message to display the remaining amount of minutes and seconds
            if remaining >= 60: display = f"{remaining // 60}:{(remaining % 60):02d}"
            else: display = f"There are {remaining} seconds left." # If else (seconds are less than 60), display the amount of seconds
            timer_label.config(text = display) # Configure the timer label to contain the display message

        # If else (the timer is 0), change the text of the label to "Time's up!"
        else:
            timer_label.config(text = "Time's up!") # Change the text of the timer label

            # Function to erase the timer-associated labels
            def erase_label(id):
                metronome.stop(event_id, root) # Stop the metronome with the necessary data
                global timer_label # Define timer_label as a global variable
                global pause_button # Define pause_button as a global variable
                
                root.after_cancel(id) # Cancel the after event running in the window

                # Remove the tkinter objects from the window and set them to None so that we can reenable them should the timer be restarted
                timer_label.destroy()
                pause_button.destroy()
                timer_label = None
                pause_button = None

            timed_event = root.after(1500, lambda: erase_label(timed_event)) # Create a win.after() event that erases the label after 1.5 seconds
            root.after_cancel(timer) # Cancel the countdown timer
            timer_button.config(command = lambda: start_timer(seconds, root, timer_button), state = "normal") # Add the timer command back to the timer button and reenable it

    update_timer(seconds) # Call the update_timer function with the amount of seconds passed to it