import base64
import os
import pickle

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

                # The Body of the message is in Encrypted format. So, we have to decode it.
                # Get the data and decode it with base 64 decoder.
                # pprint(payload.get('parts'))
                body = payload.get('body')
                data = str(body.get('data'))
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = base64.b64decode(data)

                # Printing the subject, sender's email and message
                print("Subject: ", subject)
                print("From: ", sender)
                print('\n')

            except:
                raise Exception("Error whilst getting messages!")


if __name__ == "__main__":
    gmail = Gmail()
    gmail.get_emails()