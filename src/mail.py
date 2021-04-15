import base64
import os
import pickle
from pprint import pprint

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Gmail:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        self.credentials = None

        if os.path.exists('auth/token.pickle'):
            with open('auth/token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file('auth/credentials.json', self.SCOPES)
                self.credentials = self.flow.run_local_server(port=8080)

            # Save acces token
            with open('auth/token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)

    def get_emails(self):
        # Connect to Gmail API
        service = build('gmail', 'v1', credentials=self.credentials)

        # Request a list of all messages
        result = service.users().messages().list(maxResults=5, userId='me').execute()

        # Messages is a list of dicts, where each dict contains a message ID
        messages = result.get('messages')

        ret = []

        # Iterate over it
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']

                # Look for Subject and Sender Email in the headers
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = str(d['value'])
                        sender = sender.replace('\"', "").split(" ")[0]
            except:
                raise Exception("Error whilst getting messages!")

            ret.append(
                {
                    "subject": subject,
                    "sender": sender
                }
            )
        return ret


if __name__ == "__main__":
    gmail = Gmail()
    for item in gmail.get_emails():
        pprint(item)
