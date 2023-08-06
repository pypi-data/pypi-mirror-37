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
import threading
import time
import Queue
import json
import traceback
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob_de import TextBlobDE
import langid
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP, ROUND_HALF_DOWN, ROUND_DOWN
from collections import defaultdict
from raven import Client
import execnet
from nltk.tokenize import TweetTokenizer
import enlighten
import multiprocessing as mp
# db_helper

from  zas_rep_tools_data.utils import path_to_data_folder, path_to_models, path_to_someweta_models, path_to_stop_words
from  zas_rep_tools.src.extensions.tweet_nlp.ark_tweet_nlp.CMUTweetTagger import check_script_is_present, runtagger_parse
from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, LenGen, path_to_zas_rep_tools, is_emoji, text_has_emoji, char_is_punkt, text_has_punkt, text_is_punkt, text_is_emoji, categorize_token_list, recognize_emoticons_types,removetags, remove_html_codded_chars, get_number_of_streams_adjust_cpu, Rle, instance_info, MyThread, SharedCounterExtern, SharedCounterIntern, Status,function_name,statusesTstring,rle,from_ISO639_2, to_ISO639_2
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.utils.zaslogger import ZASLogger
from zas_rep_tools.src.utils.debugger import p
import zas_rep_tools.src.utils.db_helper as db_helper
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.classes.basecontent import BaseContent, BaseDB
from zas_rep_tools.src.utils.corpus_helpers import CorpusData
from zas_rep_tools.src.utils.custom_exceptions import  ZASCursorError, ZASConnectionError,DBHandlerError,ProcessError,ErrorInsertion,ThreadsCrash
import nltk
from nltk.corpus import stopwords
import gc

try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download("stopwords")

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download("punkt")


import platform
if platform.uname()[0].lower() !="windows":
    #p("hjklhjk")
    import colored_traceback
    colored_traceback.add_hook()
    #os.system('setterm  -back black -fore white -store -clear')
    #os.system('setterm -term linux -back 0b2f39 -fore a3bcbf -store -clear')
else:
    import colorama
    os.system('color 09252d') # change background colore of the terminal 

