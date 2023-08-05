
__all__ = ['ArgumentError', 'NotFoundError']

class ArgumentError(Exception):

    def __str__(self):
        return ('Argument not available.')


class NotFoundError(Exception):

    def __str__(self):
        return ('Not found.')
