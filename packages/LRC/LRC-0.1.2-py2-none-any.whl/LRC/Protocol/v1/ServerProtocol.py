from LRC.Protocol.v1.BaseProtocol import V1BaseProtocol


class ServerProtocol(V1BaseProtocol): # how do server unpack message, how to pack message sent to server
    '''
    server protocol defines how do server unpack message, how to pack message sent to server
    process several kinds of message :
        connection request          -- ask for permission for connection to waiter

    '''

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack request to raw_message
        :param kwargs:  specifications for a request/command/respond
        :return:        raw_message to send
        '''
        if 'request' in kwargs:
            raw_message = self._pack_request_message(**kwargs)
        else:
            raise ValueError('ServerProtocol :  only request message supported for now.')
        return self.encode(raw_message)

    # functional
    def _pack_request_message(self, **kwargs):
        raw_message = "request="
        raw_message += ",name='{}'".format(kwargs['request'])
        del kwargs['request']
        for k, v in kwargs.items():
            raw_message += self._pack_pair(k, v)
        return raw_message