class Corpus(BaseContent,BaseDB,CorpusData):
    def __init__(self,  use_test_pos_tagger=False, tok_split_camel_case=True, end_file_marker = -1, 
                use_end_file_marker = False, status_bar= True, heal_me_if_possible=False,**kwargs):
        super(type(self), self).__init__(**kwargs)
        
        #p(heal_me_if_possible, "heal_me_if_possible")
        #Input: Encapsulation:
        self._end_file_marker = end_file_marker
        self._use_end_file_marker = use_end_file_marker
        self._status_bar = status_bar
        self._tok_split_camel_case = tok_split_camel_case
        self._raise_exception_if_error_insertion = True if "test" in self._mode  else False
        self._use_test_pos_tagger = use_test_pos_tagger
        self._heal_me_if_possible = heal_me_if_possible
        #self._diff_emoticons = diff_emoticons


        #InstanceAttributes: Initialization
        self.corpdb = False
        self.offshoot = defaultdict(list)
        self.runcount = 0
        self.locker = threading.Lock()
        self._emo_sym = set(["-", ':', '=','(',')', ";"])
        self.em_start = set([":","-",";","="])
        self.em_end =  set(["(",")"])


        self.logger.low_debug('Intern InstanceAttributes was initialized')
        self.logger.debug('An instance of Corpus() was created ')
  

        ## Log Settings of the Instance
        attr_to_flag = False
        attr_to_len = False
        self._log_settings(attr_to_flag =attr_to_flag,attr_to_len =attr_to_len)



        ############################################################
        ####################__init__end#############################
        ############################################################



    def __del__(self):
        super(type(self), self).__del__()
        try:
            self.status_bars_manager.stop()
        except:
            pass







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




    def additional_attr(self, language, tokenizer,pos_tagger,sentiment_analyzer,
                        sent_splitter,preprocession, lang_classification,del_url,
                        del_punkt,del_num,del_mention,del_hashtag,del_html,case_sensitiv,
                        emojis_normalization,text_field_name,id_field_name):
        additional_attributes = {
                "language":language,
                "tokenizer":tokenizer,
                "pos_tagger":pos_tagger,
                "sentiment_analyzer":sentiment_analyzer,
                "sent_splitter":sent_splitter,
                "preprocession":preprocession,
                "lang_classification":lang_classification if language != "test" else False,
                "del_url":del_url,
                "del_punkt":del_punkt,
                "del_num":del_num,
                "del_mention":del_mention,
                "del_hashtag": del_hashtag,
                "del_html":del_html,
                "case_sensitiv":case_sensitiv,
                "emojis_normalization":emojis_normalization,
                "text_field_name":text_field_name,
                "id_field_name":id_field_name,
                }
        return additional_attributes

        

    ###########################INITS + Open##########################

    def init(self, prjFolder, DBname, language,  visibility, platform_name,
                    encryption_key=False,fileName=False, source=False, license=False,
                    template_name=False, version=False, cols_and_types_in_doc=False, corpus_id=False,
                    tokenizer=True,pos_tagger=False,sentiment_analyzer=False,
                    sent_splitter=False,preprocession=True, lang_classification=False,del_url=False,
                    del_punkt=False,del_num=False,del_mention=False,del_hashtag=False,del_html=False,case_sensitiv=False,
                    emojis_normalization=True,text_field_name="text",id_field_name="id"):


        if self.corpdb:
            self.logger.error("CorpusInitError: An active Corpus Instance was found. Please close already initialized/opened Corpus, before new initialization.", exc_info=self._logger_traceback)
            return False

        #p((text_field_name,id_field_name))
        #p((locals()))
        #sys.exit()

        # Validate Input variables
        valid_answer = list(self._valid_input(language, preprocession, tokenizer, sent_splitter, pos_tagger, sentiment_analyzer))
        if False in valid_answer[:-1]:
            self.logger.error("InputValidationError: Corpus Instance can not be initialized!", exc_info=self._logger_traceback)
            return False
        setted_options = valid_answer[-1]
        #p(setted_options,"setted_options")
        if not isinstance(setted_options, dict):
            self.logger.error("Setted Options after Validation wasn't given.")
            return False

        tokenizer = setted_options["tokenizer"]
        sent_splitter = setted_options["sent_splitter"]
        pos_tagger = setted_options["pos_tagger"]
        sentiment_analyzer = setted_options["sentiment_analyzer"]



        #p(self._logger_level,"!!self._logger_level")
        #p(self._logger_save_logs, "!!self._logger_save_logs")
        self.corpdb = DBHandler( **self._init_attributesfor_dbhandler())
        was_initialized =  self.corpdb.init("corpus", prjFolder, DBname, language, visibility,
            platform_name=platform_name,encryption_key=encryption_key, fileName=fileName,
            source=source, license=license, template_name=template_name, version=version,
            cols_and_types_in_doc=cols_and_types_in_doc,
            corpus_id=corpus_id)
        #p(was_initialized, "was_initialized")
        if not was_initialized:
            self.logger.critical("CorpInit: Current Corpus for following attributes  wasn't initialized: 'dbtype='{}'; 'dbname'='{}; id='{}'; encryption_key='{}'; template_name='{}'; language='{}'.".format("corpus", DBname,corpus_id, encryption_key, template_name, language))
            return False
        #self.corpdb.add_attributs()
        
        self.corpdb.update_attrs(self.additional_attr(language, tokenizer,pos_tagger,sentiment_analyzer,
                        sent_splitter,preprocession, lang_classification,del_url,
                        del_punkt,del_num,del_mention,del_hashtag,del_html,case_sensitiv,
                        emojis_normalization,text_field_name,id_field_name))
        self.set_all_intern_attributes_from_db()
        self.corpdb.update_attr("locked", False)
        #p((tokenizer, pos_tagger, sentiment_analyzer, lang_classification, sent_splitter))
        #p((type(tokenizer), type(pos_tagger), type(sentiment_analyzer), type(lang_classification), type(sent_splitter)))
        if self._save_settings:
            self.logger.settings("InitCorpusDBAttributes: {}".format( instance_info(self.corpdb.get_all_attr(), attr_to_len=False, attr_to_flag=False, as_str=True)))
        if self.corpdb.exist():
            self.logger.debug("CorpusInit: '{}'-Corpus was successful initialized.".format(DBname))
            return True
        else:
            self.logger.error("CorpusInit: '{}'-Corpus wasn't  initialized.".format(DBname), exc_info=self._logger_traceback)
            return False

        #self.logger.settings("InitializationAttributes: {}".format( instance_info(inp_dict, attr_to_len=attr_to_len, attr_to_flag=attr_to_flag, as_str=True)))

    
    def close(self):
        self.corpdb.close()
        self.corpdb = False

    def _close(self):
        self.corpdb._close()
        self.corpdb = False


    def open(self, path_to_corp_db, encryption_key=False):
        if self.corpdb:
            self.logger.error("CorpusOpenerError: An active Corpus Instance was found. Please close already initialized/opened Corpus, before new initialization.", exc_info=self._logger_traceback)
            return False

        self.corpdb = DBHandler(**self._init_attributesfor_dbhandler())
        self.corpdb.connect(path_to_corp_db, encryption_key=encryption_key)

        if self.corpdb.exist():
            #p(self.corpdb.typ())
            if self.corpdb.typ() != "corpus":
                self.logger.error("Current DB is not an Corpus.")
                self._close()
                return False
            self.logger.info("CorpusOpener: '{}'-Corpus was successful opened.".format(os.path.basename(path_to_corp_db)))
            self.set_all_intern_attributes_from_db()
            self.logger.settings("OpenedCorpusDBAttributes: {}".format( instance_info(self.corpdb.get_all_attr(), attr_to_len=False, attr_to_flag=False, as_str=True)))
            return True
        else:
            self.logger.warning("CorpusOpener: Unfortunately '{}'-Corpus wasn't opened.".format(os.path.basename(path_to_corp_db)), exc_info=self._logger_traceback)
            return False

    def set_all_intern_attributes_from_db(self):
        info_dict = self.info()
        self._del_url = info_dict["del_url"]
        self._tokenizer = info_dict["tokenizer"]
        self._template_name = info_dict["template_name"]
        self._sentiment_analyzer = info_dict["sentiment_analyzer"]
        self._preprocession = info_dict["preprocession"]
        self._text_field_name = info_dict["text_field_name"]
        self._id_field_name = info_dict["id_field_name"]
        self._id = info_dict["id"]
        self._pos_tagger = info_dict["pos_tagger"]
        self._del_hashtag = info_dict["del_hashtag"]
        self._lang_classification = info_dict["lang_classification"]
        self._source = info_dict["source"]
        self._version = info_dict["version"]
        self._del_html = info_dict["del_html"]
        self._del_punkt = info_dict["del_punkt"]
        self._sent_splitter = info_dict["sent_splitter"]
        self._visibility = info_dict["visibility"]
        self._language = info_dict["language"]
        self._typ = info_dict["typ"]
        self._del_url = info_dict["del_url"]
        self._case_sensitiv = info_dict["case_sensitiv"]
        self._name = info_dict["name"]
        self._license = info_dict["license"]
        self._created_at = info_dict["created_at"]
        self._platform_name = info_dict["platform_name"]
        self._del_num = info_dict["del_num"]
        self._del_mention = info_dict["del_mention"]
        self._emojis_normalization = info_dict["emojis_normalization"]
        


    def _init_attributesfor_dbhandler(self):
        init_attributes_db_handler = {
                        "stop_if_db_already_exist":self._stop_if_db_already_exist,
                        "rewrite":self._rewrite,
                        "logger_level":self._logger_level,
                        "optimizer":self._optimizer,
                        "in_memory":self._in_memory,
                        "logger_traceback":self._logger_traceback,
                        "logger_folder_to_save":self._logger_folder_to_save,
                        "logger_usage":self._logger_usage,
                        "logger_save_logs":self._logger_save_logs,
                        "thread_safe":self._thread_safe,
                        "mode":self._mode,
                        "error_tracking":self._error_tracking,
                        "ext_tb":self._ext_tb,
                        "isolation_level":self._isolation_level,
                        "optimizer_page_size":self._optimizer_page_size,
                        "optimizer_cache_size":self._optimizer_cache_size,
                        "optimizer_locking_mode":self._optimizer_locking_mode,
                        "optimizer_synchronous":self._optimizer_synchronous,
                        "optimizer_journal_mode":self._optimizer_journal_mode,
                        "optimizer_temp_store":self._optimizer_temp_store,
                        "use_cash":self._use_cash,
                        "replace_double_items":True,
                        "stop_process_if_possible":self._stop_process_if_possible,
                        "make_backup": self._make_backup,
                        "lazyness_border": self._lazyness_border,
                        "replace_double_items": self._replace_double_items, 
                        "save_settings": self._save_settings, 
                        "save_status": self._save_status,
                        "log_content": self._log_content,
                        "clear_logger": self._clear_logger,
                        }
        return init_attributes_db_handler




    def info(self):
        if not self._check_db_should_exist():
            return False

        if not self._check_db_should_be_an_corpus():
            return False

        return copy.deepcopy(self.corpdb.get_all_attr())

    ###########################Setters######################

    def _init_insertions_variables(self):
        self.insertion_status_extended = defaultdict(lambda:lambda:0)
        self.inserted_insertion_status_general = defaultdict(lambda:0)
        self.error_insertion_status_general = defaultdict(lambda:0)
        self.outsorted_insertion_status_general = defaultdict(lambda:0)
        self._terminated = False
        self._threads_num = False
        self.main_status_bar_of_insertions = False
        self.preprocessors = defaultdict(dict)
        self.active_threads = []
        self.KeyboardInterrupt = 0
        self.status_bars_manager =  False
        execnet.set_execmodel("eventlet", "thread")
        self.opened_gateways = execnet.Group()
        self.threads_error_bucket = Queue.Queue()
        # self.threads_success_bucket = Queue.Queue()
        self.threads_status_bucket = Queue.Queue()
        self.threads_success_exit = []
        self.threads_unsuccess_exit = []
        self.channels_error_bucket = Queue.Queue()
        self.status_bars_bucket = Queue.Queue()
        #self.counter = SharedCounterIntern()
        #self.total_ignored_last_insertion = 0
        self.total_inserted_during_last_insert= 0 
        self.total_ignored_last_insertion = 0 
        self.total_outsorted_insertion_during_last_insertion_process = 0
        self.total_error_insertion_during_last_insertion_process = 0
        self._timer_on_main_status_bar_was_reset = False
        self._start_time_of_the_last_insertion = False
        self._end_time_of_the_last_insertion = False
        self._last_insertion_was_successfull = False
        self.counters_attrs = defaultdict(lambda:defaultdict(dict))
        self.status_bars_manager =  self._get_status_bars_manager()
        #self._cleaned_token = (None, u":DEL:")
        self._colnames_in_doc_wasnt_checked = False
        self._tags_to_delete = self._compute_tags_to_delete()
        self._cleaned_tags = {
                                "number":":number:",
                                "URL":":URL:",
                                "symbol":":symbol:",
                                "mention":":mention:",
                                "hashtag":":hashtag:",
                            }

    def insert_duration(self):
        if not self._last_insertion_was_successfull:
            self.logger.error("Last insertion wasn't successfully end ->  It is not possible to return this Duration.")
            return None
        if not self._start_time_of_the_last_insertion and not self._end_time_of_the_last_insertion:
            self.logger.error("Start or End Time for last insertion wasn't saved. -> It is not possible to return this Duration.")
            return None

        return self._end_time_of_the_last_insertion-self._start_time_of_the_last_insertion



    def _check_termination(self, thread_name="Thread0"):
        if self._terminated:
            self.logger.critical("'{}'-Thread was terminated.".format(thread_name))
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            sys.exit()



    def _initialisation_of_insertion_process(self, inp_data, tablename="documents", thread_name="Thread0",  log_ignored=True, dict_to_list=False):
            if self._status_bar:
                if self._threads_num>1:
                    if self._status_bar:
                        unit = "files" if self._use_end_file_marker else "rows"
                        self.main_status_bar_of_insertions.unit = unit
                        self.main_status_bar_of_insertions.total += len(inp_data)

            ### Preprocessors Initialization
            if self._preprocession:
                if thread_name not in self.preprocessors:
                    if not self._init_preprocessors(thread_name=thread_name)["status"]:
                        self.logger.error("Error during Preprocessors initialization. Thread '{}' was stopped.".format(thread_name), exc_info=self._logger_traceback)
                        self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":"Error during Preprocessors initialization"})
                        self._terminated = True
                        return False

            self.logger.debug("_InsertionProcess: Was started for '{}'-Thread. ".format(thread_name))
            
            if self._status_bar:
                if self._threads_num>1:
                    if not self._timer_on_main_status_bar_was_reset:
                        #p(self.main_status_bar_of_insertions.start, "start1")
                        self.main_status_bar_of_insertions.start= time.time()
                        #p(self.main_status_bar_of_insertions.start, "start2")
                        self._timer_on_main_status_bar_was_reset = True

                unit = "files" if self._use_end_file_marker else "rows"
                status_bar_insertion_in_the_current_thread = self._get_new_status_bar(len(inp_data), "{}:Insertion".format(thread_name), unit)
                return status_bar_insertion_in_the_current_thread
            self._check_termination(thread_name=thread_name)
            return None



    def count_basic_stats(self):
        if not self._check_db_should_exist():
            return False
        sent_num = 0
        token_num = 0
        doc_num = self.corpdb.rownum("documents")
        if self._status_bar:
            try:
                if not self.status_bars_manager.enabled:
                    self.status_bars_manager = self._get_status_bars_manager()
            except:
                self.status_bars_manager = self._get_status_bars_manager()

            status_bar_start = self._get_new_status_bar(None, self.status_bars_manager.term.center("CorpSummarizing") , "", counter_format=self.status_bars_manager.term.bold_white_on_magenta("{fill}{desc}{fill}"))
            status_bar_start.refresh()
            status_bar_current = self._get_new_status_bar(doc_num, "Processed:", "document(s)")


        #if doc_num["status"]
        #p((sent_num, token_num,doc_num))
        #p(list(self.docs()))
        if self._preprocession:
            for text_elem in self.docs(columns=self._text_field_name):
                #p((type(text_elem),repr(text_elem)))
                text_elem = json.loads(text_elem[0])
                #p(text_elem)
                for sent_cont in text_elem:
                    sent_num += 1
                    #p(sent_cont[0], "sent_cont")
                    token_num += len(sent_cont[0])

                if self._status_bar:
                    status_bar_current.update(incr=1)

            self.corpdb.update_attr("sent_num", sent_num)
            self.corpdb.update_attr("token_num", token_num)
            self.corpdb.update_attr("doc_num", doc_num)
            self.corpdb.commit()
        else:
            self.logger.info("Basic Statistics can not be computed, because current Corpus wasn't preprocessed.")


        if self._status_bar:
            status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("DocNum: '{}'; SentNum: '{}'; TokenNum: '{}'; ".format(doc_num, sent_num, token_num) ), "",  counter_format=self.status_bars_manager.term.bold_white_on_magenta('{fill}{desc}{fill}\n'))
            status_bar_total_summary.refresh()
            self.status_bars_manager.stop()

    def _is_colnames_in_doctable(self, cols_to_check, debug=False):
        cols_in_doc_table = self.corpdb.col("documents")
        for colname in  cols_to_check:
            if colname not in  cols_in_doc_table:
                if debug:
                    self.logger.debug("'{}'-Colname wasn't found in the DocumentTable. ".format(colname, cols_in_doc_table))
                else:
                    self.logger.error("'{}'-Colname wasn't found in the DocumentTable. ".format(colname, cols_in_doc_table))
                return False
        #self.logger.error("ALLES SUPPI")
        return True


    def _insert(self, inp_data, tablename="documents",  thread_name="Thread0",  log_ignored=True, dict_to_list=False):
        try:  
            self._check_termination(thread_name=thread_name) 
            time.sleep(2) # 

            ############################################################
            ####################INITIALISATION####################
            ############################################################
            status_bar_insertion_in_the_current_thread = self._initialisation_of_insertion_process( inp_data, tablename=tablename,  thread_name=thread_name,  log_ignored=log_ignored, dict_to_list=dict_to_list)
            if self._status_bar:
                if not  status_bar_insertion_in_the_current_thread: return False
                #
            ############################################################
            #################### MAIN INSERTION PROCESS ####################
            ############################################################
            
            to_update = True
            self._colnames_in_doc_wasnt_checked = True
            #p((self.corpdb.col("documents")))
            for row_as_dict in inp_data:
                #self._check_termination(thread_name=thread_name) 
                #p(row_as_dict.keys(), "row_as_dict.keys")
                #p(row_as_dict, "row_as_dict")
                #sys.exit()
                if self._colnames_in_doc_wasnt_checked:
                    if row_as_dict:
                        with self.locker:
                            if self._colnames_in_doc_wasnt_checked:
                                #p("----1111")
                                if self._terminated:
                                    self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
                                    return False
                                return_error = False
                                #p("0000")

                                #invalid_symbols_in_colnames = "{}[]:,;-()°^<>="
                                is_invalid = False
                                for colname in row_as_dict.keys():
                                    try:
                                        colname = colname.decode("utf-8")
                                    except:
                                        pass
                                    for invalid_symbol in Corpus.invalid_symbols_in_colnames:
                                        #p((colname, invalid_symbol, ))
                                        #p((type(colname),type(invalid_symbol)))
                                        if invalid_symbol in colname:
                                            if invalid_symbol == " ":
                                                invalid_symbol = "WHITE_SPACE"
                                            self.logger.error("InvalidColNamesError:  '{}'-ColumnName contain minimum one invalid Symbol, and that is:  '{}'. ".format(colname, invalid_symbol))
                                            is_invalid = True
                                            #self._terminated = True

                                if is_invalid:
                                    self.logger.error("In the input Data (ColNames) was found minimum one invalid symbol. Please clean Data from the invalid symbols and start this process one more time.  Please consult logs for more Information.\n   Please ensure that all ColNames in you input Data don't contain following symbols: '{}'.".format(Corpus.invalid_symbols_in_colnames))
                                    self._terminated = True
                                    self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                                    return False

                                if not self._is_colnames_in_doctable(row_as_dict.keys(), debug=self._heal_me_if_possible):
                                    #p("1111")
                                    if self.corpdb.rownum("documents") == 0:
                                        #p("22222")
                                        if self._heal_me_if_possible:
                                            #p("22222´´´´´´´")
                                            cursor_name = thread_name+"_temp"
                                            old_cols_in_doc = self.corpdb.col("documents")
                                            drop_status = self.corpdb.drop_table("documents", dbname="main", thread_name=cursor_name)
                                            if not drop_status["status"]:
                                                self.logger.error("HealingError: Tables 'Documents' wasn't deleted. ")
                                                self._terminated = True
                                                self._colnames_in_doc_wasnt_checked = False
                                                self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                                                return False
                                            
                                            temp_cols_and_types_in_doc = [(colname, "TEXT") for colname in row_as_dict.keys()]
                                            init_table_status= self.corpdb._init_default_table("corpus", "documents", temp_cols_and_types_in_doc, constraints=db_helper.default_constraints["corpus"]["documents"])
                                            if not init_table_status["status"]:
                                                self.logger.error("HealingError: Reinitialisation of the ColNames is failed:\n  Status_Information:\n    ColNamesFromDocTablesBevoreHealing='{}';\n    DefaultColNames='{}';\n    ColnamesWhichWasFoundInCurrentDocItem='{}'.".format(old_cols_in_doc, db_helper.default_tables["corpus"]["documents"]["basic"].keys(),  row_as_dict.keys()))
                                                self._terminated = True
                                                self._colnames_in_doc_wasnt_checked = False
                                                self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                                                return False

                                            self.corpdb._update_temp_indexesList_in_instance(thread_name=cursor_name)
                                            #self._update_database_pragma_list(thread_name=thread_name)
                                            self.corpdb._update_pragma_table_info(thread_name=cursor_name)

                                        else:
                                            #p("2222______")
                                            #return_error = False
                                            if self._log_content:
                                                cols_in_elem = row_as_dict.keys()
                                                cols_in_doc = self.corpdb.col("documents")
                                                diff = set(cols_in_elem).symmetric_difference(set(cols_in_doc))
                                            else:
                                                cols_in_elem = ":HIDDEN:"
                                                cols_in_doc = ":HIDDEN:"
                                                diff = ":HIDDEN:"
                                            self.logger.error("InputColNamesDifference: Current DocItem contain also not initialized colnames.\n     Info_about_the_current_State:\n    ColsFromTheCurrentDocItem: '{}';\n    InitilizedColsInTheDocumentsTable: '{}';\n    ColsDifferenz: '{}'\n  Solution:\n   1) Use 'template_name'-Option in Corpus to use preinitialised colnames (ex:{});\n   2) Use 'cols_and_types_in_doc'-Option and predefine your own colnames and types (example for API: [('gender', 'TEXT'), ('age','INTEGER')]; example for command_line_interface: 'gender:TEXT,age:INTEGER')  ;\n   3) Set 'heal_me_if_possible'-Option to give the DB permission to repair some broken data if it is possible. But be carefully with that option because, it could create unexpected errors.\n".format(cols_in_elem, cols_in_doc, diff,DBHandler.templates.keys() ))
                                            self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                                            self._terminated = True
                                            self._colnames_in_doc_wasnt_checked = False
                                            return False

                                        self._colnames_in_doc_wasnt_checked = False
                                        self.logger.info("Cols from given Text Collections was extracted and the documentsTables was hield.")
                                        #p((self.corpdb.col("documents")))

                                    else:
                                        #p("3333")
                                        #return_error = False
                                        if self._log_content:
                                            cols_in_elem = row_as_dict.keys()
                                            cols_in_doc = self.corpdb.col("documents")
                                            diff = set(cols_in_elem).symmetric_difference(set(cols_in_doc))
                                        else:
                                            cols_in_elem = ":HIDDEN:"
                                            cols_in_doc = ":HIDDEN:"
                                            diff = ":HIDDEN:"
                                        if self._heal_me_if_possible:
                                            self.logger.error("InputColNamesDifference: Current DocItem contain also not initialized colnames. And it wasn't possible to repair it.\n  Info_about_the_current_State:\n    ColsFromTheCurrentDocItem: '{}';\n    InitilizedColsInTheDocumentsTable: '{}';\n    ColsDifferenz: '{}' \n  Solution:\n   1) Use 'template_name'-Option in Corpus to use preinitialised colnames (ex:{});\n   2) Use 'cols_and_types_in_doc'-Option and predefine your own colnames and types (example for API: [('gender', 'TEXT'), ('age','INTEGER')]; example for command_line_interface: 'gender:TEXT,age:INTEGER')  ;".format(cols_in_elem, cols_in_doc, diff,DBHandler.templates.keys() ))
                                        else:
                                            self.logger.error("InputColNamesDifference: Current DocItem contain also not initialized colnames.\n   Info_about_the_current_State:\n    ColsFromTheCurrentDocItem: '{}';\n    InitilizedColsInTheDocumentsTable: '{}';\n    ColsDifferenz: '{}' \n  Solution:\n   1) Use 'template_name'-Option in Corpus to use preinitialised colnames (ex:{});\n   2) Use 'cols_and_types_in_doc'-Option and predefine your own colnames and types (example for API: [('gender', 'TEXT'), ('age','INTEGER')]; example for command_line_interface: 'gender:TEXT,age:INTEGER')  ;\n   3) Set 'heal_me_if_possible'-Option to give the DB permission to repair some broken data if it is possible. But be carefully with that option because, it could create unexpected errors.".format(cols_in_elem, cols_in_doc, diff,DBHandler.templates.keys() ))
                                            
                                        self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                                        self._terminated = True
                                        self._colnames_in_doc_wasnt_checked = False
                                        return False
                    self._colnames_in_doc_wasnt_checked = False



                #p(row_as_dict ,"rw_as_dict ")
                #self.offshoot[self.runcount].append(row_as_dict)
                self._check_termination(thread_name=thread_name) 
                #p(status_bar_insertion_in_the_current_thread, "status_bar_insertion_in_the_current_thread")
                if row_as_dict == self._end_file_marker:
                    #f.write("{}\n".format(row_as_dict))

                    if self._status_bar:
                        if self._use_end_file_marker:
                            status_bar_insertion_in_the_current_thread.update(incr=1)
                            if self._threads_num>1:
                                self.main_status_bar_of_insertions.update(incr=1)
                    continue
                else:
                    if self._status_bar:
                        if not self._use_end_file_marker:
                            status_bar_insertion_in_the_current_thread.update(incr=1)
                            if self._threads_num>1:
                                self.main_status_bar_of_insertions.update(incr=1)
                        else:
                            if to_update:
                                to_update = False
                                counter = status_bar_insertion_in_the_current_thread.count
                                status_bar_insertion_in_the_current_thread.count = counter + 1
                                #p(status_bar_insertion_in_the_current_thread.count, "1status_bar_insertion_in_the_current_thread.count")
                                status_bar_insertion_in_the_current_thread.refresh()
                                status_bar_insertion_in_the_current_thread.count == counter
                                #p(status_bar_insertion_in_the_current_thread.count, "2status_bar_insertion_in_the_current_thread.count")
                                status_bar_insertion_in_the_current_thread.refresh()

                #p(status_bar_insertion_in_the_current_thread, "status_bar_insertion_in_the_current_thread")
                # for empty insertions
                if not row_as_dict:
                    #f.write("{}\n".format(row_as_dict))
                    self.outsorted_insertion_status_general[thread_name] +=1
                    continue
                
                ############################################################
                #################### TEXT PREPROSSESION ###################
                ############################################################
                if self._preprocession:
                    text_preprocessed = False
                    try:
                        preproc = self._preprocessing(row_as_dict[self._text_field_name],thread_name=thread_name, log_ignored=log_ignored, row=row_as_dict)
                        if preproc:
                            if preproc == "terminated":
                                self.logger.critical("{} got an  Termination Command!! and was terminated.".format(thread_name))
                                self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
                                self._terminated = True
                                return False

                            text_preprocessed = json.dumps(preproc)
                        else:
                            text_preprocessed = preproc
                        #p(text_preprocessed, "text_preprocessed")
                    except KeyError, e: 
                        print_exc_plus() if self._ext_tb else ""
                        msg = "PreprocessingError: (KeyError) See Exception: '{}'. Probably text_field wasn't matched. Possible Explanations:  1. The wrong text_field name was given or 2. matched file has not right structure (every text file should have min an text_element and an id_element)  or 3. ImplemenationError, where row  was given as list and not as dict.  Possible Solution: 1. Check if given file has an id and text element, if not, than you can sort this file out, to be sure, that every thing going right. And than create CorpusDB one more time. ".format(e)
                        #self.logger.error(msg, exc_info=self._logger_traceback)
                        self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                        if log_ignored:
                            self.logger.error_insertion(msg, exc_info=self._logger_traceback)
                    
                        #return False
                    except Exception, e:
                        self.logger.error("PreprocessingError:  See Exception: '{}'. ".format(e),  exc_info=self._logger_traceback)
                        self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                        return False


                    if text_preprocessed:
                        row_as_dict[self._text_field_name] = text_preprocessed
                    else:
                        #self._check_termination(thread_name=thread_name) 
                        #self.logger.warning("Text in the current DictRow (id='{}') wasn't preprocessed. This Row was ignored.".format(row_as_dict["id"]))
                        self.outsorted_insertion_status_general[thread_name] +=1
                        continue
                #else:
                #    row_as_dict[self._text_field_name] = (row_as_dict[self._text_field_name], None)


                ############################################################
                ####################INSERTION INTO DB ####################
                ############################################################
                # #return "outsorted"
                self._check_termination(thread_name=thread_name)
                insertion_status = self.corpdb.lazyinsert( tablename, row_as_dict, thread_name=thread_name, dict_to_list=dict_to_list)


                if insertion_status["status"]: 
                    self.inserted_insertion_status_general[thread_name] += insertion_status["out_obj"]
                    self.outsorted_insertion_status_general[thread_name] += insertion_status["outsort"]
                    #self.logger.low_debug("Row was inserted into DB.")
                elif insertion_status["action"] == "outsorted":
                    self.outsorted_insertion_status_general[thread_name] +=1
                elif insertion_status["action"] == "ThreadsCrash":
                    msg = "ThreadsCrash: Please use option 'thread_safe' to ensure ThreadSafety and run script again. |ErrorTrackID:'{}'| (To see more use search logs with TrackID)".format(insertion_status["track_id"])
                    self.logger.error(msg)
                    if log_ignored:
                        self.logger.error_insertion("IgnoredRow: |ErrorTrackID:'{}'| Current Row: '{}' wasn't inserted (by dbhandler.lazyinsert()) into DB. Consult logs to find the reason.".format(insertion_status["track_id"],row_as_dict))
                    
                    self.threads_status_bucket.put({"name":thread_name, "status":"ThreadsCrash", "track_id":insertion_status["track_id"]})
                    self._terminated = True
                    raise ThreadsCrash, msg
                    sys.exit()

                elif insertion_status["action"] in ["failed", "ignored"]:
                    self.error_insertion_status_general[thread_name] +=1
                    if log_ignored:
                        self.logger.error_insertion("IgnoredRow: |ErrorTrackID:'{}'| Current Row: '{}' wasn't inserted (by dbhandler.lazyinsert()) into DB. Consult logs to find the reason.".format(insertion_status["track_id"],row_as_dict))
                    continue
                elif insertion_status["action"] == "stop_execution":
                    self.error_insertion_status_general[thread_name] +=1
                    if log_ignored:
                        self.logger.error_insertion("IgnoredRow: |ErrorTrackID:'{}'| Current Row: '{}' wasn't inserted (by dbhandler.lazyinsert()) into DB. Consult logs to find the reason.".format(insertion_status["track_id"],row_as_dict))
                    self.logger.error(insertion_status["desc"])
                    self._terminated = True
                    
                else:
                    self.error_insertion_status_general[thread_name] +=1
                    if log_ignored:
                        self.logger.error_insertion("IgnoredRow: |ErrorTrackID:'{}'| Current Row: '{}' wasn't inserted (by dbhandler.lazyinsert()) into DB. Consult logs to find the reason.".format(insertion_status["track_id"],row_as_dict))
                    continue


            ############################################################
            ####################FINISCHING ####################
            ############################################################
            self._check_termination(thread_name=thread_name) 

            if self._status_bar:
                status_bar_insertion_in_the_current_thread.refresh()
                self.counters_attrs["_insert"][thread_name]["start"] = status_bar_insertion_in_the_current_thread.start
                self.counters_attrs["_insert"][thread_name]["end"] = status_bar_insertion_in_the_current_thread.last_update
                self.counters_attrs["_insert"][thread_name]["total"] = status_bar_insertion_in_the_current_thread.total
                self.counters_attrs["_insert"][thread_name]["desc"] = status_bar_insertion_in_the_current_thread.desc
                status_bar_insertion_in_the_current_thread.close(clear=False)

            self.threads_status_bucket.put({"name":thread_name, "status":"done"})
            self.logger.debug("_Insert: '{}'-Thread is done and was stopped.".format(thread_name))
            return True

        except KeyboardInterrupt:
            self.logger.critical("{} get an  KeyboardInterruption.".format(thread_name))
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            self._terminated = True
            #self.terminate_all("KeyboardInterrupt")
            return False

        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("_InsertError: See Exception: '{}'. ".format(e), exc_info=self._logger_traceback)
            self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
            return False


    def insert(self, inp_data, tablename="documents", thread_name="Thread0",  allow_big_number_of_streams=False, number_of_allow_streams=8, log_ignored=True, dict_to_list=False, create_def_indexes=True):
        try:
            if not self._check_db_should_exist():
                return False

            if self.corpdb.get_attr("locked"):
                            self.logger.error("Current DB ('{}') is still be locked. Possibly it in ht now fr in-useom other process or la thest computation process is failed.".format(self.corpdb.fname()))
                            return False
            self.corpdb.update_attr("locked", True)

            self._init_insertions_variables()
            self._start_time_of_the_last_insertion = time.time()
            self.runcount += 1
            if isinstance(inp_data, LenGen):
                inp_data= [inp_data]
            elif isinstance(inp_data, list):
                if isinstance(inp_data[0], dict):
                    inp_data = [inp_data]
                #elif isinstance(inp_data[0],  LenGen)
                #    pass
            else:
                self.logger.critical("Possibly not right type of data was given. It could be messed up the process.")
            #return True
            #self.status_bars_manager =  self._get_status_bars_manager()
            #Manager.term
            #self.status_bars_manager.term print(t.bold_red_on_bright_green('It hurts my eyes!'))
            
            

            if self._status_bar:
                print "\n"
                if self._in_memory:
                    dbname = ":::IN-MEMORY-DB:::"
                else:
                    dbname = '{}'.format(self.corpdb.fname())
                status_bar_starting_corpus_insertion = self._get_new_status_bar(None, self.status_bars_manager.term.center( dbname) , "", counter_format=self.status_bars_manager.term.bold_white_on_red("{fill}{desc}{fill}"))
                status_bar_starting_corpus_insertion.refresh()
            ## threads
            if self._status_bar:
                status_bar_threads_init = self._get_new_status_bar(len(inp_data), "ThreadsStarted", "threads")
            
            i=1
            if len(inp_data)>=number_of_allow_streams:
                if not allow_big_number_of_streams:
                    self.logger.critical("Number of given streams is to big ('{}'). It it allow to have not more as {} streams/threads parallel. If you want to ignore this border set 'allow_big_number_of_streams' to True. But it also could mean, that the type of data_to_insert is not correct. Please check inserted data. It should be generator/list of rows (packed as dict).".format(len(inp_data),number_of_allow_streams))
                    return False

            self._threads_num = len(inp_data)
            if self._threads_num>1:
                if self._status_bar:
                    unit = "files" if self._use_end_file_marker else "rows"
                    #self.main_status_bar_of_insertions = self._get_new_status_bar(0, "AllThreadsTotalInsertions", unit,
                    #                    bar_format= self.status_bars_manager.term.bright_magenta( u'{desc}{desc_pad}{percentage:3.0f}%|{bar}| {count:{len_total}d}/{total:d} [{elapsed}<{eta}, {rate:.2f}{unit_pad}{unit}/s]\t\t\t\t'))

                    self.main_status_bar_of_insertions = self._get_new_status_bar(0, "AllThreadsTotalInsertions", unit)
                    self.main_status_bar_of_insertions.refresh()
                    #self.main_status_bar_of_insertions.total = 0


            for gen in inp_data:
                #p(gen, "gen")
                #self.logger.critical(("3", type(gen), gen ))
                if not self._isrighttype(gen):
                    self.logger.error("InsertionError: Given InpData not from right type. Please given an list or an generator.", exc_info=self._logger_traceback)
                    return False

                thread_name = "Thread{}".format(i)
                processThread = MyThread(target=self._insert, args=(gen, tablename,  thread_name, log_ignored, dict_to_list), name=thread_name)
                #processThread = mp.Process(target=self._insert, args=(gen, tablename,  thread_name, log_ignored, dict_to_list), name=thread_name )
                
                #processThread.setDaemon(True)
                processThread.start()
                self.active_threads.append(processThread)
                if self._status_bar:
                    status_bar_threads_init.update(incr=1)
                i+=1
                time.sleep(1)

            #p("All Threads was initialized", "insertparallel")  
            self.logger.info("'{}'-thread(s) was started. ".format(len(self.active_threads)))

            time.sleep(3)

            if not self._wait_till_all_threads_are_completed("Insert"):
                return False

            status = self.corpdb._write_cashed_insertion_to_disc(with_commit=True)
            if status["status"]:
                self.inserted_insertion_status_general[thread_name] += status["out_obj"]
                self.outsorted_insertion_status_general[thread_name] += status["outsort"]
            else:
                return status

            ## save attributes from the main counter
            if self._status_bar:
                if self.main_status_bar_of_insertions:
                    self.counters_attrs["insert"]["start"] = self.main_status_bar_of_insertions.start
                    self.counters_attrs["insert"]["end"] = self.main_status_bar_of_insertions.last_update
                    self.counters_attrs["insert"]["total"] = self.main_status_bar_of_insertions.total
                    self.counters_attrs["insert"]["desc"] = self.main_status_bar_of_insertions.desc
                else:
                    self.counters_attrs["insert"] = False

            self._print_summary_status()
            self.opened_gateways.terminate()
            del self.opened_gateways
            gc.collect()
            #self.corpdb.commit()
            
            if self._status_bar:
                was_inserted = sum(self.inserted_insertion_status_general.values()) 
                error_insertion = sum(self.error_insertion_status_general.values())
                empty_insertion = sum(self.outsorted_insertion_status_general.values())
                was_ignored = error_insertion + empty_insertion
                status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("TotalRowInserted:'{}'; TotalIgnored:'{}' ('{}'-error, '{}'-outsorted)".format(was_inserted, was_ignored,error_insertion,empty_insertion ) ), "",  counter_format=self.status_bars_manager.term.bold_white_on_red('{fill}{desc}{fill}\n'))
                status_bar_total_summary.refresh()
                self.status_bars_manager.stop()

            self.corpdb._commit()
            rownum = self.corpdb.rownum("documents")
            if rownum >0:
                self.logger.info("Current CorpusDB has '{}' rows in the Documents Table.".format(rownum))
                self.corpdb.update_attr("locked", False)
            else:
                self.logger.error("InsertionProcessFailed: No one Document was added into CorpDB.")
                return False

            if create_def_indexes:
                self.corpdb.init_default_indexes(thread_name=thread_name)
                self.corpdb._commit()


            self._last_insertion_was_successfull = True
            self._end_time_of_the_last_insertion = time.time()
            self.count_basic_stats()


            if len(self.threads_unsuccess_exit) >0:
                self.logger.error("Insertion process is failed. (some thread end with error)")
                raise ProcessError, "'{}'-Threads end with an Error.".format(len(self.threads_unsuccess_exit))
                return False
            else:
                self.logger.info("Insertion process end successful!!!")
                self.corpdb._commit()
                return True
            

        except KeyboardInterrupt:
            #self.logger.warning("KeyboardInterrupt: Process was stopped from User. Some inconsistence in the current DB may situated.")
            self.terminate_all("KeyboardInterrupt", thread_name=thread_name)
            #self.logger.critical("KeyboardInterrupt: All Instances was successful aborted!!!")
            #sys.exit()
        except Exception, e:
            self.logger.error(" See Exception: '{}'. ".format(e),  exc_info=self._logger_traceback)
            return False




    def terminate_all(self, reason, thread_name="Thread0"):
        try:
            self.logger.critical("Termination Process was initialized. Reason: '{}'.".format(reason))
            self._terminated = True
            time.sleep(2)
            if self.status_bars_manager:
                self.status_bars_manager.stop()
            if self.opened_gateways:
                self.opened_gateways.terminate()

            self._wait_till_all_threads_are_completed("TerminateAll",sec_to_wait=0, sec_to_log = 1)
            self._print_summary_status()
            
            self.logger.critical("All active Threads was successful terminated!!!")
            if reason == "KeyboardInterrupt":
                self.logger.critical("Corpus was Terminated ({}). (For more information please consult logs)".format(reason))
            else:
                raise ProcessError, "Corpus was Terminated ({}). (For more information please consult logs)".format(reason)
            return True
        except KeyboardInterrupt:
            self.logger.critical("Process was killed un-properly!!!")
            sys.exit()
            



