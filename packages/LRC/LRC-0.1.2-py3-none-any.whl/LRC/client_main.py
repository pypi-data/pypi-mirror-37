def main():
    import sys
    if '-h' in sys.argv or '--help' in sys.argv:
        print(_help_str())
        exit()
    if '--version' in sys.argv:
        from LRC.Common.info import version
        print('LRC version {}'.format(version))
        exit()
    verbose = False
    if '--verbose' in sys.argv:
        verbose = True

    import os
    from kivy.config import Config
    Config.read(os.path.join('Client', 'android.ini'))

    from LRC.Common.logger import logger
    from LRC.Client.ClientUI import ClientUI

    logger.set_logger(name='kivy')

    # start application
    ClientUI(verbose=verbose).run()


def _help_str():
    return '''
LRC server
[Usage]
    lrcwaiter

[options]
    --help, -h              show this help info
    --version               show LRC version
    --verbose               show more information in log

[more]
    for more infomation, see https://github.com/davied9/LANRemoteController
'''


if '__main__' == __name__:
    main()
