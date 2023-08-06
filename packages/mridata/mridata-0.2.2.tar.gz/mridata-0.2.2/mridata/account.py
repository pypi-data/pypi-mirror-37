import requests
from urllib.parse import urljoin

MRIDATA_ORG = 'http://mridata.org/'
LOGIN_URL = urljoin(MRIDATA_ORG, 'accounts/login/')


def login(username, password):

    session = requests.Session()
    session.get(LOGIN_URL)
    csrftoken = session.cookies['csrftoken']
    login_data = {'username': username, 'password': password,
                  'csrfmiddlewaretoken': csrftoken}
    p = session.post(LOGIN_URL, data=login_data)

    if 'login'in p.url:
        raise Exception('Cannot find user with the given credentials.')

    return session
