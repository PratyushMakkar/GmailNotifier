# Gmail Notifications

**Gmail Notifier** is a python application script that monitors your Gmail Inbox using the Gmail API for any new emails. The user recieves a desktop notification each time there is a new email sent. 

## :pushpin: Set up 
1. Use the <kbd>Use this template</kbd> commpand to create a repository with the source code. 
1. Create a virtual environement <kbd>env</kbd> from the command <kbd>python3 -m venv env</kbd> in the folder where you want to create the project.
1. Clone the source code in the into your project folder.
1. Install the following python libraries
    -  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
1. Enable the Gmail API and create the ncessary credentials.
    - Go to the [Google Developor Console](https://console.cloud.google.com/) and create a new project.
    - Enable the Gmail API for the project through the [API Console](https://console.cloud.google.com/apis/)
    - From the <kbd>Credentials</kbd> tab in the API Console, create a <kbd>OAuth 2.0 Client ID</kbd> and a <kbd>Service Account</kbd> 
    - Select the <kbd>Edit Oauth Client ID</kbd> button in the OAuth Client ID actions and select <kbd>Download JSON</kbd>. Rename this file to <kbd>credentials.json</kbd> and upload it to the <kbd>utils</kbd> folder in your project root. Ensure that the location for the credentials is consistent in the <kbd>.env</kbd> folder. 
    - Using the <kbd>Edit</kbd> action for the service account, create a key by navigating to the <kbd>Keys</kbd> tab and selecting the approporate options. Download the key as a  <kbd>.Json</kbd> file. Rename the file to  <kbd>serviceCredentials.json</kbd> and upload it to the <kbd>utils</kbd> folder at project root.
1. Enable the Google Pub/Sub messaging service
    -
1.  <kbd>cd</kbd> into the folder where the <kbd>main.py</kbd> file is located. Use the <kbd>python main.py</kbd> command in the terminal to start the script. 
## License
This project is licensed under the [Mozilla Public License 2.0](LICENSE)