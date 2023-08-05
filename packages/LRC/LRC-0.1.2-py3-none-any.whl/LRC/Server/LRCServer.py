from __future__ import print_function
from LRC.Controller.LRCController import Controller
from LRC.Common.logger import logger
from LRC.Protocol.v1.ServerProtocol import ServerProtocol
from LRC.Protocol.v1.WaiterProtocol import WaiterProtocol
from LRC.Protocol.v1.ClientProtocol import ClientProtocol
from multiprocessing import Process, Manager
from threading import Thread


try: # python 2
    from SocketServer import UDPServer
except ImportError:  # python 3
    from socketserver import UDPServer


class LRCServer ( UDPServer, object ):

    allow_reuse_address = True

    def __init__(self, **kwargs ):
        super(LRCServer, self).__init__(kwargs["server_address"], None )
        self.waiter_address     = kwargs["waiter_address"]
        self.message_encoding   = kwargs["message_encoding"] if "message_encoding" in kwargs else 'utf-8'
        self.verify_code        = kwargs["verify_code"] if "verify_code" in kwargs else None
        self.client_list        = kwargs["client_list"] if "client_list" in kwargs else None
        self.log_mailbox        = kwargs["log_mailbox"] if "log_mailbox" in kwargs else None
        self.info       = self.log_mailbox.put_nowait if self.log_mailbox else logger.info
        self.warning    = self.log_mailbox.put_nowait if self.log_mailbox else logger.warning
        # protocol
        self.server_protocol = ServerProtocol()
        self.client_protocol = ClientProtocol()
        # verbose info
        if 'verbose' in kwargs and kwargs['verbose'] is True:
            from functools import partial
            self._verbose_info = self._verbose_info_imp
            self._verbose_info('verbose enabled.')
        else:
            from LRC.Common.empty import empty
            self._verbose_info = empty
        self._verbose_info('server {}, waiter {}'.format( self.server_address, self.waiter_address))

    # interfaces
    def finish_request(self, request, client_address):
        self._verbose_info('receive request {} from {}'.format(request, client_address))
        tag, kwargs = self.server_protocol.unpack_message(request[0])
        self._verbose_info('unpack result : {}, {}'.format(tag, kwargs))
        if 'request' == tag:
            if 'connect to waiter' == kwargs['name']:
                if self.client_list is not None and client_address not in self.client_list:
                    self.client_list.append(client_address)
                    self.info('Server: add client {0} to client list.'.format(client_address))
                respond_message = self.client_protocol.pack_message(
                    respond=kwargs['name'], state='confirm', waiter_address=self.waiter_address)
                self.socket.sendto(respond_message, client_address)

    def verify_request(self, request, client_address):
        # todo: check verify_code, check client blacklist, and so on ...
        return True

    # functional
    def _verbose_info_imp(self, info):
        self.info('LRC server : [verbose] {}'.format(info))



from pykeyboard import PyKeyboard
import re

