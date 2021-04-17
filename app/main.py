import os
import requests
from bs4 import BeautifulSoup
import settings


def get_latest_image_url():
    response = requests.get(settings.WORKPLACE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find("div", id="main").find("div", class_="calendar-box").find_all("img")
    latest_index = len(images) - 1
    return images[latest_index].get("src")


def save_image(url):
    response = requests.get(url)
    base = os.path.dirname(os.path.abspath(__file__))
    name = os.path.normpath(os.path.join(base, 'downloads/latest_image.png'))
    file = open(f"{name}", "wb")
    file.write(response.content)
    file.close()


if __name__ == '__main__':
    latest_image_url = get_latest_image_url()
    print(latest_image_url)
    save_image(latest_image_url)
