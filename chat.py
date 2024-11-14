import json
from datetime import datetime

def get_history():
    with open('chat.json', 'r') as f:
        data : dict = json.load(f)
        return data.get('chat').get('history')
    
def get_history_llm():
    with open('chat.json', 'r') as f:
        data : dict = json.load(f)

    return [{"role": item["role"], "content": item["content"]} for item in data.get('chat', {}).get('history', [])]


def add_message(user: str, content: str):
    time = datetime.now()
    
    # First, open the file in read mode to get the existing data
    with open('chat.json', 'r') as f:
        data: dict = json.load(f)

    chat_history: list = data.get('chat', {}).get('history', [])


    # Append the new message to thgit push --set-upstream origin maine history
    chat_history.append(
        {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "role": user,
            "content": content
        }
    )

    # Now, open the file in write mode to save the updated data
    with open('chat.json', 'w') as f:
        data['chat']['history'] = chat_history
        json.dump(data, f, indent=4)  # Use json.dump to write JSON with indentation

def clear_history():
    with open('chat.json', 'w') as f:
        data = {
            "chat" : {
                "history" : []
            }
        }
        json.dump(data, f, indent=4)  