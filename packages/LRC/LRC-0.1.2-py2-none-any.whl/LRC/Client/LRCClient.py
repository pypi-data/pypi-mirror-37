from LRC.Protocol.v1.ServerProtocol import ServerProtocol
from LRC.Protocol.v1.WaiterProtocol import WaiterProtocol
from LRC.Protocol.v1.ClientProtocol import ClientProtocol
from LRC.Controller.LRCController import Controller
from LRC.Common.logger import logger
from LRC.Common.empty import empty
from socket import *


def _verbose_info(info):
    logger.info('LRCClient : verbose : {}'.format(info))


class LRCClient(object):

    def __init__(self, *, verbose=False, server_address=('127.0.0.1',35530), **kwargs):
        self._verbose = False
        self.verbose_info = empty
        self.verbose = verbose
        self.server_address = server_address
        self.waiter_address = None
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.settimeout(0.5)
        self.client_protocol = ClientProtocol()
        self.waiter_protocol = WaiterProtocol()
        self.server_protocol = ServerProtocol()

    # property
    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        if val == self._verbose: return
        if val:
            self.verbose_info = _verbose_info
        else:
            self.verbose_info = empty

    # interfaces
    def connect(self, server_address):
        # update configurations
        self.server_address = server_address
        # send request
        request_message = self.server_protocol.pack_message(request='connect to waiter', state='request')
        self.socket.sendto(request_message, server_address)
        # receive respond
        msg, server_address = self.socket.recvfrom(1024)
        self.verbose_info('got : {}'.format(msg))
        tag, kwargs = self.client_protocol.unpack_message(msg)
        self.verbose_info('unpack : {} -- {}'.format(tag, kwargs))
        if 'respond' == tag:
            if 'confirm' == kwargs['state']:
                try:
                    self.waiter_address = kwargs['waiter_address']
                except Exception as err:
                    logger.error('Client : parse waiter_address error : {}'.format(err.args))
                    self.waiter_address = None
            else:
                logger.error('Client : request to server {} failed, state : {}'.format(self.server_address, kwargs['state']))
        if self.waiter_address:
            if self.waiter_address[0] in ['127.0.0.1', '0.0.0.0']: # if waiter is on server, then modify waiter address
                self.waiter_address = (server_address[0], self.waiter_address[1])
            logger.info('Client : parse waiter address from : {0} with waiter address : {1}'.format(msg, self.waiter_address))

    def send_combinations(self, *args):
        if self.waiter_address:
            message = self.waiter_protocol.pack_message(controller=Controller('LRCClient', *args))
            self.socket.sendto(message, self.waiter_address)
        else:
            logger.error('Client : waiter address unknown, connect to server to get one.')


if '__main__' == __name__:
    def __test000__():
        import time

        server_address = ('127.0.0.1',35530)
        client = LRCClient()
        client.connect(server_address)

        time.sleep(5)
        print('start tap keys now')

        client.send_combinations('j')
        client.send_combinations('o', 'shift')
        client.send_combinations('k', 'shift')
        client.send_combinations('e')

        pass

    __test000__()
    pass

