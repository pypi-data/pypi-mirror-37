from LRC.Server.Command import BaseCommand
from LRC.Common.logger import logger


class TestCommand(BaseCommand):

    def __init__(self, **_kwargs):
        pass

    def __str__(self):
        return  'TestCommand'

    def execute(self, **kwargs):
        logger.info('TestCommand : execute')


def get_command_instance(**_kwargs):
    return TestCommand(**_kwargs)


class TestCommandKwargs(BaseCommand):

    def __init__(self, **_kwargs):
        self.kwargs = _kwargs['kwargs']
        del _kwargs['kwargs']
        logger.info('TestCommandKwargs.__init__ -- {}'.format(_kwargs))

    def __str__(self):
        return  'TestCommandKwargs -- {}'.format(self.kwargs)

    def execute(self, **kwargs):
        logger.info('TestCommandKwargs ({}) : execute'.format(self.kwargs))

def get_test_command_kwargs(**_kwargs):
    return TestCommandKwargs(**_kwargs)

