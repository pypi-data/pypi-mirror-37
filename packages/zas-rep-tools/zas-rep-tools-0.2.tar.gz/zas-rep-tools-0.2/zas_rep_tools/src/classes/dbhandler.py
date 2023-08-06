#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : XXX{Information about this code}XXX
# Author:
# c(Developer) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###Programm Info######
#
#
#
#
#Info:
# SQLite will easily do 50,000 or more INSERT statements per second on an average desktop computer. 
# But it will only do a few dozen transactions per second. 
# avoid cursore.executescript() becuase it makes commit first 
# By default, the sqlite module opens transactions implicitly before a Data Modification Language (DML) statement (i.e. INSERT/UPDATE/DELETE/REPLACE), and commits transactions implicitly before a non-DML, non-query statement (i. e. anything other than SELECT or the aforementioned).
from __future__ import absolute_import


import os
import copy
import sys
import time
import logging
import json
import traceback
import threading
import gc
import inspect
import threading
import subprocess


from collections import defaultdict, OrderedDict
from raven import Client
from time import gmtime, strftime
import random
from shutil import copyfile

#import sqlite3 as sqlite
#from pysqlcipher import dbapi2 as sqlite
#import zas_rep_tools.src.classes.sql.singlethreadsinglecursor as sqlite
#import zas_rep_tools.src.classes.sql.MultiThreadMultiCursor as sqlite


from zas_rep_tools.src.utils.zaslogger import ZASLogger  
from zas_rep_tools.src.utils.custom_exceptions import  ZASCursorError, ZASConnectionError,DBHandlerError,ProcessError,ErrorInsertion,ThreadsCrash
import  zas_rep_tools.src.utils.db_helper as db_helper
from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, path_to_zas_rep_tools, instance_info, Status,function_name, SharedCounterExtern, SharedCounterIntern, statusesTstring
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.classes.basecontent import BaseContent, BaseDB
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus

import platform
if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama



 #"pclsjt"
        # optimizer_names= {
        #                 "p":"page_size",
        #                 "c":"cache_size", #When you change the cache size using the cache_size pragma, the change only endures for the current session. The cache size reverts to the default value when the database is closed and reopened.
        #                 "l":"locking_mode",
        #                 "s":"synchronous",
        #                 "j":"journal_mode",
        #                 "t":"temp_store", 
        #                    }


class DBHandler(BaseContent, BaseDB):
    __metaclass__ = db_helper.DBErrorCatcher
    #DBErrorCatcher = True

    templates = {
            "twitter":db_helper.default_tables["corpus"]["documents"]["twitter"],
            "blogger":db_helper.default_tables["corpus"]["documents"]["blogger"]
            }

    supported_db_typs = ["stats", "corpus"]
    path_to_json1 = os.path.join(path_to_zas_rep_tools, "src/extensions/json1/json1")
        

    default_optimizer_flags = "lj"

    mapped_states = {
                "synchronous":{
                            "0":"off",
                            "1":"normal",
                            "2":"full",
                            "3":"extra",
                            },
                "temp_store":{
                            "0":"default",
                            "1":"file",
                            "2":"memory"
                            }
                }
    non_mapped_states= {
                "journal_mode":["delete" , "truncate" , "persist" , "memory" , "wal" , "off"],
                "locking_mode": ["normal" , "exclusive"],
                }



    def __init__(self, **kwargs):
        super(type(self), self).__init__(**kwargs)

        global sqlite
        #p(self._optimizer, "11self._optimizer")
        if self._thread_safe:
            import zas_rep_tools.src.classes.sql.MultiThreadMultiCursor as sqlite
            self._check_same_thread = False
            #DBHandler.default_optimizer_flags 
            if not self._optimizer:
                self._optimizer = DBHandler.default_optimizer_flags 
            #self._optimizer = "l"
        else:
            from pysqlcipher import dbapi2 as sqlite
            self._check_same_thread = True

        #p(self._optimizer, "22self._optimizer")

        self._arguments_for_connection = self._get_arguments_for_conn()
        self.locker = threading.Lock()
        self._double_items =  "or REPLACE" if self._replace_double_items else "or IGNORE"
        
        if self._thread_safe:
            self.logger.info("DBHandler was started in ThreadSafeMode.")
        else:
            self.logger.warning("DBHandler was started in  Thread-UNSAFE-Mode. (If you will use current Object in MultiThread Environment, than it could due to crash and all your data will be gone. But for using in the One-Thread Environment it speed-up the process about 10%.)")
        #InstanceAttributes: Initialization
        self._init_instance_variables()


        #p(int(self.number_of_new_inserts_after_last_commit), "self.number_of_new_inserts_after_last_commit")
        self.logger.debug('An instance of DB() was created ')


        ## Log Settings of the Instance
        attr_to_flag = ["files_from_zips_to_read_orig", "files_from_zips_to_read_left_over", ] 
        attr_to_len = ["files_to_read_orig", "files_to_read_leftover", "zips_to_read", ]
        self._log_settings(attr_to_flag =attr_to_flag,attr_to_len =attr_to_len)


        ############################################################



        ############################################################
        ####################__init__end#############################
        ############################################################






    def __del__(self):
        #import psutil
        #for proc in psutil.process_iter():
        #    p("<<<")
        #    for f in proc.open_files():
        #        print f
        #    p(">>>")
        #    #p( proc.open_files() )
        if self._db:
            if self._use_cash:
                self._write_cashed_insertion_to_disc()
            if int(self.number_of_new_inserts_after_last_commit):
                self.logger.info("Connection with DB was closed without commits. {} new inserts wasn't committed/saved_on_the_disk. (Notice: All not-committed changes in the DB wasn't saved on the disk!!!  Please use 'db.close()' to commit all changes into DB and save them on the disk before exit the script.".format( int(self.number_of_new_inserts_after_last_commit) ) )
            else:
                self.logger.info("Connection with DB was closed without commits. ({} insertion was waiting for commit)".format( int(self.number_of_new_inserts_after_last_commit) ) )
            if self._created_backups:
                for dbname in copy.deepcopy(self._created_backups):
                    self._del_backup(dbname)
            try:
                self._db.close()
                del self._threads_cursors
            except:
                pass

        if int(self.error_insertion_counter) > 0:
            self.logger.error("'{}'-ErrorInsertion(s) was done.".format(int(self.error_insertion_counter)))
            raise ErrorInsertion, "'{}'-ErrorInsertion was processed. See additional Information in the logs.".format(int(self.error_insertion_counter))
        del self._db
        self._db = False
        self.logger.debug("DB-Instance was destructed")

        
        #self.logger.newline(1)
        super(type(self), self).__del__()



    def _get_arguments_for_conn(self):
        _arguments_for_connection = {"check_same_thread":self._check_same_thread}
        if not (self._isolation_level == False): #https://www.quora.com/What-is-the-purpose-of-an-SQLite3-transaction-if-it-is-not-exclusive
            '''
            DEFERRED #Acquire and release the appropriate lock(s) for each SQL operation automatically. The operative philosophy here is Just-In-Time; no lock is held for longer than needed, and BEGIN itself doesn’t try to grab any locks at all. 
            IMMEDIATE #  Immediately try to acquire and hold RESERVED locks on all databases opened by this connection. This instantly blocks out all other writers for the duration of this transaction. BEGIN IMMEDIATE TRANSACTION will block or fail if another connection has a RESERVED or EXCLUSIVE lock on any of this connection’s open DBs.
            EXCLUSIVE #Immediately acquire and hold EXCLUSIVE locks on all databases opened by this connection. This instantly blocks out all other connections for the duration of this transaction. BEGIN EXCLUSIVE TRANSACTION will block or fail if another connection has any kind of lock on any of this connection’s open DBs.
            '''
            _arguments_for_connection["isolation_level"] = self._isolation_level

        if self._thread_safe:
            _arguments_for_connection["logger_usage"] = self._logger_usage
            _arguments_for_connection["logger_level"] = self._logger_level
            _arguments_for_connection["logger_save_logs"] = self._logger_save_logs
            _arguments_for_connection["logger_traceback"] = self._logger_traceback
            _arguments_for_connection["save_status"] = self._save_status
            _arguments_for_connection["save_settings"] = self._save_settings
            _arguments_for_connection["ext_tb"] = self._ext_tb
            _arguments_for_connection["mode"] = self._mode
            _arguments_for_connection["error_tracking"] = self._error_tracking


            
        #p(_arguments_for_connection)
        return _arguments_for_connection


####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
######################################Extern########################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################



