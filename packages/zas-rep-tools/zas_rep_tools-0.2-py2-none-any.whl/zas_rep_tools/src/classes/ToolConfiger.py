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
#from zas_rep_tools.src.classes.exporter import Exporter
#from zas_rep_tools.src.classes.reader import Reader
#from zas_rep_tools.src.classes.dbhandler import DBHandler
#from zas_rep_tools.src.classes.corpus import Corpus
#from zas_rep_tools.src.classes.stats import Stats
#from zas_rep_tools.src.utils.zaslogger import ZASLogger
from zas_rep_tools.src.classes.basecontent import BaseContent
from zas_rep_tools.src.utils.configer_helpers import ConfigerData

class ToolConfiger(BaseContent,ConfigerData):
    def __init__(self, rewrite=False,stop_if_db_already_exist = True,**kwargs):
        super(type(self), self).__init__(**kwargs)
        #p((self._mode,self._logger_save_logs), "self._logger_save_logs", c="b")
        #Input: Encapsulation:
        self._rewrite = rewrite
        self._stop_if_db_already_exist = stop_if_db_already_exist


        #InstanceAttributes: Initialization
        self._path_to_zas_rep_tools = path_to_zas_rep_tools
        self._path_to_user_config_data = os.path.join(self._path_to_zas_rep_tools, "user_config/user_data.fs")
        
        self._path_to_zas_rep_tools_data = path_to_data_folder
        self._path_to_zas_rep_tools_someweta_models = path_to_someweta_models
        self._path_to_zas_rep_tools_stop_words = path_to_stop_words

        self._user_data= self._get_user_config_db()
        if not self._user_data:
            self.logger.error("UserConfigData wasn't found or wasn't created. Execution was stopped!")
            sys.exit()


        #self._get_user_config_db() 
        # if not self._check_correctness_of_the_test_data():
        #     self.logger.error("TestDataCorruption: Please check test data.", exc_info=self._logger_traceback)
        #     sys.exit()

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

    # def row_text_elements(self, lang="all"):
    #     return copy.deepcopy(self._row_text_elements(lang=lang))
    
    # def text_elements(self, token=True, unicode_str=True,lang="all"):
    #     return copy.deepcopy(self._text_elements(token=token, unicode_str=unicode_str, lang=lang))

    # def docs_row_values(self,token=True, unicode_str=True, lang="all"):
    #     return copy.deepcopy(self._docs_row_values(token=token,unicode_str=unicode_str, lang=lang))

    # def docs_row_dict(self, token=True, unicode_str=True, all_values=False, lang="all"):
    #     '''
    #     just one dict with colums as key and list of all values as values for each columns()key
    #     '''
    #     return copy.deepcopy(self._docs_row_dict(token=token, unicode_str=unicode_str, all_values=all_values, lang=lang))

    # def docs_row_dicts(self, token=True, unicode_str=True,  lang="all"):
    #     '''
    #     list of dicts  with colums and values for each row
    #     '''
    #     return copy.deepcopy(self._docs_row_dicts(token=token, unicode_str=unicode_str, lang=lang))



    ###########################Config Values#######################

    @cached_property
    def path_to_zas_rep_tools(self):
        return copy.deepcopy(self._path_to_zas_rep_tools)

    @nottest
    @cached_property
    def path_to_tests(self):
        #p(self._path_to_zas_rep_tools)
        return os.path.join(self._path_to_zas_rep_tools, "tests/") 


    # @cached_property
    # def path_to_testdbs(self):
    #     return copy.deepcopy(self._path_to_testdbs)       

    # @cached_property
    # def test_dbs(self):
    #     return copy.deepcopy(self._test_dbs)             

    # @cached_property
    # def init_info_data(self):
    #     return copy.deepcopy(self._init_info_data)     

    # @cached_property
    # def columns_in_doc_table(self):
    #      return copy.deepcopy(self._columns_in_doc_table)            

    # @cached_property
    # def columns_in_info_tabel(self):
    #     return copy.deepcopy(self._columns_in_info_tabel)             

    # @cached_property
    # def columns_in_stats_tables(self):
    #     return copy.deepcopy(self._columns_in_stats_tables)     


    # @cached_property
    # def path_to_testsets(self):
    #      return copy.deepcopy(self._path_to_testsets)   

    # @cached_property
    # def types_folder_names_of_testsets(self):
    #      return copy.deepcopy(self._types_folder_names_of_testsets)  


    def clean_user_data(self):
        if self._user_data.clean():
            return True
        else:
            return False

    def get_data_from_user(self, user_info_to_get=False, rewrite=False):
        if not rewrite:
            rewrite = self._rewrite
        if user_info_to_get:
            if isinstance(user_info_to_get, (unicode, str)):
                user_info_to_get = [user_info_to_get]
        else:
            user_info_to_get = self._suported_user_info


        for user_info_name in user_info_to_get:
            if user_info_name not in self._suported_user_info:
                self.logger.error("UserDataGetterError:  '{}' - data not supported.  ".format(user_info_name), exc_info=self._logger_traceback)
                continue

            if user_info_name == "error_tracking":
                if rewrite:
                    self._cli_menu_error_agreement()
                    continue

                if self._user_data["error_tracking"] is None:
                    self._cli_menu_error_agreement()

            elif user_info_name == "project_folder":
                if rewrite:
                    self._cli_menu_get_from_user_project_folder()
                    continue
                if self._user_data["project_folder"] is None:
                    self._cli_menu_get_from_user_project_folder()

            elif user_info_name == "twitter_creditials":
                if rewrite:
                    self._cli_menu_get_from_user_twitter_credentials()
                    continue

                if self._user_data["twitter_creditials"] is None:
                    self._cli_menu_get_from_user_twitter_credentials()


            elif user_info_name == "email":
                if rewrite:
                    self._cli_menu_get_from_user_emails()
                    continue

                if  self._user_data["email"] is None:
                    self._cli_menu_get_from_user_emails()

            else:
                self.logger.critical("Not supported user_data_getter ('{}').".format(user_info_name))






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





    def _get_user_config_db(self):
        #try:
        try:
            if not os.path.isdir(os.path.split(self._path_to_user_config_data)[0]):
                self.logger.debug(" 'user_config' folder was created in '{}' ".format(os.path.split(self._path_to_user_config_data)[0]))
                os.mkdir(os.path.split(self._path_to_user_config_data)[0])
                db = MyZODB(self._path_to_user_config_data)
                db["permission"] = True
                db["twitter_creditials"] = None
                db["email"] = None
                db["project_folder"] = None
                db["error_tracking"] = None
            else:
                db = MyZODB(self._path_to_user_config_data)
                db["permission"] = True

            return db
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            if "permission" in str(e).lower():
                self.logger.error("UserConfigDBGetterError: Problem with permission. Probably solution. Please execute same command with 'sudo'-Prefix and enter your admin password. Exception: '{}'. ".format(e) ,exc_info=self._logger_traceback)
            else: 
                self.logger.error("UserConfigDBGetterError: '{}'. ".format(e) ,exc_info=self._logger_traceback)
            return False
 
 



    def _cli_menu_get_from_user_project_folder(self):
        getted_project_folder  = False

        def _get_input(args):
            getted_input = input(args)
            return str(getted_input)
        # Create the menu
        menu1 = SelectionMenu(["No", "Yes"],
                                title="Set Project Folder.",
                                #subtitle="(via Email)",
                                prologue_text="Every created database will be saved in the project folder. Before you can work with this tool you need to set up an Project Folder. Do you want to do it now? (if you want to use current directory as project folder just type an dot. exp: '.' )",
                                #epilogue_text="222"
                                )

        menu1.show()
        menu1.join()
        selection1 = menu1.selected_option
        #print selection1

        if selection1 == 1:
            status = True
            while status:
                prj_fldr = raw_input("Enter Project Folder: ")
                if os.path.isdir(prj_fldr):
                    abs_path = os.path.abspath(prj_fldr)
                    getted_project_folder = abs_path
                    status = False

                else: 
                    self.logger.critical("DirValidation: Given project Folder is not exist. Please retype it. (or type 'Ctrl+D' or 'Ctrl+C' to interrupt this process.)")
                    #print 

        if getted_project_folder:
            if getted_project_folder ==".":
                getted_project_folder = os.getcwd()
            self._user_data["project_folder"] = getted_project_folder
        #else:
        #    self._user_data["email"] = False
        #    return 
        
        return  getted_project_folder 



    def _cli_menu_get_from_user_emails(self):
        getted_emails = []
        # Create the menu
        menu1 = SelectionMenu(["No", "Yes"],
                    title="User Notification.",
                    subtitle="(via Email)",
                    prologue_text="This package can send to the users some important information. For example some day statistics for Twitter-Streamer or if some error occurs. Do you want to use this possibility? (Your email adress will stay on you Computer and will not be send anywhere.)",
                    #epilogue_text="222"
                    )

        menu1.show()
        menu1.join()
        selection1 = menu1.selected_option
        #print selection1

        if selection1 == 1:
            # Part 1: Get number of emails 
            status = True
            while status:
                menu2 = ConsoleMenu(
                                    title="Number of email addresses.",
                                    #subtitle="(via Email)",
                                    prologue_text="How much email addresses do you want to set?",
                                    #epilogue_text="222"
                                    )
                one_email = SelectionItem("one", 0)
                number_of_emails = FunctionItem("many", function=raw_input, args=["Enter a number:  "], should_exit=True)
                
                menu2.append_item(one_email)
                menu2.append_item(number_of_emails)
                menu2.show()
                menu2.join()
                getted_number = number_of_emails.return_value
                selection2 = menu2.selected_option
                #print selection2, getted_number
                if selection2 == 0:
                    status = False
                    number = 1
                else:
                    try:
                        if unicode(getted_number).isnumeric() or isinstance(getted_number, int):
                            number = int(getted_number)
                            status = False
                            
                        else:
                            self.logger.error("InputErr: Given Object is not an integer. Please retype your input! (in 5 seconds...)", exc_info=self._logger_traceback) 
                            time.sleep(3)

                    except Exception, e:
                        self.logger.critical("EmailNumberGetterError: '{}'. ".format(e))

            ## Part2 : Get Email 
            getted_emails = []
            i=0
            while i < number:
                email = str(raw_input("(#{} from {}) Enter Email: ".format(i+1, number)))
                is_valid = validate_email(email)
                if is_valid:
                    getted_emails.append(email)
                    i+= 1
                else: 
                    self.logger.warning( "EmailValidationError: Given Email is not valid. Please retype it.")
                    
        else:
            self._user_data["email"] = False
            return     

        self._user_data["email"] = getted_emails

        return getted_emails
       





    def _cli_menu_error_agreement(self):
        menu = SelectionMenu(["No", "Yes"],
                    title="Error-Tracking Agreement.",
                    #subtitle="(agreement)",
                    prologue_text="This package use a nice possibility of the online error tracking.\n It means, if you will get an error than the developers could get an notice about it in the real time. Are you agree to send information about errors directly to developers?",
                    #epilogue_text="222"
                    )
        menu.show()
        selection = menu.selected_option
        self._user_data["error_tracking"] = False if selection==0 else True

        return selection





    def _cli_menu_get_from_user_twitter_credentials(self):
        if not internet_on():
            self.logger.critical("InternetConnectionError: No Internet connection was found. Please check your connection to Internet and repeat this step. (Internet Connection is needed to validate your Twitter Credentials.)")
            sys.exit()
            #return []

        getted_credentials = []

        def _get_input(args):
            getted_input = input(args)
            return str(getted_input)
        # Create the menu
        menu1 = SelectionMenu(["No", "Yes"],
                    title="Twitter API Credentials.",
                    #subtitle="",
                    prologue_text="If you want to stream Twitter via official Twitter API than you need to enter your account Credentials. To get more information about it - please consult a README File of this package  (https://github.com/savin-berlin/zas-rep-tools). Under 'Start to use streamer' you can see  how you can exactly get this data. Do you want to enter this data now?",
                    #epilogue_text="222"
                    )


        menu1.show()
        menu1.join()
        selection1 = menu1.selected_option
        #print selection1

        if selection1 == 1:
            # Part 1: Get number of emails 
            status = True
            while status:
                menu2 = ConsoleMenu(
                                    title="Number of twitter accounts.",
                                    #subtitle="(via Email)",
                                    prologue_text="How much twitter accounts do you want to set up?",
                                    #epilogue_text="222"
                                    )
                one_email = SelectionItem("one", 0)
                number_of_emails = FunctionItem("many", function=raw_input, args=["Enter a number:  "], should_exit=True)
                
                menu2.append_item(one_email)
                menu2.append_item(number_of_emails)
                menu2.show()
                menu2.join()
                getted_number = number_of_emails.return_value
                selection2 = menu2.selected_option
                #print selection2, getted_number
                if selection2 == 0:
                    status = False
                    number = 1
                else:
                    try:
                        if unicode(getted_number).isnumeric() or isinstance(getted_number, int):
                            number = int(getted_number)
                            status = False
                            
                        else:
                            self.logger.error("InputErr: Given Object is not an integer. Please retype your input! (in 5 seconds...)", exc_info=self._logger_traceback)
                            #print "InputErr: Given Object is not an integer. Please retype your input! (in 5 seconds...)"
                            time.sleep(3)

                    except Exception, e:
                        self.logger.error("EmailNumberGetterError: '{}'. ".format(e), exc_info=self._logger_traceback)

            ## Part2 : Get Email 
            i=0
            while i < number:
                print "\n\n(#{} from {}) Enter Twitter Credentials: ".format(i+1, number)
                consumer_key = raw_input("Enter consumer_key: ")
                consumer_secret = raw_input("Enter consumer_secret: ")
                access_token = raw_input("Enter access_token: ")
                access_token_secret = raw_input("Enter access_token_secret: ")

                
                if internet_on():
                    api = twitter.Api(consumer_key=consumer_key,
                                    consumer_secret=consumer_secret,
                                    access_token_key=access_token,
                                    access_token_secret=access_token_secret)
                    try:
                        if api.VerifyCredentials():
                            getted_credentials.append({"consumer_key":consumer_key,
                                        "consumer_secret":consumer_secret,
                                        "access_token":access_token,
                                        "access_token_secret":access_token_secret
                                        })
                            i +=1
                        else:
                            print "InvalidCredential: Please retype them."

                    except Exception, e:
                        if "Invalid or expired token" in str(e):
                            self.logger.critical("InvalidCredential: Please retype them.")
                        elif "Failed to establish a new connection" in str(e):
                            self.logger.critical("InternetConnectionFailed: '{}' ".format(e))
                        else:
                            self.logger.critical("TwitterCredentialsCheckerError: '{}' ".format(e))
                        
                else:
                    self.logger.critical("InternetConnectionError: No Internet connection was found. Please check your connection to Internet and repeat this step. (Internet Connection is needed to validate your Twitter Credentials.)")
                    sys.exit()

        else:
            self._user_data["twitter_creditials"] = False
            return 

        self._user_data["twitter_creditials"] = getted_credentials

        return getted_credentials







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









