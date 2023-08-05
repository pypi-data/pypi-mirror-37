# repobot/commands/hello.py
'''Test hello command'''

from .base import Base
from json import dumps

from .utils import set_token
import requests

class Hello(Base):
    '''say hello world'''

    @set_token
    def run(self, basicauth):
        
        r = requests.get('https://api.github.com/user', auth=basicauth)
        print('the re was', r)
        print('Hello, world!')
        print('You suplied the following optons:', dumps(self.options, indent=2, sort_keys=True))
