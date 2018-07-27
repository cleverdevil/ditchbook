import os
import requests
import sys
import conf
import json


def generate_headers():
    headers = {
        'Authorization': 'Bearer %s' % conf.TOKEN
    }
    if hasattr(conf, 'MP_DESTINATION'):
        headers['mp-destination'] = conf.MP_DESTINATION
    return headers


def upload(file_path):
    # TEMPORARY NO OP
    return 'http://example.com/image.jpeg'

    print('Attempting to upload:', file_path)

    files = {'file': ('image.jpg', open(file_path, 'rb'), 'image/jpeg')}
    response = requests.post(
        conf.MP_MEDIA_ENDPOINT,
        headers=generate_headers(),
        files=files
    )

    if response.status_code == 202:
        print('  Uploaded -> ', response.headers['Location'])
        return response.headers['Location']
    else:
        print('  Failed to upload! Status code', response.status_code)
        sys.exit(1)
        return None


def publish(mf2):
    print('Publishing MF2:')
    print(json.dumps(mf2, indent=2))

    # TEMPORARY NO OP
    return 'http://example.com/published-album'

    response = requests.post(
        conf.MP_ENDPOINT,
        json=mf2,
        headers=generate_headers()
    )

    if response.status_code == 202:
        print('  Published -> ', response.headers['Location'])
        return response.headers['Location']
    else:
        print('  Failed to publish! Status code', response.status_code)
        sys.exit(1)
        return None
