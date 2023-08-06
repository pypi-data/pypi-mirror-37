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


import os
import sys
from raven import Client
import types
import Queue
import enlighten
import json
from collections import defaultdict,Counter,OrderedDict
import copy
import threading
import time
from itertools import izip
import re
import Stemmer



from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, path_to_zas_rep_tools, Rle, categorize_token_list, get_categories, instance_info, SharedCounterExtern, SharedCounterIntern, Status,function_name,statusesTstring, ngrams,nextLowest, get_number_of_streams_adjust_cpu,LenGen,DefaultOrderedDict, from_ISO639_2, to_ISO639_2,MyThread
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.classes.exporter import Exporter
from zas_rep_tools.src.utils.zaslogger import ZASLogger
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus
from zas_rep_tools.src.classes.basecontent import BaseContent, BaseDB
import  zas_rep_tools.src.utils.db_helper as db_helper
from zas_rep_tools.src.utils.custom_exceptions import  ZASCursorError, ZASConnectionError,DBHandlerError,ProcessError,ErrorInsertion,ThreadsCrash
#from sortedcontainers import SortedDict


import platform
if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama


class Stats(BaseContent,BaseDB):

    phenomena_table_map = {
                "repl":"replications",
                "redu":"reduplications",
                "baseline":"baseline",
                }


    supported_rep_type = set(("repl", "redu"))
    supported_phanomena_to_export = supported_rep_type.union(set(("baseline",)))
    supported_syntagma_type= set(("lexem", "pos"))
    supported_sentiment = set(("negative","positive","neutral"))
    output_tables_types = set(("sum", "exhausted"))
    output_tables_col_names = {
                            "baseline":{
                                    "all":"occur_syntagma_all",
                                    "repl":{
                                            "uniq":"occur_repl_uniq",
                                            "exhausted":"occur_repl_exhausted",
                                            },
                                    "redu":{
                                            "uniq":"occur_redu_uniq",
                                            "exhausted":"occur_redu_exhausted",
                                            }
                                
                                      }
                                   }

    min_col = {
                "repl":('id','doc_id', "redufree_len",'index_in_corpus','index_in_redufree','normalized_word', 'stemmed',"in_redu"),
                "redu":('id','doc_id', "redufree_len",'index_in_corpus', 'index_in_redufree',"redu_length",'normalized_word','stemmed'),
                "baseline":["syntagma", "occur_syntagma_all", "scope",'stemmed'],
            }


    _non_pos_tags = set(["EMOIMG", "EMOASC", "number", "symbol", "hashtag", "mention","regular"])
    header_order_to_export = ("baseline", "document", "word", "repl", "redu", "context")

    def __init__(self, status_bar=True,log_ignored=True,**kwargs):
        super(type(self), self).__init__(**kwargs)


        #Input: Encapsulation:

        
        
        self._status_bar = status_bar
        self._log_ignored= log_ignored
        #self._preprocession = preprocession
        self.locker = threading.Lock()


        #InstanceAttributes: Initialization
        self.statsdb = False
        self.corp = False
        self._corp_info = False
        self.corpdb_defaultname = "corpus"
        self.attached_corpdb_name = False
        self._doc_id_tag =  db_helper.doc_id_tag
        #self._baseline_delimiter = baseline_delimiter

        #self._init_compution_variables()

        self.preprocessors = defaultdict(dict)
        self._init_preprocessors(thread_name="Thread0")

        self.logger.debug('Intern InstanceAttributes was initialized')


        self.logger.debug('An instance of Stats() was created ')

        ## Log Settings of the Instance
        attr_to_flag = False
        attr_to_len = False
        self._log_settings(attr_to_flag =attr_to_flag,attr_to_len =attr_to_len)




        ############################################################
        ####################__init__end#############################
        ############################################################

    def __del__(self):
        super(type(self), self).__del__()



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

    def _init_compution_variables(self):
        self.threads_error_bucket = Queue.Queue()
        self.threads_status_bucket = Queue.Queue()
        self.threads_success_exit = []
        self.threads_unsuccess_exit = []
        self._threads_num = 0
        self.status_bars_manager =  self._get_status_bars_manager()
        self.preprocessors = defaultdict(dict)
        #self.baseline_replication = defaultdict(lambda:defaultdict(lambda: 0) )
        #self.baseline_reduplication = defaultdict(lambda:defaultdict(lambda: 0) )
        self._terminated = False
        #self.baseline_ngramm_lenght = self._context_left + 1 +self._context_lenght
        self.temporized_baseline = defaultdict(int)
        self.active_threads = []
        self.main_status_bar_of_insertions = False
        self._timer_on_main_status_bar_was_reset = False
        self._start_time_of_the_last_insertion = False
        self._end_time_of_the_last_insertion = False
        self._last_insertion_was_successfull = False
        self.counters_attrs = defaultdict(lambda:defaultdict(dict))
        #self._avaliable_scope = self._context_lenght+1
        self.force_cleaning_flags = set()
        self.ignored_pos = set(["URL", "U"])
        self.baseline_insrt_process = False

        self._text_field_name = "text"
        self._id_field_name =  "id"

        self.temporized_repl = defaultdict(list)
        self.temporized_redu = defaultdict(list)
        self._repls_cols = self.statsdb.col("replications")
        self._redus_cols = self.statsdb.col("reduplications")
        
        self._cleaned_tags = {
                                "number":":number:",
                                "URL":":URL:",
                                "symbol":":symbol:",
                                "mention":":mention:",
                                "hashtag":":hashtag:",
                            }



    ###########################INITS + Open##########################




    def _init_column_index_variables(self):
        self.col_index_orig = {
            "repl":{colname:index for index,colname in  enumerate(self.statsdb.col("replications") )},
            "redu":{colname:index for index,colname in  enumerate(self.statsdb.col("reduplications") )},
            "baseline":{colname:index for index,colname in  enumerate(self.statsdb.col("baseline") )},
            }

        self.col_index_min = {
            "repl":{colname:index for index,colname in  enumerate(Stats.min_col["repl"])},
            "redu":{colname:index for index,colname in  enumerate(Stats.min_col["redu"])},
            "baseline":{colname:index for index,colname in  enumerate(Stats.min_col["baseline"] )},
            #"baseline":{colname:index for index,colname in  enumerate(self.statsdb.col("baseline") )},
            }


        # self.col_index_repl = {colname:index for index,colname in  enumerate(self.statsdb.col("replications") )}
        # self.col_index_redu = {colname:index for index,colname in  enumerate(self.statsdb.col("reduplications") )}
        # self.col_index_baseline = {colname:index for index,colname in  enumerate(self.statsdb.col("baseline") )}


        # self._contextR1index = {
        #         "repl":self._get_col_index("contextR1", "replications"),
        #         "redu":self._get_col_index("contextR1", "reduplications")
        #         }
        # self._normalized_word_index = {
        #         "repl":self._get_col_index("normalized_word", "replications"),
        #         "redu":self._get_col_index("normalized_word", "reduplications")
        #         }
        # self._doc_id_index = {
        #         "repl":self._get_col_index("doc_id", "replications"),
        #         "redu":self._get_col_index("doc_id", "reduplications")
        #         }
        # self._adress_index = {
        #         "repl":self._get_col_index("token_index", "replications"),
        #         "redu":self._get_col_index("start_index", "reduplications")
        #         }
        # self._rep_id = {
        #         "repl":self._get_col_index("repl_id", "replications"),
        #         "redu":self._get_col_index("redu_id", "reduplications")
        #        }




    def additional_attr(self, repl_up,ignore_hashtag,ignore_url,
                        ignore_mention,ignore_punkt,ignore_num,force_cleaning,
                        case_sensitiv,full_repetativ_syntagma,
                        min_scope_for_indexes,baseline_delimiter):
        additional_attributes = {
                "repl_up":repl_up,
                #"log_ignored":log_ignored,
                "ignore_hashtag":ignore_hashtag,
                "ignore_url":ignore_url,
                "ignore_mention":ignore_mention,
                "ignore_punkt":ignore_punkt,
                "ignore_num":ignore_num,
                "force_cleaning":force_cleaning ,
                "case_sensitiv":case_sensitiv,
                "full_repetativ_syntagma":full_repetativ_syntagma,
                "full_repetativ_syntagma": full_repetativ_syntagma,
                "min_scope_for_indexes":min_scope_for_indexes,
                "baseline_delimiter":baseline_delimiter,
                }
        return additional_attributes






    def init(self, prjFolder, DBname, language,  visibility, corpus_id=None, 
                    encryption_key=False,fileName=False,  version=False, stats_id=False,
                    context_lenght=5, full_repetativ_syntagma=False, min_scope_for_indexes=2,
                    repl_up=3, ignore_hashtag=False, force_cleaning=False,baseline_delimiter="|+|",
                    case_sensitiv=False,ignore_url=False,  ignore_mention=False, ignore_punkt=False, ignore_num=False):

        if self.statsdb:
            self.logger.error("StatsInitError: An active Stats Instance was found. Please close already initialized/opened Stats, before new initialization.", exc_info=self._logger_traceback)
            return False
         
        if context_lenght < 3:
            self.logger.error("Given Context-Length is lower as an allow minimum, which is 3.")
            return False

        self.statsdb = DBHandler( **self._init_attributesfor_dbhandler())
        was_initialized = self.statsdb.init("stats", prjFolder, DBname, language,  visibility, corpus_id=corpus_id,
                    encryption_key=encryption_key,fileName=fileName, version=version,
                    stats_id=stats_id, db_frozen=False, context_lenght=context_lenght )

        if not was_initialized:
            self.logger.error("StatsInit: Current Stats for following attributes  wasn't initialized: 'dbtype='{}'; 'dbname'='{}; corp_id='{}'; 'stats_id'='{}'; encryption_key='{}'; .".format("stats", DBname,corpus_id, stats_id,encryption_key))
            return False

        if self.statsdb.exist():
            self.add_context_columns( context_lenght)
            additional_attributes = self.additional_attr(repl_up,ignore_hashtag,ignore_url,
                        ignore_mention,ignore_punkt,ignore_num,force_cleaning,
                        case_sensitiv,full_repetativ_syntagma,min_scope_for_indexes,baseline_delimiter)
            self.statsdb.update_attrs(additional_attributes)
            self.statsdb.update_attr("locked", False) 
            self.set_all_intern_attributes_from_db()
            self.logger.settings("InitStatsDBAttributes: {}".format( instance_info(self.statsdb.get_all_attr(), attr_to_len=False, attr_to_flag=False, as_str=True)))
            self.logger.debug("StatsInit: '{}'-Stats was successful initialized.".format(DBname))
            self._init_column_index_variables()
            self.baseline_ngramm_lenght =  1 +self._context_lenght
            return True
        else:
            self.logger.error("StatsInit: '{}'-Stats wasn't  initialized.".format(DBname), exc_info=self._logger_traceback)
            return False

    def close(self):
        self.statsdb.close()
        self.statsdb = False
        self.corp = False
        self._corp_info = False
        self.attached_corpdb_name = False

    def _close(self):
        self.statsdb._close()
        self.statsdb = False
        self.corp = False
        self._corp_info = False
        self.attached_corpdb_name = False

    def open(self, path_to_stats_db, encryption_key=False):

        if self.statsdb:
            self.logger.error("StatsInitError: An active Stats Instance was found. Please close already initialized/opened Stats, before new initialization.", exc_info=self._logger_traceback)
            return False

        self.statsdb = DBHandler( **self._init_attributesfor_dbhandler())
        self.statsdb.connect(path_to_stats_db, encryption_key=encryption_key)


        if self.statsdb.exist():
            if self.statsdb.typ() != "stats":
                self.logger.error("Current DB is not an StatsDB.")
                self._close()
                return False
            self.logger.debug("StatsOpener: '{}'-Stats was successful opened.".format(os.path.basename(path_to_stats_db)))
            self.set_all_intern_attributes_from_db()
            self.logger.settings("OpenedStatsDBAttributes: {}".format( instance_info(self.statsdb.get_all_attr(), attr_to_len=False, attr_to_flag=False, as_str=True)))
            self._init_column_index_variables()
            self.baseline_ngramm_lenght =  1 +self._context_lenght
            self._init_stemmer(self._language)
            return True
        else:
            self.logger.error("StatsOpener: Unfortunately '{}'-Stats wasn't opened.".format(os.path.basename(path_to_stats_db)), exc_info=self._logger_traceback)
            return False


    def set_all_intern_attributes_from_db(self):
        #{u'name': u'bloggerCorpus', u'created_at': u'2018-07-26 17:49:11', u'visibility': u'extern', u'version': u'1', u'corpus_id': 7614, u'typ': u'stats', u'id': 3497}
        info_dict = self.info()
        self._name = info_dict["name"]
        self._created_at = info_dict["created_at"]
        self._visibility = info_dict["visibility"]
        self._version = info_dict["version"]
        self._corpus_id = info_dict["corpus_id"]
        self._typ = info_dict["typ"]
        self._id = info_dict["id"]
        self._db_frozen = info_dict["db_frozen"]
        self._context_lenght = info_dict["context_lenght"]
        self._language = info_dict["language"]
        #self._context_lenght = info_dict["context_right"]
        self._avaliable_scope = self._context_lenght+1
        self._repl_up =  info_dict["repl_up"]
        #self._log_ignored =  info_dict["log_ignored"]
        self._ignore_hashtag =  info_dict["ignore_hashtag"]
        self._ignore_url =  info_dict["ignore_url"]
        self._ignore_mention =  info_dict["ignore_mention"]
        self._ignore_punkt =  info_dict["ignore_punkt"]
        self._ignore_num =  info_dict["ignore_num"]
        self._force_cleaning  =  info_dict["force_cleaning"]
        self._case_sensitiv =  info_dict["case_sensitiv"]
        self._full_repetativ_syntagma = info_dict["full_repetativ_syntagma"]
        # self._text_field_name = info_dict["text_field_name"]
        # self._id_field_name =  info_dict["id_field_name"]
        self._min_scope_for_indexes = info_dict["min_scope_for_indexes"]
        self._pos_tagger = info_dict["pos_tagger"]
        self._sentiment_analyzer = info_dict["sentiment_analyzer"]
        self._baseline_delimiter = info_dict["baseline_delimiter"]
        #self._id_field_name = None
        #self._text_field_name = None


    def _get_col_index(self, col_name, table_name):
        try:
            return self.statsdb.col(table_name).index(col_name)
        except ValueError, e:
            self.logger.error("'{}'-Colum is not in the '{}'-Table.".fromat(col_name, table_name))
            return False

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
                        "save_settings": self._save_settings, 
                        "save_status": self._save_status,
                        "log_content": self._log_content,
                        "clear_logger": self._clear_logger,
                        #_replace_double_items
                        }
        return init_attributes_db_handler



    
    def _init_stemmer(self, language):
        if language not in Corpus.stemmer_for_languages:
            self.logger.error("StemmerINIT: is failed. '{}'-language is not supported.")
            return False
        lan = from_ISO639_2[language]
        self.stemmer = Stemmer.Stemmer(lan)
        return True

    def stemm(self, word):
        #p(word, "word")
        try:
            word.decode
            return self.stemmer.stemWord(word)
        except:
            return self.stemmer.stemWord(word[0])
    
    def add_context_columns(self, context_lenght):
       self._add_context_columns("replications", context_lenght)
       self._add_context_columns("reduplications", context_lenght)

    def _add_context_columns(self, table_name, context_lenght):
        #p("ghjkl")
        exist_columns = self.statsdb.col(table_name)
        #p(exist_columns,"exist_columns", c="r")

        ## context left
        for context_number in reversed(range(1,context_lenght+1)):

            ### WordCell####
            name = "contextL{}".format(context_number)
            exist_columns = self.statsdb.col(table_name)
            if name not in exist_columns:
                if self.statsdb.add_col(table_name, name, "JSON"):
                    self.logger.debug("'{}'-Columns was inserted into '{}'-Table. ".format(name, table_name))
                else:
                    return False
            else:
                self.logger.error("'{}'-Column is already exist in the '{}'-Table. ColumnInsertion was aborted. ".format(name, table_name))
                #yield False
                return False

            ### Additional Info Col ####
            name = "context_infoL{}".format(context_number)
            exist_columns = self.statsdb.col(table_name)
            if name not in exist_columns:
                if self.statsdb.add_col(table_name, name, "JSON"):
                    self.logger.debug("'{}'-Columns was inserted into '{}'-Table. ".format(name, table_name))
                else:
                    return False
            else:
                self.logger.error("'{}'-Column is already exist in the '{}'-Table. ColumnInsertion was aborted. ".format(name, table_name))
                #yield False
                return False

        # context right
        for context_number in range(1,context_lenght+1):
            ### WordCell####
            name = "contextR{}".format(context_number)
            if name not in exist_columns:
                self.statsdb.add_col(table_name, name, "JSON")
                self.logger.debug("'{}'-Columns was inserted into '{}'-Table. ".format(name, table_name))
                #yield True
            else:
                self.logger.error("'{}'-Column is already exist in the '{}'-Table. ColumnInsertion was aborted. ".format(name, table_name))
                return  False
                #return 


            ### Additional Info Col ####
            name = "context_infoR{}".format(context_number)
            if name not in exist_columns:
                self.statsdb.add_col(table_name, name, "JSON")
                self.logger.debug("'{}'-Columns was inserted into '{}'-Table. ".format(name, table_name))
                #yield True
            else:
                self.logger.error("'{}'-Column is already exist in the '{}'-Table. ColumnInsertion was aborted. ".format(name, table_name))
                return  False
                #return 
        exist_columns = self.statsdb.col(table_name)
        #p(exist_columns,"exist_columns", c="r")
        return True
        #sys.exit()




    def info(self):
        if not self._check_stats_db_should_exist():
            return False

        if not self._check_db_should_be_an_stats():
            return False

        return self.statsdb.get_all_attr()



    # def get_streams_from_corpus(self,inp_corp,stream_number,datatyp="dict"):
    #     row_num = inp_corp.corpdb.rownum("documents")
    #     rows_pro_stream = row_num/stream_number
    #     streams = []
    #     num_of_getted_items = 0
    #     for i in range(stream_number):
    #         thread_name = "Thread{}".format(i)
    #         if i < (stream_number-1): # for gens in between 
    #             gen = inp_corp.corpdb.lazyget("documents",limit=rows_pro_stream, offset=num_of_getted_items,thread_name=thread_name, output=datatyp)
    #             num_of_getted_items += rows_pro_stream
    #             streams.append((thread_name,LenGen(gen, rows_pro_stream)))
    #         else: # for the last generator
    #             gen = inp_corp.corpdb.lazyget("documents",limit=-1, offset=num_of_getted_items,thread_name=thread_name, output=datatyp)
    #             streams.append((thread_name,LenGen(gen, row_num-num_of_getted_items)))
    #     return streams


    def get_streams_from_corpus(self,inp_corp,stream_number,datatyp="dict", size_to_fetch=1000):
        row_num = inp_corp.corpdb.rownum("documents")
        rows_pro_stream = row_num/stream_number
        streams = []
        num_of_getted_items = 0
        #p((self._id_field_name, self._text_field_name))
        def intern_gen(limit, offset):
            #p((limit, offset))
            query = u'SELECT {}, {}  FROM  main.documents  LIMIT {} OFFSET {};'.format(self._id_field_name, self._text_field_name,limit,  offset) 
            cur = inp_corp.corpdb._threads_cursors[thread_name].execute(query)
            while True:
                res = list(cur.fetchmany(size_to_fetch))
                if not res:
                    break
                for row in  res:
                    #yield {self._id_field_name:row[0], self._text_field_name:row[1]}
                    yield row
        #p(num_of_getted_items,"num_of_getted_items")
        for i in range(stream_number):
            thread_name = "Thread{}".format(i)
            if i < (stream_number-1): # for gens in between     
                #gen = inp_corp.corpdb.lazyget("documents",limit=rows_pro_stream, offset=num_of_getted_items,thread_name=thread_name, output=datatyp)
                #gen = inp_corp.corpdb.lazyget("documents",limit=rows_pro_stream, offset=num_of_getted_items,thread_name=thread_name, output=datatyp)
                
                
                #p((rows_pro_stream, num_of_getted_items))
                streams.append((thread_name,LenGen(intern_gen(rows_pro_stream, num_of_getted_items), rows_pro_stream)))
                num_of_getted_items += rows_pro_stream
                #print num_of_getted_items, rows_pro_stream
            else: # for the last generator
                #gen = inp_corp.corpdb.lazyget("documents",limit=-1, offset=num_of_getted_items,thread_name=thread_name, output=datatyp)
                #p((-1, num_of_getted_items))
                streams.append((thread_name,LenGen(intern_gen(-1, num_of_getted_items), row_num-num_of_getted_items)))
                num_of_getted_items += rows_pro_stream
        
        return streams


# query = u'SELECT {}, {}  FROM  main.documents  LIMIT {} OFFSET {};'.format(self._id_field_name, self._text_field_name,rows_pro_stream, num_of_getted_items) 

