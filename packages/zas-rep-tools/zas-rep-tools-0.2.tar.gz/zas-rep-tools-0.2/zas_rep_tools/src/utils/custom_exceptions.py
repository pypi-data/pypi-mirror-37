

class ValidationError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(ValidationError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors


class ZASCursorError(Exception):
    '''
    test
    '''

class ZASConnectionError(Exception):
    '''
    test
    '''


class DBHandlerError(Exception):
    '''
    test
    '''


class ProcessError(Exception):
    '''
    test
    '''


class StackTraceBack(Exception):
    '''
    test
    '''


class ErrorInsertion(Exception):
    '''
    test
    '''
class ThreadsCrash(Exception):
    '''
    test
    '''


    

