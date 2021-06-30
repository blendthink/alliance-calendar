from pathlib import Path

from app.repository import CalendarImageRepository


def download_calendar_image(month: int, downloads_path: Path) -> Path:
    zfill_month = f"{month}".zfill(2)
    image_destination_path = downloads_path.joinpath('calendar', f'{zfill_month}', 'image.png')
    image_destination_path.parent.mkdir(parents=True, exist_ok=True)
    image_url = CalendarImageRepository.scrap_calendar_image_url(month=month)
    CalendarImageRepository.fetch_calendar_image(calendar_image_url=image_url,
                                                 image_destination_path=image_destination_path)
    return image_destination_path
