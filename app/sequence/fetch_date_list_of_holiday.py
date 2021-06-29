import datetime
import shutil
from pathlib import Path
from typing import List

import cv2
import numpy as np
import pytesseract
from pytesseract import Output


def fetch_date_list_of_holiday(month: int, image_destination_path: Path) -> List[datetime.date]:
    img = cv2.imread(f'{image_destination_path}')

    # BGR -> グレースケール
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二値化(閾値220を超えた画素を255にする。)
    ret, img_thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

    # エッジ抽出 (Canny)
    edges = cv2.Canny(img_thresh, 1, 100, apertureSize=3)

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
    month_first_day = datetime.date(year=now_year, month=month, day=1)
    weekday = month_first_day.weekday()

    # index との紐付け
    month_first_day_index = 0 if weekday == 6 else weekday + 1

    tmp_path = Path(__file__).parent.joinpath('tmp')
    tmp_path.mkdir(parents=True, exist_ok=True)

    date_list_of_holiday = list()

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
        cv2.imwrite(f"{tmp_path}/{i}.png", cropped_image)

        # テキスト抽出
        text = pytesseract.image_to_string(image=cropped_image, lang='eng+jpn', output_type=Output.STRING)

        month_day = i - (month_first_day_index - 1)
        if '休' in text and 1 <= month_day <= 31:
            date = datetime.date(year=now_year, month=month, day=month_day)
            date_list_of_holiday.append(date)

    # 一時ファイルをディレクトリごと削除
    shutil.rmtree(tmp_path)

    return date_list_of_holiday
