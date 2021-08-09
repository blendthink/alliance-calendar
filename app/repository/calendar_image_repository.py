import re

import requests
from bs4 import BeautifulSoup
from urllib3.util.url import parse_url
from pathlib import Path

from app import settings
from app.data.calendar_image_url import CalendarImageUrl


class CalendarImageRepository:

    @staticmethod
    def scrap_calendar_image_url(month: int) -> CalendarImageUrl:
        if month not in range(1, 12):
            raise ValueError('1 ~ 12')

        response = requests.get(settings.WORKPLACE_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # calendar img tags
        img_tags = soup.find("div", id="main").find("div", class_="calendar-box").find_all("img")

        for img_tag in img_tags:
            image_url = img_tag.get("src")

            # image url is 01.png ~ 12.png
            zfill_month = f"{month}".zfill(2)
            re_genre = r'{}.png$'.format(zfill_month)
            regex_pattern = re.compile(re_genre)
            result = re.search(regex_pattern, image_url)
            if bool(result):
                url = parse_url(image_url)
                return CalendarImageUrl(url)

        raise FileNotFoundError

    @staticmethod
    def get_calendar_image(calendar_image_url: CalendarImageUrl) -> bytes:
        url = calendar_image_url.url
        response = requests.get(url)
        return response.content

    @staticmethod
    def save_calendar_image(image: bytes, image_destination_path: Path):
        file = image_destination_path.open(mode="wb")
        file.write(image)
        file.close()
