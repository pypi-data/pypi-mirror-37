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
import gc
from testfixtures import tempdir, TempDirectory

from zas_rep_tools.src.classes.TestsConfiger import TestsConfiger
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

#TestsConfiger(mode="dev", rewrite=True).create_test_data(use_original_classes=True, status_bar=True, corp_log_ignored=True, corp_language="en", corp_lang_classification=False, corp_pos_tagger="tweetnlp")

class TestZASTestsConfigerTestsConfiger(BaseTester,unittest.TestCase):
#class TestZASTestsConfigerTestsConfiger():
    #_multiprocess_can_split_ = True
    #_multiprocess_shared_  = True
    #  #@classmethod 
    def setUp(self):
        #p(str(super))
        #pass
        super(type(self), self).setUp()
        #super(BaseTester, self).__init__()
        #p(self.__dict__)
        

    # #@classmethod 
    def tearDown(self):
        super(type(self), self).tearDown()

        #pass

    # def setUp(self):

    #     create_test_data()

    #     gc.collect() ## Start Garbage Collector, before start with the new test case.
        
    #     #### MODI######
    #     #self.mode = "test"
    #     self.mode = "test+s+"
    #     #self.mode = "test+s-"
    #     #self.mode = "dev"
    #     #self.mode = "dev-"
    #     #self.mode = "silent"
    #     #self.mode = "error"

    #     #### Set TestsConfiger #####
    #     clear_logger()
    #     self.configer = TestsConfiger(mode="silent") # MODE SHOULD BE "test". !!!

    #     self.tempdir = TempDirectory()
        

    #     self.path_to_zas_rep_tools = self.configer.path_to_zas_rep_tools
    #     #gc.collect()


    # #@classmethod 
    # def tearDown(self):
    #     #del self.configer
    #     t = self.tempdir
    #     #self.tempdir.cleanup()
    #     del self
    #     gc.collect()
    #     t.cleanup()
    #     del t
    #     #gc.collect()







####################################################################################################
####################################################################################################
###################### START STABLE TESTS #########################################################
####################################################################################################
####################################################################################################


###################INITIALISATION:000############################################



    ###### xxx: 000 ######

    def _unidiff_output(self,expected, actual):
        """
        Helper function. Returns a string containing the unified diff of two multiline strings.
        """

        import difflib
        expected=expected.splitlines(1)
        actual=actual.splitlines(1)

        diff=difflib.unified_diff(expected, actual)

        return ''.join(diff)



    def _get_meta_data_by_db_file_name(self, db_fname_to_search):

        for encryption, encryption_data in self.configer.test_dbs.iteritems():
            for template_name, template_name_data in encryption_data.iteritems():
                for language, language_data in template_name_data.iteritems():
                    for db_type, db_fname in language_data.iteritems():
                        #p((db_fname_to_search,db_fname))
                            if db_fname_to_search == db_fname:
                                return (encryption, template_name, language,db_type)
        return (None,None,None,None)


    ##### xx :0== ######

    @attr(status='stable')
    #@wipd
    def test_init_configer_000(self):
        self.prj_folder()
        configer = TestsConfiger(mode=self.mode)




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


