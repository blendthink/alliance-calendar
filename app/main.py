import os
import requests
from bs4 import BeautifulSoup
from pytesseract import Output

import settings
import pytesseract
from PIL import Image

FILE_PARENT_PATH = os.path.dirname(os.path.abspath(__file__))
SAVE_IMAGE_PATH = os.path.normpath(os.path.join(FILE_PARENT_PATH, 'downloads/latest_image.png'))
SAVE_BLACK_IMAGE_PATH = os.path.normpath(os.path.join(FILE_PARENT_PATH, 'downloads/latest_black_image.png'))
SAVE_CSV_PATH = os.path.normpath(os.path.join(FILE_PARENT_PATH, 'downloads/image.csv'))


def get_latest_image_url():
    response = requests.get(settings.WORKPLACE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find("div", id="main").find("div", class_="calendar-box").find_all("img")
    latest_index = len(images) - 1
    return images[latest_index].get("src")


def save_image(url):
    response = requests.get(url)
    file = open(f"{SAVE_IMAGE_PATH}", "wb")
    file.write(response.content)
    file.close()


def convert_to_black_image(img):
    gray_img = img.convert('L')
    black_img = gray_img.point(lambda x: 0 if x < 216 else 255)
    black_img.save(f"{SAVE_BLACK_IMAGE_PATH}")
    return black_img


def analyze_image():
    image = Image.open(SAVE_IMAGE_PATH)
    black_image = convert_to_black_image(image)

    # テキスト抽出
    text = pytesseract.image_to_string(image=black_image, lang='eng+jpn', output_type=Output.STRING)
    file = open(f"{SAVE_CSV_PATH}", "w")
    file.write(text)
    file.close()

    print(text)


if __name__ == '__main__':
    latest_image_url = get_latest_image_url()
    print(latest_image_url)
    save_image(latest_image_url)
    analyze_image()
