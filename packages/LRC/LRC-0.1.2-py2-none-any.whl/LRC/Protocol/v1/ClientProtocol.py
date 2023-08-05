from LRC.Protocol.v1.BaseProtocol import V1BaseProtocol


class ClientProtocol(V1BaseProtocol): # how do client unpack message, how to pack message sent to client
    '''
    client protocol defines how do client unpack message, how to pack message sent to client
    process several kinds of message :
        connection request respond          -- contains info about success or not, and how to connect to waiter

    '''

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack message from given information
        :param kwargs:      information from application
        :return message:    message to send
        '''
        if 'respond' in kwargs:
            raw_message = self._pack_respond_message(**kwargs)
        else:
            raise ValueError('ClientProtocol : only respond message supported for now.')
        return self.encode(raw_message)

    def unpack_message(self, message):
        '''
        unpack message into command or controller
        :param message:     message received
        :return command:    command parsed from message
        '''
        raw_message = self.decode(message)
        tag = self._unpack_tag(raw_message)
        args_message = raw_message[len(tag)+1:]
        kwargs = self._unpack_args(args_message)
        return tag, kwargs

    # functional
    def _pack_respond_message(self, **kwargs):
        raw_message = "respond="
        raw_message += ",request='{}'".format(kwargs['respond'])
        del kwargs['respond']
        for k, v in kwargs.items():
            raw_message += self._pack_pair(k, v)
        return raw_message

