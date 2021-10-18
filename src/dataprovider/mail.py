import datetime
import json
import logging
import os
import pickle
from pprint import pprint

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO)


class Gmail:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        self.credentials = None

        secret = os.environ.get('SECRET_DATA_DIR')
        self.token_pickle = secret + '/token.pickle'
        self.credential_json = secret + '/credentials.json'
        self.repository = secret + '/repository.json'

        if os.path.exists(self.token_pickle):
            with open(self.token_pickle, 'rb') as token:
                self.credentials = pickle.load(token)
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(self.credential_json, self.SCOPES)
                self.credentials = self.flow.run_local_server(port=9090)

            with open(self.token_pickle, 'wb') as token:
                pickle.dump(self.credentials, token)

    def get_emails(self, how_many: int, by_labels: list):
        """
        Get emails
        :param how_many: how manyu you want to get.
        :param by_labels: by what labels - e.g. UNREAD
        :return: dictionary of emails
        """
        # Connect to Gmail API
        service = build('gmail', 'v1', credentials=self.credentials)

        # Request a list of all messages
        result = service.users().messages().list(maxResults=how_many, userId='me',
                                                 labelIds=by_labels).execute()

        # Messages is a list of dicts, where each dict contains a message ID
        messages = result.get('messages')

        ret = []

        # Iterate over it
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            subject = None
            sender = None

            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']

                # Look for Subject and Sender Email in the headers
                for header in headers:
                    if header['name'] == 'Subject':
                        subject = header['value']
                    if header['name'] == 'From':
                        sender = str(header['value'])
                        sender = sender.replace('\"', "").split('<')[0]
                date = datetime.datetime.fromtimestamp(int(txt['internalDate']) / 1000)
                date = date.strftime("%Y.%m.%d.")

            except:
                raise Exception("Error whilst getting messages!")

            ret.append(
                {
                    "subject": subject,
                    "sender": sender,
                    "date": date
                }
            )
        self.persist(self.repository, ret)
        return ret

    def persist(self, to_repository, what):
        if not os.path.exists(to_repository):
            f = open(to_repository, 'w')
            f.close()
        if os.stat(to_repository).st_size == 0:
            with open(to_repository, 'w', encoding='utf-8') as file:
                json.dump(what, file, ensure_ascii=False)


# TESTS
if __name__ == "__main__":
    gmail = Gmail()
    for item in gmail.get_emails(how_many=5, by_labels=['UNREAD']):
        pprint(item)
