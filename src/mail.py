
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Gmail:
    # user = 'martongergely11@gmail.com'
    # passw = '148785NKFc2wns'

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        self.credentials = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                self.credentials = self.flow.run_local_server(port=8080)

            # Save acces token
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)

    def get_emails(self):
        # Connect to Gmail API
        service = build('gmail', 'v1', credentials=self.credentials)

        # Request a list of all messages





if __name__ == "__main__":
    pass