class LRCWaiter( UDPServer, object ): # waiter serve all the time

    allow_reuse_address = True

    def __init__(self, **kwargs ):
        super(LRCWaiter, self).__init__(kwargs["waiter_address"], None )
        self.message_encoding       = kwargs["message_encoding"] if "message_encoding" in kwargs else 'utf-8'
        self.connect_server_address = kwargs["server_address"]
        self.client_list            = kwargs["client_list"] if "client_list" in kwargs else None
        self.log_mailbox            = kwargs["log_mailbox"] if "log_mailbox" in kwargs else None
        self.info       = self.log_mailbox.put_nowait if self.log_mailbox else logger.info
        self.warning    = self.log_mailbox.put_nowait if self.log_mailbox else logger.warning
        self.keyboard = PyKeyboard()
        self.key_matcher = re.compile(r'[a-zA-Z ]+')
        # self.key_settings = Controller.settings
        self.execute_delay = 0
        # protocol
        self.waiter_protocol = WaiterProtocol()
        self.server_protocol = ServerProtocol()
        # verbose info
        if 'verbose' in kwargs and kwargs['verbose'] is True:
            from functools import partial
            self._verbose_info = self._verbose_info_imp
            self._verbose_info('verbose enabled.')
        else:
            from LRC.Common.empty import empty
            self._verbose_info = empty
        self._verbose_info('server {}, waiter {}'.format( self.connect_server_address, self.server_address))

    # interfaces
    def finish_request(self, request, client_address):
        self._verbose_info('receive request {} from {}'.format(request, client_address))
        tag, kwargs = self.waiter_protocol.unpack_message(request[0])
        if 'controller' == tag:
            controller = kwargs['controller']
            key_combination = controller.get_key_list()
            try:
                if self.execute_delay > 0:
                    from threading import Timer
                    Timer( self.execute_delay, self.keyboard.press_keys, args=(key_combination,)).start()
                    self.info('Waiter: schedule pressing keys in {2} seconds from {0} : {1}'.format(client_address, key_combination, self.execute_delay))
                else:
                    self.keyboard.press_keys(key_combination)
                    self.info('Waiter: pressing keys from {0} : {1}'.format(client_address, key_combination))
            except Exception as err:
                self.info('Waiter: can\'t press key from {0} {1} : {2}'.format(client_address, key_combination, err.args))
        else:
            self._verbose_info('unknown request {} with parameters : {}'.format(tag, kwargs))

    def verify_request(self, request, client_address):
        if self.client_list is None or client_address not in self.client_list:
            self.warning('Waiter: shutdown request from unknown client : {0}'.format(client_address))
            return False
        return True

    # functional
    def _verbose_info_imp(self, info):
        self.info('LRC waiter : [verbose] {}'.format(info))



def start_server(**kwargs):
    '''
    start LRC server with given parameters
    :param kwargs:
        required :
            server_address      -- LRC server address, e.g. ('127.0.0.1', 33791)
            waiter_address      -- LRC waiter address, e.g. ('127.0.0.1', 33791)
        optional :
            message_encoding    -- 'utf-8'(default)
            verify_code         -- None
            client_list         -- None
            log_mailbox         -- None
    :return:
    '''
    LRCServer(**kwargs).serve_forever()


def start_waiter(**kwargs):
    '''
    start LRC waiter with given parameters
    :param kwargs:
        required :
            connect_server_address  -- LRC server address, e.g. ('127.0.0.1', 33791)
            waiter_address          -- LRC waiter address, e.g. ('127.0.0.1', 33791)
        optional :
            message_encoding        -- 'utf-8'(default)
            verify_code             -- None
            client_list             -- None
            log_mailbox             -- None
    :return:
    '''
    LRCWaiter(**kwargs).serve_forever()


