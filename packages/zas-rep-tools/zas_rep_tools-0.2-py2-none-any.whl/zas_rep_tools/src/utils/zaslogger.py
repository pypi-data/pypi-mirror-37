import logging
import datetime
import time
import os
import sys
from collections import defaultdict
import codecs
import traceback
import inspect
import gc
#import logging.Handler

from logutils.colorize import ColorizingStreamHandler
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.custom_exceptions import StackTraceBack
#from zas_rep_tools.src.utils.helpers import stack

#ZASLogger._root_logger

def clear_logger():
    del ZASLogger._root_logger
    del ZASLogger._handlers
    del ZASLogger._loggers
    ZASLogger._root_logger = None
    ZASLogger._creation_day = None
    ZASLogger._creation_time = None
    ZASLogger._loggers = defaultdict(dict)
    ZASLogger._handlers = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    ZASLogger._event_folder = None
    ZASLogger._save_lower_debug = False
    ZASLogger._save_debug = False

class ZASLogger(object):
    _root_logger = None
    _creation_day = None
    _creation_time = None
    _loggers = defaultdict(dict)
    _handlers = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    _event_folder = None
    _save_lower_debug = False
    _save_debug = False
    _set_functon_name_as_event_name = False

    #p(_save_lower_debug, "_save_lower_debug")

    # def __new__(self):
    #   '''
    #   __new__ is the first step of instance creation. It's called first, and is responsible for returning a new instance of your class. In contrast, __init__ doesn't return anything; it's only responsible for initializing the instance after it's been created.
    #   '''
    #   if ZASLogger._root_logger is None:
    #       ZASLogger._root_logger = logging.getLogger()
    #   return ZASLogger._root_logger
    #   #pass

    def __init__(self, logger_name, level=logging.INFO,  folder_for_log="logs", logger_usage=True, save_logs=False):
        #p(ZASLogger._set_functon_name_as_event_name,c="r")
        folder_for_log = folder_for_log if folder_for_log else "logs"

        # Init Root Logger
        if ZASLogger._root_logger is None:
            ZASLogger._root_logger = logging.getLogger()
            self._set_filters(ZASLogger._root_logger)

        self._logger_name = logger_name
        self._level = level
        self._folder_for_log = folder_for_log
        self._logger_usage = logger_usage
        self._save_logs = save_logs

        if self._logger_usage:
            self.update_root_logger()
        self._formatter = logging.Formatter(u'%(asctime)7s [%(name)s] %(threadName)11s:{%(sthread)s} [%(funcName)s()]  %(levelname)5s \n %(message)s \n', "%H:%M:%S")
        self._logger = None
        self.day_folder = None
        self.time_folder = None
        #ZASLogger._event_folder = None
        self.level_functions = {}

        if self._logger_usage:
            self._set_day()
            self._set_time()
            self._set_dirs()

    #def __del__(self):


    def _close_handlers(self):
        if ZASLogger._handlers[self._logger_name]:
            for handler_name, handler in ZASLogger._handlers[self._logger_name].items():
                #p((handler_name), c="r")
                if handler_name == 'FileHandler':
                    for file_handler in handler.values():
                        #p((file_handler), c="r")
                        file_handler.flush()
                        file_handler.close()
                        del file_handler
                else:
                    handler.flush()
                    handler.close()
                    del handler
            del ZASLogger._handlers[self._logger_name]
            #del self
            gc.collect()     


    def update_root_logger(self):
        #p((self._logger_name,self._level,ZASLogger._root_logger.level),c="m")
        if self._level < ZASLogger._root_logger.level:
            ZASLogger._root_logger.setLevel(self._level)
            #p((self._logger_name,self._level,ZASLogger._root_logger.level),c="r")
            #p(ZASLogger._handlers)
        if self._save_logs:
            ZASLogger._root_logger.setLevel(1)
            #p((self._logger_name,self._level,ZASLogger._root_logger.level),c="r")


        
    #def _init_logger(self):


    def getLogger(self):
        #p((self._logger_usage, self._logger_name), c="m")
        self._set_usage()
        self._logger = logging.getLogger(self._logger_name)
        if not self._logger_usage: self._logger.handlers = []
        ZASLogger._loggers[self._logger_name] = self._logger
        self._set_filters()
        self._add_additional_levels()
        if self._logger_usage:
            self._add_stream_handler()
            if self._save_logs:
                self._makedirs()
                self._add_multihandler()
                self._add_default_file_handlers()
        #p(self._logger.handlers)
        return self._logger
        


    def _set_usage(self):
        if self._logger_usage:
            logging.disable(logging.NOTSET)
        else:
            logging.disable(sys.maxint)
            self._root_logger.setLevel(sys.maxint)
            ZASLogger._handlers[self._logger_name]["StreamHandler"] = []
            ZASLogger._handlers[self._logger_name]["FileHandler"] = defaultdict(lambda:[])
            ZASLogger._handlers["MultiHandler"] = []
            #p(self._logger.handlers, "self._logger.handlers")
            # if self._logger.handlers:
            #     pass
            #self._logger.setLevel(100)

    def _clear(self):
        clear_logger()

    def _set_dirs(self):
        self.day_folder = os.path.join(self._folder_for_log,ZASLogger._creation_day)
        self.time_folder = os.path.join(self.day_folder,ZASLogger._creation_time)


    def _makedirs(self):
        if self._save_logs and self._logger_usage:
            if not ZASLogger._event_folder or not os.path.isdir(ZASLogger._event_folder):
                i = 0
                status = True
                func_name = None

                #p((self._logger_name,self._level,ZASLogger._set_functon_name_as_event_name, self._save_logs),c="m")
                if  ZASLogger._set_functon_name_as_event_name:
                    status2= True
                    st = inspect.stack()
                    stack_index = -15
                    while status2:
                        #p(stack_index,"stack_index",c="m")
                        try:
                            current_stack_depth = st[stack_index]
                            func_name = current_stack_depth[3]
                            #p((stack_index,func_name),"func_name", c="r")
                            if "test_" in func_name.lower():
                                module_name = os.path.splitext(os.path.basename(current_stack_depth[1]))[0]
                                status2 = False
                                break
                            else:
                                if stack_index < -25:
                                    p("FunctionNameError: It wasn't possible to find FunctionName of the TestCase.", "ERROR", c="r")
                                    #sys.exit()
                                    #ZASLogger._root_logger.error("FunctionNameError: It wasn't possible to find FunctionName of the TestCase.".format())
                                    #sys.exit()
                                    func_name = "none"
                                    module_name = "none"
                                    status2 = False
                                    break
                                stack_index-=1
                                #continue
                        except:
                            p("FunctionNameError: (IndexOutOfList) It wasn't possible to find FunctionName of the TestCase.", "ERROR", c="r")
                            func_name = "none"
                            module_name = "none"
                            status2 = False

                    temp_folder = "{}__{}".format(module_name,func_name)
                    #ZASLogger._event_folder = new_file_name
                    clear_path = os.path.join(self.day_folder,temp_folder)

                else:
                    #temp_folder = self.time_folder
                    clear_path = self.time_folder
                    #temp_path = clear_path

                temp_path = clear_path
                while status:
                    i += 1
                    if not os.path.isdir(temp_path):
                        os.makedirs(temp_path)
                        ZASLogger._event_folder = temp_path
                        status = False
                    else:
                        temp_path = "{}--{}".format(clear_path,i)



    def _set_day(self, reset=False):
        if (ZASLogger._creation_day is None) or reset==True:
            ZASLogger._creation_day = datetime.date.today().strftime("%Y_%m_%d")

    def _set_time(self, reset=False):
        if ZASLogger._creation_time is None or reset==True:
            ZASLogger._creation_time = time.strftime('%H_%M')




    def _set_filters(self, logger=None):
        #p(logger, "1logger_in_filt")
        logger = logger if logger else self._logger
        #p(logger, "2logger_in_filt")
        #d = DuplicateFilter()
        f = ContextFilter()
        #self._logger.addFilter(d)
        logger.addFilter(f)


    def _check_stream_hander_uniqness(self, current_handler):
        i = 0
        indexes_to_delete = []
        #print "befove", self._logger.handlers
        for hndlr in self._logger.handlers:
            if type(current_handler).__name__ == type(hndlr).__name__:
                indexes_to_delete.append(i)
            i+=0
        for indx in indexes_to_delete:
            #print self._logger.handlers[indx]
            del self._logger.handlers[indx]

    def handlers(self):
        output= defaultdict(list)
        for hndl in self._logger.handlers:
            output[type(hndl).__name__].append(hndl.level)
        return output



    def _add_stream_handler(self):
        # Create a logger, with the previously-defined handler
        if not ZASLogger._handlers[self._logger_name]["StreamHandler"] or ZASLogger._handlers[self._logger_name]["StreamHandler"].level > self._level:
            
            # ((self._logger_name, self._level))
            handler = RainbowLoggingHandler(sys.stdout)
            self._check_stream_hander_uniqness(handler)
            handler.setLevel(self._level)
            #if self._level == logging.ERROR:
            #    handler.addFilter(SealedOffFilter(logging.ERROR))
            ZASLogger._handlers[self._logger_name]["StreamHandler"] = handler
            self._logger.addHandler(handler)
            self._logger.low_debug("StreamHandler for '{}'-level in '{}'-Logger was added.".format(self._level, self._logger_name))

        else:
            self._logger.low_debug("StreamHandler for '{}'-level in '{}'-Logger is already exist. New Handler wasn't added.".format(self._level, self._logger_name))


    def _add_default_file_handlers(self):
        self._add_file_handler(logging.CRITICAL, "critical", sealed_off=False)
        self._add_file_handler(logging.ERROR, "error", sealed_off=True)
        self._add_file_handler(logging.WARNING, "warning", sealed_off=True)
        self._add_file_handler(logging.INFO, "info", sealed_off=False)
        if self._level <= 10 or ZASLogger._save_debug:
            self._add_file_handler(logging.DEBUG, "debug", sealed_off=False)

                    #elif level_num==10:
                    #    if ZASLogger._save_debug:
                    #        self._add_file_handler(level_num, level_name.lower(), sealed_off=sealed_off)
                    


    def _add_file_handler(self, level, fname, sealed_off=True):
        if not ZASLogger._handlers[self._logger_name]["FileHandler"][level]:
            if self._save_logs:
                handler = logging.FileHandler(os.path.join(ZASLogger._event_folder, "{}.log".format(fname)) ,mode="a", encoding="utf-8", delay=True)
                handler.setLevel(level)
                handler.setFormatter(self._formatter)
                self._check_file_hander_uniqness(handler)
                if sealed_off:
                    handler.addFilter(SealedOffFilter(level))
                ZASLogger._handlers[self._logger_name]["FileHandler"][level] = handler
                self._logger.addHandler(handler)
                self._logger.low_debug("FileHandler for '{}'-level in '{}'-Logger was added.".format(level, self._logger_name))
        else:
            self._logger.low_debug("FileHandler for '{}'-level in '{}'-Logger is already exist. New Handler wasn't added.".format(level, self._logger_name))


    def _add_multihandler(self,sealed_off=True):
        multi_handler = MultiHandler(ZASLogger._event_folder)
        multi_handler.setLevel(self._level)
        multi_handler.setFormatter(self._formatter)
        if not ZASLogger._handlers["MultiHandler"]:
            ZASLogger._handlers["MultiHandler"] = multi_handler
            ZASLogger._root_logger.addHandler(multi_handler)
            self._logger.low_debug("MultiHandler for '{}'-level was added. ".format(self._level))
        else:
            if ZASLogger._handlers["MultiHandler"].level > self._level:
                old_level = ZASLogger._handlers["MultiHandler"].level
                ZASLogger._handlers["MultiHandler"] = multi_handler
                #p(ZASLogger._root_logger.handlers, c="m")
                ZASLogger._root_logger.handlers = []
                ZASLogger._root_logger.addHandler(multi_handler)
                #p(ZASLogger._root_logger.handlers, c="m")
                self._logger.low_debug("MultiHandler for '{}'-level is already exist and was changed to '{}'-level. ".format(old_level,self._level ))






    def _check_file_hander_uniqness(self, current_handler):
        i = 0
        indexes_to_delete = []
        #print "befove", self._logger.handlers
        for hndlr in self._logger.handlers:
            if type(current_handler).__name__ == type(hndlr).__name__:
                if current_handler.level ==hndlr.level:
                    indexes_to_delete.append(i)
            i+=0
        for indx in indexes_to_delete:
            #print self._logger.handlers[indx]
            del self._logger.handlers[indx]





    def function_builder(self,level_name,level_num, logger_name,logger, sealed_off=True, **kws):
        def current_level_logger(message, *args, **kws):
            l = False
            try:
                #stck = inspect.stack()
                l = ZASLogger._handlers[logger_name].get("FileHandler", False).get(level_num, False)
            except:
                l = False

            if l == False:
                if self._save_logs and self._logger_usage:
                    self._makedirs()
                    if level_num==9:
                        if ZASLogger._save_lower_debug:
                            self._add_file_handler(level_num, level_name.lower(), sealed_off=sealed_off)
                    else:
                        self._add_file_handler(level_num, level_name.lower(), sealed_off=sealed_off)


            logger.log(level_num, message, **kws)
        return current_level_logger


    def _set_level(self, level_name, level_num, sealed_off=True):
        '''
        if not ZASLogger._handlers["FileHandler"][level_num]:
            self._add_file_handler(level_num, level_name.lower(), sealed_off=True)
        '''
        #logger = self._logger
        self._add_level(level_name.upper(), log_num=level_num, custom_log_module=logging)
        self.level_functions[level_name.lower()] = self.function_builder(level_name,level_num, self._logger_name,self._logger, sealed_off=sealed_off)
        # f="""def {}(message, *args, **kws):
        #     logger.log({}, message)
        # """.format(level_name.lower(), level_num)
        # exec(f)
        #p(self.level_functions)
        var = """self._logger.{0} = self.level_functions['{0}']""".format(level_name.lower())
        exec(var)


    def _add_additional_levels(self):
        self._set_level("low_debug", 9, sealed_off=False)
        self._set_level("outsorted_stats", 8)
        self._set_level("outsorted_corpus", 7)
        self._set_level("outsorted_reader", 6)
        self._set_level("error_insertion", 55)
        self._set_level("healed", 4)
        self._set_level("status", 3)
        self._set_level("test", 2)
        self._set_level("settings", 1)



    def _add_level(self,log_name,custom_log_module=None,log_num=None,
                    log_call=None, lower_than=None, higher_than=None,
                    same_as=None, verbose=True):
        '''
        Function to dynamically add a new log level to a given custom logging module.
        <custom_log_module>: the logging module. If not provided, then a copy of
            <logging> module is used
        <log_name>: the logging level name
        <log_num>: the logging level num. If not provided, then function checks
            <lower_than>,<higher_than> and <same_as>, at the order mentioned.
            One of those three parameters must hold a string of an already existent
            logging level name.
        In case a level is overwritten and <verbose> is True, then a message in WARNING
            level of the custom logging module is established.
        '''
        if custom_log_module is None:
            import imp
            custom_log_module = imp.load_module('custom_log_module',
                                                *imp.find_module('logging'))
        log_name = log_name.upper()
        def cust_log(par, message, *args, **kws):
            # Yes, logger takes its '*args' as 'args'.
            if par.isEnabledFor(log_num):
                par._log(log_num, message, args, **kws)
        available_level_nums = [key for key in custom_log_module._levelNames
                                if isinstance(key,int)]

        available_levels = {key:custom_log_module._levelNames[key]
                                 for key in custom_log_module._levelNames
                                if isinstance(key,str)}
        if log_num is None:
            try:
                if lower_than is not None:
                    log_num = available_levels[lower_than]-1
                elif higher_than is not None:
                    log_num = available_levels[higher_than]+1
                elif same_as is not None:
                    log_num = available_levels[higher_than]
                else:
                    raise Exception('Infomation about the '+
                                    'log_num should be provided')
            except KeyError:
                raise Exception('Non existent logging level name')
        # if log_num in available_level_nums and verbose:
        #     custom_log_module.warn('Changing ' +
        #                               custom_log_module._levelNames[log_num] +
        #                               ' to '+log_name)
        custom_log_module.addLevelName(log_num, log_name)

        if log_call is None:
            log_call = log_name.lower()
        exec('custom_log_module.Logger.'+eval('log_call')+' = cust_log', None, locals())
        return custom_log_module





