from __future__ import print_function
import datetime
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'Test Randevu',
        'start': {
            'dateTime': '2026-03-22T15:00:00',
            'timeZone': 'Europe/Istanbul',
        },
        'end': {
            'dateTime': '2026-03-22T16:00:00',
            'timeZone': 'Europe/Istanbul',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    print("Randevu oluşturuldu!")
    print(event.get('htmlLink'))

if __name__ == '__main__':
    main()