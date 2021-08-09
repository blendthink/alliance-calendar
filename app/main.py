from pathlib import Path

from sequence import receive_argument_month
from sequence import build_image_destination_path
from sequence import download_calendar_image
from sequence import extract_date_list_of_holiday
from sequence import register_holiday_to_calendar

FILE_PARENT_PATH = Path(__file__).parent
DOWNLOADS_PATH = FILE_PARENT_PATH.joinpath('downloads')

if __name__ == '__main__':
    month = receive_argument_month()
    image_destination_path = build_image_destination_path(month=month, downloads_path=DOWNLOADS_PATH)
    download_calendar_image(month=month, image_destination_path=image_destination_path)
    date_list = extract_date_list_of_holiday(month=month, image_destination_path=image_destination_path)
    register_holiday_to_calendar(date_list=date_list)
