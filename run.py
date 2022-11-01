from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from configs import OTP_EMAIL
from gmail_api import GmailAuth, email_list, get_email, GmailMessages


# If modifying these scopes, delete the file token.json.

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    s_date = datetime.datetime(year=2022,month=11,day=1)
    e_date = s_date + datetime.timedelta(days=1)
    # auth = GmailAuth()

    mail = GmailMessages()
    mail.update_mail_list(_from=OTP_EMAIL,_start_date=s_date,_end_date=e_date)
    otp, time = mail.get_mail_details()

    print(f"OTP: {otp} - time: {time}")


if __name__ == '__main__':
    main()