import json
from pathlib import Path

from settings import GOOGLE_EMAIL_ADDRESS

from sequence import extract_date_list_of_holiday
from sequence import download_calendar_image
from sequence import register_holiday_to_calendar

FILE_PARENT_PATH = Path(__file__).parent
DOWNLOADS_PATH = FILE_PARENT_PATH.joinpath('downloads')
CREDENTIALS_PATH = FILE_PARENT_PATH.joinpath('credentials.json')

if __name__ == '__main__':
    month = 7
    image_destination_path = download_calendar_image(month=month, downloads_path=DOWNLOADS_PATH)
    date_list = extract_date_list_of_holiday(month=month, image_destination_path=image_destination_path)
    credentials_obj = json.load(CREDENTIALS_PATH.open())
    register_holiday_to_calendar(credentials_obj=credentials_obj, email_address=GOOGLE_EMAIL_ADDRESS ,date_list=date_list)
