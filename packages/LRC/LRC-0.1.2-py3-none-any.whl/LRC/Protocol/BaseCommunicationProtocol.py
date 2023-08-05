
class BaseCommunicationProtocol(object):
    """Base class for communication protocol

     Methods for the caller:

    - __init__()

    Methods that may be overridden:

    -

    Methods for derived classes:

    - encode()
      encode message
    - decode()
      decode message

    Class variables that may be overridden by derived classes or
    instances:

    -

    Instance variables:

    - encoding
      encoding for basic encode process (included in encode/decode)

    """

    def __init__(self, **kwargs):
        self.encoding = kwargs["encoding"] if 'encoding' in kwargs else 'utf-8'

    def encode(self, raw_message):
        '''
        encode message
        :param raw_message: encoded message
        :return: messaged that has encoded
        '''
        return raw_message.encode(self.encoding)

    def decode(self, message):
        '''
        decode message
        :param message: encoded message
        :return: raw message that decoded from encoded message
        '''
        return message.decode(self.encoding)