class BuessExpection(Exception):

    def __index__(self,reason):
        self.__reason  = reason
        pass

    def __str__(self):
        print(self.__reason)
