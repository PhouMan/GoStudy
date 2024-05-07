import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import webbrowser    
from datetime import datetime

urL='https://www.google.com'
chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab(urL)


datapath = "csvfiles"
idcalendar = secret_email
SCOPES = ['https://www.googleapis.com/auth/calendar']


def isolate_data(data_string):

  try:
    _, data_portion = data_string.split('=', 1)
    return data_portion.strip()
  except ValueError:
    return None



def validDate(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False



def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
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
    for name in os.listdir(datapath):
        if name != ".gitkeep":
            with open(os.path.join(datapath, name)) as file:
                text = file.read().replace("```","").replace("python","")
                base_name, _ = os.path.splitext(name)  # Extract base name without .txt extension
                completePath = os.path.join(datapath,base_name+'.csv')
                file = open(completePath,'w')
                file.write(text.strip())
                file.close()

                with open(f'csvfiles/{base_name}.csv','r') as file:
                    fileread = file.read()
                    data = json.loads(isolate_data(fileread))       

                    count = 0
                    for i in data["Assignment"]:
                        try:
                            if validDate(data["Date"][count]) == False:
                                count +=1
                            else:
                                addEvent(creds,i,data["Date"][count],data["Date"][count])
                                count +=1
                        except IndexError:
                            pass


def addEvent(creds,name, startdate,enddate):
   

    event = {
    'summary': name,
    'start': {
        'date': startdate,
        },
    'end': {
        'date': enddate,
        },
    }

    service = build('calendar', 'v3', credentials=creds,client_options={"quota_project_id": "hackathon-422304"})
    event = service.events().insert(calendarId=idcalendar, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



if __name__ == '__main__':
    main()


