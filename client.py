import os
import os.path
import utils

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = utils.setup_logger("status.log")


class Client:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        self.service = None
        logger.info("Logger created...")
        self.initialize_client()

    def initialize_client(self):
        """
        Initializes Gmail API client
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API Client initialized...")
        except HttpError as error:
            # TODO(developer) - Handle errors from Gmail API.
            logger.error(f"Error connecting Gmail API client! {error}")

    def print_email_bodies(self, email_ids):
        for email_id in email_ids:
            try:
                message = self.service.users().messages().get(userId='me', id=email_id, format='full').execute()
                payload = message['payload']
                body = utils.get_email_body(payload)
                print(f"Email ID: {email_id}")
                print("Email Body:")
                print(body)
                print("---")
            except HttpError as error:
                logger.error(f"Error fetching email ID: {email_id} - {error}")

    def fetch_emails(self, filter_addresses: list, search_query: ''):

        # Fetch emails for each address
        all_emails = []
        for filter_address in filter_addresses:
            query = f'from:{filter_address} {search_query}'.strip()

            results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], q=query).execute()
            emails = results.get('messages', [])
            all_emails.extend(emails)

        return all_emails