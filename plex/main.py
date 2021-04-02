import requests as req
import base64
import json
from utils.main import get_server_address

sign_in_url = 'https://plex.tv/users/sign_in.json'
server_url = get_server_address()


def get_access_token(auth_data):
    auth = '%s:%s' % (auth_data[0], auth_data[1])
    base64string = base64.b64encode(auth.encode('ascii'))

    headers = {'Authorization': 'Basic %s' % base64string.decode('ascii'),
               'X-Plex-Client-Identifier': 'suisinho-plex',
               'X-Plex-Product': 'suisinho-plex',
               'X-Plex-Version': '0.1.0'}

    r = req.post(sign_in_url, headers=headers)

    if r.status_code == 201:
        data = json.loads(r.content)
        token = data['user']['authToken']

        return token

    return None


def get_libraries(token):
    lib_path = server_url + '/library/sections'
    libraries = []

    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}

    r = req.get(lib_path, headers=headers)

    if r.status_code == 200:
        data = json.loads(r.content)
        for item in data['MediaContainer']['Directory']:
            if item['hidden'] == 0:
                libraries.append(item['title'])

    return libraries
