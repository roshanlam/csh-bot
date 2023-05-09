import json
import requests

def openJSON(filename: str):
    data: dict = {}
    with open(filename) as f:
        data = json.load(f)
    return data

def writeJSON(filename: str, data: dict):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def calcGrade(grades: dict):
    data: dict = {}
    data = openJSON('data.json')
    grade = 0
    for key in data:
        if key == grades['class']:
            data = data[key]
            break
    for key in grades:
        if key == 'class':
            continue
        grade += float(grades[key]) * (data[key]/100)
    return grade

def fetchJSON(url: str, headers=None):
    response = None
    if headers:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def handleJokes(json_data: dict):
    if json_data['type'] == 'single':
        return json_data['joke']
    elif json_data['type'] == 'twopart':
        return json_data['setup'] + '\n' + json_data['delivery']
    
# a reusable decorator to make a command only work in a specific channel
def strictCommand(bot_command: str, channel_id: int):
    def decorator(func):
        async def wrapper(message):
            if message.content.startswith(bot_command):
                if message.channel.id == channel_id:
                    await func(message)
                else:
                    await message.channel.send('You can only use this command in <#{}>'.format(channel_id))
        return wrapper
    return decorator
