import os
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

datapath = "/home/tylerl126/geegee/CSVFiles"

for name in os.listdir(datapath):
    if name != ".gitkeep":
        with open(os.path.join(datapath, name)) as file:
            text = file.read().replace("```","").replace("python","")
            base_name, _ = os.path.splitext(name)  # Extract base name without .txt extension
            completePath = os.path.join(datapath,base_name+'.csv')
            file = open(completePath,'w')
            file.write(text.strip())
            file.close()


SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('/home/tylerl126/geegee/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, summary, start_datetime, end_datetime):
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'America/New_York',  
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'America/New_York',  
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    datapath = "/home/tylerl126/geegee/CSVFiles"
    service = get_calendar_service()
    for filename in os.listdir(datapath):
        if filename != ".gitkeep":
            filepath = os.path.join(datapath, filename)
            df = pd.read_csv(filepath)

            for index, row in df.iterrows():
                summary = row['Summary']
                start_date = row['Start Date']
                start_time = row['Start Time']
                end_date = row['End Date']
                end_time = row['End Time']

                start_datetime_str = f"{start_date}T{start_time}"
                end_datetime_str = f"{end_date}T{end_time}"

                start_datetime = pd.to_datetime(start_datetime_str)
                end_datetime = pd.to_datetime(end_datetime_str)

                create_event(service, summary, start_datetime, end_datetime)