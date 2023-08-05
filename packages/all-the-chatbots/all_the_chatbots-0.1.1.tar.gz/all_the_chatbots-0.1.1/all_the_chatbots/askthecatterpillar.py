import requests


def ask_the_caterpillar(query):
    data = requests.post('https://www.askthecaterpillar.com/query', {"query": query})
    data = json.loads(data.text)
    return data["data"]["messages"][0]["content"]
