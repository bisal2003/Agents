from googleapiclient.discovery import build
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

# ------------- CONFIGURATION -------------
API_KEY = 'AIzaSyB6OTHSZWW9aSbnVlHpGogkM54T1sRGoQw'  # replace with your actual API key
COUNTRY = 'India'  # Can be used to change calendar ID if needed
CALENDAR_ID = 'en.indian#holiday@group.v.calendar.google.com'  # India holiday calendar
# ----------------------------------------

def get_holidays(start_date, end_date):
    service = build('calendar', 'v3', developerKey=API_KEY)

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_date.isoformat() + 'Z',
        timeMax=end_date.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print("No holidays found in the given range.")
        return

    print(f"Holidays from {start_date.date()} to {end_date.date()}:\n")
    for event in events:
        start = event['start'].get('date')
        summary = event['summary']
        print(f"{start} - {summary}")

if __name__ == '__main__':
    today = datetime.now(pytz.utc)
    start_date = today.replace(day=1) 
    end_date = start_date + relativedelta(months=1) 

   
    get_holidays(start_date, end_date)
