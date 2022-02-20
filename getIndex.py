import json

def getIndex(path):
    with open(path, "r") as f:
        dictionary = json.load(f)
    return dictionary
