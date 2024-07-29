import requests
import json
    
def add_message(content,role,conversation_id):
    
    url = "http://127.0.0.1:5000/message"

    payload = json.dumps({
    "conversation_id": conversation_id,
    "content": content,
    "role": role
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return