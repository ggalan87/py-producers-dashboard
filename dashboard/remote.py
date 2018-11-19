import lorem
from dashboard.models import Show

import requests
import math
import json

class Store:

    sample_descr = lorem.paragraph()

    shows = \
    [
        Show('Rastamidnights', ['arouraios'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
        Show('Awsome show title', ['arouraios'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
        Show('Awkward show title', ['ggalan'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
    ]

    def get_user_shows(self, username):
        user_shows = []
        for s in self.shows:
            if username in s.users:
                user_shows.append(s)
        return user_shows


def validate_login(username, password):
    return username == 'arouraios' and password == 'papakia'
    #return not (username + password)


def get_metadata():
    try:
        r = requests.get('http://prod.radio.uoc.gr:9670/')
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        # Awkward way to get the errno from the error message, because it is not stored in the object, unlike older
        # version of the library as reported in:
        # https://stackoverflow.com/questions/19370436/get-errno-from-python-requests-connectionerror
        # msg = e.args[0].reason.args[0]
        # errno = int(re.search(r"\[Errno\ ([0-9]+)\]", msg).group(1))
        # exit(errno)
        return None, 15

    try:
        data = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        print(r.text)
        raise Exception("Strange JSON {}".format(r.text))

    duration = int(data['current_song']['Duration'])
    elapsed = int(data['current_song']['Elapsed'])

    return data, (duration - elapsed)


def query_autopilot_remaining():
    data, next = get_metadata()
    print(data)
    return next
