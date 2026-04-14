import requests
import json

url = "http://localhost:8000/summarize"
text = "This is a test text for summarization. " * 10  # 390 chars

payload = {
    "text": text,
    "length": "short",
    "regenerate": False
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
