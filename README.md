Perequisites: googlemail account

Do the following settings in google cloud (retrieved from https://developers.google.com/gmail/api/quickstart/python)

#1 In the Google Cloud console, enable the Gmail API. <br>
#2 Create new Project in google cloud. <br>
#3 oauth2 in google cloud needs to be configured: <br>
In the Google Cloud console, go to Menu menu > APIs & Services > Credentials. <br>
Go to Credentials <br>
Click Create Credentials > OAuth client ID. <br>
Click Application type > Desktop app. <br>
In the Name field, type a name for the credential. This name is only shown in the Google Cloud console. <br>
Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.<br>
Click OK. The newly created credential appears under OAuth 2.0 Client IDs.<br>
Download the json file and save it as client_secret.json in current working directory.<br>
In "OAuthZustimmungsbildschirm" (oauth authorization window) click on Api and services to add a user:<br>
type in email where you want to send emails from<br>
