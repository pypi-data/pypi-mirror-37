from LRC.Protocol.BaseProtocol import BaseProtocol
from LRC.Common.logger import logger
import re

class V1BaseProtocol(BaseProtocol):
    '''
    V1BaseProtocol defines common protocol for v1 of LRC protocol
    '''

    _tag_exp = re.compile(r'^(\w+)\=')
    _arg_key_exp = re.compile(r'\,\w+=')

    def __init__(self, **kwargs):
        super(V1BaseProtocol, self).__init__(**kwargs)

    # interface
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
    def _unpack_tag(self, message):
        try:
            tag = self._tag_exp.findall(message)[0]
            return tag
        except:
            return ''

    def _unpack_args(self, message):
        args=dict()
        ranges = []

        for m in self._arg_key_exp.finditer(message):
            ranges.append(m.span())

        N = len(ranges)
        for i in range(N):
            r = ranges[i]
            if N-1 == i: # last value
                k = message[r[0]+1:r[1]-1]
                v = message[r[1]:len(message)]
            else:
                r_next = ranges[i+1]
                k = message[r[0]+1:r[1]-1]
                v = message[r[1]:r_next[0]]
            try:
                v = eval(v)
            except Exception as err:
                logger.error('V1BaseProtocol : can not evaluate value from "{}" : {}'.format(v, err.args))
            args[k] = v

        return args

    def _pack_pair(self, k, v):
        if str is type(v):
            return ",{}='{}'".format(k, v)
        else:
            return ",{}={}".format(k, v)

if '__main__' == __name__:
    test_str = 'controller=,name="controller",controller={"copy dump": {"test a": ["left alt", "L"]}},joke="do i know you",yahoo={"copy dump": {"test b": ["right alt", "j]}}'
    protocol = V1BaseProtocol()

    print('str = {}'.format(test_str))

    test_str = test_str.encode(protocol.encoding)
    tag, kwargs = protocol.unpack_message(test_str)

    print('tag = {}'.format(tag))
    n = 0
    print('kwargs = ')
    for k, v in kwargs.items():
        print('    volume {}'.format(n))
        print('        k : {}'.format(k))
        print('        v : {}(type) {}'.format(type(v), v))
        n += 1
