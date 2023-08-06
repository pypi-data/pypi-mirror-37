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


auto_clear = True


def connect(*args, **kwargs):
        #with self.lock:
        return SingleThreadMultiCursor().connect(*args, **kwargs)


class SingleThreadMultiCursor(BasicConnection):
    

        


