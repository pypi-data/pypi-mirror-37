# repobot/commands/login.py
'''set login token'''

from .base import Base

import keyring
import requests
#from requests.auth import HTTPBasicAuth
import sys
import re
import getpass

class Login(Base):
    '''login class'''

    def run(self):
        
        username = input('Github username: ')
        password = getpass.getpass()

        res = requests.get('https://api.github.com/user', auth=requests.auth.HTTPBasicAuth(username, password))

        if res.status_code != 200:
            print('Invalid login request.')
            return sys.exit(1)
        
        keyring.set_password('repobot', 'username', username)
        keyring.set_password('repobot', 'password', password)
        print('Successfully authenticated')        
