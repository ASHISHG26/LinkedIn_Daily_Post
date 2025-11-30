import os
import requests

# Paste your access token here temporarily (later we'll move it into .env)
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

url = "https://api.linkedin.com/v2/userinfo"

headers = {
    "Authorization": f"Bearer AQVUzbWEe0Yc1Gngssxk9aGP57E29w0N-sCnZ2aHmJHCxZ-len_nraZeC43bISNkf2NKmy3Bm0gRrzqM3ngm4TYHABEfVw0fSMGu3w3ew9ne3_dhepreLqvWtnmfvUkNKvex8XOBzRNs7uIb-2STiXSxMcYjdE9r673q-ZrxEy5jpWPjOzQudNzra9ymC3z1SYJ-EgbicLnk28vBO7-IWwYh5L7mq3nyRkNB6dvEsDyeA6bYO5to_kkQj09uUqyQWo7WYW6TMJAdhpabu3asc9jWBMyd9V5q_8-o3SSlD5dTTqmjI4qjbdYGPyvhg_0jKwmYIbY71ROkcvyDvebUF1aoazZgDA"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print("Body:", response.text)