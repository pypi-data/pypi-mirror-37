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
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree 
import sys

from zas_rep_tools.src.classes.exporter import Exporter
from zas_rep_tools.src.classes.reader import Reader
#from zas_rep_tools.src.classes.configer import Configer
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester




class TestZAScorpusExporterExporter(BaseTester,unittest.TestCase):
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




    ##### xx :0== ######


    @attr(status='stable')
    #@wipd
    def test_exporter_initialisation_with_list_000(self):
        #self.prj_folder()
        self.blogger_lists()
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)
        exporter.should.be.a(Exporter)

        

    @attr(status='stable')
    #@wipd
    def test_exporter_initialisation_with_reader_obj_001(self):
        self.blogger_corpus()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", regex_template="blogger", mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)
        exporter.should.be.a(Exporter)


    ##### throws_exceptions:050  ######




#################################Beginn##############################################
############################INTERN METHODS###########################################
#####################################################################################

###################    :100############################################ 

    ###### ***** ######

    #@attr(status='stable')
    #@wipd
    #def test_XXX_name_100(self):
    ##self.logger_initialisation()
    #   pass

    ###### ***** ######


    ###### ***** ######






#################################END#################################################
############################INTERN METHODS###########################################
#####################################################################################








#################################Beginn##############################################
############################EXTERN METHODS###########################################
#####################################################################################


###################    :500############################################ 
    ###### ***** ######
   

   

    @attr(status='stable')
    #@wipd
    def test_export_to_csv_from_list_000(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)


        exporter.tocsv(self.tempdir_project_folder, "blogger_corpus",self.fieldnames, rows_limit_in_file=1)
        
        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".csv" in item:
                i+=1

        #p((len(self.input_list_fake_blogger_corpus), i))
        if len(self.input_list_fake_blogger_corpus) != i:
            assert False


    @attr(status='stable')
    #@wipd
    def test_export_to_csv_from_reader_001(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", send_end_file_marker=False, regex_template="blogger", mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)

        exporter.tocsv(self.tempdir_project_folder, "blogger_corpus",self.fieldnames, rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".csv" in item:
                i+=1

        #p(list(reader.getlazy()))
        if len(list(reader.getlazy())) != i:
            assert False




    @attr(status='stable')
    #@wipd
    def test_export_to_xml_from_list_002(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        #real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/xml")
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)
        #exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)

        exporter.toxml(self.tempdir_project_folder, "blogger_corpus", rows_limit_in_file=1)
        #exporter.toxml(real_fold, "blogger_corpus", rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".xml" in item:
                i+=1

        if len(self.input_list_fake_blogger_corpus) != i:
            assert False


    @attr(status='stable')
    #@wipd
    def test_export_to_xml_from_reader_003(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt",send_end_file_marker=False, regex_template="blogger", mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)

        exporter.toxml(self.tempdir_project_folder, "blogger_corpus", rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".xml" in item:
                i+=1


        if len(list(reader.getlazy())) != i:
            assert False






    @attr(status='stable')
    #@wipd
    def test_export_to_json_from_list_004(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        #real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/json")
        #exporter = Exporter( , mode="dev", rewrite=True)
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode, rewrite=True, silent_ignore = True)
        exporter.tojson(self.tempdir_project_folder, "blogger_corpus", rows_limit_in_file=1)
        #exporter.tojson(real_fold, "blogger_corpus", rows_limit_in_file=1)
        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".json" in item:
                i+=1

        #p((len(self.input_list_fake_blogger_corpus), i, j))
        if len(self.input_list_fake_blogger_corpus) != i:
            assert False




    @attr(status='stable')
    #@wipd
    def test_export_to_json_from_reader_005(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", send_end_file_marker=False,regex_template="blogger", mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)

        exporter.tojson(self.tempdir_project_folder, "blogger_corpus", rows_limit_in_file=1)

        i=0
        for item in os.listdir(self.tempdir_project_folder):
            if ".json" in item:
                i+=1

        #p((len(self.input_list_fake_blogger_corpus), i))
        if len(list(reader.getlazy())) != i:
            assert False





    @attr(status='stable')
    #@wipd
    def test_export_to_sqlite_from_list_006(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        #real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/")
        exporter = Exporter(self.input_list_fake_blogger_corpus, mode=self.mode)

        dbname = "blogger_corpus"
        #p(self.fieldnames)
        exporter.tosqlite(self.tempdir_project_folder, dbname, self.fieldnames)
        #exporter.tosqlite(real_fold, dbname, self.fieldnames)

 
        for item in os.listdir(self.tempdir_project_folder):
            if ".db" in item:
                if dbname not in item:
                    assert False




    @attr(status='stable')
    #@wipd
    def test_export_to_sqlite_from_reader_007(self):
        self.blogger_corpus()
        self.prj_folder()
        self.blogger_lists()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", send_end_file_marker=False,regex_template="blogger", mode=self.mode)
        exporter = Exporter(reader.getlazy(), mode=self.mode)
        dbname = "blogger_corpus"

        exporter.tosqlite(self.tempdir_project_folder, dbname, self.fieldnames)

 
        for item in os.listdir(self.tempdir_project_folder):
            if ".db" in item:
                if dbname not in item:
                    assert False



    # #@attr(status='stable')
    # @wipd
    # def test_export_to_json_from_reader_(self):
    #     real_fold = os.path.join(self.path_to_zas_rep_tools, "data/tests_data/Corpora/BloggerCorpus/xml")
    #     reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_hightrepetativ_set), "txt", regex_template="blogger", mode=self.mode)
    #     exporter = Exporter(reader.getlazy())

    #     exporter.tojson(real_fold, "blogger_corpus", rows_limit_in_file=100)





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







