from pathlib import Path

from sequence import extract_date_list_of_holiday
from sequence import download_calendar_image

FILE_PARENT_PATH = Path(__file__).parent
DOWNLOADS_PATH = FILE_PARENT_PATH.joinpath('downloads')

if __name__ == '__main__':
    month = 7
    image_destination_path = download_calendar_image(month=month, downloads_path=DOWNLOADS_PATH)
    date_list = extract_date_list_of_holiday(month=month, image_destination_path=image_destination_path)
    print(date_list)
