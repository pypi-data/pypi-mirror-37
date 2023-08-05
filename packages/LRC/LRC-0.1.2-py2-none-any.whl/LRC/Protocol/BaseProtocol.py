from LRC.Protocol.BaseCommunicationProtocol import BaseCommunicationProtocol

class BaseProtocol(BaseCommunicationProtocol):

    """Base class for protocol

     Methods for the caller:

    - __init__()

    Methods that may be overridden:

    - pack_message(*args, **kwargs) -> encoded message
      pack message from application information
    - unpack_message(message) -> *args (info from decoded message)
      unpack message, and parse information from it

    Methods for derived classes:

    - encode() -> encoded message
      encode message
    - decode() -> decoded message
      decode message

    Class variables that may be overridden by derived classes or
    instances:

    -

    Instance variables:

    - encoding
      encoding for basic encode process (included in encode/decode)

    """

    def __init__(self, **kwargs):
        super(BaseProtocol, self).__init__(**kwargs)

    def pack_message(self, **kwargs):
        '''
        pack message from given information
        :param kwargs:      information from application
        :return message:    message to send
        '''
        return self.encode('')

    def unpack_message(self, message):
        '''
        unpack message into application information
        :param message:     message to parse from
        :return *args:      information unpacked
        '''
        return ''



