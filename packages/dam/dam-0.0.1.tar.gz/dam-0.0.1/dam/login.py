import requests
from getpass import getpass

from .session import Session

def login(email=None, password=None):
    if not email:
        email = input("Enter your Discord email: ")
    if not password:
        password = getpass("Enter your password: ")

    params = {
            'captcha_key': None, 
            'email': email, 
            'password': password,
            'undelete': False
    }
    r = requests.post("https://discordapp.com/api/v6/auth/login", json=params, headers={'User-Agent': 'ogdog'})

    if r.status_code == 400:
        raise BadCredentials()
    else:
        return Session(r.json()['token'])
