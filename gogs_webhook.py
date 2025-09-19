from flask import Flask, request
import requests

from emailClient import SendMessage

app = Flask(__name__)

GOGS_API = "http://10.10.80.134:3000/api/v1"
GOGS_URL = "http://10.10.80.134:3000"
ORG = "ECON"
TOKEN = "a0cda256fb20e91a4d9d925c8eab644ddec08e6b"
TEAM = "Owners"


def retrieve_gogs_org_emails(base_gogs_api_url: str, org: str, team: str, token: str) -> list[str]:
    headers = {"Authorization": f"token {token}"}
    url = f"{base_gogs_api_url}/orgs/ECON/teams"


    team_id = get_team_id(url, org, team, headers)
    if team_id is None:
        raise ValueError(f"Team '{team}' not found")

    url = f"{base_gogs_api_url}/admin/teams/{team_id}/members"
    email_list = get_user_email_list(url, headers)
    return email_list


def get_team_id(gogs_url: str, org: str, team_name: str, headers: str) -> int:
    data = execute_gogs_api_request(gogs_url, headers)
    print(data)
    for item in data:
        if item.get("name") == team_name:
            team_id = item.get("id")
            print(f"Team ID of '{team_name}': {team_id}")
            return team_id

def get_user_email_list(gogs_url: str, headers: str) -> list[str]:
    data = execute_gogs_api_request(gogs_url, headers)
    email_list = [member.get("email") for member in data if member.get("email")]
    return email_list

def execute_gogs_api_request(url: str, headers: str) -> dict:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def send_messages(sender, email_list, subject, body):
    for recipient in email_list:
        SendMessage(sender, recipient, subject, "", body)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    event = request.headers.get("X-Gogs-Event")

    emails = retrieve_gogs_org_emails(GOGS_API, ORG, TEAM, TOKEN)
    subject = f"[Gogs] {event} event in {payload['repository']['full_name']}"
    body = f"Event: {event}\n\nPayload:\n{payload}"
    sender = "xaver.max.gruber@googlemail.com"
    send_messages(sender, emails, subject, body)
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
    #print(retrieve_gogs_org_emails(GOGS_API, ORG, TEAM, TOKEN))
