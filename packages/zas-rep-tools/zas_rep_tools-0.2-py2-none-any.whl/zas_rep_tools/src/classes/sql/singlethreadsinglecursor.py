from threading import Thread
#import Queue

#import apsw
from pysqlcipher import dbapi2 as sqlite
from zas_rep_tools.src.utils.custom_exceptions import  ZASCursorError, ZASConnectionError
from zas_rep_tools.src.utils.debugger import p
from  zas_rep_tools.src.classes.sql.basic import BasicConnection, BasicCursor


OperationalError = sqlite.OperationalError
DatabaseError = sqlite.DatabaseError
DataError = sqlite.DataError
InternalError =sqlite.InternalError
IntegrityError = sqlite.IntegrityError
NotSupportedError = sqlite.NotSupportedError
ProgrammingError = sqlite.ProgrammingError
InterfaceError = sqlite.InterfaceError

auto_clear = True


def connect(*args, **kwargs):
        #with self.lock:
        return SingleThreadSingleCursor().connect(*args, **kwargs)


class SingleThreadSingleCursor(BasicConnection):#, sqlite):
    
    def __init__(self, *args, **kwargs):
        #super(type(self), self).__init__(*args,**kwargs)
        self._connection = False
        super(type(self), self).__init__(*args, **kwargs)
        self.active_cursor = False


    def cursor(self, *args, **kwargs):
        self.active_cursor = self._cursor(*args, **kwargs)
        return self.active_cursor

    def _cursor(self, *args, **kwargs):
        if not self._connection:
            raise ZASConnectionError, "No active Connection!"

        if self.active_cursor:
            if auto_clear:
                self.clear()
            else:
                raise ZASCursorError, "Cursor is already exist! Set 'auto_clear'-Option."

        if not self.active_cursor:
            return BasicCursor(self._connection,*args, **kwargs)

    def clear(self):
        if not self.active_cursor:
            raise ZASCursorError ,"Cursor is not exist!"

        del self.active_cursor
        self.active_cursor = None

        


