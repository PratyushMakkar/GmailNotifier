# :envelope_with_arrow: Gmail Notifier 

**Gmail Notifier** is a python application script that monitors your Gmail Inbox using the Gmail API for any new emails. The user recieves a desktop notification each time there is a new email sent. 

## :pushpin: Set up 
1. Use the <kbd>Use this template</kbd> commpand to create a repository with the source code. 
1. Create a virtual environement <kbd>env</kbd> from the command <kbd>python3 -m venv env</kbd> in the folder where you want to create the project.
1. Clone the source code in the into your project folder.
1. Install the following python libraries
    -  <kbd>pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib</kbd> 
1. Enable the Gmail API and create the ncessary credentials.
    - Go to the [Google Developor Console](https://console.cloud.google.com/) and create a new project. Include the Project ID in the <kbd>PROJECT_ID</kbd> environment variable in the <kbd>.env</kbd> file. 
    - Enable the Gmail API for the project through the [API Console](https://console.cloud.google.com/apis/) for the project.
    - From the <kbd>Credentials</kbd> tab in the API Console, create a <kbd>OAuth 2.0 Client ID</kbd> and a <kbd>Service Account</kbd> 
    - Select the <kbd>Edit Oauth Client ID</kbd> button in the OAuth Client ID actions and select <kbd>Download JSON</kbd>. Rename this file to <kbd>credentials.json</kbd> and upload it to the <kbd>utils</kbd> folder in your project root. Ensure that the location for the credentials is consistent in the <kbd>.env</kbd> file. 
    - Using the <kbd>Edit</kbd> action for the service account, create a key by navigating to the <kbd>Keys</kbd> tab and selecting the approporate options. Download the key as a  <kbd>.Json</kbd> file. Rename the file to  <kbd>serviceCredentials.json</kbd> and upload it to the <kbd>utils</kbd> folder at project root.
1. Enable the Google Pub/Sub messaging service. The python program uses Google Pub/Sub as a messaging tool.
    - Create a <kbd>Pub/Sub Topic</kbd> using the <kbd>Create Topic</kbd> tab within the same project created in the previous step. 
    - To create a <kbd>Pub/Sub scubscription</kbd> navigate to the <kbd>Topics</kbd> tab and select the topic created in the previous step. 
    - Navigate the <kbd>Subscriptions</kbd> tab and select <kbd>Create Subscription</kbd>. Select the approporate options neccesary. 
    - Add the service account created prior as a <kbd>Pub/Sub Subscriber</kbd> using the <kbd>Add Principal</kbd> section in the <kbd>Permissions</kbd> tab.
1.  <kbd>cd</kbd> into the folder where the <kbd>main.py</kbd> file is located. Use the:memo: command in the terminal to start the script. 
## :memo: TODO  
1. Include support for scheduling. Create a configuration file which records the <kbd>_HistoryID</kbd> neccesary to poll the Pub/Sub client.
1. Provide Support for programmatically replying to emails. 
## License
This project is licensed under the [Mozilla Public License 2.0](LICENSE)