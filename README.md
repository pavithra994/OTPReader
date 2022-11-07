# Bank OTP Scrapper

this is a Python package that contains handy functions for scrap OTP keys from gmail. currently only working for sampath bank otp emails.


## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bank_otp_scrapper like below. 
Rerun this command to check for and install  updates .
```bash
pip install git+https://github.com/pavithra994/OTPReader
```
## Pre-requirments
* you must have enabled the Gmail API (Check the documentation)[https://developers.google.com/gmail/api/quickstart/python]
* download the OAuth 2.0 Client credintials inside the project root as credentials.json 

## Usage
Features:
* GmailMessages  --> initiate the GmailMessage instance. 
* GmailMessages.update_mail_list    --> update the self.mails (list)
* GmailMessages.get_mail_details      --> get the OTP value and timestamp from single item in mails list.
* GmailMessages.latest  --> get the OTP value and timestamp from leatest message

#### Demo of some of the features:
```python
from bank_otp_scrapper.gmail_api import GmailMessages

mail = GmailMessages()
otp, time = mail.latest()
print(f"OTP: {otp} - time: {time}")

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
