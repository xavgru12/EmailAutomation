Perequisites: googlemail account

Do the following settings in google cloud (retrieved from https://developers.google.com/gmail/api/quickstart/python)

#1 In the Google Cloud console, enable the Gmail API.
#2 Create new Project in google cloud.
#3 oauth2 in google cloud needs to be configured:
In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.
Go to Credentials
Click Create Credentials > OAuth client ID.
Click Application type > Desktop app.
In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
Download the json file and save it as clien_secret.json in current working directory.
In "OAuthZustimmungsbildschirm" (oauth authorization window) click on Api and services to add a user:
type in email where you want to send emails froms

install needed packages with:
pip install -r requirements.txt