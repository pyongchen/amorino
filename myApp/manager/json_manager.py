import json


class JsonManager(object):
    def __init__(self):
        pass

    @staticmethod
    def read_json(path):
        json_file = open(path, "r")
        data = json.load(json_file)
        json_file.close()
        return data

    @staticmethod
    def write_json(path, data):
        json_file = open(path, "w")
        json_file.write(json.dumps(data))
        json_file.close()

jsonManager = JsonManager()