#                     while True:
#                         #p(cursor, "cursor")
#                         results = cursor["out_obj"].fetchmany(size_to_fetch)
#                         #p(results, "results")
#                         results = list(results)
#                         #p(results, "results")
#                         if not results:
#                             break
#                         for row in results:
#                             #p(row,"row")
#                             yield row





    def _get_export_phanomena(self,repl=False, redu=False, baseline=False):
        to_export = []
        if repl:
            to_export.append("repl")
        if redu:
            to_export.append("redu")
        if baseline:
            to_export.append("baseline")
        return to_export




    def _get_exporter_flags(self,repl=False, redu=False, baseline=False):
        flags = []

        if redu: 
            flags.append(True)

        if repl: 
            flags.append(True)

        if baseline:
            flags.append(True)

        return flags



                
    
    # def _get_header(self, flags, repl=False, redu=False, baseline=False, output_table_type="exhausted", embedded_baseline=True, max_scope=False, additional_doc_cols=False):
    #     header_main = []
    #     header_additional = []
    #     baseline_col_names = Stats.output_tables_col_names["baseline"]
    #     extracted_colnames_for_repl = [item[0] for item in db_helper.default_tables["stats"]["replications"]]
    #     extracted_colnames_for_redu = [item[0] for item in db_helper.default_tables["stats"]["reduplications"]]
    #     baseline_col_names_repl = [baseline_col_names["all"],baseline_col_names["repl"]["uniq"],baseline_col_names["repl"]["exhausted"]]
    #     baseline_col_names_redu = [baseline_col_names["all"],baseline_col_names["redu"]["uniq"],baseline_col_names["redu"]["exhausted"]]

    #     #db_helper.get
    #     if max_scope and max_scope >1:
    #         header_main.append("syntagma")
    #         header_additional.append("syntagma")


    #     if len(flags) == 1:
    #         if repl:
    #             header_main = [item[0] for item in db_helper.default_tables["stats"]["replications"]]
    #         elif redu:
    #             header_main = [item[0] for item in db_helper.default_tables["stats"]["reduplications"]]
    #         elif baseline:
    #             header_main = [item[0] for item in db_helper.default_tables["stats"]["baseline"]]

    #     elif len(flags) == 2:
    #         if output_table_type == "sum":
    #             pass

    #         else:
    #             if repl and baseline:
    #                 if embedded_baseline:
    #                     #header_main.append(db_helper.tag_normalized_word)
    #                     #extracted_colnames_for_repl.remove(db_helper.tag_normalized_word)
    #                     extracted_colnames_for_repl.remove(db_helper.tag_normalized_word)
    #                     header_main.append(db_helper.tag_normalized_word)
    #                     header_main += baseline_col_names_repl
    #                     header_main += extracted_colnames_for_repl
                        
    #                 else:
    #                     header_main += extracted_colnames_for_repl
    #                     baseline_col_names_repl.insert(0,db_helper.tag_normalized_word)
    #                     header_additional += baseline_col_names_repl


    #             elif redu and baseline:
    #                 if embedded_baseline:
    #                     #header_main.append(db_helper.tag_normalized_word)
    #                     extracted_colnames_for_redu.remove(db_helper.tag_normalized_word)
    #                     header_main.append(db_helper.tag_normalized_word)
    #                     header_main += baseline_col_names_redu
    #                     header_main += extracted_colnames_for_redu
                        
    #                 else:
    #                     header_main += extracted_colnames_for_redu
    #                     baseline_col_names_redu.insert(0,db_helper.tag_normalized_word)
    #                     header_additional += baseline_col_names_redu


    #             elif redu and repl: 
    #                 extracted_colnames_for_repl.remove(db_helper.tag_normalized_word)
    #                 extracted_colnames_for_redu.remove(db_helper.tag_normalized_word)
    #                 #header_main.append(db_helper.tag_normalized_word)
    #                 header_main.append(db_helper.tag_normalized_word)
    #                 #if embedded_baseline:
    #                 #header_main.append(db_helper.tag_normalized_word)
    #                 uniq_for_redu = [item for item in extracted_colnames_for_redu if item not in extracted_colnames_for_repl]
    #                 header_main += extracted_colnames_for_repl+uniq_for_redu
                        


    #     elif len(flags) == 3:
    #         if embedded_baseline:
    #             extracted_colnames_for_repl.remove(db_helper.tag_normalized_word)
    #             extracted_colnames_for_redu.remove(db_helper.tag_normalized_word)
    #             header_main.append(db_helper.tag_normalized_word)
    #             header_additional.append(db_helper.tag_normalized_word)
    #             header_additional += baseline_col_names_repl
    #             baseline_col_names_redu.remove(baseline_col_names["all"])
    #             header_additional += baseline_col_names_redu
    #             header_main += extracted_colnames_for_repl
    #             uniq_for_redu = [item for item in extracted_colnames_for_redu if item not in extracted_colnames_for_repl]
    #             header_main += uniq_for_redu

    #         else:
    #             extracted_colnames_for_repl.remove(db_helper.tag_normalized_word)
    #             extracted_colnames_for_redu.remove(db_helper.tag_normalized_word)
    #             header_main.append(db_helper.tag_normalized_word)
    #             header_main += baseline_col_names_repl
    #             baseline_col_names_redu.remove(baseline_col_names["all"])
    #             header_main += baseline_col_names_redu
    #             header_main += extracted_colnames_for_repl
    #             uniq_for_redu = [item for item in extracted_colnames_for_redu if item not in extracted_colnames_for_repl]
    #             header_main += uniq_for_redu




    #         #self.logger.error("Simultan Export for 3 Phenomena at the same time is not implemented.")


    #     if len(header_additional)==1:
    #         header_additional = []
            

    #     if header_main and header_additional:
    #         return header_main, header_additional
    #     elif header_main:
    #         return header_main




    def _add_context_columns(self, table_name, context_lenght):
        #p("ghjkl")
        exist_columns = self.statsdb.col(table_name)
        #p(exist_columns,"exist_columns", c="r")

        ## context left
        for context_number in reversed(range(1,context_lenght+1)):

            ### WordCell####
            name = "contextL{}".format(context_number)
            exist_columns = self.statsdb.col(table_name)
            if name not in exist_columns:
                if self.statsdb.add_col(table_name, name, "JSON"):
                    self.logger.debug("'{}'-Columns was inserted into '{}'-Table. ".format(name, table_name))
                else:
                    return False
            else:
                self.logger.error("'{}'-Column is already exist in the '{}'-Table. ColumnInsertion was aborted. ".format(name, table_name))
                #yield False
                return False

            ### Additional Info Col ####
            name = "context_infoL{}".format(context_number)
            exist_columns = self.statsdb.col(table_name)
            if name not in exist_columns:
                if self.statsdb.add_col(table_name, name, "JSON"):
                    self.logger.debug("'{}'-Columns was inserted into '{}'-Table. ".format(name, table_name))
                else:
                    return False
            else:
                self.logger.error("'{}'-Column is already exist in the '{}'-Table. ColumnInsertion was aborted. ".format(name, table_name))
                #yield False
                return False

        # context right
        for context_number in range(1,context_lenght+1):
            ### WordCell####
            name = "contextR{}".format(context_number)
            if name not in exist_columns:
                self.statsdb.add_col(table_name, name, "JSON")
                self.logger.debug("'{}'-Columns was inserted into '{}'-Table. ".format(name, table_name))
                #yield True
            else:
                self.logger.error("'{}'-Column is already exist in the '{}'-Table. ColumnInsertion was aborted. ".format(name, table_name))
                return  False
                #return 


            ### Additional Info Col ####
            name = "context_infoR{}".format(context_number)
            if name not in exist_columns:
                self.statsdb.add_col(table_name, name, "JSON")
                self.logger.debug("'{}'-Columns was inserted into '{}'-Table. ".format(name, table_name))
                #yield True
            else:
                self.logger.error("'{}'-Column is already exist in the '{}'-Table. ColumnInsertion was aborted. ".format(name, table_name))
                return  False
                #return 
        exist_columns = self.statsdb.col(table_name)
        #p(exist_columns,"exist_columns", c="r")
        return True
        #sys.exit()


    def attached_corpdb_number(self):
        if not self._check_stats_db_should_exist():
            return False
        
        return len(self.statsdb.dbnames)-1
    
    def attach_corpdb(self, path_to_corpdb, encryption_key=False):
        if not self._check_stats_db_should_exist():
            return False
        

        #p(path_to_corpdb, "path_to_corpdb")
        if not self.statsdb.attach(path_to_corpdb, encryption_key=encryption_key, db_name=self.corpdb_defaultname)["status"]:
            self.logger.error("'{}' wasn't attached.".format(path_to_corpdb))
            return False


        id_from_attached_corp = self.statsdb.get_attr("id",dbname=self.corpdb_defaultname)
        corp_id = self.statsdb.get_attr("corpus_id",dbname="main")
        #p(())
        if id_from_attached_corp != corp_id:
            self.logger.error("Attached CorpDB (id='{}') is not suitable with the current StatsDB. Current StatsDB is suitable with CorpDB with id='{}'.".format(id_from_attached_corp, corp_id))
            self.statsdb.detach(dbname=self.corpdb_defaultname)
            return False


        self.attached_corpdb_name = self.corpdb_defaultname
        return True


    def _get_context_cols(self, direction, context_lenght):
        output = ()

        if direction == "left":
            for context_number in reversed(range(1,context_lenght+1)):

                ### WordCell####
                output +=  ("contextL{}".format(context_number),)
                ### Additional Info Col ####
                output += ("context_infoL{}".format(context_number),)

        else:
            # context right
            for context_number in range(1,context_lenght+1):
                ### WordCell####
                output +=  ("contextR{}".format(context_number),)
                ### Additional Info Col ####
                output += ("context_infoR{}".format(context_number),) 

        return output      
                
    
    def _get_header(self,  repl=False, redu=False, baseline=False, output_table_type="exhausted",  max_scope=False, additional_doc_cols=False, context_len_left=True, context_len_right=True,word_examples_sum_table=True):
        if not self._check_stats_db_should_exist():
            return False
        if output_table_type == "exhausted":
            return self._get_header_exhausted( repl=repl, redu=redu, baseline=baseline, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right)
        else:
            return self._get_header_sum(repl=repl, redu=redu,word_examples_sum_table=word_examples_sum_table)


    def _get_header_sum(self, repl=False, redu=False, word_examples_sum_table=True):
        if repl and redu:
            self.logger.error("GetSummeryHeaderError: Repl and Redu was selected in the same time. Summery Header could be created just for one Phenomen each time.")
            return False

        output = False

        col_repls_core = ("letter", "NrOfRepl", "Occur")
        col_redus_core = ("word", "ReduLength", "Occur")
        if repl: 
            col_repls_core = col_repls_core+("Examples",)  if word_examples_sum_table else col_repls_core
            output =  col_repls_core

        if redu: 
            #col_redus_core = col_redus_core+("Examples",)  if word_examples_sum_table else col_redus_core
            output =  col_redus_core

        return output


    def _get_header_exhausted(self, repl=False, redu=False, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True):
        if (repl and not baseline) or (redu and not baseline):
            self.logger.error("Export is possible just with selected baseline. Please select also baseline to start the export process.")
            return False

        if baseline:
            baseline = ()
            baseline += db_helper.default_col_baseline_main
            baseline += db_helper.default_col_baseline_repls_core if repl else ()
            baseline += db_helper.default_col_baseline_redus_core if redu else ()
            baseline += db_helper.default_col_baseline_repls_addit if repl else ()
            baseline += db_helper.default_col_baseline_redus_addit if redu else ()
            baseline = tuple(item[0] for item in baseline)

        if repl: 
            repl = ()
            repl += db_helper.default_col_for_rep_core 
            repl += db_helper.default_col_for_rep_indexes
            repl += db_helper.default_col_for_rep_repl_data 
            repl = tuple(item[0] for item in repl)


        if redu: 
            redu = ()
            redu += db_helper.default_col_for_rep_core 
            redu += db_helper.default_col_for_rep_indexes
            redu += db_helper.default_col_for_rep_redu_data 
            redu = tuple(item[0] for item in redu)


        word = ()
        if repl and not redu:
            word += db_helper.default_col_for_repl_word_info
            word += db_helper.default_col_for_rep_addit_info_word
            
        elif not repl and  redu:
            word += db_helper.default_col_for_redu_word_info
            word += db_helper.default_col_for_rep_addit_info_word

        elif repl and redu:
            word += db_helper.default_col_for_repl_word_info
            word += db_helper.default_col_for_rep_addit_info_word
        word = tuple(item[0] for item in word) if word else ()


        document = ()
        context = ()
        if repl or redu:
            document += (tuple(item[0] for item in db_helper.default_col_for_rep_doc_info) ,)
            if additional_doc_cols:
                document += (tuple(additional_doc_cols),)
            else:
                document += (None,)

            ## context left
            #context += () 
            avalible_context_num_in_stats = self.statsdb.get_attr("context_lenght")
            if context_len_left:
                context_len_left = avalible_context_num_in_stats if context_len_left is True else context_len_left
                if context_len_left > avalible_context_num_in_stats:
                    self.logger.error("Given ContextLeft Number is higher as possible. Current StatsDB was computed for '{}'-context number. Please use one number, which are not higher as computed context number for current StatsDB.".format(context_len_left,avalible_context_num_in_stats))
                    return False
                context += self._get_context_cols("left", context_len_left)

            if context_len_right:
                context_len_right = avalible_context_num_in_stats if context_len_right is True else context_len_right
                if context_len_right > avalible_context_num_in_stats:
                    self.logger.error("Given ContextRight Number is higher as possible. Current StatsDB was computed for '{}'-context number. Please use one number, which are not higher as computed context number for current StatsDB.".format(context_len_right,avalible_context_num_in_stats))
                    return False
                context += self._get_context_cols("right", context_len_right)


        if not repl and not redu and not baseline:
            return {}
        else:
            return {"baseline":baseline, "document":document, "word":word, "repl":repl, "redu":redu,  "context":context}





    def cols_exists_in_corpb(self, cols_to_check):
        if not self._check_stats_db_should_exist():
            return False
        if not self.attached_corpdb_name:
            self.logger.error("'{}' wasn't attached.".format(path_to_corpdb))
            return False

        cols_in_doc_tables_in_attached_corp = self.statsdb.col("documents", dbname=self.attached_corpdb_name)

        for col in cols_to_check:
            if col not in cols_in_doc_tables_in_attached_corp:
                self.logger.error("'{}'-ColumnName wasn't found in CorpDB. Please use one of the following additional ColNames: '{}'.".format(col, cols_in_doc_tables_in_attached_corp))
                return False

        return True



    def order_header(self,header, additional_doc_cols,export_file_type):
        #p(header, "header")
        if export_file_type == "csv":
            wrapped_tag_pattern = "[{}]."
        else:
            wrapped_tag_pattern = "{}."
        ordered_header = []
        for table_part in  Stats.header_order_to_export:
            if table_part == "document":
                #p(header[table_part], "header[table_part]")
                try:
                    temp_list = list(header[table_part][0])
                except:
                    temp_list = []
                wrapped_tag = wrapped_tag_pattern.format(table_part)
                ordered_header += ["{}{}".format(wrapped_tag,col) for col in temp_list ]
                if additional_doc_cols:
                    if header[table_part][1]:
                        temp_list = list(header[table_part][1])
                        wrapped_tag = wrapped_tag_pattern.format(table_part)
                        ordered_header += ["{}{}".format(wrapped_tag,col) for col in temp_list ]
                #p(ordered_header, "ordered_header")
            else:
                if  header[table_part]:
                    for col in header[table_part]:
                        #p(col, "col " )
                        wrapped_tag = wrapped_tag_pattern.format(table_part)
                        ordered_header.append("{}{}".format(wrapped_tag,col))
        return ordered_header


    #Stats._non_pos_tags = set(["EMOIMG", "EMOASC", "number", "symbol", "hashtag", "mention","regular"])

    def export(self,path_to_export_dir, syntagma="*", repl=False, redu=False,
                baseline=True, syntagma_type="lexem", sentiment=False,
                fname=False, export_file_type="csv", rows_limit_in_file=1000000,
                encryption_key_corp=False, output_table_type="exhausted",
                additional_doc_cols=False, encryption_key_for_exported_db=False,
                path_to_corpdb=False, max_scope=False, stemmed_search=False,rewrite=False,
                context_len_left=True, context_len_right=True, separator_syn=" || ",
                word_examples_sum_table=True,ignore_num=False,ignore_symbol=False,):
        #p(locals())
        #p((path_to_export_dir,syntagma,repl,redu,syntagma_type,max_scope))
        export_file_type =  export_file_type.lower()
        fname =fname if fname else "export_{}".format(time.time())
        if self.statsdb.get_attr("locked"):
                self.logger.error("Current DB is still be locked. Possibly it is right now in-use from other process or the last computation-process is failed.")
                return False

        if export_file_type not in Exporter.supported_file_formats:
            self.logger.error("ExportError: '{}'-FileType is not supported. Please use one of the following file type: '{}'.".format(export_file_type, Exporter.supported_file_formats))
            return False
            
        if output_table_type not in Stats.output_tables_types:
            self.logger.error("Given Type for the outputTable ('{}') is not supported. Please select one of the following types: '{}'. ".format(output_table_type, Stats.output_tables_types))
            return False

        if sentiment:
            if not self._sentiment_analyzer:
                self.logger.error("GetterError: Sentiment wasn't computed for current CorpusDB thats why it is not possible to export Data with sentiment.")
                return False

        if syntagma_type == "pos":
            if not self._pos_tagger:
                if syntagma != "*":
                    try:
                        syntagma[0].decode
                        for word in syntagma:
                            if word not in Stats._non_pos_tags:
                                self.logger.error(u"POSGetterError: Additional POS-Tag was found in Syntagma. ('{}')  Current CorpusDB contain just default meta tags. ('{}') If you want to search in additional POS, than recompute CorpusDB with POS-Tagger.".format(word,Stats._non_pos_tags))
                                return False
                    except:
                        try:
                            syntagma[0][0].decode
                            for syn  in syntagma:
                                for word in syn:
                                    if word not in Stats._non_pos_tags:
                                        self.logger.error(u"POSGetterError: Additional POS-Tag was found in Syntagma. ('{}')  Current CorpusDB contain just default meta tags. ('{}') If you want to search in additional POS, than recompute CorpusDB with POS-Tagger.".format(word,Stats._non_pos_tags))
                                        return False
                        except:
                            self.logger.error("SyntagmaError: Given Syntagma has incorrect structure.")
                            return False



        #if repl and redu and baseline: 
        #    self.logger.critical("It is not possible to get repls and redus parallel. Please select one option at the same moment.")
        #    return False

        flags = self._get_exporter_flags(repl=repl, redu=redu, baseline=baseline)
        if len(flags) == 0:
            self.logger.error("No One Phenomena to Export was selected")
            return False

        if path_to_corpdb:
            if not self.attach_corpdb(path_to_corpdb):
                self.logger.debug("Given CorpDB '{}' either not exist or not suitable with the current StatsDB.".format(path_to_corpdb))
                return False
        if not path_to_corpdb and additional_doc_cols:
            self.logger.error("Additional Columns from CorpusDB was given, but the path to CorpDB wasn't given. Please give also the path to CorpDB.")
            return False

        if additional_doc_cols:
            if not self.cols_exists_in_corpb(additional_doc_cols):
                return False

        if output_table_type == "sum":
            reptype_sum_table = "repl" if repl else "redu"
        else:
            reptype_sum_table = False


        # p(locals())
        #p(max_scope, "max_scope")
        header = self._get_header( repl=repl, redu=redu, baseline=True, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        if not header:
            return False

        rows_generator = self._export_generator(header,inp_syntagma=syntagma, reptype_sum_table=reptype_sum_table,
                                                syntagma_type=syntagma_type, sentiment=sentiment, separator_syn=separator_syn,
                                                output_table_type=output_table_type,max_scope=max_scope,
                                                ignore_num=ignore_num,ignore_symbol=ignore_symbol,
                                                word_examples_sum_table=word_examples_sum_table,stemmed_search=stemmed_search)

        if not rows_generator:
            self.logger.error("RowGenerator is failed.")
            return False
        if output_table_type == "sum":
            ordered_header = header
        else:
            ordered_header = self.order_header(header, additional_doc_cols,export_file_type)
        #p(ordered_header, "ordered_header")
        def intern_gen():
            # p("111")
            for row in  rows_generator:
                # p("222")
                if row:
                    yield {k:v for k,v in  zip(ordered_header,row)}

        exporter = Exporter(intern_gen(),rewrite=rewrite,silent_ignore=False )
        if export_file_type == "csv":
            exporter.tocsv(path_to_export_dir, fname, ordered_header, rows_limit_in_file=rows_limit_in_file)

        elif export_file_type == "xml":
            exporter.toxml(path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file, root_elem_name="export", row_elem_name="line")
            
        #elif export_file_type == "sqlite":
        #    exporter.tosqlite(path_to_export_dir, fname, ordered_header,  encryption_key=encryption_key_for_exported_db, table_name="Export")

        elif export_file_type == "json":
            exporter.tojson(path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file,)

        else:
            self.logger.error("'{}'-FileType is not supported..".format(export_file_type))
            return False


    def _get_values_from_doc(self, doc_id, cols_to_get):
        if not self.attached_corpdb_name:
            self.logger.error("No One CorpDB was attached. To get additional Columns from corpus, you need attach the right CorpDB before.")
            return False
        #p((doc_id, cols_to_get), c="m")
        #p(self.statsdb.getall("documents", columns=cols_to_get, dbname=self.attached_corpdb_name, where="{}={}".format(self._doc_id_tag, doc_id)), c="r")
        return   self.statsdb.getone("documents", columns=cols_to_get, dbname=self.attached_corpdb_name, where="{}={}".format(self._doc_id_tag, doc_id))



    def _export_generator(self,header,inp_syntagma="*", syntagma_type="lexem", sentiment=False,
                            output_table_type="exhausted", reptype_sum_table=False, separator_syn=" || ",
                            thread_name="Thread0",ignore_num=False,ignore_symbol=False,
                            word_examples_sum_table=True,max_scope=False,stemmed_search=False):

        if not separator_syn:
            self.logger.error("No Separator for Syntagma was selected.")
            yield False
            return 

        # p((inp_syntagma, max_scope),c="r")
        #p(locals())
        def redu_constr(single_redu):
                temp_row = []
                for table_part in  Stats.header_order_to_export:
                    if table_part == "baseline":
                        temp_row += current_ordered_baseline_row
                        #p(temp_row, "temp_row")

                    elif table_part == "document":
                        #p(header["document"])
                        temp_row += [single_redu[ix_redu[col_name]] for col_name in header["document"][0]]
                        doc_id = single_redu[ix_doc_id_redu]
                        col_from_corp = header["document"][1]
                        #p(col_from_corp, "col_from_corp", c="g")
                        if col_from_corp:
                            values_from_corp = self._get_values_from_doc(doc_id, col_from_corp)
                            #p(values_from_corp, "values_from_corp")
                            if values_from_corp:
                                temp_row += list(values_from_corp)
                            else:
                                self.logger.error("No values from Corpus was returned")
                                yield False
                                return 

                    elif table_part == "word":
                        temp_row += [None if col_name == 'rle_word' else single_redu[ix_redu[col_name]] for col_name in header["word"]]

                    elif table_part == "repl":
                        temp_row += [None for col_name in header["repl"]]

                    elif table_part == "redu":
                        temp_row += [single_redu[ix_redu[col_name]] for col_name in header["redu"]]
                        #extracted_redus.append(single_redu[ix_redu_id])

                    elif table_part == "context":
                        temp_row += [single_redu[ix_redu[col_name]] for col_name in header["context"]]

                #exported_rows_count += 1
                #p(temp_row, "2121temp_row",c="m")
                #exported_rows_count += 1
                yield temp_row
                return





        # p("!99999")
        if output_table_type == "sum":
            if reptype_sum_table not in ("repl", "redu"):
                self.logger.error("Wrong RepType ('{}') was selected.".format(reptype_sum_table))
                yield False
                return 

            if self._status_bar:
                try:
                    if not self.status_bars_manager.enabled:
                        self.status_bars_manager = self._get_status_bars_manager()
                except:
                    self.status_bars_manager = self._get_status_bars_manager()

                status_bar_start = self._get_new_status_bar(None, self.status_bars_manager.term.center("Exporter (sum)") , "", counter_format=self.status_bars_manager.term.bold_white_on_green("{fill}{desc}{fill}"))
                status_bar_start.refresh()
                


            data = self.compute_rep_sum(inp_syntagma,  reptype_sum_table, syntagma_type=syntagma_type, sentiment=sentiment,
                                stemmed_search=stemmed_search, thread_name=thread_name, ignore_num=ignore_num,
                                ignore_symbol=ignore_symbol, word_examples_sum_table=word_examples_sum_table)

            #p(data, "data")
            exported_rows_count = 0
            if reptype_sum_table == "redu":
                tag =  "Words"
                if self._status_bar:
                    status_bar_current = self._get_new_status_bar(len(data), "Exporting:", "word")
                for word, word_data in  dict(sorted(data.items())).items():
                    if self._status_bar:
                        status_bar_current.update(incr=1)
                    for redu_length, occur in dict(sorted(word_data.items())).items():
                        exported_rows_count += 1
                        yield (word, redu_length,occur)
                    #pass
            else:
                tag = "Letters"
                if self._status_bar:
                    status_bar_current = self._get_new_status_bar(len(data), "Exporting:", "letter")
                for letter, letter_data in  dict(sorted(data.items())).items():
                    if self._status_bar:
                        status_bar_current.update(incr=1)
                    for NrOfRepl, repl_data in dict(sorted(letter_data.items())).items():
                        exported_rows_count += 1
                        occur = repl_data[0]
                        temp_row = (letter, NrOfRepl, occur)
                        if word_examples_sum_table:
                            examples = dict(repl_data[1])
                            temp_row += (examples, )
                        yield temp_row


            if self._status_bar:
                #i += 1
                #print status_bar_current.total, i
                #if status_bar_current.total != i:
                #   status_bar_current.total = i
                status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("Exported: {}:'{}'; Rows: '{}'; ".format(tag, status_bar_current.count,exported_rows_count) ), "",  counter_format=self.status_bars_manager.term.bold_white_on_green('{fill}{desc}{fill}\n'))
                status_bar_total_summary.refresh()
                self.status_bars_manager.stop()

        else:
            # p("!88888")
            if not header:
                self.logger.error("Header is empty. Please give non-empty header.")
                yield False
                return 
            try:
                repl = True if header["repl"] else False
                redu = True  if header["redu"] else False
                baseline = True if header["baseline"] else False
            except:
                self.logger.error("Header has wrong structure. Please give header with the right structure. Probably  was selected not correct 'output_table_type'.  ")
                yield False
                return 
            #p((header, repl, redu, baseline))
            #Stats.header_order_to_export

            # p("!7777")

            data =  self.get_data(inp_syntagma=inp_syntagma,repl=repl, redu=redu, baseline=baseline, syntagma_type=syntagma_type, 
                                sentiment=sentiment,thread_name=thread_name, max_scope=max_scope, stemmed_search=stemmed_search,send_empty_marker=True,
                                minimum_columns=False,order_output_by_syntagma_order=False, return_full_tuple=False,delete_duplicates=True,
                                get_columns_repl=False,get_columns_redu=False,get_columns_baseline=False,if_type_pos_return_lexem_syn=True)
            #p(len(data), "dd")
            # p((inp_syntagma, repl, redu,baseline, syntagma_type, sentiment, thread_name,max_scope, stemmed_search,), c="r")
            if not data:
                self.logger.error("Current Generator wasn't initialized. Because No Data was found in the current StatsDB for current settings. Please try to change the settings.")
                yield False
                return 

            if self._status_bar:
                try:
                    if not self.status_bars_manager.enabled:
                        self.status_bars_manager = self._get_status_bars_manager()
                except:
                    self.status_bars_manager = self._get_status_bars_manager()

                status_bar_start = self._get_new_status_bar(None, self.status_bars_manager.term.center("Exporter (exhausted)") , "", counter_format=self.status_bars_manager.term.bold_white_on_green("{fill}{desc}{fill}"))
                status_bar_start.refresh()
                status_bar_current_all = self._get_new_status_bar(self.statsdb.rownum("baseline"), "All:", "syntagma")
                #p(len(data), "dd")
                status_bar_current_right = self._get_new_status_bar(len(data), "Qualified:", "syntagma")
                status_bar_current_all.refresh()
                status_bar_current_right.refresh()
            # p("!666")
            ix_baseline = self.col_index_orig["baseline"]
            ix_repl = self.col_index_orig["repl"]
            ix_redu = self.col_index_orig["redu"]
            ix_repl_in_redu = ix_repl["in_redu"]
            ix_redu_in_redufree = ix_redu["index_in_redufree"]
            ix_doc_id_repl = ix_repl["doc_id"]
            ix_doc_id_redu = ix_redu["doc_id"]
            ix_redu_id = ix_redu["id"]
            i = 0
            exported_rows_count = 0
            # p("!555")
            # p(data, "data")
            count = 0
            for i, item in enumerate(data):
                if item == None:
                    count += 1
                # p((i,count))
                #p((i, item))
                # p(item, "item")
                if not item:
                    if self._status_bar:
                        status_bar_current_all.update(incr=1)
                    continue
                i += 1
                # p("!444")
                if self._status_bar:
                    status_bar_current_all.update(incr=1)
                    status_bar_current_right.update(incr=1)
                #if inp_syntagma == ["klitze, kleine"]:
                #   p(item, "item")
                #p(item , "item")
                #temp_rows = []
                #### Prepare Baseline
                vals_bas =  item["baseline"]
                if not vals_bas:
                    self.logger.error("'baseline'-Element is empty. (syntagma: '{}')".format(item["syntagma"]))
                    yield False
                    break
                    #ret
                #p(vals_bas, "vals_bas")
                #p(header["baseline"],'header["baseline"]')
                if len(vals_bas)> 1:
                    #p(vals_bas, "vals_bas")
                    self.logger.error( "Baseline Element has more as 1 item. If you searching in 'pos' and you got this error, please select 'if_type_pos_return_lexem_syn'-option to ensure right work. ")
                    yield False
                    return 

                vals_bas = vals_bas[0]
                
                #p(vals_bas,"vals_bas")
                #current_ordered_baseline_row = [ " || ".join(vals_bas[ix_baseline[col_name]]) if col_name in ["syntagma", "stemmed"] else vals_bas[ix_baseline[col_name]] for col_name in header["baseline"]]
                current_ordered_baseline_row = []
                for col_name in header["baseline"]:
                    if col_name == "syntagma":
                        current_ordered_baseline_row.append(separator_syn.join(vals_bas[ix_baseline[col_name]]))
                    elif col_name == "stemmed":
                        current_ordered_baseline_row.append(separator_syn.join(vals_bas[ix_baseline[col_name]].split(self._baseline_delimiter)))
                    else:
                        current_ordered_baseline_row.append(vals_bas[ix_baseline[col_name]])

                #p(current_ordered_baseline_row, "current_ordered_baseline_row")
                ### Prepare Other Data
                
                if repl:
                    
                    #temp_row = []
                    vals_repl =  item["repl"]
                    if not vals_repl:
                        if redu:
                            vals_redu =  item["redu"]
                            if vals_redu: # if just redus was found, but not repls for current syntagma, than extract just redus
                                for single_redu in vals_redu:
                                    exported_rows_count += 1
                                    yield tuple(redu_constr(single_redu))[0]
                        
                        #vals_redu_dict = {singl_redu[ix_doc_id_redu]:{} for singl_redu in vals_redu}

                        #return

                    if redu:
                        vals_redu =  item["redu"]
                        vals_redu_dict = defaultdict(lambda:defaultdict(None))
                        redu_ids = defaultdict(dict)
                        for singl_redu in vals_redu:
                            redu_doc_id = singl_redu[ix_doc_id_redu]
                            redu_index = singl_redu[ix_redu_in_redufree]

                            redu_ids[singl_redu[ix_redu_id]] = (singl_redu[ix_doc_id_redu], singl_redu[ix_redu_in_redufree])
                            vals_redu_dict[redu_doc_id][redu_index] = singl_redu
                        #vals_redu_dict = {singl_redu[ix_doc_id_redu]:{} for singl_redu in vals_redu}

                    #temp_data = []
                    extracted_redus= set()
                    for single_repl in vals_repl:
                        temp_row = []
                        #p(single_repl, "single_repl", c="r")
                        #for 
                        for table_part in  Stats.header_order_to_export:
                            if table_part == "baseline":
                                temp_row += current_ordered_baseline_row

                            elif table_part == "document":
                                #p(header["document"])
                                temp_row += [single_repl[ix_repl[col_name]] for col_name in header["document"][0]]
                                doc_id = single_repl[ix_doc_id_repl]
                                col_from_corp = header["document"][1]
                                #p(col_from_corp, "col_from_corp", c="g")
                                if col_from_corp:
                                    values_from_corp = self._get_values_from_doc(doc_id, col_from_corp)
                                    #p(values_from_corp, "values_from_corp")
                                    if values_from_corp:
                                        temp_row += list(values_from_corp)
                                    else:
                                        self.logger.error("No values from Corpus was returned")
                                        yield False
                                        return 

                            elif table_part == "word":
                                temp_row += [single_repl[ix_repl[col_name]] for col_name in header["word"]]

                            elif table_part == "repl":
                                temp_row += [single_repl[ix_repl[col_name]] for col_name in header["repl"]]


                            elif table_part == "redu":
                                if redu:
                                    in_redu = single_repl[ix_repl_in_redu]
                                    if in_redu:
                                        if not vals_redu:  # if wasn't found - than re-exctract with other flag
                                            current_syntagma = vals_bas[ix_baseline["syntagma"]]
                                            #p((in_redu,single_repl, vals_redu,current_syntagma))
                                            vals_redu = self._get_data_for_one_syntagma(current_syntagma,redu=True, repl=False, baseline=False,get_also_non_full_repetativ_result=True)["redu"]
                                            #p(vals_redu, "22vals_redu")
                                            vals_redu_dict = defaultdict(lambda:defaultdict(None))
                                            for singl_redu in vals_redu:
                                                vals_redu_dict[singl_redu[ix_doc_id_redu]][singl_redu[ix_redu_in_redufree]] = singl_redu 

                                        if not  vals_redu: 
                                            self.logger.error("ImplementationError: No redus was extracted for '{}'-syntagma. ".format(current_syntagma))  
                                            yield False
                                            return  


                                        repl_doc_id = single_repl[ix_doc_id_repl]
                                        #p((single_repl))
                                        #p(vals_redu_dict[repl_doc_id].keys(), "111redu_ixs")
                                        try:
                                            redu_for_current_repl = vals_redu_dict[repl_doc_id][in_redu]
                                        except KeyError:
                                            current_syntagma = vals_bas[ix_baseline["syntagma"]]
                                            #!!!!!!!p((in_redu,single_repl, vals_redu,current_syntagma))
                                            vals_redu = self._get_data_for_one_syntagma(current_syntagma,redu=True, repl=False, baseline=False,get_also_non_full_repetativ_result=True)["redu"]
                                            #p(vals_redu, "22vals_redu")
                                            vals_redu_dict = defaultdict(lambda:defaultdict(None))
                                            for singl_redu in vals_redu:
                                                vals_redu_dict[singl_redu[ix_doc_id_redu]][singl_redu[ix_redu_in_redufree]] = singl_redu 

                                            if not  vals_redu: 
                                                self.logger.error("ImplementationError: No redus was extracted for '{}'-syntagma. ".format(current_syntagma))  
                                                yield False
                                                return 

                                        #p((single_repl))
                                        #p(vals_redu_dict[repl_doc_id].keys(), "222redu_ixs")
                                        redu_for_current_repl = vals_redu_dict[repl_doc_id][in_redu]


                                        if not redu_for_current_repl: # if wasn't found - than re-exctract with other flag
                                            self.logger.error("DB-Inconsistence or ImplementationError: For Current Repl ('{}') in Redu ('{}') wasn't found any redu in the StatsDB.".format(single_repl, in_redu))   
                                            yield False
                                            return  

                                        temp_row += [redu_for_current_repl[ix_redu[col_name]] for col_name in header["redu"]]
                                        extracted_redus.add(redu_for_current_repl[ix_redu_id])

                                    else:
                                        temp_row += [None for col_name in header["redu"]]


                            elif table_part == "context":
                                temp_row += [single_repl[ix_repl[col_name]] for col_name in header["context"]]

                        exported_rows_count += 1
                        #p(temp_row, "temp_row")
                        yield temp_row

                    ## for redus, which still be not extracted
                    if redu:
                        for r_id, data in  redu_ids.items():
                            if r_id not in extracted_redus:
                                redu_to_extract = vals_redu_dict[data[0]][data[1]]
                                exported_rows_count += 1
                                #p(tuple(redu_constr(redu_to_extract))[0], c="r")
                                yield tuple(redu_constr(redu_to_extract))[0]
            

                elif not repl and redu:
                    temp_row = []
                    vals_redu =  item["redu"]
                    if not vals_redu:
                        self.logger.error("'redu'-Element is empty. (syntagma: '{}')".format(item["syntagma"]))
                        yield False
                        #return

                    for single_redu in vals_redu:
                        temp_row = []
                        for table_part in  Stats.header_order_to_export:
                            if table_part == "baseline":
                                temp_row += current_ordered_baseline_row

                            elif table_part == "document":
                                #p(header["document"])
                                temp_row += [single_redu[ix_redu[col_name]] for col_name in header["document"][0]]
                                col_from_corp = header["document"][1]
                                doc_id = single_redu[ix_doc_id_redu]
                                if col_from_corp:
                                    values_from_corp = self._get_values_from_doc(doc_id, col_from_corp)
                                    if values_from_corp:
                                        temp_row += list(values_from_corp)
                                    else:
                                        self.logger.error("No values from Corpus was returned")
                                        yield False
                                        return 

                            elif table_part == "word":
                                temp_row += [single_redu[ix_redu[col_name]] for col_name in header["word"]]


                            elif table_part == "redu":
                                temp_row += [single_redu[ix_redu[col_name]] for col_name in header["redu"]]

                            elif table_part == "context":
                                temp_row += [single_redu[ix_redu[col_name]] for col_name in header["context"]]

                        exported_rows_count += 1
                        yield temp_row
                    

                elif not redu and not repl:
                    self.logger.error("No one Phanomena was selected. Please select Redu or Repls to export.")
                    yield False
                    return


            if self._status_bar:
                # i += 1
                # print status_bar_current_right.total, count, i
                # if status_bar_current_right.total !=  count:
                #  status_bar_current_right.total = i
                #  status_bar_current_right.refresh()

                #p((status_bar_current_all.total, status_bar_current_all.count))
                if status_bar_current_all.total != status_bar_current_all.count:
                    status_bar_current_all.count = status_bar_current_all.total #= status_bar_current_all.count
                    status_bar_current_all.refresh()

                status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("Exported: Syntagmas:'{}'; Rows: '{}'; ".format(status_bar_current_right.count,exported_rows_count) ), "",  counter_format=self.status_bars_manager.term.bold_white_on_green('{fill}{desc}{fill}\n'))
                status_bar_total_summary.refresh()
                self.status_bars_manager.stop()
            #p(i, "i")
            if i == 0:
                self.logger.critical("No Data was found for current settings. Please try to change the settings.")
                yield False
                return 
            



    def _check_exist_columns_to_get(self, get_columns_repl, get_columns_redu,get_columns_baseline):
        status = True
        if get_columns_repl:
            columns_from_db = self.statsdb.col("replications")
            for col in get_columns_repl:
                if col not in columns_from_db:
                    self.logger.error("'{}'-column is not exist in 'replications'-Table. ".format(col) )
                    status = False


        if get_columns_redu:
            columns_from_db = self.statsdb.col("reduplications")
            for col in get_columns_redu:
                if col not in columns_from_db:
                    self.logger.error("'{}'-column is not exist in 'reduplications'-Table. ".format(col) )
                    status = False

        if get_columns_baseline:
            columns_from_db = self.statsdb.col("baseline")
            for col in get_columns_baseline:
                if col not in columns_from_db:
                    self.logger.error("'{}'-column is not exist in 'baseline'-Table. ".format(col) )
                    status = False

        return status




    def _convert_cols_to_indexes(self, get_columns_repl,get_columns_redu,get_columns_baseline,indexes):
        indexes_to_get_repl = []
        indexes_to_get_redu = []
        indexes_to_get_baseline  = []
        
        if get_columns_repl:
            ix = indexes["repl"]
            for col in  get_columns_repl:
                indexes_to_get_repl.append(ix[col])

        if get_columns_redu:
            ix = indexes["redu"]
            for col in  get_columns_redu:
                indexes_to_get_redu.append(ix[col])

        if get_columns_baseline:
            ix = indexes["baseline"]
            for col in  get_columns_baseline:
                indexes_to_get_baseline.append(ix[col])

        return indexes_to_get_repl,indexes_to_get_redu,indexes_to_get_baseline 

        #return ""



    def _extract_certain_columns(self,data, indexes_to_get_repl,indexes_to_get_redu,indexes_to_get_baseline):
        #pass
        #indexes = self.col_index_min if minimum_columns else self.col_index_orig
        if indexes_to_get_repl:
            repls = data["repl"]
            if repls:
                new_repls = []
                for repl in repls:
                    new_repls.append([repl[i] for i in indexes_to_get_repl])

                data["repl"] = new_repls


        if indexes_to_get_redu:
            redus = data["redu"]
            if redus:
                new_redus = []
                for redu in redus:
                    new_redus.append([redu[i] for i in indexes_to_get_redu])

                data["redu"] = new_redus


        if indexes_to_get_baseline:
            baseline = data["baseline"]
            if baseline:
                new_baseline = []
                for b in baseline:
                    new_baseline.append([b[i] for i in indexes_to_get_baseline])

                data["baseline"] = new_baseline

        
        return data


    def compute_rep_sum(self,syntagma_to_search,  reptype, syntagma_type="lexem",sentiment=False,
                        stemmed_search=False, thread_name="Thread0", ignore_num=False,ignore_symbol=False, word_examples_sum_table=True):
        
        max_scope = 1
        if reptype == "repl":
            repl = True
            redu = False
        else:
            repl = False
            redu = True


        num = self._get_row_num_in_baseline_with_rep(redu=redu, repl=repl, max_scope=max_scope)

        if self._status_bar:
            try:
                if not self.status_bars_manager.enabled:
                    self.status_bars_manager = self._get_status_bars_manager()
            except:
                self.status_bars_manager = self._get_status_bars_manager()

            status_bar_current = self._get_new_status_bar(num, "Summarizing:", "syntagma")

        
        #minimum_columns = True
        if reptype == "repl":
            collected_repls_from_corp = defaultdict(lambda:defaultdict(lambda: [[],None]))
            get_columns_repl = ("doc_id","index_in_corpus","repl_letter",  "repl_length", "rle_word", "pos")
            ### Step 1: Collect Data From Corpus
            i = 0
            for item in self.get_data(syntagma_to_search, repl=True, redu=False, baseline=False, get_columns_repl=get_columns_repl,
                                    max_scope=max_scope,sentiment=sentiment,syntagma_type=syntagma_type,
                                    stemmed_search=stemmed_search):
                if self._status_bar:
                    status_bar_current.update(incr=1)
                i+= 1
                #p(item, "item")
                #repls = item["repl"]
                for repl in item["repl"]:
                    if ignore_num:
                        if repl[5] == "number":
                            continue 
                    if ignore_symbol:
                        if repl[5] == "symbol":
                            continue
                    #p(repl, "repl")
                    collected_repls_from_corp[repl[0]][repl[1]][0].append((repl[2], repl[3]))
                    if word_examples_sum_table:
                        collected_repls_from_corp[repl[0]][repl[1]][1] = repl[4]

            ### Step 1: Compute Summ
            if word_examples_sum_table:
                summery = defaultdict(lambda:defaultdict(lambda:[0,defaultdict(lambda: 0) ]))
            else:
                summery = defaultdict(lambda:defaultdict(lambda:[0]))

            for doc_id, doc_data in collected_repls_from_corp.iteritems():
                for index_in_corpus , repl_container in doc_data.iteritems():
                    for repl in repl_container[0]:
                        #p(repl, "repl")
                        summery[repl[0]][repl[1]][0] += 1
                        if word_examples_sum_table:
                            summery[repl[0]][repl[1]][1][repl_container[1]] += 1
            #p(word_examples_sum_table, "word_examples_sum_table")


            if self._status_bar:
                if status_bar_current.total != i:
                    #raise Exception, "PREDICED LEN IS NOT CORRECT IN SUM COMPUTER"
                    status_bar_current.total = i
            if i == 0:
                self.logger.error("('{}'-sum) Nothing was extracted for '{}'-syntagma. No Data was found for given settings.".format(reptype,syntagma_to_search))
            return summery


        else:
            get_columns_redu = (db_helper.tag_normalized_word,"redu_length",  "pos")
            collected_redus_from_corp = defaultdict(lambda: defaultdict(lambda:0))
            i = 0
            #p((syntagma_to_search,max_scope, sentiment, syntagma_type, stemmed_search))
            for item in self.get_data(syntagma_to_search, redu=True, repl=False, baseline=False, get_columns_redu=get_columns_redu, max_scope=max_scope,
                                        sentiment=sentiment,syntagma_type=syntagma_type,stemmed_search=stemmed_search):
                #p(item,"item")
                i += 1
                if self._status_bar:
                    status_bar_current.update(incr=1)

                for redu in item["redu"]:
                    if ignore_num:
                        if redu[3] == "number":
                            continue 
                    if ignore_symbol:
                        if redu[3] == "symbol":
                            continue
                    #p(redu)
                    collected_redus_from_corp[redu[0]][redu[1]] += 1


            if self._status_bar:
                if status_bar_current.total != i:
                    #raise Exception, "PREDICED LEN IS NOT CORRECT IN SUM COMPUTER"
                    status_bar_current.total = i
            if i == 0:
                self.logger.error("('{}'-sum) Nothing was extracted for '{}'-syntagma. No Data was found for given settings.".format(reptype,syntagma_to_search))
            return collected_redus_from_corp
            #p(collected_redus_from_corp, "collected_redus_from_corp")



    def _get_row_num_in_baseline_with_rep(self, redu=False, repl=False, max_scope=False):
        #p((redu, repl, max_scope))
        if repl or redu:
            rep_w_list = []
            if repl: 
                w_repl = " occur_repl_uniq IS NOT NULL "
                if self._full_repetativ_syntagma:
                    w_repl = "({} AND occur_full_syn_repl IS NOT NULL )".format(w_repl )
                rep_w_list.append(w_repl)
            
            if redu: 
                w_redu = " occur_redu_uniq IS NOT NULL "
                if self._full_repetativ_syntagma:
                    w_redu = "({} AND occur_full_syn_redu IS NOT NULL )".format(w_redu)
                rep_w_list.append(w_redu)

            #if redu: rep_w_list.append(" occur_redu_uniq IS NOT NULL ")
            where_str = "OR".join(rep_w_list)
            where_str =  "({})".format(where_str) if len(rep_w_list)>1 else where_str
            if max_scope: where_str += " AND scope<={} ".format(max_scope)
            
            where_str = where_str if where_str else False
            #p(where_str,"where_str")
            num= self.statsdb.rownum("baseline", where=where_str,connector_where="OR")
        else:
            num = 0

        return num


    def get_data(self,inp_syntagma="*",repl=False, redu=False, baseline=False, syntagma_type="lexem", 
                sentiment=False,thread_name="Thread0", max_scope=False, stemmed_search=False,send_empty_marker=False,
                minimum_columns=False,order_output_by_syntagma_order=False, return_full_tuple=False,delete_duplicates=True,
                get_columns_repl=False,get_columns_redu=False,get_columns_baseline=False,
                if_type_pos_return_lexem_syn=False):

        #p(inp_syntagma, "0inp_syntagma")
        # p((inp_syntagma,repl,redu,baseline))
        # p("..9999")
        #p(locals())
        if inp_syntagma == "*":
            #p("..888")
            return self._get_data(inp_syntagma=inp_syntagma,repl=repl, redu=redu, baseline=baseline, syntagma_type=syntagma_type, 
                sentiment=sentiment,thread_name=thread_name, max_scope=max_scope, stemmed_search=stemmed_search,
                minimum_columns=minimum_columns,order_output_by_syntagma_order=order_output_by_syntagma_order,send_empty_marker=send_empty_marker, 
                return_full_tuple=return_full_tuple,delete_duplicates=delete_duplicates, if_type_pos_return_lexem_syn=if_type_pos_return_lexem_syn,
                get_columns_repl=get_columns_repl,get_columns_redu=get_columns_redu,get_columns_baseline=get_columns_baseline)
        else:
            if thread_name not in self.preprocessors:
                if not self._init_preprocessors(thread_name=thread_name):
                    self.logger.error("Error during Preprocessors initialization. Thread '{}' was stopped.".format(thread_name), exc_info=self._logger_traceback)
                    self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":"Error during Preprocessors initialization"})
                    self._terminated = True
                    return False
            # p("..7777")
            try:
                inp_syntagma[0].decode # if iterator with just one syntagma
                extract_type = 1
            except AttributeError:
                try:
                    inp_syntagma[0][0].decode #if iterator with just many different syntagma
                    extract_type = 2
                except AttributeError as e:
                    self.logger.error("Given Syntagma '{}' has not correct format. Exception: '{}'.".format(inp_syntagma, repr(e)))
                    return False
                except Exception as e:
                    self.logger.error(" Exception was throw: '{}'.".format( repr(e)))
                    return False

        # p("..666")
        if extract_type == 1:
            #p("..555")
            #p(inp_syntagma, "999999inp_syntagma")
            gen =  self._get_data(inp_syntagma=inp_syntagma,repl=repl, redu=redu, baseline=baseline, syntagma_type=syntagma_type, 
                sentiment=sentiment,thread_name=thread_name, max_scope=max_scope, stemmed_search=stemmed_search,
                minimum_columns=minimum_columns,order_output_by_syntagma_order=order_output_by_syntagma_order,send_empty_marker=send_empty_marker,
                return_full_tuple=return_full_tuple,delete_duplicates=delete_duplicates,if_type_pos_return_lexem_syn=if_type_pos_return_lexem_syn,
                get_columns_repl=get_columns_repl,get_columns_redu=get_columns_redu,get_columns_baseline=get_columns_baseline)
            #p(len(gen), "num") 
            
            if not gen:
                self.logger.error("Current Generator wasn't created")
                return False
            return gen
        else:
            #p("..444")
            generators = []
            #p(inp_syntagma, "1999999inp_syntagma")
            #p(inp_syntagma, "2inp_syntagma")
            not_init_gens = -1
            for counter,  inp_syn in enumerate(inp_syntagma):
                gen = self._get_data(inp_syntagma=inp_syn,repl=repl, redu=redu, baseline=baseline, syntagma_type=syntagma_type, 
                sentiment=sentiment,thread_name=thread_name, max_scope=max_scope, stemmed_search=stemmed_search,send_empty_marker=send_empty_marker,
                minimum_columns=minimum_columns,order_output_by_syntagma_order=order_output_by_syntagma_order,
                return_full_tuple=return_full_tuple,delete_duplicates=delete_duplicates, if_type_pos_return_lexem_syn=if_type_pos_return_lexem_syn,
                get_columns_repl=get_columns_repl,get_columns_redu=get_columns_redu,get_columns_baseline=get_columns_baseline)
                if not gen:
                    not_init_gens += 1
                else:
                    #self.logger.error("Current Generator wasn't created")
                    #return False
                    generators.append(gen)

            if counter == not_init_gens:
                #p(not_init_gens)
                self.logger.error("Not one generator was created!")
                return False

            #p(generators, "generators")
            # p("..333")
            num = sum([len(gen) for gen in generators])
            #p(num, "num")
            def intern_gen():
                # p("..222")
                for gen in generators:
                    if not gen:
                        yield False
                        return 
                    for item in gen:
                        yield item

            return LenGen(intern_gen(), num)


    def _lexem_syn_extractor_from_pos(self, inp_syntagma, inpdata, repl=False, redu=False, baseline=False,
                                    sentiment=False, minimum_columns=False,order_output_by_syntagma_order=False, 
                                    return_full_tuple=False,delete_duplicates=True,#send_empty_marker=False,
                                    get_columns_repl=False,get_columns_redu=False,get_columns_baseline=False):
        max_scope=False
        stemmed_search=False
        inpdata = list(inpdata)
        if len(inpdata) > 1:
            self.logger.error("The Length of given generator is more as 1.")
            return False

        elif len(inpdata) == 0:
            self.logger.error("The Length of given generator is 0.")
            return False

        
        inpdata = inpdata[0]
        if not inpdata:
            return False

        syn_len = len(inp_syntagma)
        exctracted_baseline = [b for b in inpdata["baseline"] if len(b[0])==syn_len]
        def intern_gen():
            already_exported_syntagma = set()
            for b in exctracted_baseline:
                lexem_syn = b[0]
                #p(lexem_syn, "1111lexem_syn", c="r")
                data = self._get_data_for_one_syntagma(lexem_syn, repl=repl, redu=redu, baseline=baseline, syntagma_type="lexem", additional_pos_where=inp_syntagma, 
                                            sentiment=sentiment, max_scope=False,
                                            for_optimization=False, stemmed_search=False, get_also_non_full_repetativ_result=False,
                                            order_output_by_syntagma_order=order_output_by_syntagma_order, return_full_tuple=return_full_tuple,
                                            minimum_columns=minimum_columns, delete_duplicates=delete_duplicates,)
                #p(data,">>>>data", c="c")
                s = tuple(data["syntagma"])
                if s in already_exported_syntagma:
                    continue
                else:
                    already_exported_syntagma.add(s)
                yield data

        return LenGen(intern_gen(), len(exctracted_baseline))




    def _get_data(self,inp_syntagma="*",repl=False, redu=False, baseline=False, syntagma_type="lexem", 
                sentiment=False,thread_name="Thread0", max_scope=False, stemmed_search=False, send_empty_marker=False,
                minimum_columns=False,order_output_by_syntagma_order=False, return_full_tuple=False,delete_duplicates=True,
                get_columns_repl=False,get_columns_redu=False,get_columns_baseline=False,if_type_pos_return_lexem_syn=False):

        #print "111"
        # p("---9999")
        #p(inp_syntagma, "11inp_syntagma")
        if not self._check_stats_db_should_exist():
            return False 

        #if not isinstance(inp_syntagma, (list,tuple))
        if syntagma_type not in Stats.supported_syntagma_type:
            self.logger.error("Given SyntagmaType '{}' is not supported. Please select one of the following types: '{}'.".format(syntagma_type, Stats.supported_syntagma_type))
            return False 

        if not inp_syntagma:
            self.logger.error("NO InpSyntagma was given.")
            return False

        if sentiment and sentiment not in Stats.supported_sentiment:
            self.logger.error("Given SentimentType '{}' is not supported. Please select one of the following types: '{}'. (!should be given in lower case!)".format(sentiment, Stats.supported_sentiment))
            return False 

        indexes = self.col_index_min if minimum_columns else self.col_index_orig
        if get_columns_repl or get_columns_redu or get_columns_baseline:
            if not self._check_exist_columns_to_get( get_columns_repl, get_columns_redu,get_columns_baseline):
                self.logger.error("Some given columns_to_get is not exist.")
                return False
                 
            indexes_to_get_repl,indexes_to_get_redu,indexes_to_get_baseline = self._convert_cols_to_indexes(get_columns_repl,get_columns_redu,get_columns_baseline,indexes)
        #print "2222"
        # p("---888")
        if not repl and not redu and not baseline:
            self.logger.error("No Phenomena to export was selected. Please choice phenomena to export from the following list: '{}'. ".format(Stats.supported_phanomena_to_export))
            return False

        # p("---777")
        if inp_syntagma == "*":
            # p("---6666")
            #print "333"
            #p(inp_syntagma,"0000inp_syntagma")
            
            num = self._get_row_num_in_baseline_with_rep(redu=redu, repl=repl, max_scope=max_scope)
            #p(num, "num")
            def intern_gen_all():
                # p("---555")
                for baseline_container in self._baseline("*",max_scope=max_scope):
                    #inp_syntagma =  self._preprocess_syntagma(inp_syntagma,thread_name=thread_name, syntagma_type=syntagma_type)
                    # p(max_scope, "max_scope")
                    # p(("---4444", baseline_container))
                    data =  self._get_data_for_one_syntagma(baseline_container[0],repl=repl, redu=redu, baseline=False,
                            syntagma_type=syntagma_type, sentiment=sentiment,thread_name=thread_name, stemmed_search=False,
                            max_scope=max_scope, order_output_by_syntagma_order=order_output_by_syntagma_order, 
                            return_full_tuple=return_full_tuple,delete_duplicates=delete_duplicates,
                            minimum_columns=minimum_columns,indexes=indexes)
                    
                    # p(("--333", data))
                    #if data:
                    #    sys.exit()



                    if data:
                        if baseline:
                            data["baseline"] = (baseline_container,)
                        if get_columns_repl or get_columns_redu or get_columns_baseline:
                            data = self._extract_certain_columns(data, indexes_to_get_repl,indexes_to_get_redu,indexes_to_get_baseline)
                        yield data
                    else:
                        if data is False:
                            yield False
                            return
                        
                        if send_empty_marker:
                            yield None
                        continue
                    

            return LenGen(intern_gen_all(), num)

        #self._empty_marker = None

        else:
            # p("---222")
            #print "444"
            inp_syntagma =  self._preprocess_syntagma(inp_syntagma,thread_name=thread_name, syntagma_type=syntagma_type, stemmed_search=stemmed_search)
            if not inp_syntagma:
                self.logger.error("Error by preprocessing of the InpSyntagma.")
                return  False
            #p(inp_syntagma, "555inp_syntagma")
            if stemmed_search:
                #print "555"
                    #p(temp_syntagma, "temp_syntagma")
                where_num = "stemmed='{}'".format(self._baseline_delimiter.join(inp_syntagma) )
                num = self.statsdb.rownum("baseline", where=where_num)
                def intern_gen_2():
                    scope = len(inp_syntagma)
                    where = tuple(self._get_where_statement(inp_syntagma,scope=scope,thread_name=thread_name, with_context=False,syntagma_type="lexem", sentiment=sentiment, stemmed_search=True))#, splitted_syntagma=splitted_syntagma)
                    if not where:
                        yield False
                        return 
                    for baseline_container in self._baseline(inp_syntagma,where=where, minimum_columns=minimum_columns,max_scope=max_scope,split_syntagma=True):
                        #p(baseline_container, "baseline_container")
                        data =  self._get_data_for_one_syntagma(baseline_container[0],repl=repl, redu=redu, baseline=False, syntagma_type=syntagma_type,
                                                sentiment=sentiment,thread_name=thread_name, max_scope=False, stemmed_search=False,
                                                order_output_by_syntagma_order=order_output_by_syntagma_order,minimum_columns=minimum_columns,
                                                return_full_tuple=return_full_tuple,delete_duplicates=delete_duplicates,indexes=indexes)
                        #p(data, "data")
                        if data:
                            data["baseline"] = (baseline_container,)
                            data["stem_syn"] = inp_syntagma
                            if get_columns_repl or get_columns_redu or get_columns_baseline:
                                data = self._extract_certain_columns(data, indexes_to_get_repl,indexes_to_get_redu,indexes_to_get_baseline)
                            #p(data, "data")
                            yield data
                        else:
                            if send_empty_marker:
                                yield None
                        #else:
                        #    yield {}
                if if_type_pos_return_lexem_syn and syntagma_type=="pos":
                    #p("if_type_pos_return_lexem_syn")
                    return self._lexem_syn_extractor_from_pos(inp_syntagma, intern_gen_all(),
                                                    repl=repl, redu=redu, baseline=baseline,
                                                    sentiment=sentiment,
                                                    minimum_columns=minimum_columns,order_output_by_syntagma_order=order_output_by_syntagma_order, return_full_tuple=return_full_tuple,delete_duplicates=delete_duplicates,
                                                    get_columns_repl=get_columns_repl,get_columns_redu=get_columns_redu,get_columns_baseline=get_columns_baseline)
                else:
                    return LenGen(intern_gen_2(), num)


            else:
                #print "666"

                def inter_gen_3():
                    data =  self._get_data_for_one_syntagma(inp_syntagma,repl=repl, redu=redu, baseline=baseline, syntagma_type=syntagma_type,
                                            sentiment=sentiment,thread_name=thread_name, max_scope=max_scope, stemmed_search=False,
                                            order_output_by_syntagma_order=order_output_by_syntagma_order,minimum_columns=minimum_columns,
                                            return_full_tuple=return_full_tuple,delete_duplicates=delete_duplicates,indexes=indexes)
                    if data:
                        if get_columns_repl or get_columns_redu or get_columns_baseline:
                            data = self._extract_certain_columns(data, indexes_to_get_repl,indexes_to_get_redu,indexes_to_get_baseline)
                        #p(data, "data")
                        yield data   
                    else:
                        if send_empty_marker:
                            yield None
           

                if if_type_pos_return_lexem_syn and syntagma_type=="pos":
                    #p("if_type_pos_return_lexem_syn")
                    return self._lexem_syn_extractor_from_pos(inp_syntagma,inter_gen_3(),
                                                    repl=repl, redu=redu, baseline=baseline,
                                                    sentiment=sentiment,
                                                    minimum_columns=minimum_columns,order_output_by_syntagma_order=order_output_by_syntagma_order, return_full_tuple=return_full_tuple,delete_duplicates=delete_duplicates,
                                                    get_columns_repl=get_columns_repl,get_columns_redu=get_columns_redu,get_columns_baseline=get_columns_baseline)
                else:
                    return LenGen(inter_gen_3(), 1)   




    def _get_data_for_one_syntagma(self,inp_syntagma_splitted, inp_syntagma_unsplitted=False,
                            repl=False, redu=False, baseline=False, syntagma_type="lexem", additional_pos_where=False, 
                            sentiment=False,thread_name="Thread0", max_scope=False,
                            for_optimization=False, stemmed_search=False, get_also_non_full_repetativ_result=False,
                            #get_columns_repl=False, get_columns_redu=False,get_columns_baseline=False,
                            order_output_by_syntagma_order=False, return_full_tuple=False, output_type="list",
                            minimum_columns=False, delete_duplicates=True, indexes=False, ):#,splitted_syntagma=True):
        #p((inp_syntagma_splitted, repl, redu, baseline,stemmed_search,additional_pos_where))
        #p(locals())
        scope = len(inp_syntagma_splitted)
        if not self._is_syntagma_scope_right(scope):
            #self.logger.error("The Length ('{}') of  Given SyntagmaToSearch ('{}') is  bigger as allow ('{}'). Please recompute StatsDB with the bigger ContextNumber.".format(scope, inp_syntagma_splitted,self._avaliable_scope))
            #if isinstance()
            return None

        if stemmed_search:
            inp_syntagma_splitted =  self._preprocess_syntagma(inp_syntagma_splitted,thread_name=thread_name, syntagma_type=syntagma_type, stemmed_search=stemmed_search)
            if inp_syntagma_unsplitted:
                inp_syntagma_unsplitted = self._baseline_delimiter.join(inp_syntagma_splitted)


        if not indexes:
            indexes = self.col_index_min if minimum_columns else self.col_index_orig

        #p(indexes, "indexes")
        _repl = []
        _redu = []
        _baseline = []
        
        #p(syntagma_type, "syntagma_type")
        #p(scope,"scope2")
        where1 = False
        if repl:
            if not where1:
                where1 = tuple(self._get_where_statement(inp_syntagma_splitted,scope=scope,thread_name=thread_name,
                                            with_context=True,syntagma_type=syntagma_type, sentiment=sentiment, 
                                            inp_syntagma_unsplitted=inp_syntagma_unsplitted,stemmed_search=stemmed_search,
                                            additional_pos_where=additional_pos_where))#, splitted_syntagma=splitted_syntagma)
                if not where1: return False
            #p(where1,"where1_repl", c="b")
            _repl = self.get_reps("repl",inp_syntagma_splitted,scope,where1,indexes,thread_name=thread_name, minimum_columns=minimum_columns,
                                order_output_by_syntagma_order=order_output_by_syntagma_order, return_full_tuple=return_full_tuple,stemmed_search=False,
                                output_type=output_type,delete_duplicates=delete_duplicates,
                                syntagma_type=syntagma_type, for_optimization=for_optimization, get_also_non_full_repetativ_result=get_also_non_full_repetativ_result)
            #p(_repl, "_repl")
            # if get_columns_repl:
            #     if minimum_columns:
            #         self.logger.error("IllegalState: 'minimum_columns'-Option is True. It is not allow to get certain columns, if this option is true. Please switch off this option.")
            #         return {}


        if redu:
            if not where1:
                where1 = tuple(self._get_where_statement(inp_syntagma_splitted,scope=scope,thread_name=thread_name, with_context=True,
                                                syntagma_type=syntagma_type, sentiment=sentiment, inp_syntagma_unsplitted=inp_syntagma_unsplitted,
                                                stemmed_search=stemmed_search,additional_pos_where=additional_pos_where))#, splitted_syntagma=splitted_syntagma)
                if not where1: return False
            #p(where1,"where1_redu", c="b")
            _redu = self.get_reps("redu",inp_syntagma_splitted,scope,where1,indexes,thread_name=thread_name, minimum_columns=minimum_columns,
                            order_output_by_syntagma_order=order_output_by_syntagma_order, return_full_tuple=return_full_tuple,stemmed_search=False,
                            output_type=output_type,delete_duplicates=delete_duplicates,
                            syntagma_type=syntagma_type, for_optimization=for_optimization, get_also_non_full_repetativ_result=get_also_non_full_repetativ_result)

        #p((repl,_repl, redu, _redu))

        if baseline:
            if syntagma_type == "lexem":
                where2 = tuple(self._get_where_statement(inp_syntagma_splitted,scope=scope,thread_name=thread_name, with_context=False,syntagma_type=syntagma_type, sentiment=sentiment, inp_syntagma_unsplitted=inp_syntagma_unsplitted,stemmed_search=stemmed_search, additional_pos_where=additional_pos_where))#, splitted_syntagma=splitted_syntagma)
                if not where2: return False
                _baseline = tuple(self._baseline(inp_syntagma_splitted,where=where2,minimum_columns=minimum_columns, thread_name=thread_name))
            else:
                all_syntagmas = []
                if _repl:
                    all_syntagmas += self._extract_all_syntagmas(_repl, "repl", ordered_output_by_syntagma_order=order_output_by_syntagma_order,minimum_columns=minimum_columns)
                if _redu:
                    all_syntagmas += self._extract_all_syntagmas(_redu, "redu", ordered_output_by_syntagma_order=order_output_by_syntagma_order,minimum_columns=minimum_columns)

                #p(all_syntagmas,"all_syntagmas")

                for temp_syntagma in set(all_syntagmas):
                    #p(temp_syntagma, "temp_syntagma")
                    where2 = tuple(self._get_where_statement(temp_syntagma,scope=scope,thread_name=thread_name, with_context=False,syntagma_type="lexem", sentiment=sentiment,
                                                        inp_syntagma_unsplitted=inp_syntagma_unsplitted,stemmed_search=stemmed_search,
                                                        additional_pos_where=False))#, splitted_syntagma=splitted_syntagma)
                    if not where2: return False
                    _baseline += tuple(self._baseline(temp_syntagma,where=where2, minimum_columns=minimum_columns,thread_name=thread_name))

        #p((inp_syntagma_splitted,_repl, _redu, _baseline,))
        if not _repl and not _redu and not _baseline:
            return {}

        if return_full_tuple:
            #p((_repl, _redu,_baseline))
            if not _repl[0] and not _redu[0] and not _baseline:
                return {}


        return {"repl":_repl, "redu":_redu, "baseline":_baseline,"syntagma":inp_syntagma_splitted}



    def get_reps(self, rep_type,inp_syntagma_splitted,scope,where,indexes,thread_name="Thread0",
                order_output_by_syntagma_order=False, return_full_tuple=False, stemmed_search=False,
                output_type="list", minimum_columns=False,
                delete_duplicates=True, syntagma_type="lexem", for_optimization=False,
                get_also_non_full_repetativ_result=False):
        #p((rep_type,inp_syntagma_splitted,scope),"get_reps_BEGINN", c="r")
        ### Step 1: Variables Initialization
        _rep = []
        is_full_repetativ = True
        
        #if for_optimization:
        #    col_to_get = "id"
        #else:
        col_to_get = Stats.min_col[rep_type] if minimum_columns else False
        #p((rep_type, inp_syntagma_splitted, get_also_non_full_repetativ_result, for_optimization, scope,where))
        # p((where), "where_by_get_reps")
        ### Step 2: 
        if order_output_by_syntagma_order:
            for word,w in izip(inp_syntagma_splitted,where):
                current_reps = tuple(self._rep_getter_from_db(rep_type,inp_syntagma_splitted,scope=scope,where=w,thread_name=thread_name,columns=col_to_get, output_type=output_type, for_optimization=for_optimization))
                #if not current_reps:
                #    return False
                #p( current_reps, " current_reps")
                # p((current_reps, w))
                #for 
                if current_reps:
                    if for_optimization: return True # if match, than return True
                else:
                    if for_optimization: continue 
                    is_full_repetativ = False
                    if self._full_repetativ_syntagma:
                        if not get_also_non_full_repetativ_result:
                            _rep = ()
                            break
                          
                _rep.append( (word,current_reps))

            if for_optimization: return False # if here, it means, that not one match was found till now.

            ### Check, if reps in containers are empty 
            i = 0
            for container in _rep:
                if not container[1]:
                    i += 1
            if len(_rep) == i:
                _rep =  ()

        else:
            for w in where:
                #p(w, "w_in_rep", c="c")
                #print 1111
                current_reps = tuple(self._rep_getter_from_db(rep_type,inp_syntagma_splitted,scope=scope,where=w,thread_name=thread_name,columns=col_to_get,  output_type=output_type, for_optimization=for_optimization))
                #print "current_reps= ", current_reps
                if current_reps:
                    #print 22222
                    if for_optimization: return True # if match, than return True
                else:
                    #print 3333
                    if for_optimization: continue 
                    is_full_repetativ = False
                    if self._full_repetativ_syntagma:
                        if not get_also_non_full_repetativ_result:
                            _rep = ()
                            break
                #print 4444   
                _rep += current_reps

            if for_optimization: return False # if here, it means, that not one match was found till now.
            #print 555

        if _rep:
            ## Step 5: 
            if get_also_non_full_repetativ_result: return _rep
            id_ix = indexes[rep_type]["id"]
            if  self._full_repetativ_syntagma and scope > 1 and is_full_repetativ:
                reconstructed,length = self._reconstruct_syntagma(rep_type, _rep, order_output_by_syntagma_order,indexes,syntagma_type=syntagma_type,stemmed_search=stemmed_search)
                full_syntagmas, allowed_ids = self._exctract_full_syntagmas(reconstructed,scope,length,inp_syntagma_splitted,syntagma_type=syntagma_type)
                _rep = self._filter_full_rep_syn(rep_type,_rep, allowed_ids,order_output_by_syntagma_order ,id_ix) #

            if delete_duplicates:
               _rep = self._delete_dublicats_in_reps( _rep, order_output_by_syntagma_order,id_ix)


        ### Step 6: 
        if return_full_tuple:
            try:
                full_syn_sum = len(full_syntagmas) if _rep else 0
            except:
                full_syn_sum = None
            if _rep:
                return (_rep, is_full_repetativ, full_syn_sum)
            else:
                _rep
        else:
            return _rep
     





    def _reconstruct_syntagma(self,rep_type, reps, order_output_by_syntagma_order,indexes,syntagma_type="lexem",stemmed_search=False,):
        #p((rep_type, reps, inp_syntagma_splitted, scope,minimum_columns,order_output_by_syntagma_order))
        #p(indexes)
        reconstr_tree = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:[None,tuple()])))
        #reconstr_tree = defaultdict(lambda: defaultdict(lambda: defaultdict(tuple)))
        length = {}

        indexes = indexes[rep_type]
        word_tag = "stemmed" if stemmed_search else 'normalized_word'
        syn_ix = indexes[word_tag] if syntagma_type == "lexem" else indexes['pos']
        #p(syn_ix,"syn_ix")
        #p(indexes['normalized_word'], "indexes['normalized_word']")
        #p(indexes['pos'],"indexes['pos']")

        if order_output_by_syntagma_order:
            for word, reps_bunch in reps:
                #word = reps_container[0]
                #reps_bunch = reps_container[1]
                for i, rep in enumerate(reps_bunch):
                    #p((i, rep))
                    #p(rep[syn_ix])
                    doc_id = rep[indexes["doc_id"]]
                    index_in_redufree = json.loads(rep[indexes["index_in_redufree"]])
                    if doc_id not in length:
                        length[doc_id] = json.loads(rep[indexes["redufree_len"]])
                    reconstr_tree[doc_id][index_in_redufree[0]][index_in_redufree[1]][1] += (rep[indexes["id"]],)
                    if not reconstr_tree[doc_id][index_in_redufree[0]][index_in_redufree[1]][0]:
                        reconstr_tree[doc_id][index_in_redufree[0]][index_in_redufree[1]][0] = rep[syn_ix]
                     #+= (rep[indexes["id"]],)

        else:
            for i,rep in enumerate(reps):
                #p((i, rep))
                doc_id = rep[indexes["doc_id"]]
                index_in_redufree = json.loads(rep[indexes["index_in_redufree"]])
                if doc_id not in length:
                    length[doc_id] = json.loads(rep[indexes["redufree_len"]])
                reconstr_tree[doc_id][index_in_redufree[0]][index_in_redufree[1]][1] += (rep[indexes["id"]],)
                if not reconstr_tree[doc_id][index_in_redufree[0]][index_in_redufree[1]][0]:
                    reconstr_tree[doc_id][index_in_redufree[0]][index_in_redufree[1]][0] = rep[syn_ix]

        #p({  d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in reconstr_tree.iteritems()})
        return reconstr_tree,length




    def _exctract_full_syntagmas(self,reconstr_tree, scope, redu_free_elem_length,inp_syntagma_splitted,syntagma_type="lexem"):
        #p((reconstr_tree, scope, redu_free_elem_length,inp_syntagma_splitted,syntagma_type))
        try:
            #if syntagma_type == "pos":

            output_ix = ()
            allowed_ids = ()
            start_new = False
            incr = False
            cont = False
            orig_first_word = inp_syntagma_splitted[0]
            #pos = True if syntagma_type=="pos" else False

            for doc_id, doc_data in dict(sorted(reconstr_tree.items())).iteritems():
                redu_free_length = [l-1 for l in redu_free_elem_length[doc_id]] # convert length to index
                current_syn_ixs = ()
                syn_start_word = None
                start_tok = None
                temp_tok = None
                last_token = None
                last_sent = None
                temp_ids = ()
                counter_full_syn = 0
                for current_sent, sents_data in dict(sorted(doc_data.items())).iteritems():
                    for current_tok in sorted(sents_data.keys()):
                        # p((doc_id,current_sent,current_tok,start_tok, current_syn_ixs),c="m")
                        if temp_tok:
                            # print ",,,,,,"
                            tok_to_use = temp_tok
                        else:
                            # print "...."
                            tok_to_use = start_tok

                        if not start_tok:
                            # print "111"
                            last_token = current_tok
                            start_tok = (current_sent,current_tok)
                            start_new = True
                            counter_full_syn = 1
                        else:
                            # print "2222"
                            # print tok_to_use, counter_full_syn,current_tok
                            if (tok_to_use[1]+counter_full_syn) == current_tok:
                                # print "222+++"
                                counter_full_syn += 1
                                incr = True
                            else:#
                                # print "222---"
                                #print current_tok, (current_sent,last_sent), (last_token,redu_free_length[last_sent])
                                if current_tok==0 and ((current_sent-last_sent) == 1) and (last_token==redu_free_length[last_sent]): # if  the first token of the next sent build full_syntagma with the last token of the last sent
                                    # print "222!!!"
                                    temp_tok = (current_sent, current_tok)
                                    counter_full_syn = 1
                                    incr = True
                                else:
                                    # print "222???"
                                    start_new = True
                        #i = 0
                        while True:
                            #i+=1
                            #if i >3: break
                            if start_new:
                                # p("STARTED",c="m")
                                start_new = False
                                incr = True
                                # p(len(current_syn_ixs),"len(current_syn_ixs)")
                                if len(current_syn_ixs) == scope:
                                    # p("SAVED",c="m")
                                    output_ix += (current_syn_ixs,)
                                    #output_words += ((current_syn_words),)
                                    #output_doc_id += (doc_id,)
                                    allowed_ids += temp_ids
                                
                                
                                # Clean old vars
                                
                                current_syn_ixs=()
                                syn_start_word = sents_data[current_tok][0]
                                # print orig_first_word, syn_start_word
                                if orig_first_word  not in syn_start_word:
                                    # print "NOT ORIG AS START"
                                    cont = True
                                    break

                                #syn_start_word = None
                                temp_ids = ()
                                temp_tok = None
                                start_tok = (current_sent,current_tok)
                                counter_full_syn = 1
                                
                                # print "+++", counter_full_syn,syn_start_word


                            if incr:
                                incr = False
                                # p("INCR_START",c="m")
                                # print "!!!!!!!", syn_start_word, sents_data[current_tok]
                                if syn_start_word:
                                    # p((syn_start_word,sents_data[current_tok][0], counter_full_syn, current_syn_ixs,current_tok,sents_data[current_tok]),c="r")
                                    
                                    #if syn_start_word == sents_data[current_tok][0] and counter_full_syn>1 and not pos:
                                    #    # p("START NEW",c="m")
                                    #    start_new = True
                                    #    continue
                                    if len(current_syn_ixs)==scope:
                                        start_new = True
                                        continue                                    

                                current_syn_ixs += ((current_sent,current_tok),)
                                curr_rep = sents_data[current_tok]
                                #current_syn_words += (curr_rep[0],)
                                #syn_start_word = curr_rep[0]
                                
                                temp_ids += tuple(curr_rep[1])
                                # p("INCR_DONE",c="m")
                                break

                        if cont:
                            cont = False
                            continue


                        last_token = current_tok
                    last_sent = current_sent

                if len(current_syn_ixs) == scope:
                    output_ix += (current_syn_ixs,)
                    allowed_ids += temp_ids
            #p((output_ix, set(allowed_ids)))
            return output_ix, set(allowed_ids)
        except Exception as e:
            self.logger.error("Exception was throwed: '{}'.".format(repr(e)) ,exc_info=self._logger_traceback)
            return False, False






    def _delete_dublicats_in_reps(self,reps,order_output_by_syntagma_order,id_ix):
        new_reps = []
        used_id = set()
        if order_output_by_syntagma_order:
            for word, reps in reps[::-1]:
                temp_reps = ()
                for rep in reps:
                    rep_id = rep[id_ix]
                    if rep_id not in used_id:
                        used_id.add(rep_id)
                        temp_reps += (rep,)

                if temp_reps:
                    new_reps.append( (word,temp_reps) )
                else:
                    if self._full_repetativ_syntagma:
                        new_reps =  ()
                        break
                    else:
                        new_reps.append( (word,temp_reps) )
            new_reps = new_reps[::-1]
        else:
            #new_reps = ()
            for rep in reps:
                rep_id = rep[id_ix]
                if rep_id not in used_id:
                    used_id.add(rep_id)
                    new_reps.append( rep)

        return new_reps


    def _filter_full_rep_syn(self,rep_type,_rep, allowed_ids,order_output_by_syntagma_order, id_index):
        #p((rep_type,_rep, allowed_ids,order_output_by_syntagma_order), c="r")
        new_reps = []
        if order_output_by_syntagma_order:
            for word, reps in _rep:
                temp_reps = ()
                for rep in reps:
                    if rep[id_index] in allowed_ids:
                        temp_reps += (rep,)

                if temp_reps:
                    new_reps.append((word,temp_reps))
                else:
                    new_reps =  ()
                    break
        else:
            #new_reps = ()
            for rep in _rep:
                if rep[id_index] in allowed_ids:
                    new_reps.append(rep)

            if not new_reps:
                new_reps =  ()
                #break
        return new_reps

    def _rep_getter_from_db(self, rep_type,inp_syntagma="*", scope=False,
                            where=False, output_type="list", size_to_get=1000,
                            columns=False,thread_name="Thread0",
                            for_optimization=False,):
        if inp_syntagma != "*":
            if not where:
                self.logger.error("Where wasn't given.")
                #yield False
                return

        try:
            table_name = Stats.phenomena_table_map[rep_type]
        except:
            self.logger.error("Given RepType ('{}') is not exist.".format(rep_type))
            #yield False
            return 

        generator = self.statsdb.lazyget(table_name,  columns=columns, where=where, connector_where="AND", output=output_type, case_sensitiv=self._case_sensitiv,thread_name=thread_name)

        if for_optimization:
            try:
                next(generator)
                yield True
                return
            except StopIteration:
                #pass
                return
   

        for row in generator:
            yield row



    def _extract_all_syntagmas(self, entry, typ, ordered_output_by_syntagma_order=False,minimum_columns=False):
        #p(ordered_output_by_syntagma_order, "ordered_output_by_syntagma_order")
        all_syntagmas = set()
        #p(entry, "entry")
        if ordered_output_by_syntagma_order:
            for word_container in entry:
                for rep in word_container[1]:
                    done = False
                    for index in xrange(1, self._avaliable_scope+1):
                        temp_syntagma = []
                        for i in xrange(index):
                            #p(self._get_index_by_codepoint(i, typ), "self._get_index_by_codepoint(i, typ)")
                            word = rep[self._get_index_by_codepoint(i, typ,minimum_columns)]
                            #temp_syntagma.append(word)
                            if word:
                                temp_syntagma.append(word)
                            else:
                                #break
                                done=True
                                if done: break
                        
                        #p(temp_syntagma,"{}temp_syntagma".format(typ))
                        all_syntagmas.add(tuple(temp_syntagma))
                        #all_syntagmas.add(temp_syntagma)
                        if done: break

        else:
            #p(entry, "entry", c="r")
            for rep in entry:
                
                #p(rep,"rep", c="r")
                done = False
                for index in xrange(1, self._avaliable_scope+1):
                    temp_syntagma = []
                    for i in xrange(index):
                        #p(self._get_index_by_codepoint(i, typ), "self._get_index_by_codepoint(i, typ)")
                        word = rep[self._get_index_by_codepoint(i, typ,minimum_columns)]
                        #temp_syntagma.append(word)
                        #p(word, "word", c="m")
                        if word:
                            temp_syntagma.append(word)
                        else:
                            #break
                            done=True
                            if done: break
                    
                    #p(temp_syntagma,"{}temp_syntagma".format(typ))
                    all_syntagmas.add(tuple(temp_syntagma))
                    #all_syntagmas.add(temp_syntagma)
                    if done: break
                    #all_syntagmas.append(temp_syntagma)
                
        #p(all_syntagmas,"set_all_syntagmas")
        return all_syntagmas


  

    def _baseline(self, inp_syntagma="*", max_scope=False,  where=False, connector_where="AND", output="list", size_to_fetch=1000, thread_name="Thread0", split_syntagma=True,minimum_columns=False ,limit=-1, offset=0):
        #temp_cols_to_get = Stats.min_col["baseline"] if minimum_columns else False
        #columns = columns if columns else temp_cols_to_get
        columns = Stats.min_col["baseline"] if minimum_columns else False
        #p((where, inp_syntagma,max_scope))
        # p(locals())
        if inp_syntagma == "*":
            if max_scope is not False:
                w = "scope <= {}".format(max_scope)
                if where:
                    if isinstance(where, (list, tuple)):
                        #answer = None
                        ix = None
                        for index, tw in  enumerate(where):
                            if "scope" in tw:
                                ix = index
                        if ix:
                            where[ix] = w
                        else:
                            where.append(w)
                            if connector_where != "AND":
                                self.logger.error("PossibleWrongData: ConnectorWhere is 'OR' but should be 'AND'")

                    else:
                        temp_where = [where]
                        if "scope" not in where:
                            temp_where.append(w)
                        else:
                            temp_where = [w]
                else:
                    where = w


            
            #baseline_num = len(list(self.statsdb.lazyget("baseline", columns=columns, where=where, connector_where=connector_where, output=output, case_sensitiv=self._case_sensitiv,thread_name=thread_name+"BSGET",limit=limit, offset=offset, size_to_fetch=size_to_fetch)))
            # p((where,max_scope,baseline_num), "where")
            # print 000
            for row in self.statsdb.lazyget("baseline", columns=columns, where=where, connector_where=connector_where, output=output, case_sensitiv=self._case_sensitiv,thread_name=thread_name+"BSGET",limit=limit, offset=offset, size_to_fetch=size_to_fetch):
                # p(row, "row")
                # print 111
                if split_syntagma and row:
                    # print 222
                    #temp_row = list(row)
                    #row = list(row)
                    splitted_syntagma = row[0].split(self._baseline_delimiter)
                    #row[0] = splitted_syntagma
                    r = (splitted_syntagma,) + row[1:]
                    # p((r, split_syntagma))
                    yield (splitted_syntagma,) + row[1:]
                    #yield splitted_syntagma
                else:
                    # p((row, split_syntagma))
                    yield row

        else:
            if not where:
                self.logger.error("Where wasn't given.")
                yield False
                return

            for row in self.statsdb.lazyget("baseline", columns=columns, where=where, connector_where="AND", output=output, case_sensitiv=self._case_sensitiv,limit=limit, offset=offset):
                #p(row, "row")
                if split_syntagma and row:
                    row = list(row)
                    row[0] = row[0].split(self._baseline_delimiter)
                yield row

        #sys.exit()



    def _get_index_by_codepoint(self,  codepoint, typ,minimum_columns):
        indexes = self.col_index_min[typ] if minimum_columns else self.col_index_orig[typ]
        if codepoint == 0:
            return indexes["normalized_word"]
        elif codepoint == 1:
            return indexes["contextR1"]
        else:
            return indexes["contextR1"] + (2* (codepoint-1))

        


    def _get_where_statement(self,inp_syntagma_splitted, inp_syntagma_unsplitted=False,
                            scope=False, syntagma_type="lexem", sentiment=False,thread_name="Thread0", 
                            with_context=True,stemmed_search=False, additional_pos_where=False):#, splitted_syntagma=True):
        ### Syntagma Preprocessing
        #o = type(inp_syntagma_splitted)
        #p((inp_syntagma_splitted, o))
        status= True
        convert = False
        if syntagma_type != "pos":
            try:
                if not inp_syntagma_unsplitted:
                    try:
                        inp_syntagma_unsplitted = self._baseline_delimiter.join(inp_syntagma_splitted)
                    except TypeError:
                        inp_syntagma_unsplitted = self._baseline_delimiter.join([unicode(syntagma) for syntagma in inp_syntagma_splitted])
            except (UnicodeDecodeError, UnicodeEncodeError):
                convert = True
        

        while status:
            if convert: 
                #p( inp_syntagma_splitted, "1 inp_syntagma_splitted")
                try:
                    inp_syntagma_splitted = [word.decode("utf-8") for word in inp_syntagma_splitted]
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

                try: 
                    if inp_syntagma_unsplitted:
                        try:
                            inp_syntagma_unsplitted = inp_syntagma_unsplitted.decode("utf-8")
                        except (UnicodeDecodeError, UnicodeEncodeError):
                            pass
                    else:
                        inp_syntagma_unsplitted = self._baseline_delimiter.join(inp_syntagma_splitted)
                    #p(repr(inp_syntagma_unsplitted), "inp_syntagma_unsplitted")
                except (UnicodeDecodeError, UnicodeEncodeError):
                    inp_syntagma_unsplitted = self._baseline_delimiter.join([unicode(t) for t in inp_syntagma_splitted])
                #p(repr(inp_syntagma_unsplitted), "2 inp_syntagma_unsplitted")
                try:
                    additional_pos_where = [word.decode("utf-8") for word in additional_pos_where]
                except:
                    pass


            #p(inp_syntagma_splitted, "inp_syntagma_splitted")
            try:
                #wheres = []
                if with_context: # for repl and redu
                    if syntagma_type == "lexem":
                        if stemmed_search:
                            normalized_word_tag_name = "stemmed"
                        else:
                            normalized_word_tag_name = "normalized_word"
                    else:
                        normalized_word_tag_name = "pos"
                    #normalized_word_tag_name = "normalized_word" if syntagma_type == "lexem" else "pos"
                    if stemmed_search:
                        context_tag_name_r = "context_infoR"
                        context_tag_name_l = "context_infoL"
                        word_index = 2
                    else:
                        context_tag_name_r = "contextR"  if syntagma_type == "lexem" else "context_infoR"
                        context_tag_name_l = "contextL"  if syntagma_type == "lexem" else "context_infoL"
                        word_index = 0
                    # splitted_syntagma = inp_syntagma_splitted if splitted_syntagma else inp_syntagma_splitted.split(self._baseline_delimiter)
                    # unsplitted_syntagma = inp_syntagma_splitted if splitted_syntagma else inp_syntagma_splitted.split(self._baseline_delimiter)
                    if scope > self.baseline_ngramm_lenght:
                        self.logger.error("WhereGetter: Given Scope ('{}') is higher as allow ('{}'). (given syntagma:'{}'). ".format(scope, self.baseline_ngramm_lenght, inp_syntagma_splitted))
                        #yield False
                        return 

                    for token_index in xrange(scope):
                        last_token_index = scope-1
                        where = []
                        for i, token in  zip(range(scope),inp_syntagma_splitted):
                            #p(token, "token")
                            #token = token.replace("'", '"') if "'" in token  else token
                            if i < token_index:
                                #ix = token_index -1
                                #json_extract("text", "$[1]")
                                col_name = u"{}{}".format(context_tag_name_l,token_index-i)

                                search_pattern = u"{}='{}'".format(col_name,token) if syntagma_type == "lexem" and not stemmed_search  else  u'json_extract("{}", "$[{}]")  = "{}"'.format(col_name,word_index,token)
                                #search_pattern = u"='{}'".format(token) if syntagma_type == "lexem" else  u"LIKE '%{}%'".format(token)
                                where.append(search_pattern)
                                if additional_pos_where and syntagma_type!="pos":
                                    col_name = u"{}{}".format("context_infoL",token_index-i)
                                    search_pattern = u'json_extract("{}", "$[0]")  = "{}"'.format(col_name,additional_pos_where[i])
                                    where.append(search_pattern)
                                #where.append(u"{}{} {} ".format(context_tag_name_l,token_index-i,search_pattern))

                            elif i == token_index:
                                where.append(u"{}='{}' ".format(normalized_word_tag_name,token))
                                if additional_pos_where and syntagma_type!="pos":
                                    where.append(u" pos = '{}' ".format(additional_pos_where[i]))
                            elif i > token_index:
                                col_name = u"{}{}".format(context_tag_name_r,i-token_index)
                                search_pattern = u"{}='{}'".format(col_name,token) if syntagma_type == "lexem" and not stemmed_search else  u'json_extract("{}", "$[{}]")  = "{}"'.format(col_name,word_index,token)
                                #search_pattern = u"='{}'".format(token) if syntagma_type == "lexem" else  u"LIKE '%{}%'".format(token)
                                where.append(search_pattern)
                                if additional_pos_where and syntagma_type!="pos":
                                    col_name = u"{}{}".format("context_infoR",i-token_index)
                                    search_pattern = u'json_extract("{}", "$[0]")  = "{}"'.format(col_name,additional_pos_where[i])
                                    where.append(search_pattern)

                        if sentiment:
                            where.append(u"polarity LIKE '%{}%'".format(sentiment))
                        yield where

                    return 


                else:
                    if syntagma_type == "pos":
                        #p((inp_syntagma_splitted, inp_syntagma_unsplitted))
                        self.logger.error("To get Where Expression without context for SyntagmaType='pos' is not possible. ")
                        #return False
                        #yield False
                        return
                    syntagma_tag ='stemmed' if stemmed_search else "syntagma"
                    syntagma_qeary = u"{}= '{}'".format(syntagma_tag,inp_syntagma_unsplitted)
                    #p([syntagma_qeary], "[syntagma_qeary]")
                    #return [syntagma_qeary]
                    yield syntagma_qeary
                    return 

            except (UnicodeDecodeError, UnicodeEncodeError):
                convert = True

            





    def _is_syntagma_scope_right(self, scope_num):
        #self._context_left
        #self._context_lenght
        if scope_num > self._avaliable_scope:
            #self.logger.error("")
            return False
        else:
            return True





    def _preprocess_syntagma(self, inp_syntagma,thread_name="Thread0", syntagma_type="lexem",stemmed_search=False):

        #p(inp_syntagma,"inp_syntagma")
        #p((inp_syntagma), "11")
        try:
            inp_syntagma = [token.decode("utf-8") for token in inp_syntagma]
        except:
            pass

        #p((inp_syntagma), "22")
        if not isinstance(inp_syntagma, (list,tuple)):
            self.logger.error("Given inp_syntagma ('{}') is from an un-support type ('{}')".format(inp_syntagma, type(inp_syntagma)))
            return False
        if syntagma_type == "lexem":
            #p((self._case_sensitiv),"self._case_sensitiv")
            if not self._case_sensitiv:
                inp_syntagma = [token.lower() for token in inp_syntagma]
            inp_syntagma = [self.preprocessors[thread_name]["rle"].del_rep(token) for token in inp_syntagma]
            
        #p((inp_syntagma))
        if stemmed_search:
            inp_syntagma = [self.stemm(word) for word in inp_syntagma]
        return inp_syntagma
        #p(inp_syntagma,"inp_syntagma")
        #if not self._case_sensitiv:
        #    inp_syntagma = [token.lower() for token in inp_syntagma]


    def _check_settings_for_force_cleaning(self):
        temp_force_cleaning = False
        if self._corp_info["case_sensitiv"] is True and self._case_sensitiv is False:
            temp_force_cleaning = True
        elif self._corp_info["case_sensitiv"] is False and self._case_sensitiv is True:
            self.logger.error("Current CorpDB was lower_cased. And  StatdDB was initialized with sensitive case. Because tt is not possible any more to reconstruct the case back, this operation is illegal. Please change setting and try one more time.")
            return False

        if self._corp_info["del_url"] is False and self._ignore_url is True:
            temp_force_cleaning = True


        if self._corp_info["del_punkt"] is False and self._ignore_punkt is True:
            temp_force_cleaning = True


        if self._corp_info["del_num"] is False and self._ignore_num is True:
            temp_force_cleaning = True


        if self._corp_info["del_mention"] is False and self._ignore_mention is True:
            temp_force_cleaning = True


        if self._corp_info["del_hashtag"] is False and self._ignore_hashtag is True:
            temp_force_cleaning = True


        if temp_force_cleaning:
            self.statsdb.update_attr("force_cleaning", True)
            self.set_all_intern_attributes_from_db() 
            if self._force_cleaning is not True:
                self.logger.error("Force_cleaning-Option wasn't activated.")
                return False
        else:
            self.statsdb.update_attr("force_cleaning", False)
            self.set_all_intern_attributes_from_db() 

        return True   



    ###########################Setters####################

