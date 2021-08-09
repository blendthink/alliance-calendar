from pathlib import Path

from app.repository import CalendarImageRepository


def download_calendar_image(month: int, image_destination_path: Path):
    image_url = CalendarImageRepository.scrap_calendar_image_url(month=month)
    CalendarImageRepository.fetch_calendar_image(calendar_image_url=image_url,
                                                 image_destination_path=image_destination_path)
