#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : Tests for XXX Module
# Author:
# c(Developer) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###Programm Info######
#
#
#
#
#

import unittest
import os
import logging
import sure
import copy
from collections import defaultdict
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree 
import json
import time
import threading

from zas_rep_tools.src.classes.ToolConfiger import ToolConfiger
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.classes.reader import Reader




from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.helpers import NestedDictValues, levenstein
from zas_rep_tools.src.utils.basetester import BaseTester


import platform
if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

# create test data, id needed



class TestZASToolConfigerToolConfiger(BaseTester,unittest.TestCase):
    #_multiprocess_can_split_ = True
    _multiprocess_shared_  = True
    #@classmethod 
    def setUp(self):
        #p(str(super))
        
        super(type(self), self).setUp()
        #super(BaseTester, self).__init__()
        #p(self.__dict__)
        

    #@classmethod 
    def tearDown(self):
        super(type(self), self).tearDown()






####################################################################################################
####################################################################################################
###################### START STABLE TESTS #########################################################
####################################################################################################
####################################################################################################


###################INITIALISATION:000############################################



    ###### xxx: 000 ######


    # def _get_meta_data_by_db_file_name(self, db_fname_to_search):

    #     for encryption, encryption_data in self.configer.test_dbs.iteritems():
    #         for template_name, template_name_data in encryption_data.iteritems():
    #             for language, language_data in template_name_data.iteritems():
    #                 for db_type, db_fname in language_data.iteritems():
    #                     #p((db_fname_to_search,db_fname))
    #                         if db_fname_to_search == db_fname:
    #                             return (encryption, template_name, language,db_type)
    #     return (None,None,None,None)


    ##### xx :0== ######

    @attr(status='stable')
    #@wipd
    def test_init_configer_000(self):
        self.prj_folder()
        configer = ToolConfiger(mode=self.mode)




    ##### throws_exceptions:050  ######




#################################Beginn##############################################
############################INTERN METHODS###########################################
#####################################################################################

###################    :100############################################ 

    ###### ***** ######



    ###### ***** ######


    ###### ***** ######






#################################END#################################################
############################INTERN METHODS###########################################
#####################################################################################








#################################Beginn##############################################
############################EXTERN METHODS###########################################
#####################################################################################


    def SendKeys(self,keys):
        if keys == '{ENTER}':
            keys = 'return'
        from os import system
        system('osascript -e \'tell application "System Events" to keystroke ' + keys + "'")

###################  Corpus Initialization :500############################################ 
   
    #@attr(status='stable')
    #@wipd
    def test_get_user_data_for_error_tracking_500(self):
        pass
        configer = ToolConfiger(mode=self.mode)        
        
        # # # #p(configer._user_data)
        # #configer.get_data_from_user(rewrite=True)
        # processThread = threading.Thread(target=configer.get_data_from_user, args=(False, True), name="Tester")
        # processThread.setDaemon(True)
        # processThread.start()
        

        # #p(processThread.isAlive())
        # #time.sleep(1.2)
        # wd_bevore =  str(os.getcwd())
        # while processThread.isAlive():
        #     time.sleep(2)
        #     if processThread.isAlive():
        #         self.SendKeys("3")
        #         self.SendKeys("return")
        #     else:
        #         break

        
        # #self.SendKeys("3")
        # #self.SendKeys("return")
        # #time.sleep(1)
        # wd_after =  str(os.getcwd())
        # #p((wd_bevore, wd_after))
        # if wd_bevore != wd_after:
        #     wd_after2 =  str(os.getcwd())
        #     p(wd_after2,"wd_after2")
        #     assert False
        #     #self.SendKeys("cd {}".format(wd_bevore))
        #     #self.SendKeys(wd_bevore)
        #     #self.SendKeys("return")




#################################END##################################################
############################EXTERN METHODS############################################
######################################################################################





####################################################################################################
####################################################################################################
###################### STOP STABLE TESTS #########################################################
####################################################################################################
####################################################################################################


























####################################################################################################
####################################################################################################
###################### START WORK_IN_PROGRESS (wipd) TESTS #########################################
####################################################################################################
####################################################################################################











####################################################################################################
####################################################################################################
###################### STOP WORK_IN_PROGRESS (wipd) TESTS #########################################
####################################################################################################
####################################################################################################







