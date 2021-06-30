import datetime
import json
from pathlib import Path
from typing import List

from app import settings

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


def register_holiday_to_calendar(date_list: List[datetime.date]):
    credentials_path = Path(__file__).parent.parent.joinpath('credentials.json')
    credentials_obj = json.load(credentials_path.open())

    credentials = Credentials.from_service_account_info(credentials_obj, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(settings.GOOGLE_EMAIL_ADDRESS)

    service = build('calendar', 'v3', credentials=delegated_credentials)

    # TODO
