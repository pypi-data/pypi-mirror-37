import json

class Config(object):
    def __init__(self, dict):
        vars(self).update(dict)


def loadconfig(json_file):
    with open(json_file, 'r') as j:
        json_str = j.read()
    return json.loads(json_str, object_hook=Config)
