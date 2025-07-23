import requests
from config import GEMINI_API_KEY

def ask_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"

    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    params = {
        "key": GEMINI_API_KEY
    }

    response = requests.post(url, headers=headers, params=params, json=body)

    if response.status_code == 200:
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error {response.status_code}: {response.text}"