# Create a special logger that logs to per-thread-name files
# I'm not confident the locking strategy here is correct, I think this is
# a global lock and it'd be OK to just have a per-thread or per-file lock.
class MultiHandler(logging.Handler):
    def __init__(self, dirname):
        super(MultiHandler, self).__init__()
        self.files = {}
        self.dirname = dirname
        if not os.access(dirname, os.W_OK):
            raise Exception("Directory %s not writeable" % dirname)

    def flush(self):
        self.acquire()
        try:
            for fp in self.files.values():
                fp.flush()
        finally:
            self.release()

    def _get_or_open(self, key):
        "Get the file pointer for the given key, or else open the file"
        self.acquire()
        try:
            if self.files.has_key(key):
                return self.files[key]
            else:
                fp = codecs.open(os.path.join(self.dirname, "%s.log" % key), "a", encoding="utf-8")
                self.files[key] = fp
                return fp
        finally:
            self.release()

    def emit(self, record):
        # No lock here; following code for StreamHandler and FileHandler
        try:
            #p(record)
            if "sthread" not in record.__dict__:
                record.sthread = str(record.thread)[10:] if len(
                                str(record.thread)) > 10 else str(record.thread)

            fp = self._get_or_open(record.threadName)
            msg = self.format(record)
            fp.write('%s\n' % msg.encode("utf-8"))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            #p(record.__dict__)
            self.handleError(record)



