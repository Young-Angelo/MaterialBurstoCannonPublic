import json
import requests

def get_quote():
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " " + " - " + json_data[0]['a']
        return quote

def write_json(arg1,storage):
    with open(storage,'w') as f:
        json.dump(arg1,f)
def read_json(storage):
    with open(storage) as b:
        data = json.load(b)
        return data

def check(author):
    def inner_check(message):
        if message.author != author:
            return False
        try:
            str(message.content)
            return True
        except ValueError:
            return False
    return inner_check
