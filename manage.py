import os
import settings
import json


if not os.path.exists(os.path.join(settings.PATH, 'api.json')):
    with open(os.path.join(settings.PATH, 'api.json'), 'w') as fp:
        json.dump(
            {
                'api_id': '',
                'api_hash': '',
                'name': '',
                'number': ''
            },
            fp,
            indent=4,
        )


with open('api.json', 'r') as fp:
    settings.NAME = json.load(fp)['name']
    settings.NUMBER = json.load(fp)['number']

