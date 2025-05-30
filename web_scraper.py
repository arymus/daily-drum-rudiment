# Imports
from bs4 import BeautifulSoup # BeautifulSoup for performing web scrapes
import requests; import random # Requests for sending HTTP requests and random for generating random items from a list

# Function to scrape data at a certain URL and parse it into HTML
def scrape_soup(url):
    # HTTP headers to send along with the requests we make
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'} # User agent which contains data about my laptop to ensure the correect content is served in the response

    # Send a GET request to the URL
    # Send the headers from before as the request header
    scrape = requests.get(url, headers = headers)

    # Take the stext returned by the scrape (aka the HTML content but as plaintext)
    # Pass the plaintext through the HTML parser to be returned as HTML
    soup = BeautifulSoup(scrape.text, "html.parser")

    return soup # Return the data as HTML

# Function to get a random rudiment
def get_rudiment():
    content = scrape_soup("https://www.40drumrudiments.com") # Get the HTML content from https://www.40drumrudiments.com

    # links_html is a list that iterates through every <a> tag with an href attribute as a and filters out the ones that do not have a class attribute
    links_html = [a for a in content.find_all("a", href = True) if not a.has_attr("class")]
    rudiments = [] # An empty list for storing the rudiments

    links_html.pop(0) # Remoe the first item from the list because the first item is a link to the home page, which causes an error if it's selected as the rudiment
    # For each link in links_html, where an individual link is i
    for i in links_html:

        # Create a rudiment_data dictionary to hold data
        rudiment_data = {
            "name": i.string, # Get the text content from the <a> tag and set it as the name of the rudiment
            "url": f"https://www.40drumrudiments.com{i.get('href')}" # Concatenate the href attribute with the homepage as the URL because the link returns as a subdirectory of the homepage
        }

        rudiments.append(rudiment_data) # Add the rudiment data to the list of raw links

    return random.choice(rudiments) # Return a randomly rudiment from the list

# Function to get the youtube tutorial on how to play the rudiment
def get_video(rudiment):
    content = scrape_soup(rudiment["url"]) # Get the HTML content from the rudiment's URL
    video_frame = content.find("iframe") # Return the <iframe> tag in the page, which holds the youtube tutorial video

    # Try to get the src attribute from the video frame but if there's an AttributeError print an error message
    try: iframe_content = scrape_soup(video_frame.get("src")) # Get the HTML content from the link in the src attribute of the <iframe> tag
    except AttributeError: print(rudiment["name"] + "returned None :(") # Print the rudiment's name in an error message on AttributeError

    link = iframe_content.find("a") # Retrieve the first <a> tag from the HTML
    return link.get("href") # Return the href of the <a> tag (the website it takes you to)


# Function to get the thumbnail from a URL and write it to an image
def get_thumbnail(url):
    content = scrape_soup(url) # Get the HTML content of the URL passed to the function
    thumbnail = content.find("meta", property = "og:image")['content']
    print(f"Thumbnail URL: {thumbnail}") # Print the URL

    # Try to get extension from URL
    import os # Import os for handling OS functions with Python

    # os.path.splittext splits the file name of the thumbnail from its extension and puts them into an array
    # [1] gets the second item from the split array, which would be the file extension
    # .lower() makes the extension lowercase
    ext = os.path.splitext(thumbnail)[1].lower()

    # If the extension isn't jpg, jpeg, png, gif, bmp, or webp
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
        ext = '.jpg'  # Default to jpg

    filename = f"rudiment_thumbnail{ext}" # Set filename to be rudiment_thumbnail with the extension that's found

    # Try to run this code block and catch errors
    try:

        # Send a GET request to the thumbnail's URL
        # Send the user agent in the header, which contains information about my laptop to ensure the correct content is served in the response
        img_scrape = requests.get(thumbnail, headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})

        # Print data about the image to the console
        print(f"Image HTTP status: {img_scrape.status_code}") # HTTP status code
        print(f"Final image URL after redirects: {img_scrape.url}") # Image URL

        # If the status code is 200 (OK)
        if img_scrape.status_code == 200:

            # If the scrape contains content
            if img_scrape.content:

                # Open the file in write-binary mode, represented as file
                with open(filename, "wb") as file:
                    file.write(img_scrape.content) # Write the image's binary data to the file
                    print(f"Image written as {filename}!") # Print a success messagej

                return filename # Return the file

            # If else (image scrape is empty)
            else:
                print("Image content is empty!") # Print warning

        # If else (status code isn't 200, aka an ERROR)
        else:
            print("HTTP error! Status code: " + str(img_scrape.status_code)) # Print HTTP error

    # Catch any errors, defined as e
    except Exception as e:
        print(f"Exception occurred while downloading image: {e}") # Print the error

    return None # Return none
