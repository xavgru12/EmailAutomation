from flask import Flask, request
import requests

from emailClient import SendMessage

app = Flask(__name__)

GOGS_API = "http://10.10.80.134:3000/api/v1"
GOGS_URL = "http://10.10.80.134:3000"
ORG = "ECON"
TOKEN = "a0cda256fb20e91a4d9d925c8eab644ddec08e6b"  # needs read access

def get_org_emails():
    headers = {"Content-Type": "application/json", "Authorization": f"token {TOKEN}"}
    r = requests.get(f"{GOGS_API}/org/{ORG}/repos", headers=headers)
    if r.status_code == 200 or r.status_code == 201:
        pass
    else:
        #print(f"Error fetching members: {r.status_code} {r.text}")
        raise Exception("Failed to fetch members")
    emails = []
    for m in r.json():
        user = m["login"]
        u = requests.get(f"{GOGS_API}/users/{user}", headers=headers).json()
        if "email" in u and u["email"]:
            emails.append(u["email"])
    return emails

def get_org_emails2(gogs_url: str, org: str, token: str) -> list[str]:
    """
    Fetch public emails of members of a Gogs organization.

    gogs_url: Base URL of Gogs server, e.g. https://gogs.example.com
    org: Organization name
    token: Personal access token
    """
    #working
    # headers = {"Authorization": f"token {token}"}
    # members_url = f"{gogs_url}/api/v1/user/orgs"
    # response = requests.get(members_url, headers=headers)
    # response.raise_for_status()
    # members = response.json()
    # print(members)

    # working
    headers = {"Authorization": f"token {token}"}
    url = f"{gogs_url}/repos/ECON/ag-econ-w/collaborators"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    collaborators = response.json()
    print(collaborators)

    headers = {"Authorization": f"token {token}"}
    url = f"{gogs_url}/orgs/ECON/teams"

    data = execute_gogs_api_request(url, headers)
    print(data)
    for item in data:
        if item.get("name") == "Owners":
            team_id = item.get("id")
            print(f"Team ID of 'Owners': {team_id}")

    # url = f"{gogs_url}/repos/{org}/members"
    # data = execute_gogs_api_request(url, headers)
    # print("Team members:", data)

    # print(members)
    # base = gogs_url.rstrip('/')
    # headers = {"Content-Type": "application/json", "Authorization": f"token {token}"}
    # session = requests.Session()
    # session.headers.update(headers)

    # emails: set[str] = set()
    # page = 1

    # while True:
    #     # List org members
    #     resp = session.get(f"{base}/api/v1/org/{org}/members")
    #     if not resp.ok:
    #         raise RuntimeError(f"Failed to list members: {resp.status_code}")

    #     members = resp.json()
    #     if not members:
    #         break  # no more members

    #     for m in members:
    #         username = m.get("login")
    #         if not username:
    #             continue

    #         # Get user details
    #         uresp = session.get(f"{base}/api/v1/users/{username}")
    #         if uresp.ok:
    #             u = uresp.json()
    #             if u.get("email"):
    #                 emails.add(u["email"])

    #     page += 1

    # return sorted(emails)

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
    
    #emails = get_org_emails()
    emails = ["xaver.max.gruber+EmailClient@googlemail.com"]
    subject = f"[Gogs] {event} event in {payload['repository']['full_name']}"
    body = f"Event: {event}\n\nPayload:\n{payload}"
    sender = "xaver.max.gruber@googlemail.com"
    send_messages(sender, emails, subject, body)
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
    #print(get_org_emails2(GOGS_API, ORG, TOKEN))
