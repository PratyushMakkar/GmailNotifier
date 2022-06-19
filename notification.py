import traceback
from pynotifier import Notification
from GmailNotificationService.gmail import ReturnMessagesAsGmailModels
from GmailNotificationService.model import GmailModel

def CreateNewGmailNotification(subject: str, sender: str, content: str):
    return Notification(
	    title= subject+ ' BY ' + sender,
	    description=content,
	    icon_path='utils/gmail.png', # On Windows .ico is required, on Linux - .png
	    duration=10,                                   # Duration in seconds
	    urgency='critical'
    ).send()

def InitiatePushNotification():
	messages_array = ReturnMessagesAsGmailModels()
	print(messages_array)
	for message in messages_array:
		if isinstance(message, GmailModel):
			try:
				CreateNewGmailNotification(message.subject , message.sender, message.snippet)
			except Exception as err:
				print(traceback.print_exception(err))
		else:
			pass
