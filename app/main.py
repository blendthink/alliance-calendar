from pathlib import Path

from sequence import download_calendar_image
from sequence import extract_date_list_of_holiday
from sequence import register_holiday_to_calendar

FILE_PARENT_PATH = Path(__file__).parent
DOWNLOADS_PATH = FILE_PARENT_PATH.joinpath('downloads')

if __name__ == '__main__':
    month = 7
    image_destination_path = download_calendar_image(month=month, downloads_path=DOWNLOADS_PATH)
    date_list = extract_date_list_of_holiday(month=month, image_destination_path=image_destination_path)
    register_holiday_to_calendar(date_list=date_list)
