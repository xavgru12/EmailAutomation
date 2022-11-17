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

Using EmailAutomation:
#1 in applic.py: write your email address down
#2 in Model/General are the files for the greeting text: GreetingFormal.txt and GreetingInformal.txt
#3 in Model/ create a folder and as subfolder add Content.txt and Subject.txt, folder name will be your context argument
#4 in CompanyDatabase.yaml: use the format to write your data in

In the text files you can define the language eg #English and #German.
In CompanyDatabase.yaml there is company name with contact details: contactFullName contactNickName email
formality, function(hr etc), language, sex. All the fields need to be defined for every contact.

run script using
python applic.py --company <company_name> --context <your_folder_name>

optional argument:
function: either hr, technical or team_lead (position in company)