###################  Corpus Initialization :500############################################ 
   
    # #@attr(status='stable')
    # #@wipd
    # def test_create_all_test_dbs_5(self):
    #     c = TestsConfiger(mode=self.mode, rewrite=True)
    #     #c.logger.info("ghjk")
    #     #c.logger.outsorted("ghjk")
    #     #c.logger.log(8, "fghjk")
    #     #c.logger.log(50, "fghjk")
    #     #c.logger.outsorted_reader("outsorted_reader")
    #     #c.logger.outsorted_corpus("outsorted_corpus")
    #     #c.logger.outsorted_stats("outsorted_corpus")
    #     #c.logger.outsorted_reader("outsorted_reader")
    #     #c.logger.outsorted_corpus("outsorted_corpus")
    #     #c.logger.info("info")
    #     #c.logger.info("fghjkl")
    #     #c.logger.error("fghjkl")
    #     #p(c.text_elements(token=True, unicode_str=True))
    #     #c.create_test_dbs(use_original_classes=True, status_bar=True, corp_log_ignored=True,corp_lang_classification=True)
    #     #p(c._docs_row_dict(token=True, unicode_str=True, all_values=True , lang="all") )
    #     # p("fghjl")
    #     # time.sleep(2)
    #     # p("fghjl")
    #     # p("fghjl")
    #     # time.sleep(2)
    #     # p("fghjl")
    #     # p("fghjl")
    #     # p("fghjl")
    #     # time.sleep(2)
    #     # p("fghjl")
    #     # p("fghjl")
    #     # p("fghjl")
    #     # time.sleep(2)
    #     # p("fghjl")
    #     #c.create_test_dbs(abs_path_to_storage_place=self.tempdir_project_folder, use_original_classes=True, status_bar=True, corp_log_ignored=True, corp_language="en", corp_lang_classification=False, corp_pos_tagger="tweetnlp")
    #     #p(TestsConfiger(mode=self.mode).self.docs_row_values(token=True, unicode_str=True))

    #@attr(status='stable')
    #@wipd
    def test_create_all_test_dbs_created_with_dbhandler_500(self):
        self.prj_folder()
        #abs_path_to_storage_place=os.path.join(self.path_to_zas_rep_tools, self.path_to_testdbs)
        abs_path_to_storage_place=self.tempdir_project_folder
        configer = TestsConfiger(mode=self.mode, rewrite=True)
         
        configer.create_test_dbs(rewrite=True, abs_path_to_storage_place=abs_path_to_storage_place, use_original_classes=False)
        #configer.create_test_dbs(rewrite=False, abs_path_to_storage_place=self.path_to_zas_rep_tools)

        created_dbs = [filename for filename in os.listdir(abs_path_to_storage_place) if ".db" in filename]
        #number_db_which_should_be_created = len(self.configer.init_info_data) * len(["corpus","stats"]) * len(["plaintext", "encrypted"])
        #p(os.listdir(abs_path_to_storage_place))
        number_db_which_should_be_created = len(list(NestedDictValues(self.configer._test_dbs)))

        if len(created_dbs) != number_db_which_should_be_created:
            assert False

        for db_name in created_dbs:
            #p(db_name)
            encryption, template_name, language, db_type= self._get_meta_data_by_db_file_name(db_name)
            #p((encryption, template_name, language, db_type))
            #sys.exit()
            #p(encryption)
            if not encryption:
                assert False

            db = DBHandler(mode=self.mode)
            if encryption == "encrypted":
                encryption_key=self.configer.init_info_data[template_name]["encryption_key"][db_type]
                db.connect(os.path.join(abs_path_to_storage_place,db_name), encryption_key=encryption_key)
            else:
                db.connect(os.path.join(abs_path_to_storage_place,db_name))

            if db_type == "corpus":
                for item1, item2 in zip(self.configer.docs_row_values(token=True, unicode_str=True, lang="all")[template_name], db.getall("documents")):
                    for i1,i2 in zip(item1, item2):
                        if isinstance(i1, (list,tuple,dict)):
                            #p(i1)
                            i1 = json.dumps(i1)
                            #continue
                        if  i1 == False :
                            i1=0
                        if  i1 == True :
                            i1=1
                        if unicode(i1) != unicode(i2):
                            p((unicode(i1) , unicode(i2)))
                            assert False
            elif db_type == "stats":
                ### Here for stats
                pass





    @attr(status='stable')
    #@wipd
    def test_create_all_test_dbs_created_with_corpus_and_stats_classes_501(self):
        self.prj_folder()
        self.test_dbs()
        #abs_path_to_storage_place=os.path.join(self.path_to_zas_rep_tools, self.path_to_testdbs)
        abs_path_to_storage_place=self.tempdir_project_folder

        configer = TestsConfiger(mode=self.mode, rewrite=True)
        #configer.create_test_dbs(abs_path_to_storage_place=abs_path_to_storage_place, use_original_classes=True, status_bar=True, corp_log_ignored=True,corp_lang_classification=True)
        configer.create_test_dbs(abs_path_to_storage_place=abs_path_to_storage_place, use_original_classes=True, status_bar=True, corp_log_ignored=True,corp_lang_classification=True, use_test_pos_tagger=False)

        created_dbs = [filename for filename in os.listdir(abs_path_to_storage_place) if ".db" in filename]
        number_db_which_should_be_created = len(list(NestedDictValues(self.configer._test_dbs)))
        if len(created_dbs) != number_db_which_should_be_created:
            assert False

        #p(created_dbs ," created_dbs")
        for db_name in created_dbs:
            #p(db_name)
            encryption, template_name, language, db_type= self._get_meta_data_by_db_file_name(db_name)
            #p((encryption, template_name, language, db_type))
            #sys.exit()
            #p(encryption)
            #if not encryption:
            #    assert False

            db = DBHandler(mode=self.mode)
            if encryption == "encrypted":
                encryption_key=self.configer.init_info_data[template_name]["encryption_key"][db_type]
                #p(encryption_key,"encryption_key", c="r")
                db.connect(os.path.join(abs_path_to_storage_place,db_name), encryption_key=encryption_key)
            else:
                db.connect(os.path.join(abs_path_to_storage_place,db_name))

            if db_type == "corpus":
                #p(language)
                #p(self.configer.docs_row_values(token=True, unicode_str=True, lang="de")[template_name])
                #p(self.configer.docs_row_values(token=True, unicode_str=True, lang="all"))
                #sys.exit()
                for item1, item2 in zip(self.configer.docs_row_values(token=True, unicode_str=True, lang=language)[template_name], db.getall("documents")):
                    if len(item1)!=len(item2):
                        assert False
                    for i1,i2 in zip(item1, item2):
                        if isinstance(i1, (list,tuple,dict)):
                            # #p(i1)
                            i2= json.loads(i2)
                            i2 = [token[0] for sent_container in i2 for token in sent_container[0] ]
                            i1 = "".join(i1)
                            i2 = "".join(i2)
                            if i1!=i2:
                                str_len1 = len(i1)
                                str_len2 = len(i2)
                                percent = int((str_len1 *20)/100)
                                distance = levenstein(i1, i2)
                                #p(abs(str_len1-str_len2), "abs(str_len1-str_len2)")
                                #p((str_len1,percent), "percent")
                                if (abs(str_len1-str_len2) <= 10) and (distance <= percent):
                                    assert True
                                else:
                                    #p(abs(str_len1-str_len2), "abs(str_len1-str_len2)")
                                    #p((str_len1,percent), "percent")
                                    assert False
                            else:
                                assert True
                        else:
                            if  i1 == False :
                                i1=0
                            if  i1 == True :
                                i1=1
                            if unicode(i1) != unicode(i2):
                                #p((i1, i2), "i1, i2", c="r")
                                assert False
                #sys.exit()
            elif db_type == "stats":
                ### Here for stats
                pass
                #p((db.rownum("replications"), db.rownum("reduplications"), db.rownum("baseline")))
                assert db.rownum("replications") > 1
                assert db.rownum("reduplications") > 1
                assert db.rownum("baseline") > 1





    @attr(status='stable')
    #@wipd
    def test_create_all_test_cases_for_diff_fileformats_502(self):
        self.prj_folder()
        configer = TestsConfiger(mode=self.mode)
        abs_path_to_storage_place=self.tempdir_project_folder

        #sys.exit()
        #configer.create_testsets_in_diff_file_formats(rewrite=True,abs_path_to_storage_place=abs_path_to_storage_place)  
        returned_flags = set(list(configer.create_testsets_in_diff_file_formats(rewrite=False,abs_path_to_storage_place=abs_path_to_storage_place)))
        #p(returned_flags)
        if  not (len(returned_flags) > 1) or True not in returned_flags:
           return False
        #sys.exit()
        for  file_format, test_sets in configer.types_folder_names_of_testsets.iteritems():
            for  name_of_test_set, folder_for_test_set in test_sets.iteritems():
                if file_format == "txt":
                    continue

                if file_format == "sqlite":
                    continue
                abs_path_to_current_test_case = os.path.join(abs_path_to_storage_place, configer._path_to_testsets["blogger"], folder_for_test_set)
                #p(abs_path_to_current_test_case, c="r")

                if not os.path.isdir(abs_path_to_current_test_case):
                    os.makedirs(abs_path_to_current_test_case)


                #p(configer._types_folder_names_of_testsets)
                path_to_txt_corpus = os.path.join(configer.path_to_zas_rep_tools,configer._path_to_testsets["blogger"] , configer._types_folder_names_of_testsets["txt"][name_of_test_set] )
                #p(path_to_txt_corpus)
                reader_txt = Reader(path_to_txt_corpus, "txt", regex_template="blogger",send_end_file_marker=False, mode=self.mode)
                reader_current_set = Reader(abs_path_to_current_test_case, file_format, send_end_file_marker=False, mode=self.mode)
                #p((list(reader_txt.getlazy()), ))
                data_from_txt = defaultdict(list)
                data_from_current_set = defaultdict(list)
                for item in reader_txt.getlazy():
                    for k,v in item.iteritems():
                        if unicode(v).isnumeric():
                            v = int(v)
                        data_from_txt[k].append(v)
                        

                for item in reader_current_set.getlazy():
                    for k,v in item.iteritems():
                        if unicode(v).isnumeric():
                            v = int(v)
                        data_from_current_set[k].append(v)
                
                for col in self.configer.columns_in_doc_table["blogger"]:
                   #p(col)
                   if col != "rowid":
                       for txt_item, current_set_item in zip(sorted(data_from_txt[col]),sorted(data_from_current_set[col])):
                            #p((repr(txt_item), repr(current_set_item)))
                            if txt_item != current_set_item:
                                assert False



    @attr(status='stable')
    #@wipd
    def test_create_test_data_503(self):
        self.prj_folder()
        #abs_path_to_storage_place=os.path.join(self.path_to_zas_rep_tools, self.path_to_testdbs)
        abs_path_to_storage_place=self.tempdir_project_folder
        configer = TestsConfiger(mode=self.mode, rewrite=False)
        configer.create_test_data(abs_path_to_storage_place= abs_path_to_storage_place, use_original_classes=True,
                            status_bar=True, corp_log_ignored=True,corp_lang_classification=True,
                            corp_pos_tagger=False, corp_sentiment_analyzer=False,  use_test_pos_tagger=True)
        #p(os.listdir(abs_path_to_storage_place))

        # 1
        ###DBs
        ### Check Number of created DBs
        created_dbs = [filename for filename in os.listdir(abs_path_to_storage_place) if ".db" in filename]
        number_db_which_should_be_created = len(list(NestedDictValues(self.configer._test_dbs)))
        #p(created_dbs)

        # 2
        ## Other OutputFiles
        ### Check Number of Created ZIP Archive 
        created_zips = [filename for filename in os.listdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets["blogger"])) if ".zip" in filename]
        created_folders = [filename for filename in os.listdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets["blogger"])) if os.path.isdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets["blogger"],  filename))]

        if len(created_zips) != len(created_folders):
            assert False

        for folder in created_folders:
            for folder_for_corpus_set in os.listdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets["blogger"], folder)):
                #p((folder_for_corpus_set), "folder_for_corpus_set", c="r")
                if folder == "sqlite":
                    extention = "db"
                else:
                    extention = folder
                files = [file for file in os.listdir(os.path.join(abs_path_to_storage_place, configer._path_to_testsets["blogger"], folder, folder_for_corpus_set)) if extention in file ] #
                if len(files)== 0:
                    #p((folder,extention, files ))
                    assert False


    # #@attr(status='stable')
    # #@wipd
    # def test_get_user_data_for_error_tracking(self):
    #     configer = TestsConfiger(mode=self.mode)        
        
    #     #p(configer._cli_menu_error_agreement())
    #     #p(configer._user_data)

    #     #p(configer._cli_menu_get_from_user_twitter_credentials())
    #     #p(configer._user_data)

    #     #p(configer._cli_menu_get_from_user_emails())
    #     #p(configer._user_data)

    #     # p(configer._cli_menu_get_from_user_project_folder())
    #     # p(configer._user_data)

     
    #     #p(configer._user_data.clean())
    #     # p(configer._user_data)

    #     #configer.get_data_from_user()
    #     # p(configer._user_data)

    #     #configer.get_data_from_user(rewrite=True)
    #     #p(configer._user_data)

    #     # configer.get_data_from_user("email", rewrite=True)
    #     # p(configer._user_data)



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