#self.KeyboardInterrupt
    # def _terminated_all_activ_threads(self):
    #     for t in self.active_threads:
    #         if t.isAlive():
    #             t.terminate()
    #             t.join()
    #             self.logger.info("'{}'-Thread was terminated".format(t.name))
    #         else:
    #             self.logger.info("'{}'-Thread can not be terminated, because it is already died.".format(t.name))



    ###########################Getters#######################

    def _intern_docs_getter(self, columns=False, select=False,  where=False, connector_where="AND", output="list", size_to_fetch=1000, limit=-1, offset=-1):
        if not self._check_db_should_exist():
            yield False
            return 
        for row in self.corpdb.lazyget("documents", columns=columns, select=select, where=where, connector_where=connector_where, output=output, size_to_fetch=size_to_fetch, limit=limit, offset=offset):
            yield row


    def docs(self, columns=False, select=False,  where=False, connector_where="AND", output="list", size_to_fetch=1000, limit=-1, offset=-1, stream_number=1, adjust_to_cpu=True, min_files_pro_stream=1000):
        row_number = self.corpdb.rownum("documents")
        #p((row_number))
        if self.corpdb.get_attr("locked"):
                self.logger.error("Current DB is still be locked. Possibly it is right now in-use from other process or the last insertion-process is failed.")
                return False

        wish_stream_number = stream_number
        if stream_number <1:
            stream_number = 1000000
            adjust_to_cpu = True
            self.logger.debug("StreamNumber is less as 1. Automatic computing of stream number according cpu was enabled.")


        if adjust_to_cpu:
            stream_number= get_number_of_streams_adjust_cpu( min_files_pro_stream, row_number, stream_number)
            if stream_number is None:
                self.logger.error("Number of docs in the table is 0. No one generator could be returned.")
                return []

        
        list_with_generators = []
        number_of_files_per_stream = int(Decimal(float(row_number)/stream_number).quantize(Decimal('1.'), rounding=ROUND_UP))
        


        if stream_number > row_number:
            self.logger.error("StreamNumber is higher as number of the files to read. This is not allowed.")
            return False

        current_index = 0


        for i in range(stream_number):
            #p(i, "i")
            if i < (stream_number-1): # for gens in between 
                new_index = current_index+number_of_files_per_stream
                gen  = self._intern_docs_getter( columns=columns, select=select,  where=where, connector_where=connector_where, output=output, size_to_fetch=size_to_fetch, limit=number_of_files_per_stream, offset=current_index)
                lengen = LenGen(gen, number_of_files_per_stream)
                current_index = new_index
            else: # for the last generator
                gen  = self._intern_docs_getter( columns=columns, select=select,  where=where, connector_where=connector_where, output=output, size_to_fetch=size_to_fetch, limit=-1, offset=current_index)
                lengen = LenGen(gen, row_number-current_index)

            if stream_number == 1:
                if wish_stream_number > 1 or wish_stream_number<=0:
                    #p((stream_number,wish_stream_number))
                    return [lengen]
                else:
                    return lengen
            list_with_generators.append(lengen)

        self.logger.debug(" '{}'-streams was created.".format(stream_number))
        return list_with_generators










    # ###########################Attributes####################


    # def update_attr(self,attribut_name, value):
    #     if not self._check_db_should_exist():
    #         return False

    #     if not self.corpdb.update_attr(attribut_name, value,  dbname="main"):
    #         self.logger.error("AttrUpdate: Bot possible. ", exc_info=self._logger_traceback)
    #         return False

    # def add_attributs(self,attributs_names, values):
    #     if not self._check_db_should_exist():
    #         return False

    #     if not self.corpdb.add_attributs(attributs_names, values, dbname="main"):
    #         self.logger.error("AttrUpdate: Bot possible. ", exc_info=self._logger_traceback)
    #         return False


    # def get_attr(self,attributName, dbname=False):
    #     if not self._check_db_should_exist():
    #         return False
    #     return self.corpdb.get_attr(attributName, dbname="main")


    # def get_all_attr(self):
    #     if not self._check_db_should_exist():
    #         return False
    #     #p(self.corpdb.get_all_attr("main"))
    #     return self.corpdb.get_all_attr(dbname="main")







    ###########################Other Methods##################


    def exist(self):
        return True if self.corpdb else False


    def db(self):
        if not self._check_db_should_exist():
            return False
        self.logger.debug("DBConnection was passed.")
        return self.corpdb









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





    ###########################Input-Validation#############




    def _init_preprocessors(self, thread_name="Thread0"):
        if not self._check_db_should_exist():
            return False
        try:
            #p(self._preprocession, "self._preprocession", c="r")
            #print self._preprocession

            if self._preprocession:
                ### Step 1: Init Status Bar 
                if not self._terminated:
                    p_list = [self._sent_splitter, self._pos_tagger, self._lang_classification, self._tokenizer, self._sentiment_analyzer] #,self._stemmer
                    #p(p_list, "p_list")
                    preprocessors_number = sum([True for pp in p_list if pp ])
                    if self._status_bar:
                        status_bar_preprocessors_init = self._get_new_status_bar(preprocessors_number, "{}:PreprocessorsInit".format(thread_name), "unit")
                    #p(p_list, "p_list")
                ### Step 2. 
                if not self._terminated: 
                    if not self._set_tokenizer(split_camel_case=self._tok_split_camel_case, language=self._language, thread_name=thread_name):
                        #return False
                        return Status(status=False, desc="SetTokenizerFailed")
                    if self._status_bar:
                        status_bar_preprocessors_init.update(incr=1)
                        status_bar_preprocessors_init.refresh()

                # if not self._terminated: 
                #     if not self._set_stemmer(thread_name=thread_name):
                #         #return False
                #         return Status(status=False, desc="SetStemmerFailed")
                #     if self._status_bar:
                #         status_bar_preprocessors_init.update(incr=1)
                #         status_bar_preprocessors_init.refresh()

                if not self._terminated: 
                    if self._sent_splitter:
                        #is_tuple = True if True in [self._tok_token_classes,self._tok_extra_info] else False
                        if not self._set_sent_splitter( thread_name=thread_name):
                            return Status(status=False, desc="SetSentSplitterFailed")
                        if self._status_bar:
                            status_bar_preprocessors_init.update(incr=1)
                            status_bar_preprocessors_init.refresh()
                            #status_bar_preprocessors_init.update(incr=1)

                if self._sentiment_analyzer:
                    if self._status_bar:
                        status_bar_preprocessors_init.update(incr=1)
                        status_bar_preprocessors_init.refresh()

                if not self._terminated: 
                    if self._pos_tagger:
                        if not self._set_pos_tagger(thread_name=thread_name):
                            return Status(status=False, desc="SetPOSTaggerFailed")
                        if self._status_bar:
                            status_bar_preprocessors_init.update(incr=1)
                            status_bar_preprocessors_init.refresh()

                if not self._terminated: 
                    if self._lang_classification:
                        if self._set_rle(thread_name):
                            if self._status_bar:
                                status_bar_preprocessors_init.update(incr=1)
                                status_bar_preprocessors_init.refresh()
                        else:
                            self.logger.error("RLE in '{}'-Thread wasn't initialized. Script was aborted.".format(thread_name), exc_info=self._logger_traceback)
                            #self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                            return Status(status=False, desc="SetRLEFailed")

                

                if not self._terminated: 
                    self.logger.debug("PreprocessorsInit: All Preprocessors for '{}'-Thread was initialized.".format(thread_name))
                    return Status(status=True, desc=preprocessors_number)

                

                if self._terminated:
                    self.logger.critical("{} was terminated!!!".format(thread_name))
                    self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
                    self._terminated = True
                    return Status(status=False, desc="WasTerminated")

                    if self._status_bar:
                        self.counters_attrs["_init_preprocessors"][thread_name]["start"] = status_bar_preprocessors_init.start
                        self.counters_attrs["_init_preprocessors"][thread_name]["end"] = status_bar_preprocessors_init.last_update
                        self.counters_attrs["_init_preprocessors"][thread_name]["total"] = status_bar_preprocessors_init.total
                        self.counters_attrs["_init_preprocessors"][thread_name]["desc"] = status_bar_preprocessors_init.desc

            else:
                return Status(status=False, desc="PreprocessorsWasDisabled")

        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            msg = "PreprocessorsInitError: See Exception: '{}'. ".format(e)
            self.logger.error(msg, exc_info=self._logger_traceback)
            return Status(status=False, desc=msg)

        

    def _get_status_bars_manager(self):
        config_status_bar = {'stream': sys.stdout,
                  'useCounter': True, 
                  "set_scroll": True,
                  "resize_lock": True
                  }
        enableCounter_status_bar = config_status_bar['useCounter'] and config_status_bar['stream'].isatty()
        return enlighten.Manager(stream=config_status_bar['stream'], enabled=enableCounter_status_bar, set_scroll=config_status_bar['set_scroll'], resize_lock=config_status_bar['resize_lock'])


    def _set_rle(self,  thread_name="Thread0"):
        try:
            self.logger.low_debug("INIT-RLE: Start the initialization of Run_length_encoder for '{}'-Thread.".format(thread_name))
            self.preprocessors[thread_name]["rle"] = Rle(self.logger)
            #p(("RLE_INIT",thread_name))
            self.logger.debug("INIT-RLE: Run_length_encoder for '{}'-Thread was initialized.".format(thread_name))
            return True
        except Exception, e:
            self.logger.error("Exception was encountered: '{}'. ".format(e), exc_info=self._logger_traceback)
            return False



    def _status_bars(self):
        if self.status_bars_manager:
            return self.status_bars_manager.counters
        else:
            self.logger.error("No activ Status Bar Managers was found.", exc_info=self._logger_traceback)
            return False




    def _wait_till_all_threads_are_completed(self, waitername, sec_to_wait=3, sec_to_log = 15):
        time_counter = sec_to_log
        while not ( (len(self.threads_success_exit) >= len(self.active_threads)) or (len(self.threads_unsuccess_exit) != 0)):
        #while len(self.threads_unsuccess_exit) == 0
            #p(((len(self.threads_success_exit) <= len(self.active_threads))), "(len(self.threads_success_exit) < len(self.active_threads))")
            #p((len(self.threads_unsuccess_exit) == 0), "(len(self.threads_unsuccess_exit) == 0)")
            if time_counter >= sec_to_log:
                time_counter = 0
                self.logger.low_debug("'{}'-Waiter: {}sec was gone.".format(waitername, sec_to_log))

            if not self.threads_status_bucket.empty():
                answer = self.threads_status_bucket.get()
                thread_name = answer["name"]
                status = answer["status"]
                if status == "done":
                    if thread_name not in self.threads_success_exit:
                        self.threads_success_exit.append(answer)
                elif status in  ["failed", "terminated"]:
                    if thread_name not in self.threads_unsuccess_exit:
                        self.threads_unsuccess_exit.append(answer)
                elif status == "ThreadsCrash":
                    if thread_name not in self.threads_unsuccess_exit:
                        self.threads_unsuccess_exit.append(answer)
                        self.terminate_all("ThreadsCrash", thread_name=thread_name)
                    self.logger.critical("'{}'-Thread returned ThreadCrash-Error. |ErrorTrackID:'{}'| (To see more about it track ErrorID in the logs)".format(thread_name,answer["track_id"]))
                    return False
                else:
                    self.logger.error("ThreadsWaiter: Unknown Status was send: '{}'. Break the execution! ".format(status), exc_info=self._logger_traceback)
                    sys.exit()


                self.threads_status_bucket.task_done()

            time.sleep(sec_to_wait)
            time_counter += sec_to_wait
            #self._check_threads()
            self._check_buckets()

        self.logger.debug("Waiter '{}' was stopped. ".format(waitername))

        return True


    def _get_new_status_bar(self, total, desc, unit, counter_format=False, bar_format=False):
        #counter_format
        if counter_format:
            if bar_format:
                counter = self.status_bars_manager.counter(total=total, desc=desc, unit=unit, leave=True, counter_format=counter_format, bar_format=bar_format)
            else:
                counter = self.status_bars_manager.counter(total=total, desc=desc, unit=unit, leave=True, counter_format=counter_format)
        else:
            if bar_format:
                counter = self.status_bars_manager.counter(total=total, desc=desc, unit=unit, leave=True, bar_format=bar_format)
            else:
                counter = self.status_bars_manager.counter(total=total, desc=desc, unit=unit, leave=True)
        return counter
 
    def _check_if_threads_still_alive(self):
        for thread in self.active_threads:
            if not thread.isAlive():
                yield False
            yield True





    def _check_buckets(self, thread_name="Thread0"):
        status = False
        if not self.threads_error_bucket.empty():
            while not self.threads_error_bucket.empty():
                e = self.threads_error_bucket.get()
                self.threads_error_bucket.task_done()
                self.logger.error("InsertionError(in_thread_error_bucket): '{}'-Thread throw following Exception: '{}'. ".format(e[0], e[1]), exc_info=self._logger_traceback)
                status = True

        if not self.channels_error_bucket.empty():
            while not self.channels_error_bucket.empty():
                e = self.channels_error_bucket.get()
                self.channels_error_bucket.task_done()
                self.logger.error("InsertionError(in_channel_error_bucket): '{}'-Thread ('{}') throw following Exception: '{}'. ".format(e[0], e[1],e[2]), exc_info=self._logger_traceback)
                status = True

        if status:
            self.logger.error("BucketChecker: Some threads/channels throw exception(s). Program can not be executed. ".format(), exc_info=self._logger_traceback)
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            self._terminated = True
            #sys.exit()


    def _print_summary_status(self):
        for thread in self.active_threads:
            thread_name = thread.getName()
            self.total_inserted_during_last_insert +=  self.inserted_insertion_status_general[thread_name]
            self.total_outsorted_insertion_during_last_insertion_process +=  self.outsorted_insertion_status_general[thread_name]
            self.total_error_insertion_during_last_insertion_process += self.error_insertion_status_general[thread_name]
        
        self.total_ignored_last_insertion += (self.total_outsorted_insertion_during_last_insertion_process+self.total_error_insertion_during_last_insertion_process)
        #self.logger.info("Summary for {}:\n Total inserted: {} rows; Total ignored: {} rows, from that was {} was error insertions and {} was out-sorted insertions (exp:  cleaned tweets/texts, ignored retweets, etc.).".format(thread_name, self.inserted_insertion_status_general[thread_name], self.error_insertion_status_general[thread_name]+ self.outsorted_insertion_status_general[thread_name], self.error_insertion_status_general[thread_name], self.outsorted_insertion_status_general[thread_name]))
        self.logger.info(">>>Summary<<< Total inserted: {} rows; Total ignored: {} rows, from that  {} was error insertions and {} was out-sorted insertions (exp:  cleaned tweets/texts, ignored retweets, ignored files with wrong structure etc.). If you want to see all ignored data than set 'mode'-option  to 'prod+' and consult logs which contain following pattern '*outsorted*'. ".format(self.total_inserted_during_last_insert, self.total_ignored_last_insertion, self.total_error_insertion_during_last_insertion_process, self.total_outsorted_insertion_during_last_insertion_process))
        
        if self.total_error_insertion_during_last_insertion_process >0:
            msg = "'{}'-ErrorInsertion was processed.".format(self.total_error_insertion_during_last_insertion_process)
            if self._raise_exception_if_error_insertion:
                raise ErrorInsertion, msg
            else:
                self.logger.error(msg)

    def _valid_input(self, language, preprocession, tokenizer, sent_splitter, pos_tagger, sentiment_analyzer):
        # if not self._decoding_to_unicode:
        #     self.logger.warning("InputValidation: Automaticly Decoding Input byte string to unicode string is deactivated. This could lead to wrong work of this tool. (ex. Emojis will not recognized in the right way, etc.). To ensure correct work of this Tool, please switch on following option ->  'decoding_to_unicode'.")

        if  language not in from_ISO639_2 and language != "test":
            self.logger.error("InputValidationError: Given Language '{}' is not valid code by ISO639_2. Please use the valid language code by ISO639_2.".format(language), exc_info=self._logger_traceback)
            yield False
            return 

        if language not in Corpus.supported_languages_tokenizer:
            self.logger.error("InputValidationError: Given Language '{}' is not supported by tokenizer.".format(language), exc_info=self._logger_traceback)
            yield False
            return

        if preprocession:
            ## Choice Tokenizer
            if tokenizer is False:
                tokenizer = True
                self.logger.critical("Tokenizer was automatically activated. For Text-Preprocessing tokenizer should be activate. ")
                #yield False
                #return
            if  tokenizer is True:
                try:
                    tokenizer = Corpus.tokenizer_for_languages[language][0]
                except:
                    self.logger.critical("Tokenized for '{}' is not implemented. Please switch off this function or select other language.".format(language))
                    yield False
                    return

            else:
                if tokenizer not in Corpus.supported_tokenizer:
                    self.logger.error("InputValidationError: Given Tokenizer '{}' is not supported.".format(tokenizer), exc_info=self._logger_traceback)
                    yield False
                if tokenizer not in Corpus.tokenizer_for_languages[language]:
                    self.logger.critical("InputValidationError: '{}'-tokenizer is not support '{}'-language. Please use another one. For this session the default one will be used. ".format(tokenizer, language))
                    tokenizer = Corpus.tokenizer_for_languages[language][0]
                    #yield False
            self.logger.debug("'{}'-Tokenizer was chosen.".format(tokenizer))

            # ## Choice Stemmer
            # if stemmer is False:
            #     stemmer = True
            #     self.logger.critical("Stemmer was automatically activated. For Text-Preprocessing tokenizer should be activate.")

            # if  stemmer is True:
            #     try:
            #         stemmer = Corpus.stemmer_for_languages[language][0]
            #     except:
            #         self.logger.critical("Stemmer for '{}' is not implemented. Please switch off this function or select other language.".format(language))
            #         yield False
            #         return
            # else:
            #     if stemmer not in Corpus.supported_languages_stemmer:
            #         self.logger.error("InputValidationError: Given Stemmer '{}' is not supported.".format(stemmer), exc_info=self._logger_traceback)
            #         yield False
            #     if stemmer not in Corpus.stemmer_for_languages[language]:
            #         self.logger.critical("InputValidationError: '{}'-stemmer is not support '{}'-language. Please use another one. For this session the default one will be used. ".format(stemmer, language))
            #         stemmer = Corpus.stemmer_for_languages[language][0]
            #         #yield False
            # self.logger.debug("'{}'-Stemmer was chosen.".format(stemmer))


            ## Choice Sent Splitter
            if sent_splitter:
                if language not in Corpus.supported_languages_sent_splitter:
                    self.logger.error("InputValidationError: Given Language '{}' is not supported by Sentences Splitter.".format(language), exc_info=self._logger_traceback)
                    yield False
                if sent_splitter is True:
                    sent_splitter = Corpus.sent_splitter_for_languages[language][0]
                else:
                    if sent_splitter not in Corpus.supported_sent_splitter:
                        self.logger.error("InputValidationError: Given SentenceSplitter '{}' is not supported.".format(sent_splitter), exc_info=self._logger_traceback)
                        yield False
                    if sent_splitter not in Corpus.sent_splitter_for_languages[language]:
                        self.logger.critical("InputValidationError: '{}'-SentenceSplitter  is not support '{}'-language. Please use another one. For this session the default one will be used. ".format(sent_splitter, language))
                        sent_splitter = Corpus.sent_splitter_for_languages[language][0]
                self.logger.debug("'{}'-SentSplitter was chosen.".format(sent_splitter))


            ## Choice POS Tagger
            if pos_tagger:

                if language not in Corpus.supported_languages_pos_tagger:
                    self.logger.error("InputValidationError: Given Language '{}' is not supported by POS-Tagger.".format(language), exc_info=self._logger_traceback)
                    yield False
                if pos_tagger is True:
                    try:
                        pos_tagger = Corpus.pos_tagger_for_languages[language][0]
                    except:
                        self.logger.critical("POS-Tagger for '{}' is not imlemented. Please switch off this function or select other language.".format(language))
                        yield False
                        return

                else:
                    if pos_tagger not in Corpus.supported_pos_tagger:
                        self.logger.error("InputValidationError: Given POS-Tagger '{}' is not supported.".format(pos_tagger), exc_info=self._logger_traceback)
                        yield False
                    if not self._use_test_pos_tagger:
                        if pos_tagger not in Corpus.pos_tagger_for_languages[language]:
                            self.logger.critical("InputValidationError: '{}'-POS-Tagger is not support '{}'-language. Please use another one. For this session the default one will be used. ".format(pos_tagger, language))
                            pos_tagger = Corpus.pos_tagger_for_languages[language][0]
                            #yield True
                    if not  sent_splitter:
                        self.logger.error("InputError: POS-Tagging require sentence splitter. Please use an option to activate it!",  exc_info=self._logger_traceback)
                        yield False
                
                if self._use_test_pos_tagger:
                  pos_tagger = "tweetnlp"


                self.logger.debug("'{}'-POS-Tagger was chosen.".format(pos_tagger))


            if sentiment_analyzer:
                if language not in Corpus.supported_languages_sentiment_analyzer:
                    self.logger.error("InputValidationError: Given Language '{}' is not supported by SentimentAnalyzer.".format(language), exc_info=self._logger_traceback)
                    yield False
                if sentiment_analyzer is True:
                    try:
                        sentiment_analyzer = Corpus.sentiment_analyzer_for_languages[language][0]
                    except:
                        self.logger.critical("SentimentAnalyzer for '{}' is not imlemented. Please switch off this function or select other language.".format(language))
                        yield False
                        return

                else:
                    if sentiment_analyzer not in Corpus.supported_sentiment_analyzer:
                        self.logger.error("InputValidationError: Given SentimentAnalyzer '{}' is not supported.".format(sentiment_analyzer), exc_info=self._logger_traceback)
                        yield False

                self.logger.debug("'{}'-SentimentAnalyzer was chosen.".format(sentiment_analyzer))


        else:
            self.logger.warning("Preprocessing is disable. -> it will be not possible to compute statistics for it. Please enable preprocessing, if you want to compute statistics later.")
            #yield False
        yield True 
        yield {
                "tokenizer": tokenizer, 
                "sent_splitter": sent_splitter, 
                "pos_tagger": pos_tagger,  
                "sentiment_analyzer": sentiment_analyzer, 
                }
        return 





    def _compute_tags_to_delete(self):
        #p((del_url, self._del_punkt, self._del_num, self._del_mention, ))
        tags_to_delete = set()
        if self._del_url:
            tags_to_delete.add("URL")
        if self._del_punkt:
            tags_to_delete.add("symbol")
        if self._del_num:
            tags_to_delete.add("number")
        if self._del_mention:
            tags_to_delete.add("mention")
        if self._del_hashtag:
            tags_to_delete.add("hashtag")
        return tags_to_delete



    def _clean_sents_list(self, inp_sent_list):
        #p(self._tags_to_delete, "self._tags_to_delete")
        cleaned = []
        for sents in inp_sent_list:
            cleaned_sent = []
            for token in sents:
                #p(token, "token")
                if token[1] not in self._tags_to_delete:
                    cleaned_sent.append(token)
                else:
                    cleaned_sent.append((None, self._cleaned_tags[token[1]]))
            cleaned.append(cleaned_sent)

        return cleaned
        # for sent in inp_sent_list:
        #     #print token 
        #     if token[1] in tags_to_delete:
        #         #p(token, c="r")
        #         continue
        #     cleaned.append(token)
        # return cleaned


    # def _categorize_token_list(self, inp_token_list):
    #     if self._tokenizer != "somajo":
    #         return categorize_token_list(inp_token_list)


    def _lower_case_sents(self, inpsents):
            lower_cased = []
            for sents in inpsents:
                lower_cased_sent = []
                for token in sents:
                    #p(token[0].lower(), c="m")
                    tok = token[0]
                    if tok:
                        lower_cased_sent.append((tok.lower(), token[1]))
                    else:
                        lower_cased_sent.append(token)
                
                lower_cased.append(lower_cased_sent)
            return lower_cased



    def _re_recognize_complex_clustered_emojis(self,inp_list):
        #p(inp_list,"inp_list")
        pattern = ['EMOIMG',"emoticon",]
        prev_pos = ""
        collected_elem = ()
        new_output_list = []
        #p(inp_list, "111inp_list")
        #### Step 1: collect all EMOIMG in neibourghood in one token
        for token_container in inp_list:
            #p(token_container, "token_container", c="r")
            if token_container[1] in pattern:
                if prev_pos:
                    #p((prev_pos, token_container), c="m")
                    if prev_pos == token_container[1]:
                        new_text_elem = u"{}{}".format(collected_elem[0], token_container[0])
                        collected_elem = (new_text_elem, collected_elem[1])
                        #continue
                    else:
                        new_output_list.append(collected_elem)
                        prev_pos = token_container[1]
                        collected_elem = token_container
                        #continue
                else:
                    prev_pos = token_container[1]
                    collected_elem = token_container
                    #continue
            else:
                if prev_pos:
                    new_output_list.append(collected_elem)
                    new_output_list.append(token_container)
                    collected_elem = ()
                    prev_pos = ""

                else:
                    new_output_list.append(token_container) 
        #p(inp_list, "222inp_list")
        return inp_list



    def _normalize_emojis(self,inp_list):
        #p(inp_list,"inp_list")
        pattern = ['EMOIMG',"emoticon",]
        prev = ""
        collected_elem = ()
        new_output_list = []

        for token_container in inp_list:
            #p(token_container, "token_container", c="r")
            if token_container[1] in pattern:
                if prev:
                    #p((prev, token_container), c="m")
                    if prev == token_container[0]:
                        new_text_elem = u"{}{}".format(collected_elem[0], token_container[0])
                        collected_elem = (new_text_elem, collected_elem[1])
                        #continue
                    else:
                        new_output_list.append(collected_elem)
                        prev = token_container[0]
                        collected_elem = token_container
                        #continue
                else:
                    prev = token_container[0]
                    collected_elem = token_container
                    #continue
            else:
                if prev:
                    new_output_list.append(collected_elem)
                    new_output_list.append(token_container)
                    collected_elem = ()
                    prev = ""

                else:
                    new_output_list.append(token_container)

        if prev:
            new_output_list.append(collected_elem)
            collected_elem = ()
            prev = ""
        #p(new_output_list, "new_output_list",c="r")
        return new_output_list


    def _error_correction_after_somajo_tokenization(self,output):
        new_output = []
        token_index = -1
        ignore_next_step = False
        e = ("_","-")

        try:
            output[1]
        except:
            return output
        #p(output,"11output")

        ### ReCategorize Symbols
        output = [(token_cont[0], u"symbol") if text_is_punkt(token_cont[0]) and token_cont[1]!= "symbol" else token_cont  for token_cont in output ]
        #p(output,"22output",c="m")
        
        for i,tok in zip(xrange(len(output)),output):
            if i == 0:
                new_output.append(tok)

            elif i > 0:
                
                last_elem = new_output[-1]
                #p((last_elem,tok))
                #if last_elem[1] == 
                #p((last_elem[1], tok[1]))
                if last_elem[1] == "emoticon" and tok[1] == 'regular':
                    if last_elem[0][-1] == tok[0][0]:
                        new_output[-1] = (last_elem[0]+tok[0], last_elem[1])
                    else:
                        new_output.append(tok)
                elif last_elem[1] in ("symbol", "regular", 'EMOASC','emoticon') and tok[1] == 'symbol':
                    if last_elem[0][-1] == tok[0][0]:
                        new_output[-1] = (last_elem[0]+tok[0], last_elem[1])
                        #new_output[-1] = (last_elem[0]+tok[0], "FUCK")
                    elif last_elem[0][-1] in self._emo_sym and tok[0][0] in self._emo_sym:
                        #p((tok, last_elem))
                        if (last_elem[0][0] in self.em_start and last_elem[0][-1]in self.em_end) or (last_elem[0][-1] in self.em_start and last_elem[0][0]in self.em_end):
                            new_output.append(tok)
                        else:
                            new_output[-1] = (last_elem[0]+tok[0], "EMOASC")

                    else:
                        new_output.append(tok)
                elif last_elem[1] == "mention" and tok[1] == 'regular':
                    #print last_elem[0][-1],tok[0][0]
                    if tok[0][0] in e:
                        new_output[-1] = (last_elem[0]+tok[0], last_elem[1])
                        #new_output[-1] = (last_elem[0]+tok[0], "FUCK")
                    else:
                        new_output.append(tok)
                else:
                    new_output.append(tok)

                ## check if last two elements possibly are same
                if len(new_output)>1:
                    last_item = new_output[-1]
                    bevore_the_last_item = new_output[-2]
                    
                    if last_item[0][0] == bevore_the_last_item[0][0]:
                        if len(rle.del_rep(last_item[0])) and  len(rle.del_rep(bevore_the_last_item[0])) == 1 :
                            #p(new_output, "111new_output", c="r")
                            if last_item[1] == "symbol" and bevore_the_last_item[1] == "symbol":
                                poped = new_output.pop()
                                new_output[-1] = (last_item[0]+poped[0], poped[1])
        #p(new_output, "22new_output", c="r")

        return new_output







    ###########################Preprocessing###############
    def _preprocessing(self, inp_str, thread_name="Thread0", log_ignored=True, row=False):
        #self.logger.debug("Preprocessing: '{}'-Thread do preprocessing.".format( thread_name ))

        ### convert to unicode, if needed!!!=) 
        ## it is important, fo right works of further preprocessing steps 
        try: 
            output = inp_str.decode("utf-8")
        except:
            output = inp_str

        # p(type(output), "output")

        #p(self.preprocessors)
        #time.sleep(5)
        # Preprocessing woth Python !!! (gut) https://www.kdnuggets.com/2018/03/text-data-preprocessing-walkthrough-python.html
        # python code: https://de.dariah.eu/tatom/preprocessing.html

        #############Step 0 ########################
        # Step 0:  Noise Removal (https://www.kdnuggets.com/2017/12/general-approach-preprocessing-text-data.html)
            # remove text file headers, footers
            # remove HTML, XML, etc. markup and metadata
            # extract valuable data from other formats, such as JSON, or from within databases
            # if you fear regular expressions, this could potentially be the part of text preprocessing in which your worst fears are realized
        #was_found= False
        # if 1111 == row["id"] or "1111" == row["id"]:
        #     self.logger.critical(("start",output))
        #     was_found = True

        if self._del_html:
            output = removetags(output)  
            output = remove_html_codded_chars(output)    # delete html-codded characters sets 
            #if was_found:
            #    self.logger.critical(("del_html",output))
            #p(output, "html_deleted")
        #if self._del_rep:

        ############Step 1 ########################
        ##### Step 1: Language Classification
        #self.logger.critical("LANGPREPROC in {}".format(thread_name))
        #### time.sleep(10)
        if self._lang_classification:
            output_with_deleted_repetitions = self.preprocessors[thread_name]["rle"].del_rep(output) #output #self._rle.del_rep(output)
            #self.logger.critical(output_with_deleted_repetitions)
            lang = langid.classify(output_with_deleted_repetitions)[0]
            if lang != self._language:
                #p(output_with_deleted_repetitions, "lan_outsorted")
                try:
                    if log_ignored:
                        row = row if row else ":ORIG_ROW_WASNT_GIVEN:"
                        self.logger.outsorted_corpus(u"LangClassification: Following row was out-sorted and ignored. Reason: Given language not equal to recognized language ('{}'!='{}');  TextElement: '{}'; FullRow: '{}'. ".format(self._language, lang, output, row))
                except Exception, e:
                    #p(str(e),"e")
                    self.logger.error(u"LangClassificationResultsStdOut: See Exception: '{}'. ".format(e))
                return None


        #############Step 2 ########################
        # Step 2.1: Tokenization &  (https://www.kdnuggets.com/2017/12/general-approach-preprocessing-text-data.html)
        #p(inp_str, "inp_str")
        output = self.tokenize(output, thread_name=thread_name)
        output = [(token[0].replace("'", '"'), token[1]) if "'" in token[0] else token for token in output ]
        #if not output:
        #    return "terminated"
        #if was_found:
        #    self.logger.critical(("tokenize",output))

        #p((len(output),output), "tokenized")
        #time.time(3)


        # Step 2.2
        if self._tokenizer == "somajo":
            output = self._error_correction_after_somajo_tokenization(output)
            #p((len(output),output), "error_corrected")
        else:
            #############Step 3 ########################
            # Step 3: Categorization (if wasn't done before)
            #if self._tokenizer != "somajo":
            output = categorize_token_list(output)
            #p(categorize_token_list, "categorize_token_list")



        #############Step 4 ########################
        # Step 4: Categorization (if wasn't done before)
        #if  self._tokenizer == "somajo":  #self._diff_emoticons and
        
        output = recognize_emoticons_types(output)
        #p(output, "recognize_emoticons_types")

        #sys.exit()

        #############Step 5 ########################
        # Step 5: normalization - Part0
        #### Normalisation Emojis
        if self._emojis_normalization:
            #output = self._re_recognize_complex_clustered_emojis(output)
            output = self._normalize_emojis(output)
            #p(output, "emojis_normalization")



        #############Step 6 ########################
        #Step 6:  Segmentation
        if self._sent_splitter:
            output = self.split_sentences(output, thread_name=thread_name)
            #p(output, c="r")
            #if output
            if not output:
                return "terminated"
            #p((len(sentences),sentences), "sentences", c="r")
            #p(len(output), "splitted")
            #p(output, "splitted")
            #p((len(output),output), "splitted")

        else:
            output = [output]
        #if was_found:
        #    self.logger.critical(("sent_splitter",output))
        #p(output, "sent_splitted")




        #############Step 8 ########################
        # Step 8: Tagging
        #output, cutted_ = 
        #p(output, "output")
        if self._pos_tagger: #u'EMOASC', 'EMOIMG'
            non_regular_tokens = self._backup_non_regular_tokens(output)
            #p(non_regular_tokens, "non_regular_tokens")
            output = [self.tag_pos([token[0] for token in sent ], thread_name=thread_name) for sent in output]
            if not output[0]:
                return "terminated"
            output = self._rebuild_non_regular_tokens(non_regular_tokens, output)
            #p(output, "tagged")
        #if was_found:
        #    self.logger.critical(("pos",output))
        #############Step  ########################
        # Step : WDS


        #############Step 7 ########################
        # Step 7: normalization - Part1
            #> Stemming or Lemmatization (https://www.kdnuggets.com/2017/12/general-approach-preprocessing-text-data.html)
            #remove numbers (or convert numbers to textual representations)
            #remove punctuation (generally part of tokenization, but still worth keeping in mind at this stage, even as confirmation)
        output = self._clean_sents_list(output)
        #if was_found:
        #    self.logger.critical(("cleaned",output))
        #p(output, "cleaned")




        #############Step 9 ########################
        # Step 9: normalization
            #> Stemming or Lemmatization (https://www.kdnuggets.com/2017/12/general-approach-preprocessing-text-data.html)
            #> case normalisation (lower case)
            #(NO)remove default stop words (general English stop words) 
        if not self._case_sensitiv:
            output = self._lower_case_sents(output)
            #p(output, "lowercased")
        #if was_found:
        #    self.logger.critical(("lowercased",output))


        #############Step  10 ########################
        # Step 10: Emotikons? werden die durch den Tokenizer zu einer Entität?



        #############Step 11 ########################
        # Step 11: Sentiment Analysis
        output_with_sentiment = []
        #p(output, "output")
        for sent in output:
            #p(" ".join([token[0] for token in sent]), c="m")
            #p(sent)
            if self._sentiment_analyzer:
                polarity = self.get_sentiment(" ".join([token[0] for token in sent if token[0]]))
                #p(polarity, "polarity", c="r")
            else:
                polarity = (None, None)
            output_with_sentiment.append((sent, polarity))
        #for 
        output = output_with_sentiment
        #if was_found:
        #    self.logger.critical(("sentiment",output))
        #p(output, "sentiment")

        #was_found =False

        return output



    def _backup_non_regular_tokens(self,output):
        #["url", "emoji", "emoticon", "symbol", "mention", "hashtag"]
        #"regular"
        non_regular_tokens = []
        sent_index = -1
        for sent in output:
            sent_index += 1
            token_index = -1
            for token in sent:
                token_index += 1
                if token[1] != "regular":
                    #if token[1] != "emoticon":
                    non_regular_tokens.append((sent_index, token_index, token[1]))

        return non_regular_tokens


    def _rebuild_non_regular_tokens(self, non_regular_tokens, output):
        for backup_data in non_regular_tokens:
            #p(backup_data,"backup_data")
            #p(output,"output")
            output[backup_data[0]][backup_data[1]] = (output[backup_data[0]][backup_data[1]][0], backup_data[2])
        return output



    ############Tokenization#############

    def tokenize(self,inp_str, thread_name="Thread0"):
        try:
        
            #self.logger.low_debug("'{}'-Tokenizer: Tokenizer was called from '{}'-Thread.".format(self._tokenizer, thread_name))
            
            if self._tokenizer == "somajo":
                return self._tokenize_with_somajo(inp_str, thread_name=thread_name)
            elif self._tokenizer == "nltk":
                return self._tokenize_with_nltk(inp_str, thread_name=thread_name)
            else:
                self.logger.error("TokenizationError: No one Tokenizer was chooses.", exc_info=self._logger_traceback)
                return False
        except KeyboardInterrupt:
            self.logger.critical("TokenizerError:  in '{}'-Thread get an  KeyboardInterruption.".format(thread_name))
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            self._terminated = True
            #self.terminate_all("KeyboardInterrupt")
            return False
        except Exception, e:
            self.logger.error("TokenizerError:  in '{}'-Thread. See Exception '{}'.".format(thread_name,e))
            self.terminate = True
            return False
            #sys.exit()
            #return [("",""),("","")]



    def _set_tokenizer(self, split_camel_case=True, language="de", thread_name="Thread0"):
        token_classes=True
        extra_info=False
        self.logger.low_debug("INIT-Tokenizer: Start the initialization of '{}'-Tokenizer for '{}'-Thread.".format(self._tokenizer,thread_name))
        if self._tokenizer == "somajo":
            tokenizer_obj = self._get_somajo_tokenizer( split_camel_case=split_camel_case, token_classes=token_classes, extra_info=extra_info, language=language,thread_name=thread_name)
            if not tokenizer_obj:
                self.logger.error("Tokenizer for '{}'-Thread wasn't initialized.".format(thread_name), exc_info=self._logger_traceback)
                return False
        elif self._tokenizer == "nltk":
            #from nltk import word_tokenize
            #word_tokenize(tweet)
            tokenizer_obj = TweetTokenizer()
        else:
            self.logger.error("INIT-TokenizerError '{}'-tokenizer is not supported. ".format(self._tokenizer), exc_info=self._logger_traceback)
            return False
        self.preprocessors[thread_name]["tokenizer"] = tokenizer_obj
        self.logger.debug("INIT-Tokenizer: '{}'-Tokenizer for '{}'-Thread was initialized.".format(self._tokenizer,thread_name))
        return True


    def _tokenize_with_somajo(self,inp_str, thread_name="Thread0"):
        #p(self.preprocessors)
        #self.logger.exception(self.preprocessors)
        #self.logger.exception(self.preprocessors[thread_name]["tokenizer"])
        self.preprocessors[thread_name]["tokenizer"].send(inp_str)
        return self.preprocessors[thread_name]["tokenizer"].receive()


    def _tokenize_with_nltk(self, inp_str, thread_name="Thread0"):
        return self.preprocessors[thread_name]["tokenizer"].tokenize(inp_str)

    def _get_somajo_tokenizer(self, split_camel_case=True, token_classes=True, extra_info=False, language="de", thread_name="Thread0"):
        self.logger.low_debug("Start the initialisation of the SoMaJo-Tokenizer.")
        try:
            args = 'split_camel_case={}, token_classes={}, extra_info={}, language="{}" '.format(split_camel_case, token_classes, extra_info, language)
            gw_id = "tokenizer_{}".format(thread_name)
            #p(gw_id, "gw_id")
            #p(self.opened_gateways, "self.opened_gateways")
            gw  = self.opened_gateways.makegateway("popen//python=python3//id={}".format(gw_id))
            channel = gw.remote_exec("""
                import sys, gc
                from somajo import Tokenizer
                #print "hhh"
                tokenizer = Tokenizer({2})
                channel.send("ready")
                while True:
                    received = channel.receive()
                    if received == -1:
                        del tokenizer
                        gc.collect()
                        channel.send("stopped")
                        break
                    channel.send(tokenizer.tokenize(received))
                sys.exit()
                        """.format(self._logger_level, gw_id,args))
            #channel_error_bucket = pickle.dumps(self.channels_error_bucket)
            #channel.send(channel_error_bucket)
            answer = channel.receive()
            #p( answer, "answer")
            if answer == "ready":
                self.logger.low_debug("ChannelReady: Channel for Somajo tokenizer ('{}') is open and ready. ".format(thread_name))
                return channel
            else:
                self.logger.error("SomajoTokenizerGetterError: Channel wasn't opended properly. Got following answer: '{}'. and was aborted!!! ".format(answer))
                self._terminated = True
                self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                return False
            
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.channels_error_bucket.put((thread_name,"Tokenizer",e))
            self.logger.error("SomajoTokenizerGetterError: '{}'-Thread throw following exception: '{}'. ".format(thread_name, e), exc_info=self._logger_traceback)
            #T, V, TB = sys.exc_info()
            
            self.threads_status_bucket.put({"name":thread_name, "status":"failed", "exception":e})
            #sys.exit()
            return False
        






    # ###########Word Stemmer###########


    # def stemm(self,inp_str, thread_name="Thread0"):
    #     try:
    #         self.logger.low_debug("'{}'-Stemmer: Stemmer was called from '{}'-Thread.".format(self._tokenizer, thread_name))
    #         if self._stemmer == "pystemmer":
    #             return self._stemm_with_pystemmer(inp_str, thread_name=thread_name)
    #         else:
    #             self.logger.error("StemmError: selected stemmer '{}' is not supported.".format(self._stemmer), exc_info=self._logger_traceback)
    #             return False
    #     except KeyboardInterrupt:
    #         self.logger.critical("StemmerError:  in '{}'-Thread get an  KeyboardInterruption.".format(thread_name))
    #         self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
    #         self._terminated = True
    #         #self.terminate_all("KeyboardInterrupt")
    #         return False
    #     except Exception, e:
    #         self.logger.error("StemmerError:  in '{}'-Thread. See Exception '{}'.".format(thread_name,e))
    #         self.terminate = True
    #         return False
    #         #sys.exit()
    #         #return [("",""),("","")]


    # def _set_stemmer(self, thread_name="Thread0"):
    #     self.logger.low_debug("INIT-Stemmer: Start the initialization of '{}'-Stemmer for '{}'-Thread.".format(self._stemmer,thread_name))
    #     if self._stemmer == "pystemmer":
    #         try:
    #             tokenizer_obj = Stemmer.Stemmer(from_ISO639_2[self._language])
    #         except Exception as e:
    #             self.logger.error("Stemmer for '{}'-Thread wasn't initialized.".format(thread_name), exc_info=self._logger_traceback)
    #             return False

    #     else:
    #         self.logger.error("INIT-StemmerError '{}'-stemmer is not supported. ".format(self._stemmer), exc_info=self._logger_traceback)
    #         return False
    #     self.preprocessors[thread_name]["stemmer"] = stemmer_obj
    #     self.logger.debug("INIT-Stemmer: '{}'-Stemmer for '{}'-Thread was initialized.".format(self._stemmer,thread_name))
    #     return True


    # def _stemm_with_pystemmer(self,word, thread_name="Thread0"):
    #     #p(self.preprocessors)
    #     #self.logger.exception(self.preprocessors)
    #     #self.logger.exception(self.preprocessors[thread_name]["stemmer"])
        
    #     return self.preprocessors[thread_name]["stemmer"].stemWord(word)





    ############Sentence Splitting############

    def split_sentences(self,inp_list, thread_name="Thread0"):
        try:
        
            #self.logger.low_debug("'{}'-SentSplitter: SentSplitter was called from '{}'-Thread.".format(self._sent_splitter, thread_name))
            if self._sent_splitter == "somajo":
                return self._split_sentences_with_somajo(inp_list,thread_name=thread_name)
        except KeyboardInterrupt:
            self.logger.critical("SentSplitterError:  in '{}'-Thread get an  KeyboardInterruption.".format(thread_name))
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            self._terminated = True
            #self.terminate_all("KeyboardInterrupt")
            return False  
        except Exception, e:
            self.logger.error("SentSplitterError:  in '{}'-Thread. See Exception '{}'.".format(thread_name,e))
            self.terminate = True
            #return [[("",""),("","")],[("",""),("","")]]
            #sys.exit()
            return False

    def _set_sent_splitter(self, is_tuple=True,thread_name="Thread0"):
        #is_tuple  -means, that input tokens are tuples with additonal information about their type (ex: URLS, Emoticons etc.)
        self.logger.low_debug("INITSentSplitter: Start the initialization of '{}'-SentSplitter for '{}'-Thread.".format(self._sent_splitter,thread_name))
        #p(self._sent_splitter)
        if self._sent_splitter == "somajo":
            sent_splitter_obj = self._get_somajo_sent_splitter( is_tuple=is_tuple, thread_name=thread_name)
            if not sent_splitter_obj:
                self.logger.error("SentSplitter for '{}'-Thread wasn't initialized.".format(thread_name))
                return False
        self.preprocessors[thread_name]["sent_splitter"] = sent_splitter_obj
        self.logger.debug("INITSentSplitter: '{}'-SentSplitter for '{}'-Thread was initialized.".format(self._sent_splitter,thread_name))
        return True

    def _split_sentences_with_somajo(self,inp_list, thread_name="Thread0"):
        #self.logger.low_debug("SoMaJo-SentSpliter: Start splitting into sentences.")
        self.preprocessors[thread_name]["sent_splitter"].send(inp_list)
        return self.preprocessors[thread_name]["sent_splitter"].receive()


    def _get_somajo_sent_splitter(self, is_tuple=True, thread_name="Thread0"):
        try:
            args = 'is_tuple="{}" '.format(is_tuple)
            gw  = self.opened_gateways.makegateway("popen//python=python3//id=sent_splitter_{}".format(thread_name))
            #self.opened_gateways.append(gw)
            channel = gw.remote_exec("""
                import sys,gc
                from somajo import  SentenceSplitter
                sentence_splitter = SentenceSplitter({})
                channel.send("ready")
                while True:
                    received = channel.receive()
                    if received == -1:
                        del sentence_splitter
                        gc.collect()
                        channel.send("stopped")
                        break
                    channel.send(sentence_splitter.split(received))
                sys.exit()
                    """.format(args))

            answer = channel.receive()
            if answer == "ready":
                self.logger.low_debug("ChannelReady: Channel for SentSplitter ('{}') is open and ready. ".format(thread_name))
                return channel
            else:
                self.logger.error("SomajoSentSplitterGetterError: Channel wasn't opended properly. Got following answer: '{}'. and was aborted!!! ".format(answer))
                self._terminated = True
                self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                return False



        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("SomajoSentSplitterGetterError: '{}'-Thread throw following exception: '{}'. ".format(thread_name, e), exc_info=self._logger_traceback)
            self.channels_error_bucket.put((thread_name,"SentSplitter",e))
            #T, V, TB = sys.exc_info()
            
            self.threads_status_bucket.put({"name":thread_name, "status":"failed", "exception":e})
            return False

        





    ###########PoS-Tagging###########

    def tag_pos(self,inp_list, thread_name="Thread0"):
        try:
        
            #self.logger.low_debug("'{}'-POSTagger: POS-tagger was called from '{}'-Thread.".format(self._sent_splitter, thread_name))
            if self._pos_tagger == "someweta":
                #p("someweta")
                return self._tag_pos_with_someweta(inp_list, thread_name=thread_name)
            elif self._pos_tagger == "tweetnlp":
                #p("tweetnlp")
                return self._tag_pos_with_tweetnlp(inp_list)
        except KeyboardInterrupt:
            self.logger.critical("POSTaggerError:  in '{}'-Thread get an  KeyboardInterruption.".format(thread_name))
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            self._terminated = True
            #self.terminate_all("KeyboardInterrupt")
            return False         
        except Exception, e:
            #p((inp_list,self._pos_tagger, self.preprocessors[thread_name]["pos-tagger"]))
            self.logger.error("POSTaggerError: in '{}'-Thread. See Exception '{}'.".format(thread_name,e))
            self.terminate = True
            #return [[("",""),("","")],[("",""),("","")]]
            #sys.exit()
            return False



    def _set_pos_tagger(self, thread_name="Thread0"):
        #p(self._pos_tagger)
    
        self.logger.low_debug("INIT-POS-Tagger: Start the initialization of '{}'-pos-tagger for '{}'-Thread.".format(self._pos_tagger,thread_name))
        if self._pos_tagger == "someweta":
            model_name = Corpus.pos_tagger_models[self._pos_tagger][self._language][0]
            path_to_model = os.path.join(path_to_someweta_models,model_name)
            if not os.path.isfile(path_to_model):
                self.logger.error("Current Model wasn't found: '{}'. ".format(path_to_model))
                return False
            #p((model_name, path_to_model))
            #self.logger.critical("{}, {}".format(model_name, path_to_model))
            pos_tagger_obj = self._get_someweta_pos_tagger(path_to_model,thread_name=thread_name)
            if not pos_tagger_obj:
                self.logger.error("POS-Tagger for '{}'-Thread wasn't initialized.".format(thread_name), exc_info=self._logger_traceback)
                return False
            #p(pos_tagger_obj)
            #sys.exit()
        elif self._pos_tagger == "tweetnlp":
            try:
                if not check_script_is_present():
                    self.logger.error("TweetNLP Java-Script File wasn't found", exc_info=self._logger_traceback)
                    return False
            except Exception as e:
                self.logger.error("TweetNLP_tagger wasn't initialized. Please check if JAVA was installed on your PC. Exception: '{}'.".format(repr(e)) )
                self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                self.terminate = True
                return False
            pos_tagger_obj = None
        self.preprocessors[thread_name]["pos-tagger"] = pos_tagger_obj
        self.logger.debug("INIT-POS-Tagger: '{}'-pos-tagger for '{}'-Thread was initialized.".format(self._pos_tagger,thread_name))
        return True


    def _tag_pos_with_someweta(self,inp_list, thread_name="Thread0"):
        self.preprocessors[thread_name]["pos-tagger"].send(inp_list)
        tagged = self.preprocessors[thread_name]["pos-tagger"].receive()
        #p(tagged, "tagged_with_someweta")
        return tagged

    def _tag_pos_with_tweetnlp(self,inp_list):
        #CMUTweetTagger.runtagger_parse(['example tweet 1', 'example tweet 2'])
        #p(runtagger_parse(inp_list), "tagged_with_tweet_nlp")
        return runtagger_parse(inp_list)


    def _get_someweta_pos_tagger(self, path_to_model, thread_name="Thread0"):
        try:
            gw  = self.opened_gateways.makegateway("popen//python=python3//id=pos_{}".format(thread_name))
            #self.opened_gateways.append(gw)
            channel = gw.remote_exec("""
                    import sys, gc
                    from someweta import  ASPTagger

                    asptagger = ASPTagger(5, 10)
                    asptagger.load('{}')

                    channel.send("ready")
                    while True:
                        received = channel.receive()
                        if received == -1:
                            del asptagger
                            gc.collect()
                            channel.send("stopped")
                            break
                        channel.send(asptagger.tag_sentence(received))

                    sys.exit()
                    """.format(path_to_model))

            answer = channel.receive()
            if answer == "ready":
                self.logger.low_debug("ChannelReady: Channel for SeMeWeTa-POSTagger ('{}') is open and ready. ".format(thread_name))
                return channel
            else:
                self.logger.error("SoMeWeTaPOSTaggerGetterError: Channel wasn't opended properly. Got following answer: '{}'. and was aborted!!! ".format(answer))
                self._terminated = True
                self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                return False



        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("SoMeWeTaPOSTaggerGetterError: '{}'-Thread throw following exception: '{}'. ".format(thread_name,e), exc_info=self._logger_traceback)
            self.channels_error_bucket.put((thread_name,"POSTagger",e))
            #T, V, TB = sys.exc_info()
            
            self.threads_status_bucket.put({"name":thread_name, "status":"failed", "exception":e})
            return False
        














    ###########Sentiment###########

    def get_sentiment(self,inp_str, thread_name="Thread0"):
    
        #self.logger.low_debug("'{}'-SentimentAnalyzer: was called from '{}'-Thread.".format(self._sent_splitter, thread_name))
        if self._sentiment_analyzer == "textblob":
            return self._get_sentiment_with_textblob(inp_str, thread_name=thread_name)
        # elif self._pos_tagger == "tweetnlp":
        #     return self._tag_pos_with_tweetnlp(inp_str)





    # def _set_sentiment_analyzer(self, thread_name="Thread0"):
    #     #p(self._pos_tagger)
    #     self.logger.debug("INIT-SentimentAnalyzer: Start the initialization of '{}'-sentiment analyzer for '{}'-Thread.".format(self._sentiment_analyzer,thread_name))
    #     if self._sentiment_analyzer == "textblob":
    #         if self._language == "fr":
    #             sentiment_analyser_obj = 
    #         elif self._language =="de":
    #             sentiment_analyser_obj = 
    #         elif self._language == "en":
    #             sentiment_analyser_obj= 

    #         if not sentiment_analyser_obj:
    #             self.logger.error("SentimentAnalyzer for '{}'-Thread wasn't initialized.".format(thread_name))
    #             return False


    #     self.preprocessors[thread_name]["sentiment_analyser"] = sentiment_analyser_obj
    #     self.logger.debug("INIT-SentimentAnalyzer: '{}'-pos-tagger for '{}'-Thread was initialized.".format(self._sentiment_analyzer,thread_name))
    #     return True




    def get_sent_sentiment_with_textblob_for_en(self, sent_as_str):
        '''
        Utility function to classify sentiment of passed sent_as_str
        using textblob's sentiment method
        '''
        # create TextBlob object of passed sent_as_str text
        analysis = TextBlob(sent_as_str)
        # set sentiment
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return ('positive', polarity)
        elif polarity == 0:
            return ('neutral',polarity)
        else:
            return ('negative',polarity)




    def get_sent_sentiment_with_textblob_for_de(self, sent_as_str):
        '''
        # https://media.readthedocs.org/pdf/textblob-de/latest/textblob-de.pdf
        Utility function to classify sentiment of passed sent_as_str
        using textblob's sentiment method
        '''
        # create TextBlob object of passed sent_as_str text
        analysis = TextBlobDE(sent_as_str)
        # blob.tags # [('Der', 'DT'), ('Blob', 'NN'), ('macht', 'VB'),
        #             #  ('in', 'IN'), ('seiner', 'PRP$'), ...]
        # blob.noun_phrases # WordList(['Der Blob', 'seiner unbekümmert-naiven Weise',
        #             #           'den gewissen Charme', 'hölzerne Regie',
        #             #           'konfuse Drehbuch'])
        # set sentiment
        #for sentence in blob.sentences: print(sentence.sentiment.polarity):
            # 1.0 # 0.0

        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return ('positive', polarity)
        elif polarity == 0:
            return ('neutral',polarity)
        else:
            return ('negative',polarity)

    def get_sent_sentiment_with_textblob_for_fr(self, sent_as_str):
        '''
        #https://github.com/sloria/textblob-fr
        # https://media.readthedocs.org/pdf/textblob-de/latest/textblob-de.pdf
        Utility function to classify sentiment of passed sent_as_str
        using textblob's sentiment method
        '''
        # create TextBlob object of passed sent_as_str text
        tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        analysis = tb(sent_as_str)
        #analysis.sentiment

        # blob.tags # [('Der', 'DT'), ('Blob', 'NN'), ('macht', 'VB'),
        #             #  ('in', 'IN'), ('seiner', 'PRP$'), ...]
        # blob.noun_phrases # WordList(['Der Blob', 'seiner unbekümmert-naiven Weise',
        #             #           'den gewissen Charme', 'hölzerne Regie',
        #             #           'konfuse Drehbuch'])
        # set sentiment
        polarity = analysis.sentiment[0]
        if polarity > 0:
            return ('positive', polarity)
        elif polarity == 0:
            return ('neutral',polarity)
        else:
            return ('negative',polarity)





    def _get_sentiment_with_textblob(self,inp_str, thread_name="Thread0"):
        if self._language == "de":
            return self.get_sent_sentiment_with_textblob_for_de(inp_str)
        elif self._language in ["en", "test"]:
            return self.get_sent_sentiment_with_textblob_for_en(inp_str)
        elif self._language == "fr":
            return self.get_sent_sentiment_with_textblob_for_fr(inp_str)
        else:
            self.logger.error("SentimentGetterwithTextBlob: Given Language '{}' is not supported. Please use one of the following languages: '{}'. ".format(self._language, Corpus.supported_languages_sentiment_analyzer))
            return False










    def _check_db_should_be_an_corpus(self):
        if self.corpdb.typ() != "corpus":
            self.logger.error("No active DB was found. You need to connect or initialize a DB first, before you can make any operation on the DB.", exc_info=self._logger_traceback)
            return False
        else:
            return True




    def _isrighttype(self, inp_data):
        #p(inp_data)
        check = (isinstance(inp_data, list), isinstance(inp_data, LenGen))
        #p(check, "check")
        if True not in check:
            self.logger.error("InputValidationError: Given 'inpdata' is not iterable. ", exc_info=self._logger_traceback)
            return False
        return True


    def _check_db_should_exist(self):
        if not self.corpdb: 
            self.logger.error("No active DB was found. You need to connect or initialize a DB first, before you can make any operation on the DB.", exc_info=self._logger_traceback)
            return False
        else:
            return True




    def _check_db_should_not_exist(self):
        if self.corpdb: 
            self.logger.error("An active DB was found. You need to initialize new empty Instance of DB before you can do this operation.", exc_info=self._logger_traceback)
            return False
        else:
            return True


    def check_status_gateways(self):
        status= []
        try:
            for gw in self.opened_gateways:
                status.append(gw.remote_status())
        except Exception,e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("GateWaysStatusCheckerError: Throw following Exception '{}'.".format(e), exc_info=self._logger_traceback)
        
        self.logger.info("GateWaysStatusChecker: '{}'-Gateways was asked for their status..".format(len(status)))
        return status


    def close_all_gateways(self):
        closed=0
        try:
            for gw in self.opened_gateways:
                gw.exit()
                closed +=1
        except Exception,e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("GateWaysCloserError: Throw following Exception '{}'.".format(e), exc_info=self._logger_traceback)
        
        self.logger.info("GateWaysCloser: '{}'-Gateways was closed.".format(closed))


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


