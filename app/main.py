import os
import requests
from bs4 import BeautifulSoup
import settings
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

FILE_PARENT_PATH = os.path.dirname(os.path.abspath(__file__))
SAVE_IMAGE_PATH = os.path.normpath(os.path.join(FILE_PARENT_PATH, 'downloads/latest_image.png'))


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


def analyze_image():
    image = Image.open(SAVE_IMAGE_PATH)

    # 画像を配列に変換
    im_list = np.array(image)

    # データプロットライブラリに貼り付け
    plt.imshow(im_list)

    # 表示
    plt.show()

    # テキスト抽出
    txt = pytesseract.image_to_string(image)
    print(txt)


if __name__ == '__main__':
    latest_image_url = get_latest_image_url()
    print(latest_image_url)
    save_image(latest_image_url)
    analyze_image()
