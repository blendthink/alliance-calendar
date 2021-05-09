import os
import requests
from bs4 import BeautifulSoup
from pytesseract import Output

import settings
import pytesseract
from PIL import Image

import cv2
import numpy as np

import datetime

FILE_PARENT_PATH = os.path.dirname(os.path.abspath(__file__))
SAVE_IMAGE_PATH = os.path.normpath(os.path.join(FILE_PARENT_PATH, 'downloads/latest_image.png'))
SAVE_BLACK_IMAGE_PATH = os.path.normpath(os.path.join(FILE_PARENT_PATH, 'downloads/latest_black_image.png'))
SAVE_CSV_PATH = os.path.normpath(os.path.join(FILE_PARENT_PATH, 'downloads/image.csv'))
SAVE_CROP_IMAGE_PARENT_PATH = os.path.normpath(os.path.join(FILE_PARENT_PATH, 'crops'))

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
    return gray_img


def analyze_image():
    img = cv2.imread(SAVE_IMAGE_PATH)

    # BGR -> グレースケール
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二値化(閾値220を超えた画素を255にする。)
    ret, img_thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

    # エッジ抽出 (Canny)
    edges = cv2.Canny(img_thresh, 1, 100, apertureSize=3)
    cv2.imwrite('edges.png', edges)
    # 膨張処理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges = cv2.dilate(edges, kernel)
    # 輪郭抽出
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 面積でフィルタリング
    rects = []
    for cnt, hrchy in zip(contours, hierarchy[0]):
        if cv2.contourArea(cnt) < 3000:
            continue  # 面積が小さいものは除く
        if hrchy[3] == -1:
            continue  # ルートノードは除く
        # 輪郭を囲む長方形を計算する。
        rect = cv2.minAreaRect(cnt)
        rect_points = cv2.boxPoints(rect).astype(int)
        rects.append(rect_points)

    # x-y 順でソート
    rects = sorted(rects, key=lambda x: (x[0][1], x[0][0]))

    # 月初めが何曜日か判定する
    now_year = datetime.date.today().year
    now_month = datetime.date.today().month
    month_first_day = datetime.date(year=now_year, month=now_month, day=1)
    weekday = month_first_day.weekday()

    # index との紐付け
    month_first_day_index = 0 if weekday == 6 else weekday + 1

    # 描画する。
    for i, rect in enumerate(rects):
        color = np.random.randint(0, 255, 3).tolist()
        cv2.drawContours(img, rects, i, color, 2)
        cv2.putText(img, str(i), tuple(rect[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)

        rect0 = rect[0]
        rect2 = rect[2]

        left = rect0[0]
        bottom = rect0[1]
        right = rect2[0]
        top = rect2[1]

        cropped_image = img_thresh[bottom: top, left: right]
        cv2.imwrite(f"{SAVE_CROP_IMAGE_PARENT_PATH}/{i}.png", cropped_image)

        # テキスト抽出
        text = pytesseract.image_to_string(image=cropped_image, lang='eng+jpn', output_type=Output.STRING)

        month_day = i - (month_first_day_index - 1)
        if '休' in text and 1 <= month_day <= 31:
            print(f"休診日: {now_year}/{now_month}/{month_day}")

    cv2.imwrite('img.png', img)

if __name__ == '__main__':
    latest_image_url = get_latest_image_url()
    print(latest_image_url)
    save_image(latest_image_url)
    analyze_image()
