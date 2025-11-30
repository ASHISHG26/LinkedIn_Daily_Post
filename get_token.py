import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/callback")
AUTH_CODE = os.getenv("LINKEDIN_AUTH_CODE")

token_url = "https://www.linkedin.com/oauth/v2/accessToken"

data = {
    "grant_type": "authorization_code",
    "code": AUTH_CODE,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

response = requests.post(token_url, data=data)

print("Status:", response.status_code)
print("Body:", response.text)