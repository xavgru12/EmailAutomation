from flask import Flask, request
import requests
import json

from emailClient import SendMessage

app = Flask(__name__)

GOGS_API = "http://10.10.80.134:3000/api/v1"
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

def format_payload_for_pull_request(payload: dict) -> str:
    action = payload.get("action", "updated")
    pr = payload.get("pull_request", {})
    title = pr.get("title", "No title")
    url = pr.get("html_url", "")
    mergeable = pr.get("mergeable", None)
    merged = pr.get("merged", None)
    merged_at = pr.get("merged_at", None)
    merged_by = pr.get("merged_by", None)
    head_branch = pr.get("head_branch", None)
    base_branch = pr.get("base_branch", None)
    email = payload.get("sender", None).get("email", None)
    user_name = payload.get("sender", None).get("username", None)
    assignee = pr.get("assignee", None).get("username", None) if pr.get("assignee", None) else "None"

    # format like this again: html url, title, action, head_branch, base_branch, email, user_name, mergeable, merged, merged_at, merged_by
    formatted = (
        f"URL: {url}\n"
        f"Title: {title}\n"
        f"Action: {action}\n"
        f"Merge from: {head_branch}\n"
        f"Merge into: {base_branch}\n"
        f"Assigned to: {assignee}\n"
        f"Action by user: {user_name}\n"
        f"Action by email: {email}\n"
        f"Merged: {merged}\n"
    )
    if merged is True:
        formatted += (
            f"Merged At: {merged_at}\n"
            f"Merged By: {merged_by}\n"
        )
    else:
        formatted += (f"Mergeable: {mergeable}\n")

    formatted += f"\n--\n Full payload: {json.dumps(payload, indent=2)}\n--\nThis email was automatically sent by the Gogs Webhook."
    return formatted

def send_messages(sender, email_list, subject, body):
    for recipient in email_list:
        SendMessage(sender, recipient, subject, "", body)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    event = request.headers.get("X-Gogs-Event")
    sender = "xaver.max.gruber@googlemail.com"

    if event == "pull_request":
        emails = retrieve_gogs_org_emails(GOGS_API, ORG, TEAM, TOKEN)
        body = format_payload_for_pull_request(payload)
        action = payload.get("action", "updated")
        repository = payload.get("repository", {}).get("full_name", "unknown repository")
        subject = f"[Gogs] Pull Request {action} in {repository}"
        send_messages(sender, emails, subject, body)
    return "OK"

if __name__ == "__main__":
    #app.run(port=5000)
    print(retrieve_gogs_org_emails(GOGS_API, ORG, TEAM, TOKEN))
