import datetime
import json
from pathlib import Path
from typing import List

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from app import settings

SCOPES = ['https://www.googleapis.com/auth/calendar']


def register_holiday_to_calendar(date_list: List[datetime.date]):
    credentials_path = Path(__file__).parent.parent.joinpath('credentials.json')
    credentials_obj = json.load(credentials_path.open())

    credentials = Credentials.from_service_account_info(credentials_obj, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(settings.GOOGLE_EMAIL_ADDRESS)

    service = build('calendar', 'v3', credentials=delegated_credentials)

    for date in date_list:
        date_text = date.strftime("%Y-%m-%d")
        end_date = date + datetime.timedelta(days=1)
        end_date_text = end_date.strftime("%Y-%m-%d")
        body = {
            "summary": f"{settings.CALENDAR_SUMMARY}",
            "start": {
                "date": f"{date_text}",
                "timeZone": "Asia/Tokyo",
            },
            "end": {
                "date": f"{end_date_text}",
                "timeZone": "Asia/Tokyo",
            },
        }
        event = service.events().insert(calendarId='primary', body=body).execute()
        print('Event created: %s' % (event.get('htmlLink')))
