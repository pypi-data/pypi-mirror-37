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
#import copy
import sys
#import regex
import logging
import sys
#import signal
import platform

import shutil
import io
import inspect
import time
from datetime import date
import tweepy
import langid
import unicodecsv as csv
import codecs
import json

#from collections import defaultdict
from raven import Client
#from cached_property import cached_property
from encodings.aliases import aliases
import nltk
from nltk.corpus import stopwords
import threading
#import multiprocessing

try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download("stopwords")


if platform.uname()[0].lower() !="windows":
    from blessings import Terminal


if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

from  zas_rep_tools_data.utils import path_to_data_folder, path_to_models, path_to_someweta_models, path_to_stop_words
from zas_rep_tools.src.utils.zaslogger import ZASLogger
#from zas_rep_tools.src.utils.logger import main_logger
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.utils.helpers import write_data_to_json, paste_new_line, send_email, set_class_mode, print_mode_name, path_to_zas_rep_tools, instance_info
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus
from zas_rep_tools.src.classes.basecontent import BaseContent

#from zas_rep_tools.src.classes.configer import Configer

abs_paths_to_stop_words = path_to_stop_words


global last_error
last_error = ""


#### initialize all counters
num_tweets_all_saved_for_this_session = 0
num_tweets_all_getted_for_one_day = 0
num_tweets_saved_on_the_disk_for_one_day = 0
num_tweets_selected_for_one_day = 0 # selected language, contain tweets and retweets
num_tweets_outsorted_for_one_day = 0
num_tweets_undelivered_for_one_day = 0
num_retweets_for_one_day = 0
num_original_tweets_for_one_day = 0
#runing_theards = []

