import datetime
import os
import pickle
from pprint import pprint

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.data.enums import Constants
from src.data.repository import Repository


class Gmail:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        self.credentials = None

        secret = os.environ.get('SECRET_DATA_DIR')
        self.token_pickle = secret + '/token.pickle'
        self.credential_json = secret + '/credentials.json'
        self.repository = Constants.CACHE_PATH.value + '/repository.json'

        if os.path.exists(self.token_pickle):
            with open(self.token_pickle, 'rb') as token:
                self.credentials = pickle.load(token)
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                try:
                    self.credentials.refresh(Request())
                except Exception:
                    os.remove(os.environ.get('SECRET_DATA_DIR') + '/token.pickle')
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(self.credential_json, self.SCOPES)
                self.credentials = self.flow.run_local_server(port=9090)

            with open(self.token_pickle, 'wb') as token:
                pickle.dump(self.credentials, token)

    def get_emails_by_labels(self, how_many: int, by_labels: list):
        """
        Get emails
        :param how_many: how many you want to get.
        :param by_labels: by what labels - e.g. UNREAD
        :return: dictionary of emails
        """
        service = build('gmail', 'v1', credentials=self.credentials)
        result = service.users().messages().list(maxResults=how_many, userId='me',
                                                 labelIds=by_labels).execute()
        messages = result.get('messages')
        ret = []
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            subject = None
            sender = None
            try:
                payload = txt['payload']
                headers = payload['headers']
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

        repo = Repository()
        repo.persist_dict(self.repository, ret)
        return ret


# TESTS
if __name__ == "__main__":
    gmail = Gmail()
    for item in gmail.get_emails_by_labels(how_many=5, by_labels=['UNREAD']):
        pprint(item)
