import datetime
import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import configs

class GmailAuth:
    creds = None

    def __init__(self):
        if os.path.exists(configs.GMAIL_API_TOKEN):
            self.creds = Credentials.from_authorized_user_file(configs.GMAIL_API_TOKEN, configs.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    configs.GMAIL_API_CREDENTIALS, configs.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    @property
    def service(self):
        return build('gmail', 'v1', credentials=self.creds)


class GmailMessages:
    def __init__(self,service=None):
        self.mails = []
        if service:
            self.service = service
        else:
            auth = GmailAuth()
            self.service = auth.service

    def update_mail_list(self,_from=None,_start_date=None,_end_date=None):
        _q = []
        if _from:
            _q.append(f"from:{_from}")
        if _start_date:
            _q.append(f"after:{_start_date.strftime('%Y/%m/%d')}")
        if _end_date:
            _q.append(f"before:{_end_date.strftime('%Y/%m/%d')}")

        search_query = " ".join(_q)

        _results = self.service.users().messages().list(userId='me', q=search_query).execute()
        self.mails = _results.get("messages", [])
        return self.mails

    def get_mail_details(self,id=0):
        """
        :param id: default id = 0 that means first message in mails list.
                    if id is any int value it means relevant message in the mails list (by index)
                    id is str that means message directly from gmail_id
        """
        if type(id) == int:
            try:
                gmail_id = self.mails[id]["id"]
            except:
                raise ValueError("mail list is empty. try update_mail_list method")
        else:
            gmail_id = id

        _mail = self.service.users().messages().get(userId='me', id=gmail_id).execute()

        _snippet = _mail.get("snippet", "")
        _headers = _mail.get("payload", {}).get("headers", [])
        time = None
        for h in _headers:
            if h.get("name") == "Received":
                _timestamp = re.search(configs.DATETIME_REGEX, h["value"])
                time = datetime.datetime.strptime(_timestamp[0], "%d %b %Y %H:%M:%S %z").astimezone()
                break
        _otp = re.search("\d{6}", _snippet)
        otp = _otp[0] if _otp else None

        return otp, time

    def latest(self,date_range=1):
        s_date = datetime.datetime.now().astimezone()
        e_date = s_date + datetime.timedelta(days=1)

        self.update_mail_list(_from=configs.OTP_EMAIL,_start_date=s_date,_end_date=e_date)
        if len(self.mails) > 0:
            return self.get_mail_details()
        return "No OTP", s_date







def email_list(service,_from=None,_start_date=None,_end_date=None):
    """ serach query: q='from:sampathotp@sampath.lk  after:2022/10/25 before:2022/10/26' """
    _q = []
    if _from:
        _q.append(f"from:{_from}")
    if _start_date:
        _q.append(f"after:{_start_date.strftime('%Y/%m/%d')}")
    if _end_date:
        _q.append(f"before:{_end_date.strftime('%Y/%m/%d')}")

    search_query = " ".join(_q)

    result = service.users().messages().list(userId='me',q=search_query).execute()

    return result.get("messages",[])


def get_email(service,id):
    """{'id': '1840f800d9cb5799',
    'threadId': '1840f7e22c43052c',
    'labelIds': ['CATEGORY_PERSONAL', 'INBOX'],
    'snippet': 'Dear valued customer, Please Use 893311 as the Vishwa OTP for current login session.
                This OTP is Valid till you logout. Regards, Sampath Vishwa.',
    'payload': {    'partId': '',
                    'mimeType': 'text/html',
                    'filename': '',
                    'headers': [
                    {'name': 'Delivered-To', 'value': 'pavithra.blog@gmail.com'},
                    { 'name': 'Received',
                      'value': 'by 2002:a....p4103246rbb;        Tue, 25 Oct 2022 07:16:01 -0700 (PDT)'
                                }, ...
                                """
    _mail = service.users().messages().get(userId='me', id=id).execute()

    _snippet = _mail.get("snippet","")
    _headers = _mail.get("payload", {}).get("headers",[])
    time = None
    for h in _headers:
        if h.get("name") == "Received":
            _timestamp = re.search(configs.DATETIME_REGEX, h["value"])
            time = datetime.datetime.strptime(_timestamp[0],"%d %b %Y %H:%M:%S %z").astimezone()
            break
    _otp = re.search("\d{6}", _snippet)
    otp = _otp[0] if _otp else None

    return otp, time

