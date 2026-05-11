class ObjectDoesNotExist(BaseException):
    pass

class ObjectAlreadyExists(BaseException):
    pass

class ServerDown(BaseException):
    pass

class ServerBadResponse(BaseException):
    pass