#_drop_created_indexes
    def compute(self,inp_corp, stream_number=1, datatyp="dict", 
                adjust_to_cpu=True,min_files_pro_stream=1000,cpu_percent_to_get=50, 
                thread_name="Thread0", create_indexes=True, freeze_db=False,
                drop_indexes=True,optimized_for_long_syntagmas=True,
                baseline_insertion_border=1000000):
        if not self._check_stats_db_should_exist():
            return False
        #p(stream_number, "stream_number")
        if not self._check_db_should_be_an_stats():
            return False

        #self._baseline_intime_insertion_till = baseline_intime_insertion_till
        try:
            if not isinstance(inp_corp, Corpus):
                self.logger.error("Given InpObject is not from Corpus type. Insert was aborted!")
                return False

            if self.statsdb.get_attr("locked"):
                self.logger.error("Current DB is still be locked. Possibly it in ht now fr in-useom other process or la thest computation process is failed.")
                return False
            self.statsdb.update_attr("locked", True)
            self._init_compution_variables()
            if  self._db_frozen: ## insert "db_frozen" as attribute to the StatsDB!!!
               msg = "Current StatsDB is closed for new Insertions because it  was already SizeOptimized and all temporary Data was deleted"
               self.logger.error(msg)
               self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
               self._terminated = True
               return False

            if drop_indexes:
                self._drop_created_indexes()

            self._init_compution_variables()

            self.corp = inp_corp
            self._corp_info  = self.corp.info()
            self._text_field_name = self._corp_info["text_field_name"]
            self._id_field_name =  self._corp_info["id_field_name"]

            self.statsdb.update_attr("pos_tagger",self._corp_info["pos_tagger"])
            self.statsdb.update_attr("sentiment_analyzer",self._corp_info["sentiment_analyzer"])
            self._pos_tagger = self._corp_info["pos_tagger"]
            self._sentiment_analyzer = self._corp_info["sentiment_analyzer"]


            self._compute_cleaning_flags()
            #p(self.force_cleaning_flags, "self.force_cleaning_flags")
            #p(self._force_cleaning, "self._force_cleaning")
            if not self._check_settings_for_force_cleaning():
                return False
            #p(self._force_cleaning, "self._force_cleaning")


            if not self._language:
                self.statsdb.update_attr("language",self._corp_info["language"])
            else:
                if self._language != self._corp_info["language"]:
                    self.logger.error("StatsDB language ('{}') is not equal to the inserting CorpDB ('{}'). Those meta data should be equal for staring the insertion process. Please select other corpus, which you want to insert to the current statsDB or initialize a new StatsDB with right language.".format(self._language, self._corp_info["language"]))
                    return False

            #p(self._corpus_id, "self._corpus_id")
            if not self._corpus_id:
                self.statsdb.update_attr("corpus_id", self._corp_info["id"])
                self.set_all_intern_attributes_from_db()

            else:
                if self._corpus_id != self._corp_info["id"]:
                    self.logger.error("Current StatdDb was already computed/initialized for Corpus with id '{}'. Now you try to insert Corpus with id '{}' and it is not allow.".format(self._corpus_id,self._corp_info["id"]))
            #p(self._corpus_id, "self._corpus_id")

            self._init_stemmer(self._corp_info["language"])
            
            #self.status_bars_manager =  self._get_status_bars_manager()

            ##### Status-Bar - Name of the processed DB
            if self._status_bar:
                # print "\n"
                if self._in_memory:
                    dbname = ":::IN-MEMORY-DB:::"
                else:
                    dbname = '{}'.format(self.statsdb.fname())
                status_bar_starting_corpus_insertion = self._get_new_status_bar(None, self.status_bars_manager.term.center( dbname) , "", counter_format=self.status_bars_manager.term.bold_white_on_blue("{fill}{desc}{fill}"))
                status_bar_starting_corpus_insertion.refresh()



            if adjust_to_cpu:
                stream_number= get_number_of_streams_adjust_cpu( min_files_pro_stream, inp_corp.corpdb.rownum("documents"), stream_number, cpu_percent_to_get=cpu_percent_to_get)
                if stream_number is None or stream_number==0:
                    #p((self._get_number_of_left_over_files(),self.counter_lazy_getted),"self._get_number_of_left_over_files()")
                    self.logger.error("Number of input files is 0. Not generators could be returned.", exc_info=self._logger_traceback)
                    return []

            streams= self.get_streams_from_corpus(inp_corp, stream_number, datatyp=datatyp)
            #p(streams, "streams")
            ## threads
            if self._status_bar:
                status_bar_threads_init = self._get_new_status_bar(len(streams), "ThreadsStarted", "threads")
            
            #p((stream_number, len(streams)))
            #i=1
            self._threads_num = len(streams)
            if self._threads_num>1:
                if self._status_bar:
                    unit = "rows"
                    self.main_status_bar_of_insertions = self._get_new_status_bar(0, "AllThreadsTotalInsertions", unit)
                    self.main_status_bar_of_insertions.refresh()
                    #self.main_status_bar_of_insertions.total = 0
            else: 
                self.main_status_bar_of_insertions = False


            for stream in streams:
                gen = stream[1]
                if not self._isrighttype(gen):
                    self.logger.error("StatsComputationalError: Given InpData not from right type. Please give an list or an generator.", exc_info=self._logger_traceback)
                    return False
                #p(gen)

                thread_name = stream[0]
                processThread = threading.Thread(target=self._compute, args=(gen,datatyp,  thread_name,baseline_insertion_border), name=thread_name)
                processThread.setDaemon(True)
                processThread.start()
                self.active_threads.append(processThread)
                if self._status_bar:
                    status_bar_threads_init.update(incr=1)
                #i+=1
                time.sleep(1)

            self.logger.info("'{}'-thread(s) was started. ".format(len(self.active_threads)))

            time.sleep(3)

            if not self._wait_till_all_threads_are_completed("Compute"):
                return False


            self.statsdb._write_cashed_insertion_to_disc(with_commit=True)



            ## save attributes from the main counter
            if self._status_bar:
                if self.main_status_bar_of_insertions:
                    self.counters_attrs["compute"]["start"] = self.main_status_bar_of_insertions.start
                    self.counters_attrs["compute"]["end"] = self.main_status_bar_of_insertions.last_update
                    self.counters_attrs["compute"]["total"] = self.main_status_bar_of_insertions.total
                    self.counters_attrs["compute"]["desc"] = self.main_status_bar_of_insertions.desc
                else:
                    self.counters_attrs["compute"] = False


            #self._print_summary_status()

            inserted_repl = self.statsdb.rownum("replications")
            inserted_redu = self.statsdb.rownum("reduplications")
            uniq_syntagma_in_baseline = self.statsdb.rownum("baseline")

            if self._status_bar:
                status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("Repl:'{}'; Redu:'{}'; UniqSyntagmaBaseline: '{}'.".format(inserted_repl, inserted_redu,uniq_syntagma_in_baseline ) ), "",  counter_format=self.status_bars_manager.term.bold_white_on_blue('{fill}{desc}{fill}\n'))
                status_bar_total_summary.refresh()
                self.status_bars_manager.stop()
                #print "\n"

            if not self._status_bar:
                self.logger.info("Current StatsDB has '{}' rows in the Replications Table; '{}' rows in the Reduplications Table;'{}' rows in the Baseline Table; ".format(inserted_repl,inserted_redu,uniq_syntagma_in_baseline))
            else:
                self.logger.debug("Current StatsDB has '{}' rows in the Replications Table; '{}' rows in the Reduplications Table;'{}' rows in the Baseline Table; ".format(inserted_repl,inserted_redu,uniq_syntagma_in_baseline))
            #self.logger.info("Current StatsDB has '{}' rows in the Reduplications Table.".format(inserted_redu))
            #self.logger.info("Current StatsDB has '{}' rows in the Baseline Table.".format(uniq_syntagma_in_baseline))


            self._last_insertion_was_successfull = True
            self._end_time_of_the_last_insertion = time.time()



            self.statsdb._commit()
            if create_indexes:
                self.statsdb.init_default_indexes(thread_name=thread_name)
                self.create_additional_indexes(optimized_for_long_syntagmas=optimized_for_long_syntagmas)
                self.statsdb._commit()

            if not self._check_baseline_consistency():
                self.logger.error("StatsDBCorrupt: Current StatsDB is inconsistent.")
                return False

            if freeze_db:
                self.optimize_db(stream_number=stream_number, min_row_pro_sream=min_files_pro_stream)

            self.statsdb._commit()
            self._compute_baseline_sum()

            if not self._check_statsdb_consistency():
                self.logger.error("StatsDBCorrupt: Current StatsDB is inconsistent.")
                return False
            
            if len(self.threads_unsuccess_exit) >0:
                self.logger.error("StatsComputational process is failed. (some thread end with error)")
                raise ProcessError, "'{}'-Threads end with an Error.".format(len(self.threads_unsuccess_exit))
                #self.statsdb.update_attr("locked", False)
                return False
            else:
                self.logger.info("StatsComputational process end successful!!!")
                self.statsdb.update_attr("locked", False)
                self.statsdb._commit()
                return True

        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("ComputeError: See Exception: '{}'. ".format(e), exc_info=self._logger_traceback)
            self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
        except KeyboardInterrupt:
            self.logger.warning("KeyboardInterrupt: Process was stopped from User. Some inconsistence in the current DB may situated.")
            sys.exit()
           


    def _compute(self, inp_data, datatyp="dict",  thread_name="Thread0",  baseline_insertion_border=1000000,add_also_repeted_redu_to_baseline=True):
        try:
            if not self._check_corp_should_exist():
                self._terminated = True
                msg = "StatsObj wasn't found."
                self.logger.error(msg)
                self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
                return False

            if not self._corp_info:
                self._terminated = True
                msg = "CorpInfo wasn't found."
                self.logger.error(msg)
                self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
                return False 

            status_bar_insertion_in_the_current_thread = self._initialisation_computation_process( inp_data,  thread_name=thread_name, )
            
            if self._status_bar:
                if not  status_bar_insertion_in_the_current_thread: return False

            self.logger.debug("_ComputationalProcess: Was started for '{}'-Thread. ".format(thread_name))
            i = 0
            for doc_elem in inp_data:
                self._check_termination(thread_name=thread_name)
                i+= 1
                if self._status_bar:
                    status_bar_insertion_in_the_current_thread.update(incr=1)
                    if self.main_status_bar_of_insertions:
                        self.main_status_bar_of_insertions.update(incr=1)

                text_elem = json.loads(doc_elem[1])
                #p((sum([len(s[0]) for s in  text_elem]), "doc_elem"))
                if self._force_cleaning:
                    text_elem  = self._preprocess(text_elem,thread_name=thread_name)
                #p(text_elem, c="m")

                ### Extraction 
                extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container = self.extract_replications(text_elem, thread_name=thread_name)
                #p((extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container), "REPLS")
                
                extracted_redu_in_text_container, redu_free_text_container, mapping_redu = self.extract_reduplications(repl_free_text_container, rle_for_repl_in_text_container, thread_name=thread_name)
                #p((extracted_redu_in_text_container, redu_free_text_container, mapping_redu), "REDUS")
                
                computed_baseline = self.compute_baseline(redu_free_text_container,extracted_redu_in_text_container)
                stemmed_text_container = [[self.stemm(token) for token in sent] for sent in redu_free_text_container]
                
                #p(stemmed_text_container, "stemmed_text_container")
                ### Insertion

                self.insert_repl_into_db(doc_elem,text_elem,extracted_repl_in_text_container, repl_free_text_container,rle_for_repl_in_text_container,redu_free_text_container,mapping_redu,stemmed_text_container, thread_name=thread_name)
                self.insert_redu_into_db(doc_elem,text_elem,extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container, mapping_redu,stemmed_text_container,thread_name=thread_name)

                #if "@ronetejaye" in [t for sent in redu_free_text_container for t in sent]:
                #    p((doc_elem,redu_free_text_container,repl_free_text_container), "doc_elem")
                
                with self.locker:
                    self.baseline_lazyinsertion_into_db(computed_baseline,extracted_redu_in_text_container,baseline_insertion_border=baseline_insertion_border,thread_name=thread_name)

            self._write_repl_into_db(thread_name=thread_name)
            self._write_redu_into_db(thread_name=thread_name)        

            with self.locker:
                self.baseline_insert_left_over_data(thread_name=thread_name)


            if self._status_bar:
                status_bar_insertion_in_the_current_thread.refresh()
                self.counters_attrs["_compute"][thread_name]["start"] = status_bar_insertion_in_the_current_thread.start
                self.counters_attrs["_compute"][thread_name]["end"] = status_bar_insertion_in_the_current_thread.last_update
                self.counters_attrs["_compute"][thread_name]["total"] = status_bar_insertion_in_the_current_thread.total
                self.counters_attrs["_compute"][thread_name]["desc"] = status_bar_insertion_in_the_current_thread.desc
                status_bar_insertion_in_the_current_thread.close(clear=False)


            self.threads_status_bucket.put({"name":thread_name, "status":"done"})
            self.logger.debug("_Compute: '{}'-Thread is done and was stopped.".format(thread_name))
            return True


        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            msg = "_ComputeError: See Exception: '{}'. ".format(e)
            self.logger.error(msg, exc_info=self._logger_traceback)
            self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
            self.statsdb.rollback()
            return False



    def _check_termination(self, thread_name="Thread0"):
        if self._terminated:
            self.logger.critical("'{}'-Thread was terminated.".format(thread_name))
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            sys.exit()


    def _get_occur(self,counted_rep, scope=1,splitted_syntagma=False):
        if scope>1:
            #if
            occur_uniq = defaultdict(lambda:0)
            occur_rep_exhausted = defaultdict(lambda:0)
            for word, word_data in counted_rep.iteritems():
                for doc_id, doc_data in word_data.iteritems():
                    for rep_count in doc_data.values():
                        occur_uniq[word] += 1
                        occur_rep_exhausted[word] += rep_count
            if splitted_syntagma:
                occur_uniq_output = ()
                occur_e_output = ()
                #tuple(occur_uniq[word] for word in splitted_syntagma )
                for word in splitted_syntagma:
                    occur_uniq_output += (occur_uniq[word],)
                    occur_uniq[word] = "IGNOR"
                    occur_e_output += (occur_rep_exhausted[word],)
                    occur_rep_exhausted[word] = "IGNOR"

                return (occur_uniq_output,occur_e_output)
            else:
                return (sum(occur_uniq.values()),sum(occur_rep_exhausted.values()) )
        else:
            occur_uniq = 0
            occur_rep_exhausted = 0
            for doc_id, doc_data in counted_rep.iteritems():
                for rep_count in doc_data.values():
                    occur_uniq += 1
                    occur_rep_exhausted += rep_count
            return (occur_uniq,occur_rep_exhausted)





    def _insert_temporized_sum_into_baseline_table_in_db(self,temporized_sum,tables_name, ):
        placeholders = " ,".join(["?" for i in range(len(temporized_sum[0]))])
        qeary = """
        INSERT OR REPLACE INTO {} VALUES ({});
        """
        self.statsdb._threads_cursors["sum_inserter"].executemany(qeary.format(tables_name,placeholders), temporized_sum)




    def recompute_syntagma_repetativity_scope(self, full_repetativ_syntagma,_check_statsdb_consistency=True):
        values_from_db = self.statsdb.get_attr("full_repetativ_syntagma")
        if full_repetativ_syntagma not in [True, False]:
            self.logger.error("A non-boolean symbol ('{}') was given as full_repetativ_syntagma-Option. ".format(full_repetativ_syntagma))
            return False

        if full_repetativ_syntagma == values_from_db:
            self.logger.warning("There is nothing to recompute. Values for 'full_repetativ_syntagma' was given: '{}' and values in  StatsDB is '{}'.".format(full_repetativ_syntagma, values_from_db))
            return False

        # if self._full_repetativ_syntagma and self._db_frozen and full_repetativ_syntagma == False:
        #     self.logger.warning("Recomputing from True->False is failed!!! Because this StatsDB was already optimized and all not-full-repetativ-syntagmas was already deleted during this process.")
        #     return False
        if self.statsdb.get_attr("locked"):
                        self.logger.error("Current DB is still be locked. Possibly it in ht now fr in-useom other process or la thest computation process is failed.")
                        return False

        self.statsdb.update_attr("locked", True)

        
                
        self.statsdb.update_attr("full_repetativ_syntagma", full_repetativ_syntagma)
        self.set_all_intern_attributes_from_db()

        if self._compute_baseline_sum():
            self.logger.info("StatsDB FullSyntagmaRepetativnes was recompute with success.")
            

        if _check_statsdb_consistency:
            if not self._check_baseline_consistency():
                self.logger.error("StatsDBCorrupt: Current StatsDB is inconsistent.")
                return False

            if not self._check_statsdb_consistency():
                self.logger.error("StatsDBCorrupt: Current StatsDB is inconsistent.")
                return False

        else:
            self.logger.error("FullRepetativnes wasn't recompute.")
            return False


        self.statsdb.update_attr("locked", False)
        return True
        #self.statsdb.update_attr("full_repetativ_syntagma", full_repetativ_syntagma)
        




    def _compute_baseline_sum(self, insertion_border=10000, thread_name="Thread0",size_to_fetch=10000, ):
        if not self._check_stats_db_should_exist():
            return False

        if self._status_bar:
            try:
                if not self.status_bars_manager.enabled:
                    self.status_bars_manager = self._get_status_bars_manager()
            except:
                self.status_bars_manager = self._get_status_bars_manager()

            status_bar_start = self._get_new_status_bar(None, self.status_bars_manager.term.center("RepetitionSummarizing") , "", counter_format=self.status_bars_manager.term.bold_white_on_cyan("{fill}{desc}{fill}"))
            status_bar_start.refresh()
            status_bar_current = self._get_new_status_bar(self.statsdb.rownum("baseline"), "Processed:", "syntagma")

        # ### compute syntagmas to delete
        counter_summerized = 0
        temporized_sum = []
        temp_rep = defaultdict()


        minimum_columns = False
        syntagma_type = "lexem"
        indexes = self.col_index_min if minimum_columns else self.col_index_orig

        #### Compute indexes
        ix_repl = indexes["repl"]
        ix_redu = indexes["redu"]

        ix_word_redu = ix_redu['normalized_word']
        ix_word_repl = ix_repl['normalized_word']
        ix_token_redu = ix_redu["index_in_corpus"]
        ix_token_repl = ix_repl["index_in_corpus"]
        ix_length_redu = ix_redu["redu_length"]
        #ix_in_redu_repl = ix_repl["in_redu"]
        ix_doc_id_redu = ix_redu["doc_id"]
        ix_doc_id_repl = ix_repl["doc_id"]

        row_num_bevore = self.statsdb.rownum("baseline") +1000
        #for i, baseline_container in enumerate(self._baseline("*",max_scope=False, split_syntagma=False,thread_name="baseline_getter")):
        #gen = self.statsdb.lazyget("baseline", thread_name="baseline_sum")
        # def intern_gen():
        #     gen = self.statsdb._threads_cursors["baseline_getter"].execute("SELECT * FROM baseline;") #lazyget("baseline", thread_name="baseline_sum")
        #     while True:
        #         results = gen.fetchmany(size_to_fetch)
        #         results = list(results)
        #         if not results:
        #             break

        #         for row in results:
        #             yield row
        ### create_temp_table
        #self.statsdb._threads_cursors["baseline_creater"].execute("CREATE TABLE 'temp_baseline' AS SELECT sql FROM sqlite_master WHERE type='table' AND name='baseline'" ).fetchall()
        self.statsdb._commit()
        self._temp_baseline_name = "_baseline"
        status = self.statsdb.addtable(self._temp_baseline_name, db_helper.default_columns_and_types_for_stats_baseline ,constraints= db_helper.default_constraints_for_stats_baseline)
        self.statsdb._commit()


        for i, baseline_container in enumerate(self.statsdb.lazyget("baseline", thread_name="baseline_sum")):
            if i >row_num_bevore:
               self.logger.error("InvalidState: BaselineGetter send more items as need. Script is failed! ( Probably an ImplementationsError. Please contact Egor Savin: ego@savin.berlin) ")
               sys.exit()
                #return 
            #p(baseline_container, "baseline_container")
            if self._status_bar:
                status_bar_current.update(incr=1)
            #inp_syntagma =  self._preprocess_syntagma(inp_syntagma,thread_name=thread_name, syntagma_type=syntagma_type)
            unsplitted_syntagma = baseline_container[0]
            splitted_syntagma = unsplitted_syntagma.split(self._baseline_delimiter)
            #p(baseline_container,"baseline_container")
            scope = len(splitted_syntagma)
            where = tuple(self._get_where_statement(splitted_syntagma,scope=scope,thread_name=thread_name,
                                             with_context=True,syntagma_type="lexem"))#, splitted_syntagma=splitted_syntagma)
            if not where: return False

            repls_container = self.get_reps("repl",splitted_syntagma,scope,where,indexes,thread_name=thread_name,return_full_tuple=True,
                                delete_duplicates=False,syntagma_type=syntagma_type, minimum_columns=minimum_columns)
            
            redus_container = self.get_reps("redu",splitted_syntagma,scope,where,indexes,thread_name=thread_name,return_full_tuple=True,
                                delete_duplicates=False,syntagma_type=syntagma_type, minimum_columns=minimum_columns)
            
            temp_baseline_row = baseline_container[:4]
            
            #p((repls_container, redus_container, temp_baseline_row))
            if repls_container or redus_container:
                counter_summerized += 1

            occur_full_syn_repl = None
            occur_full_syn_redu = None
            if scope==1:
                if repls_container:
                    repls =repls_container[0]
                    temp_repl = defaultdict(lambda:defaultdict(int))
                    for repl in repls:
                        temp_repl[repl[ix_doc_id_repl]][repl[ix_token_repl]] += 1
                    occur = self._get_occur(temp_repl)
                    temp_baseline_row += occur
                    occur_full_syn_repl = occur[0]

                else:
                    temp_baseline_row += (None,None)

                if redus_container:    
                    redus = redus_container[0]
                    temp_redu = defaultdict(lambda:defaultdict(int))
                    for redu in redus:
                        temp_redu[redu[ix_doc_id_redu]][redu[ix_token_redu]] += redu[ix_length_redu]

                    occur = self._get_occur(temp_redu)
                    temp_baseline_row += occur
                    occur_full_syn_redu = occur[0]

                else:
                    temp_baseline_row += (None,None)

                temp_baseline_row += (occur_full_syn_repl,occur_full_syn_redu)


            else:
                occur_full_syn_repl = None
                occur_full_syn_redu = None
                #p((baseline_container[0],data),"data")
                if repls_container:
                    repls =repls_container[0]
                    #p(repls_container, "repls_container")
                    counted_repls = defaultdict(lambda:defaultdict(lambda:defaultdict(int)))
                    for repl in repls:
                        #p(repl[3], "repl[3]")
                        counted_repls[repl[ix_word_repl]][repl[ix_doc_id_repl]][repl[ix_token_repl]] += 1 #. if not in_redu, that each repl will be counted
                    #p(counted_repls,"counted_repls")
                    temp_baseline_row += self._get_occur(counted_repls,scope=scope,splitted_syntagma=splitted_syntagma)
                    occur_full_syn_repl = repls_container[2] if repls_container[1] else None


                else:
                    temp_baseline_row += (None,None)

                if redus_container:
                    redus = redus_container[0]
                    counted_redus = defaultdict(lambda:defaultdict(lambda:defaultdict(int)))
                    for redu in redus:
                        counted_redus[redu[ix_word_redu]][redu[ix_doc_id_redu]][redu[ix_token_redu]] += redu[ix_length_redu]
                    #p(counted_redus, "counted_redus")
                    temp_baseline_row += self._get_occur(counted_redus,scope=scope,splitted_syntagma=splitted_syntagma)
                    occur_full_syn_redu = redus_container[2] if redus_container[1] else None

                else:
                    temp_baseline_row += (None,None)

                temp_baseline_row += (occur_full_syn_repl, occur_full_syn_redu)

            temporized_sum.append(db_helper.values_to_list( temp_baseline_row, "one"))
            #self.statsdb._threads_cursors["sum_inserter"].execute(qeary.format(self._temp_baseline_name,placeholders), db_helper.values_to_list( temp_baseline_row, "one") )

            if len(temporized_sum) > self._lazyness_border:
                self._insert_temporized_sum_into_baseline_table_in_db(temporized_sum,self._temp_baseline_name)
                temporized_sum = []


        if len(temporized_sum) > 0:
            self._insert_temporized_sum_into_baseline_table_in_db(temporized_sum,self._temp_baseline_name)
            temporized_sum = []


        self.statsdb._threads_cursors["baseline_creater"].execute("DROP  TABLE {};".format("baseline") )
        self.statsdb._commit()
        self.statsdb._threads_cursors["baseline_creater"].execute("ALTER TABLE {} RENAME TO baseline;".format(self._temp_baseline_name) )  #  #
        self.statsdb._commit()
        self.statsdb._update_temp_indexesList_in_instance(thread_name=thread_name)
        #self.statsdb._update_database_pragma_list(thread_name=thread_name)
        self.statsdb._update_pragma_table_info(thread_name=thread_name)
        self.statsdb._update_temp_tablesList_in_instance(thread_name=thread_name)


        if self._status_bar:
            status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("Syntagmas: Processed:'{}'; Summerized:'{}';".format(status_bar_current.count, counter_summerized) ), "",  counter_format=self.status_bars_manager.term.bold_white_on_cyan('{fill}{desc}{fill}\n'))
            status_bar_total_summary.refresh()
            self.status_bars_manager.stop()




        if counter_summerized > 0:
            self.logger.info("All Syntagmas was counted and summerized.")
            return counter_summerized
        else:
            self.logger.info("No one Syntagmas summerized.")
            return False



    def _set_rle(self,  thread_name="Thread0"):
        try:
            self.logger.debug("INIT-RLE: Start the initialization of Run_length_encoder for '{}'-Thread.".format(thread_name))
            self.preprocessors[thread_name]["rle"] = Rle(self.logger)
            self.logger.debug("INIT-RLE: Run_length_encoder for '{}'-Thread was initialized.".format(thread_name))
            return True
        except Exception, e:
            self.logger.error("Exception was encountered: '{}'. ".format(e), exc_info=self._logger_traceback)
            return False

    def _init_preprocessors(self, thread_name="Thread0"):
        try:

            if not self._set_rle(thread_name):
                self.logger.error("RLE in '{}'-Thread wasn't initialized. Script will be aborted.".format(thread_name), exc_info=self._logger_traceback)
                self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
                return False

            # if self._status_bar:
            #     status_bar_preprocessors_init = self._get_new_status_bar(1, "{}:PreprocessorsInit".format(thread_name), "unit")


            # if self._set_rle(thread_name):
            #     if self._status_bar:
            #         status_bar_preprocessors_init.update(incr=1)
            #         status_bar_preprocessors_init.refresh()
            # else:
            #     status_bar_preprocessors_init.total -= 1
            #     self.logger.error("RLE in '{}'-Thread wasn't initialized. Script will be aborted.".format(thread_name), exc_info=self._logger_traceback)
            #     self.threads_status_bucket.put({"name":thread_name, "status":"failed"})
            #     return False



            # if self._status_bar:
            #     self.counters_attrs["_init_preprocessors"][thread_name]["start"] = status_bar_preprocessors_init.start
            #     self.counters_attrs["_init_preprocessors"][thread_name]["end"] = status_bar_preprocessors_init.last_update
            #     self.counters_attrs["_init_preprocessors"][thread_name]["total"] = status_bar_preprocessors_init.total
            #     self.counters_attrs["_init_preprocessors"][thread_name]["desc"] = status_bar_preprocessors_init.desc

            self.logger.debug("PreprocessorsInit: All Preprocessors for '{}'-Thread was initialized.".format(thread_name))
            return True
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("PreprocessorsInitError: See Exception: '{}'. ".format(e), exc_info=self._logger_traceback)
            return False



    def _compute_cleaning_flags(self):
        if not self.force_cleaning_flags:
            if not self._corp_info["del_url"]:
                if self._ignore_url:
                    self.force_cleaning_flags.add("URL")

            if not self._corp_info["del_hashtag"]:
                if self._ignore_hashtag:
                    self.force_cleaning_flags.add("hashtag")

            if not self._corp_info["del_mention"]:
                if self._ignore_mention:
                    self.force_cleaning_flags.add("mention")

            if not self._corp_info["del_punkt"]:
                if self._ignore_punkt:
                    self.force_cleaning_flags.add("symbol")

            if not self._corp_info["del_num"]:
                if self._ignore_num:
                    self.force_cleaning_flags.add("number")
         # = {
         #                        "number":":number:",
         #                        "URL":":URL:",
         #                        "symbol":":symbol:",
         #                        "mention":":mention:",
         #                        "hashtag":":hashtag:",
         #                    }



    def _preprocess(self, text_elem,thread_name="Thread0"):
        #p(text_elem, "text_elem", c="r")
        #time.sleep(3)
        #p(text_elem, "text_elem")
        new_text_elem = []
        for sent_container in text_elem:
            #p(sent_container, "sent_container")
            sent = sent_container[0]
            #p(sent, "sent")
            sentiment = sent_container[1]
            #categories = get_categories([token[0] for token in sent])
            #p(categories, "categories")
            temp_sent = []
            #i = -1å
            for token_container in sent:
                #p(token_container, "token_container")
                #i+=1
                categorie = token_container[1]
                if categorie in self.force_cleaning_flags:
                    if self._log_ignored:
                        self.logger.outsorted_stats("Following Token was ignored: '{}'. Reason: 'It is an URL'.".format(token_container))
                        #indexes_to_del.append((index_level_1, index_level_2, index_level_3))
                    temp_sent.append((None,self._cleaned_tags[categorie]))
                    continue

                #p(token_container)
                if not self._case_sensitiv:
                    temp_sent.append((token_container[0].lower(), token_container[1]))
                else:
                    temp_sent.append(token_container)
                #p([token_container[0],token_container[1], i])
                #p(temp_sent, "temp_sent")

            new_text_elem.append((temp_sent, sentiment))
            #p((temp_sent), "temp_sent", c="r")

        self.logger.debug("Text-Cleaning for current text_elem is done.")
        #p(new_text_elem, "new_text_elem",c="r")
        #sys.exit()
        return new_text_elem


    def extract_reduplications(self,repl_free_text_container,rle_for_repl_in_text_container, thread_name="Thread0"):
        #self.logger.low_debug("ReduExtraction was started")
        extracted_redu_in_text_container = []
        redu_free_text_container = []
        text_elem_mapping = []
        mapping_redu = []
        #p(text_elem, "text_elem")
        #p(repl_free_text_container, "repl_free_text_container")
        sent_index = -1
        #total_sent_number = len(repl_free_text_container)
        #p(total_sent_number,"total_sent_number")
        for sent in repl_free_text_container:
            ########### SENTENCE LEVEL ##################

            sent_index+= 1
            #p(sent, "sent")
            repl_in_tuples, mapped = self.preprocessors[thread_name]["rle"].encode_to_tuples(sent,mapping=True)
            #p(repl_in_tuples, "repl_in_tuples")
            extracted_reps, rep_free_sent = self.preprocessors[thread_name]["rle"].rep_extraction_sent(repl_in_tuples,mapped)
            #redu_free_index = -1
            for rep in  extracted_reps:
                #redu_free_index += 1
                start_index = rep['start_index_in_orig']
                length = rep['length']
                i_redu_free = rep["index_in_redu_free"]
                repl_free_range = repl_free_text_container[sent_index][start_index:start_index+length]
                rle_range = rle_for_repl_in_text_container[sent_index][start_index:start_index+length]
                addit_info = []
                #p((, ))
                #p(repl_free_range, "repl_free_range")
                #p(rle_range, "rle_range")

                addit_info = [r if r else o for o,r in zip(repl_free_range,rle_range)]
                #addit_info = [r if (r,o[1]) else o for o,r in zip(orig_range,rle_range)]

                #p(addit_info, "addit_info", c="r")
                counts = Counter(addit_info)
                #p(counts, "counts")
                rep_free_sent[i_redu_free] = (rep_free_sent[i_redu_free], dict(counts))

            #p((extracted_reps, rep_free_sent), c="r")
            #p(rep_free_sent, "rep_free_sent")
            extracted_redu_in_text_container.append(extracted_reps)
            redu_free_text_container.append(rep_free_sent)
            mapping_redu.append(mapped)
            #sys.exit()
        #self.logger.low_debug("ReduExtraction was finished")
        return extracted_redu_in_text_container, redu_free_text_container, mapping_redu






    def extract_replications(self, text_elem, thread_name="Thread0"):
        #self.logger.low_debug("ReplExtraction was started")
        repl_free_text_container = []
        rle_for_repl_in_text_container = []
        extracted_repl_in_text_container = []

        #p(text_elem)
        sent_index = -1
        total_sent_number = len(text_elem)
        for sent_container in text_elem:
            ########### SENTENCE LEVEL ##################
            repl_free_text_container.append([])
            rle_for_repl_in_text_container.append([])
            extracted_repl_in_text_container.append([])
            sent_index+= 1
            
            #p((type(sent_container),sent_container), "sent_container_in_repl_extr")
            try:
                sent = sent_container[0]
                sentiment = sent_container[1]
            except Exception as e:
                #p(sent_container, "sent_container")
                self._terminated = True
                msg = "Given SentContainer has wrong structure! SentContainer: '{}'; Exception: '{}'.".format(sent_container,e)
                self.logger.error(msg)
                self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
                return False

            if not self._case_sensitiv:
                sent = [[token_container[0].lower(), token_container[1]]  if token_container[0] else token_container  for token_container in sent ]

            temp_sent = []
            token_index = -1
            for token_container in sent:
                token_index+=1
                try:
                    token = token_container[0]
                    pos = token_container[1]
                    #nr_of_token_in_sent = token_index
                except Exception, e:
                    #p(sent_container, "sent_container")
                    self._terminated = True
                    msg = "Given TokenContainer has wrong structure! '{}'.".format(token_container)
                    self.logger.error(msg)
                    self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
                    return False

                if  pos not in self.ignored_pos:

                    if token:
                        repl_in_tuples = self.preprocessors[thread_name]["rle"].encode_to_tuples(token)
                        extracted_reps, rep_free_word,rle_word = self.preprocessors[thread_name]["rle"].rep_extraction_word(repl_in_tuples, get_rle_as_str=True)
                        #p((repl_in_tuples,extracted_reps, rep_free_word,rle_word))
                    else:
                        #p((pos, token))
                        rep_free_word = pos
                        extracted_reps = None

                    
                    repl_free_text_container[sent_index].append(rep_free_word)

                    if extracted_reps:
                        #p((extracted_reps, rep_free_word,rle_word),c="r")
                        rle_for_repl_in_text_container[sent_index].append(rle_word)
                        extracted_repl_in_text_container[sent_index].append(extracted_reps)
                    else:
                        rle_for_repl_in_text_container[sent_index].append("")
                        extracted_repl_in_text_container[sent_index].append("")
                else:
                    repl_free_text_container[sent_index].append(token)
                    rle_for_repl_in_text_container[sent_index].append("")
                    extracted_repl_in_text_container[sent_index].append("")

                #p((sent_index,token_index, repl_free_text_container[sent_index][token_index],rle_for_repl_in_text_container[sent_index][token_index] ,extracted_repl_in_text_container[sent_index][token_index]))
        #p(repl_free_text_container, "repl_free_text_container")
        #self.logger.low_debug("ReplExtraction was finished")
        return extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container 



    def _get_cleaned_redu_free(self, redu_free_text_container):
        inp_token_list = []
        for sent in redu_free_text_container:
            for token in sent:

                try:
                    token[1].values
                    inp_token_list.append(token[0])
                except (IndexError,AttributeError):
                    inp_token_list.append(token)
        return inp_token_list
        
    def compute_baseline(self, redu_free_text_container,extracted_redu_in_text_container):
        #self.logger.low_debug("Baseline Computation for current text-element was started")
        ## Step 1: Extract ngramm from redu and repl free text element
        inp_token_list = self._get_cleaned_redu_free(redu_free_text_container)
        computed_baseline  = []
        for n in xrange(1,self.baseline_ngramm_lenght+1):
            computed_baseline += [tuple(inp_token_list[i:i+n]) for i in xrange(len(inp_token_list)-n+1)]

        ## Step 2: Add reduplicated unigramms

        #self.logger.low_debug("Baseline Computation was finished.")
        return computed_baseline






    def baseline_insert_temporized_data(self,temporized_baseline,thread_name="Thread0"):
        try:
            #self.logger.low_debug("Insertion Process of temporized Baseline was started")
            qeary = """
                    INSERT OR REPLACE INTO baseline VALUES (
                        :0,
                        :1,
                        :2,
                        COALESCE((SELECT occur_syntagma_all FROM baseline WHERE syntagma=:0), 0) + :3,
                        NULL,NULL,NULL,NULL,NULL,NULL
                    );"""

            cursor = self.statsdb._db.cursor()

            def intern_gen():
                for syntag, count in temporized_baseline.iteritems():
                    #print syntag
                    #self.logger.error("{}".format(syntag))
                    #sys.exit()
                    yield (
                            self._baseline_delimiter.join(syntag).strip(),
                            self._baseline_delimiter.join([self.stemm(w) for w in syntag]).strip(),
                            len(syntag), 
                            count,  
                         )

            cursor.executemany(qeary, intern_gen() )
            self.logger.low_debug("Temporized Baseline was inserted into DB.")
            return True
        except Exception as e:
            self.logger.error("INsertionError: {}".format(repr(e)),  exc_info=self._logger_traceback)
            self.terminated = True
            return False


    # def baseline_intime_insertion_into_db(self,thread_name="Thread0"):
    #     temporized_baseline_to_insert = self.temporized_baseline
    #     self.temporized_baseline = defaultdict(int)
    #     thread_name = "basinsrt"
    #     if self.baseline_insrt_process:
    #         try:
    #             i = 0
    #             while True:
    #                 #a = self.baseline_insrt_process.isAlive()
    #                 #p(a, "isalive")
    #                 i += 1
    #                 if not self.baseline_insrt_process.isAlive():
    #                     self.logger.debug("Waiting is finished ->  (BaselineInsertion will be start)")
    #                     break
    #                 else:
    #                     if i >= 50:
    #                         self.logger.error("Timeout limit was reached. Probably something goes wrong!!!!")
    #                         self.terminated = True
    #                         sys.exit()
    #                     self.logger.debug("Wait till BaselineInsertion is done.")
    #                     time.sleep(1)
    #         except AttributeError:
    #             pass
    #     #p("5555")
    #     self.baseline_insrt_process = threading.Thread(target=self.baseline_insert_temporized_data, args=(temporized_baseline_to_insert, thread_name), name=thread_name)
    #     self.baseline_insrt_process.setDaemon(True)
    #     self.baseline_insrt_process.start()
    #     #time.sleep(5)


    # def baseline_insert_left_over_data(self,thread_name="Thread0"):
    #     thread_name = "basinsrt"
    #     # p("111")
    #     if self.baseline_insrt_process:
    #         # p("222")
    #         i = 0
    #         try:
    #             while True:
    #                 i += 1
    #                 #a = self.baseline_insrt_process.isAlive()
    #                 #p(a, "isalive")
    #                 if not self.baseline_insrt_process.isAlive():
    #                     self.logger.debug("Waiting is finished ->  (BaselineInsertion will be start)")
    #                     break
    #                 else:
    #                     if i >= 50:
    #                         self.logger.error("Timeout limit was reached. Probably something goes wrong!!!!")
    #                     self.logger.debug("Wait till BaselineInsertion is done.")
    #                     time.sleep(1)

    #         except AttributeError:
    #             pass
    #     #p("5555")
    #     self.baseline_insert_temporized_data(self.temporized_baseline,thread_name=thread_name)

    def temporize_baseline(self, computed_baseline,extracted_redu_in_text_container):
        #self.temporized_baseline = defaultdict(int)
        #p(computed_baseline, "computed_baseline")
        for syntagma in computed_baseline:
            #p(syntagma)
            #if "@ronetejaye" in syntagma:
            #    p(syntagma, "syntagma")
            self.temporized_baseline[syntagma] += 1

        #if add_also_repeted_redu:
        for sent in extracted_redu_in_text_container:
            for redu in sent:
                if redu:
                    #p((redu["word"],),"re_wo")
                    self.temporized_baseline[(redu["word"],)] += redu["length"]-1
                    #computed_baseline += [(redu["word"],)]*(redu["length"]-1) # -1, because 1 occur of this unigramm is already in the baseline
                    
    
        self.logger.low_debug("BaselineStats for current text-element was temporized.")


    def baseline_intime_insertion_into_db(self,thread_name="Thread0"):
        thread_name = "baseline_insrt"
        self.baseline_insert_temporized_data(self.temporized_baseline,thread_name=thread_name)
        self.temporized_baseline= defaultdict(int)

    def baseline_insert_left_over_data(self,thread_name="Thread0"):
        thread_name = "baseline_insrt"
        self.baseline_insert_temporized_data(self.temporized_baseline,thread_name=thread_name)
        self.temporized_baseline= defaultdict(int)



    def baseline_lazyinsertion_into_db(self,computed_baseline,extracted_redu_in_text_container, baseline_insertion_border=100000,thread_name="Thread0", ):
        #l = len(self.temporized_baseline)
        #p((l, baseline_insertion_border))
        if len(self.temporized_baseline) > baseline_insertion_border:
            self.temporize_baseline(computed_baseline, extracted_redu_in_text_container)
            self.baseline_intime_insertion_into_db()
        else:
            self.temporize_baseline(computed_baseline,extracted_redu_in_text_container)
        #self.insert_temporized_baseline_into_db()



    def insert_repl_into_db(self,doc_elem,text_elem,extracted_repl_in_text_container, repl_free_text_container,rle_for_repl_in_text_container, redu_free_text_container,mapping_redu,stemmed_text_container, thread_name="Thread0"):
        #self.logger.low_debug("Insertion of current ReplsIntoDB was started")
        sent_index = -1
        redufree_len = tuple(len(sent) for sent in redu_free_text_container)
        #p((redu_free_text_container,redufree_len, ))
        #p(mapping_redu, "mapping_redu")
        for sent in extracted_repl_in_text_container:
            #p(sent, "sent")
            sent_index += 1
            token_index = -1

            #temp_next_left_index_in_orig_t_elem = mapping_redu[sent_index][temp_index]
            #p((doc_elem))
            for repls_for_current_token in sent:
                token_index += 1
                if repls_for_current_token:
                    #p(repls_for_current_token, "repls_for_current_token")
                    for repl_container in repls_for_current_token:
                        #p(repl_container, "repl_container")
                        if repl_container:
                            try:
                                #p((sent_index, token_index), c="c")
                                current_sent_from_map = mapping_redu[sent_index]
                                next_left_index_in_orig_t_elem = token_index if token_index in current_sent_from_map else nextLowest(current_sent_from_map,token_index)
                                token_index_in_redu_free = current_sent_from_map.index(next_left_index_in_orig_t_elem)
                                it_is_redu = self._is_redu(sent_index,token_index_in_redu_free,redu_free_text_container)
                                input_dict = {
                                    "doc_id": doc_elem[0],
                                    # "doc_id": doc_elem[self._id_field_name],
                                    'redufree_len':redufree_len,
                                    "index_in_corpus": (sent_index,token_index),
                                    "index_in_redufree": (sent_index,token_index_in_redu_free),
                                    "rle_word": rle_for_repl_in_text_container[sent_index][token_index],
                                    "pos":text_elem[sent_index][0][next_left_index_in_orig_t_elem][1]  if it_is_redu else text_elem[sent_index][0][token_index][1],
                                    "normalized_word": repl_free_text_container[sent_index][token_index],
                                    "stemmed":stemmed_text_container[sent_index][token_index_in_redu_free],
                                    "polarity":text_elem[sent_index][1],
                                    "repl_letter": repl_container[0],
                                    "repl_length": repl_container[1],
                                    "index_of_repl": repl_container[2],
                                    "in_redu": (sent_index,token_index_in_redu_free)  if it_is_redu  else None
                                            }
                            except Exception as e:
                                #p(sent_container, "sent_container")
                                self._terminated = True
                                msg = "Given ReplContainer has wrong structure! '{}'. ('{}')".format(repl_container, repr(e))
                                self.logger.error(msg)
                                self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
                                return False


                            #p(((sent_index, token_index),repl_free_text_container[sent_index][token_index], ), "GET KONTEXT FueR DAS WORD")
                            #input_dict = 
                            self._get_context_left_for_repl(input_dict, text_elem, token_index_in_redu_free, mapping_redu, redu_free_text_container, sent_index,stemmed_text_container,)
                            #input_dict = 
                            self._get_context_right_for_repl(input_dict, text_elem, token_index_in_redu_free, mapping_redu, redu_free_text_container, sent_index,stemmed_text_container,)
                            self._repl_inserter(input_dict, thread_name=thread_name)
                            #p(input_dict, "input_dict")
                            #self.statsdb.lazyinsert("replications", input_dict, thread_name=thread_name)

        #self.logger.low_debug("Insertion of current ReplsIntoDB was finished")


    def _repl_inserter(self, inp_dict, thread_name="Thread0"):
        if len(self.temporized_repl[thread_name]) > self._lazyness_border:
            self._temporize_repl(inp_dict, thread_name=thread_name)
            self._write_repl_into_db(thread_name=thread_name)
        else:
            self._temporize_repl(inp_dict, thread_name=thread_name)

    def _temporize_repl(self, inp_dict,thread_name="Thread0"):
        temp_list = []
        for col in self._repls_cols:
            temp_list.append(inp_dict.get(col,None))
            #temp_list.append()
        self.temporized_repl[thread_name].append(db_helper.values_to_list(temp_list, "one"))

    def _write_repl_into_db(self,thread_name="Thread0"):
        #thread_name = 
        placeholders = ', '.join('?'*len(self._repls_cols))
        query = "INSERT or IGNORE INTO main.replications VALUES ({});".format(placeholders)
        #p((query,placeholders),"query")
        #p(self.temporized_repl[thread_name][0])
        #p(len(self.temporized_repl[thread_name][0]))
        self.statsdb._threads_cursors[thread_name].executemany(query,self.temporized_repl[thread_name] )
        self.temporized_repl[thread_name] = []





    def _redu_inserter(self, inp_dict, thread_name="Thread0"):
        if len(self.temporized_redu[thread_name]) > self._lazyness_border:
            self._temporize_redu(inp_dict, thread_name=thread_name)
            self._write_redu_into_db(thread_name=thread_name)
        else:
            self._temporize_redu(inp_dict, thread_name=thread_name)

    def _temporize_redu(self, inp_dict,thread_name="Thread0"):
        temp_list = []
        for col in self._redus_cols:
            temp_list.append(inp_dict.get(col,None))
            #temp_list.append()
        self.temporized_redu[thread_name].append(db_helper.values_to_list(temp_list, "one"))

    def _write_redu_into_db(self,thread_name="Thread0"):
        #thread_name = 
        placeholders = ', '.join('?'*len(self._redus_cols))
        query = "INSERT or IGNORE INTO main.reduplications VALUES ({});".format(placeholders)
        #p((query,placeholders),"query")
        #p(self.temporized_redu[thread_name][0])
        #p(len(self.temporized_redu[thread_name][0]))
        self.statsdb._threads_cursors[thread_name].executemany(query,self.temporized_redu[thread_name] )
        self.temporized_redu[thread_name] = []







    def insert_redu_into_db(self,doc_elem,text_elem,extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container, mapping_redu,stemmed_text_container,thread_name="Thread0"):
        #self.logger.low_debug("Insertion of current RedusIntoDB was started")
        sent_index = -1
        #p(extracted_redu_in_text_container, "extracted_redu_in_text_container")
        
        redufree_len = tuple(len(sent) for sent in redu_free_text_container)
        for redu_in_sent in extracted_redu_in_text_container:
            sent_index += 1
            for redu in redu_in_sent:
                #p(redu, c="r")
                #if redu:
                #p(redu_in_sent, "redu_in_sent")
                #p(redu_free_text_container, "redu_free_text_container")
                try:
                    rle_word = rle_for_repl_in_text_container[sent_index][redu['start_index_in_orig']]
                    #p((redu['start_index_in_orig'],rle_for_repl_in_text_container[sent_index][redu['start_index_in_orig']]), "redu['start_index_in_orig']", c="m")
                    #p(redu_free_text_container[sent_index][redu['index_in_redu_free']], "orig_words")
                    index_in_redu_free = redu["index_in_redu_free"]
                    input_dict = {
                            "doc_id": doc_elem[0],
                            # "doc_id": doc_elem[self._id_field_name],
                            'redufree_len':redufree_len,
                            "index_in_corpus": (sent_index,redu['start_index_in_orig']),
                            "index_in_redufree": (sent_index,index_in_redu_free),
                            #"rle_word": rle_word if rle_word else repl_free_text_container[sent_index][redu['start_index_in_orig']],
                            "pos":text_elem[sent_index][0][redu['start_index_in_orig']][1],
                            "normalized_word": repl_free_text_container[sent_index][redu['start_index_in_orig']],
                            "stemmed":stemmed_text_container[sent_index][index_in_redu_free],
                            'orig_words':redu_free_text_container[sent_index][index_in_redu_free][1],
                            "redu_length": redu['length'],
                            "polarity":text_elem[sent_index][1],
                            #"repl_letter": repl_container[0],
                            #"index_of_repl": repl_container[2],
                            }
                    
                except Exception as e:
                    #p(sent_container, "sent_container")
                    self._terminated = True
                    msg = "Given ReduContainer has wrong structure! '{}'. ('{}')".format(redu, e)
                    self.logger.error(msg)
                    self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
                    return False

                #sent = 
                start_index = redu['start_index_in_orig']
                #redu_length = redu['length']

                #input_dict = 
                self._get_context_left_for_redu(input_dict, text_elem,  mapping_redu, redu_free_text_container,sent_index , redu,stemmed_text_container,)
                #input_dict = 
                self._get_context_right_for_redu(input_dict, text_elem, mapping_redu, redu_free_text_container, sent_index,redu,stemmed_text_container,)


                #p("RIGHT STOP ---------------------\n", c="c")
                #self.statsdb.lazyinsert("reduplications", input_dict, thread_name=thread_name)
                self._redu_inserter(input_dict, thread_name=thread_name)
                #p(input_dict, "input_dict")

        #self.logger.low_debug("Insertion of current RedusIntoDB was finished")





    def _get_context_left_for_repl(self, input_dict, text_elem, token_index_in_redu_free, mapping_redu, redu_free_text_container, sent_index,stemmed_text_container,):
        ### context left
        #p(token_index_in_redu_free, "1token_index_in_redu_free")
        for context_number in range(1,self._context_lenght+1):
            col_name_context = "contextL{}".format(context_number)
            col_name_info = "context_infoL{}".format(context_number)
            #p(token_index_in_redu_free, "2token_index_in_redu_free")
            temp_index = token_index_in_redu_free - context_number
            ## if needed context_item in the current sent 
            #p((context_number,sent_index,temp_index))
            if temp_index >= 0:
                
                temp_next_left_index_in_orig_t_elem = mapping_redu[sent_index][temp_index]

                try:
                    #p((redu_free_text_container,sent_index, temp_index), "redu_free_text_container")
                    redu_free_text_container[sent_index][temp_index][1].items
                    
                    item = redu_free_text_container[sent_index][temp_index][0]
                    info = (text_elem[sent_index][0][temp_next_left_index_in_orig_t_elem][1],
                            redu_free_text_container[sent_index][temp_index][1],
                            stemmed_text_container[sent_index][temp_index])
                    #info = text_elem[sent_index][0][temp_index][1]
                except :
                    #p(repr(e), "E1")
                    item = redu_free_text_container[sent_index][temp_index]
                    info = (text_elem[sent_index][0][temp_next_left_index_in_orig_t_elem][1],
                        None,
                        stemmed_text_container[sent_index][temp_index])

            else: ## if needed context_item not in the current sent 
                #leftover_contextnumber = context_number - token_index # left over times to go to the left
                leftover_contextnumber = context_number - token_index_in_redu_free # left over times to go to the left
                if not context_number: # if the not time to go to the left
                    #p("WrongContextNumber. It should be >0", c="r")
                    raise Exception, "WrongContextNumber. It should be >0"
                number_of_loops = 0
                while True:
                    number_of_loops += 1
                    temp_sent_index = sent_index - number_of_loops
                    if temp_sent_index < 0:
                        item = None
                        info = None
                        break 
                    last_sent = redu_free_text_container[temp_sent_index+1]
                    current_sent = redu_free_text_container[temp_sent_index]
                    leftover_contextnumber = leftover_contextnumber if number_of_loops == 1 else leftover_contextnumber-(len(last_sent))
                    if leftover_contextnumber <= len(current_sent) and leftover_contextnumber >= 0:
                        
                        temp_index = -leftover_contextnumber
                        temp_next_left_index_in_orig_t_elem = mapping_redu[temp_sent_index][temp_index]
                        current_sent_from_map = mapping_redu[temp_sent_index]
                        temp_token_index_in_redu_free = current_sent_from_map.index(temp_next_left_index_in_orig_t_elem)
                        try:
                            redu_free_text_container[temp_sent_index][temp_index][1].items
                            item = redu_free_text_container[temp_sent_index][temp_index][0]
                            info = (
                                    text_elem[temp_sent_index][0][temp_next_left_index_in_orig_t_elem][1],
                                    redu_free_text_container[temp_sent_index][temp_index][1],
                                    stemmed_text_container[temp_sent_index][temp_token_index_in_redu_free])
                            #info = text_elem[temp_sent_index][0][temp_index][1]

                        except :
                            #p(e, "E2")
                            item = redu_free_text_container[temp_sent_index][temp_index]
                            info = (text_elem[temp_sent_index][0][temp_next_left_index_in_orig_t_elem][1],
                                    None, 
                                    stemmed_text_container[temp_sent_index][temp_token_index_in_redu_free])

                        break
                        #text_elem[sent_index][0][token_index][1]

            #item = json.dumps(item)
            input_dict.update({col_name_context: item, col_name_info:info})  
        return input_dict  




    def _get_context_right_for_repl(self, input_dict, text_elem, token_index_in_redu_free, mapping_redu, redu_free_text_container, sent_index,stemmed_text_container,):
        #context right
        for context_number in range(1,self._context_lenght+1):
            col_name_context = "contextR{}".format(context_number)
            col_name_info = "context_infoR{}".format(context_number)
            #while True:
            #temp_index = token_index + context_number
            
            temp_index = token_index_in_redu_free + context_number
            
            ## if needed context_item in the current sent 
            if temp_index < len(redu_free_text_container[sent_index]):
                ####p((sent_index, temp_index, len(mapping_redu[sent_index])), "temp_next_left_index_in_orig_t_elem")
                temp_next_left_index_in_orig_t_elem = mapping_redu[sent_index][temp_index]
                
                try:
                    redu_free_text_container[sent_index][temp_index][1].items
                    item = redu_free_text_container[sent_index][temp_index][0]
                    info = (text_elem[sent_index][0][temp_next_left_index_in_orig_t_elem][1],
                            redu_free_text_container[sent_index][temp_index][1],
                            stemmed_text_container[sent_index][temp_index])
                    #info = text_elem[sent_index][0][temp_index][1]

                except :
                    item = redu_free_text_container[sent_index][temp_index]
                    info = (text_elem[sent_index][0][temp_next_left_index_in_orig_t_elem][1],
                            None,
                            stemmed_text_container[sent_index][temp_index])

            else: ## if needed context_item not in the current sent 
                #leftover_contextnumber = context_number - (len(sent) - (token_index+1)) # left over times to go to the left
                leftover_contextnumber = context_number - (len(redu_free_text_container[sent_index]) - (token_index_in_redu_free+1)) # left over times to go to the left
                if not leftover_contextnumber: # if the not time to go to the left
                    raise Exception, "1. WrongContextNumber. It should be >0"
                number_of_loops = 0
                while True:
                    number_of_loops += 1
                    temp_sent_index = sent_index + number_of_loops
                    if temp_sent_index >= len(redu_free_text_container):
                        item = None
                        info = None
                        break 
                    last_sent = redu_free_text_container[temp_sent_index-1]
                    current_sent = redu_free_text_container[temp_sent_index]
                    leftover_contextnumber = leftover_contextnumber if number_of_loops == 1 else leftover_contextnumber-(len(last_sent))
                    if leftover_contextnumber <= 0 :
                        raise Exception, "2. WrongLeftoverContextNumber. It should be >0"
                    if leftover_contextnumber <= len(current_sent) and leftover_contextnumber > 0:
                        temp_index =leftover_contextnumber-1
                        temp_next_left_index_in_orig_t_elem = mapping_redu[temp_sent_index][temp_index]
                        current_sent_from_map = mapping_redu[temp_sent_index]
                        temp_token_index_in_redu_free = current_sent_from_map.index(temp_next_left_index_in_orig_t_elem)
                        try:
                            redu_free_text_container[temp_sent_index][temp_index][1].items
                            item = redu_free_text_container[temp_sent_index][temp_index][0]
                            info = (text_elem[temp_sent_index][0][temp_next_left_index_in_orig_t_elem][1],
                                    redu_free_text_container[temp_sent_index][temp_index][1],
                                    stemmed_text_container[temp_sent_index][temp_token_index_in_redu_free])

                        except :
                            #p("444")
                            item = redu_free_text_container[temp_sent_index][temp_index]
                            info = (text_elem[temp_sent_index][0][temp_next_left_index_in_orig_t_elem][1],
                                    None,
                                    stemmed_text_container[temp_sent_index][temp_token_index_in_redu_free])

                        break
            #item = json.dumps(item)
            input_dict.update({col_name_context: item, col_name_info:info}) 


        return input_dict 





    def _get_context_right_for_redu(self, input_dict, text_elem, mapping_redu, redu_free_text_container, sent_index,redu,stemmed_text_container,):
        ## context right
        #p("---------------------\nRIGHT START", c="c")
        for context_number in range(1,self._context_lenght+1):
            col_name_context = "contextR{}".format(context_number)
            col_name_info = "context_infoR{}".format(context_number)
            #while True:
            temp_index = redu['index_in_redu_free'] + context_number
            
            
            #p((context_number,sent_index,temp_index,len(redu_in_sent)), "context_number,sent_index,temp_index,len(redu_in_sent)")
            ## if needed context_item in the current sent 
            if temp_index < len(redu_free_text_container[sent_index]):
                #item = redu_free_text_container[sent_index][temp_index]
                
                token_index_in_orig_t_elem = mapping_redu[sent_index][temp_index] 
                #p((sent_index,temp_index, token_index_in_orig_t_elem), "sent_index,temp_index, token_index_in_orig_t_elem")
                try:
                    #p("111")
                    redu_free_text_container[sent_index][temp_index][1].items
                    
                    item = redu_free_text_container[sent_index][temp_index][0]
                    info = (text_elem[sent_index][0][token_index_in_orig_t_elem][1],
                            redu_free_text_container[sent_index][temp_index][1],
                            stemmed_text_container[sent_index][temp_index])
                    #info = text_elem[sent_index][0][temp_index][1]

                except:
                    #p("222")
                    
                    item = redu_free_text_container[sent_index][temp_index]
                    info = (text_elem[sent_index][0][token_index_in_orig_t_elem][1],
                            None,
                            stemmed_text_container[sent_index][temp_index])

                #p((item, info), c="b")
                #info = rle_for_repl_in_text_container[sent_index][start_index:start_index+redu['length']]
                #info = text_elem[sent_index][0][temp_index][1]
                #p((col_name_context,item, info), "item", c="m")
            else: ## if needed context_item not in the current sent 
                leftover_contextnumber = context_number - (len(redu_free_text_container[sent_index]) - (redu['index_in_redu_free']+1)) # left over times to go to the left
                if not leftover_contextnumber: # if the not time to go to the left
                    raise Exception, "1. WrongContextNumber. It should be >0"
                number_of_loops = 0
                while True:
                    number_of_loops += 1
                    temp_sent_index = sent_index + number_of_loops
                    if temp_sent_index >= len(redu_free_text_container):
                        item = None
                        info = None
                        #p((item, info), c="b")
                        break 
                    last_sent = redu_free_text_container[temp_sent_index-1]
                    current_sent = redu_free_text_container[temp_sent_index]
                    leftover_contextnumber = leftover_contextnumber if number_of_loops == 1 else leftover_contextnumber-(len(last_sent))
                    if leftover_contextnumber <= 0 :
                        raise Exception, "2. WrongLeftoverContextNumber. It should be >0"
                    if leftover_contextnumber <= len(current_sent) and leftover_contextnumber > 0:
                        temp_index = leftover_contextnumber-1
                        token_index_in_orig_t_elem = mapping_redu[temp_sent_index][temp_index] 
                        #p((temp_sent_index,temp_index, token_index_in_orig_t_elem), "sent_index,temp_index, token_index_in_orig_t_elem")
                        try:
                            #p("333")

                            redu_free_text_container[temp_sent_index][temp_index][1].items

                            item = redu_free_text_container[temp_sent_index][temp_index][0]
                            info = (text_elem[temp_sent_index][0][token_index_in_orig_t_elem][1],
                                    redu_free_text_container[temp_sent_index][temp_index][1],
                                    stemmed_text_container[temp_sent_index][temp_index])
                            #info = text_elem[temp_sent_index][0][temp_index][1]

                        except:
                            #p("444")
                            item = redu_free_text_container[temp_sent_index][temp_index]
                            info = (text_elem[temp_sent_index][0][token_index_in_orig_t_elem][1],
                                    None,
                                    stemmed_text_container[temp_sent_index][temp_index])
                        #p((item, info), c="b")
                        #info = [number_of_loops, temp_sent_index, leftover_contextnumber]


                        #item = current_sent[temp_index]
                        #info = text_elem[temp_sent_index][0][temp_index][1]
                        #p((col_name_context,item,info), c="r")
                        break


            #item = json.dumps(item)
            input_dict.update({col_name_context: item, col_name_info:info})  


        return input_dict



    def _get_context_left_for_redu(self, input_dict, text_elem, mapping_redu, redu_free_text_container, sent_index,redu,stemmed_text_container,):

        ### context Left
        for context_number in range(1,self._context_lenght+1):
            col_name_context = "contextL{}".format(context_number)
            col_name_info = "context_infoL{}".format(context_number)
            #while True:
        
            temp_index = redu['index_in_redu_free'] - context_number

            ## if needed context_item in the current sent 
            if (temp_index) >= 0:
                token_index_in_orig_t_elem = mapping_redu[sent_index][temp_index] 
                try:
                    redu_free_text_container[sent_index][temp_index][1].items
                    
                    item = redu_free_text_container[sent_index][temp_index][0]
                    info = (text_elem[sent_index][0][token_index_in_orig_t_elem][1],
                            redu_free_text_container[sent_index][temp_index][1],
                            stemmed_text_container[sent_index][temp_index])
                    #info = text_elem[sent_index][0][temp_index][1]

                except:
                    
                    item = redu_free_text_container[sent_index][temp_index]
                    info = (text_elem[sent_index][0][token_index_in_orig_t_elem][1],
                            None,
                            stemmed_text_container[sent_index][temp_index])
                #'start_index_in_orig'
                #p((col_name_context,item, info), "item", c="m")
            else: ## if needed context_item not in the current sent 
                leftover_contextnumber = context_number - redu['index_in_redu_free'] # left over times to go to the left
                if not context_number: # if the not time to go to the left
                    raise Exception, "WrongContextNumber. It should be >0"
                number_of_loops = 0
                while True:
                    number_of_loops += 1
                    temp_sent_index = sent_index - number_of_loops
                    if temp_sent_index < 0:
                        item = None #[number_of_loops, temp_sent_index, leftover_contextnumber]
                        info = None
                        break 
                    last_sent = redu_free_text_container[temp_sent_index+1]
                    current_sent = redu_free_text_container[temp_sent_index]
                    leftover_contextnumber = leftover_contextnumber if number_of_loops == 1 else leftover_contextnumber-(len(last_sent))
                    if leftover_contextnumber <= len(current_sent) and leftover_contextnumber >= 0:
                        #item = current_sent[-leftover_contextnumber]
                        #p(leftover_contextnumber, "leftover_contextnumber")
                        #info = text_elem[temp_sent_index][0][-leftover_contextnumber][1]
                        #info = rle_for_repl_in_text_container[sent_index][start_index:start_index+redu['length']]
                        temp_index = -leftover_contextnumber
                        token_index_in_orig_t_elem = mapping_redu[temp_sent_index][temp_index] 
                        try:
                            redu_free_text_container[temp_sent_index][temp_index][1].items
                            item = redu_free_text_container[temp_sent_index][temp_index][0]
                            info = (text_elem[temp_sent_index][0][token_index_in_orig_t_elem][1],
                                    redu_free_text_container[temp_sent_index][temp_index][1],
                                    stemmed_text_container[temp_sent_index][temp_index])
                            #info = text_elem[temp_sent_index][0][temp_index][1]

                        except:
                            item = redu_free_text_container[temp_sent_index][temp_index]
                            info = (text_elem[temp_sent_index][0][token_index_in_orig_t_elem][1],
                                    None,
                                    stemmed_text_container[temp_sent_index][temp_index])

                        break
                        #text_elem[sent_index][0][redu['index_in_redu_free']][1]

            #item = json.dumps(item)
            input_dict.update({col_name_context: item, col_name_info:info})  

        return input_dict                      




    ###################Optimizators########################


    def get_streams_from_baseline(self,stream_number, max_scope=False,size_to_fetch=1,  split_syntagma=False):
        row_num = self.statsdb.rownum("baseline")
        rows_pro_stream = row_num/stream_number
        streams = []
        num_of_getted_items = 0
        for i in range(stream_number):
            thread_name = "BSThread{}".format(i)
            # p((i,thread_name ), "get_streams_from_baseline")
            if i < (stream_number-1): # for gens in between 
                gen = self._baseline("*",max_scope=False,thread_name=thread_name,limit=rows_pro_stream, offset=num_of_getted_items,size_to_fetch=size_to_fetch, split_syntagma=split_syntagma)
                
                num_of_getted_items += rows_pro_stream
                streams.append((thread_name,LenGen(gen, rows_pro_stream)))
            else: # for the last generator
                gen = self._baseline("*",max_scope=False,thread_name=thread_name,limit=-1, offset=num_of_getted_items,size_to_fetch=size_to_fetch, split_syntagma=split_syntagma)
                
                streams.append((thread_name,LenGen(gen, row_num-num_of_getted_items)))
        return streams


    def _check_termination(self, thread_name="Thread0"):
        if self._terminated:
            self.logger.critical("'{}'-Thread was terminated.".format(thread_name))
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            sys.exit()

    def clean_baseline_table(self,stream_number=1, min_row_pro_sream=1000, cpu_percent_to_get=50, adjust_to_cpu=True):
        #p(self.statsdb.rownum("baseline"))
        if adjust_to_cpu:
            stream_number= get_number_of_streams_adjust_cpu( min_row_pro_sream, self.statsdb.rownum("baseline"), stream_number, cpu_percent_to_get=cpu_percent_to_get)
            if stream_number is None or stream_number==0:
                #p((self._get_number_of_left_over_files(),self.counter_lazy_getted),"self._get_number_of_left_over_files()")
                self.logger.error("StreamNumber is 0. Not generators could be returned.", exc_info=self._logger_traceback)
                return []

        self._init_compution_variables()
        streams= self.get_streams_from_baseline(stream_number, split_syntagma=False)
        self._terminated = False
        if self._status_bar:
            try:
                if not self.status_bars_manager.enabled:
                    self.status_bars_manager = self._get_status_bars_manager()
            except:
                self.status_bars_manager = self._get_status_bars_manager()

            status_bar_start = self._get_new_status_bar(None, self.status_bars_manager.term.center("StatsDB-Optimization") , "", counter_format=self.status_bars_manager.term.bold_white_on_cyan("{fill}{desc}{fill}"))
            status_bar_start.refresh()
            status_bar_threads_init = self._get_new_status_bar(len(streams), "ThreadsStarted", "threads")
            
            #status_bar_current = self._get_new_status_bar(self.statsdb.rownum("baseline"), "{}:BaselineOptimization".format(thread_name), "syntagma")
            #if self._status_bar:
                
            
        self._threads_num = len(streams)
        row_num_bevore = self.statsdb.rownum("baseline")
        if self._threads_num>1:
            if self._status_bar:
                unit = "rows"
                self.main_status_bar = self._get_new_status_bar(row_num_bevore, "AllThreadsTotalInsertions", unit)
                self.main_status_bar.refresh()
        else:
            self.main_status_bar = False


        syntagmas_to_delete = []
        #p(len(syntagmas_to_delete), "syntagmas_to_delete")
        for stream in streams:
            gen = stream[1]
            if not self._isrighttype(gen):
                self.logger.error("StatsBaselineCleanError: Given InpData not from right type. Please give an list or an generator.", exc_info=self._logger_traceback)
                return False
            #p(gen)

            thread_name = stream[0]
            processThread = threading.Thread(target=self._clean_baseline_table, args=(gen,syntagmas_to_delete, thread_name), name=thread_name)
            processThread.setDaemon(True)
            processThread.start()
            self.active_threads.append(processThread)
            if self._status_bar:
                status_bar_threads_init.update(incr=1)
            #i+=1
            time.sleep(1)


        if not self._wait_till_all_threads_are_completed("Compute"):
            return False

        #row_num_bevore = self.statsdb.rownum("baseline")
        ##### delete syntagmas from baseline-table
        qeary = "DELETE FROM baseline WHERE syntagma = ?;"
        #p(len(syntagmas_to_delete), "syntagmas_to_delete")
        if syntagmas_to_delete:
            self.statsdb.executemany(qeary,syntagmas_to_delete)
        row_num_after = self.statsdb.rownum("baseline")

        self.statsdb._commit()
        if self._status_bar:
            status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("Syntagmas: Bevore:'{}'; After:'{}'; Removed: '{}'.".format(row_num_bevore, row_num_after, row_num_bevore-row_num_after ) ), "",  counter_format=self.status_bars_manager.term.bold_white_on_cyan('{fill}{desc}{fill}\n'))
            status_bar_total_summary.refresh()
            self.status_bars_manager.stop()
        #p(len(syntagmas_to_delete), "syntagmas_to_delete")
        #syntagmas_to_delete = []
        if (row_num_bevore-row_num_after) == len(syntagmas_to_delete):
            if self._status_bar:
                self.logger.info("Baseline-Table was cleaned.")
            else:
                self.logger.info("Baseline-Table was cleaned.")
            return True
        else:
            False


    def _clean_baseline_table(self, gen,syntagmas_to_delete, thread_name="Thread0"):
        try:
            if not self._check_stats_db_should_exist():
                return False
                #return
            ### compute syntagmas to delete
            if self._status_bar:
                status_bar_current = self._get_new_status_bar(len(gen), "{}:".format(thread_name), "syntagma")

            minimum_columns = False
            indexes = self.col_index_min if minimum_columns else self.col_index_orig
            #indexes = self.col_index_min
            case = "" if self._case_sensitiv else " COLLATE NOCASE "
            for baseline_container in gen:
                was_found = False
                if self._status_bar:
                    status_bar_current.update(incr=1)
                    if self.main_status_bar:
                        self.main_status_bar.update(incr=1)

                #self._check_termination(thread_name=thread_name)
                inp_syntagma_splitted = baseline_container[0].split(self._baseline_delimiter)
                scope = len(inp_syntagma_splitted)
                syntagma_type = "lexem"
                where = self._get_where_statement(inp_syntagma_splitted,scope=scope,thread_name=thread_name,
                                                  with_context=True,syntagma_type=syntagma_type)
                collected_w = ()
                for w in where:
                    #p(w, "w")
                    #_threads_cursors["Thread0"].execute("SELECT id FROM replications WHERE {} ;".format(" AND ".join(w)))
                    if w:
                        current_reps = self.statsdb._threads_cursors[thread_name].execute(u"SELECT id FROM replications WHERE {} {};".format(u" AND ".join(w), case)).fetchone()
                        #current_reps = self.statsdb.getone("replications", where=w,connector_where="AND",case_sensitiv=self._case_sensitiv,thread_name=thread_name)
                        #tuple(self._rep_getter_from_db("repl",inp_syntagma_splitted,scope=scope,where=w,thread_name=thread_name, for_optimization=True))
                        if current_reps:
                            #p("REPL was found")
                            was_found = True
                            break

                        collected_w += (w,)
                    else:
                        self.logger.error("No where Statements was given. Probably an ImplementationsError.")
                        return  False
                    #else:

                ## Step 2: If no one repls was found, than search for redus
                if was_found:
                    continue

                for w in collected_w:
                    #collected_w.append(w)
                    if w:
                        current_reps = self.statsdb._threads_cursors[thread_name].execute(u"SELECT id FROM reduplications WHERE {} {};".format(u" AND ".join(w), case)).fetchone()
                        #current_reps = current_reps = self.statsdb.getone("reduplications", where=w,connector_where="AND",case_sensitiv=self._case_sensitiv,thread_name=thread_name)
                        #tuple(self._rep_getter_from_db("redu",inp_syntagma_splitted,scope=scope,where=w,thread_name=thread_name, for_optimization=True))
                        if current_reps:
                            #p("REDU was found")
                            was_found = True
                            break
                    else:
                        self.logger.error("No where Statements was given. Probably an ImplementationsError.")
                        return False
                
                if was_found:
                    continue
                
                syntagmas_to_delete.append((baseline_container[0],))
            
            self.threads_status_bucket.put({"name":thread_name, "status":"done"})
            return True
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            msg = "_CleanBaselineTableError: See Exception: '{}'. ".format(e)
            self.logger.error(msg, exc_info=self._logger_traceback)
            self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":msg})
            self._terminated = True
            self.statsdb.rollback()
            return False




    def _check_baseline_consistency(self):
        try:

            #p(baseline, "baseline")
            if self._status_bar:
                try:
                    if not self.status_bars_manager.enabled:
                        self.status_bars_manager = self._get_status_bars_manager()
                except:
                    self.status_bars_manager = self._get_status_bars_manager()

                status_bar_start = self._get_new_status_bar(None, self.status_bars_manager.term.center("Baseline-ConsistencyTest") , "", counter_format=self.status_bars_manager.term.bold_white_on_cyan("{fill}{desc}{fill}"))
                status_bar_start.refresh()
            
            normalized_word_tag = db_helper.tag_normalized_word
            consistency = True
            # counter_inconsistency = 0

            ###############################
            num = self.statsdb.rownum("baseline")
            if self._status_bar:
               status_bar_current = self._get_new_status_bar(num, "BaselineCheck:", "syntagma")
            #indexes = self.col_index_min if minimum_columns else self.col_index_orig
            indexes = self.col_index_orig
            ix_syntagma = indexes["baseline"]["syntagma"]
            ix_scope = indexes["baseline"]["scope"]
            ix_stemmed = indexes["baseline"]["stemmed"]
            for r in self.statsdb.lazyget("baseline"):
                if self._status_bar:
                    status_bar_current.update(incr=1)

                syntagma = r[ix_syntagma].split(self._baseline_delimiter)
                stemmed = r[ix_stemmed].split(self._baseline_delimiter)
                scope = r[ix_scope]
                if (len(syntagma)  != scope)  or (len(stemmed) != scope):
                    #p((len(syntagma) != len(stemmed) != 10),c="r")
                    consistency = False
                    self.logger.error("BaselineInvalidEntry: syntagma : '{}';  stemmed: '{}';  scope: '{}'; ".format(syntagma, stemmed, scope))


            if self._status_bar:
                if status_bar_current.count != status_bar_current.total:
                    status_bar_current.count = status_bar_current.total
                    status_bar_current.refresh()

                if consistency:
                    status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("Baseline is consistent."), "",  counter_format=self.status_bars_manager.term.bold_white_on_cyan('{fill}{desc}{fill}\n'))
                else:
                    status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("ERROR!!! Baseline is INCONSISTENT."), "",  counter_format=self.status_bars_manager.term.bold_white_on_red('{fill}{desc}{fill}\n'))
                
                status_bar_total_summary.refresh()
                self.status_bars_manager.stop()

            if consistency:
                return True
            else:
                #inconsistent_words
                #inconsistent_words = inconsistent_words if self._log_content else ":HIDDED_CONTENT:"
                self.logger.error("StatsDB is inconsistence. Try to set other 'baseline_delimiter' (used now: '{}') And if after that action your Baseline still stay broken than it could be an ImplementationsError. If you have this Problem, please contact Egor Savin (egor@savin.berlin).".format(self._baseline_delimiter))
                return False
        except Exception as e:
            self.logger.error("ConsistencyTestError: '{}' ".format(repr(e)))
            return False



    def _check_statsdb_consistency(self):
        try:
            baseline = self.statsdb.lazyget("baseline", columns="syntagma", where="scope=1")
            if baseline:
                baseline = set([b[0] for b in baseline  if b])
            else:
                self.logger.error("BaselineTableErorr: No one syntagma with scope 1 was found. It could mean, that this StatsDB is corrupt or inconsistent")
                return False
            #p(baseline, "baseline")
            if self._status_bar:
                try:
                    if not self.status_bars_manager.enabled:
                        self.status_bars_manager = self._get_status_bars_manager()
                except:
                    self.status_bars_manager = self._get_status_bars_manager()

                status_bar_start = self._get_new_status_bar(None, self.status_bars_manager.term.center("StatsDB-ConsistencyTest") , "", counter_format=self.status_bars_manager.term.bold_white_on_cyan("{fill}{desc}{fill}"))
                status_bar_start.refresh()
            
            normalized_word_tag = db_helper.tag_normalized_word
            consistency = True
            # counter_inconsistency = 0
            inconsistent_words = []
            ##############################
            ########## REPLS ###########
            ###############################
            num_repl = self.statsdb.execute("SELECT count(DISTINCT {}) FROM replications;".format(normalized_word_tag))
            if num_repl:
                num_repl = num_repl.fetchone()[0]
            else:
                self.logger.error("ERROR by getting ReplRowNumber. consistencyTest is failed.")
                return False

            if self._status_bar:
                status_bar_repl = self._get_new_status_bar(num_repl, "ReplsCheck:", "syntagma")
            for r in self.statsdb.getall("replications", columns=normalized_word_tag, distinct=True):
                if self._status_bar:
                    status_bar_repl.update(incr=1)
                #p(r[0],"r[0]")
                if r[0] not in baseline:
                    consistency = False
                    # counter_inconsistency += 1
                    try:
                        word = r[0].decode()
                    except:
                        pass
                    inconsistent_words.append(word)
                    self.logger.debug(u"StatsDB is inconsistence. There Exist NO-Baseline-Entry  for '{}'-word ".format(word))


            ##############################
            ########## REDUS ###########
            ##############################

            num_redu = self.statsdb.execute("SELECT count(DISTINCT {}) FROM reduplications;".format(normalized_word_tag))
            if num_redu:
                num_redu = num_redu.fetchone()[0]
            else:
                self.logger.error("ERROR by getting ReduRowNumber. consistencyTest is failed.")
                return False
            #p("555")
            if self._status_bar:
                status_bar_redu = self._get_new_status_bar(num_redu, "RedusCheck:", "syntagma")
            for r in self.statsdb.getall("reduplications", columns=normalized_word_tag,  distinct=True):
                if self._status_bar:
                        status_bar_redu.update(incr=1)
                #p(r[0],"r[0]")
                if r[0] not in baseline:
                    consistency = False
                    # counter_inconsistency += 1
                    try:
                        word = r[0].decode()
                    except:
                        pass
                    inconsistent_words.append(word)
                    self.logger.debug(u"StatsDB is inconsistence. There Exist NO-Baseline-Entry  for '{}'-word ".format(word))


            if self._status_bar:
                #p((num_repl, num_redu))
                #p((status_bar_repl.count, status_bar_repl.total, status_bar_redu.count, status_bar_redu.total))
                if status_bar_repl.count != status_bar_repl.total:
                    status_bar_repl.count = status_bar_repl.total
                    status_bar_repl.refresh()
                if status_bar_redu.count != status_bar_redu.total:
                    status_bar_redu.count = status_bar_redu.total
                    status_bar_redu.refresh()
                if consistency:
                    status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("StatsDB is consistent."), "",  counter_format=self.status_bars_manager.term.bold_white_on_cyan('{fill}{desc}{fill}\n'))
                else:
                    status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("ERROR!!! StatsDB is INCONSISTENT."), "",  counter_format=self.status_bars_manager.term.bold_white_on_red('{fill}{desc}{fill}\n'))
                status_bar_total_summary.refresh()
                self.status_bars_manager.stop()

            if consistency:
                return True
            else:
                #inconsistent_words
                inconsistent_words = inconsistent_words if self._log_content else ":HIDDED_CONTENT:"
                self.logger.error("StatsDB is inconsistence. '{}'-words don't have any entry in BaselineTable. It could be an ImplementationsError. If you have this Problem, please contact Egor Savin (egor@savin.berlin).\n  InconsistentWords: '{}'. ".format(len(inconsistent_words), inconsistent_words))
                return False
        except Exception as e:
            self.logger.error("ConsistencyTestError: '{}' ".format(repr(e)))
            return False

    def optimize_db(self,stream_number=1,thread_name="Thread0",optimized_for_long_syntagmas=False,min_row_pro_sream=1000, cpu_percent_to_get=50, adjust_to_cpu=True):
        if not self._db_frozen:
            if self.clean_baseline_table(stream_number=stream_number,min_row_pro_sream=min_row_pro_sream, cpu_percent_to_get=cpu_percent_to_get, adjust_to_cpu=adjust_to_cpu):
                #p(self._db_frozen,"self._db_frozen")
                self.statsdb.update_attr("db_frozen", True)
                self.set_all_intern_attributes_from_db()
                self.statsdb._commit()
                if self._db_frozen:
                    self.logger.info("Current StatsDB was successfully optimized.")
                    return True

                else:
                    return False
            else:
                self.logger.info("OptimizationError: StatsDB wasn't space optimized.")
                return False
        else:
            self.logger.warning("Current StatsDB was already optimized!")
            return False


    def _get_number_created_indexes(self):
        all_indexes = self.statsdb._get_indexes_from_db()
        created_indexes_raw = [item for item in all_indexes if "autoindex" not in item[1] ]
        return len(created_indexes_raw)

    def _get_created_indexes(self):
        all_indexes = self.statsdb._get_indexes_from_db()

        #p(all_indexes, "all_indexes")
        pattern = re.compile(r"create.+index(.+)on\s.*\((.+)\)", re.IGNORECASE)
        pattern_index_columns = re.compile(r"\((.+)\)")

        created_indexes_raw = [(item[2],pattern.findall(item[4])[0]) for item in all_indexes if "autoindex" not in item[1]]
        created_indexes = defaultdict(list)
        for index in created_indexes_raw:
            created_indexes[index[0]].append((index[1][0].strip(" ").strip("'").strip('"'),index[1][1].strip("'").strip('"').split(",")))
        return created_indexes


    def _drop_created_indexes(self, table_name="*"):
        indexes = self._get_created_indexes()
        if table_name == "*":
            for table_name, data in indexes.iteritems():
                for created_index_container in data:
                    self.statsdb.execute("DROP INDEX {};".format(created_index_container[0]))
        else:
            if table_name not in self.statsdb.tables():
                self.logger.error("'{}'-Tables not exist in the given Stats-DB. ".format(table_name))
                return False


    def _get_column_pairs_for_indexes(self,scope=False,optimized_for_long_syntagmas=False):
        columns_to_index = defaultdict(list)
        if optimized_for_long_syntagmas:
            scope = self.baseline_ngramm_lenght
            #if scope > 5:
            #    scope == 4
            #pass
        else:
            scope = scope if scope else self._min_scope_for_indexes
            #scope = 0

        if scope > self.baseline_ngramm_lenght:
            scope = self.baseline_ngramm_lenght


        for syntagma_type in ["lexem","pos"]:
            normalized_word_tag_name = "normalized_word" if syntagma_type == "lexem" else "pos"
            context_tag_name_r = "contextR"  if syntagma_type == "lexem" else "context_infoR"
            context_tag_name_l = "contextL"  if syntagma_type == "lexem" else "context_infoL"
        
            for step in xrange(scope+1):
                for token_index in xrange(step):
                    temp_columns = []
                    for i in xrange(step):
                        if i < token_index:
                            col_name = u"{}{}".format(context_tag_name_l,token_index-i)
                            temp_columns.append(col_name)
                        elif i == token_index:
                            col_name = u"{}".format(normalized_word_tag_name)
                            temp_columns.append(col_name)

                        elif i > token_index:
                            col_name = u"{}{}".format(context_tag_name_r,i-token_index)
                            temp_columns.append(col_name)

                    columns_to_index[syntagma_type].append(temp_columns)

        return columns_to_index


    def _get_biggest_column_pairs_for_indexes(self, raw_columns_to_index):
        #p(raw_columns_to_index, "raw_columns_to_index")
        for syntagma_type, column_pairs in  raw_columns_to_index.iteritems():
            temp_pairs_for_current_syntagma_type = {}
            for column_pair in column_pairs:
                if column_pair[0] not in temp_pairs_for_current_syntagma_type:
                    temp_pairs_for_current_syntagma_type[column_pair[0]] = column_pair
                else:
                    if len(temp_pairs_for_current_syntagma_type[column_pair[0]]) < len(column_pair):
                        temp_pairs_for_current_syntagma_type[column_pair[0]] = column_pair
            raw_columns_to_index[syntagma_type] = temp_pairs_for_current_syntagma_type.values()

        #p(raw_columns_to_index, "raw_columns_to_index")
        return raw_columns_to_index


    def _get_not_exists_indexes(self,raw_columns_to_index,tables_to_index,created_indexes):
        indexes_optimizes = defaultdict(list,{table_name:[col[1] for col in data] for table_name, data in created_indexes.iteritems() })
        columns_to_index = defaultdict(lambda:defaultdict(list))
        for table_name in tables_to_index:
            for syntagma_type, data in raw_columns_to_index.iteritems():
                for columns_bunch in data:
                    if columns_bunch not in indexes_optimizes[table_name]:
                        columns_to_index[table_name][syntagma_type].append(columns_bunch)
        #p(columns_to_index, "columns_to_index")

        return columns_to_index










    def create_additional_indexes(self,thread_name="Thread0", scope=False, optimized_for_long_syntagmas=False):
        tables_to_index = ["replications", "reduplications"]
        ### Step 0: Init Status Bar
        if self._status_bar:
            try:
                if not self.status_bars_manager.enabled:
                    self.status_bars_manager = self._get_status_bars_manager()
            except:
                self.status_bars_manager = self._get_status_bars_manager()

            status_bar_start = self._get_new_status_bar(None, self.status_bars_manager.term.center("StatsDB-Indexing") , "", counter_format=self.status_bars_manager.term.bold_white_on_cyan("{fill}{desc}{fill}"))
            status_bar_start.refresh()
            #status_bar_current = self._get_new_status_bar(self.statsdb.rownum("baseline"), "BaselineOptimization", "syntagma")
            
        ### compute syntagmas to delete
        #### Step 1: Extract exist indexes
        indexes = self._get_created_indexes()
        number_indexes_bevore = self._get_number_created_indexes()

        
        #qeary = "CREATE UNIQUE INDEX  {} ON {} ({});"
        #qeary = "CREATE UNIQUE INDEX IF NOT EXISTS {} ON {} ({});"
        qeary = "CREATE INDEX {} ON {} ({});"

        ### Step 2: Compute needed indexes to create
        raw_columns_to_index = self._get_column_pairs_for_indexes(scope=scope,optimized_for_long_syntagmas=optimized_for_long_syntagmas)
        raw_columns_to_index = self._get_biggest_column_pairs_for_indexes(raw_columns_to_index)
        #p(raw_columns_to_index, "raw_columns_to_index")

        #### Step3: Delete those columns_pairs, which exists in the StatsDB
        columns_to_index = self._get_not_exists_indexes(raw_columns_to_index, tables_to_index,indexes)
        number_to_create = len([col for table_name, data in columns_to_index.iteritems() for syntagma_type, columns in data.iteritems() for col in columns ])


        ### Step 4: Delete those indexes from StatsDB, which will be not needed after creation a new indexes
        #index_names_to_delete_from_db = self._get_indexes_which_are_smaller_than_new_one(indexes, columns_to_index)


        ### Step 5: Create Indexes
        if self._status_bar:
            status_bar_current = self._get_new_status_bar(number_to_create, "IndexCreation:", "index")
        i = 0
        for table_name, data in columns_to_index.iteritems():
            for syntagma_type, columns  in data.iteritems():
                for columns_bunch in columns:
                    if self._status_bar:
                        status_bar_current.update(incr=1)
                    i += 1
                    #p(columns_bunch, "columns_bunch")
                    index_name = "ix_{}_{}_scope_{}_nr_{}".format(table_name[:4],syntagma_type, len(columns_bunch),i)
                    prepared_qeary = qeary.format(index_name, table_name, ",".join(columns_bunch))
                    #p(prepared_qeary, "prepared_qeary")
                    self.statsdb.execute(prepared_qeary)



        self.statsdb._commit()

        ### Step 6: Print Status
        if self._status_bar:
            #bevore = i 
            #after = self.statsdb.rownum("baseline")
            number_indexes_after = self._get_number_created_indexes()
            status_bar_total_summary = self._get_new_status_bar(None, self.status_bars_manager.term.center("Indexes: NumBevore:'{}'; NumAfter:'{}'; WasCreated: '{}'.".format(number_indexes_bevore, number_indexes_after, number_indexes_after-number_indexes_bevore ) ), "",  counter_format=self.status_bars_manager.term.bold_white_on_cyan('{fill}{desc}{fill}\n'))
            status_bar_total_summary.refresh()
            self.status_bars_manager.stop()
            #print "\n"

        return number_to_create








    ###########################Other Methods##################


    def exist(self):
        return True if self.statsdb else False


    def db(self):
        if not self._check_stats_db_should_exist():
            return False
        self.logger.debug("DBConnection was passed.")
        return self.statsdb









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







    #######################Status Bars##############

    def _get_new_status_bar(self, total, desc, unit, counter_format=False):
        #counter_format
        try:
            self.status_bars_manager
        except AttributeError:
            self.status_bars_manager = self._get_status_bars_manager()

        if counter_format:
            counter = self.status_bars_manager.counter(total=total, desc=desc, unit=unit, leave=True, counter_format=counter_format)
        else:
            counter = self.status_bars_manager.counter(total=total, desc=desc, unit=unit, leave=True)
        return counter

    def _get_status_bars_manager(self):
        config_status_bar = {'stream': sys.stdout,
                  'useCounter': True, 
                  "set_scroll": True,
                  "resize_lock": True
                  }
        enableCounter_status_bar = config_status_bar['useCounter'] and config_status_bar['stream'].isatty()
        return enlighten.Manager(stream=config_status_bar['stream'], enabled=enableCounter_status_bar, set_scroll=config_status_bar['set_scroll'], resize_lock=config_status_bar['resize_lock'])

    def _status_bars(self):
        if self.status_bars_manager:
            return self.status_bars_manager.counters
        else:
            self.logger.error("No activ Status Bar Managers was found.", exc_info=self._logger_traceback)
            return False















    #################################



    def _check_db_should_be_an_stats(self):
        if self.statsdb.typ() != "stats":
            self.logger.error("No active DB was found. You need to connect or initialize a DB first, before you can make any operation on the DB.", exc_info=self._logger_traceback)
            return False
        else:
            return True


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







    def _initialisation_computation_process(self, inp_data, thread_name="Thread0"):
        if self._status_bar:
            if self._threads_num>1:
                if self._status_bar:
                    unit =  "rows"
                    self.main_status_bar_of_insertions.unit = unit
                    self.main_status_bar_of_insertions.total += len(inp_data)

        ### Preprocessors Initialization
        if thread_name not in self.preprocessors:
            if not self._init_preprocessors(thread_name=thread_name):
                self.logger.error("Error during Preprocessors initialization. Thread '{}' was stopped.".format(thread_name), exc_info=self._logger_traceback)
                self.threads_status_bucket.put({"name":thread_name, "status":"failed", "info":"Error during Preprocessors initialization"})
                self._terminated = True
                return False

        self.logger.debug("_InitComputationalProcess: Was initialized for '{}'-Thread. ".format(thread_name))
        
        if self._status_bar:
            if self._threads_num>1:
                if not self._timer_on_main_status_bar_was_reset:
                    #p(self.main_status_bar_of_insertions.start, "start1")
                    self.main_status_bar_of_insertions.start= time.time()
                    #p(self.main_status_bar_of_insertions.start, "start2")
                    self._timer_on_main_status_bar_was_reset = True

            unit = "rows"
            status_bar_insertion_in_the_current_thread = self._get_new_status_bar(len(inp_data), "{}:Insertion".format(thread_name), unit)
        self._check_termination(thread_name=thread_name)
        if self._status_bar:
            return status_bar_insertion_in_the_current_thread
        else:
            False


    def _is_redu(self, sent_index, token_index,redu_free_text_container):
        try:
            redu_free_text_container[sent_index][token_index][1].items
            return True
        except:
            return False
    def _check_buckets(self):
        status = False
        if not self.threads_error_bucket.empty():
            while not self.threads_error_bucket.empty():
                e = self.threads_error_bucket.get()
                self.threads_error_bucket.task_done()
                self.logger.error("InsertionError(in_thread_error_bucket): '{}'-Thread throw following Exception: '{}'. ".format(e[0], e[1]), exc_info=self._logger_traceback)
                status = True

        # if not self.channels_error_bucket.empty():
        #     while not self.channels_error_bucket.empty():
        #         e = self.channels_error_bucket.get()
        #         self.channels_error_bucket.task_done()
        #         self.logger.error("InsertionError(in_channel_error_bucket): '{}'-Thread ('{}') throw following Exception: '{}'. ".format(e[0], e[1],e[2]), exc_info=self._logger_traceback)
        #         status = True

        if status:
            self.logger.error("BucketChecker: Some threads/channels throw exception(s). Program can not be executed. ".format(), exc_info=self._logger_traceback)
            sys.exit()




    def _check_termination(self, thread_name="Thread0"):
        if self._terminated:
            self.logger.critical("'{}'-Thread was terminated.".format(thread_name))
            self.threads_status_bucket.put({"name":thread_name, "status":"terminated"})
            sys.exit()

    def _isrighttype(self, inp_data):
        #p(inp_data)
        check = (isinstance(inp_data, list), isinstance(inp_data, LenGen))
        #p(check, "check")
        if True not in check:
            self.logger.error("InputValidationError: Given 'inpdata' is not iterable. ", exc_info=self._logger_traceback)
            return False
        return True



    # def _isrighttype(self, inp_data):
    #     check = (isinstance(inp_data, list), isinstance(inp_data, types.GeneratorType))
    #     if True not in check:
    #         self.logger.error("InputValidationError: Given 'inpdata' is not iterable. ", exc_info=self._logger_traceback)
    #         return False
    #     return True



    def _check_corp_should_exist(self):
        if not self.corp: 
            self.logger.error("No active CorpusObj was found. You need to connect or initialize a Corpus first, before you can make any operation with Stats.", exc_info=self._logger_traceback)
            return False
        else:
            return True


    def _check_stats_db_should_exist(self):
        if not self.statsdb: 
            self.logger.error("No active DB was found. You need to connect or initialize a DB first, before you can make any operation with Stats.", exc_info=self._logger_traceback)
            return False
        else:
            return True

    def _check_stats_db_should_not_exist(self):
        if self.statsdb: 
            self.logger.error("An active DB was found. You need to initialize new empty Instance of DB before you can do this operation.", exc_info=self._logger_traceback)
            return False
        else:
            return True



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












