# repobot/commands/base.py
'''The base command.'''

class Base(object):
    '''A base command.'''

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('The run() command was not implemented for this subclass')