class Streamer(BaseContent):
    supported_languages_by_langid = [u'af', u'am', u'an', u'ar', u'as', u'az', u'be', u'bg', u'bn', u'br', u'bs', u'ca', u'cs', u'cy', u'da', u'de', u'dz', u'el', u'en', u'eo', u'es', u'et', u'eu', u'fa', u'fi', u'fo', u'fr', u'ga', u'gl', u'gu', u'he', u'hi', u'hr', u'ht', u'hu', u'hy', u'id', u'is', u'it', u'ja', u'jv', u'ka', u'kk', u'km', u'kn', u'ko', u'ku', u'ky', u'la', u'lb', u'lo', u'lt', u'lv', u'mg', u'mk', u'ml', u'mn', u'mr', u'ms', u'mt', u'nb', u'ne', u'nl', u'nn', u'no', u'oc', u'or', u'pa', u'pl', u'ps', u'pt', u'qu', u'ro', u'ru', u'rw', u'se', u'si', u'sk', u'sl', u'sq', u'sr', u'sv', u'sw', u'ta', u'te', u'th', u'tl', u'tr', u'ug', u'uk', u'ur', u'vi', u'vo', u'wa', u'xh', u'zh', u'zu']
    supported_languages_by_twitter = [u'fr', u'en', u'ar', u'ja', u'es', u'de', u'it', u'id', u'pt', u'ko', u'tr', u'ru', u'nl', u'fil', u'msa', u'zh-tw', u'zh-cn', u'hi', u'no', u'sv', u'fi', u'da', u'pl', u'hu', u'fa', u'he', u'ur', u'th', u'en-gb']
    NLTKlanguages= {u'ru': u'russian', u'fr': u'french', u'en': u'english', u'nl': u'dutch', u'pt': u'portuguese', u'no': u'norwegian', u'sv': u'swedish', u'de': u'german', u'tr': u'turkish', u'it': u'italian', u'hu': u'hungarian', u'fi': u'finnish', u'da': u'danish', u'es': u'spanish'}
    supported_languages = set(supported_languages_by_langid) & set(supported_languages_by_twitter )

    supported_encodings_types = set(aliases.values())

    supported_filter_strategies = ['t', 't+l']
    stop_words_collection = {k:stopwords.words(v) for k,v in NLTKlanguages.iteritems()}
    stop_words_collection.update({u"de":os.path.join(abs_paths_to_stop_words, u"de.txt")}) # add my own set for german lang

    supported_stop_words = [k for k in stop_words_collection] # language naming should be the same as in this module "langid.classify(data["text"])[0]""

    supported_platforms= ["twitter"]
    #p(path_to_zas_rep_tools)

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, storage_path,
                platfrom="twitter", language=False, terms=False, stop_words=False, encoding="utf_8",
                email_addresse=False, ignore_rt=False, save_used_terms=False, filterStrat=False, **kwargs):
        
        #super(Streamer, self).__init__(**kwargs)
        super(type(self), self).__init__(**kwargs)
        #super(BaseContent, self).__init__(**kwargs)
        global num_tweets_all_saved_for_this_session
        global num_tweets_all_getted_for_one_day 
        global num_tweets_saved_on_the_disk_for_one_day
        global num_tweets_selected_for_one_day 
        global num_tweets_outsorted_for_one_day 
        global num_tweets_undelivered_for_one_day 
        global num_retweets_for_one_day 
        global num_original_tweets_for_one_day 

        
        #Input: Instance Encapsulation:
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        self._storage_path = storage_path
        self._platfrom = platfrom
        self._language = language # 
        self._terms = terms 
        self._stop_words = stop_words
        self._encoding = encoding
        self._email_addresse = email_addresse
        self._ignore_retweets = ignore_rt
        self._save_used_terms = save_used_terms
        self._filterStrat = filterStrat
        self._streamer_settings = {"language":self._language, 
                     "terms":True if self._terms else False,
                     "stop_words":True if self._stop_words else False ,
                     "filter":self._filterStrat  }


        # make Variable global for tweepy
        if platform.uname()[0].lower() !="windows":
            self.t = Terminal()
        else:
            self.t = False

        

        # Validation 
        self._validate_input()

        self.logger.debug('Intern InstanceAttributes was initialized')

        self.logger.debug('An instance of Streamer() was created ')


        if platfrom not in Streamer.supported_platforms:
            self.logger.error("Given Platform({}) is not supported. Please choice one of the following platforms: {}".format(platfrom,Streamer.supported_platforms), exc_info=self._logger_traceback)
            sys.exit()

        ## Log Settings of the Instance
        self._log_settings(attr_to_flag = False,attr_to_len = False)


    def __del__(self):
        super(type(self), self).__del__()


    def _get_stop_words(self):
        #p(Streamer.stop_words_collection[self._language], c="m")
        
        # to ensure the possibility to get intern stop_words_set

        # if not self._language:
        #     language = str(self._language)
        # else:
        #     language = self._language


        if self._stop_words and not self._language:
            self.logger.error("ToolRestriction: Stop-words cannot be given as stand-alone parameter. It should be given together with the any languages. If you want to give stop-words alone, please use for it parameter with the name 'terms'. ", exc_info=self._logger_traceback)
            sys.exit()

        elif not self._stop_words and  self._language:
            if self._language in Streamer.stop_words_collection:
                if isinstance(Streamer.stop_words_collection[self._language], (str,unicode)):
                    if os.path.isfile(Streamer.stop_words_collection[self._language]):
                        stop_words = [line.strip() for line in codecs.open(Streamer.stop_words_collection[self._language], encoding=self._encoding)]
                        self.logger.debug("Stop words was read from a file")
                    else:
                        self.logger.error("StopWordsGetterError: Given path to stop_words is not exist", exc_info=self._logger_traceback)
                        sys.exit()
                elif isinstance(Streamer.stop_words_collection[self._language], list):
                    stop_words = Streamer.stop_words_collection[self._language]
                    self.logger.debug("Stop words was read from a given list")
                else:
                    self.logger.error("StopWordsGetterError: Not supported format of stop-words. Please give them as path of as a list.", exc_info=self._logger_traceback)
                    sys.exit()

                self._streamer_settings["stop_words"] = True
                self.logger.info("Stop-words was took from the intern-set for the '{}' language.".format(self._language))
                
            else:
                self.logger.error("StopWordsGetterError: Stop-words for given language ('{}') wasn't found in the intern set of stop-words. Please import them into the Streamer using 'stop_words' parameter ".format(language) , exc_info=self._logger_traceback)
                sys.exit()
            #self.logger.error("TwitterRestriction: Language cannot be given as stand-alone parameter. It should be given together with the stop-words or terms.", exc_info=self._logger_traceback)
            #sys.exit()

        elif self._stop_words and self._language:
            #Streamer.stop_words_collection[self._language] = 
            if isinstance(self._stop_words, (str,unicode)):
                if self._stop_words in Streamer.stop_words_collection:
                    if isinstance(Streamer.stop_words_collection[self._stop_words], (str,unicode)):
                        if os.path.isfile(Streamer.stop_words_collection[self._stop_words]):
                            stop_words = [line.strip() for line in codecs.open(Streamer.stop_words_collection[self._stop_words], encoding=self._encoding)]
                            self.logger.debug("Stop words was read from a file")
                        else:
                            self.logger.error("StopWordsGetterError: Given path to stop_words is not exist", exc_info=self._logger_traceback)
                            sys.exit()
                    elif isinstance(Streamer.stop_words_collection[self._stop_words], list):
                        stop_words = Streamer.stop_words_collection[self._stop_words]
                        self.logger.debug("Stop words was read from a given list")
                    else:
                        self.logger.error("StopWordsGetterError: Given path to stop_words or stop-words in the intern collection is not exist", exc_info=self._logger_traceback)
                        sys.exit()
                    self.logger.info("Stop-words was took from the intern-set for the '{}' language.".format(self._stop_words))

                elif os.path.isfile(self._stop_words):
                    stop_words = [line.strip() for line in codecs.open(self._stop_words, encoding=self._encoding)]
                    self.logger.debug("Stop words was read from a file")

                else:
                    self.logger.error("StopWordsGetterError: Not supported format of stop-words. Please give them as path or as a list. (or check, if given path to file exist)", exc_info=self._logger_traceback)
                    sys.exit()


            elif isinstance(self._stop_words, list):
                stop_words = self._stop_words
                self.logger.debug("Stop words was read from a given list")
            else:
                self.logger.error("StopWordsGetterError: Not supported format of stop-words. Please give them as path of as a list.", exc_info=self._logger_traceback)
                sys.exit()

        elif not self._stop_words and not self._language and not self._terms:
            self.logger.error("InputError: No filtering parameters was given.", exc_info=self._logger_traceback)
            sys.exit()

        else:
            self.logger.error("StopWordsGetterError: Something was wrong!", exc_info=self._logger_traceback)
            sys.exit()


        return stop_words


    def cleaned_instance_attributes(self):
        #p(self.__dict__)
        exclude = ["_consumer_key","_consumer_secret","_access_token", "_access_token_secret", "client", "logger"]
        return {k:v for k,v in self.__dict__.iteritems() if k not in exclude} 

    def _validate_input(self):
        self._validate_given_language()

        if not self._stop_words:

            if self._language:
                if not self._terms and self._language not in Streamer.supported_stop_words:
                    self.logger.error("InputError: Terms or/and stop-words wasn't given. According the Twitter 'Developer Agreement and Policy' -  'terms' or/and 'stop-words' should be given. A Language is just an option and not obligatory for the Streamer. ", exc_info=self._logger_traceback)
                    sys.exit()
            else:
                if not self._terms:
                    self.logger.error("InputError: Nothing was given. Streamer need some input to initialize the Filtering. (Please give any terms/stop-words/language)  ", exc_info=self._logger_traceback)
                    sys.exit()

        
        self._evaluate_stop_words()
        self._evaluate_terms()
        self._validate_filter_strat()
        self._validate_storage_path()
        self._validate_given_encoding()
        

    def _validate_storage_path(self):
        if not os.path.isdir(self._storage_path):
            try:
                os.makedirs(self._storage_path)
                self.logger.info("Following storage directory was created: '{}'. There you will find all streamed data.".format(os.path.join(os.getcwd(),self._storage_path)))
            except:
                self.logger.error("PathError: It wasn't possible to create following directory: '{}' ".format(os.path.join(os.getcwd(),self._storage_path)), exc_info=self._logger_traceback)
                sys.exit()

    def _validate_filter_strat(self):
        if self._filterStrat:
            if self._filterStrat not in Streamer.supported_filter_strategies:
                self.logger.error("Given filter-strategies ('{}') is not supported. Please use one of the possible: {}".format(self._filterStrat,Streamer.supported_filter_strategies), exc_info=self._logger_traceback)
                sys.exit()
        elif not self._filterStrat:
            if self._language:
                self._filterStrat = "t+l"
                self._streamer_settings['filter'] = self._filterStrat
                self.logger.info("FilterStrategie was automatically set to: '{}'.".format(self._filterStrat))
            elif not self._language:
                self._filterStrat = "t" 
                self._streamer_settings['filter'] = self._filterStrat
                self.logger.info("FilterStrategie was automatically set to: '{}'.".format(self._filterStrat))

    def _validate_given_language(self):
        if self._language:
            if self._language not in Streamer.supported_languages:
                self.logger.error("Given Language ('{}'') is not supported. Please use one of the following languages: {}".format(self._language, Streamer.supported_languages), exc_info=self._logger_traceback)
                sys.exit()

            # if not self._stop_words:
            #     self.logger.error("TwitterRestriction: Language cannot be given as stand-alone parameter. It should be given together with the stop-words or terms. ", exc_info=self._logger_traceback)
            #     sys.exit()


    def get_track_terms(self):
        all_terms_to_track = []

        if self._terms:
            if self._stop_words:
                all_terms_to_track = self._get_stop_words() + self._terms

            elif not self._stop_words:
                all_terms_to_track = self._terms

        elif not self._terms:
            if self._stop_words:
                all_terms_to_track = self._get_stop_words()

            elif not self._stop_words:
                if not self._language:
                    self.logger.error("InputError: Don't found any 'stop_words/terms/language'. It is not allow to stream Twitter without any stop_words/terms." , exc_info=self._logger_traceback )
                    sys.exit()
                all_terms_to_track = self._get_stop_words()


        if len(all_terms_to_track) > 400:
            self.logger.error("InputError:  The Number of given stop_word/terms are exceeded (Twitter-API restriction). It is allow to track not more as 400 words. It was given '{}' words together. Please give less number of  stop_word/terms.\n\n  Following words was given: \n{} ".format(len(all_terms_to_track), all_terms_to_track) , exc_info=self._logger_traceback)
            sys.exit()
        elif len(all_terms_to_track) == 0:
            self.logger.error("InputError:  Not terms/stop_words for tracking was given.", exc_info=self._logger_traceback)
            sys.exit()
        #p(all_terms_to_track)
        return all_terms_to_track



    def _evaluate_terms(self):
        if self._terms:
            if isinstance(self._terms, (str,unicode)):
                if os.path.isfile(self._terms):
                    self._terms = [line.strip() for line in codecs.open(self._terms, encoding=self._encoding)]
                else:
                    self.logger.error("PathError: Given Path ({}) to terms are not exist".format(self._terms), exc_info=self._logger_traceback)
                    sys.exit()

            elif isinstance(self._terms, list):
                for term in self._terms:
                    if not isinstance(term, (str,unicode)):
                        self.logger.error("TypeError: Some of the given terms in the list is not string/unicode.", exc_info=self._logger_traceback)
                        sys.exit()


            else:
                self.logger.error("InputError:  Not supported format of terms. Please give them as path of as a list.", exc_info=self._logger_traceback)
                sys.exit()





    def _evaluate_stop_words(self):
        # change setting, if was toked intern stop_words set
        # if self._language and not self._stop_words and not self._terms:
        #     if self._language in Streamer.supported_stop_words:
        #         self._streamer_settings["stop_words"] = True



        if self._stop_words and not self._language:
            self.logger.error("ToolRestriction: Stop-words cannot be given as stand-alone parameter. It should be given together with the any languages. If you want to give stop-words alone, please use for it parameter with the name 'terms'. ", exc_info=self._logger_traceback)
            sys.exit()

        elif not self._stop_words and  self._language:
            pass

        elif self._stop_words and self._language:
            pass

        elif not self._stop_words and not self._language and not self._terms:
            self.logger.error("InputError: No filtering parameters was given.", exc_info=self._logger_traceback)
            sys.exit()

        # else:
        #     self.logger.error("StopWordsGetterError: Something was wrong!", exc_info=self._logger_traceback)
        #     sys.exit()





    def _validate_given_encoding(self):
        if self._encoding not in Streamer.supported_encodings_types:
            self.logger.error("Given encoding ({}) is not supported. Choice one of the following encodings: {}".format(self._encoding, Streamer.supported_encodings_types), exc_info=self._logger_traceback)
            sys.exit()

    def get_supported_platforms(self):
        return Streamer.supported_platforms

    def get_supported_languages(self):
        return Streamer.supported_languages

    def get_exist_stop_words(self):
        return Streamer.supported_languages

    def _create_main_log_message(self):
        msg_to_log = " >>>Streaming was started<<< "
        if self._language:
            msg_to_log = "{} for '{}' language".format(msg_to_log, self._language)

        if self._terms and self._language:
            msg_to_log = "{} and for given terms".format(msg_to_log)
        elif self._terms and not self._language:
            msg_to_log = "{} for given terms".format(msg_to_log)

        if (self._stop_words and self._language) or (self._stop_words and self._terms):
            msg_to_log = "{} and for given stop_words".format(msg_to_log)
        elif self._stop_words and not self._language and not self._terms:
            msg_to_log = "{} for given stop_words".format(msg_to_log)

        return msg_to_log

    def _initialize_status_bar(self):
        if platform.uname()[0].lower() !="windows":
            if self._language:
                sys.stdout.write("\n Status: {startW} totalSaved  {stop} = {startW}{selected:^8}{stop} + {startW}{retweets:^8}{stop} + {startW}other_lang{stop}    {startW}|undelivered|{stop} \n".format(selected=self._name_in_the_status_bar_original_tweets, retweets= self._name_in_the_status_bar_retweets, startW=self.t.bold_black_on_bright_white,  stop=self.t.normal))
                print "         {startW}{total:^13d}{stop}   {startW}{original:^8d}{stop}   {startW}{retweets:^8}{stop}   {startW}{outsorted:^10d}{stop}    {startW}|{undelivered:^11d}|{stop}  ".format(total=0, original=0, retweets= 0, outsorted=0, undelivered=0 ,startW=self.t.bold_black_on_bright_white,  stop=self.t.normal)
            else:
                sys.stdout.write("\n Status: {startW} totalSaved  {stop}    {startW}|undelivered|{stop} \n".format( startW=self.t.bold_black_on_bright_white,  stop=self.t.normal))
                print "         {startW}{total:^13d}{stop}    {startW}|{undelivered:^11d}|{stop}  ".format(total=0,  undelivered=0 ,startW=self.t.bold_black_on_bright_white,  stop=self.t.normal)
        else:
            if self._language:
                sys.stdout.write("\n Status:  totalSaved   = {selected:^8} + {retweets:^8} + other_lang    |undelivered| \n".format(selected=self._name_in_the_status_bar_original_tweets, retweets= self._name_in_the_status_bar_retweets))
                print "         {total:^13d}   {original:^8d}   {retweets:^8}   {outsorted:^10d}    |{undelivered:^11d}|  ".format(total=0, original=0, retweets= 0, outsorted=0, undelivered=0 )
            else:
                sys.stdout.write("\n Status:  totalSaved      |undelivered| \n")
                print "         {total:^13d}    |{undelivered:^11d}|  ".format(total=0,  undelivered=0)
 

    def stream_twitter(self):
        global old_date
        global logfile
        global storage_path
        global email_addresse
        global file_selected
        global file_outsorted
        global file_undelivered
        global file_retweets
        global path_to_the_jsons
        global last_error
        global num_tweets_all_saved_for_this_session
        global num_tweets_saved_on_the_disk_for_one_day
        #global runing_theards
        #global last_error

        # initialize it once
        langid.classify("test")


        email_addresse= self._email_addresse
        storage_path = self._storage_path

        old_date = date.today()
        path_to_the_day = os.path.join(storage_path, str(old_date))
        #last_error = ""

        file_selected, file_outsorted, file_undelivered, file_retweets, path_to_the_jsons =  create_new_files_for_new_day(str(old_date), storage_path, self._language)

        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(),timeout=5)
        global logfile
        logfile = codecs.open(os.path.join(self._storage_path,"streaming.log"), 'a', encoding="utf-8")
        #localtime = time.asctime( time.localtime(time.time()) )
        


        # longer timeout to keep SSL connection open even when few tweets are coming in
        stream = tweepy.streaming.Stream(auth, CustomStreamListener(streamer_settings=self._streamer_settings,language=self._language, ignore_retweets=self._ignore_retweets, logger_level=self._logger_level, logger_folder_to_save=self._logger_folder_to_save, logger_usage=self._logger_usage, logger_save_logs=self._logger_save_logs,  ext_tb=self._ext_tb), timeout=1000.0)
        terms = self.get_track_terms()
        self.logger.info("{} terms/stop_words used for tacking.".format(len(terms)))
        #p(terms)
        if self._save_used_terms:
            #p(os.path.join(path_to_the_day, "used_terms.log"))
            output_file_used_terms = codecs.open(os.path.join(path_to_the_day, "used_terms.log"), "a", encoding="utf-8")
            output_file_used_terms.write("{}:::{}:::{}\n\n\n".format(old_date, len(terms), terms))
            output_file_used_terms.close()
        #p(terms)
        # open output file
        
        #non_stop = True 
        last_5_error = []
        self._name_in_the_status_bar_original_tweets = "orig_{}".format(self._language) if self._language else "original"
        self._name_in_the_status_bar_retweets = "rt_{}".format(self._language) if self._language else "retweets"
        # stall_warnings - will inform you if you're falling behind. Falling behind means that you're unable to process tweets as quickly as the Twitter API is sending them to you.
        while True:
            #send_email("msm.filin@gmail.com", "Error", "Some error ")
            try:

                msg_to_log = self._create_main_log_message()
                #log_msg = "\n{} Starting stream for '{}' language.\n" 
                logfile.write( "{} {} \n".format(time.asctime( time.localtime(time.time()) ) , msg_to_log)  )
                msg_settings = "StreamerFilterSetting: {}".format(self._streamer_settings)


                if self._filterStrat == "t+l":
                    if not self._language:
                        self.logger.error("FilterStrategieError: Language is not given! But selected Strategy ('{}') requires an language. Please select  another Strategy or give an language. ".format(self._filterStrat), exc_info=self._logger_traceback)
                        sys.exit()
                    else:
                        log_msg_settings = "{} (l+t)".format(msg_settings)
                        logfile.write( "    {} \n".format(log_msg_settings) )
                        self.logger.info(log_msg_settings)
                        self.logger.info(msg_to_log)
                        self._initialize_status_bar()
                        #stream = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=30)
                        stream.filter(languages=[self._language], track=terms, stall_warnings=True)
                        #streamer_arguments = "languages=['{}'], track={}, stall_warnings=True".format(self._language, terms)
                elif self._filterStrat == "t":
                    log_msg_settings = "{} (t)".format(msg_settings)
                    logfile.write( "    {} \n".format(log_msg_settings) )
                    self.logger.info(log_msg_settings)
                    self.logger.info(msg_to_log)
                    self._initialize_status_bar()
                    #stream = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=30)
                    stream.filter(track=terms, stall_warnings=True) # , async=True


                
            except KeyboardInterrupt:
                print_exc_plus() if self._ext_tb else ""
                paste_new_line()
                self.logger.info("Streaming was aborted. stopping all processes.....")
                log_msg = "    {} Stream was aborted by user 'KeyboardInterrupt' \n" 
                logfile.write(  log_msg.format(time.asctime(time.localtime(time.time())))  )

                stream.disconnect() # that should wait until next tweet, so let's delete it
                del stream

                num_tweets_all_saved_for_this_session += num_tweets_saved_on_the_disk_for_one_day
                stats_cli = generate_status_msg_after_one_day(self._language,cl=True)
                stats_logfile = generate_status_msg_after_one_day(self._language)
                msg = "Short Conclusion:\n {}".format( stats_cli)
                self.logger.info(msg)
                logfile.write("    Short Conclusion for the last day ({}):\n{}".format(old_date, stats_logfile))
                logfile.close()
                file_selected.close()
                file_outsorted.close()
                file_undelivered.close()
                file_retweets.close()

                # for theard in runing_theards:
                #     if theard.isAlive():
                #         theard.do_run = False
                #         theard.daemon = True
                #         self.logger.info("'{}'-Theard was stopped!!!".format(theard.name))

                self.logger.info("All processes was correctly closed.")
                sys.exit(1)
                #os._exit(1)

            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                if "Failed to establish a new connection" in str(e):
                    log_msg = "     {} No Internet Connection. Wait 15 sec.....  \n" 
                    logfile.write(  log_msg.format(time.asctime(time.localtime(time.time())))  )
                    paste_new_line()
                    self.logger.critical("No Internet Connection. Wait 15 sec.....")
                    time.sleep(5)
                else:
                    log_msg = "     {} Stream get an Error: '{}' \n" 
                    logfile.write(  log_msg.format(time.asctime(time.localtime(time.time())),e)  )
                    paste_new_line()
                    self.logger.critical("Streaming get an Error......‘{}‘".format(e))

                if "IncompleteRead" not in str(e):
                    last_5_error.append(str(e))

                if len(last_5_error) >= 5:
                    if len(set(last_5_error)) ==1 :
                        log_msg = "     {} Stream was stopped after 5 same errors in stack: '{}' \n" 
                        logfile.write(  log_msg.format(time.asctime(time.localtime(time.time())),e)  )
                        msg = 'Hey,</br></br> Something was Wrong!  Streamer throw the following error-message and the Streaming Process was stopped:</br> <p style="margin-left: 50px;"><strong><font color="red">{}</strong> </font> </p> Please  check if everything is fine with this Process. </br></br> Greeting, </br>Your Streamer'.format(e)
                        last_error = str(e)
                        subject = "TwitterStreamer was stopped (Reason: last 5 errors are same)"
                        paste_new_line()
                        send_email(email_addresse, subject, msg)
                        self.logger.error("Stream was stopped after 5 same errors in stack")
                        #os._exit(1)
                        sys.exit()
                    else:
                        last_5_error = []

                if last_error != str(e):
                    msg = "Hey,</br></br> Something was Wrong!  Streamer throw the following error-message:</br> <p style='margin-left: 50px;''><strong><font color='red'>{}</strong> </font> </p> Please  check if everything is fine with this Process. </br></br> Greeting, </br>Your Streamer".format(e)
                    last_error = str(e)
                    paste_new_line()
                    send_email(email_addresse, 'Error: '+str(e), msg)







            # except tweepy.TweepError, e:
            #     paste_new_line()
            #     self.logger.info("Streaming geted an error: '{}'".format(e))
            #     log_msg = "    Streaming geted an error: {} \n" 
            #     logfile.write(  log_msg.format(e) )


                




