from array import array
from multiprocessing.dummy import Array
import re
import traceback
from urllib import response
from pyparsing import Optional
import requests
from GmailNotificationService.gmailConfig import CreateGmailService
import os
from google.api_core import retry
from google.cloud import pubsub_v1 as pubsub
from dotenv import load_dotenv
import json
from GmailNotificationService.gmailConfig import CreateSubscriptionClient, CreateSubscriptionPath
from GmailNotificationService.model import GmailModel


load_dotenv()

service = CreateGmailService()
TOPIC_NAME = os.environ.get("TOPIC_NAME")

subscriber = CreateSubscriptionClient()
subscription_path = CreateSubscriptionPath()
NUM_MESSAGES = 3

global_history_id = None 

def SubscribeToUserInbox():
    json = {
        "labelIds": ["UNREAD"],
        "labelFilterAction": "include",
        "topicName": TOPIC_NAME 
    }
    try: 
        response_object = service.users().watch(userId = "me", body=json).execute()
    except Exception as err: 
        print("Error occured: {0}".format(err))
        return {"message": "Error ocuured"}

    try: 
        history_id = response_object['historyId']
        global global_history_id 
        global_history_id = history_id
        print("global_history_id is {0}".format(history_id))

    except KeyError as err:
        print(traceback.print_exception(err))
        print("An Error Occured. Count not find the key 'historyId' in the response form user.watch ")

    return response_object

def UnsubscribeToUserInbox():
    try: 
        print(service.users().stop(userId = "me").execute())
    except Exception as err: 
        print("Error occured: {0}".format(err))
        return {"message": "Error ocuured"}

def PollMessages():
    with subscriber:
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
            retry=retry.Retry(deadline=300),
        )
        if len(response.received_messages) == 0:
            return

        return response

@DeprecationWarning
def _ExtractLatestHistory(response):
    try:
        recieved_messages = response.received_messages
        messages = len(recieved_messages)
        recieved_message = recieved_messages[messages-1]
        data = recieved_message.message.data
        data_json = json.loads(data)
        historyId = data_json['historyId']
        return str(historyId)
    except:
        return ""

def _UpdateLatesHistory(response):
    try:
        global global_history_id
        global_history_id = response['historyId']
    except KeyError as e:
        traceback.print_exception(e)
        print("Key Error: Could not find the resource 'historyId' in the response to user.history.list ")

def ListChanges(startHistoryId: str, userId: str = "me"):
    try:
        response = service.users().history().list(userId = userId,  startHistoryId = startHistoryId).execute()
        return response
    except Exception as err:
        print("Error occured: {0}".format(err))
        return {"message": "Error ocuured"}

def _ExtractMessageId(response) -> array:
    message_ids = []
    try: 
        print(response)
        response_array = response['history']
        for item in response_array:
            messages_added = item['messages']
            for message in messages_added: 
                message_data = message
                message_ids.append(message_data['id'])
        return message_ids
    except Exception as err:
        print("Error Occured: {0}".format(err))
        print(traceback.print_exception(err))
        return []

def GetMessages(messageIds: array) -> array:
    messages = []

    for id in messageIds:
        try:
            response_object = service.users().messages().get(userId='me', id=id, format ='full').execute()
            messages.append(response_object)
        except:
            pass
    return messages

def ModelFromMessageJSON(json) -> GmailModel:
    gmail = GmailModel()
    try: 
        headers = json['payload']['headers']
        _subject = [i['value'] for i in headers if i['name']=="Subject"][0]
        _sender = [i['value'] for i in headers if i['name']=="From"][0]
        _snippet = json['snippet']
        
        if ((type(_snippet) == str) & (type(_subject) == str) & (type(_sender) == str)):
            gmail.snippet= _snippet
            gmail.subject = _subject        
            gmail.sender = _sender
            return gmail
        else: 
            raise TypeError

    except KeyError as e:
        print(traceback.print_exception(e))
        return None
    except TypeError as e:
        print(traceback.print_exception(e))
        return None

def AcknowledgeMessages(response):
    ack_ids = []
    try:
        for received_message in response.received_messages:
            print(f"Received: {received_message.message.data}.")
            ack_ids.append(received_message.ack_id)

        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )
    except Exception as e:
        pass

def ReturnMessagesAsGmailModels() -> array:

    if (global_history_id is None):
        SubscribeToUserInbox()
        print(global_history_id)

    messages_array = []
    try: 
        recentChanges = ListChanges(global_history_id)
        _UpdateLatesHistory(recentChanges)
        messages = _ExtractMessageId(recentChanges)

        for item in GetMessages(messages):
            gmail = ModelFromMessageJSON(item)
            messages_array.append(gmail)

        return messages_array

    except Exception as e:
        return []

def AcknowledgeAllMessages():
    with subscriber:   
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": 1000000},
            retry=retry.Retry(deadline=300),
        )
        if len(response.received_messages) == 0:
            return

        ack_ids = []
        try:
            for received_message in response.received_messages:
                print(f"Received: {received_message.message.data}.")
                ack_ids.append(received_message.ack_id)

            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )
        except Exception as e:
            pass

#AcknowledgeAllMessages()

'''
response = PollMessages() 
print(response)
data = _ExtractLatestHistory(response)
json_data = ListChanges(data)
print(json.dumps(ListChanges(data), indent=2)+ "Here")
messages = _ExtractMessageId(json_data)
print(messages)
json = GetMessages(messages)
print(json)
for item in json:
    print(ModelFromMessageJSON(item))
'''