class LRCServerManager(object):

    def __init__(self):
        try:
            self.communication_manager = Manager()
            self.client_list = self.communication_manager.list()
            self.log_mailbox = self.communication_manager.Queue()
            self.mode = 'full'
        except Exception as err:
            logger.error('LRC : Manager start failed, only basic function started')
            self.communication_manager = None
            self.client_list = None
            self.log_mailbox = None
            self.mode = 'basic'

        self._server_process = None
        self.server_config = dict()

        self._waiter_process = None
        self.waiter_config = dict()

        self._mailbox_watcher_thread = None
        self._start_mailbox_watcher()

    # commands interfaces
    def start_server(self, **kwargs):
        self._update_server_config(kwargs)
        self._start_server(**kwargs)

    def stop_server(self):
        if self._server_process:
            if self._server_process.is_alive():
                logger.info('LRC : stop server')
                self._server_process.terminate()
            self._server_process = None

    def start_waiter(self, **kwargs):
        self._update_waiter_config(kwargs)
        self._start_waiter(**kwargs)

    def stop_waiter(self):
        if self._waiter_process:
            if self._waiter_process.is_alive():
                logger.info('LRC : stop waiter')
                self._waiter_process.terminate()
            self._waiter_process = None

    def stop_communication_manager(self):
        if self.communication_manager:
            manager = self.communication_manager
            self.communication_manager = None
            manager.shutdown()

    def quit(self):
        self.stop_server()
        self.stop_waiter()
        self.stop_communication_manager()

    # functional
    def _update_server_config(self, config):
        if 'client_list' not in config or config['client_list'] is None and self.client_list:
            config['client_list'] = self.client_list
        if 'log_mailbox' not in config or config['log_mailbox'] is None and self.log_mailbox:
            config['log_mailbox'] = self.log_mailbox

    def _start_server(self, **kwargs):
        if self._server_process:
            if self._server_process.is_alive():
                if kwargs == self.server_config:
                    logger.info('LRC : server already running')
                    return
                else:
                    logger.info('LRC : terminate server process for restart')
                    self._server_process.terminate()
            self._server_process = None
        try:
            self._server_process = Process(target=start_server, kwargs=kwargs)
            self._server_process.start()
            self.server_config = kwargs
            logger.info('LRC : start server process at {}'.format(kwargs['server_address']))
        except Exception as err:
            logger.error('LRC : start server process failed : {}'.format(err.args))

    def _update_waiter_config(self, config):
        if 'client_list' not in config or config['client_list'] is None and self.client_list:
            config['client_list'] = self.client_list
        if 'log_mailbox' not in config or config['log_mailbox'] is None and self.log_mailbox:
            config['log_mailbox'] = self.log_mailbox

    def _start_waiter(self, **kwargs):
        if self._waiter_process:
            if self._waiter_process.is_alive():
                if kwargs == self.waiter_config:
                    logger.info('LRC : waiter already running')
                    return
                else:
                    logger.info('LRC : terminate waiter process for restart')
                    self._waiter_process.terminate()
            self._waiter_process = None
        try:
            self._waiter_process = Process(target=start_waiter, kwargs=kwargs)
            self._waiter_process.start()
            self.waiter_config = kwargs
            logger.info('LRC : start waiter process at {}'.format(kwargs['waiter_address']))
        except Exception as err:
            logger.error('LRC : start waiter process failed : {}'.format(err.args))

    def _start_mailbox_watcher(self):
        if not self._mailbox_watcher_thread:
            self._mailbox_watcher_thread = Thread(target=self._mailbox_watcher)
            self._mailbox_watcher_thread.start()

    # detailed
    def _mailbox_watcher(self):
        while True:
            try:
                logger.info(self.log_mailbox.get()) # get will block until there is data
            except Exception as err:
                if self.communication_manager:
                    logger.error('LRC : mailbox error : {}({})'.format(err, err.args))
                else:
                    logger.info('LRC : closing servers.')
                    break


if '__main__' == __name__:

    def test000_async_server():
        import time
        from multiprocessing import Process
        from threading import Thread

        waiter_address = ('127.0.0.1',35527)
        server_address = ('127.0.0.1',35530)

        waiter = LRCWaiter(waiter_address=waiter_address, connect_server_address=server_address)
        server = LRCServer(server_address=server_address, waiter_address=waiter_address)

        st = Thread(target=server.serve_forever)
        print('serve thread created :', st)
        st.start()
        print('start server at', server.server_address)

        wt = Thread(target=waiter.serve_forever)
        print('waiter thread created :', wt)
        wt.start()
        print('start wait at', waiter.server_address)


        time.sleep(15)
        server.shutdown()
        waiter.shutdown()
        print('force to close servers ')
        print('server :', st, '-- closed :', server._BaseServer__is_shut_down.is_set())
        print('waiter :', wt, '-- closed :', waiter._BaseServer__is_shut_down.is_set())
        pass

    test000_async_server()

    pass
