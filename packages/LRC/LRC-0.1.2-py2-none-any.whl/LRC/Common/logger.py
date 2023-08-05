from __future__ import print_function
from functools import partial
import os

class Logger(object):

    _counts = 0

    def __init__(self, **kwargs):
        # initialize ----------------------------------------------------------------------------------------------
        id = Logger._counts
        Logger._counts += 1
        # public
        self.id                 = id # logger index, indicate the total number of logger
        self.name               = 'not set' # logger name, such as 'default' 'kivy'
        self.stream_id          = None  # stream id, mostly file path
        # protected
        self._id_len            = 1
        self._tag_len           = 8
        self._stream            = None
        self._debug_handler     = print
        self._info_handler      = print
        self._warning_handler   = print
        self._error_handler     = print
        self._formatter         = self._default_formatter
        self._debug_buffer      = list()
        self._info_buffer       = list()
        self._warning_buffer    = list()
        self._error_buffer      = list()
        # initialize raw logger - take care of first time running --------------------------------------------------
        self.set_logger(**kwargs)

    def __del__(self):
        try: # to make this more robust, somehow directly will generate error
            self.flush_buffers()
            self.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush_buffers()
        self.close()

    def close(self):
        if self._stream:
            self._set_raw_logger()
            self._stream.flush()
            self._stream.close()
            self._stream = None

    def buffer_debug(self, *args):
        self._debug_buffer.append(args)

    def buffer_info(self, *args):
        self._info_buffer.append(args)

    def buffer_warning(self, *args):
        self._warning_buffer.append(args)

    def buffer_error(self, *args):
        self._error_buffer.append(args)

    def flush_buffers(self):
        for args in self._debug_buffer:
            self.debug(*args)
        self._debug_buffer.clear()
        for args in self._info_buffer:
            self.info(*args)
        self._info_buffer.clear()
        for args in self._warning_buffer:
            self.warning(*args)
        self._warning_buffer.clear()
        for args in self._error_buffer:
            self.error(*args)
        self._error_buffer.clear()

    def debug(self, *args):
        self._debug_handler(*args)

    def info(self, *args):
        self._info_handler(*args)

    def warning(self, *args):
        self._warning_handler(*args)

    def error(self, *args):
        self._error_handler(*args)

    def set_formatter(self, formatter=None):
        try:
            test_info = formatter('info', 'test') # a test to show error when set this formatter
            self._formatter = formatter
            return
        except:
            self._formatter = self._default_formatter

    def set_logger(self, *, name='default', log_file=None, **kwargs):
        self.close()
        self._set_raw_logger()
        self.name = name
        self.stream_id = log_file

    def _first_run(self, op, *args): # first time info/warning/error is called, is when handlers are set
        # initialize all handlers at first-time running
        if 'kivy' == self.name:
            try:
                import kivy.logger
                self._debug_handler     = kivy.logger.Logger.debug
                self._info_handler      = kivy.logger.Logger.info
                self._warning_handler   = kivy.logger.Logger.warning
                self._error_handler     = kivy.logger.Logger.error
                self.name = 'kivy'
                self.info('logger : set to kivy logger')
            except ImportError:
                self._set_default_logger()
                self.name = 'default'
                self.error('logger : can not import kivy logger(kivy not installed ???), set to default logger')
            except Exception as err:
                self._set_default_logger()
                self.name = 'default'
                self.error('logger : got error when import kivy logger, set to default logger.')
                self.error('logger : error message : {}'.format(err))
        elif 'default' == self.name:
            self._set_default_logger()
        else:
            unrecognized_logger = self.name
            self._set_default_logger()
            self.info('logger : unrecognized logger {}, set to default.'.format(unrecognized_logger))
        # answer first call
        try:
            getattr(self, op)(*args)
        except Exception as err:
            raise Exception('first call {} for logger failed with message : {}.'.format(op, err))

    def _set_raw_logger(self, *args, **kwargs):
        self._debug_handler     = partial( self._first_run, 'debug')
        self._info_handler      = partial( self._first_run, 'info')
        self._warning_handler   = partial( self._first_run, 'warning')
        self._error_handler     = partial( self._first_run, 'error')

    def _set_default_logger(self):
        # try to parse log stream id
        log_file = self.stream_id
        if log_file is None:
            import time
            now = time.localtime()
            log_file = 'log_%04d-%02d-%02d_%02d%02d%02d.log' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            log_file = os.path.join('logs', log_file)
        log_file = os.path.abspath(log_file)
        try:
            log_file_dir = os.path.dirname(log_file)
            if not os.path.exists(log_file_dir):
                os.mkdir(log_file_dir)
            self.stream_id = log_file
            self._stream = open(log_file, 'a')
        except Exception as err:
            print('[error  ] error while opening log_file, got : {}.'.format(err))
        # set default handlers
        if self._stream:
            self._set_default_handlers_with_stream()
            self.info('starting logging into stream : {}'.format(self.stream_id))
        else:
            self._set_default_handlers()
        self.name = 'default'

    def _default_formatter(self, tag, *args):
        _format = '[%{}s][%-{}s]'.format(self._id_len, self._tag_len)
        return _format % (self.id, tag) + ' '.join(args)

    def _set_default_handlers(self):
        self._debug_handler     = self._default_debug_handler
        self._info_handler      = self._default_info_handler
        self._warning_handler   = self._default_warning_handler
        self._error_handler     = self._default_error_handler

    def _set_default_handlers_with_stream(self):
        self._debug_handler     = self._default_debug_handler_with_stream
        self._info_handler      = self._default_info_handler_with_stream
        self._warning_handler   = self._default_warning_handler_with_stream
        self._error_handler     = self._default_error_handler_with_stream

    def _default_debug_handler(self, *args):
        print(self._formatter('DEBUG', *args))

    def _default_info_handler(self, *args):
        print(self._formatter('info', *args))

    def _default_warning_handler(self, *args):
        print(self._formatter('warning', *args))

    def _default_error_handler(self, *args):
        print(self._formatter('error', *args))

    def _default_debug_handler_with_stream(self, *args):
        msg = self._formatter('DEBUG', *args)
        print(msg)
        self._stream.write(msg)
        self._stream.write('\n')
        self._stream.flush()

    def _default_info_handler_with_stream(self, *args):
        msg = self._formatter('info', *args)
        print(msg)
        self._stream.write(msg)
        self._stream.write('\n')
        self._stream.flush()

    def _default_warning_handler_with_stream(self, *args):
        msg = self._formatter('warning', *args)
        print(msg)
        self._stream.write(msg)
        self._stream.write('\n')
        self._stream.flush()

    def _default_error_handler_with_stream(self, *args):
        msg = self._formatter('error', *args)
        print(msg)
        self._stream.write(msg)
        self._stream.write('\n')
        self._stream.flush()


logger = Logger()


if '__main__' == __name__: # test logger

    def _test_case_000():
        logger.debug('test debug')
        logger.info('test info')
        logger.warning('test warning')
        logger.error('test error')

    def _test_case_001():
        _logger = Logger(log_file=r'logs\test.log')
        _logger.debug('test debug')
        _logger.info('test info')
        _logger.warning('test warning')
        _logger.error('test error')
        _logger.close()
        _logger.info('after closed')

    def _test_case_002():
        logger.set_logger(name='default', log_file='logs\\take_your_time.log')
        logger.debug('test debug')
        logger.info('test info')
        logger.warning('test warning')
        logger.error('test error')

    def _test_case_003():
        logger.set_logger(name='default', log_file='logs\\take_your_time.log')
        logger.info('test default formatter')
        def formatter(tag, *args):
            return '{} -- {}'.format(tag, ' * '.join(args))
        logger.set_formatter(formatter)
        logger.info('test default formatter', 'cannot be true')

    _test_case_003()
    pass