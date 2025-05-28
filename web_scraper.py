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
    thumbnail = soup.find("meta", property = "og:image")["content"]
    print(thumbnail)

    img_scrape = requests.get(thumbnail)
    if img_scrape.status_code == 200:
        with open("rudiment_thumbnail.png", "wb") as file:
            file.write(img_scrape.content)
            print("Image written!")
    else:
        file.write("")
        file.close()
        print("HTTP error! Status code: " + str(img_scrape.status_code))
