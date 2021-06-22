from __future__ import print_function
import os.path
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
CLIENT_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'V1'
SCOPES = ['https://mail.google.com/']
Gdic = {'person': "ROOT", 'title': "관리자"}


def quick():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    logging.warning("main start")
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

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    userInfo = service.users().getProfile(userId='me').execute()
    print(userInfo)

    results = service.users().messages().list(
        userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    print(results)

    if not messages:
        print("No messages found.")
    else:
        print("Message snippets:")
        for message in messages:
            msg = service.users().messages().get(
                userId='me', id=message['id']).execute()
            print(msg['snippet'])
            Gdic['title'] += msg['snippet']
            email_data = msg['payload']['headers']
            for values in email_data:
                name = values["name"]
                if name == "From":
                    from_name = values["value"]
                    Gdic['person'] += from_name
                    print(from_name)
           # print (msg['snippet'])
            print("############################\n")
    return Gdic

   # os.remove("token.json")


if __name__ == '__main__':
    quick()
