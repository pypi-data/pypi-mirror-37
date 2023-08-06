#from threading import Thread
import threading
import Queue
import inspect

#import apsw
from pysqlcipher import dbapi2 as sqlite
from zas_rep_tools.src.utils.custom_exceptions import  ZASCursorError, ZASConnectionError
from zas_rep_tools.src.utils.debugger import p
from  zas_rep_tools.src.classes.sql.basic import BasicConnection, BasicCursor
from zas_rep_tools.src.classes.basecontent import BaseContent


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
        #p(kwargs, "1**kwargs", c="r")
        
        return MultiThreadMultiCursor(*args, **kwargs).connect(*args, **kwargs)


class MultiThreadMultiCursor(BaseContent,BasicConnection,threading.Thread):#, sqlite):
    def __init__(self, *args, **kwargs):
        #p(kwargs, "2.1**kwargs", c="r")
        super(type(self), self).__init__( **kwargs)
        #p(kwargs, "2.2**kwargs", c="r")
        #BaseContent.__init__(self,*args, **kwargs)
        #p(kwargs, "2.2**kwargs", c="r")
        #BasicConnection.__init__(self,*args, **kwargs)
        threading.Thread.__init__(self)
        self.lock_connection = threading.Lock()
        #self.active_cursor = False
        self.daemon = True
        self.start()
        #p("NEW DB Class was init {}".format(inspect.stack()[-18][3]))   
        #5/0

    def connect(self, *args, **kwargs):
        #p(args, "3args")
        #p(kwargs, "3kwargs")
        isolation_level = kwargs.get("isolation_level", None)
        check_same_thread = kwargs.get("check_same_thread", None)
        kargs = {}
        if isolation_level != None: kargs["isolation_level"] = isolation_level
        if check_same_thread != None: kargs["check_same_thread"] = check_same_thread

        if not self._connection:
            self._connection = sqlite.connect(*args, **kargs)
            return self
        else:
            raise ZASConnectionError, "Connection is already exist!"     
        

    def _cursor(self, *args, **kwargs):
        if not self._connection:
            raise ZASConnectionError, "No active Connection!"

        return MultiCursor(self._connection,self.lock_connection,*args, **kwargs)

    #lock = threading.Lock()


# class ThreadSafeConnection(self):
#     def __init(*args, **kwargs):
#         self._connection = sqlite.connect(*args, **kwargs)
#         self.lock_connection = threading.Lock()






class MultiCursor(BasicCursor,threading.Thread):
    def __init__(self, connection,conn_lock,*args, **kwargs):
        threading.Thread.__init__(self)
        self.connection = connection
        self.lock_connection = conn_lock
        self.cursor = self.connection.cursor(*args, **kwargs)
        self.daemon = True 
        self.start()


    # def __init__(self, *args, **kwargs):
    #     super(type(self), self).__init__(*args, **kwargs)
    #     BasicCursor.__init__(self,*args, **kwargs)
    #     threading.Thread.__init__(self)
    #     #self.active_cursor = False
    #     self.daemon = True 
    #     self.lock_cursor = threading.Lock()
    #     self.start()
        #p("CURSOR WAS INIT {}".format(inspect.stack()[-18][3]), c="b")   


    def execute(self,sql,*args, **kwargs):
        #print self, "67"
        #self.cursor = self.connection.cursor()
        #p(locals())
        with self.lock_connection:
            self._check_cursor_existenz()
            self.cursor.execute(sql,*args, **kwargs)
            self.join()
            return self


    def executemany(self,sql,*args, **kwargs):
        #p((sql, args[0]))
        with self.lock_connection:
            self._check_cursor_existenz()
            self.cursor.executemany(sql,*args, **kwargs)
            self.join()
            return self


    def executescript(self,sql,*args, **kwargs):
        with self.lock_connection:
            self._check_cursor_existenz()
            self.cursor.executescript(sql,*args, **kwargs)
            self.join()
            return self


