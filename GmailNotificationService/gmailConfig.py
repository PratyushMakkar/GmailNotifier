from __future__ import print_function
import base64
import os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import pubsub_v1 as pubsub
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.environ.get("project_id")
subscription_id = os.environ.get("subscription_id")

subscriber = pubsub.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def CreateGoogleCredentials():
    if (os.path.exists('token.json')):
        return Credentials('token.json')

def CreateSubscriptionClient():
    return pubsub.SubscriberClient.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

def CreateSubscriptionPath():
    subscriber = CreateSubscriptionClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    return subscription_path

def CreateGmailService():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'utils/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service




