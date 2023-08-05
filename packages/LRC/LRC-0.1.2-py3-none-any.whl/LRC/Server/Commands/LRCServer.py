from LRC.Server.LRCServer import LRCServerManager
from LRC.Server.Config import LRCServerConfig
from multiprocessing import Process, Manager, freeze_support


_manager = None
def manager():
    global _manager
    if not _manager:
        _manager = LRCServerManager()
    return _manager


def start_lrc_server(**kwargs):
    config = LRCServerConfig(**kwargs)
    manager().start_server(**config.server_config)


def start_lrc_waiter(**kwargs):
    config = LRCServerConfig(**kwargs)
    manager().start_waiter(**config.waiter_config)


def start_lrc(**kwargs):
    config = LRCServerConfig(**kwargs)
    manager().start_server(**config.server_config)
    manager().start_waiter(**config.waiter_config)


def stop_lrc_server():
    manager().stop_server()


def stop_lrc_waiter():
    manager().stop_waiter()


def stop_lrc():
    manager().stop_server()
    manager().stop_waiter()


def quit():
    global _manager
    if _manager:
        _manager.quit()
        _manager = None


if '__main__' == __name__:

    def test_case_000(): # basic usage
        from LRC.Server.Config import LRCServerConfig
        from time import sleep
        freeze_support()

        manager = LRCServerManager()

        config = LRCServerConfig()
        config.server_port = 35530
        config.waiter_port = 35527

        manager.start_server(**config.server_config)
        manager.start_waiter(**config.waiter_config)

        sleep(30)
        manager.quit()


    def test_case_001():
        from LRC.Server.Config import LRCServerConfig
        from time import sleep

        config = LRCServerConfig()
        config.server_port = 35530
        config.waiter_port = 35527

        manager().start_server(**config.server_config)
        manager().start_waiter(**config.waiter_config)

        sleep(30)
        manager().quit()


    test_case_001()