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
#
from __future__ import absolute_import

import os
import copy
import sys
import logging
import inspect
import shutil
import traceback
#import shelve
import time
import json
from collections import defaultdict
from raven import Client
from cached_property import cached_property
import inspect
from consolemenu import *
from consolemenu.items import *
from validate_email import validate_email
import urllib2
import twitter
from nltk.tokenize import TweetTokenizer
from nose.tools import nottest

from  zas_rep_tools_data.utils import path_to_data_folder, path_to_models, path_to_someweta_models, path_to_stop_words
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, MyZODB,transaction, path_to_zas_rep_tools, internet_on, make_zipfile, instance_info, SharedCounterExtern, SharedCounterIntern, Status, function_name,statusesTstring
import zas_rep_tools.src.utils.db_helper as db_helper
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus
from zas_rep_tools.src.classes.exporter import Exporter
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.classes.stats import Stats
from zas_rep_tools.src.utils.zaslogger import ZASLogger
from zas_rep_tools.src.classes.basecontent import BaseContent
from zas_rep_tools.src.utils.configer_helpers import ConfigerData

@nottest
class TestsConfiger(BaseContent,ConfigerData):
    def __init__(self, rewrite=False,stop_if_db_already_exist = True,**kwargs):
        super(type(self), self).__init__(**kwargs)

        #Input: Encapsulation:
        self._rewrite = rewrite
        self._stop_if_db_already_exist = stop_if_db_already_exist


        #InstanceAttributes: Initialization
        self._path_to_zas_rep_tools = path_to_zas_rep_tools
        self._path_to_user_config_data = os.path.join(self._path_to_zas_rep_tools, "user_config/user_data.fs")
        self._path_to_zas_rep_tools_data = path_to_data_folder
        self._path_to_zas_rep_tools_someweta_models = path_to_someweta_models
        self._path_to_zas_rep_tools_stop_words = path_to_stop_words

        #self._get_user_config_db() 
        if not self._check_correctness_of_the_test_data():
            self.logger.error("TestDataCorruption: Please check test data.", exc_info=self._logger_traceback)
            sys.exit()

        self.logger.debug('Intern InstanceAttributes was initialized')

        self.logger.debug('An instance of {}() was created '.format(self.__class__.__name__))


        ## Log Settings of the Instance
        attr_to_flag = ["_types_folder_names_of_testsets","_test_dbs", "_init_info_data", "_columns_in_doc_table", "_columns_in_info_tabel", "_columns_in_stats_tables", "_text_elements_collection"]
        attr_to_len = False
        self._log_settings(attr_to_flag =attr_to_flag,attr_to_len =attr_to_len)


        ############################################################
        ####################__init__end#############################
        ############################################################

    def __del__(self):
        pass
        #super(type(self), self).__del__()




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

    def row_text_elements(self, lang="all"):
        return copy.deepcopy(self._row_text_elements(lang=lang))
    
    def text_elements(self, token=True, unicode_str=True,lang="all"):
        return copy.deepcopy(self._text_elements(token=token, unicode_str=unicode_str, lang=lang))

    def docs_row_values(self,token=True, unicode_str=True, lang="all"):
        return copy.deepcopy(self._docs_row_values(token=token,unicode_str=unicode_str, lang=lang))

    def docs_row_dict(self, token=True, unicode_str=True, all_values=False, lang="all"):
        '''
        just one dict with colums as key and list of all values as values for each columns()key
        '''
        return copy.deepcopy(self._docs_row_dict(token=token, unicode_str=unicode_str, all_values=all_values, lang=lang))

    def docs_row_dicts(self, token=True, unicode_str=True,  lang="all"):
        '''
        list of dicts  with colums and values for each row
        '''
        return copy.deepcopy(self._docs_row_dicts(token=token, unicode_str=unicode_str, lang=lang))



    ###########################Config Values#######################

    @cached_property
    def path_to_zas_rep_tools(self):
        return copy.deepcopy(self._path_to_zas_rep_tools)

    @cached_property
    def path_to_zas_rep_tools_data(self):
        return copy.deepcopy(self._path_to_zas_rep_tools_data)


    @nottest
    @cached_property
    def path_to_testdbs(self):
        return copy.deepcopy(self._path_to_testdbs)       

    @nottest
    @cached_property
    def test_dbs(self):
        return copy.deepcopy(self._test_dbs)             

    @cached_property
    def init_info_data(self):
        return copy.deepcopy(self._init_info_data)     

    @cached_property
    def columns_in_doc_table(self):
         return copy.deepcopy(self._columns_in_doc_table)            

    @cached_property
    def columns_in_info_tabel(self):
        return copy.deepcopy(self._columns_in_info_tabel)             

    @cached_property
    def columns_in_stats_tables(self):
        return copy.deepcopy(self._columns_in_stats_tables)     

    @nottest
    @cached_property
    def path_to_testsets(self):
         return copy.deepcopy(self._path_to_testsets)   

    @cached_property
    def types_folder_names_of_testsets(self):
         return copy.deepcopy(self._types_folder_names_of_testsets)  


    # def clean_user_data(self):
    #     if self._user_data.clean():
    #         return True
    #     else:
    #         return False

    # def get_data_from_user(self, user_info_to_get=False, rewrite=False):
    #     if not rewrite:
    #         rewrite = self._rewrite
    #     if user_info_to_get:
    #         if isinstance(user_info_to_get, (unicode, str)):
    #             user_info_to_get = [user_info_to_get]
    #     else:
    #         user_info_to_get = self._suported_user_info


    #     for user_info_name in user_info_to_get:
    #         if user_info_name not in self._suported_user_info:
    #             self.logger.error("UserDataGetterError:  '{}' - data not supported.  ".format(user_info_name), exc_info=self._logger_traceback)
    #             continue

    #         if user_info_name == "error_tracking":
    #             if rewrite:
    #                 self._cli_menu_error_agreement()
    #                 continue

    #             if "error_tracking" not in self._user_data:
    #                 self._cli_menu_error_agreement()

    #         elif user_info_name == "project_folder":
    #             if rewrite:
    #                 self._cli_menu_get_from_user_project_folder()
    #                 continue
    #             if "project_folder" not in self._user_data:
    #                 self._cli_menu_get_from_user_project_folder()

    #         elif user_info_name == "twitter_creditials":
    #             if rewrite:
    #                 self._cli_menu_get_from_user_twitter_credentials()
    #                 continue

    #             if "twitter_creditials" not in self._user_data:
    #                 self._cli_menu_get_from_user_twitter_credentials()


    #         elif user_info_name == "email":
    #             if rewrite:
    #                 self._cli_menu_get_from_user_emails()
    #                 continue

    #             if "email" not in self._user_data:
    #                 self._cli_menu_get_from_user_emails()

    #         else:
    #             self.logger.critical("Not supported user_data_getter ('{}').".format(user_info_name))


    @nottest
    def create_test_data(self, abs_path_to_storage_place=False, use_original_classes = True, corp_lang_classification=False, 
                         corp_pos_tagger=True, corp_sent_splitter=True, corp_sentiment_analyzer=True, status_bar=True,
                         corp_log_ignored=False, use_test_pos_tagger=False,rewrite=False):
        self.create_testsets(rewrite=rewrite,abs_path_to_storage_place=abs_path_to_storage_place,silent_ignore = True)
        if not self.create_test_dbs(rewrite=rewrite, abs_path_to_storage_place=abs_path_to_storage_place, use_original_classes=use_original_classes, 
                            corp_lang_classification=corp_lang_classification, corp_log_ignored=corp_log_ignored,
                            corp_pos_tagger=corp_pos_tagger, corp_sent_splitter=corp_sent_splitter,
                            corp_sentiment_analyzer=corp_sentiment_analyzer, status_bar=status_bar,
                            use_test_pos_tagger=use_test_pos_tagger):
            return False
        self.logger.info("Test Data was initialized.")
        return True


    @nottest
    def create_test_dbs(self, rewrite=False, abs_path_to_storage_place = False,corp_log_ignored=False,
                        use_original_classes = True, corp_lang_classification=True, use_test_pos_tagger=False,
                        corp_pos_tagger=True, corp_sent_splitter=True, corp_sentiment_analyzer=True, status_bar=True):
        try:
            if not abs_path_to_storage_place:
                abs_path_to_storage_place = os.path.join(self._path_to_zas_rep_tools, self._path_to_testdbs)
            ### clean journal files
            exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
            exist_fnames_in_dir = [fname for fname in exist_fnames_in_dir if ".db-journal" in fname]
            if exist_fnames_in_dir:
                for fname in exist_fnames_in_dir:
                    os.remove(os.path.join(abs_path_to_storage_place, fname))
                msg = "'{}' '.db-journal' files was deleted. ".format(len(exist_fnames_in_dir))
                self.logger.critical(msg)
                #p(msg, "CRITICAL", c="r")

            if not  rewrite:
                rewrite = self._rewrite
            #for 
            exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
            num = len(exist_fnames_in_dir)
            #p((num, exist_fnames_in_dir), "exist_fnames_in_dir")
            exist_fnames_in_dir = [fname for fname in exist_fnames_in_dir if (".db" in fname) and (".db-journal" not in fname)]
            fnames_test_db = [fname for encr, encr_data in self._test_dbs.items() for template_name, template_name_data in encr_data.items() for lang, lang_data in template_name_data.items() for db_type, fname in lang_data.items()]
            test_db_num = len(fnames_test_db)
            #p((fnames_test_db,exist_fnames_in_dir,test_db_num), "fnames_test_db")
            clean = False
            if len(exist_fnames_in_dir) != len(fnames_test_db):
                clean = True
                self.logger.critical("Some TestDB are missing. There was found '{}'-DBs. But it should be '{}'. Process of TestDB Creation will be started. ".format(len(exist_fnames_in_dir), len(fnames_test_db)))

            else:
                for fname in fnames_test_db:
                    if fname not in exist_fnames_in_dir:
                        msg = "Some TestDB are missing. (eg: '{}') Process of TestDB Creation will be started. ".format(fname)
                        self.logger.critical(msg)
                        #p(msg, "CRITICAL", c="r")
                        clean = True
                        break 

            if clean:
                clean = False
                for fname in exist_fnames_in_dir:
                    os.remove(os.path.join(abs_path_to_storage_place, fname))
                exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
                exist_fnames_in_dir = [fname for fname in exist_fnames_in_dir if ".db-journal" in fname]
                for fname in exist_fnames_in_dir:
                    os.remove(os.path.join(abs_path_to_storage_place, fname))

            activ_corp_dbs = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))) )
            for template_name, init_data in  self._init_info_data.iteritems():
                #p(template_name)
                for encryption in ["plaintext", "encrypted"]:
                    for dbtype in ["corpus", "stats"]:
                        # if exist  and rewrite=True -> remove existed db


                        #p(self._columns_in_info_tabel[dbtype])
                        dbname = self._init_info_data[template_name]["name"]
                        #language = self._init_info_data[template_name]["language"]
                        visibility = self._init_info_data[template_name]["visibility"]
                        platform_name = self._init_info_data[template_name]["platform_name"]
                        license = self._init_info_data[template_name]["license"]
                        template_name = self._init_info_data[template_name]["template_name"]
                        version = self._init_info_data[template_name]["version"]
                        source = self._init_info_data[template_name]["source"]
                        encryption_key = self._init_info_data[template_name]["encryption_key"][dbtype] if  encryption=="encrypted" else False
                        corpus_id = self._init_info_data[template_name]["id"]["corpus"]
                        stats_id = self._init_info_data[template_name]["id"]["stats"]
                        #p((dbtype, encryption_key))
                        
                        # for which languages create 
                        if encryption == "encrypted":
                            if template_name == "twitter":
                                languages = ["de"]
                            elif template_name == "blogger":
                                continue
                                #languages = ["en"]

                        elif encryption == "plaintext":
                            if template_name == "twitter":
                                continue
                                #languages = ["de"]
                            elif template_name == "blogger":
                                languages = ["de", "en", "test"]

                        for language in languages:

                            # If Rewrite is on, delete  db for current attributes. if this exist in the 'self._test_dbs'. If not, than ignore.
                            try:
                                path_to_db = os.path.join(abs_path_to_storage_place, self._test_dbs[encryption][template_name][language][dbtype])
                                if rewrite:
                                    if os.path.isfile(path_to_db):
                                        os.remove(path_to_db)
                                        self.logger.debug("RewriteOptionIsON: Following DB was deleted from TestDBFolder: '{}'. TestDBCreationScript will try to created this DB.".format(path_to_db))
                                    else:
                                        #self.logger.debug("11111{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                        self.logger.debug("RewriteOptionIsON: Following DB wasn't found in the TestDBFolder and wasn't deleted: '{}'. TestDBCreationScript will try to created this DB.".format(path_to_db))              
                                else:
                                    if os.path.isfile(path_to_db):
                                        self.logger.debug("RewriteOptionIsOFF: '{}'-DB exist and will not be rewrited/recreated.".format(path_to_db))
                                        continue

                            except KeyError, k:
                                self.logger.debug("KeyError: DBName for '{}:{}:{}:{}' is not exist in the 'self._test_dbs'. TestDBCreationScript will try to created this DB. ".format(encryption,template_name,language,dbtype))
                                continue
                            except Exception, e:
                                self.logger.error("See Exception: '{}'. (line 703). Creation of the TestDBs was aborted.".format(e), exc_info=self._logger_traceback)
                                sy.exit()

                            #self.logger.debug("2222{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                            db_id = corpus_id if dbtype == "corpus" else stats_id
                            self.logger.info("TestDBCreationProcess: Was started for DB with following attributes: 'dbtype='{}'; id='{}'; encryption='{}'; template_name='{}'; language='{}'. ".format(dbtype, db_id,encryption,template_name,language ))
                            if dbtype=="corpus":
                                #self.logger.debug("3333{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                if not use_original_classes:
                                    db = DBHandler(logger_level=logging.ERROR,logger_traceback=self._logger_traceback,
                                            logger_folder_to_save=self._logger_folder_to_save,logger_usage=self._logger_usage,
                                            logger_save_logs= self._logger_save_logs, mode=self._mode,
                                            error_tracking=self._error_tracking,  ext_tb= self._ext_tb,
                                            stop_if_db_already_exist=self._stop_if_db_already_exist, rewrite=self._rewrite)
                                    was_initialized = db.init(dbtype, abs_path_to_storage_place, dbname, language, visibility, platform_name=platform_name, license=license , template_name=template_name, version=version , source=source, corpus_id=corpus_id, stats_id=stats_id, encryption_key=encryption_key)["status"]
                                    # self.logger.critical("was_initialized={}".format(was_initialized))
                                    # sys.exit()
                                    #!!!!
                                    #self.logger.debug("444{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                    if not was_initialized:
                                        if self._stop_if_db_already_exist:
                                            self.logger.debug("DBInitialisation: DBName for '{}:{}:{}:{}' wasn't initialized. Since 'self._stop_if_db_already_exist'-Option is on, current Script will ignore current DB and will try to create next one.".format(encryption,template_name,language,dbtype))
                                            continue
                                        else:
                                            self.logger.error("DBInitialisationError: DBName for '{}:{}:{}:{}' wasn't initialized. TestDBCreation was aborted.".format(encryption,template_name,language,dbtype))
                                            return False
                                    #self.logger.debug("5555{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                    rows_to_insert = self.docs_row_values(token=True, unicode_str=True)[template_name]
                                    path_to_db = db.path()
                                    #self.logger.debug("6666{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                    if not path_to_db:
                                        self.logger.error("Path for current DB wasn't getted. Probably current corpus has InitializationError. TestDBCreation was aborted.")
                                        sys.exit()

                                    db.lazyinsert("documents",rows_to_insert)
                                    #self.logger.debug("77777{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                    #p(( len(db.getall("documents")), len(rows_to_insert)))
                                    if "Connection" not in str(type(db)):
                                        pass

                                    #p((len(db.getall("documents")) , len(rows_to_insert)), c="r")
                                    
                                    if len(db.getall("documents")) != len(rows_to_insert):
                                        
                                        #db.close()
                                        #p(db._db)
                                        os.remove(path_to_db)
                                        #shutil.rmtree(path_to_db)
                                        self.logger.error("TestDBsCreation(InsertionError): Not all rows was correctly inserted into DB. This db was ignored and not created.", exc_info=self._logger_traceback)
                                        #sys.exit()
                                        sys.exit()
                                        continue
                                    db.commit()
                                    db.close()

                                else:
                                    #if use_test_pos_tagger and language == "en":
                                    #    corp_pos_tagger = "tweetnlp" if corp_pos_tagger else corp_pos_tagger
                                    #else:
                                    #    corp_pos_tagger = True if corp_pos_tagger else False
                                    #if corp_language:
                                    #    language = corp_language
                                    #p((corp_pos_tagger,language), "pos_tagger")
                                    corp = Corpus(logger_level=logging.ERROR, logger_traceback=self._logger_traceback,
                                                    logger_folder_to_save=self._logger_folder_to_save, use_test_pos_tagger=use_test_pos_tagger,
                                                    logger_usage=self._logger_usage, logger_save_logs= self._logger_save_logs,
                                                    mode=self._mode ,  error_tracking=self._error_tracking,  ext_tb= self._ext_tb,
                                                    stop_if_db_already_exist=self._stop_if_db_already_exist, status_bar=status_bar,
                                                    rewrite=self._rewrite)
                                    #p(corp.info())
                                    #self.logger.debug("444{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                    was_initialized = corp.init(abs_path_to_storage_place,dbname, language, visibility,platform_name,
                                                    license=license , template_name=template_name, version=version, source=source,
                                                    corpus_id=corpus_id, encryption_key=encryption_key,
                                                    lang_classification=corp_lang_classification,
                                                    pos_tagger=corp_pos_tagger, sent_splitter=corp_sent_splitter,
                                                    sentiment_analyzer=corp_sentiment_analyzer,)
                                    #self.logger.debug("555{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                    #self.logger.critical("was_initialized={}".format(was_initialized))
                                    #p(corp.info())
                                    if not was_initialized:
                                        if self._stop_if_db_already_exist:
                                            self.logger.debug("DBInitialisation: DBName for '{}:{}:{}:{}' wasn't initialized. Since 'self._stop_if_db_already_exist'-Option is on, current Script will ignore current DB and will try to create next one.".format(encryption,template_name,language,dbtype))
                                            continue
                                        else:
                                            self.logger.error("DBInitialisationError: DB for '{}:{}:{}:{}' wasn't initialized. TestDBCreation was aborted.".format(encryption,template_name,language,dbtype))
                                            return False

                                    rows_as_dict_to_insert = self.docs_row_dicts(token=False, unicode_str=True)[template_name]

                                    path_to_db = corp.corpdb.path()
                                    fname_db = corp.corpdb.fname()
                                    #self.logger.debug("777{}:{}:{}:{}".format(dbname, language, platform_name, dbtype))
                                    if not path_to_db or not fname_db:
                                        self.logger.error("Path or FileName for current CorpusDB wasn't getted. (lang='{}', dbname='{}', id='{}',platform_name='{}', visibility='{}', encryption_key='{}') Probably current corpus has InitializationError. TestDBCreation was aborted.".format(language, dbname,corpus_id, platform_name, visibility, encryption_key))
                                        sys.exit()
                                    #p((path_to_db,fname_db))
                                    was_inserted = corp.insert(rows_as_dict_to_insert, log_ignored=corp_log_ignored)

                                    if not was_inserted:
                                        os.remove(path_to_db)
                                        msg = "Rows wasn't inserted into the '{}'-DB. This DB was deleted and script of creating testDBs was aborted.".format(fname_db)
                                        self.logger.error(msg)
                                        raise Exception, msg
                                        sys.exit()
                                        return False
                                        #continue
                                    else:
                                        if not corp_lang_classification:
                                            if len(corp.docs()) != len(rows_as_dict_to_insert):
                                                os.remove(path_to_db)
                                                #shutil.rmtree(path_to_db)
                                                msg = "TestDBsCreation(InsertionError): Not all rows was correctly inserted into DB. This DB was deleted and script of creating testDBs was aborted."
                                                self.logger.error(msg, exc_info=self._logger_traceback)
                                                #sys.exit()
                                                raise Exception, msg
                                                #continue
                                        if corp.total_error_insertion_during_last_insertion_process:
                                            msg = "TestDBsCreation(InsertionError): '{}'-ErrorInsertion was found!!! Not all rows was correctly inserted into DB. This DB was deleted and script of creating testDBs was aborted.".format(corp.total_error_insertion_during_last_insertion_process)
                                            self.logger.error(msg, exc_info=self._logger_traceback)
                                            raise Exception, msg
                                            return False
                                        else:
                                            self.logger.debug("'{}'-TestDB was created. Path: '{}'.".format(fname_db,path_to_db))
                                    #corp.commit()
                                    self.logger.debug("'{}': Following rows was inserted:\n '{}'. \n\n".format(fname_db, '\n'.join("--->"+str(v) for v in  list(corp.docs())  )  ))
                                    activ_corp_dbs[template_name][encryption][dbtype][language] = corp

                                    ### get SENTS
                                    # corp.corpdb.commit()
                                    # if language== "de":
                                    #     p(list(corp.docs()), "de", c="r")

                                    # elif language== "en":
                                    #     p(list(corp.docs()), "en", c="m")
                                    #     time.sleep(15)
                                    #else:
                                    #    time.sleep(15)


                                    

                            elif dbtype=="stats":
                                ## here insert all rows into stats dbs
                                if not use_original_classes:
                                    stats = DBHandler(logger_level=logging.ERROR,logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save,logger_usage=self._logger_usage, logger_save_logs= self._logger_save_logs, mode=self._mode ,  error_tracking=self._error_tracking,  ext_tb= self._ext_tb, stop_if_db_already_exist=self._stop_if_db_already_exist, rewrite=self._rewrite)
                                    stats.init(dbtype, abs_path_to_storage_place, dbname, language, visibility, platform_name=platform_name, license=license , template_name=template_name, version=version , source=source, corpus_id=corpus_id, stats_id=stats_id, encryption_key=encryption_key)
                                    stats.close()
                                else:
                                    #p(activ_corp_dbs, "activ_corp_dbs")
                                    #p((template_name,encryption,dbtype,language))
                                    stats = Stats(logger_level=logging.ERROR, logger_traceback=self._logger_traceback,
                                        logger_folder_to_save=self._logger_folder_to_save, logger_usage=self._logger_usage,
                                        logger_save_logs= self._logger_save_logs, mode=self._mode, error_tracking=self._error_tracking, 
                                        ext_tb= self._ext_tb, stop_if_db_already_exist=self._stop_if_db_already_exist,
                                        status_bar=status_bar,rewrite=self._rewrite)
                                    #p(corp.info())
                                    was_initialized = stats.init(abs_path_to_storage_place,dbname, language, visibility, 
                                                             version=version, corpus_id=corpus_id,  stats_id=stats_id,
                                                             encryption_key=encryption_key,case_sensitiv=False,
                                                             full_repetativ_syntagma=True,baseline_delimiter="++")
                                    #p((encryption_key,dbtype,dbname,language,visibility,platform_name ), "encryption_key____stats")
                                    corp =  activ_corp_dbs[template_name][encryption]["corpus"][language]
                                    #p(corp, "corp")
                                    if isinstance(corp, Corpus):
                                        stats.compute(corp)

                                        corp.corpdb.commit()
                                        stats.statsdb.commit()
                                        corp.close()
                                        stats.close()
                                    else:
                                        self.logger.error("Given CorpObj ('{}') is invalid".format(corp))
                                        return False

            #### check if db was created
            exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
            exist_fnames_in_dir = [fname for fname in exist_fnames_in_dir if (".db" in fname) and (".db-journal" not in fname)]
            if len(fnames_test_db) != len(exist_fnames_in_dir):
                self.logger.error("TestDBs wasn't initialized correctly. There was found '{}' testDBs in the TestDBFolder, but it should be '{}'. ".format(len(exist_fnames_in_dir), len(fnames_test_db)))
                return False
            for fname in fnames_test_db:
                if fname not in exist_fnames_in_dir:
                    self.logger.error("'{}'-testDB wasn't found in the TestDB-Folder. End with Error.".format(fname))
                    return False
            self.logger.info("TestDBs was initialized.")
            return True
        except KeyboardInterrupt:
            exist_fnames_in_dir = os.listdir(abs_path_to_storage_place)
            exist_fnames_in_dir = [fname for fname in exist_fnames_in_dir if ".db" in fname]
            for fname in exist_fnames_in_dir:
                os.remove(os.path.join(abs_path_to_storage_place, fname))
            sys.exit()
            return False


    @nottest
    def create_testsets(self, rewrite=False, abs_path_to_storage_place=False, silent_ignore = True):
        return list(self.create_testsets_in_diff_file_formats(rewrite=rewrite, abs_path_to_storage_place=abs_path_to_storage_place,silent_ignore=silent_ignore))

    @nottest
    def create_testsets_in_diff_file_formats(self, rewrite=False, abs_path_to_storage_place=False, silent_ignore = True):
        #p(abs_path_to_storage_place)
        #sys.exit()
        if not  rewrite:
            rewrite = self._rewrite
        if not abs_path_to_storage_place:
            abs_path_to_storage_place = self._path_to_zas_rep_tools
        #p("fghjk")
        created_sets = []
        if not abs_path_to_storage_place:
            sys.exit()
        try:
            # make test_sets for Blogger Corp 
            for  file_format, test_sets in self._types_folder_names_of_testsets.iteritems():
                for  name_of_test_set, folder_for_test_set in test_sets.iteritems():
                    if file_format == "txt":
                        continue
                    abs_path_to_current_test_case = os.path.join(abs_path_to_storage_place, self._path_to_testsets["blogger"], folder_for_test_set)
                    # p((file_format, name_of_test_set))
                    # p(abs_path_to_current_test_case)
                    if rewrite:
                        if os.path.isdir(abs_path_to_current_test_case):
                            shutil.rmtree(abs_path_to_current_test_case)
                            #os.remove(abs_path_to_current_test_case)

                    if not os.path.isdir(abs_path_to_current_test_case):
                        os.makedirs(abs_path_to_current_test_case)


                    path_to_txt_corpus = os.path.join(self.path_to_zas_rep_tools,self._path_to_testsets["blogger"] , self._types_folder_names_of_testsets["txt"][name_of_test_set] )

                            

                    reader = Reader(path_to_txt_corpus, "txt", regex_template="blogger",logger_level= self._logger_level,logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save,logger_usage=self._logger_usage, logger_save_logs= self._logger_save_logs, mode=self._mode ,  error_tracking=self._error_tracking,  ext_tb= self._ext_tb)
                    exporter = Exporter(reader.getlazy(),  rewrite=rewrite, silent_ignore=silent_ignore, logger_level= self._logger_level,logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save,logger_usage=self._logger_usage, logger_save_logs= self._logger_save_logs, mode=self._mode ,  error_tracking=self._error_tracking,  ext_tb= self._ext_tb)

                    if file_format == "csv":
                        if name_of_test_set == "small":
                            flag = exporter.tocsv(abs_path_to_current_test_case, "blogger_corpus",self._columns_in_doc_table["blogger"], rows_limit_in_file=5)
                            if not flag:
                                yield False
                            else:
                                created_sets.append("csv")
                                yield True
                        else:
                            flag= exporter.tocsv(abs_path_to_current_test_case, "blogger_corpus",self._columns_in_doc_table["blogger"], rows_limit_in_file=2)
                            if not flag:
                                yield False
                            else:
                                created_sets.append("csv")
                                yield True
                        
                    

                    elif file_format == "xml":
                        if name_of_test_set == "small":
                            flag = exporter.toxml(abs_path_to_current_test_case, "blogger_corpus", rows_limit_in_file=5)
                            if not flag:
                                yield False
                            else:
                                created_sets.append("xml")
                                yield True
                        else:
                            flag = exporter.toxml(abs_path_to_current_test_case, "blogger_corpus", rows_limit_in_file=2)
                            if not flag:
                                yield False
                            else:
                                created_sets.append("xml")
                                yield True


                    elif file_format == "json":
                        if name_of_test_set == "small":
                            flag = exporter.tojson(abs_path_to_current_test_case, "blogger_corpus", rows_limit_in_file=5)
                            if not flag:
                                yield False
                            else:
                                created_sets.append("json")
                                yield True
                        
                        else:
                            flag = exporter.tojson(abs_path_to_current_test_case, "blogger_corpus", rows_limit_in_file=2)
                            if not flag:
                                yield False
                            else:
                                created_sets.append("json")
                                yield True
  


                    elif file_format == "sqlite":
                        flag = exporter.tosqlite(abs_path_to_current_test_case, "blogger_corpus",self._columns_in_doc_table["blogger"])
                        if not flag:
                            yield False
                        else:
                            created_sets.append("sqlite")
                            yield True

            #p(created_sets, "created_sets")
            for created_set in set(created_sets):
                path_to_set = os.path.join(abs_path_to_storage_place, self._path_to_testsets["blogger"], created_set)
                #p(path_to_set)
                #p(os.path.join(os.path.split(path_to_set)[0], created_set+".zip"))
                make_zipfile(os.path.join(os.path.split(path_to_set)[0], created_set+".zip"), path_to_set)

            self.logger.info("TestSets (diff file formats) was initialized.")
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("SubsetsCreaterError: Throw following Exception: '{}'. ".format(e), exc_info=self._logger_traceback)
                
        







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







    def _check_correctness_of_the_test_data(self):

        ## Check mapping of columns and values 
        try:
            for template, data_columns in self._columns_in_doc_table.iteritems():
                for  data_values in self.docs_row_values(token=True, unicode_str=True)[template]:
                    #p((len(data_columns), len(data_values)))
                    if len(data_columns) != len(data_values):
                        self.logger.error("TestDataCorruption: Not same number of columns and values.", exc_info=self._logger_traceback)
                        return False

        except Exception, e:
            #p([(k,v) for k,v in self._columns_in_doc_table.iteritems()])
            #p(self.docs_row_values(token=True, unicode_str=True))
            self.logger.error("TestDataCorruption: Test Data in Configer is inconsistent. Probably  - Not same template_names in columns and rows. See Exception: '{}'. ".format(e), exc_info=self._logger_traceback)
            return False
        return True
        #sys.exit()

        # ##### Encrypted #######

    ###########################Preprocessing###############







####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
###################################Other Classes#####################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################









