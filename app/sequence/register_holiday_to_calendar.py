import datetime
from typing import List

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


def register_holiday_to_calendar(credentials_obj: object, email_address: str, date_list: List[datetime.date]):
    credentials = Credentials.from_service_account_info(credentials_obj, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(email_address)

    service = build('calendar', 'v3', credentials=delegated_credentials)

    # TODO
