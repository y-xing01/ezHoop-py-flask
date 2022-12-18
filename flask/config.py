import json

with open("/flask/.secrets.json") as config_file:
    config = json.load(config_file)