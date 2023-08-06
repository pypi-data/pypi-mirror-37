from threading import Thread
import Queue
import inspect
import time
#import apsw
from pysqlcipher import dbapi2 as sqlite
from zas_rep_tools.src.utils.custom_exceptions import  ZASCursorError, ZASConnectionError
from zas_rep_tools.src.utils.debugger import p

OperationalError = sqlite.OperationalError
DatabaseError = sqlite.DatabaseError
DataError = sqlite.DataError
InternalError =sqlite.InternalError
IntegrityError = sqlite.IntegrityError
NotSupportedError = sqlite.NotSupportedError
ProgrammingError = sqlite.ProgrammingError
InterfaceError = sqlite.InterfaceError



class BasicConnection(object):#, sqlite):
    
    def __init__(self,*args, **kwargs):
        self._connection = False
        #self._init_cursors = []

    # def __del__(self):
    #     #p(self._init_cursors, "init_cursors")
    #     #p("CONNECTION WAS DESTRUCTED", c="r")
    def __del__(self):
        try:
            self._connection.close()
            del self._connection
        except:
            pass


    def connect(self, *args, **kwargs):
        if not self._connection:
            self._connection = sqlite.connect(*args, **kwargs)
            #return Status(status=True)
            #return None
            #p("NEW CONNECTION WAS ESTABL. {}, {}".format(inspect.stack()[-18][3], args[0]), c="g")
            return self
        else:
            raise ZASConnectionError, "Connection is already exist!"


    def cursor(self, *args, **kwargs):
        c = self._cursor(*args, **kwargs)
        #self._init_cursors.append(c)
        return c


    def _cursor(self, *args, **kwargs):
        if not self._connection:
            raise ZASConnectionError, "No active Connection!"

        return BasicCursor(self._connection,*args, **kwargs)


    def enable_load_extension(self,*args, **kwargs):
        self._connection.enable_load_extension(*args, **kwargs)


    def rollback(self,*args, **kwargs):
        self._connection.rollback(*args, **kwargs)


    def create_function(self,*args, **kwargs):
        self._connection.create_function(*args, **kwargs)


    def create_aggregate(self,*args, **kwargs):
        self._connection.create_aggregate(*args, **kwargs)


    def create_collation(self,*args, **kwargs):
        self._connection.create_collation(*args, **kwargs)



    def interrupt(self,*args, **kwargs):
        self._connection.interrupt(*args, **kwargs)



    def set_authorizer(self,*args, **kwargs):
        self._connection.set_authorizer(*args, **kwargs)


    def set_progress_handler(self,*args, **kwargs):
        self._connection.set_progress_handler(*args, **kwargs)

    def load_extension(self,*args, **kwargs):
        self._connection.load_extension(*args, **kwargs)


    def close(self):
        if not self._connection:
            raise ZASConnectionError, "No active Connection!"
        self._connection.close()
        self._connection = False  


    def commit(self):
        if not self._connection:
            raise ZASConnectionError, "No active Connection!"

        self._connection.commit()      



    @property
    def row_factory(self):
        return self._connection.row_factory


    @row_factory.setter
    def row_factory(self, value):
        self._connection.row_factory = value


    @property
    def text_factory(self):
        return self._connection.text_factory


    @text_factory.setter
    def text_factory(self, value):
        self._connection.text_factory = value


    @property
    def total_changes(self):
        return self._connection.total_changes


    @total_changes.setter
    def total_changes(self, value):
        self._connection.total_changes = value


    @property
    def iterdump(self):
        return self._connection.iterdump


    @iterdump.setter
    def iterdump(self, value):
        self._connection.iterdump = value


    @property
    def isolation_level(self):
        return self._connection.isolation_level


    @isolation_level.setter
    def isolation_level(self, value):
        self._connection.isolation_level = value

        
       
        


class BasicCursor(object):
    def __init__(self, connection,*args, **kwargs):
        self.connection = connection
        self.cursor = self.connection.cursor(*args, **kwargs)

    def __del__(self):
        try:
            self.cursor.close()
        except:
            pass
        #p("CURSOR WAS DESTRUCTED", c="m")


    def _check_cursor_existenz(self):
        if not self.cursor:
            raise ZASCursorError, "Cursor to Connection not exist or was deleted. (Check 'auto_clear'-Option)"


    def fetchone(self):
        self._check_cursor_existenz()
        elem = self.cursor.fetchone()
        return elem


    def fetchmany(self,size_to_fetch):
        self._check_cursor_existenz()
        for row in  self.cursor.fetchmany(size_to_fetch):
            if row:
                yield row 
            else:
                yield None
                return   

    def fetchall(self):
        self._check_cursor_existenz()
        elem = self.cursor.fetchall()
        return elem


    def _is_fetchable(self,sql):
        self._check_cursor_existenz()
        sql = sql.lower()
        #p(sql)
        if "select" in sql or "pragma" in sql:
            return True
        else:
            return False



    def execute(self,sql,*args, **kwargs):
        self._check_cursor_existenz()
        self.cursor.execute(sql,*args, **kwargs)
        return self


    def executemany(self,sql,*args, **kwargs):
        self._check_cursor_existenz()
        self.cursor.executemany(sql,*args, **kwargs)
        return self


    def executescript(self,sql,*args, **kwargs):
        self._check_cursor_existenz()
        self.cursor.executescript(sql,*args, **kwargs)
        return self


    @property
    def rowcount(self):
        self._check_cursor_existenz()
        return self.cursor.rowcount
    
    @property
    def lastrowid(self):
        self._check_cursor_existenz()
        return self.cursor.lastrowid


    @property
    def description(self):
        self._check_cursor_existenz()
        return self.cursor.description



