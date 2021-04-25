import requests as req
import base64
import json
from utils.main import get_server_address

SIGN_IN_URL = 'https://plex.tv/users/sign_in.json'
SECTIONS_URL = '/library/sections'
server_url = get_server_address()
media_type_ids = {'movies': 28, 'animes': 29, 'series': 30, 'courses': 32, 'animated-series': 33}


def get_access_token(auth_data):
    auth = '%s:%s' % (auth_data[0], auth_data[1])
    base64string = base64.b64encode(auth.encode('ascii'))

    headers = {'Authorization': 'Basic %s' % base64string.decode('ascii'),
               'X-Plex-Client-Identifier': 'suisinho-plex',
               'X-Plex-Product': 'suisinho-plex',
               'X-Plex-Version': '0.1.0'}

    r = req.post(SIGN_IN_URL, headers=headers)

    if r.status_code == 201:
        data = json.loads(r.content)
        token = data['user']['authToken']

        return token

    return None


def get_libraries(token):
    lib_path = server_url + SECTIONS_URL
    libraries = []

    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}

    r = req.get(lib_path, headers=headers)

    if r.status_code == 200:
        data = json.loads(r.content)

        for item in data['MediaContainer']['Directory']:
            if item['hidden'] == 0:
                libraries.append(item['title'])

    return libraries


def get_library_content(token, section):
    media_path = server_url + SECTIONS_URL + '%s/all' % media_type_ids[section]
    items = []

    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}

    r = req.get(media_path, headers=headers)

    if r.status_code == 200:
        data = json.loads(r.content)

        for item in data['MediaContainer']['Metadata']:
            items.append(item['title'])

    return items