class CustomStreamListener(tweepy.StreamListener):

    def __init__(self, streamer_settings=False, language=False, ignore_retweets = False,
                logger_level=logging.INFO, logger_folder_to_save="logs", logger_usage=True,
                logger_traceback=False,logger_save_logs=False, 
                ext_tb=False ):
        global logfile
        global num_tweets_all_saved_for_this_session
        global num_tweets_saved_on_the_disk_for_one_day
        global num_tweets_all_getted_for_one_day 
        global num_tweets_selected_for_one_day 
        global num_tweets_outsorted_for_one_day 
        global num_tweets_undelivered_for_one_day 
        global num_retweets_for_one_day 
        global num_original_tweets_for_one_day 
        #global runing_theards

        ## Developing Mode: Part 1
        # self._devmode = devmode
        # self._logger_level = logger_level 
        # if self._devmode:
        #     self._logger_level = logging.DEBUG
        #     logger_traceback = True


        ## Logger Initialisation 
        self._logger_traceback =logger_traceback
        self._logger_folder_to_save = logger_folder_to_save
        self._logger_usage = logger_usage
        self._logger_save_logs = logger_save_logs
        self._logger_level = logger_level
        self.L = ZASLogger(self.__class__.__name__, level=self._logger_level,
                            folder_for_log=self._logger_folder_to_save,
                            logger_usage=self._logger_usage,
                            save_logs=self._logger_save_logs)
        self.logger = self.L.getLogger()




        self._ignore_retweets = ignore_retweets


        self.restart_all_counters()
        self._language = language
        self._streamer_settings = streamer_settings
        self._ignore_retweets = ignore_retweets
        self._ext_tb = ext_tb
        if platform.uname()[0].lower() !="windows":
            self.t = Terminal()
        else:
            self.t =False


        if self._ignore_retweets:
            num_retweets_for_one_day = ">ignore<"

        #sys.stdout.write("\r         {startW}{total:^13d}{stop}   {startW}{original:^8d}{stop}   {startW}{retweets:^8}{stop}   {startW}{outsorted:^9d}{stop}  {startW}{undelivered:^11d}{stop}  ".format(total=num_tweets_all_getted_for_one_day, original=num_original_tweets_for_one_day, retweets= num_retweets_for_one_day, outsorted=num_tweets_outsorted_for_one_day, undelivered=num_tweets_undelivered_for_one_day ,startW=self.t.bold_black_on_bright_white, startG=self.t.bold_black_on_bright_green, startY=self.t.bold_black_on_bright_yellow, startB=self.t.bold_black_on_bright_blue, startR=self.t.bold_black_on_bright_red, stop=self.t.normal))


    def on_connect(self):
        sys.stdout.write("\033[A") # “Move the cursor up (1 line up)”
        #pass



    def archive_jsons(self,path_to_the_jsons):
        ## Step 1: Find the best right name 
        f_base_name = "jsons"
        extenstion = ".zip"
        full_fname = f_base_name+extenstion
        i=0
        while True:
            i+=1
            if os.path.isfile(os.path.join(os.path.dirname(path_to_the_jsons),full_fname)):
                f_base_name = f_base_name + "_"+ str(i)
                full_fname = f_base_name+extenstion
            else:
                break

        # Step 2: if in the current folder alredy exist an Archive, than remove it
        if os.path.isfile(os.path.join(os.getcwd(),full_fname)):
            os.remove(os.path.join(os.getcwd(),full_fname)) 
        #sys.exit()
        make_zipfile(full_fname, path_to_the_jsons)

        #p(ziparch)
        shutil.move(os.path.join(os.getcwd(),full_fname), os.path.dirname(path_to_the_jsons))
        shutil.rmtree(path_to_the_jsons, ignore_errors=True)
        self.logger.debug("All JSONS was moved and orig (not archived) folder was deleted.")
        paste_new_line()
        self.logger.info("All JSONS was archived and moved.")
        paste_new_line()
        self._initialize_status_bar()


    def _initialize_status_bar(self):
        self._name_in_the_status_bar_original_tweets = "orig_{}".format(self._language) if self._language else "original"
        self._name_in_the_status_bar_retweets = "rt_{}".format(self._language) if self._language else "retweets"
        if platform.uname()[0].lower() !="windows":
            if self._language:
                sys.stdout.write("\n Status: {startW} totalSaved  {stop} = {startW}{selected:^8}{stop} + {startW}{retweets:^8}{stop} + {startW}other_lang{stop}    {startW}|undelivered|{stop} \n".format(selected=self._name_in_the_status_bar_original_tweets, retweets= self._name_in_the_status_bar_retweets, startW=self.t.bold_black_on_bright_white,  stop=self.t.normal))
                #print "         {startW}{total:^13d}{stop}   {startW}{original:^8d}{stop}   {startW}{retweets:^8}{stop}   {startW}{outsorted:^10d}{stop}    {startW}|{undelivered:^11d}|{stop}  ".format(total=0, original=0, retweets= 0, outsorted=0, undelivered=0 ,startW=self.t.bold_black_on_bright_white,  stop=self.t.normal)
            else:
                sys.stdout.write("\n Status: {startW} totalSaved  {stop}    {startW}|undelivered|{stop} \n".format( startW=self.t.bold_black_on_bright_white,  stop=self.t.normal))
                #print "         {startW}{total:^13d}{stop}    {startW}|{undelivered:^11d}|{stop}  ".format(total=0,  undelivered=0 ,startW=self.t.bold_black_on_bright_white,  stop=self.t.normal)
        else:
            if self._language:
                sys.stdout.write("\n Status:  totalSaved   = {selected:^8} + {retweets:^8} + other_lang    |undelivered| \n".format(selected=self._name_in_the_status_bar_original_tweets, retweets= self._name_in_the_status_bar_retweets))
                #print "         {total:^13d}   {original:^8d}   {retweets:^8}   {outsorted:^10d}    |{undelivered:^11d}|  ".format(total=0, original=0, retweets= 0, outsorted=0, undelivered=0 )
            else:
                sys.stdout.write("\n Status:  totalSaved      |undelivered| \n")
                #print "         {total:^13d}    |{undelivered:^11d}|  ".format(total=0,  undelivered=0)
 


    def restart_all_counters(self):
        global num_tweets_all_saved_for_this_session
        global num_tweets_all_getted_for_one_day 
        global num_tweets_saved_on_the_disk_for_one_day
        global num_tweets_selected_for_one_day 
        global num_tweets_outsorted_for_one_day 
        global num_tweets_undelivered_for_one_day 
        global num_retweets_for_one_day 
        global num_original_tweets_for_one_day
        num_tweets_all_getted_for_one_day = 0
        num_tweets_saved_on_the_disk_for_one_day = 0
        num_tweets_selected_for_one_day = 0 # selected language, contain tweets and retweets
        num_tweets_outsorted_for_one_day = 0
        num_tweets_undelivered_for_one_day = 0
        num_retweets_for_one_day = ">ignore<" if self._ignore_retweets else 0
        num_original_tweets_for_one_day = 0


    def on_data(self, data):

        global old_date
        global file_selected
        global file_outsorted
        global file_undelivered
        global file_retweets
        global logfile
        global path_to_the_jsons
        global email_addresse
        global num_tweets_all_saved_for_this_session
        global num_tweets_all_getted_for_one_day 
        global num_tweets_saved_on_the_disk_for_one_day
        global num_tweets_selected_for_one_day 
        global num_tweets_outsorted_for_one_day 
        global num_tweets_undelivered_for_one_day 
        global num_retweets_for_one_day 
        global num_original_tweets_for_one_day
        #global runing_theards
      
          
        new_date = date.today()

        # new day was started
        if not new_date == old_date:

            # Preparation for the last day
            file_selected.close()
            file_outsorted.close()
            file_undelivered.close()
            file_retweets.close()
            paste_new_line()

            # #clean closed theards
            # for theard in runing_theards:
            #     if not theard.isAlive():
            #         self.runing_theards.remove(theard)

            processThread = threading.Thread(target=self.archive_jsons, args=(path_to_the_jsons,), name="archive_jsons")
            processThread.setDaemon(True)
            processThread.start()
            #runing_theards.append(processThread)


            # self.archive_jsons(path_to_the_jsons)

            file_selected, file_outsorted, file_undelivered, file_retweets, path_to_the_jsons =  create_new_files_for_new_day(str(new_date), storage_path, self._language)
            # file_selected.write('[\n') # start a new json array
            # file_outsorted.write('[\n') # start a new json array
            
            num_tweets_all_saved_for_this_session += num_tweets_saved_on_the_disk_for_one_day
            
            paste_new_line()
            stats_cli = generate_status_msg_after_one_day(self._language,cl=True)
            stats_logfile = generate_status_msg_after_one_day(self._language)
            msg = "Short Conclusion for day ({}):\n {}".format(old_date, stats_cli)
            self.logger.info(msg)
            logfile.write("    End of The day -> {}\n".format(old_date))
            logfile.write("    Short Conclusion for the day ({}):\n{}".format(old_date, stats_logfile))

            # Send Email
            streamer_settings_str_html = streamer_settings_to_str(self._streamer_settings).replace("\n", "</br>")
            stats_cli_to_html = stats_cli.replace("\n", "</br>")
            #p(stats_cli_to_html, c="m")
            msg = 'Hey,</br></br>  Yeeeeeap, News Day was started!  </br></br>See Stats for the last Day "{}" below: </br> <p style="margin-left: 50px;"><strong><font color="green">{}</strong> </font> </p>  </br></br> </br> Streamer Settings: <p style="margin-left: 50px;"><strong><font color="blue">{}</strong> </font> </p>  With love, </br>Your Streamer'.format(old_date, stats_cli.replace("\n", "</br>"), streamer_settings_str_html)
            subject = "TwitterStreamer started New Day ({})".format(new_date)
            send_email(email_addresse, subject, msg)

            # Start new day 
            old_date = new_date
            self.restart_all_counters()
            #p(num_tweets_saved_on_the_disk_for_one_day)
            self.logger.info("New day was started! ({})".format(old_date))
            logfile.write("    New day was started! -> {}\n".format(new_date))
            paste_new_line()
            self._initialize_status_bar()




        data = json.loads(data)
        

        ### Print Status of downloaded Tweets
        num_tweets_all_getted_for_one_day += 1
        
        try:
            tId = data["id"]


            # if tweets longer as 140 characters
            if "extended_tweet" in data:
                text = data["extended_tweet"]["full_text"].replace('\n', ' ').replace('\r', ' ')
            else:
                text = data["text"].replace('\n', ' ').replace('\r', ' ')


            # filter out all retweets
            lang = langid.classify(text)[0]
            # if len(data) ==2:
            #     p(data)
            if lang == self._language:
                num_tweets_selected_for_one_day += 1
                if self._ignore_retweets:
                    if "retweeted_status" not in data:
                        num_original_tweets_for_one_day += 1
                        file_selected.write(u"{} <t>{}</t>\n".format(unicode(tId),  text))
                        write_data_to_json(os.path.join(path_to_the_jsons, "{}.json".format(tId)), data)
                        num_tweets_saved_on_the_disk_for_one_day += 1

                else:
                    if "retweeted_status" in data:
                        num_retweets_for_one_day += 1
                        file_retweets.write(u"{} \n".format(unicode(tId)))
                    else:
                        num_original_tweets_for_one_day += 1
                        file_selected.write(u"{} <t>{}</t>\n".format(unicode(tId),  text))
                    

                    write_data_to_json(os.path.join(path_to_the_jsons, "{}.json".format(tId)), data)
                    num_tweets_saved_on_the_disk_for_one_day += 1


            else:
                if self._ignore_retweets:
                    if "retweeted_status" not in data:
                        num_tweets_outsorted_for_one_day +=1
                        file_outsorted.write(u"{} <t>{}</t> <l>{}</l>\n".format(unicode(tId),  text, lang))
                        write_data_to_json(os.path.join(path_to_the_jsons, "{}.json".format(tId)), data)
                        num_tweets_saved_on_the_disk_for_one_day += 1
                else:  
                    num_tweets_outsorted_for_one_day +=1
                    file_outsorted.write(u"{} <t>{}</t> <l>{}</l>\n".format(unicode(tId),  text, lang))
                    write_data_to_json(os.path.join(path_to_the_jsons, "{}.json".format(tId)), data)
                    num_tweets_saved_on_the_disk_for_one_day += 1



            self._update_status_bar()


            #self._output_file_other_tweets.write(  data["created_at"]+ data["id_str"]+ data["text"] + "\n"  )
        except KeyError, ke:
            print_exc_plus() if self._ext_tb else ""
            #p(data)
            if "limit" in str(data):
                #{u'limit': {u'track': 233, u'timestamp_ms': u'1527958183844'}}
                #p(data)
                if data["limit"]["track"] > num_tweets_undelivered_for_one_day:
                    num_tweets_undelivered_for_one_day = data["limit"]["track"]
                
                #pattern = r""
                time_now = time.asctime( time.localtime(time.time()) )
                file_undelivered.write(u"{} {} \n".format( time_now, data) )
            else:
                paste_new_line()
                self.logger.critical(str(repr(ke)))
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""

            log_msg = "Encountered error with status code: '{}' \n"
            logfile.write(  log_msg.format(time.asctime(time.localtime(time.time())),e)  )
            paste_new_line()
            self.logger.critical(log_msg.format(e))



    def _update_status_bar(self):
        if platform.uname()[0].lower() !="windows":
            if self._language:
                sys.stdout.write("\r         {startW}{total:^13d}{stop}   {startW}{original:^8d}{stop}   {startW}{retweets:^8}{stop}   {startW}{outsorted:^10d}{stop}    {startW}|{undelivered:^11d}|{stop}  ".format(total=num_tweets_saved_on_the_disk_for_one_day, original=num_original_tweets_for_one_day, retweets= num_retweets_for_one_day, outsorted=num_tweets_outsorted_for_one_day, undelivered=num_tweets_undelivered_for_one_day ,startW=self.t.bold_black_on_bright_white,  stop=self.t.normal))
                sys.stdout.flush()
            else:
                sys.stdout.write("\r         {startW}{total:^13d}{stop}    {startW}|{undelivered:^11d}|{stop}  ".format(total=num_tweets_saved_on_the_disk_for_one_day,  undelivered=num_tweets_undelivered_for_one_day ,startW=self.t.bold_black_on_bright_white,  stop=self.t.normal))
                sys.stdout.flush()

        else:
            if self._language:
                sys.stdout.write("\r         {total:^13d}   {original:^8d}   {retweets:^8}   {outsorted:^10d}    |{undelivered:^11d}|  ".format(total=num_tweets_saved_on_the_disk_for_one_day, original=num_original_tweets_for_one_day, retweets= num_retweets_for_one_day, outsorted=num_tweets_outsorted_for_one_day, undelivered=num_tweets_undelivered_for_one_day ))
                sys.stdout.flush()
            else:
                sys.stdout.write("\r         {total:^13d}    |{undelivered:^11d}|  ".format(total=num_tweets_saved_on_the_disk_for_one_day,  undelivered=num_tweets_undelivered_for_one_day ))
                sys.stdout.flush()


    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        log_msg = "     {} Encountered error with status code (Streamer still be on): '{}' \n"
        logfile.write(  log_msg.format(time.asctime(time.localtime(time.time())),status_code)  )
        


        #return True # Don't kill the stream

        if status_code == 401:
            #print status_code
            logger_msg = "UnauthorizedError401: Your credentials are invalid or your system time is wrong.\nTry re-creating the credentials correctly again following the instructions here (https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens). \nAfter recreation you need to retype your data. Use: $ zas-rep-tools retypeTwitterData"
            paste_new_line()
            self.logger.error(logger_msg, exc_info=self._logger_traceback)
            #return False
            #os._exit(1)

            msg = 'Hey,</br></br> Something was Wrong!  Streamer throw the following error-message and the Streaming Process was stopped:</br> <p style="margin-left: 50px;"><strong><font color="red">{}</strong> </font> </p> Please  check if everything is fine with this Process. </br></br> Greeting, </br>Your Streamer'.format(logger_msg)
            subject = "TwitterStreamer was stopped (Reason: UnauthorizedError401)"
            send_email(email_addresse, subject, msg)
            sys.exit()

        else:
            paste_new_line()
            self.logger.critical(log_msg.format(time.asctime(time.localtime(time.time())),status_code))

        return True

    def on_timeout(self):
        """Called when stream connection times out"""
        logfile.write("    "+str(time.asctime( time.localtime(time.time()) )) + ' Timeout...' + "\n")
        paste_new_line()
        self.logger.warning(" Timeout...")
        time.sleep(5)
        return True # Don't kill the stream


    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://dev.twitter.com/docs/streaming-apis/messages#Disconnect_messages_disconnect
        """
        logfile.write("    "+str(time.asctime( time.localtime(time.time()) )) + ' Disconnected from twitter...' + "\n")
        paste_new_line()
        self.logger.warning("OnDisconnect: Twitter sends a disconnect notice ('{}')".format(notice))
        time.sleep(5)
        return True

    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        logfile.write("    "+str(time.asctime( time.localtime(time.time()) )) + ' Disconnected from twitter...' + "\n")
        paste_new_line()
        self.logger.warning("OnLimit: Limitation notice arrives ('{}')".format(track))
        time.sleep(5)
        return True

    def on_warning(self, notice):
        """Called when a disconnection warning message arrives"""
        logfile.write("    "+str(time.asctime( time.localtime(time.time()) )) + ' Disconnected from twitter...' + "\n")
        paste_new_line()
        self.logger.warning("OnWarning: disconnection warning message arrives ('{}')".format(notice))
        time.sleep(5)
        return True



def create_new_files_for_new_day(current_data, storage_path, language):
    #p("new day")
    language = language if language else "none"
    path_to_the_day = os.path.join(storage_path, str(current_data))
    #p(path_to_the_day)
    path_to_the_jsons = os.path.join(path_to_the_day, "jsons")
    if not os.path.isdir(path_to_the_day):
        os.mkdir(path_to_the_day)
        

    if not os.path.isdir(path_to_the_jsons):
        os.mkdir(path_to_the_jsons)


    outfile_name = "tweets-" + current_data

    outfile_full_name = outfile_name + ".txt"
    language_outfile_name = "{}_{}".format( language,outfile_full_name)
    other_outfile_name =  "outsorted_{}".format(outfile_full_name)
    retweets_id_name =  "{}_retweets_{}".format(language,outfile_full_name)

    file_retweets = codecs.open(os.path.join(path_to_the_day, retweets_id_name), "a", encoding="utf-8")
    output_file_selected_tweets = codecs.open(os.path.join(path_to_the_day, language_outfile_name), "a", encoding="utf-8")
    output_file_outsorted_tweets = codecs.open(os.path.join(path_to_the_day,other_outfile_name), "a", encoding="utf-8")
    output_file_undelivered_tweets = codecs.open(os.path.join(path_to_the_day,"undelivered_"+outfile_name+ ".log"), "a", encoding="utf-8")
    return output_file_selected_tweets, output_file_outsorted_tweets, output_file_undelivered_tweets , file_retweets, path_to_the_jsons





def generate_status_msg_after_one_day(language, cl=False):
    #p(self._language)
    if cl:
        if language:
            msg = "TotalSavedThisSession: {session}\n    TotalSavedThisDay: {total}\n    Original-{lang}-Tweets: {original}\n    Original-{lang}-Retweets: {retweets}\n    Other languages: {outsorted}\n    Undelivered: {undelivered} ".format(session=num_tweets_all_saved_for_this_session, total=num_tweets_saved_on_the_disk_for_one_day, original=num_original_tweets_for_one_day, retweets= num_retweets_for_one_day, outsorted=num_tweets_outsorted_for_one_day, undelivered=num_tweets_undelivered_for_one_day, lang=language )

        else:
            msg = "TotalSavedThisSession: {session}\n    TotalSavedThisDay: {total}\n    Undelivered: {undelivered}".format(session=num_tweets_all_saved_for_this_session,total=num_tweets_saved_on_the_disk_for_one_day,  undelivered=num_tweets_undelivered_for_one_day )
    else:
        if language:
            msg = "     TotalSavedThisSession: {session}\n     TotalSavedThisDay: {total}\n     Original-{lang}-Tweets: {original}\n     Original-{lang}-Retweets: {retweets}\n     Other languages: {outsorted}\n     Undelivered: {undelivered} \n".format(session=num_tweets_all_saved_for_this_session, total=num_tweets_saved_on_the_disk_for_one_day, original=num_original_tweets_for_one_day, retweets= num_retweets_for_one_day, outsorted=num_tweets_outsorted_for_one_day, undelivered=num_tweets_undelivered_for_one_day, lang=language )

        else:
            msg = "     TotalSavedThisSession: {session}\n     TotalSavedThisDay: {total}\n     Undelivered: {undelivered}\n".format(session=num_tweets_all_saved_for_this_session,total=num_tweets_saved_on_the_disk_for_one_day,  undelivered=num_tweets_undelivered_for_one_day )
    
    #p(msg)
    return msg


def streamer_settings_to_str(settings):
    output = ""
    for setting_name, value in settings.iteritems():
        output += "'{}' = '{}'\n".format(setting_name,value)
    return output 

