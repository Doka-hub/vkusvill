import os
import json


with open('api.json', 'r') as fp:
    data = json.load(fp)
NAME = data['name']
NUMBER = data['number']