###########################DB-Initialization#############################

    def init(self, typ, prjFolder, DBname, language, visibility,
            platform_name=False,  encryption_key=False, fileName=False,
            source=False, license=False, template_name=False, version=False,
            cols_and_types_in_doc=False, corpus_id=False,
            stats_id=False, retrival_template_automat = True, thread_name="Thread0", db_frozen=False,
            context_lenght=None):

        cols_and_types_in_doc = copy.deepcopy(cols_and_types_in_doc)
        supported_typs = DBHandler.supported_db_typs
        typ = typ.lower()
        if typ == "corpus":
            if not platform_name:
                self.logger.error("'Platform_name' wasn't given. 'Corpus' initialization need 'platform_name'.", exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            status = self.init_corpus(prjFolder, DBname, language,  visibility, platform_name, encryption_key=encryption_key,fileName=fileName, source=source, license=license, template_name=template_name, version=version, corpus_id=corpus_id, cols_and_types_in_doc=cols_and_types_in_doc, retrival_template_automat=retrival_template_automat, thread_name=thread_name)
            
            if not status["status"]:
                return status
            
            return Status(status=True)

        elif typ == "stats":
            #if not corpus_id:
            #    self.logger.error("'Corpus_id' wasn't given. 'Stats' initialization need Corpus_id.", exc_info=self._logger_traceback)
            #    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
                
            status = self.init_stats(prjFolder, DBname, language, visibility, corpus_id, encryption_key=encryption_key,fileName=fileName, version=version, stats_id=stats_id, thread_name=thread_name, db_frozen=db_frozen, context_lenght=context_lenght)
            if not status["status"]:
                return status
            
            return Status(status=True)

        else:
            self.logger.error("Given DB-Typ is not supported! Please one of the following  types: '{}'.".format(typ, supported_typs), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))





    def init_corpus(self, prjFolder, DBname, language,  visibility, platform_name,
                    encryption_key=False,fileName=False, source=False, license=False,
                    template_name=False, version=False,  thread_name="Thread0",
                    cols_and_types_in_doc=False, corpus_id=False, retrival_template_automat = True):
        ### Preprocessing: Create File_Name
        #p(template_name, "-3template_name")
        cols_and_types_in_doc =copy.deepcopy(cols_and_types_in_doc)
        # if retrival_template_automat:
        #     if not template_name:
        #         if platform_name in DBHandler.templates:
        #             template_name = platform_name
        #             self.logger.debug("For given '{}'-Platform  was found an '{}'-Template. (since 'retrival_template_automat'-Option set to  True, found Template will be automatically used for Corpus Initialization. If you don't want it than set this Option to False)".format(platform_name, template_name))
        
        self._encryption_key = encryption_key
        source="NULL" if not source else source
        license = "NULL" if not license else license
        version = "NULL" if not "NULL" else version
        #p(template_name, "-2template_name")
        template_name = "NULL" if not template_name else template_name
        typ= "corpus"
        #p(template_name, "-1template_name")
        
        if not corpus_id:
            corpus_id= db_helper.create_id(DBname,language, typ, visibility)
        #p((self._rewrite, self._stop_if_db_already_exist))
        fileName,path_to_db = db_helper.get_file_name(prjFolder,corpus_id,DBname,
                            language,visibility, typ,fileName, platform_name,
                            encrypted= True if encryption_key else False,
                            rewrite=self._rewrite,
                            stop_if_db_already_exist=self._stop_if_db_already_exist)
        
        if path_to_db is None:
            self.logger.info("InitCorpusDBProblem: DB with the same Name '{}' is already exist. InitProcess was stopped.".format(fileName))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2)) 

        
        ### Initialisation of DB
        if not self._check_db_should_not_exist()["status"]:
            return self._check_db_should_not_exist()




        if os.path.isdir(prjFolder):
            path_to_db =":memory:"  if self._in_memory else path_to_db
            self._db = sqlite.connect(path_to_db,  **self._arguments_for_connection)
            #p(self._arguments_for_connection,"self._arguments_for_connection")
            self._init_threads_cursors_obj()
            

            if self._optimizer:
                self._optimize(thread_name=thread_name)
            #self._threads_cursors[thread_name] = self._db.cursor()
            self._check_db_compilation_options(self._db)
            if self._encryption_key:
                try:
                    #c = self._db.cursor()
                    self._threads_cursors[thread_name].execute("PRAGMA key='{}'".format(self._encryption_key))
                    self._commit()
                    self.is_encrypted = True
                except Exception as  exception:
                    print_exc_plus() if self._ext_tb else ""
                    self.logger.error("Something happens while initialization of Corpus '{}'".format( exception), exc_info=self._logger_traceback)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            self._update_database_pragma_list(thread_name=thread_name) 
            self._update_temp_list_with_dbnames_in_instance(thread_name=thread_name)

            created_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            attributs_list = db_helper.default_tables[typ]["info"]
            values = [corpus_id, DBname, platform_name, template_name, version, language, created_at, source,license,visibility,typ]
            
            status = self._init_info_table(attributs_list)
            if not status["status"]:
                self.logger.error("CorpusInitialisatioError: Corpus wasn't initialized because  info Table wasn't initialized. ", exc_info=self._logger_traceback)
                self._close()
                os.remove(path_to_db)
                return status
            #sys.exit()
            #p(self.tables(), "tables")
            #p(dict(zip([attr[0] for attr in attributs_list],values)))
            status = self.add_attributs(dict(zip([attr[0] for attr in attributs_list],values)))
            if not status["status"]:
                self.logger.error("CorpusInitialisatioError: Corpus wasn't initialized because attributes wasn't added into   info Table. ", exc_info=self._logger_traceback)
                self._close()
                os.remove(path_to_db)

                return status
            #p(template_name, "000template_name")
            status = self._init_default_tables("corpus", template=template_name, cols_and_types_in_doc=cols_and_types_in_doc)
            if not status["status"] :
                self.logger.error("CorpusInitialisatioError: Corpus wasn't initialized because  default Tables wasn't initialized. ", exc_info=self._logger_traceback)
                self._close()
                os.remove(path_to_db)
                return status
            #self._init_documents_table_in_corpus()
            self._commit()
            #p(self.tables(), "tables")
            self._update_temp_indexesList_in_instance(thread_name=thread_name)
            #self._update_database_pragma_list(thread_name=thread_name)
            self._update_pragma_table_info(thread_name=thread_name)
            #p(self.col("documents"))
            #sys.exit()
            self.logger.info("Corpus-DB ({}) was initialized and saved on the disk: '{}'. ".format(fileName, path_to_db))
            #self.logger.info("Corpus-DB ({}) was connected.".format(fileName))
            self._mainDB_was_initialized = True
            return Status(status=True)
        else:
            self.logger.error("Given Project Folder is not exist: '{}'. ".format(prjFolder), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))





    def init_stats(self, prjFolder, DBname, language, visibility, corpus_id, thread_name="Thread0",
                    encryption_key=False,fileName=False, version=False, stats_id=False,  db_frozen=False,
                    context_lenght=None):

        self._encryption_key = encryption_key

        ### Preprocessing: Create File_Name
        version = "NULL" if not version else version
        typ= "stats"

        if not stats_id:
            stats_id= db_helper.create_id(DBname,language, typ, visibility)

        
        if not stats_id:
            self.logger.error("Id wasn't created. Stats-ID was given without Corpus-ID. This is an illegal input.", exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        fileName,path_to_db = db_helper.get_file_name(prjFolder,corpus_id,DBname,
                        language,visibility, typ, fileName, second_id=stats_id,
                        encrypted= True if encryption_key else False,
                        rewrite=self._rewrite, stop_if_db_already_exist=self._stop_if_db_already_exist)
        
        if path_to_db is None:
            self.logger.info("InitStatsDBProblem: DB with the same Name '{}' is already exist. InitProcess was stopped.".format(fileName))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2)) 

        ### Initialisation of DB
        if not self._check_db_should_not_exist()["status"]:
            return self._check_db_should_not_exist()

        if os.path.isdir(prjFolder):
            path_to_db =":memory:"  if self._in_memory else path_to_db
            self._db = sqlite.connect(path_to_db, **self._arguments_for_connection)


            if self._optimizer:
                self._optimize(thread_name=thread_name)
            self._init_threads_cursors_obj()
            #self._threads_cursors[thread_name] = self._db.cursor()
            self._check_db_compilation_options(self._db)
            if self._encryption_key:
                try:
                    #c = self._db.cursor()
                    self._threads_cursors[thread_name].execute("PRAGMA key='{}'".format(self._encryption_key))
                    self._commit()
                    self.is_encrypted = True
                except Exception as  exception:
                    print_exc_plus() if self._ext_tb else ""
                    self.logger.error("Something happens while initialization of Stats '{}'".format( exception), exc_info=self._logger_traceback)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


            self._update_database_pragma_list(thread_name=thread_name)
            self._update_temp_list_with_dbnames_in_instance(thread_name=thread_name)
            if not stats_id:
                stats_id= db_helper.create_id(DBname,language, typ, visibility,corpus_id=corpus_id)
            created_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            attributs_list = db_helper.default_tables[typ]["info"]
            #p(attributs_list, "attributs_list")
            values = [stats_id,corpus_id, DBname, version,  created_at, visibility,typ,db_frozen,context_lenght]
            #p(values, "values")

            status = self._init_info_table(attributs_list)
            #p(dict(zip([attr[0] for attr in attributs_list],values)))
            if not status["status"]:
                self.logger.error("StatsInitialisatioError: Stats wasn't initialized because  info Table wasn't initialized. ", exc_info=self._logger_traceback)
                self._close()
                os.remove(path_to_db)
                return status

            status = self.add_attributs(dict(zip([attr[0] for attr in attributs_list],values)))
            if not status["status"]:
                self.logger.error("StatsInitialisatioError: Stats wasn't initialized because attributes wasn't added into   info Table. ", exc_info=self._logger_traceback)
                self._close()
                os.remove(path_to_db)
                return status

            status = self._init_default_tables("stats")    
            if not status["status"]:
                self.logger.error("StatsInitialisatioError: Corpus wasn't initialized because  default Tables wasn't initialized. ", exc_info=self._logger_traceback)
                self._close()
                os.remove(path_to_db)
                return status
            
            self._commit()
            #self.dbnames.append("main")

            self._update_temp_indexesList_in_instance(thread_name=thread_name)
            #self._update_database_pragma_list(thread_name=thread_name)
            self._update_pragma_table_info(thread_name=thread_name)
            
            self.logger.info("Stats-DB ({}) was initialized and saved on the disk: '{}'. ".format(fileName, path_to_db))
            #self.logger.info("Stats-DB ({}) was connected.".format(fileName))
            self._mainDB_was_initialized = True
            return Status(status=True)
        else:
            self.logger.error("Given Project Folder is not exist: '{}'. ".format(prjFolder), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def initempty(self, prjFolder, DBname, encryption_key=False,  thread_name="Thread0"):
        ### Preprocessing: Create File_Name
        self._encryption_key = encryption_key
        fileName,path_to_db = db_helper.get_file_name_for_empty_DB(prjFolder,DBname,
                    encrypted= True if encryption_key else False,
                    rewrite=self._rewrite, stop_if_db_already_exist=self._stop_if_db_already_exist)
        
        if path_to_db is None:
            self.logger.info("InitEmptyDBProblem: DB with the same Name '{}' is already exist. InitProcess was stopped.".format(fileName))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2)) 

        if not self._check_db_should_not_exist()["status"]:
            return self._check_db_should_not_exist()

        if os.path.isdir(prjFolder):
            path_to_db =":memory:"  if self._in_memory else path_to_db
            self._db = sqlite.connect(path_to_db, **self._arguments_for_connection)


            if self._optimizer:
                self._optimize(thread_name=thread_name)
            self._init_threads_cursors_obj()
            #self._threads_cursors[thread_name] = self._db.cursor()
            self._check_db_compilation_options(self._db)
            if self._encryption_key:
                try:
                    #c = self._db.cursor()
                    self._threads_cursors[thread_name].execute("PRAGMA key='{}'".format(self._encryption_key))
                    self._commit()
                    self.is_encrypted = True
                except Exception as  exception:
                    print_exc_plus() if self._ext_tb else ""
                    self.logger.error("Something happens while initialization of Corpus '{}'".format( exception), exc_info=self._logger_traceback)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            self._update_database_pragma_list(thread_name=thread_name)
            self._update_temp_list_with_dbnames_in_instance(thread_name=thread_name)
            self._update_temp_indexesList_in_instance(thread_name=thread_name)
            #self._update_database_pragma_list(thread_name=thread_name)
            self._update_pragma_table_info(thread_name=thread_name)
            
            #p(self._db)

            self.logger.info("Empty-DB ({}) was initialized and saved on the disk: '{}'. ".format(fileName, path_to_db))
            #self.logger.info("Empty-DB ({}) was connected.".format(fileName))
            self._mainDB_was_initialized = True
            
            return Status(status=True)
        else:
            self.logger.error("Given Project Folder is not exist: '{}'. ".format(prjFolder), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))





    def init_default_indexes(self, thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        try:
            for table_name, index_query_list in db_helper.default_indexes[self.typ()].iteritems():  
                for index_query in index_query_list:
                    #p(index_query)
                    #c = self._db.cursor()
                    self._threads_cursors[thread_name].execute(index_query)
                    self.logger.debug("Index for '{}'-DB, '{}'-Table was initialized.".format(self.typ(), table_name))
            self._update_temp_indexesList_in_instance(thread_name=thread_name)
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("IndexesInitError: Following Exception was throw: '{}'".format(e), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



# ##########################DB-Connection#############################


    def dump(self, file_name):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        with open(file_name, 'w') as f:
            for line in self._db.iterdump():
                f.write('%s\n' % line)



    def connect(self,path_to_db, encryption_key=False, reconnection=False, logger_debug=False, thread_name="Thread0"):
        #p(logger_debug, "logger_debug")

        if not self._check_file_existens(path_to_db):
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        if not self._check_db_should_not_exist()["status"]:
            return self._check_db_should_not_exist()
        self._encryption_key = encryption_key

        dbName = os.path.splitext(os.path.basename(path_to_db))[0]

        status = self._validation_DBfile(path_to_db, encryption_key=encryption_key)
        if not status["status"]:
            self.logger.debug("ValidationError: DB cannot be connected!", exc_info=self._logger_traceback)
            return status
        else:
            self._db = status["out_obj"]
            self._init_threads_cursors_obj()
            #self._threads_cursors[thread_name] = self._db.cursor()

        if encryption_key:
            self.is_encrypted = True

        try:
            self._update_database_pragma_list(thread_name=thread_name)
            self._update_temp_list_with_dbnames_in_instance(thread_name=thread_name)
            self._update_temp_tablesList_in_instance(thread_name=thread_name)
            #self._update_database_pragma_list(thread_name=thread_name)
            self._update_pragma_table_info(thread_name=thread_name)
            self._update_temp_attributsList_in_instance(thread_name=thread_name)
            self._update_temp_indexesList_in_instance(thread_name=thread_name)
            self.not_initialized_dbs.append("main")
            
        except sqlite.DatabaseError, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("DatabaseError: {}".format(e), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("ConnectionError: {}".format(e), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))            
        

        if reconnection:
            msg= "DB ('{}') was RE-connected".format(dbName)
        else:
            msg= "DB ('{}') was connected.".format(dbName)

        if logger_debug:
            self.logger.debug(msg)
        else:
            self.logger.info(msg)

        return Status(status=True)



    def _backup(self, dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        
        if dbname not in self.dbnames:
            self.logger.error(" '{}'-DB is not exist in the instance.".format(dbname))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        fname = os.path.splitext(self.fname(dbname=dbname))
        new_fname = fname[0]+"_backup"+fname[1]
        dirname = self.dirname(dbname=dbname)
        path = self.path(dbname=dbname)
        copyfile(path, os.path.join(dirname, new_fname))
        self._created_backups[dbname] = os.path.join(dirname, new_fname)
        self.logger.info("Temporary-Backup of '{}'-DB  was created in '{}'.".format(fname[0]+fname[1], dirname))




    def attach(self,path_to_db, encryption_key=False, reattaching=False, db_name=False,thread_name="Thread0"):
        #p((path_to_db, encryption_key), c="m")
        status = self._check_file_existens(path_to_db)
        if not status["status"]:
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        status = self._validation_DBfile( path_to_db, encryption_key=encryption_key)
        #self._reinitialize_logger()
        if not status["status"]:
            self.logger.error("ValidationError: DB cannot be attached!", exc_info=self._logger_traceback)
            return status
        else:
            del status["out_obj"]
        gc.collect()

        dbName = db_name if db_name else "_" + os.path.splitext(os.path.basename(path_to_db))[0]
        
        if self._encryption_key:
            if encryption_key:
                query = "ATTACH DATABASE '{path_to_db}' AS {dbName} KEY '{key}';".format(path_to_db=path_to_db, dbName=dbName, key=encryption_key)

            else:
                query = "ATTACH DATABASE '{path_to_db}' AS {dbName} KEY '';".format(path_to_db=path_to_db, dbName=dbName)

        else:
            if encryption_key:
                query = "ATTACH DATABASE '{path_to_db}' AS {dbName} KEY '{key}';".format(path_to_db=path_to_db, dbName=dbName, key=encryption_key)

            else:
                query = "ATTACH DATABASE '{path_to_db}' AS {dbName};".format(path_to_db=path_to_db, dbName=dbName)

        #p(query)
        #p(self._attachedDBs_config,"1self._attachedDBs_config", c="r")
        
        if dbName not in self.dbnames:
            try:
                #cursor = self._db.cursor()
                self._threads_cursors[thread_name].execute(query)
            except Exception as  exception:
                print_exc_plus() if self._ext_tb else ""
                if "unrecognized token" in str(exception):
                    self.logger.error("DBAttachError:  While attaching of the '{}'-DB attacher get an following error: '{}'. Probably you used not allowed characters in the db or file name. (e.g. '.' not allowed).".format(dbName, repr(exception) ), exc_info=self._logger_traceback)
                else:    
                    self.logger.error("DBAttachError: Something happens while attaching of '{}'-DB: '{}'".format(dbName, repr(exception) ), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            #p(self._attachedDBs_config,"2self._attachedDBs_config", c="r")
            self._attachedDBs_config.append((path_to_db, dbName, encryption_key))

            self._update_database_pragma_list(thread_name=thread_name)
            self._update_temp_list_with_dbnames_in_instance(thread_name=thread_name)
            self._update_temp_tablesList_in_instance(thread_name=thread_name)
            #self._update_database_pragma_list(thread_name=thread_name)
            self._update_pragma_table_info(thread_name=thread_name)
            self._update_temp_attributsList_in_instance(thread_name=thread_name)
            self.not_initialized_dbs.append(dbName)
        
            if reattaching:
                self.logger.info("DB ('{}') was Reattached".format(dbName))
            else:
                self.logger.info("DB ('{}') was attached".format(dbName))
            return Status(status=True)
        else:
            self.logger.error("DB '{}' is already attached. You can not attached same DB more as 1 time!".format(dbName), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))




    def reattach(self, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()

        list_to_reattach =[]
        if dbname and dbname!="main":
            list_to_reattach.append(dbname)
        else:
            list_to_reattach = [attacheddb[1] for attacheddb in self._attachedDBs_config]

        #p(list_to_reattach,"list_to_reattach",c="m")
        for attached_db_name in list_to_reattach:
            if attached_db_name  in self.dbnames:
                configs_list_of_detached_dbs =self.detach(attached_db_name, thread_name=thread_name)
                #p(configs_list_of_detached_dbs )
                if configs_list_of_detached_dbs:
                    path_to_db = configs_list_of_detached_dbs[0][0]
                    encryption_key = configs_list_of_detached_dbs[0][2]
                    dbname_to_retach = configs_list_of_detached_dbs[0][1]
                    status = self.attach(path_to_db, encryption_key=encryption_key, thread_name=thread_name)
                    #p(status,"status")
                    if not status["status"]:
                        self.logger.error("'{}' DB wasn't re-attached".format(dbname_to_retach), exc_info=self._logger_traceback)
                        return status

                else:
                    self.logger.error("'{}' DB wasn't detached.".format(attached_db_name), exc_info=self._logger_traceback)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            else:
                self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure.".format(attached_db_name), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        return Status(status=True)



    def detach(self, dbname="main", thread_name="Thread0"):

        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()

        list_to_detach =[]
        detached_dbs = []
        if dbname and dbname!="main":
            list_to_detach.append(dbname)
        else:
            list_to_detach = [attacheddb[1] for attacheddb in self._attachedDBs_config]

        #p(list_to_detach,"list_to_detach", c="r")
        for attached_db_name in list_to_detach:
            if attached_db_name  in self.dbnames:
                configs = self._get_configs_from_attached_DBList(attached_db_name)
                
                if configs:
                    #p(configs, c="m")
                    self._del_attached_db_from_a_config_list(attached_db_name)
                    query = "DETACH DATABASE '{}';".format( attached_db_name)
                    
                    try:
                        #cursor = self._db.cursor()
                        self._threads_cursors[thread_name].execute(query)
                        self.logger.debug("'{}'-DB was detached.".format(attached_db_name))

                        detached_dbs.append(configs[0])
                        self.not_initialized_dbs.remove(attached_db_name)
                        if attached_db_name in self._created_backups:
                            self._del_backup(attached_db_name)

                    except Exception as  exception:
                        print_exc_plus() if self._ext_tb else ""
                        self.logger.error("Something happens while detaching of '{}'-DB: '{}'".format(attached_db_name, repr(exception) ), exc_info=self._logger_traceback)
                else:
                    self.logger.error("Given Attached DB '{}' is not in the Config-List of AttachedDBs. ".format(attached_db_name), exc_info=self._logger_traceback)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
            else:
                self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(attached_db_name), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        self._update_database_pragma_list(thread_name=thread_name)
        self._update_temp_list_with_dbnames_in_instance(thread_name=thread_name)
        self._update_temp_tablesList_in_instance(thread_name=thread_name)
        #self._update_database_pragma_list(thread_name=thread_name)
        self._update_pragma_table_info(thread_name=thread_name)
        self._update_temp_attributsList_in_instance(thread_name=thread_name)
        return detached_dbs






##########################DB-Attributes#####################



    def add_attributs(self,inp_dict, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()

        status =  self.insertdict("info", inp_dict, dbname=dbname, thread_name=thread_name)
        if status["status"]:
            self._update_temp_attributsList_in_instance(thread_name=thread_name)
            #self._update_pragma_table_info(thread_name=thread_name)
            return status
        else:
            self.logger.error("Attributes wasn't added into InfoTable (dbName:{})".format(dbname), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))




    def update_attr(self,attribut_name, value, dbname="main", thread_name="Thread0"):
        ### Exception Handling
        
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        # Check if attributes and values have the same length
        if not isinstance(attribut_name, (str, unicode)):
            self.logger.error("Given AttributName should be an string or unicode object.", exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        # if given attribute exist in the Info_Table
        if attribut_name not in self.col("info", dbname=dbname):
            self.logger.error("Given Attribute ('{}') is not exist in this DataBase.".format(attribut_name), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        if dbname  in self.dbnames:
            query = 'UPDATE {}.info  \nSET {}="{}";'.format(dbname,attribut_name,value)
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        
        ### Update Attribute
        if "info" in self.tables(dbname=dbname):
            try:
                #cursor = self._db.cursor()
                self._threads_cursors[thread_name].execute(query)
                self._commit()
                self._update_temp_attributsList_in_instance(thread_name=thread_name)
                return Status(status=True)
            except Exception as  exception:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("Something happens while detaching of '{}'-DB: '{}'".format(attached_db_name, repr(exception) ), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        else:
            self.logger.error("Info-Table is wasn't found or not exist. Please initialize the Info Table, bevor you may add any attributes.", exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def update_attrs(self, inp_dict, dbname="main", thread_name="Thread0"):
        ### Exception Handling
        
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        # Check if attributes and values have the same length
        # Check if attributes and values have the same length
        if not isinstance(inp_dict, dict):
            self.logger.error("UpdateAttributes: InputDict is not an 'dict'.", exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        inp_dict = copy.deepcopy(inp_dict)

        # if given attribute exist in the Info_Table
        col_in_info_table = self.col("info", dbname=dbname)
        if not all(elem in col_in_info_table for elem in inp_dict.keys()):
            average = list(set(inp_dict.keys())-set(col_in_info_table))
            self.logger.error("Some of the given  Attributes ('{}') is not exist in this DataBase. ".format(average ), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        attrib_to_str = ",".join(["{}='{}'".format(k,v)  for k,v in inp_dict.iteritems()])

        if dbname  in self.dbnames:
            query = 'UPDATE {}.info  \nSET {};'.format(dbname,attrib_to_str)
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        
        ### Update Attribute
        if "info" in self.tables(dbname=dbname):
            try:
                #cursor = self._db.cursor()
                self._threads_cursors[thread_name].execute(query)
                self._commit()
                self._update_temp_attributsList_in_instance(thread_name=thread_name)
                return Status(status=True)
            except Exception as  exception:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("Something happens while detaching of '{}'-DB: '{}'".format(attached_db_name, repr(exception) ), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        else:
            self.logger.error("Info-Table is wasn't found or not exist. Please initialize the Info Table, bevor you may add any attributes.", exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))





    def get_attr(self,attributName, dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        if not isinstance(attributName, (str, unicode)):
            self.logger.error("Given AttributName should be an string or unicode object.", exc_info=self._logger_traceback)
            #return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))
            return None
         
        if not self._attributs_dict:
            self.logger.warning("Temporary AttributesList is empty")
            #return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))
            return None

        # if given attribute exist in the Info_Table
        #p((attributName, self._attributs_dict,dbname))
        try:
            if attributName not in self._attributs_dict[dbname]:
                self.logger.error("Given Attribute ('{}') is not exist in the '{}'-DB.".format(attributName,dbname), exc_info=self._logger_traceback)
                #return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))
                return None
        except KeyError: 
            self.logger.error("'{}'-DB is not found.".format(dbname))
            return None

        if dbname  in self.dbnames:
            try:
                return self._attributs_dict.get(dbname, None).get(attributName, None)
            except:
                return None
            #[dbname][attributName]
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            #return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))
            return None



    def get_all_attr(self, dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if u"info" in self.tables(dbname=dbname):
            if dbname  in self.dbnames:
                return self._attributs_dict[dbname]
            else:
                self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
                return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        else:
            self.logger.error("Info-Table wasn't found or not exist. Please initialize the Info Table, bevor you may add any attributes.", exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))











##########################DB-Execute Commands#####################



    def execute(self, query, values=False, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()

        try:
            #c = 
            s = self._execute(query, values=values, dbname=dbname, thread_name=thread_name, new_cursor=True)
            #p(s, c="r")
            if not  s["status"]:
                return False
            else: 
                cur = s["out_obj"]
            #p(cur, "cur")
            self._update_temp_tablesList_in_instance(thread_name=thread_name)
            self._update_temp_indexesList_in_instance(thread_name=thread_name)
            self._update_database_pragma_list(thread_name=thread_name)
            self._update_pragma_table_info(thread_name=thread_name)
            return cur

        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while execution of the following query: '{}'. See following Exception: '{}'. ".format(query,str(exception)), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        
    def executescript(self, query, thread_name="Thread0", dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        try:
            #cur = self._db.cursor()
            self._threads_cursors[thread_name].executescript(query)
            self._update_temp_tablesList_in_instance(thread_name=thread_name)
            self._update_temp_indexesList_in_instance(thread_name=thread_name)
            self._update_database_pragma_list(thread_name=thread_name)
            self._update_pragma_table_info(thread_name=thread_name)
            return cur
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while execution of the following query: '{}'. See following Exception: '{}'. ".format(query,str(exception)), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


    def executemany(self, query, argument, thread_name="Thread0", dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        try:
            s = self._executemany(query, values=argument, dbname=dbname, thread_name=thread_name, new_cursor=True)
            if not  s["status"]:
                return s
            else: 
                cur = s["out_obj"]

            self._update_temp_tablesList_in_instance(thread_name=thread_name)
            self._update_temp_indexesList_in_instance(thread_name=thread_name)
            self._update_database_pragma_list(thread_name=thread_name)
            self._update_pragma_table_info(thread_name=thread_name)
            return cur
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while execution of the following query: '{}'. See following Exception: '{}'. ".format(query,str(exception)), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def _executemany(self, query, values=False, dbname="main", thread_name="Thread0", new_cursor = False):
        return self._execution(query, values=values, dbname=dbname, many=True, thread_name=thread_name, new_cursor=new_cursor)


    def _execute(self, query, values=False, dbname="main", thread_name="Thread0", new_cursor = False):
        return self._execution(query, values=values, dbname=dbname, many=False,thread_name=thread_name, new_cursor=new_cursor)

    def _execution(self,query, values=False, dbname="main", many=False, thread_name="Thread0", new_cursor = False):
        #p("EXECUTION")
        try:
            try:
                cursor = self._threads_cursors[thread_name]
            except:
                self._threads_cursors[thread_name] = self._db.cursor()
                cursor = self._threads_cursors[thread_name]

            cursor = self._db.cursor() if new_cursor else cursor
            #p(type(cursor))
            #p(query,"query")
            if many:
                if values:
                    cursor.executemany(query, values)
                else:
                    cursor.executemany(query)
            else:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)

            if self._thread_safe:
                cursor.join()
                #time.sleep(5)

            return Status(status=True, out_obj=cursor)

        except (sqlite.OperationalError, sqlite.IntegrityError) as  exception:
            track_id = self._error_track_id.incr()
            l_query = query if self._log_content else "!!LogContentDisable!!"
            l_values =  values if self._log_content else "!!LogContentDisable!!"
            
            if "UNIQUE constraint failed:" in str(exception):
                msg = "UniquenessERROR:  Redundant row was get and was out-sorted. |ErrorTrackID:'{}'| See Exception: '{}'.  InpQuery: '{}'.  InpValues: '{}'. ".format( track_id, repr(exception), l_query, l_values)
                #self.logger.outsorted_corpus() 
                if self.typ(dbname=dbname) == "corpus":
                    level_name =  "outsorted_corpus"
                    self.logger.outsorted_corpus(msg) 
                elif self.typ(dbname=dbname) == "stats":
                    level_name = "outsorted_stats"
                    self.logger.outsorted_stats(msg)
                else:
                    level_name = "error_insertion"
                    self.logger.error_insertion(msg)
                    self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                        desc="Redundant row was get.",
                        level=level_name, action="outsorted",
                        inp_obj= (query, values,dbname),
                        error_name="{} (UniquenessERROR)".format(exception.__class__.__name__), exception=exception)
            
            elif "SQL logic error" in str(exception):
                msg = "SQL logic error (ThreadsCrash):  Probably it is the result of ThreadsCrash. Please use option 'thread_safe' to ensure ThreadSafety and run script again. (Attention: Executed insertions could be inconsistent!)  |ErrorTrackID:'{}'| See Exception: '{}'.  InpQuery: '{}'.  InpValues: '{}'. ".format( track_id, repr(exception), l_query, l_values)
                #self.logger.outsorted_corpus() 
                level_name = "error_insertion"
                self.logger.error_insertion(msg)
                self.error_insertion_counter.incr()
                #if self._raise_exceptions:
                #    raise ThreadsCrash, 
                #    "SQL logic error:   Probably it is the result of ThreadsCrash. Please use option 'thread_safe' to ensure ThreadSafety and run script again.   |ErrorTrackID:'{}'| (Attention: Executed insertions could be inconsistent!) ".format(track_id)
                return Status(status=False, track_id=track_id,
                        desc="SQL logic error. ",
                        level=level_name, action="ThreadsCrash",
                        inp_obj= (query, values,dbname),
                        error_name="{} (ErrorBindingParameter)".format(exception.__class__.__name__), exception=exception)

            else:
                msg = "ExecutionError:  '{}'. (current Execution was ignored) |ErrorTrackID:'{}'|".format( repr(exception),track_id )
                if "has no column named" in str(exception):
                    msg = "ExecutionError:  '{}'. (current Execution was ignored) Possible Solution: 'Insert failed columns into SQL-DataBase or use Reader-Template to format and outsorte not needed columns. ' |ErrorTrackID:'{}'|".format( repr(exception),track_id )
                self.logger.error_insertion(msg, exc_info=self._logger_traceback)
                self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                            desc="It is not possible to insert all got columns into CorpDB. Possible Explanation: 1. Current DB was initialized with wrong and not full number of columns, please reinitialize current CorpusDB with right column names and types. Or use also option  precomputed corp types. For this use option  'template_name' on the Corpus Level ( while Initialization) (ex:template_name='twitter',or template_name='blogger'  ) or also on the Reader Level 'reader_formatter_name='twitter'.",
                            level="error_insertion", action="stop_execution",
                            inp_obj= (query, values,dbname),  func_name=function_name(-3),
                            error_name=exception.__class__.__name__, exception=repr(exception))

        except sqlite.InterfaceError as  exception:
            #p((query, values))
            track_id = self._error_track_id.incr()
            l_query = query if self._log_content else "!!LogContentDisable!!"
            l_values =  values if self._log_content else "!!LogContentDisable!!"
            #self.error_insertion_counter.incr()
            if "Error binding parameter " in str(exception):
                msg = "Error binding parameter(ThreadsCrash):  Probably it is the result of ThreadsCrash. Please use option 'thread_safe' to ensure ThreadSafety and run script again. (Attention: Executed insertions could be inconsistent!)   |ErrorTrackID:'{}'| See Exception: '{}'.  InpQuery: '{}'.  InpValues: '{}'. ".format( track_id, repr(exception), l_query, l_values)
                #self.logger.outsorted_corpus() 
                level_name = "error_insertion"
                self.logger.error_insertion(msg)
                
                #if self._raise_exceptions:
                #    raise ThreadsCrash, "Error binding parameter:  Probably it is the result of ThreadsCrash. Please use option 'thread_safe' to ensure ThreadSafety and run script again.   |ErrorTrackID:'{}'| (Attention: Executed insertions could be inconsistent!) ".format(track_id)
                self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                        desc="Error binding parameter",
                        level=level_name, action="ThreadsCrash",
                        inp_obj= (query, values,dbname),
                        error_name="{} (ErrorBindingParameter)".format(exception.__class__.__name__), exception=exception)
            else:
                self.logger.error_insertion("ExecutionError:  '{}'. (current Execution was ignored) |ErrorTrackID:'{}'|".format( repr(exception),track_id ), exc_info=self._logger_traceback)
                self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                            desc=repr(exception),
                            level="error_insertion", action="ignored",
                            inp_obj= (query, values,dbname),  func_name=function_name(-3),
                            error_name=exception.__class__.__name__, exception=exception)


        except Exception as  exception:
            track_id = self._error_track_id.incr()
            print_exc_plus() if self._ext_tb else ""
            self.logger.low_debug("ExecutionError: |ErrorTrackID:'{}'| Following Query could have an Error: '{}'. Track the error in the 'error_insertion'-Level. ".format(track_id, query, ))
            l_query = query if self._log_content else "!!LogContentDisable!!"
            l_values =  values if self._log_content else "!!LogContentDisable!!"
            self.error_insertion_counter.incr()
            if "has no column named" in str(exception):
                self.logger.error_insertion("ExecutionError: One of the columns is not in the Table. See Exception:  '{}'. (current Execution was ignored) |ErrorTrackID:'{}'| InpQuery: '{}'.  InpValues: '{}'.".format( repr(exception),track_id ,l_query, l_values ), exc_info=self._logger_traceback)
                self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                        desc="One of the columns is not in the Table.",
                        inp_obj= (query, values,dbname), func_name=function_name(-3),
                        level="error_insertion", action="ignored",
                        error_name=exception.__class__.__name__, exception=exception)

            else:
                l_query = query if self._log_content else "!!LogContentDisable!!"
                l_values =  values if self._log_content else "!!LogContentDisable!!"
                self.logger.error_insertion("ExecutionError: Something happens.  '{}'. (current Execution was ignored) |ErrorTrackID:'{}'| InpQuery: '{}'.  InpValues: '{}'. ".format(repr(exception),track_id,l_query, l_values ), exc_info=self._logger_traceback)
                self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                        desc="Something happens",
                        inp_obj= (query, values,dbname),  func_name=function_name(-3),
                        level="error_insertion", action="ignored",
                        error_name=exception.__class__.__name__, exception=exception)

























##########################DB-Info######################

    def exist(self):
        return Status(status=True) if self._db else False

    def typ(self, dbname="main"):
        return self.get_attr("typ", dbname="main")

    def name(self, dbname="main"):
        return self.get_attr("name", dbname="main")

    def visibility(self, dbname="main"):
        return self.get_attr("visibility", dbname="main")

    def version(self, dbname="main"):
        return self.get_attr("version", dbname="main")

    def id(self, dbname="main"):
        return self.get_attr("id", dbname="main")


    def encryption(self):
        if self.is_encrypted:
            return "encrypted"
        else:
            return "plaintext"

    def status(self):
        if self._db:
            if self._attachedDBs_config:
                return "manyDB"
            else:
                return "oneDB"
        else:
            return "noDB"

    def tables(self,dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if dbname in self.dbnames:
            #self.logger.low_debug("Table names was returned (dbname: '{}')".format(dbname))

            if len(self._tables_dict)>0:
                return self._tables_dict[dbname]
            else:
                self.logger.debug("Temporary TableList is empty! Probably current DB has no Tables or there is an logical error in the Implementation!")
                return []

        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return []


    def indexes(self,dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if dbname in self.dbnames:
            #self.logger.low_debug("Indexes names was returned (dbname: '{}')".format(dbname))

            if len(self._indexes_dict)>0:
                return self._indexes_dict[dbname]
            else:
                self.logger.critical("Temporary IndexList is empty!")
                return []

        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return []




    def fname(self,dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if dbname  in self.dbnames:
            for row in self._database_pragma_list:
                if row[1] == dbname:
                    return os.path.basename(row[2])
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def path(self, dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if dbname  in self.dbnames:
            for row in self._database_pragma_list:
                if row[1] == dbname:
                    return row[2]
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def dirname(self, dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        ## check existents of the dbName
        if dbname  in self.dbnames:
            for row in self._database_pragma_list:
                if row[1] == dbname:
                    return os.path.dirname(row[2])
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))


    def pathAttachedDBs(self):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        return [row[2] for row in self._database_pragma_list if row[1]!= "main"]


    def fnameAttachedDBs(self):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        return [ os.path.basename(row[2]) for row in self._database_pragma_list if row[1]!= "main"]



    def attached(self):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        return [ row[1] for row in self._database_pragma_list if row[1]!= "main"]


    

    def col(self, tableName,dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        
        if tableName not in self.tables(dbname=dbname):
            self.logger.error("'{}'-Table not exist in the '{}'-DB.".format(tableName, dbname))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        #self.logger.low_debug("Columns for Table '{}'  was returned (dbName:'{}')".format(tableName,dbname))
        return [column[1] for column in self._pragma_table_info[dbname][tableName]]



    def colt(self, tableName,dbname="main"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        
        if tableName not in self.tables(dbname=dbname):
            self.logger.error("'{}'-Table not exist in the '{}'-DB.".format(tableName, dbname))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        return [(column[1],column[2]) for column in self._pragma_table_info[dbname][tableName]]



    def rownum(self, tableName,dbname="main", thread_name="Thread0", where=False, connector_where="AND"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        ## check existents of the tableName
        if tableName not in self.tables(dbname=dbname):
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        if where:
            where_cond_as_str = db_helper.where_condition_to_str(where, connector=connector_where)
            #p(where_cond_as_str)
            if not where_cond_as_str:
                self.logger.error("GetRowNum: Where-Condition(s) wasn't compiled to String!", exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        ## check existents of the dbName
        if dbname  in self.dbnames:
            if where:
                query = "select count(*) from {dbname}.{table_name} WHERE {where} ; ".format(table_name=tableName, dbname=dbname,where=where_cond_as_str)
            else:
                query = "select count(*) from {dbname}.{table_name}; ".format(table_name=tableName, dbname=dbname)
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute(query)
            number = self._threads_cursors[thread_name].fetchone()
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while getting of RowsNumber for '{}'-Table:  '{}'.".format(tableName, repr(exception) ), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        #self.logger.debug("Number of Rows was returned")
        return number[0]
        #return [(column[1],column[2]) for column in columns]





##########################DB--Getters######################


    def getall(self, tableName, columns=False, select=False,  dbname="main", where=False, connector_where="AND", limit=-1, offset=-1, thread_name="Thread0", case_sensitiv=True, distinct=False):
        
        s = self._intern_getter(tableName, columns=columns, select=select,  dbname=dbname, where=where, connector_where=connector_where,limit=limit, offset=offset, thread_name=thread_name, case_sensitiv=case_sensitiv, distinct=distinct)
        #p(s["out_obj"])
        if s["status"]:
            return s["out_obj"].fetchall()
        else:
            self.logger.error("GetterError: Nor Cursor Element was passed from intern getter.")
            return []
            
    def getone(self, tableName, columns=False, select=False,  dbname="main", where=False, connector_where="AND", limit=-1, offset=-1, thread_name="Thread0", case_sensitiv=True, distinct=False):
        #p(dbname, "dbname")
        s = self._intern_getter(tableName, columns=columns, select=select,  dbname=dbname, where=where, connector_where=connector_where,limit=limit, offset=offset, thread_name=thread_name, case_sensitiv=case_sensitiv, distinct=distinct)
        #p(s["out_obj"])
        if s["status"]:
            return s["out_obj"].fetchone()
        else:
            self.logger.error("GetterError: Nor Cursor Element was passed from intern getter.")
            return []
            


    def lazyget(self, tableName, columns=False, select=False,  dbname="main", where=False, connector_where="AND", size_to_fetch=1000, output="list", limit=-1, offset=-1, thread_name="Thread0", case_sensitiv=True, just_check_existence=False, distinct=False):
        #self.logger.low_debug("LazyGet was invoked.")
        if output == "list":
            for row in  self.getlistlazy(tableName, columns=columns, select=select,  dbname=dbname, where=where, connector_where=connector_where, size_to_fetch=size_to_fetch,limit=limit, offset=offset, thread_name=thread_name, case_sensitiv=case_sensitiv, just_check_existence=just_check_existence, distinct=distinct):
                yield row

        elif output == "dict":
            for getted_dict in  self.getdictlazy( tableName, columns=columns, select=select,  dbname=dbname, where=where, connector_where=connector_where, size_to_fetch=size_to_fetch,limit=limit, offset=offset, thread_name=thread_name, case_sensitiv=case_sensitiv,just_check_existence=just_check_existence, distinct=distinct):
                yield getted_dict

        else:
            self.logger.error("LazyGetter: '{}'-OutputFormat is not supported. Please use one of the following: '['list','dict']' ".format(output), exc_info=self._logger_traceback)
            yield False
            return 




    def getdictlazy(self, tableName, columns=False, select=False,  dbname="main", where=False, connector_where="AND", size_to_fetch=1000, limit=-1, offset=-1, thread_name="Thread0", case_sensitiv=True,just_check_existence=False, distinct=False):
        #self.logger.low_debug("GetDictLazy was invoked.")
        list_with_keys = []
        if columns:
            if isinstance(columns, (unicode, str)):
                columns = [columns]
            list_with_keys += columns

        if not columns:
            #columns = self.col(tableName, dbname=dbname)
            list_with_keys += self.col(tableName, dbname=dbname)

        if select:       
            if isinstance(select, (unicode, str)):
                select = [select]
            list_with_keys += select

        #p(list(self.getlistlazy( tableName, columns=columns, select=select,  dbname=dbname, where=where, connector_where=connector_where, size_to_fetch=size_to_fetch,limit=limit, offset=offset)))
        generator = self.getlistlazy(tableName, columns=columns, select=select,  dbname=dbname, where=where, connector_where=connector_where, size_to_fetch=size_to_fetch,limit=limit, offset=offset, thread_name=thread_name, case_sensitiv=case_sensitiv,just_check_existence=just_check_existence, distinct=distinct)
        if just_check_existence:
            if next(generator):
                yield True
            else:
                yield False
            return 

        for row in generator:
            yield {k:v for k,v in zip(list_with_keys,row)}



    def getlistlazy(self, tableName, columns=False, select=False,  dbname="main", where=False, connector_where="AND", size_to_fetch=1000, limit=-1, offset=-1, thread_name="Thread0", case_sensitiv=True,just_check_existence=False, distinct=False):
        #self.logger.low_debug("GetListLazy was invoked.")
        cursor = self._intern_getter(tableName, columns=columns, select=select,  dbname=dbname, where=where, connector_where=connector_where,limit=limit, offset=offset, thread_name=thread_name,case_sensitiv=case_sensitiv, distinct=distinct)
        try:
            if cursor["status"]:
                #try:
                if just_check_existence:
                    #p(cursor["out_obj"].fetchone())

                    if cursor["out_obj"].fetchone():
                        yield True
                    else:
                        yield False
                    return 
     
                else:
                    while True:
                        #p(cursor, "cursor")
                        results = cursor["out_obj"].fetchmany(size_to_fetch)
                        #p(results, "results")
                        results = list(results)
                        if not results:
                            break
                        for row in results:
                            yield row

            else:
                self.logger.error("GetterError: Nor Cursor Element was passed from intern getter.")
                yield []
                return
        except Exception as e:
            self.logger.error("Exception was throw: '{}'. (cursor_obj='{}',tableName='{}', columns='{}', select='{}', where='{}', ) ".format(repr(e), cursor["out_obj"], tableName, columns, select, where))
            yield []
            return 

 

    def _intern_getter(self, tableName, columns=False, select=False,  dbname="main", where=False,
                        connector_where="AND", limit=-1, offset=-1, thread_name="Thread0",
                        case_sensitiv=True, distinct=False):
        # return cursor object
        #p((columns, select, where))
        #p(dbname, "2dbname")
        #self.logger.low_debug("InternGetter was invoked.")
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        tab_exist = self._check_if_table_exist(tableName, dbname=dbname)
        if not tab_exist["status"]:
            return tab_exist
        self._commit_if_inserts_was_did()


        if columns:
            #p((repr(columns), type(columns)))
            if isinstance(columns, (str, unicode)):
                columns = (columns,)
            #p((repr(columns), type(columns)))

            columns_existens = self._check_if_given_columns_exist(tableName, columns, dbname=dbname)
            if not columns_existens["status"]:
                return columns_existens

            if select:
                if isinstance(select, (str, unicode)):
                    select = (select,)
            else:
                select = ()
            #p((columns,select))
            try:
                select_conditions = db_helper.list_of_select_objects_to_str(columns+select)
            except TypeError:
                select_conditions = db_helper.list_of_select_objects_to_str(tuple(columns)+tuple(select))

        elif select:
            if isinstance(select, (str, unicode)):
                select = (select,)
            select_conditions = db_helper.list_of_select_objects_to_str(select)

        else:
            select_conditions = '*'

        #p(select_conditions, "select_conditions")

        if not  select_conditions:
            self.logger.error("TypeError: Select columns is not given in the right way!  '{}' was given. ".format(type(columns)), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        if where:
            where_cond_as_str = db_helper.where_condition_to_str(where, connector=connector_where)
            #p(where_cond_as_str)
            if not where_cond_as_str:
                self.logger.error("GetAllError: Where-Condition(s) wasn't compiled to String!", exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        if dbname  not in self.dbnames:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        distinct_tag = "DISTINCT" if distinct else ""

        if where:
            query = u'SELECT {} {} FROM  {}.{} \nWHERE {} LIMIT {} OFFSET {}'.format(distinct_tag,select_conditions, dbname, tableName, where_cond_as_str, limit, offset)
        else:
            query = u'SELECT {} {} FROM  {}.{} LIMIT {} OFFSET {}'.format(distinct_tag, select_conditions, dbname, tableName, limit, offset)

        if not case_sensitiv:
            query = query + " COLLATE NOCASE"

        query = query+";"


        #p(query, c="m")
        #sys.exit()
        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute(query)
            #p((self._threads_cursors[thread_name]), c="r")
            #return Status(status=True, out_obj=self._threads_cursors[thread_name])
            return Status(status=True, out_obj=self._threads_cursors[thread_name]) 
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            q = query.replace("\n", " ")
            try:
                q = q.decode("utf-8")
            except:
                pass
            self.logger.error(u"Exception was throw:  '{}' for following query: '{}'".format( repr(exception), q ), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))









    ##########################SQLITE Settings################


    def set_journal(self,mode_to_set, thread_name="Thread0",):
        modi = ["delete", "truncate", "persist", "memory", "wal", "off"]
        if mode_to_set.lower() in modi:
            return self._threads_cursors[thread_name].execute("PRAGMA journal_mode = {};".format(mode_to_set)).fetchall()
        else:
            self.logger.error("'{}'-Mode  is not supported. Use one of the following: '{}'. ".format(mode_to_set, modi))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


    def get_journal(self,thread_name="Thread0",):
        return self._threads_cursors[thread_name].execute("PRAGMA journal_mode;").fetchall()



    def set_synch(self,num, dbname="main",thread_name="Thread0",):
        #https://www.sqlite.org/pragma.html#pragma_synchronous
        if dbname not in self.dbnames:
            self.logger.error("'{}'-DB wasn't found in the current Instance. ".format(dbname))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        if num <= 3 and num >= 0:
            return self._threads_cursors[thread_name].execute("PRAGMA {}.synchronous={};".format(dbname,num)).fetchall()
        else:
            self.logger.error("'{}'-ModeNummer is not supported.  ".format(num))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

    def get_synch(self, dbname="main",thread_name="Thread0",):
        if dbname not in self.dbnames:
            self.logger.error("'{}'-DB wasn't found in the current Instance. ".format(dbname))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        return self._threads_cursors[thread_name].execute("PRAGMA {}.synchronous;".format(dbname)).fetchall()





    #self._cashed_list = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    #self._cashed_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))


    # def _is_many_values(self, values):
    #     values
    #         inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
    #         track_id = self._error_track_id.incr()
    #         self.logger.error_insertion("Throw Exception: '{}'. |ErrorTrackID:'{}'| InpObj:'{}'.".format(exception, track_id,inp_obj), exc_info=self._logger_traceback)
    #         self.error_insertion_counter.incr()
    #         return Status(status=False, track_id=track_id,
    #                     desc=str(exception),
    #                     inp_obj= (table_name, inp_obj), func_name=function_name(-2),
    #                     level="error_insertion", action="ignored",
    #                     error_name=exception.__class__.__name__,
    #                     exception=exception)

    def _dict_to_cash(self,table_name, inp_obj, dbname, commit_number,thread_name="Thread0"):
        if len(inp_obj) < 1:
                track_id = self._error_track_id.incr()
                msg = "DictTOCashError: Given Dict is empty! |ErrorTrackID:'{}'|".format(track_id)
                inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
                self.logger.outsorted_corpus("{} InpObj:'{}'.".format(msg,inp_obj), exc_info=self._logger_traceback)
                #self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                        desc=msg, func_name=function_name(-2),
                        level="outsorted_corpus", action="outsorted")
        ## Step 1: Type Recognition (many or unig elem pro key)
        try:
            #### Is it an list?
            new_val_list  = []
            ### Many Values
            for item in inp_obj.values():
                new_val_list.append([]+item)

            length = [len(item) for item in new_val_list]
            if len(set(length)) >1:
                track_id = self._error_track_id.incr()
                msg = "DictTOCashError: Given Dict Values has inconsistent length! This insertion was ignored! |ErrorTrackID:'{}'|".format(track_id)
                inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
                self.logger.error_insertion("{} InpObj:'{}'.".format(msg,inp_obj), exc_info=self._logger_traceback)
                self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                        desc=msg, func_name=function_name(-2),
                        level="error_insertion", action="ignored")

        except TypeError:
            try:
                ### Is there tuples?
                new_val_list  = []
                ### Many Values
                #p(21111)
                for item in inp_obj.values():
                    new_val_list.append(list(()+item))
                #p(2222)
                length = [len(item) for item in new_val_list ]
                #p(set(length), "length")
                if len(set(length)) >1:
                    #p(set(length), "length")
                    track_id = self._error_track_id.incr()
                    msg = "DictTOCashError: Given Dict Values has inconsistent length! This insertion was ignored! |ErrorTrackID:'{}'|".format(track_id)
                    inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
                    self.logger.error_insertion("{} InpObj:'{}'.".format(msg,inp_obj), exc_info=self._logger_traceback)
                    self.error_insertion_counter.incr()
                    return Status(status=False, track_id=track_id,
                            desc=msg, func_name=function_name(-2),
                            level="error_insertion", action="ignored")
            except TypeError:
                new_val_list = []
                for item in inp_obj.values():
                    new_val_list.append([item])

        except Exception as exception:
            #p(repr(exception))
            track_id = self._error_track_id.incr()
            msg = "DictTOCashError: Exception was encountered!  This insertion was ignored! |ErrorTrackID:'{}'|".format(track_id)
            inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("{} Exception: '{}'. InpObj:'{}'.".format(msg,exception,inp_obj), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False,
                desc=str(exception),
                level="error_insertion", action="ignored",
                error_name=exception.__class__.__name__,
                exception=exception)


        keys_in_cashed_dict = self._cashed_dict[commit_number][thread_name][dbname][table_name].keys()
        if keys_in_cashed_dict:
            values_length_in_cashed_dict = len(self._cashed_dict[commit_number][thread_name][dbname][table_name][keys_in_cashed_dict[0]])
            values_length_in_inp_dict = len(new_val_list[0])
            for key, val in zip(inp_obj.keys(), new_val_list):
                try:
                    keys_in_cashed_dict.remove(key)
                    self._cashed_dict[commit_number][thread_name][dbname][table_name][key] += val
                

                except ValueError:
                    ## following key wasn't before in the cashed dict
                    ### add None-Items, to ensure dict consistence
                    self._cashed_dict[commit_number][thread_name][dbname][table_name][key] += [None for i in xrange(values_length_in_cashed_dict)]
                    self._cashed_dict[commit_number][thread_name][dbname][table_name][key] += val

        else:## if cashed dict is empty 
            for key, val in zip(inp_obj.keys(), new_val_list):
                self._cashed_dict[commit_number][thread_name][dbname][table_name][key] += val


        # Step 3: if keys in cashed dict exist, which wasn't found in inp_dict, that insert empty values, to make cash_dict consistent 
        if keys_in_cashed_dict:
            ### if keys from key dict  stay exist, after compare them with keys from input_dict, that  insert empty items 
            values_length_in_inp_dict = len(new_val_list[0])
            for key in keys_in_cashed_dict:
                self._cashed_dict[commit_number][thread_name][dbname][table_name][key] += [None for i in xrange(values_length_in_inp_dict)]


        return Status(status=True, out_obj=0)




    def _list_to_cash(self,table_name, inp_obj, dbname, commit_number,thread_name="Thread0"):
        if len(inp_obj) < 1:
                track_id = self._error_track_id.incr()
                msg = "ListTOCashError: Given List is empty! |ErrorTrackID:'{}'|".format(track_id)
                inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
                self.logger.outsorted_corpus("{} InpObj:'{}'.".format(msg,inp_obj), exc_info=self._logger_traceback)
                #self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                        desc=msg, func_name=function_name(-2),
                        level="outsorted_corpus", action="outsorted")

        #p(inp_obj)
        #self._cashed_list[commit_number][thread_name][dbname][table_name]
        

        ## Step 1: Type Recognition (many or unig elem pro key)
        try:
            #### Is it an list?
            new_val_list  = []
            ### Many Values
            for item in inp_obj:
                new_val_list.append([]+item)

            length = [len(item) for item in new_val_list ]
            if len(set(length)) >1:
                track_id = self._error_track_id.incr()
                msg = "ListTOCashError: Given List Values has inconsistent length! This insertion was ignored! |ErrorTrackID:'{}'|".format(track_id)
                inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
                self.logger.error_insertion("{} InpObj:'{}'.".format(msg,inp_obj), exc_info=self._logger_traceback)
                self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                        desc=msg, func_name=function_name(-2),
                        level="error_insertion", action="ignored")
            #p(new_val_list, "1new_val_list")

        except TypeError:
            try:
                ### Is there tuples?
                new_val_list  = []
                ### Many Values
                #p(21111)
                for item in inp_obj:
                    new_val_list.append(list(()+item))
                #p(2222)
                length = [len(item) for item in new_val_list ]
                #p(set(length), "length")
                if len(set(length)) >1:
                    #p(set(length), "length")
                    track_id = self._error_track_id.incr()
                    msg = "ListTOCashError: Given List Values has inconsistent length! This insertion was ignored! |ErrorTrackID:'{}'|".format(track_id)
                    inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
                    self.logger.error_insertion("{} InpObj:'{}'.".format(msg,inp_obj), exc_info=self._logger_traceback)
                    self.error_insertion_counter.incr()
                    return Status(status=False, track_id=track_id,
                            desc=msg, func_name=function_name(-2),
                            level="error_insertion", action="ignored")
                #p(new_val_list, "2new_val_list")

            except TypeError:
                new_val_list = [inp_obj]
                # for item in inp_obj:
                #     new_val_list.append([item])
                #p(new_val_list, "3new_val_list")

        except Exception as exception:
            #p(repr(exception))
            track_id = self._error_track_id.incr()
            msg = "ListTOCashError: Exception was encountered!  This insertion was ignored! |ErrorTrackID:'{}'|".format(track_id)
            inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("{} Exception: '{}'. InpObj:'{}'.".format(msg,exception,inp_obj), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False,
                desc=str(exception),
                level="error_insertion", action="ignored",
                error_name=exception.__class__.__name__,
                exception=exception)


        #self._cashed_list[] = new_val_list
        self._cashed_list[commit_number][thread_name][dbname][table_name] += new_val_list





        return Status(status=True, out_obj=0)



    def _write_cashed_insertion_to_disc(self, write_just_this_commit_number=False, thread_name="Thread0", with_commit=False):
        #p("_write_cashed_insertion_to_disc")

        with self.locker:
            temp_insertion_counter = 0
            temp_outsorting_counter = 0
            if len(self._cashed_dict)>0:
                if write_just_this_commit_number:
                    if write_just_this_commit_number not in self._cashed_dict:
                        msg = "CashedWriterError: Given CommitNumber'{}' is not exist. It wasn't possible to write cashed Insertion into DB. ".format(write_just_this_commit_number)
                        self.logger.debug(msg)
                        return Status(status=True)
                    #temp_cashed_dict = self._cashed_dict[write_just_this_commit_number]

                if write_just_this_commit_number:
                    dict_to_work = {write_just_this_commit_number:self._cashed_dict[write_just_this_commit_number]}
                else:
                    dict_to_work = self._cashed_dict

                dict_to_delete = []
                for commit_number, commit_number_data in dict_to_work.iteritems():
                    for current_thread_name, thread_data in commit_number_data.iteritems():
                        for dbname, db_data in thread_data.iteritems():
                            for table_name, inp_dict in db_data.iteritems():
                                status =  self.insertdict(table_name, inp_dict, dbname, thread_name=thread_name)
                                if not status["status"]:
                                    #print status
                                    #if status["action"
                                    #self.logger.error("CashedInsertionErr(DICT): '{}'".format(status["desc"]))
                                    return status
                                else:
                                    temp_insertion_counter += status["out_obj"]
                                    temp_outsorting_counter += status["outsort"] 
                                    #del self._cashed_dict[commit_number][current_thread_name][dbname][table_name]
                                    dict_to_delete.append((commit_number,current_thread_name,dbname,table_name))
                                    # else:
                                    #     del self._cashed_dict[write_just_this_commit_number]
                                    #     #del self._cashed_dict
                                    #     #self._cashed_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))))

                if dict_to_delete:
                    for item in dict_to_delete:
                        del self._cashed_dict[item[0]][item[1]][item[2]][item[3]]

            if len(self._cashed_list)>0:
                if write_just_this_commit_number:
                    if write_just_this_commit_number not in self._cashed_list:
                        msg = "CashedWriterError: Given CommitNumber'{}' is not exist. It wasn't possible to write cashed Insertion into DB. ".format(write_just_this_commit_number)
                        self.logger.debug(msg)
                        return Status(status=True, desc=msg)
                    #temp_cashed_list = self._cashed_list[write_just_this_commit_number]

            
                if write_just_this_commit_number:
                    dict_to_work = {write_just_this_commit_number:self._cashed_list[write_just_this_commit_number]}
                else:
                    dict_to_work = self._cashed_list
                list_to_delete = []
                for commit_number, commit_number_data in dict_to_work.iteritems():
                    for current_thread_name, thread_data in commit_number_data.iteritems():
                        for dbname, db_data in thread_data.iteritems():
                            for table_name, inp_dict in db_data.iteritems():
                                status =  self.insertlist(table_name, inp_dict, dbname, thread_name=thread_name)
                                if not status["status"]:
                                    #print status
                                    #if status["action"
                                    #self.logger.error("CashedInsertionErr(DICT): '{}'".format(status["desc"]))
                                    return status
                                else:
                                    temp_insertion_counter += status["out_obj"]
                                    temp_outsorting_counter += status["outsort"]
                                    #del self._cashed_list[commit_number][current_thread_name][dbname][table_name]
                                    list_to_delete.append((commit_number,current_thread_name,dbname,table_name))
                
                if list_to_delete:
                    for item in list_to_delete:
                        del self._cashed_list[item[0]][item[1]][item[2]][item[3]]

                # if write_just_this_commit_number:
                #     del self._cashed_list[write_just_this_commit_number]
                # else:
                #     del self._cashed_list
                #     self._cashed_list = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
            if  with_commit:
                self._commits_with_lazy_writer.incr()
                self.commit

            return Status(status=True, out_obj=temp_insertion_counter, outsort=temp_outsorting_counter)
            #return Status(status=True, out_obj=temp_insertion_counter)




##########################DB-Setters##################

    def lazyinsert(self, table_name, inp_obj,  dbname="main", thread_name="Thread0", dict_to_list=False):
        #p(self._use_cash, "self._use_cash")
        # p((self._lazy_writer_number_inserts_after_last_commit, self._lazyness_border))
        try:
            #p((table_name, inp_obj))
            s =  self._check_db_should_exist()
            if not s["status"]:
                return s
            
            if dict_to_list:
                if isinstance(inp_obj, dict):
                    inp_obj = db_helper.dict_to_list(inp_obj, self.col(table_name, dbname=dbname))
                    
                    
            if isinstance(inp_obj, dict):
                if self._use_cash:
                    status = self._dict_to_cash(table_name, inp_obj, dbname, int(self._commits_with_lazy_writer),thread_name=thread_name)

                else:
                    status =  self.insertdict(table_name, inp_obj, dbname, thread_name=thread_name)

            elif isinstance(inp_obj, list):
                if self._use_cash:
                    status = self._list_to_cash(table_name, inp_obj, dbname, int(self._commits_with_lazy_writer),thread_name=thread_name)
                else:
                    status =  self.insertlist(table_name, inp_obj, dbname, thread_name=thread_name)

            else:
                track_id = self._error_track_id.incr()
                typ = type(inp_obj)
                self.logger.error("Not Supported type of lazy_writer. This type was given: '{}'. Please use one of the supported types: ['dict','list',]. |ErrorTrackID:'{}'|".format(typ, track_id), exc_info=self._logger_traceback)
                self.error_insertion_counter.incr()
                return Status(status=False, track_id=track_id,
                            desc="Not Supported type of lazy_writer.",
                            inp_obj= inp_obj, func_name=function_name(-2),
                            level="error", action="ignored",)


            if not status["status"]:
                return status      

            self._lazy_writer_number_inserts_after_last_commit.incr()

            with self.locker:
                if int(self._lazy_writer_number_inserts_after_last_commit) >=  self._lazyness_border:
                    #p("DBHANDLER: CASH WILL BE INSERTED!!!!")
                    temp_counter_insertion_after_last_commit = int(self._lazy_writer_number_inserts_after_last_commit)
                    self._lazy_writer_all_inserts_counter.incr(temp_counter_insertion_after_last_commit)
                    self._lazy_writer_number_inserts_after_last_commit.clear()
                    self._commits_with_lazy_writer.incr()
                    self._who_will_proceed_commit[thread_name] = int(self._commits_with_lazy_writer)
                    #p("DBHANDLER:CASH WAS  INSERTED!!!!")

            if thread_name in self._who_will_proceed_commit:
                temp_commit_number = self._who_will_proceed_commit[thread_name]
                del self._who_will_proceed_commit[thread_name]
                if self._use_cash:
                    status = self._write_cashed_insertion_to_disc(write_just_this_commit_number=temp_commit_number, thread_name=thread_name)
                    if not status["status"]:
                        return status

                self._commit()
                self.logger.info("LazyWriter: Last {} inserts was committed in the DB. ".format(temp_counter_insertion_after_last_commit))
            

            return status

        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            inp_obj = inp_obj if self._log_content else "RowContentLogger is Off."
            track_id = self._error_track_id.incr()
            self.logger.error_insertion("Throw Exception: '{}'. |ErrorTrackID:'{}'| InpObj:'{}'.".format(exception, track_id,inp_obj), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                        desc=str(exception),
                        inp_obj= (table_name, inp_obj), func_name=function_name(-2),
                        level="error_insertion", action="ignored",
                        error_name=exception.__class__.__name__,
                        exception=exception)






    def insertdict(self,table_name, inp_dict, dbname="main", thread_name="Thread0"):
        if not isinstance(inp_dict, dict):
            track_id = self._error_track_id.incr()
            self.logger.error("InsertDictError: Given object in not an dict! |ErrorTrackID:'{}'|".format(track_id), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                        desc="InsertDictError: Given object in not an dict!",
                        inp_obj= inp_dict, func_name=function_name(-2),
                        level="error", action="ignored")

        try:
            if self._make_backup:
                if dbname in self.not_initialized_dbs:
                    self._backup(dbname)

            random_value  = random.choice(inp_dict.values())
            type_mask = [type(value) for value in inp_dict.values()]
            if len(set(type_mask)) == 1:
                if isinstance(random_value, (list,tuple)):
                    #self.logger.low_debug("InsertDict: Many rows was found in the given dict. ")
                    return  self._insertdict_with_many_rows(table_name, inp_dict, dbname=dbname, thread_name=thread_name)

                else:
                    #self.logger.low_debug("InsertDict: One unique row was found in the given dict. ")
                    return  self._insertdict_with_one_row(table_name, inp_dict, dbname=dbname, thread_name=thread_name)

            else:
                #self.logger.low_debug("InsertDict: One unique row was found in the given dict. ")
                return self._insertdict_with_one_row(table_name, inp_dict, dbname=dbname, thread_name=thread_name)
        
            #p(self._log_content,"self._log_content")


        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            track_id = self._error_track_id.incr()
            inp_dict = inp_dict if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("InsertDictError: Following Exception was throw: '{}'. |ErrorTrackID:'{}'| Current Row: '{}'.".format(exception,track_id,inp_dict), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                        desc=str(exception),
                        inp_obj= inp_dict, func_name=function_name(-2),
                        level="error_insertion", action="ignored",
                        error_name=exception.__class__.__name__,
                        exception=exception)





    def insertlist(self,table_name, inp_list, dbname="main", thread_name="Thread0", ):
        
        if not isinstance(inp_list, list):
            track_id = self._error_track_id.incr()
            self.logger.error("InsertDictError: Given object in not an list! |ErrorTrackID:'{}'|".format(track_id), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                        desc="InsertDictError: Given object in not an list!",
                        inp_obj= inp_list, func_name=function_name(-2),
                        level="error", action="ignored")

        try:
            if self._make_backup:
                if dbname in self.not_initialized_dbs:
                    self._backup(dbname)

            random_value  = random.choice(inp_list)
            type_mask = [type(value) for value in inp_list]
            if len(set(type_mask)) == 1:
                if isinstance(random_value, (list,tuple)):
                    # self.logger.low_debug("InsertList: Many rows was found in the given list. ")
                    return self._insertlist_with_many_rows(table_name, inp_list, dbname=dbname, thread_name=thread_name)
                else:
                    # self.logger.low_debug("InsertList: One unique row was found in the given list. ")
                    return self._insertlist_with_one_row(table_name, inp_list, dbname=dbname, thread_name=thread_name)
            else:
                # self.logger.low_debug("InsertList: One unique row was found in the given list. ")
                return self._insertlist_with_one_row(table_name, inp_list, dbname=dbname, thread_name=thread_name)


        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            track_id = self._error_track_id.incr()
            inp_list = inp_list if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("InsertListError: Following Exception was throw: '{}'. |ErrorTrackID:'{}'| Current Row: '{}'.".format(exception,track_id,inp_list), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                        desc=str(exception),
                        inp_obj= inp_list, func_name=function_name(-2),
                        level="error_insertion", action="ignored",
                        error_name=exception.__class__.__name__,
                        exception=exception)




    def _insertdict_with_many_rows(self,table_name, inp_dict, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        # Check if attributes and values have the same length
        if not isinstance(inp_dict, dict):
            inp_dict = inp_dict if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("InsertDictError: InputDict is not an 'dict'.", exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        inp_dict = copy.deepcopy(inp_dict)

        status = self._dict_preprocessing_bevore_inserting(inp_dict, "many")
        if not status["status"]:
            return status

        columns = ', '.join(inp_dict.keys())
        placeholders = db_helper.values_to_placeholder(len(inp_dict))
        number_of_values = len(random.choice(inp_dict.values()))
        #p((number_of_values))

        data = self._dict_values_to_list_of_tuples(inp_dict)
        #p(data)
        if not data:
            inp_dict = inp_dict if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("Insertion: Insertion was failed! Current Raw: '{}'.".format(inp_dict ), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
 
        if dbname  not in self.dbnames:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        
           
        query = 'INSERT {} INTO {}.{} ({}) VALUES ({})'.format(self._double_items,dbname,table_name, columns, placeholders) 
        #p(query, c="r")

        if table_name in self.tables(dbname=dbname):
            status = self._executemany(query, values=data, dbname=dbname, thread_name=thread_name)
            if not status["status"]:
                status["inp_obj"] = data
                return status

            num=status["out_obj"].rowcount
            outsorted = number_of_values-num
            if table_name != "info":
                self.all_inserts_counter.incr(n=num)
                self.number_of_new_inserts_after_last_commit.incr(num)
            
            # self.logger.low_debug("Insertion:  Many rows was inserted into '{}.{}'-Table. ".format(table_name, dbname))
            #p(status["out_obj"].rowcount)
            if outsorted:
                track_id = self._error_track_id.incr()
                l_query = query if self._log_content else "!!LogContentDisable!!"
                l_values =  data if self._log_content else "!!LogContentDisable!!"
                self.logger.outsorted_corpus("'{}'-rows was outsorted/ignored while insertion process. (probably that was redundant rows.) |ErrorTrackID:'{}'|  InpQuery: '{}'.  InpValues: '{}'. ".format(outsorted,track_id,  l_query, l_values))
            return Status(status=True, out_obj=num, outsort=outsorted)

        else:
            track_id = self._error_track_id.incr()
            inp_dict = inp_dict if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("Insertion: Table ('{}') wasn't found or not exist. Please initialize the Info Table, before you may add any attributes. |ErrorTrackID:'{}'| CurrentRow: '{}'.".format(table_name, track_id ,inp_dict ), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                    desc="Table ('{}') wasn't found or not exist.".format(table_name),
                    inp_obj= inp_dict, 
                    level="error_insertion", action="ignored")
             



    def _insertdict_with_one_row(self,table_name, inp_dict, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        # Check if attributes and values have the same length
        if not isinstance(inp_dict, dict):
            self.logger.error_insertion("InsertDictError: InputDict is not form 'dict' Format.", exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        inp_dict = copy.deepcopy(inp_dict)

        status = self._dict_preprocessing_bevore_inserting(inp_dict, "one")
        if not status["status"]:
            return status

        columns = ', '.join(inp_dict.keys())
        placeholders = ':'+', :'.join(inp_dict.keys())

        if dbname  not in self.dbnames:
            self.logger.error_insertion("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        main_query = 'INSERT {} INTO {}.{} (%s) VALUES (%s)'.format(self._double_items,dbname,table_name) 
        query = main_query  % (columns, placeholders)

        if table_name in self.tables(dbname=dbname):
            status = self._execute(query, values=inp_dict, dbname=dbname, thread_name=thread_name)
            if not status["status"]:
                status["inp_obj"] = inp_dict
                return status


            num=status["out_obj"].rowcount
            outsorted = 1-num
            if table_name != "info":
                self.all_inserts_counter.incr(n=num)
                self.number_of_new_inserts_after_last_commit.incr(num)
            
            if outsorted:
                track_id = self._error_track_id.incr()
                l_query = query if self._log_content else "!!LogContentDisable!!"
                l_values =  inp_dict if self._log_content else "!!LogContentDisable!!"
                self.logger.outsorted_corpus("'{}'-rows was outsorted/ignored while insertion process. (probably that was redundant rows.) |ErrorTrackID:'{}'|  InpQuery: '{}'.  InpValues: '{}'. ".format(outsorted,track_id,  l_query, l_values))

            # self.logger.low_debug("Insertion: One row was inserted into '{}.{}'-Table. ".format(table_name, dbname))
            #p(status["out_obj"].rowcount)
            return Status(status=True, out_obj=num, outsort=outsorted)




        else:
            track_id = self._error_track_id.incr()
            inp_dict = inp_dict if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("Insertion: Table ('{}') wasn't found or not exist. Please initialize the Info Table, before you may add any attributes. |ErrorTrackID:'{}'| CurrentRow: '{}'.".format(table_name, track_id ,inp_dict ), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                    desc="Table ('{}') wasn't found or not exist.".format(table_name),
                    inp_obj= inp_dict, 
                    level="error_insertion", action="ignored")
             


    def _insertlist_with_many_rows(self,table_name, inp_list, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if dbname  not in self.dbnames:
            self.logger.error_insertion("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        number  = len(inp_list[0])
        #values_as_tuple = db_helper.values_to_tuple(inp_list, "many")
        values_as_list = db_helper.values_to_list(inp_list, "many")
        #

        if not values_as_list:
            self.logger.error_insertion("Given  Values wasn't packet into the list.", exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        
        query = 'INSERT {} INTO {}.{}  \nVALUES ({});'.format(self._double_items,dbname,table_name, db_helper.values_to_placeholder(number))

        if table_name in self.tables(dbname=dbname):
            status = self._executemany(query, values=values_as_list, dbname=dbname, thread_name=thread_name)
            if not status["status"]:
                status["inp_obj"] = inp_list
                return status


            num=status["out_obj"].rowcount
            outsorted = len(inp_list)-num
            if table_name != "info":
                self.all_inserts_counter.incr(num)
                self.number_of_new_inserts_after_last_commit.incr(num)
            
            if outsorted:
                track_id = self._error_track_id.incr()
                l_query = query if self._log_content else "!!LogContentDisable!!"
                l_values =  values_as_list if self._log_content else "!!LogContentDisable!!"
                self.logger.outsorted_corpus("'{}'-rows was outsorted/ignored while insertion process. (probably that was redundant rows.) |ErrorTrackID:'{}'|  InpQuery: '{}'.  InpValues: '{}'. ".format(outsorted,track_id,  l_query, l_values))

            # self.logger.low_debug("Insertion: Many row was inserted into '{}.{}'-Table. ".format(table_name, dbname))
            #p(status["out_obj"].rowcount)
            return Status(status=True, out_obj=num, outsort=outsorted)


        else:
            track_id = self._error_track_id.incr()
            inp_list = inp_list if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("Insertion: Table ('{}') wasn't found or not exist. Please initialize the Info Table, before you may add any attributes. |ErrorTrackID:'{}'| CurrentRow: '{}'.".format(table_name, track_id ,inp_list ), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                    desc="Table ('{}') wasn't found or not exist.".format(table_name),
                    inp_obj= inp_list, 
                    level="error_insertion", action="ignored")
             


    def _insertlist_with_one_row(self,table_name, inp_list, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if not isinstance(inp_list, (list, tuple)):
            self.logger.error_insertion("insertVError: Given Obj is not a list!", exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        #values_as_tuple = db_helper.values_to_tuple(inp_list, "one")
        values_as_list = db_helper.values_to_list(inp_list, "one")
        number  = len(inp_list)
        #p(self.colt("documents"))
        if  not values_as_list:
            self.logger.error_insertion("Given  Values wasn't packet into the list.", exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        if dbname  not in self.dbnames:
            self.logger.error_insertion("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        #p(values_as_list, c="m")
        query = 'INSERT {} INTO {}.{}  \nVALUES ({});'.format(self._double_items, dbname,table_name, db_helper.values_to_placeholder(number))
        #p((query, values_as_list), c="b")
        if table_name in self.tables(dbname=dbname):
            status = self._execute(query, values=values_as_list, dbname=dbname, thread_name=thread_name)
            if not status["status"]:
                status["inp_obj"] = inp_list
                return status

            num=status["out_obj"].rowcount
            outsorted = 1-num
            if table_name != "info":
                self.all_inserts_counter.incr(num)
                self.number_of_new_inserts_after_last_commit.incr(num)

            if outsorted:
                track_id = self._error_track_id.incr()
                l_query = query if self._log_content else "!!LogContentDisable!!"
                l_values =  values_as_list if self._log_content else "!!LogContentDisable!!"
                self.logger.outsorted_corpus("'{}'-rows was outsorted/ignored while insertion process. (probably that was redundant rows.) |ErrorTrackID:'{}'|  InpQuery: '{}'.  InpValues: '{}'. ".format(outsorted,track_id,  l_query, l_values))

            # self.logger.low_debug("Insertion: One row was inserted into '{}.{}'-Table. ".format(table_name, dbname))
            #p(status["out_obj"].rowcount)
            return Status(status=True, out_obj=num, outsort=outsorted)






        else:
            track_id = self._error_track_id.incr()
            inp_list = inp_list if self._log_content else "RowContentLogger is Off."
            self.logger.error_insertion("Insertion: Table ('{}') wasn't found or not exist. Please initialize the Info Table, before you may add any attributes. |ErrorTrackID:'{}'| CurrentRow: '{}'.".format(table_name, track_id ,inp_list ), exc_info=self._logger_traceback)
            self.error_insertion_counter.incr()
            return Status(status=False, track_id=track_id,
                    desc="Table ('{}') wasn't found or not exist.".format(table_name),
                    inp_obj= inp_list, 
                    level="error_insertion", action="ignored")
             


    def _dict_values_to_list_of_tuples(self,inp_dict):
        dict_as_list = []
        for rows in inp_dict.itervalues():
            #p(rows, c="b")
            #p(tuple(rows), c="b")
            dict_as_list.append(tuple(rows))

        #p(dict_as_list, "111")
        output = zip(*dict_as_list)
        #p(output, "222")
        return output




    def _dict_preprocessing_bevore_inserting(self, inp_dict, mode):
        try:
            for k,v in inp_dict.iteritems():
                if mode == "one":
                    if isinstance(v, (dict,tuple,list)):
                        inp_dict[k] = json.dumps(v)
                else:
                    values_list = []
                    for item in v:
                        if isinstance(item, (dict,tuple,list)):
                            values_list.append(json.dumps(item))
                        else:
                            values_list.append(item)
                    inp_dict[k] = values_list
            return Status(status=True)
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("DictPreprocessig: '{}' ".format(e), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))









    
 













##########################DB-Other Functions###############

#c.execute("alter table linksauthor add column '%s' 'float'" % author)
    
    def add_col(self, table_name, colname, typ, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()


        if dbname not in self.dbnames:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        if table_name not in self.tables():
            self.logger.error("'{}'-Table is not exist in the current DB. New Columns wasn't inserted.".format(table_name))
            return  False

        if colname in self.col(table_name):
            self.logger.error("'{}'-Column is already exist in the current DB. New Columns wasn't inserted.".format(table_name))
            return  False

        

        query = "ALTER TABLE {}.{} ADD COLUMN {} {} ".format(dbname,table_name,colname,typ)

        #p(query)
        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute(query)
            #tables_exist = cursor.fetchall()
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while inserting new columns into  '{}'-Table:  Exception: '{}'.".format(table_name, repr(exception) ), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        self._update_pragma_table_info(thread_name=thread_name)
        self._commit()
        self.logger.debug("'{}'-Column(s) was inserted into the '{}'-Table in '{}'-DB.".format(table_name,table_name,dbname))
        #self._update_temp_tablesList_in_instance(thread_name=thread_name)
        return Status(status=True)




    def get_db(self):
        return self._db


    def drop_table(self, table_name, dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()

        if dbname  in self.dbnames:
            query = "DROP TABLE  {}.{};".format(dbname,table_name)
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        #p(query)
        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute(query)
            #tables_exist = cursor.fetchall()
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while dropping the '{}'-Table:  '{}'.".format(table_name, repr(exception) ), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        
        self._commit()
        self.logger.debug("'{}'-Table was deleted from the DB (dbname: '{}')".format(table_name,dbname))
        self._update_temp_tablesList_in_instance(thread_name=thread_name)
        return Status(status=True)



    def update(self,table_name,columns_names,values, dbname="main", where=False, connector_where="AND", thread_name="Thread0"):
        # UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;

        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        # Check if attributes and values have the same length
        if len(columns_names) != len(values):
            self.logger.error("Length of given columns_names and values is not equal.", exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        columns_and_values_as_str = db_helper.columns_and_values_to_str(columns_names,values)

        if where:
            where_cond_as_str = db_helper.where_condition_to_str(where, connector=connector_where)
            if not where_cond_as_str:
                self.logger.error("GetAllError: Where-Condition(s) wasn't compiled to String!", exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        if dbname  in self.dbnames:
            if where:
                query = 'UPDATE {dbname}.{tableName}  \nSET {col_and_val} WHERE {where};'.format(col_and_val=columns_and_values_as_str, dbname=dbname, tableName=table_name, where=where_cond_as_str)
            else:
                query = 'UPDATE {dbname}.{tableName}  \nSET {col_and_val};'.format(col_and_val=columns_and_values_as_str, dbname=dbname, tableName=table_name)
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        if table_name in self.tables(dbname=dbname):
            try:
                #cursor = self._db.cursor()
                #p(query)
                self._threads_cursors[thread_name].execute(query)
                self._commit()
                return Status(status=True)
            except Exception as  exception:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("Something happens while updating the '{}'-Table:  '{}'.".format(table_name, repr(exception) ), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        else:
            self.logger.error("Table ('{}') wasn't found or not exist. Please initialize the Info Table, before you may add any attributes.".format(table_name), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def rollback(self):
        '''
        -> rollback to roll back any change to the database since the last call to commit.
        -> Please remember to always call commit to save the changes. If you close the connection using close or the connection to the file is lost (maybe the program finishes unexpectedly), not committed changes will be lost
        '''
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        temp_number_of_new_insertion_after_last_commit = int(self.number_of_new_inserts_after_last_commit)
        self._db.rollback()
        self.logger.info("ExternRollBack: '{}' insertions was rolled back.".format(temp_number_of_new_insertion_after_last_commit))
        self.number_of_new_inserts_after_last_commit.clear()
        return temp_number_of_new_insertion_after_last_commit



    def commit(self):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if self._use_cash:
            self._write_cashed_insertion_to_disc()
        #self._lazy_writer_counter = 0

        temp_number_of_new_insertion_after_last_commit = int(self.number_of_new_inserts_after_last_commit)
        #p(temp_number_of_new_insertion_after_last_commit, "temp_number_of_new_insertion_after_last_commit")
        self._db.commit()
        self.logger.info("ExternCommitter: DB was committed ({} last inserts was wrote on the disk)".format( int(self.number_of_new_inserts_after_last_commit) ) )

        self.inserts_was_committed.incr(int(self.number_of_new_inserts_after_last_commit))
        self.number_of_new_inserts_after_last_commit.clear()
        return temp_number_of_new_insertion_after_last_commit


    def _commit(self):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if self._use_cash:
            self._write_cashed_insertion_to_disc()

        temp_number_of_new_insertion_after_last_commit = int(self.number_of_new_inserts_after_last_commit)
        self._db.commit()
        self.logger.debug("InternCommitter: DB was committed ({} last insert(s) was wrote on the disk)".format( int(self.number_of_new_inserts_after_last_commit) ) )
        self.inserts_was_committed.incr(int(self.number_of_new_inserts_after_last_commit))
        self.number_of_new_inserts_after_last_commit.clear()
        return temp_number_of_new_insertion_after_last_commit




    def _default_db_closer(self, for_encryption=False):
        try:
            self._commit()
            if self._db:
                del self._threads_cursors
                gc.collect()
                self._db.close()
                self._init_instance_variables()
            else:
                msg = "No activ DB was found. There is nothing to close!"

                self.logger.error(msg)
                return Status(status=False, desc=msg)

            if for_encryption:
                msg = "DBExit: Current DB was closed! En-/Decryption Process will reopen the current DB."
            else:
                msg = "DBExit: DB was committed and closed. (all changes was saved on the disk)"
            
            return Status(status=True, desc=msg)
        except Exception,e:
            print_exc_plus() if self._ext_tb else ""
            msg = "ClossingError: DB-Closing return an Error: '{}' ".format(e)
            self.logger.error(msg, exc_info=self._logger_traceback)
            return Status(status=False, desc=msg)



    def close(self, for_encryption=False):
        s = self._default_db_closer(for_encryption=for_encryption)
        if s["status"]:
            self.logger.info(s['desc'])
        else:
            return s


    def _close(self, for_encryption=False):
    
        s = self._default_db_closer(for_encryption=for_encryption)
        if s["status"]:
            self.logger.debug(s['desc'])
        else:
            return s






    def addtable(self, table_name, attributs_names_with_types_as_list_with_tuples,dbname="main", constraints=False, thread_name="Thread0"):
        
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        #sys.exit()
        if table_name not in self.tables(dbname=dbname):
            #sys.exit()
            attributs_names_with_types_as_str = db_helper.columns_and_types_in_tuples_to_str(attributs_names_with_types_as_list_with_tuples)
            if not attributs_names_with_types_as_str:
                self.logger.error("Something was wrong by Converting attributes into string. Program was stoped!", exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            if constraints:
                if dbname:
                    if dbname  in self.dbnames:
                        query = 'CREATE TABLE {}.{} ({}\n{});'.format(dbname,table_name,attributs_names_with_types_as_str, constraints)
                    else:
                        self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
                        return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
                else:
                    query = 'CREATE TABLE {} ({}\n{});'.format(table_name,attributs_names_with_types_as_str, constraints)
            else:
                if dbname:
                    if dbname  in self.dbnames:
                        query = 'CREATE TABLE {}.{} ({});'.format(dbname,table_name,attributs_names_with_types_as_str)
                    else:
                        self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
                        return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
                else:
                    query = 'CREATE TABLE {} ({});'.format(table_name,attributs_names_with_types_as_str)
            #p( query)
            try:
                #cursor = self._db.cursor()
                self._threads_cursors[thread_name].execute(query)
                self._commit()
                self.logger.debug("'{}'-Table was added into '{}'-DB. ".format(table_name,dbname))
                self._update_temp_tablesList_in_instance(thread_name=thread_name)
                self._update_pragma_table_info(thread_name=thread_name)
                return Status(status=True)
            except sqlite.OperationalError, e:
                print_exc_plus() if self._ext_tb else ""
                if 'near "-"' in str(e):
                    self.logger.error("AddTableOperationalError: While adding Table-'{}'. Problem: '{}'. (It may be a Problem with using not allowed Symbols in the column name.  e.g.'-')\nProblem was found in the following query: '{}'.".format(table_name,e, query.replace("\n", "  ")), exc_info=self._logger_traceback)
                else:
                    self.logger.error("AddTableOperationalError: While adding Table-'{}'. Problem: '{}'. \nProblem was found in the following query: '{}'.".format(table_name,e, query.replace("\n", " ")), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        else:
            self.logger.error("'{}'-Table is already exist in the given DB. You can not initialize it one more time!".format(table_name), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


    def change_key(self, new_key_to_encryption, thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        if not self._check_should_be_str_or_unicode(new_key_to_encryption)["status"]:
            return self._check_should_be_str_or_unicode(new_key_to_encryption)["status"]

        if self._encryption_key:
            try:
                #cursor = self._db.cursor()
                self._threads_cursors[thread_name].execute("PRAGMA rekey = '{}';".format(new_key_to_encryption))
                self._commit()
                self._encryption_key = new_key_to_encryption
                self.logger.info("Encryption Key was changed!")
                return Status(status=True)
            except Exception as  exception:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("Something happens while changing of the encryption key:  '{}'.".format(repr(exception)), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        else:
            self.logger.warning("You cant change encryption key, because the current DataBase wasn't encrypted. You need first to encrypt the current DB and than you can change the encryption key.")
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def encrypte(self, key_to_encryption, dbname="main", thread_name="Thread0"):
        '''
        set key
        '''
        if dbname != "main":
            self.logger.error("Decryption could be done just for the main DataBase.")
            return Status(status=False)

        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        status= self._check_should_be_str_or_unicode(key_to_encryption)
        if not status["status"]:
            return status["status"]

        #p(status)
        if self._encryption_key:
            self.logger.critical("You can not encrypte the current DB, because it is already encrypted. What you can, it is just to change already setted key of encryption.")
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        path_to_temp_db = os.path.join(self.dirname(), "temp_encrypted.db")
        path_to_current_db = self.path()
        path_to_dir_with_current_db  = self.dirname()
        fname_of_the_current_db = self.fname()

        new_fname_of_encrypted_db= os.path.splitext(fname_of_the_current_db)[0]+"_encrypted"+os.path.splitext(fname_of_the_current_db)[1]
        new_path_to_current_encrypted_db = os.path.join(path_to_dir_with_current_db, new_fname_of_encrypted_db)
        #p(new_fname_of_encrypted_db)
        #p(self.dbnames, "1self.dbnames")
        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute("ATTACH DATABASE '{}' AS temp_encrypted KEY '{}';".format(path_to_temp_db, key_to_encryption))
            self._threads_cursors[thread_name].execute("SELECT sqlcipher_export('temp_encrypted');")
            self._threads_cursors[thread_name].execute("DETACH DATABASE temp_encrypted;")
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while Encryption:  '{}'.".format(repr(exception)), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        #p(self.dbnames, "2self.dbnames")
        if os.path.isfile(path_to_temp_db):
            self._close(for_encryption=True)
            os.rename(path_to_current_db, path_to_current_db+".temp")
            os.rename(path_to_temp_db, new_path_to_current_encrypted_db)

            s = self.connect(new_path_to_current_encrypted_db, encryption_key=key_to_encryption, reconnection=True, logger_debug=True)
            if os.path.isfile(new_path_to_current_encrypted_db) and s["status"]:
                os.remove(path_to_current_db+".temp")
                self.logger.debug("Temporary saved (old) DB was removed.")
                if self._attachedDBs_config_from_the_last_session:
                    s_reattach = self._reattach_dbs_after_closing_of_the_main_db()
                    if not  s_reattach["status"]:
                        return s_reattach
                #p(self.dbnames, "7self.dbnames")
                #self.logger.info("DB-Encryption end with success!")
                self.logger.info("Current DB was encrypted. NewName: {};  NewPath:'{}'.".format(new_fname_of_encrypted_db,new_path_to_current_encrypted_db)) 
                #p(self._db, c="m")
                return Status(status=True)
            else:
                self.logger.error("Encrypted DB wasn't found/connected. Encryption is fail! Roled back to non-encrypted DB.", exc_info=self._logger_traceback)
                os.rename(path_to_current_db+".temp", path_to_current_db)
                self.connect(path_to_current_db,reconnection=True,  logger_debug=True)
                return s

        else:
            self.logger.error("ENCRYPTION: TempDB wasn't found. Encryption is failed! Roled back to non-encrypted DB.", exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        


    def decrypte(self, thread_name="Thread0"):
        '''
        delete key
        '''
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        if not self._encryption_key:
            self.logger.critical("You can not decrypte the current DB, because it wasn't encrypted before.")
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        path_to_temp_db = os.path.join(self.dirname(), "temp_decrypted.db")
        path_to_current_db = self.path()
        path_to_dir_with_current_db  = self.dirname()
        fname_of_the_current_db = self.fname()

        new_fname_of_encrypted_db= os.path.splitext(fname_of_the_current_db)[0]+"_decrypted"+os.path.splitext(fname_of_the_current_db)[1]
        new_path_to_current_encrypted_db = os.path.join(path_to_dir_with_current_db, new_fname_of_encrypted_db)
        #p(new_fname_of_encrypted_db)

        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute("ATTACH DATABASE '{}' AS temp_decrypted KEY '';".format(path_to_temp_db))
            self._threads_cursors[thread_name].execute("SELECT sqlcipher_export('temp_decrypted');")
            #self.
            self._threads_cursors[thread_name].execute("DETACH DATABASE temp_decrypted;")

            if os.path.isfile(path_to_temp_db):

                self._close(for_encryption=True)
                #p(self._db, "conn5555")

                os.rename(path_to_current_db, path_to_current_db+".temp")
                os.rename(path_to_temp_db, new_path_to_current_encrypted_db)
                if os.path.isfile(new_path_to_current_encrypted_db) and self.connect(new_path_to_current_encrypted_db, reconnection=True, encryption_key=False, logger_debug=True)["status"]:
                    
                    self.logger.info("Current DB was decrypted. NewName: {};  NewPath:'{}'.".format(new_fname_of_encrypted_db,new_path_to_current_encrypted_db)) 
                    #self._reinitialize_logger(self, level=self._logger_level)
                    os.remove(path_to_current_db+".temp")
                    self.logger.debug("Temporary saved (old) DB was removed.")
                    if self._attachedDBs_config_from_the_last_session:
                        
                    
                        s_reattach = self._reattach_dbs_after_closing_of_the_main_db()
                        if not  s_reattach["status"]:
                            return s_reattach
                    self.logger.debug("DB-Decryption was end with success!")
                    #p(self._db, c="m")
                    return Status(status=True)
                else:
                    self.logger.error("Decrypted DB wasn't found/connected. Decryption is fail! Roled back to encrypted DB.", exc_info=self._logger_traceback)
                    os.rename(path_to_current_db+".temp", path_to_current_db)
                    self.connect(path_to_current_db,reconnection=True,  logger_debug=True)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            else:
                self.logger.error("DECRYPTION: TempDB wasn't found. Encryption is failed! Roled back to encrypted DB.", exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
    

        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while Decryption:  '{}'.".format(repr(exception)), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
######################################INTERN########################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################




###########################DB-Checker#########################

    def _check_should_be_str_or_unicode(self, giv_obj):
        if not isinstance(giv_obj, (str, unicode)):
            self.logger.error("Given Object is not from following type: (str, unicode).", exc_info=self._logger_traceback)
            return Status(status=False,
                            desc="Given Object is not from following type: (str, unicode).",
                            func_name=function_name(-3))
        else:
            return Status(status=True)


    def _check_if_given_columns_exist(self, tableName,columns, dbname="main"):
        #p((tableName,columns))
        # self.logger.low_debug("Check_if_given_columns_exist was invoke.")
        columns_from_db = self.col(tableName,dbname=dbname)
        for column in columns:
            if column not in  columns_from_db:
                if "json_extract" not in column:
                    msg = "Given Column '{}' is not exist in the following Table '{}' (dbname='{}') ".format(column,tableName,dbname)
                    self.logger.error(msg, exc_info=self._logger_traceback)
                    return Status(status=False,
                                    desc=msg,
                                    func_name=function_name(-3))
        
        # self.logger.low_debug("All Given Columns ({}) exist in the '{}'-table.".format(columns,tableName,))
        return Status(status=True)

    def _check_if_table_exist(self,tableName, dbname="main"):
        if tableName not in self.tables(dbname=dbname):
            self.logger.error("Given Table '{}' is not exist (dbname='{}')) ".format(tableName,dbname), exc_info=self._logger_traceback)
            return Status(status=False,
                            desc="Given Table '{}' is not exist (dbname='{}')) ".format(tableName,dbname),
                            func_name=function_name(-3))
        else:
            return Status(status=True)

    def _check_db_should_exist(self):
        #p("333")
        if not self._db:
            #p("33----")
            self.logger.error("No active DB was found. You need to connect or initialize a DB first, before you can make any operation on the DB.", exc_info=self._logger_traceback)
            return Status(status=False,
                            desc="No active DB was found.",
                            func_name=function_name(-3))
        else:
            return Status(status=True)


    def _check_db_should_not_exist(self):
    
        if self._db: 
            msg = "An active DB was found. You need to initialize new empty Instance of DB before you can do this operation."
            self.logger.error(msg, exc_info=self._logger_traceback)
            s = Status(status=False,
                            desc=msg,
                            func_name=function_name(-3))

            return s
        else:
            return Status(status=True)


    def _db_should_be_a_corpus(self):

        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        db_typ = self.get_attr(attributName="typ")

        if db_typ != "corpus":
            track_id = self._error_track_id.incr()
            self.logger.error("Active DB is from typ '{}'. But it should be from typ 'corpus'. |ErrorTrackID:'{}'|".format(db_typ, track_id), exc_info=self._logger_traceback)
            return Status(status=False, track_id=track_id,
                        desc="Active DB is from typ '{}'. But it should be from typ 'corpus'. ".format(db_typ),
                        func_name=function_name(-3))
        return Status(status=True)


    def _db_should_be_stats(self):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        db_typ = self.get_attr(attributName="typ")
        if db_typ != "stats":
            track_id = self._error_track_id.incr()
            self.logger.error("Active DB is from typ '{}'. But it should be from typ 'stats'. ".format(db_typ), exc_info=self._logger_traceback)
            return Status(status=False, track_id=track_id,
                        desc="Active DB is from typ '{}'. But it should be from typ 'stats'. ".format(db_typ),
                        func_name=function_name(-3))
        return Status(status=True)





    def _check_file_existens(self, path_to_file):
        if not os.path.isfile(path_to_file):
            track_id = self._error_track_id.incr()
            self.logger.error("DB-File wasn't found: ('{}').".format(path_to_file), exc_info=self._logger_traceback)
            return Status(status=False, track_id=track_id,
                        desc="DB-File wasn't found: ('{}').".format(path_to_file),
                        func_name=function_name(-3))
        else:
            return Status(status=True)

    def _get_compile_options(self, db):
        try:
            db.cursor
        except:
            self.logger.error("ExtensionLoaderError: Passed Obj is not an Sqlite-DB.", exc_info=self._logger_traceback)
            sys.exit()

        try:
            output_dict = defaultdict(list)            
            c = db.cursor()
            c.execute("PRAGMA compile_options;")
            fetched_data = c.fetchall()
            #p(fetched_data)
            for option in  fetched_data:
                if "=" in option[0]:
                    #p(option[0])
                    splitted_option = option[0].split("=")
                    output_dict[splitted_option[0]] = splitted_option[1]
                else:
                    #p(option[0],c="b")
                    output_dict["parameters"].append(option[0])

            return output_dict
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("CompilerOptionsGetterError: Something wrong is happens.See following Exception: '{}' ".format(e), exc_info=self._logger_traceback)
            sys.exit()

    def _check_if_threads_safe(self):
        if not self.compile_options:
            self.logger.error("DB-Compile Options wasn't found.")
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        try:
            if int(self.compile_options["THREADSAFE"]) == 0:
                self.logger.error("ThreadSafeCheckerError: Given Compilation of SQLITE3 Environment is unsafe to use SQLite in a multithreaded program. Following Tool (zas-rep-tool) was designed to work in multithreaded/multiprocessored Mode and requiring ThreadSafe (1 or 2) compilation of SQLITE3. Please recompile your SQLITE with one of the following options ['SQLITE_CONFIG_MULTITHREAD','SQLITE_CONFIG_SERIALIZED'). Read more here. 'https://www.sqlite.org/compile.html#threadsafe'. ")
                sys.exit()
            elif int(self.compile_options["THREADSAFE"]) == 1:
                self.logger.debug("ThreadSafeChecker(1): This SQLITE Compilation is safe for use in a multithreaded environment. Mode: Serialized (THREADSAFE=1). In serialized mode, SQLite can be safely used by multiple threads with no restriction. Read more: https://www.sqlite.org/threadsafe.html")
            
            elif int(self.compile_options["THREADSAFE"]) == 2:
                #self.logger.debug("ThreadSafeChecker: This SQLITE Compilation is safe for use in a multithreaded environment. Mode: Multi-thread (THREADSAFE=2). In this mode, SQLite can be safely used by multiple threads provided that no single database connection is used simultaneously in two or more threads. Read more: https://www.sqlite.org/threadsafe.html")
                self.logger.warning("ThreadSafeChecker(2): This SQLITE Compilation is safe for use in a multithreaded environment. Mode: Multi-thread (THREADSAFE=2) can be safely used by multiple threads provided that no single database connection is used simultaneously in two or more threads. Read more: https://www.sqlite.org/threadsafe.html")

        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("ThreadSafeCheckerError: Something wrong is happens. See following Exception: '{}' ".format(e), exc_info=self._logger_traceback)
            sys.exit()



    def _check_db_compilation_options(self, db):
        self.compile_options = self._get_compile_options(db)
        self._check_if_threads_safe()
        self._load_json1_extention_if_needed(db)


    def _load_json1_extention(self,db):
        try:
            db.cursor
        except:
            self.logger.error("ExtensionLoaderError: Passed Obj is not an Sqlite-DB.", exc_info=self._logger_traceback)
            sys.exit()

        i = 0
        while True:
            i += 1
            try:
                db.enable_load_extension(True)
                db.load_extension(DBHandler.path_to_json1)
                self.logger.debug("ExtensionLoader: 'json1'-Extension was loaded into SQLite.")
                return Status(status=True)
            except sqlite.OperationalError,e:
                if i == 2:
                    self.logger.error("It wasn't possible to compile json1 for SQLITE. Please compile 'JSON1'-C-Extension into '{}' manually.".format(DBHandler.path_to_json1))
                    sys.exit()
                if os.path.isfile(DBHandler.path_to_json1+".c"):
                    print_exc_plus() if self._ext_tb else ""
                    self.logger.debug("ExtensionLoaderError: 'json1'-Extension wasn't found in '{}'. Probably it wasn't compiled. Please compile this extension  before you can use it.".format(DBHandler.path_to_json1), exc_info=self._logger_traceback)
                    #command_str = "gcc -g -fPIC -shared {} -o {}".format(DBHandler.path_to_json1+".c", DBHandler.path_to_json1+".so")
                    #command = os.popen(command_str)
                    #execute = command.read()
                    #close = command.close()
                    #if mac "gcc -g -fPIC -dynamiclib YourCode.c -o YourCode.dylib"

                    args2 = ['gcc', '-g', '-fPIC', '-shared',DBHandler.path_to_json1+".c",'-o',DBHandler.path_to_json1]
                    answer = subprocess.Popen(args2).communicate()
                    self.logger.info("Compiled json1 wasn't found. Compilation process was started: ProcessDebug: '{}'. ".format(answer))
                    #self.logger.info("Compiled json1 wasn't found. Compilation process was started: ProcessDebug: '{}', '{}'  ".format(execute, close))
                    files = os.listdir(os.path.join(path_to_zas_rep_tools, "src/extensions/json1"))
                    #self.logger.critical("FILES::::: {}".format(files))
                    #sys.exit()
                else:
                    print_exc_plus() if self._ext_tb else ""
                    self.logger.error("ExtensionLoaderError: 'json1'-Extension and 'json' C-Source files wasn't found in '{}'. Please give the right path to json1.c File.".format(DBHandler.path_to_json1), exc_info=self._logger_traceback)
                    sys.exit()

            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("ExtensionLoaderError: Something wrong is happens. 'json1'-Extension wasn't loaded. See following Exception: '{}' ".format(e), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


    def _load_json1_extention_if_needed(self, db):
        if not self.compile_options:
            self.logger.error("DB-Compile Options wasn't found.")
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        try:
            if "ENABLE_JSON1" in self.compile_options["parameters"]:
                self.logger.debug("JSONExtentionChecker: Given Compilation of SQLITE3 Environment hat already enabled JSON Extension.")
                return Status(status=True)

            else:
                status = self._load_json1_extention(db)
                if "ENABLE_LOAD_EXTENSION" in self.compile_options["parameters"] or "OMIT_LOAD_EXTENSION" in self.compile_options["parameters"]:
                    if not status["status"]:
                        return status

                else:
                    self.logger.critical("ExtensionLoaderError: It seems like current Compilation of the SQLITE don't support loading of additional extension. But we will try to force it. ('ZAS-REP-TOOLS' requires loaded 'JSON1' extention. Please recompile your Version of SQLITE with following flags: 'SQLITE_OMIT_LOAD_EXTENSION' or 'SQLITE_ENABLE_JSON1'. See more here: https://www.sqlite.org/compile.html#threadsafe) ")
                    if not status["status"]:
                        return status

            return Status(status=True)

        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("ThreadSafeCheckerError: Something wrong is happens. See following Exception: '{}' ".format(e), exc_info=self._logger_traceback)
            sys.exit()















##############################################################################
###########################DB-Validation#######################
##############################################################################






    def _validation_DBfile(self, path_to_db, encryption_key=False,  thread_name="Thread0"):
        if os.path.isfile(path_to_db):
            try:
                _db = sqlite.connect(path_to_db, **self._arguments_for_connection)
                c = _db.cursor()
                self._check_db_compilation_options(_db)
                
                if encryption_key:
                    c.execute("PRAGMA key='{}';".format(encryption_key))
                    #self.is_encrypted = True
                c.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = c.fetchall()

            except sqlite.DatabaseError, e:
                print_exc_plus() if self._ext_tb else ""
                if encryption_key:
                    self.logger.error("ValidationError: '{}'. Or maybe a given Key is incorrect. Please give another one.  PathToDB: '{}'. ".format( e, path_to_db), exc_info=self._logger_traceback)
                else:
                    self.logger.error("ValidationError: '{}'. PathToDB: '{}'. ".format( e, path_to_db), exc_info=self._logger_traceback)
                
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
            except Exception as  exception:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("Something wrong happens while Validation '{}'. PathToDB: '{}'. ".format( repr(exception), path_to_db), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


            try:
                #c = _db.cursor()
                c.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = c.fetchall()
                #c = _db.cursor()
                # p(c)
                # p((c.cursor, c.connection))
                ## check Row Numbers
                c.execute("select count(*) from info;")
                rowNumbes = c.fetchone()[0]
                #sys.exit()
                if rowNumbes > 1:
                    self.logger.error("ValidationError: Info-Table has more as 1 row. It is incorrect!", exc_info=self._logger_traceback)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
                elif rowNumbes ==0:
                    self.logger.error("ValidationError: Info-Table is empty. It is incorrect!", exc_info=self._logger_traceback)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


                try:
                    ## Check existents of attribute typ
                    get_typ= c.execute("SELECT typ FROM info; ")
                    get_typ = c.fetchone()
                    if get_typ[0] == "stats":
                        stat_val_status = self._validate_statsDB(_db)
                        if not stat_val_status["status"]:
                            self.logger.warning("Validator is failed! Connected/Attached DB can not be used. Please choice another one.")
                        return stat_val_status
                    elif get_typ[0] == "corpus":
                        corp_val_status = self._validate_corpusDB(_db)
                        if not corp_val_status["status"]:
                            self.logger.warning("Validator is failed! Connected/Attached DB can not be used. Please choice another one.")
                        return corp_val_status
                    else:
                        self.logger.error("ValidationError: Unsupported DB-Type '{}' was found.".format(get_typ[0]), exc_info=self._logger_traceback)
                        return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

                except sqlite.OperationalError,  e:
                    print_exc_plus() if self._ext_tb else ""
                    self.logger.error("ValidationError:  '{}'. Impossible to get DB-Typ. PathToDB: '{}'. ".format( e, path_to_db), exc_info=self._logger_traceback)
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


            except Exception as  exception:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("ValidationError: Something wrong happens while Validation '{}'. PathToDB: '{}'. ".format( repr(exception), path_to_db), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            return Status(status=True)

        else:
            self.logger.error("Given DB-File is not exist: '{}'. ".format(path_to_db), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


    def _validate_corpusDB(self, db):

        ### Step 1: Attributes
        attributs_and_types = [(attr[0], attr[1].split(' ', 1 )[0])  for attr in db_helper.default_tables["corpus"]["info"]]

        c = db.cursor()
        c.execute("PRAGMA table_info('info'); ")
        columns_and_types = c.fetchall()
        columns_and_types = [(col[1], col[2])for col in columns_and_types]


        if set(columns_and_types) !=set(attributs_and_types):
            self.logger.error("CorpusDBValidationError: Given Stats-DB contain not correct attributes. Following col_and_types was extracted: '{}' and they are incorrect. Please use following data as golden standard: '{}'. ".format(columns_and_types, attributs_and_types), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        ## Step 2: Table Names
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        default_tables = ["documents"]
        extracted_tnames = [table_name[0] for table_name in tables]
        for defaultTable in default_tables:
            if defaultTable not in extracted_tnames:
                self.logger.error("CorpusDBValidationError: '{}'-default-Table wasn't found in the given Corpus-DB.".format(defaultTable), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        return Status(status=True, out_obj=db)

    def _validate_statsDB(self, db):

        ### Step 1: Attributes
        attributs_and_types = [(attr[0], attr[1].split(' ', 1 )[0])  for attr in db_helper.default_tables["stats"]["info"]]
        c = db.cursor()
        c.execute("PRAGMA table_info('info'); ")
        columns_and_types = c.fetchall()
        columns_and_types = [(col[1], col[2])for col in columns_and_types]
        #p(set(columns_and_types), "set(columns_and_types)")
        #p(set(attributs_and_types), "set(attributs_and_types)")

        if set(columns_and_types) !=set(attributs_and_types):
            self.logger.error("StatsDBValidationError: Given Stats-DB contain not correct attributes. Following col_and_types was extracted: '{}' and they are incorrect. Please use following data as golden standard: '{}'. ".format(columns_and_types, attributs_and_types), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



        ## Step 2: Table Names
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        default_tables = db_helper.default_tables["stats"].keys()
        #["repl_baseline", "redu_baseline","replications", "reduplications", "info"]
        extracted_tnames = [table_name[0] for table_name in tables]
        for defaultTable in default_tables:
            if defaultTable not in extracted_tnames:
                self.logger.error("StatsDBValidationError: '{}'-default-Table wasn't found in the given Stats-DB.".format(defaultTable), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        return Status(status=True, out_obj=db)













##############################################################################
###########################DB-OtherHelpers################
##############################################################################




    def _reinitialize_logger(self,  level=False):
        level = level if  level else self._logger_level
        ## Logger Reinitialisation
        self.l = ZASLogger(self.__class__.__name__ ,level=level, folder_for_log=self._logger_folder_to_save, logger_usage=self._logger_usage, save_logs=self._logger_save_logs)
        self.logger = self.l.getLogger()
        #self.logger = main_logger(self.__class__.__name__, level=level, folder_for_log=self._logger_folder_to_save, logger_usage=self._logger_usage, save_logs=self._logger_save_logs)
        self.logger.debug("Logger was reinitialized.")



    def _init_default_tables(self,typ, template=False, cols_and_types_in_doc=False):
        #p(template, "template")
        if template and template!="NULL":
            if template in DBHandler.templates:
                if cols_and_types_in_doc:
                    cols_and_types_in_doc += DBHandler.templates[template]
                else:
                    cols_and_types_in_doc = DBHandler.templates[template]
            else:
                self.logger.error("Given Template ('{}') is not exist".format(template), exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        #p(cols_and_types_in_doc)
        if typ == "corpus":
            #p(db_helper.default_tables["corpus"]["documents"]["basic"])
            #p(cols_and_types_in_doc)
            status= self._init_default_table("corpus", "documents", db_helper.default_tables["corpus"]["documents"]["basic"], addit_cols_and_types_in_doc=cols_and_types_in_doc, constraints=db_helper.default_constraints["corpus"]["documents"])
            if not status["status"]:
                return status
        
        elif typ == "stats":
            for table_name, columns in  db_helper.default_tables[typ].iteritems(): #foo = data.get("a",{}).get("b",{}).get("c",False)
                if table_name == "info":
                    continue
                status = self._init_default_table(typ, table_name, columns, constraints=db_helper.default_constraints.get(typ, False).get(table_name, False))
                if not status["status"]:
                    return status

        else:
            self.logger.error("Given typ of DB ('{}') is not exist.".format(typ), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        return Status(status=True)



    def _init_default_table(self, typ, tableName , default_collumns_with_types, addit_cols_and_types_in_doc=False, constraints=False):
        if typ.lower()=="corpus":
            if not self._db_should_be_a_corpus()["status"]:
                return self._db_should_be_a_corpus()
        elif typ.lower()=="stats":
            if not self._db_should_be_stats()["status"]:
                return self._db_should_be_stats()
        else:
            self.logger.error("Not supported typ ('{}') of DB. Please use one of the following DB-Types: '{}'. ".format(typ, DBHandler.supported_db_typs), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        if addit_cols_and_types_in_doc:
            columns_and_types = default_collumns_with_types + addit_cols_and_types_in_doc
        else:
            columns_and_types = default_collumns_with_types
        constraints_in_str = db_helper.constraints_list_to_str(constraints)
        #attributs_names_with_types_as_str = db_helper.columns_and_types_in_tuples_to_str(columns_and_types)
        status = self.addtable( tableName, columns_and_types,constraints=constraints_in_str)
        if not status["status"]:
            self.logger.error("InitDefaultTableError: '{}'-Table wasn't added into the {}-DB.".format(tableName, typ), exc_info=self._logger_traceback)
            return status

        self.logger.debug("{}-Table in {} was initialized".format(tableName, typ))
        return Status(status=True)


    def _commit_if_inserts_was_did(self):
        if int(self.number_of_new_inserts_after_last_commit) >0:
            self._commit()



    def _init_info_table(self, attributs_names):
        #str_attributs_names = db_helper.columns_and_types_in_tuples_to_str(attributs_names)
        status = self.addtable("info", attributs_names)
        if not status["status"]:
            return status

        self.logger.debug("Info-Table was initialized")
        return Status(status=True)



    def _del_attached_db_from_a_config_list(self, dbname):
        i=0
        found = False
        if self._attachedDBs_config:
            if dbname not  in self.dbnames:
                self.logger.warning("Given AttachedDataBaseName  is not exist: '{}'.".format(dbname))
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
            configs = self._get_configs_from_attached_DBList(dbname)
            if configs:
                self._attachedDBs_config.pop(configs[1])
                self.logger.debug("Given AttachedDB '{}' was successfully deleted from the configs-list. ".format(dbname))
                return Status(status=True)
                
            else:
                self.logger.warning("Given AttachedDB  '{}' wasn't deleted from the configs-liss. ".format(dbname))
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        else:
            self.logger.warning("List with attached DBs is already empty. You can not delete anything!")
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def _convert_if_needed_attr_to_bool(self, attributes):
        try:
            for attr_name, attr_value in attributes.iteritems():
                #attributes[]
                if isinstance(attr_value, (int, float)):
                    attr_value = str(attr_value)

                if attr_value is None:
                    #attr_value = False
                    attributes[attr_name] = False
                elif attr_value.lower() in self.bool_conv:
                    attributes[attr_name] = self.bool_conv[attr_value.lower()]
 
        except Exception, e:
            self.logger.error("Exception was encountered: '{}'. ".format(e))
            #p(dict(attributes.iteritems()))
            #sys.exit()


    def _reattach_dbs_after_closing_of_the_main_db(self):
        #p(repr(self._attachedDBs_config_from_the_last_session), "self._attachedDBs_config_from_the_last_session")
        #sys.exit()
        #p("22")
        #p(self.dbnames, "dbnames11")
        s =  self._check_db_should_exist()
        #p("666")
        if not s["status"]:
            return s

        #p(self._attachedDBs_config_from_the_last_session, "self._attachedDBs_config_from_the_last_session")
        if self._attachedDBs_config_from_the_last_session:
            for attached_db in self._attachedDBs_config_from_the_last_session:
                #p(attached_db, c="r")
                self.attach(attached_db[0], encryption_key=attached_db[2], reattaching=True)
            self.logger.debug("All attached DB was re-attached in the new connected Database")
            #p(self.dbnames, "dbnames22")
            return Status(status=True)
        else:
            self.logger.debug("There is no DBs to reattach (after closing of the main DB).")
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2), desc="There is no DBs to reattach (after closing of the main DB)")














##############################################################################
##########################Directly AttrGetterFromDB#(for updaters)##########
##############################################################################



    def _get_tables_from_db(self,dbname="main", thread_name="Thread0"):

        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        if dbname  in self.dbnames:
            query = "SELECT name FROM {}.sqlite_master WHERE type='table';".format(dbname)
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute(query)
            tables_exist = self._threads_cursors[thread_name].fetchall()
            self._commit()
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while Getting Tables:  '{}'.".format(repr(exception)), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        self.logger.low_debug("TableNames was get directly from DB.  (dbname: '{}')".format(dbname))

        return [table_name[0] for table_name in tables_exist]




    def _get_indexes_from_db(self,dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()

        if dbname  in self.dbnames:
            query = "SELECT * FROM {}.sqlite_master WHERE type='index';".format(dbname)
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute(query)
            indexes_exist = self._threads_cursors[thread_name].fetchall()
            self._commit()
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while Getting Indexes:  '{}'.".format(repr(exception)), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        self.logger.low_debug("IndexesNames was get directly from DB.  (dbname: '{}')".format(dbname))

        #return [index_name[0] for index_name in indexes_exist]
        #p(indexes_exist, c="r")
        return indexes_exist



    # def _get_db_names_from_main_db(self, thread_name="Thread0"):
    #     s =  self._check_db_should_exist()
    #     if not s["status"]:
    #         return s
    #     self._commit_if_inserts_was_did()
    #     try:
    #         #cur = self._db.cursor()
    #         self._threads_cursors[thread_name].execute("PRAGMA database_list")
    #         rows = self._threads_cursors[thread_name].fetchall()
    #     except Exception as  exception:
    #         print_exc_plus() if self._ext_tb else ""
    #         self.logger.error("Something happens while Getting DBNames:  '{}'.".format(repr(exception)), exc_info=self._logger_traceback)
    #         return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

    #     self.logger.debug("All DB-Names was taked directly from a Database.")
    #     if rows:
    #         return [ row[1] for row in rows]
    #     else:
    #         self.logger.critical("DBNamesGetter: No DB Names was returned from a DB")
    #         return []



    def _get_configs_from_attached_DBList(self, dbname):
        i=0
        found = False
        if self._attachedDBs_config:
            if dbname not  in self.dbnames:
                self.logger.warning("Given AttachedDataBaseName  is not exist: '{}'.".format(dbname))
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

            for attachedDB in self._attachedDBs_config:
                if attachedDB[1] == dbname:
                    #p((attachedDB[1], i))
                    found = i
                    break
                i=+1
            if isinstance(found, int):
                #self._attachedDBs_config.pop(found)
                self.logger.debug("Configs for '{}' was successfully found in the config-list of attached DBs. ".format(dbname))
                return (attachedDB, found)
            else:
                self.logger.warning("Configs for '{}' wasn't found!".format(dbname))
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        else:
            self.logger.warning("Configs-List with attached DBs is already empty. ")
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))



    def _get_all_attr_from_db(self,dbname="main", thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        
        if dbname  in self.dbnames:
            query = 'SELECT * FROM  {}.info;'.format( dbname)
        else:
            self.logger.error("Given dbName ('{}') is not exist in the current DB-Structure".format(dbname), exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))


        try:
            #cursor = self._db.cursor()
            self._threads_cursors[thread_name].execute(query)
            attribut = self._threads_cursors[thread_name].fetchall()[0]
            #p(attribut, "attribut")
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while Getting all Attributes from InfoTable of '{}'-DB: '{}'".format(dbname, exception), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))

        number_of_rows_info_table = self.rownum("info",dbname="main")
        if number_of_rows_info_table ==1:
            columns = self.col("info", dbname=dbname)
            return dict(zip(columns, list(attribut)))
        elif number_of_rows_info_table ==0:
            self.logger.error("Table 'info' is empty. Please set attributes bevor!", exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        else:
            self.logger.error("Table 'info' has more as 1 row. It's not correct. Please delete not needed rows.", exc_info=self._logger_traceback)
            return Status(status=None, track_id=self._error_track_id.incr(), func_name=function_name(-2))

 










##############################################################################
###########################Instance-Updater+###################
##############################################################################




    def _update_temp_tablesList_in_instance(self, thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        #p(self.dbnames, c="r")
        self._tables_dict = {}
        #if self.dbnames:
        for DBName in self.dbnames:
            self._tables_dict[DBName] = self._get_tables_from_db(dbname=DBName, thread_name=thread_name)
        #else:
        #    self._tables_dict['main'] = self._get_tables_from_db(dbname='main', thread_name=thread_name)
        
        self.logger.debug("Temporary TableList in the DB-Instance was updated!")




    def _update_temp_indexesList_in_instance(self, thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        #p(self.dbnames, c="r")
        self._indexes_dict = {}
        #if self.dbnames:
        for DBName in self.dbnames:
            self._indexes_dict[DBName] = self._get_indexes_from_db(dbname=DBName, thread_name=thread_name)
        #else:
        #    self._indexes_dict['main'] = self._get_indexes_from_db(dbname='main')
        
        self.logger.debug("Temporary IndexesList in the DB-Instance was updated!")



    def _update_temp_attributsList_in_instance(self, thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        #p(self.dbnames, c="r")
        self._attributs_dict = {}
        #if self.dbnames:
        for DBName in self.dbnames:
            attributes = self._get_all_attr_from_db(dbname=DBName, thread_name=thread_name)
            #p((DBName,attributes))
            #sys.exit()
            if attributes:
                self._convert_if_needed_attr_to_bool(attributes)
                self._attributs_dict[DBName] = attributes
            else:
                self.logger.error("Attributes wasn't updated!!!", exc_info=self._logger_traceback)
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        #else:
        #    self._attributs_dict['main'] = self._get_all_attr_from_db(dbname='main')
        
        self.logger.debug("Temporary List with all Attributes in the DB-Instance was updated!")



    def _update_temp_list_with_dbnames_in_instance(self,thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        #if not self._database_pragma_list:

        #p(self.dbnames, c="r")
        #self._database_pragma_list
        self.dbnames = [ row[1] for row in self._database_pragma_list]
        #self._get_db_names_from_main_db(thread_name=thread_name)
        #p(self.dbnames, c="m")
        if self.dbnames:
            self.logger.debug("Temporary List with DB-Names in the DB-Instance was updated!")
            return Status(status=True)
        else:
            self.logger.error("Empty List was returned.", exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        


    def _update_database_pragma_list(self, thread_name="Thread0"):
        s =  self._check_db_should_exist()
        if not s["status"]:
            return s
        self._commit_if_inserts_was_did()
        try:
            #cur = self._db.cursor()
            self._threads_cursors[thread_name].execute("PRAGMA database_list;")
            rows = self._threads_cursors[thread_name].fetchall()
            self._database_pragma_list = rows

            if not self._database_pragma_list:
                self.logger.critical("DBNamesGetter: No DB Names was returned from a DB")

            self.logger.debug("DatabasePragmaList was updated in the current instance. (got directly from the DB)")
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Something happens while getting DB-FileName:  '{}'.".format( repr(exception) ), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))


    #self._update_pragma_table_info(thread_name=thread_name)
    def _update_pragma_table_info(self, thread_name="Thread0"):
        try:
            s =  self._check_db_should_exist()
            if not s["status"]:
                return s
            self._commit_if_inserts_was_did()

            for dbname in self.dbnames:
                for table in self.tables(dbname=dbname):
                    query = "PRAGMA {}.table_info('{}'); ".format(dbname, table)
                    #cursor = self._db.cursor()
                    self._threads_cursors[thread_name].execute(query)
                    data = self._threads_cursors[thread_name].fetchall()
                    self._pragma_table_info[dbname][table] = data

            self.logger.debug("PragmaTableInfo was updated in the current instance. (got directly from the DB)")

        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("Encountered Exception: '{}' ".format(repr(exception) ), exc_info=self._logger_traceback)
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))







##############################################################################
###########################DB-Optimizer #########################
##############################################################################




    def _optimize(self, thread_name="Thread0", dbname="main"):
        pragma_pattern = "PRAGMA {}.{{}}".format(dbname)

 #"pclsjt"
        optimizer_names= {
                        "p":"page_size",
                        "c":"cache_size", #When you change the cache size using the cache_size pragma, the change only endures for the current session. The cache size reverts to the default value when the database is closed and reopened.
                        "l":"locking_mode",
                        "s":"synchronous",
                        "j":"journal_mode",
                        "t":"temp_store", 
                           }
        #p(self._optimizer_synchronous, "self._optimizer_synchronous")
        statement_setting = {
                        "p":self._optimizer_page_size,
                        "c":self._optimizer_cache_size,
                        "l":self._optimizer_locking_mode,
                        "s":self._optimizer_synchronous,
                        "j":self._optimizer_journal_mode,
                        "t":self._optimizer_temp_store
                        }

        s =  self._check_db_should_exist()
        if not s["status"]:
            return s

        #"c"
        #p((self._optimizer))
        #self._optimizer = "jlstc"
        extracted_optimizer_flags = []
        if self._optimizer:
            if self._optimizer != True:
                extracted_optimizer_flags = list(self._optimizer)


        if len(extracted_optimizer_flags)==0:
            extracted_optimizer_flags = optimizer_names.keys()

        t= type(self._optimizer)
        #p((self._optimizer, t,extracted_optimizer_flags))
        executed_statements = []
        cur = self._db.cursor()
        for flag in  extracted_optimizer_flags:
            if flag in optimizer_names:
                #if optimizer_names[flag]
                current_optimizer_name = optimizer_names[flag]
                current_optimizer_setting = str(statement_setting[flag]).lower()

                optimizer_statement = pragma_pattern.format(current_optimizer_name)
                query = "{} = {};".format(optimizer_statement, current_optimizer_setting)
                cur.execute(query)
                state = str(cur.execute(optimizer_statement+";").fetchall()[0][0]).lower()
                #p((query,state))
                executed_statements.append("Query: '{}'; Answer: '{}'. ".format(query,state))

                if current_optimizer_name in DBHandler.mapped_states:
                    #pass
                    mapped_states_k_by_v= DBHandler.mapped_states[current_optimizer_name]
                    mapped_states_v_by_k = {v: k for k, v in DBHandler.mapped_states[current_optimizer_name].iteritems()}
                    current_optimizer_setting = str(current_optimizer_setting).lower()
                    if current_optimizer_setting in mapped_states_k_by_v: 
                        if current_optimizer_setting != state:
                            self.logger.warning("OptimizerWarning: '{}' wasn't changed. (option_to_set:'{}'; getted_option_from_db:'{}')".format(current_optimizer_name,current_optimizer_setting,state))
                    elif current_optimizer_setting in mapped_states_v_by_k:
                        if mapped_states_v_by_k[current_optimizer_setting] != state:
                            self.logger.warning("OptimizerWarning: '{}' wasn't changed. (option_to_set:'{}'; getted_option_from_db:'{}')".format(current_optimizer_name,mapped_states_v_by_k[current_optimizer_setting],state))
                    else:
                        self.logger.error("OptimizerError: Wrong Argument! '{}'-Argument can not be set by '{}'. Use one of the following options: '{}'.  ".format(current_optimizer_name, current_optimizer_setting, mapped_states_k_by_v.values()))

                elif current_optimizer_name in DBHandler.non_mapped_states:
                    if current_optimizer_setting in DBHandler.non_mapped_states[current_optimizer_name]:
                        if state != current_optimizer_setting:
                            self.logger.warning("OptimizerWarning: '{}' wasn't changed. (option_to_set:'{}'; getted_option_from_db:'{}')".format(current_optimizer_name,current_optimizer_setting,state))
                    else:
                        self.logger.error("OptimizerError: Wrong Argument! '{}'-Argument can not be set by '{}'. Use one of the following options: '{}'.  ".format(current_optimizer_name, current_optimizer_setting, DBHandler.non_mapped_states[current_optimizer_name]))


            else:
                self.logger.error("Current Optimization-Flag ('{}') wasn't recognized and selected.".format(flag))

        if self._save_settings:
            executed_statements_as_str = "\n".join(executed_statements)
            self.logger.settings("Following Optimization Settings was selected: \n{}".format(executed_statements_as_str ))

        if len(executed_statements)>0:
            self.logger.info("Optimizer: '{}'-OptimizationStatements was executed!".format(len(executed_statements)))







##############################################################################
###########################Instance Cleaner##############
##############################################################################



    def _init_instance_variables(self):
        #InstanceAttributes: Initialization
        
        #dict()
        self._db = False
        self._encryption_key = False
        self.is_encrypted = False
        self.compile_options = False
        #p(self._attachedDBs_config_from_the_last_session,"self._attachedDBs_config_from_the_last_session")
        try:
            str(self._attachedDBs_config)
            self._attachedDBs_config_from_the_last_session = self._attachedDBs_config
        except AttributeError:
            self._attachedDBs_config = []
            self._attachedDBs_config_from_the_last_session = []

        #p(self._attachedDBs_config, "self._attachedDBs_config")
    
        self._attachedDBs_config = []
        self._tables_dict = {}
        self._indexes_dict = {}
        self._attributs_dict = {}
        self.dbnames = [] 
        self._created_backups = {}
        self._database_pragma_list = [] 
        self._pragma_table_info = defaultdict(lambda: defaultdict(list))
        self.not_initialized_dbs = []
        self._mainDB_was_initialized = None
        #self.lock = threading.Lock()
        self._cashed_list = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
        self._cashed_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))))
        self._who_will_proceed_commit = {}
        self._lazy_writer_all_inserts_counter = SharedCounterIntern()
        self._lazy_writer_number_inserts_after_last_commit = SharedCounterIntern()
        self._commits_with_lazy_writer = SharedCounterIntern()

        self.all_inserts_counter = SharedCounterIntern()
        self.number_of_new_inserts_after_last_commit = SharedCounterIntern()
        self.inserts_was_committed = SharedCounterIntern()
        self.error_insertion_counter = SharedCounterIntern()

        self.bool_conv = {'true': True, 'null': None, 
                         'false': False, }
        self._error_track_id = SharedCounterExtern()
        self.logger.low_debug('Intern InstanceAttributes was (re)-initialized')
        

        
    def _init_threads_cursors_obj(self):
        self._threads_cursors = defaultdict(self._db.cursor)


    def _del_backup(self, dbname):
        try:
            #p(self._created_backups,"self._created_backups", c="r")
            if dbname in self._created_backups:
                path_to_current_db = self._created_backups[dbname]
                #p(path_to_current_db, "path_to_current_db")
                #p(os.listdir(os.path.split(path_to_current_db)[0]), "os.listdir(self.tempdir_testdbs)")
                if os.path.isfile(path_to_current_db):
                    os.remove(path_to_current_db)
                    del self._created_backups[dbname]
                    self.logger.debug("BackUPRemover: Temporary BackUp for '{}'-DB was deleted. Path:'{}'.".format(dbname, path_to_current_db))
                    return Status(status=True)
                else:
                    self.logger.error("BackUPRemover: Following BackUp wasn't found on the disk: '{}'. (was ignored)  ".format(path_to_current_db))
                    return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
            else:
                self.logger.debug("For '{}'-DB any BackUps wasn't created.")
                return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))
        except Exception, e:
            self.logger.error("BackupRemover: Encountered Exception: '{}' ".format(e))
            return Status(status=False, track_id=self._error_track_id.incr(), func_name=function_name(-2))




