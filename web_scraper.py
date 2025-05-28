from bs4 import BeautifulSoup
import requests; import random

def get_rudiment():
    url = "https://www.40drumrudiments.com"
    scrape = requests.get(url)
    soup = BeautifulSoup(scrape.text, "html.parser")
    links_html = [a for a in soup.find_all("a", href = True) if not a.has_attr("class")]
    links = []

    for i in links_html:
        link = i.get("href")
        rudiment_data = {
            "name": i.string,
            "url": f"https://www.40drumrudiments.com{link}"
        }

        links.append(rudiment_data)
    
    daily_rudiment = random.choice(links)
    return daily_rudiment


# Function to scrape the link of the drum rudiment
def get_video(rudiment):
    scrape = requests.get(rudiment["url"]) # Send a GET request to the rudiment link
    soup = BeautifulSoup(scrape.text, "html.parser") # Take the data and parse it into HTML
    video_frame = soup.find("iframe") # Return an array containing the <iframe> tag in the page
    
    iframe_scrape = requests.get(video_frame.get("src"))
    iframe_soup = BeautifulSoup(iframe_scrape.text, "html.parser")
    link = iframe_soup.find("a")
    
    return link.get("href") # Return the href of the link (the website it takes you to)

def get_thumbnail(url):
    scrape = requests.get(url)
    soup = BeautifulSoup(scrape.text, "html.parser")
    thumbnail = soup.find("meta", property = "og:image")['content']
    print(f"Thumbnail URL: {thumbnail}")

    # Try to get extension from URL
    import os
    ext = os.path.splitext(thumbnail)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
        ext = '.jpg'  # Default to jpg if unknown
    filename = f"rudiment_thumbnail{ext}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    try:
        img_scrape = requests.get(thumbnail, headers=headers, allow_redirects=True)
        print(f"Image HTTP status: {img_scrape.status_code}")
        print(f"Image content length: {len(img_scrape.content)} bytes")
        print(f"Final image URL after redirects: {img_scrape.url}")
        if img_scrape.status_code == 200:
            if img_scrape.content:
                with open(filename, "wb") as file:
                    file.write(img_scrape.content)
                    print(f"Image written as {filename}!")
                return filename
            else:
                print("Image content is empty!")
        else:
            print("HTTP error! Status code: " + str(img_scrape.status_code))
    except Exception as e:
        print(f"Exception occurred while downloading image: {e}")
    return None
