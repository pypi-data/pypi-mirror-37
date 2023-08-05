
def target(portal=None, *args, **kwargs):
    print('    portal : ', portal)
    print('    args : ', args)
    print('    kwargs : ', kwargs)

def entry(*args, portal=None, **kwargs):
    print('    portal : ', portal)
    print('    args : ', args)
    print('    kwargs : ', kwargs)

def funny(portal, *args, **kwargs):
    print('    portal : ', portal)
    print('    args : ', args)
    print('    kwargs : ', kwargs)

if '__main__' == __name__:
    kwargs = dict()
    kwargs['kwargs'] = {
        'name':'test',
        'value':'joke'
    }
    kwargs['args'] = ['arg1', 'arg2']
    kwargs['portal'] = 'a transport portal'

    print('1.1 try :')
    target(kwargs)

    print('1.2 try :')
    entry(kwargs)

    print('2.1 try :')
    target(**kwargs)

    print('2.2 try :')
    funny(**kwargs)

    print('3 try :')
    target(kwargs=kwargs)

    print('4 try :')
    target(args=kwargs['args'])