class SealedOffFilter(object):
    '''
    to set records just for this level and ignore reocrds from other higher levels
    '''
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level



class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """
    #current_level_logger
    def filter(self, record):
        #p(record.__dict__,"1record.__dict__" )
        record.sthread = str(record.thread)[10:] if len(
                        str(record.thread)) > 10 else str(record.thread)
        if record.funcName == "current_level_logger":
            try:
                record.funcName = traceback.extract_stack()[-8][2]
            except:
                record.funcName = "UNKNOWN_FUNKTION"
        return True



class DuplicateFilter(logging.Filter):

    def filter(self, record):
        # add other fields if you need more granular comparison, depends on your app
        #p(current_log)
        current_log = (record.module, record.levelno, record.msg)
        #p(getattr(self, "last_log", None), c="r")
        if record.msg != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False



class RainbowLoggingHandler(ColorizingStreamHandler):
    """ A colorful logging handler optimized for terminal debugging aestetichs.

    - Designed for diagnosis and debug mode output - not for disk logs

    - Highlight the content of logging message in more readable manner

    - Show function and line, so you can trace where your logging messages
      are coming from

    - Keep timestamp compact

    - Extra module/function output for traceability

    The class provide few options as member variables you
    would might want to customize after instiating the handler.
    """



    date_format = "%H:%M:%S"

    #: How many characters reserve to function name logging
    who_padding = 22

    #: Show logger name
    show_name = True

    # Define color for message payload
    level_map = {
        logging.DEBUG: (None, 'cyan', False),
        logging.INFO: (None, 'white', True),
        logging.WARNING: ("yellow", 'white', True),
        logging.ERROR: ( 'red', "white", True),
        logging.CRITICAL: ('magenta', 'white', True),
    }



    def get_color(self, fg=None, bg=None, bold=False):
        """
        Construct a terminal color code

        :param fg: Symbolic name of foreground color

        :param bg: Symbolic name of background color

        :param bold: Brightness bit
        """
        params = []
        if bg in self.color_map:
            params.append(str(self.color_map[bg] + 40))
        if fg in self.color_map:
            params.append(str(self.color_map[fg] + 30))
        if bold:
            params.append('1')

        color_code = ''.join((self.csi, ';'.join(params), 'm'))

        return color_code

    def colorize(self, record):
        """
        Get a special format string with ASCII color codes.
        """

        # Dynamic message color based on logging level
        if record.levelno in self.level_map:
            fg, bg, bold = self.level_map[record.levelno]
        else:
            # Defaults
            bg = None
            fg = "white"
            bold = False

        # Magician's hat
        # https://www.youtube.com/watch?v=1HRa4X07jdE
        # template = [
        #     "[",
        #     self.get_color("black", None, True),
        #     "%(asctime)s",
        #     self.reset,
        #     "] ",
        #     self.get_color("white", None, True) if self.show_name else "",
        #     "%(name)s " if self.show_name else "",
        #     "%(padded_who)s",
        #     self.reset,
        #     " ",
        #     self.get_color(bg, fg, bold),
        #     "%(message)s",
        #     self.reset,
        # ]

        template = [
            "[",
            self.get_color("gray", None, False),
            "%(asctime)s",
            self.reset,
            "] ",
            #self.get_color("white", None, True) if self.show_name else "",
            self.get_color(bg, fg, bold),
            "%(name)s" if self.show_name else "",
            self.reset,
            self.get_color("green", None, False),
            " %(threadName)s:",
            self.reset,
            #"{%(process)d} ",
            "{%(sthread)s} ",
            #self.get_color("red", None, False),
            self.get_color(bg, fg, bold),
            "%(levelname)s",
            self.reset,
            self.get_color("yellow", None, False),
            " %(message)s",
            self.reset,
            self.get_color("blue", None, False),
            "  [%(padded_who)s]\n",
            self.reset,
        ]

        #'%(asctime)7s [%(name)s] %(threadName)11s:{%(sthread)s} %(levelname)5s %(message)s ' 




        format = "".join(template)

        who = [self.get_color("blue"),
               getattr(record, "funcName", ""),
               "()",
               #self.get_color("black", None, True),
               # ":",
               # self.get_color("cyan"),
               # str(getattr(record, "lineno", 0))
               ]

        who = "".join(who)

        # We need to calculate padding length manualy
        # as color codes mess up string length based calcs
        # unformatted_who = getattr(record, "funcName", "") + "()" + \
        #     ":" + str(getattr(record, "lineno", 0))

        # if len(unformatted_who) < self.who_padding:
        #     spaces = " " * (self.who_padding - len(unformatted_who))
        # else:
        #     spaces = ""

        record.padded_who = who #+ spaces
        #record.nasctime = 

        formatter = logging.Formatter(format, self.date_format)
        self.colorize_traceback(formatter, record)
        output = formatter.format(record)
        # Clean cache so the color codes of traceback don't leak to other formatters
        record.ext_text = None
        return output

    def colorize_traceback(self, formatter, record):
        """
        Turn traceback text to diff coloures.
        # """

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)

            output_list = []
            for line in formatter.formatException(record.exc_info).split("\n"):
                #p(line)
                if "Traceback" in line:
                    output_list.append(self.get_color("red", None, True))
                    output_list.append(line)
                    #output_list.append(self.reset)
                    output_list.append("\n")
                
                else:
                    if "File" in line:
                        new_line = []
                        for token in line.split(" "):
                            #p(repr(token))
                            if "file" in token.lower():
                                new_line.append("  ")
                                new_line.append(self.reset)
                                new_line.append(self.get_color("gray", None, True))
                                new_line.append(token)
                                #new_line.append(self.reset)
                                new_line.append(self.get_color("magenta", None, False))
                            elif "line" == token:
                                #p(repr(token))
                                new_line.append(self.reset)
                                #new_line.append("\t    ")
                                new_line.append(self.get_color("gray", None, True))
                                new_line.append(token)
                                new_line.append(self.get_color("magenta", None, False))
                            elif "in" == token:
                                #p(repr(token))
                                new_line.append(self.reset)
                                new_line.append(self.get_color("gray", None, True))
                                new_line.append(token)
                                new_line.append(self.get_color("magenta", None, False))
                            else:
                                new_line.append(token)
                        output_list.append(" ".join(new_line))
                    else:
                            #new_line.append()
                        #self.get_color("yellow", None, False)
                        output_list.append("\n     ")
                        output_list.append(self.get_color("magenta"))
                        output_list.append(line)
                        output_list.append("\n")
                        output_list.append(self.reset)
            

            record.exc_text = "".join(output_list)  + "\n\n\n\n"          #p(record.exc_text )

    def format(self, record):
        """
        Formats a record for output.

        Takes a custom formatting path on a terminal.
        """
        if self.is_tty:
            message = self.colorize(record)
        else:
            message = logging.StreamHandler.format(self, record)

        return message




