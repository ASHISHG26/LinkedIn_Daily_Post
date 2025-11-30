import requests

ACCESS_TOKEN = "AQVUzbWEe0Yc1Gngssxk9aGP57E29w0N-sCnZ2aHmJHCxZ-len_nraZeC43bISNkf2NKmy3Bm0gRrzqM3ngm4TYHABEfVw0fSMGu3w3ew9ne3_dhepreLqvWtnmfvUkNKvex8XOBzRNs7uIb-2STiXSxMcYjdE9r673q-ZrxEy5jpWPjOzQudNzra9ymC3z1SYJ-EgbicLnk28vBO7-IWwYh5L7mq3nyRkNB6dvEsDyeA6bYO5to_kkQj09uUqyQWo7WYW6TMJAdhpabu3asc9jWBMyd9V5q_8-o3SSlD5dTTqmjI4qjbdYGPyvhg_0jKwmYIbY71ROkcvyDvebUF1aoazZgDA"
AUTHOR_URN = "urn:li:person:azyahE35Y0"

url = "https://api.linkedin.com/rest/posts"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "LinkedIn-Version": "202502",          # a recent version in YYYYMM format
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json"
}

post_body = {
    "author": AUTHOR_URN,
    "commentary": "Testing my LinkedIn API setup 🚀\n\nThis post was created via Python. Next step: connect Groq + LangChain to generate AI/tech posts automatically.",
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}

resp = requests.post(url, headers=headers, json=post_body)

print("Status:", resp.status_code)
print("Body:", resp.text)