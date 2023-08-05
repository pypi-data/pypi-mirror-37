from LRC.Protocol.v1.BaseProtocol import V1BaseProtocol
from LRC.Controller.LRCController import Controller


class WaiterProtocol(V1BaseProtocol): # how do waiter unpack message, how to pack message sent to waiter
    '''
    waiter protocol defines how do waiter unpack message, how to pack message sent to waiter
    process several kinds of message:
        controller          -- receive a controller to execute keyboard combination locally

    '''

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack request to raw_message
        :param kwargs:  specifications for a request/command/respond
        :return:        raw_message to send
        '''
        if 'controller' in kwargs:
            raw_message = self._pack_controller_message(**kwargs)
        else:
            raise ValueError('WaiterProtocol : only controller message supported for now.')
        return self.encode(raw_message)

    def unpack_message(self, message):
        raw_message = self.decode(message)
        tag = self._unpack_tag(raw_message)
        if 'controller' == tag:
            controller_message = raw_message[len(tag)+1:]
            kwargs=dict()
            kwargs['controller'] = Controller('waiter protocol', from_str=controller_message)
        else:
            raise ValueError('WaiterProtocol : only controller message supported for now.')
        return tag, kwargs

    # functional
    def _pack_controller_message(self, **kwargs):
        raw_message = "controller="
        raw_message += "{}".format(kwargs['controller'])
        return raw_message

