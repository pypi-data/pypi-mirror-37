class ASingletonTester(object):

    __instance = None

    def __init__(self, name='default'):
        self.name = name

    @classmethod
    def Singleton(cls):
        if cls.__instance is None:
            cls.__instance = ASingletonTester()
        return cls.__instance

    def rename(self, name):
        self.name = name

def __test():
    print(ASingletonTester.Singleton().name)
    ASingletonTester.Singleton().rename('func')
    print(ASingletonTester.Singleton().name)
    ASingletonTester.Singleton().rename('joke')
    print(ASingletonTester.Singleton().name)


if '__main__' == __name__:
    __test()