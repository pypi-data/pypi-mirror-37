from LRC.Common.logger import logger
from LRC.Protocol.v1.BaseProtocol import V1BaseProtocol


class CommandServerProtocol(V1BaseProtocol):

    # interfaces
    def pack_message(self, **kwargs):
        '''
        pack message from answer
        :param respond:     request respond
        :return message:    encoded message to send
        '''
        if 'request' in kwargs:
            raw_message = self._pack_message('request',**kwargs)
        elif 'command' in kwargs:
            raw_message = self._pack_message('command',**kwargs)
        elif 'respond' in kwargs:
            raw_message = self._pack_respond(**kwargs)
        elif 'running_test' in kwargs:
            raw_message = self._pack_running_test_message(**kwargs)
        else:
            logger.info('unknown operation "{}" for LRC command server'.format(kwargs))
            raw_message = ''
        return self.encode(raw_message)

    # functional
    def _pack_message(self, tag, **kwargs):
        '''
        pack request to raw_message
        :param tag:     tag, such as request, command, respond, ...
        :param kwargs:  specifications for a request/command/respond
        :return:        raw_message to send
        '''
        # raw message format : request=name,arg0,arg1,arg2,...
        raw_message = tag + "="
        raw_message += ",name='{}'".format(kwargs[tag])
        del kwargs[tag]
        for k, v in kwargs.items():
            raw_message += self._pack_pair(k, v)
        return raw_message

    def _pack_respond(self, **kwargs):
        '''
        pack request to raw_message
        :param kwargs:  specifications for a request/command/respond
        :return:        raw_message to send
        '''
        # raw message format : request=name,arg0,arg1,arg2,...
        raw_message = "respond="
        raw_message += ",request='{}'".format(kwargs['respond'])
        del kwargs['respond']
        for k, v in kwargs.items():
            raw_message += self._pack_pair(k, v)
        return raw_message


    def _pack_running_test_message(self, **kwargs):
        '''
        pack request to raw_message
        :param kwargs:  specifications for a request/command/respond
        :return:        raw_message to send
        '''
        # raw message format : request=name,arg0,arg1,arg2,...
        raw_message = "running_test="
        raw_message += ",target='{}'".format(kwargs['running_test'])
        del kwargs['running_test']
        for k, v in kwargs.items():
            raw_message += self._pack_pair(k, v)
        return raw_message
