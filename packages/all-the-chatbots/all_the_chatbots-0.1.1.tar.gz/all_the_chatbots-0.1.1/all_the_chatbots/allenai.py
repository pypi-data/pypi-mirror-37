import requests


def ask_euclid(text):
    url = "http://euclid.allenai.org/api/solve?query=" + text
    return requests.get(url).text


def ask_aristo(text, raw=False):
    url = "http://aristo-demo.allenai.org/api/ask?text=" + text
    data = requests.get(url).json()
    if raw:
        return data
    answers = data["response"]["success"]["answers"]

    response = {}
    for a in answers:
        # 'confidence', 'analyses', 'selection', 'selected'
        if a["selected"]:
            response["answer"] = a["selection"]["directAnswer"]["answer"]
            response["confidence"] = a["confidence"]
            data = a["analyses"][0]["analysis"]["analyses"][0]
            response["expectedAnswerType"] = data['expectedAnswerType']
            response['questionSentence'] = data['questionSentence']
            response['questionType'] = data['questionType']
            response['questionTheme'] = data['questionTheme']
            response['questionSetup'] = data['questionSetup']
            response["dataSource"] = data["sourceFriendlyName"]
            response["top20"] = data['top20ThisCluster']
    return response
