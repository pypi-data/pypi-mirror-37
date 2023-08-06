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
import json
import csv
from collections import Counter, defaultdict


#from zas_rep_tools.src.classes.configer import Configer
from zas_rep_tools.src.classes.stats import Stats
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester
import  zas_rep_tools.src.utils.db_helper as db_helper



import platform
if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama



class TestZASstatsStats(BaseTester,unittest.TestCase):
    #_multiprocess_can_split_ = True
    _multiprocess_shared_  = True
    #@classmethod 
    def setUp(self):
        super(type(self), self).setUp()



        ########### EN ##############
        self.test_dict_row_en_1 = {u'star_constellation': u'lion', u'text': u'[[[["I", "PRP"], ["loved", "VBD"], ["it", "PRP"], [".", "symbol"]], ["positive", 0.7]], [[["But", "CC"], ["it", "PRP"], ["was", "VBD"], ["also", "RB"], ["verrrryyyyy", "JJ"], ["vvveRRRRRRrry", "NNP"], ["very", "RB"], ["piiiiiiiiity", "JJ"], ["pity", "NN"], ["pity", "NN"], ["piiitttyyy", "NN"], ["for", "IN"], ["me", "PRP"], ["......", "symbol"], [":-(((((", "EMOASC"], ["@real_trump", "mention"], ["#sheetlife", "hashtag"], ["#readytogo", "hashtag"], ["http://www.absurd.com", "URL"]], ["negative", -0.1875]]]', u'age': 37, u'working_area': u'IT', u'rowid': 1, u'gender': u'w', u'id': 1111}
        self.test_dict_row_en_2 = {u'star_constellation': u'lion', u'text': u'[[[["Tiny", "JJ"], ["model", "NN"], [",", "symbol"], ["but", "CC"], ["a", "DT"], ["big", "JJ"], ["big", "JJ"], ["big", "JJ"], ["explaaaaanation", "NN"], [".", "symbol"]], ["neutral", 0.0]], [[["Riiiiiight", "UH"], ["?", "symbol"]], ["neutral", 0.0]], [[["What", "WP"], ["do", "VBP"], ["youuuuuu", "PRP"], ["think", "VB"], ["about", "IN"], ["it", "PRP"], ["????", "symbol"]], ["neutral", 0.0]]]', u'age': 35, u'working_area': u'Air Industry', u'rowid': 5, u'gender': u'w', u'id': 5555}


        ########## DE ###############
        self.test_dict_row_de_1 = {u'star_constellation': u'fish', u'text': u'[[[["Klitze", "NN"], ["kliiiitze", "VMFIN"], ["kleEEEEine", "NE"], ["kleinnne", "ADJA"], ["\\u00dcberaschung", "NN"], [".", "symbol"]], ["neutral", 0.0]], [[["Trotzdem", "PAV"], ["hat", "VAFIN"], ["sie", "PPER"], ["mich", "PPER"], ["gl\\u00fccklich", "ADJD"], ["gemacht", "VVPP"], ["!", "symbol"], [":-))))", "EMOASC"], ["-)))", "EMOASC"]], ["positive", 0.5]]]', u'age': 23, u'working_area': u'Care', u'rowid': 8, u'gender': u'm', u'id': 8888}
        self.test_dict_row_de_2 = {u'star_constellation': u'aquarius', u'text': u'[[[["einen", "ART"], ["wundersch\\u00f6nen", "ADJA"], ["Taaaaaagggggg", "NN"], ["w\\u00fcnsche", "VVFIN"], ["ich", "PPER"], ["euch", "PRF"], [".", "symbol"]], ["neutral", 0.0]], [[["Genieeeeeeeeeeesst", "NN"], ["geniiiiiiiiiiiiist", "VVFIN"], ["das", "ART"], ["Leben", "NN"], [".", "symbol"]], ["neutral", 0.0]], [[["Bleeeeeeeeibt", "NN"], ["bleeeeibt", "VVFIN"], ["Huuuuuuuuuuuungrig", "NN"], [".", "symbol"], ["\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00", "EMOIMG"], ["\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08", "EMOIMG"]], ["neutral", 0.0]]]', u'age': 22, u'working_area': u'Finance', u'rowid': 9, u'gender': u'w', u'id': 9999}
    

        self.docs_ids = {
            self.test_dict_row_en_1["id"]:self.test_dict_row_en_1,
            self.test_dict_row_en_2["id"]:self.test_dict_row_en_2,
            self.test_dict_row_de_1["id"]:self.test_dict_row_de_1,
            self.test_dict_row_de_2["id"]:self.test_dict_row_de_2,
            }

        self.gold_standard_data = {
                            "lower":{
                                    "repl":["rep_lower",""],
                                    "redu": [],
                                    },
                            }

        self.path_to_stats_test_data = "data/tests_data/stats/"



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
    def test_initialization_of_the_stats_instance_000(self):
        stats = Stats(mode=self.mode)
        stats.should.be.a(Stats)

        

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
    @attr(status='stable')
    #@wipd
    def test_new_plaintext_stats_initialization_500(self):
        self.prj_folder()
        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        stats = Stats(mode=self.mode)
        #stats = Corpus(logger_level=logging.DEBUG)
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, baseline_delimiter="++")
        #p(stats.statsdb.get_all_attr())
        assert stats.exist()
   
    @attr(status='stable')
    #@wipd
    def test_new_encrypted_stats_initialization_501(self):
        self.prj_folder()
        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"


        stats = Stats(mode=self.mode)
        #stats = Corpus(logger_level=logging.DEBUG)
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
   
        assert stats.exist()
        
        

    @attr(status='stable')
    #@wipd
    def test_open_plaintext_blogger_stats_502(self):
        self.prj_folder()
        self.test_dbs()
        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"


        stats = Stats(mode=self.mode)
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_en))
  
        #p(stats.statsdb.get_all_attr("main"))
        stats.statsdb.get_all_attr("main")['name'].should.be.equal(name)
        #stats.statsdb.get_all_attr("main")['language'].should.be.equal(language)
        stats.statsdb.get_all_attr("main")['visibility'].should.be.equal(visibility)
        #stats.statsdb.get_all_attr("main")['platform_name'].should.be.equal(platform_name)
        stats.statsdb.get_all_attr("main")['typ'].should.be.equal(typ)
        stats.statsdb.get_all_attr("main")['id'].should.be.equal(stats_id)
        stats.statsdb.get_all_attr("main")['version'].should.be.equal(version)

        assert stats.exist()
   
    @attr(status='stable')
    #@wipdl
    def test_open_encrypted_twitter_stats_503(self):
        self.prj_folder()
        self.test_dbs()
        name = self.configer.init_info_data["twitter"]["name"]
        language = self.configer.init_info_data["twitter"]["language"]
        visibility = self.configer.init_info_data["twitter"]["visibility"]
        platform_name = self.configer.init_info_data["twitter"]["platform_name"]
        license = self.configer.init_info_data["twitter"]["license"]
        template_name = self.configer.init_info_data["twitter"]["template_name"]
        version = self.configer.init_info_data["twitter"]["version"]
        source = self.configer.init_info_data["twitter"]["source"]
        encryption_key = self.configer.init_info_data["twitter"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["twitter"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["twitter"]["id"]["stats"]
        typ= "stats"
        #p(encryption_key)

        stats = Stats(mode=self.mode)
        stats.open(os.path.join(self.tempdir_testdbs,self.db_twitter_encrypted_stats_de), encryption_key=encryption_key)
    

    
        stats.statsdb.get_all_attr("main")['name'].should.be.equal(name)
        #stats.statsdb.get_all_attr("main")['language'].should.be.equal(language)
        stats.statsdb.get_all_attr("main")['visibility'].should.be.equal(visibility)
        #stats.statsdb.get_all_attr("main")['platform_name'].should.be.equal(platform_name)
        stats.statsdb.get_all_attr("main")['typ'].should.be.equal(typ)
        stats.statsdb.get_all_attr("main")['id'].should.be.equal(stats_id)
        stats.statsdb.get_all_attr("main")['version'].should.be.equal(version)

        assert stats.exist()
   

    @attr(status='stable')
    #@wipd
    def test_attach_corpdb_504(self):
        self.prj_folder()
        self.test_dbs()
        

        #p(encryption_key)
    

        ### plaintext
        stats = Stats(mode=self.mode)
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_en))

        stats.attach_corpdb(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))

        assert stats.exist()
        #p(stats.attached_corpdb_number())
        assert stats.attached_corpdb_number() == 1


        ### excrypted
        encryption_key_corp = self.configer.init_info_data["twitter"]["encryption_key"]["corpus"]
        encryption_key_stats = self.configer.init_info_data["twitter"]["encryption_key"]["stats"]
        stats = Stats(mode=self.mode)
        stats.open(os.path.join(self.tempdir_testdbs,self.db_twitter_encrypted_stats_de), encryption_key=encryption_key_stats)

        stats.attach_corpdb(os.path.join(self.tempdir_testdbs,self.db_twitter_encrypted_corp_de), encryption_key=encryption_key_corp)

        assert stats.exist()
        #assert stats.attached_corpdb_number() == 1











    ###################    :600############################################ 
    @attr(status='stable')
    #@wipd
    def test_extract_repl_lower_case_600(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode, )#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)

        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        #p(stats.statsdb, "stats.statsdb")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()

        ## DE####

        ### ROW 1 ###
        extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_de_1["text"]))
        #p(repl_free_text_container, "repl_free_text_container", c="m")
        #p([t[0] for i in json.loads(self.test_dict_row_de_1["text"]) for t in i[0]])
        # p((len(extracted_repl_in_text_container),extracted_repl_in_text_container), "extracted_repl_in_text_container")
        # p((len(repl_free_text_container),repl_free_text_container), "repl_free_text_container")
        # p((len(rle_for_repl_in_text_container),rle_for_repl_in_text_container), "rle_for_repl_in_text_container")

        extracted_repl_in_text_container.should.be.equal([['', [(u'i', 4, 2)], [(u'e', 5, 2)], [(u'n', 3, 4)], '', ''], ['', '', '', '', '', '', '', [(u')', 4, 2)], [(u')', 3, 1)]]])
        repl_free_text_container.should.be.equal([[u'klitze', u'klitze', u'kleine', u'kleine', u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']])
        rle_for_repl_in_text_container.should.be.equal([['', u'kli^4tze', u'kle^5ine', u'klein^3e', '', ''], ['', '', '', '', '', '', '', u':-)^4', u'-)^3']])
        #repl_free_de_row_lowercased_1 = [[u'klitze', u'klitze', u'kleine', u'kleine', u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]

        

        ### ROW 2 ###
        extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_de_2["text"]) )
        
        # p([t[0] for i in json.loads(self.test_dict_row_de_2["text"]) for t in i[0]])
        # p((len(extracted_repl_in_text_container),extracted_repl_in_text_container), "extracted_repl_in_text_container")
        # p((len(repl_free_text_container),repl_free_text_container), "repl_free_text_container")
        # p((len(rle_for_repl_in_text_container),rle_for_repl_in_text_container), "rle_for_repl_in_text_container")

        extracted_repl_in_text_container.should.be.equal([['', '', [(u'a', 6, 1), (u'g', 6, 2)], '', '', '', ''], [[(u'e', 11, 4)], [(u'i', 13, 3)], '', '', ''], [[(u'e', 8, 2)], [(u'e', 4, 2)], [(u'u', 12, 1)], '', [(u'\U0001f600', 5, 0)], [(u'\U0001f308', 7, 0)]]])
        repl_free_text_container.should.be.equal([[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [u'bleibt', u'bleibt', u'hungrig', u'.', u'\U0001f600', u'\U0001f308']])
        rle_for_repl_in_text_container.should.be.equal([['', '', u'ta^6g^6', '', '', '', ''], [u'genie^11s^2t', u'geni^13st', '', '', ''], [u'ble^8ibt', u'ble^4ibt', u'hu^12ngrig', '', u'\U0001f600^5', u'\U0001f308^7']])
        #repl_free_de_row_lowercased_2 = [[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [u'bleibt', u'bleibt', u'hungrig', u'.', u'\U0001f600', u'\U0001f308']]

        
        # ########### EN ##############

        ### ROW 1 ###
        extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_en_1["text"]) )
        #p([t[0] for i in json.loads(self.test_dict_row_en_1["text"]) for t in i[0]])
        # p((len(extracted_repl_in_text_container),extracted_repl_in_text_container), "extracted_repl_in_text_container")
        # p((len(repl_free_text_container),repl_free_text_container), "repl_free_text_container")
        # p((len(rle_for_repl_in_text_container),rle_for_repl_in_text_container), "rle_for_repl_in_text_container")

        extracted_repl_in_text_container.should.be.equal([['', '', '', ''], ['', '', '', '', [(u'r', 4, 2), (u'y', 5, 3)], [(u'v', 3, 0), (u'r', 8, 2)], '', [(u'i', 9, 1)], '', '', [(u'i', 3, 1), (u't', 3, 2), (u'y', 3, 3)], '', '', [(u'.', 6, 0)], [(u'(', 5, 2)], '', '', '', '']])
        repl_free_text_container.should.be.equal([[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', u'very', u'very', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']])
        rle_for_repl_in_text_container.should.be.equal([['', '', '', ''], ['', '', '', '', u'ver^4y^5', u'v^3er^8y', '', u'pi^9ty', '', '', u'pi^3t^3y^3', '', '', u'.^6', u':-(^5', '', '', '', '']])
        #repl_free_en_row_lowercased_1 =    [[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', u'very', u'very', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]

        
        ### ROW 2 ###
        extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_en_2["text"]) )
        # p([t[0] for i in json.loads(self.test_dict_row_en_2["text"]) for t in i[0]])
        # p((len(extracted_repl_in_text_container),extracted_repl_in_text_container), "extracted_repl_in_text_container")
        # p((len(repl_free_text_container),repl_free_text_container), "repl_free_text_container")
        # p((len(rle_for_repl_in_text_container),rle_for_repl_in_text_container), "rle_for_repl_in_text_container")

        extracted_repl_in_text_container.should.be.equal([['', '', '', '', '', '', '', '', [(u'a', 5, 4)], ''], [[(u'i', 6, 1)], ''], ['', '', [(u'u', 6, 2)], '', '', '', [(u'?', 4, 0)]]])
        repl_free_text_container.should.be.equal([[u'tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']])
        rle_for_repl_in_text_container.should.be.equal([['', '', '', '', '', '', '', '', u'expla^5nation', ''], [u'ri^6ght', ''], ['', '', u'you^6', '', '', '', u'?^4']])
        #repl_free_en_row_lowercased_1 = [[u'tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]

    



    @attr(status='stable')
    #@wipd
    def test_extract_repl_case_sensitiv_601(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)

        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, case_sensitiv=True, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        #p(stats.statsdb, "stats.statsdb")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()

        ### DE####

        ### ROW 1 ###
        extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_de_1["text"]) )
        # p([t[0] for i in json.loads(self.test_dict_row_de_1["text"]) for t in i[0]])
        # p((len(extracted_repl_in_text_container),extracted_repl_in_text_container), "extracted_repl_in_text_container")
        # p((len(repl_free_text_container),repl_free_text_container), "repl_free_text_container")
        # p((len(rle_for_repl_in_text_container),rle_for_repl_in_text_container), "rle_for_repl_in_text_container")

        extracted_repl_in_text_container.should.be.equal([['', [(u'i', 4, 2)], [(u'E', 4, 3)], [(u'n', 3, 4)], '', ''], ['', '', '', '', '', '', '', [(u')', 4, 2)], [(u')', 3, 1)]]])
        repl_free_text_container.should.be.equal([[u'Klitze', u'klitze', u'kleEine', u'kleine', u'\xdcberaschung', u'.'], [u'Trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']])
        rle_for_repl_in_text_container.should.be.equal([['', u'kli^4tze', u'kleE^4ine', u'klein^3e', '', ''], ['', '', '', '', '', '', '', u':-)^4', u'-)^3']])
        
        ### ROW 2 ###
        extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_de_2["text"]) )
        # p([t[0] for i in json.loads(self.test_dict_row_de_2["text"]) for t in i[0]])
        # p((len(extracted_repl_in_text_container),extracted_repl_in_text_container), "extracted_repl_in_text_container")
        # p((len(repl_free_text_container),repl_free_text_container), "repl_free_text_container")
        # p((len(rle_for_repl_in_text_container),rle_for_repl_in_text_container), "rle_for_repl_in_text_container")

        extracted_repl_in_text_container.should.be.equal([['', '', [(u'a', 6, 1), (u'g', 6, 2)], '', '', '', ''], [[(u'e', 11, 4)], [(u'i', 13, 3)], '', '', ''], [[(u'e', 8, 2)], [(u'e', 4, 2)], [(u'u', 12, 1)], '', [(u'\U0001f600', 5, 0)], [(u'\U0001f308', 7, 0)]]])
        repl_free_text_container.should.be.equal([[u'einen', u'wundersch\xf6nen', u'Tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'Geniest', u'genist', u'das', u'Leben', u'.'], [u'Bleibt', u'bleibt', u'Hungrig', u'.', u'\U0001f600', u'\U0001f308']])
        rle_for_repl_in_text_container.should.be.equal([['', '', u'Ta^6g^6', '', '', '', ''], [u'Genie^11s^2t', u'geni^13st', '', '', ''], [u'Ble^8ibt', u'ble^4ibt', u'Hu^12ngrig', '', u'\U0001f600^5', u'\U0001f308^7']])
        

        # ########### EN ##############

        ### ROW 1 ###
        extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_en_1["text"]) )
        # p([t[0] for i in json.loads(self.test_dict_row_en_1["text"]) for t in i[0]]) #[u'I', u'loved', u'it', u'.', u'But', u'it', u'was', u'also', u'verrrryyyyy', u'vvveRRRRRRrry', u'very', u'piiiiiiiiity', u'pity', u'pity', u'piiitttyyy', u'for', u'me', u'......', u':-(((((', u'@real_trump', u'#sheetlife', u'#readytogo', u'http://www.absurd.com']
        # p((len(extracted_repl_in_text_container),extracted_repl_in_text_container), "extracted_repl_in_text_container")
        # p((len(repl_free_text_container),repl_free_text_container), "repl_free_text_container")
        # p((len(rle_for_repl_in_text_container),rle_for_repl_in_text_container), "rle_for_repl_in_text_container")

        extracted_repl_in_text_container.should.be.equal([['', '', '', ''], ['', '', '', '', [(u'r', 4, 2), (u'y', 5, 3)], [(u'v', 3, 0), (u'R', 6, 2)], '', [(u'i', 9, 1)], '', '', [(u'i', 3, 1), (u't', 3, 2), (u'y', 3, 3)], '', '', [(u'.', 6, 0)], [(u'(', 5, 2)], '', '', '', '']])
        repl_free_text_container.should.be.equal([[u'I', u'loved', u'it', u'.'], [u'But', u'it', u'was', u'also', u'very', u'veRry', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']])
        rle_for_repl_in_text_container.should.be.equal([['', '', '', ''], ['', '', '', '', u'ver^4y^5', u'v^3eR^6r^2y', '', u'pi^9ty', '', '', u'pi^3t^3y^3', '', '', u'.^6', u':-(^5', '', '', '', '']])
        
        ### ROW 2 ###
        extracted_repl_in_text_container,  repl_free_text_container, rle_for_repl_in_text_container = stats.extract_replications(json.loads(self.test_dict_row_en_2["text"]) )
        # p([t[0] for i in json.loads(self.test_dict_row_en_2["text"]) for t in i[0]]) #[u'Tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explaaaaanation', u'.', u'Riiiiiight', u'?', u'What', u'do', u'youuuuuu', u'think', u'about', u'it', u'????']
        # p((len(extracted_repl_in_text_container),extracted_repl_in_text_container), "extracted_repl_in_text_container")
        # p((len(repl_free_text_container),repl_free_text_container), "repl_free_text_container")
        # p((len(rle_for_repl_in_text_container),rle_for_repl_in_text_container), "rle_for_repl_in_text_container")

        extracted_repl_in_text_container.should.be.equal([['', '', '', '', '', '', '', '', [(u'a', 5, 4)], ''], [[(u'i', 6, 1)], ''], ['', '', [(u'u', 6, 2)], '', '', '', [(u'?', 4, 0)]]])
        repl_free_text_container.should.be.equal([[u'Tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'Right', u'?'], [u'What', u'do', u'you', u'think', u'about', u'it', u'?']])
        rle_for_repl_in_text_container.should.be.equal([['', '', '', '', '', '', '', '', u'expla^5nation', ''], [u'Ri^6ght', ''], ['', '', u'you^6', '', '', '', u'?^4']])


  



    @attr(status='stable')
    #@wipd
    def test_insert_repl_into_db_lower_case_602(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)


        #p(stats.statsdb, "stats.statsdb")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))




        ## DE####
        import Stemmer
        stemmer = Stemmer.Stemmer("de")
        ### ROW 1 ###
        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()

        text_list = [self.test_dict_row_de_1["id"],self.test_dict_row_de_1["text"]]
        rle_for_repl_in_text_container = [['', u'kli^4tze', u'kle^5ine', u'klein^3e', '', ''], ['', '', '', '', '', '', '', u':-)^4', u'-)^3']]
        extracted_repl_in_text_container = [['', [(u'i', 4, 2)], [(u'e', 5, 2)], [(u'n', 3, 4)], '', ''], ['', '', '', '', '', '', '', [(u')', 4, 2)], [(u')', 3, 1)]]]
        repl_free_text_container = [[u'klitze', u'klitze', u'kleine', u'kleine', u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]
        redu_free_text_container = [[(u'klitze', {u'klitze': 1, u'kli^4tze': 1}), (u'kleine', {u'kle^5ine': 1, u'klein^3e': 1}), u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        #p(stemmed_text_container ,"stemmed_text_container ")
        mapping_redu = [[0, 2, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]]
        stats.insert_repl_into_db( text_list,json.loads(self.test_dict_row_de_1["text"]),extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container,redu_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")

        #p(list(stats.statsdb.getall("replications")))
        right_output = [
                            (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'), 
                            (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), 
                            (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), 
                            (4, 8888, u'[4, 9]', u'[1, 7]', u'[1, 7]', u':-)', u':-)^4', u':-)', u')', 4, 2, None, u'EMOASC', u'["positive", 0.5]', u'sie', u'["PPER", null, "sie"]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "glucklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u'-)', u'["EMOASC", null, "-)"]', None, None, None, None, None, None, None, None), 
                            (5, 8888, u'[4, 9]', u'[1, 8]', u'[1, 8]', u'-)', u'-)^3', u'-)', u')', 3, 1, None, u'EMOASC', u'["positive", 0.5]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "glucklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', None, None, None, None, None, None, None, None, None, None)]

        list(stats.statsdb.getall("replications")).should.be.equal(right_output)


        # # ### ROW 2 ###
        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()

        text_list = [self.test_dict_row_de_2["id"],self.test_dict_row_de_2["text"]]
        rle_for_repl_in_text_container = [['', '', u'ta^6g^6', '', '', '', ''], [u'genie^11s^2t', u'geni^13st', '', '', ''], [u'ble^8ibt', u'ble^4ibt', u'hu^12ngrig', '', u'\U0001f600^5', u'\U0001f308^7']]
        extracted_repl_in_text_container = [['', '', [(u'a', 6, 1), (u'g', 6, 2)], '', '', '', ''], [[(u'e', 11, 4)], [(u'i', 13, 3)], '', '', ''], [[(u'e', 8, 2)], [(u'e', 4, 2)], [(u'u', 12, 1)], '', [(u'\U0001f600', 5, 0)], [(u'\U0001f308', 7, 0)]]]
        repl_free_text_container = [[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [u'bleibt', u'bleibt', u'hungrig', u'.', u'\U0001f600', u'\U0001f308']]
        redu_free_text_container = [[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [(u'bleibt', {u'ble^4ibt': 1, u'ble^8ibt': 1}), u'hungrig', u'.', u'\U0001f600', u'\U0001f308']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [0, 2, 3, 4, 5]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list,json.loads(self.test_dict_row_de_2["text"]),extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container,redu_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")
        #p(list(stats.statsdb.getall("replications")))
        right_output = [(1, 9999, u'[7, 5, 5]', u'[0, 2]', u'[0, 2]', u'tag', u'ta^6g^6', u'tag', u'a', 6, 1, None, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, u'einen', u'["ART", null, "ein"]', u'wundersch\xf6nen', u'["ADJA", null, "wunderschon"]', u'w\xfcnsche', u'["VVFIN", null, "wunsch"]', u'ich', u'["PPER", null, "ich"]', u'euch', u'["PRF", null, "euch"]', u'.', u'["symbol", null, "."]', u'geniest', u'["NN", null, "geni"]'), 
                            (2, 9999, u'[7, 5, 5]', u'[0, 2]', u'[0, 2]', u'tag', u'ta^6g^6', u'tag', u'g', 6, 2, None, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, u'einen', u'["ART", null, "ein"]', u'wundersch\xf6nen', u'["ADJA", null, "wunderschon"]', u'w\xfcnsche', u'["VVFIN", null, "wunsch"]', u'ich', u'["PPER", null, "ich"]', u'euch', u'["PRF", null, "euch"]', u'.', u'["symbol", null, "."]', u'geniest', u'["NN", null, "geni"]'), 
                            (3, 9999, u'[7, 5, 5]', u'[1, 0]', u'[1, 0]', u'geniest', u'genie^11s^2t', u'geni', u'e', 11, 4, None, u'NN', u'["neutral", 0.0]', u'tag', u'["NN", null, "tag"]', u'w\xfcnsche', u'["VVFIN", null, "wunsch"]', u'ich', u'["PPER", null, "ich"]', u'euch', u'["PRF", null, "euch"]', u'.', u'["symbol", null, "."]', u'genist', u'["VVFIN", null, "genist"]', u'das', u'["ART", null, "das"]', u'leben', u'["NN", null, "leb"]', u'.', u'["symbol", null, "."]', u'bleibt', u'["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]'), 
                            (4, 9999, u'[7, 5, 5]', u'[1, 1]', u'[1, 1]', u'genist', u'geni^13st', u'genist', u'i', 13, 3, None, u'VVFIN', u'["neutral", 0.0]', u'w\xfcnsche', u'["VVFIN", null, "wunsch"]', u'ich', u'["PPER", null, "ich"]', u'euch', u'["PRF", null, "euch"]', u'.', u'["symbol", null, "."]', u'geniest', u'["NN", null, "geni"]', u'das', u'["ART", null, "das"]', u'leben', u'["NN", null, "leb"]', u'.', u'["symbol", null, "."]', u'bleibt', u'["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]', u'hungrig', u'["NN", null, "hungrig"]'), 
                            (5, 9999, u'[7, 5, 5]', u'[2, 0]', u'[2, 0]', u'bleibt', u'ble^8ibt', u'bleibt', u'e', 8, 2, u'[2, 0]', u'NN', u'["neutral", 0.0]', u'geniest', u'["NN", null, "geni"]', u'genist', u'["VVFIN", null, "genist"]', u'das', u'["ART", null, "das"]', u'leben', u'["NN", null, "leb"]', u'.', u'["symbol", null, "."]', u'hungrig', u'["NN", null, "hungrig"]', u'.', u'["symbol", null, "."]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', None, None), 
                            (6, 9999, u'[7, 5, 5]', u'[2, 1]', u'[2, 0]', u'bleibt', u'ble^4ibt', u'bleibt', u'e', 4, 2, u'[2, 0]', u'NN', u'["neutral", 0.0]', u'geniest', u'["NN", null, "geni"]', u'genist', u'["VVFIN", null, "genist"]', u'das', u'["ART", null, "das"]', u'leben', u'["NN", null, "leb"]', u'.', u'["symbol", null, "."]', u'hungrig', u'["NN", null, "hungrig"]', u'.', u'["symbol", null, "."]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', None, None), 
                            (7, 9999, u'[7, 5, 5]', u'[2, 2]', u'[2, 1]', u'hungrig', u'hu^12ngrig', u'hungrig', u'u', 12, 1, None, u'NN', u'["neutral", 0.0]', u'genist', u'["VVFIN", null, "genist"]', u'das', u'["ART", null, "das"]', u'leben', u'["NN", null, "leb"]', u'.', u'["symbol", null, "."]', u'bleibt', u'["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]', u'.', u'["symbol", null, "."]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', None, None, None, None), 
                            (8, 9999, u'[7, 5, 5]', u'[2, 4]', u'[2, 3]', u'\U0001f600', u'\U0001f600^5', u'\U0001f600', u'\U0001f600', 5, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'leben', u'["NN", null, "leb"]', u'.', u'["symbol", null, "."]', u'bleibt', u'["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]', u'hungrig', u'["NN", null, "hungrig"]', u'.', u'["symbol", null, "."]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', None, None, None, None, None, None, None, None), 
                            (9, 9999, u'[7, 5, 5]', u'[2, 5]', u'[2, 4]', u'\U0001f308', u'\U0001f308^7', u'\U0001f308', u'\U0001f308', 7, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'bleibt', u'["NN", {"ble^4ibt": 1, "ble^8ibt": 1}, "bleibt"]', u'hungrig', u'["NN", null, "hungrig"]', u'.', u'["symbol", null, "."]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None, None, None)]

        list(stats.statsdb.getall("replications")).should.be.equal(right_output)




        
        # # ########### EN ##############
        stemmer = Stemmer.Stemmer("en")
        # # ### ROW 1 ###
        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()

        text_list = [self.test_dict_row_en_1["id"],self.test_dict_row_en_1["text"]]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', u'ver^4y^5', u'v^3er^8y', '', u'pi^9ty', '', '', u'pi^3t^3y^3', '', '', u'.^6', u':-(^5', '', '', '', '']]
        extracted_repl_in_text_container = [['', '', '', ''], ['', '', '', '', [(u'r', 4, 2), (u'y', 5, 3)], [(u'v', 3, 0), (u'r', 8, 2)], '', [(u'i', 9, 1)], '', '', [(u'i', 3, 1), (u't', 3, 2), (u'y', 3, 3)], '', '', [(u'.', 6, 0)], [(u'(', 5, 2)], '', '', '', '']]
        repl_free_text_container = [[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', u'very', u'very', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]
        redu_free_text_container =[[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', (u'very', {u'very': 1, u'ver^4y^5': 1, u'v^3er^8y': 1}), (u'pity', {u'pity': 2, u'pi^3t^3y^3': 1, u'pi^9ty': 1}), u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]
        mapping_redu = [[0, 1, 2, 3], [0, 1, 2, 3, 4, 7, 11, 12, 13, 14, 15, 16, 17, 18]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list,json.loads(self.test_dict_row_en_1["text"]),extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container,redu_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")
        #p(list(stats.statsdb.getall("replications")))
        right_output = [(1, 1111, u'[4, 14]', u'[1, 4]', u'[1, 4]', u'very', u'ver^4y^5', u'veri', u'r', 4, 2, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), 
                        (2, 1111, u'[4, 14]', u'[1, 4]', u'[1, 4]', u'very', u'ver^4y^5', u'veri', u'y', 5, 3, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), 
                        (3, 1111, u'[4, 14]', u'[1, 5]', u'[1, 4]', u'very', u'v^3er^8y', u'veri', u'v', 3, 0, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), 
                        (4, 1111, u'[4, 14]', u'[1, 5]', u'[1, 4]', u'very', u'v^3er^8y', u'veri', u'r', 8, 2, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), 
                        (5, 1111, u'[4, 14]', u'[1, 7]', u'[1, 5]', u'pity', u'pi^9ty', u'piti', u'i', 9, 1, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), 
                        (6, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u'i', 3, 1, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), 
                        (7, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u't', 3, 2, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), 
                        (8, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u'y', 3, 3, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), 
                        (9, 1111, u'[4, 14]', u'[1, 13]', u'[1, 8]', u'.', u'.^6', u'.', u'.', 6, 0, None, u'symbol', u'["negative", -0.1875]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]', u'#shetlife', u'["hashtag", null, "#shetlif"]', u'#readytogo', u'["hashtag", null, "#readytogo"]', u'http://www.absurd.com', u'["URL", null, "http://www.absurd.com"]'), 
                        (10, 1111, u'[4, 14]', u'[1, 14]', u'[1, 9]', u':-(', u':-(^5', u':-(', u'(', 5, 2, None, u'EMOASC', u'["negative", -0.1875]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u'@real_trump', u'["mention", null, "@real_trump"]', u'#shetlife', u'["hashtag", null, "#shetlif"]', u'#readytogo', u'["hashtag", null, "#readytogo"]', u'http://www.absurd.com', u'["URL", null, "http://www.absurd.com"]', None, None)]

        list(stats.statsdb.getall("replications")).should.be.equal(right_output)


        # # ### ROW 2 ###
        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()

        text_list = [self.test_dict_row_en_2["id"],self.test_dict_row_en_2["text"]]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', u'expla^5nation', ''], [u'ri^6ght', ''], ['', '', u'you^6', '', '', '', u'?^4']]
        extracted_repl_in_text_container = [['', '', '', '', '', '', '', '', [(u'a', 5, 4)], ''], [[(u'i', 6, 1)], ''], ['', '', [(u'u', 6, 2)], '', '', '', [(u'?', 4, 0)]]]
        repl_free_text_container = [[u'tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]
        redu_free_text_container = [[u'tiny', u'model', u',', u'but', u'a', (u'big', {u'big': 3}), u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list ,json.loads(self.test_dict_row_en_2["text"]),extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container,redu_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")
        #p(list(stats.statsdb.getall("replications")))
        right_output = [(1, 5555, u'[8, 2, 7]', u'[0, 8]', u'[0, 6]', u'explanation', u'expla^5nation', u'explan', u'a', 5, 4, None, u'NN', u'["neutral", 0.0]', u'model', u'["NN", null, "model"]', u',', u'["symbol", null, ","]', u'but', u'["CC", null, "but"]', u'a', u'["DT", null, "a"]', u'big', u'["JJ", {"big": 3}, "big"]', u'.', u'["symbol", null, "."]', u'right', u'["UH", null, "right"]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]'), 
                        (2, 5555, u'[8, 2, 7]', u'[1, 0]', u'[1, 0]', u'right', u'ri^6ght', u'right', u'i', 6, 1, None, u'UH', u'["neutral", 0.0]', u'but', u'["CC", null, "but"]', u'a', u'["DT", null, "a"]', u'big', u'["JJ", {"big": 3}, "big"]', u'explanation', u'["NN", null, "explan"]', u'.', u'["symbol", null, "."]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]', u'you', u'["PRP", null, "you"]', u'think', u'["VB", null, "think"]'), 
                        (3, 5555, u'[8, 2, 7]', u'[2, 2]', u'[2, 2]', u'you', u'you^6', u'you', u'u', 6, 2, None, u'PRP', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'right', u'["UH", null, "right"]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]', u'think', u'["VB", null, "think"]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', u'?', u'["symbol", null, "?"]', None, None), 
                        (4, 5555, u'[8, 2, 7]', u'[2, 6]', u'[2, 6]', u'?', u'?^4', u'?', u'?', 4, 0, None, u'symbol', u'["neutral", 0.0]', u'do', u'["VBP", null, "do"]', u'you', u'["PRP", null, "you"]', u'think', u'["VB", null, "think"]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', None, None, None, None, None, None, None, None, None, None)]


        list(stats.statsdb.getall("replications")).should.be.equal(right_output)




        ########################
        ####### many_rows ######
        ########################
        # # ### ROW 1 ###
        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()

        text_list = [self.test_dict_row_en_1["id"],self.test_dict_row_en_1["text"]]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', u'ver^4y^5', u'v^3er^8y', '', u'pi^9ty', '', '', u'pi^3t^3y^3', '', '', u'.^6', u':-(^5', '', '', '', '']]
        extracted_repl_in_text_container = [['', '', '', ''], ['', '', '', '', [(u'r', 4, 2), (u'y', 5, 3)], [(u'v', 3, 0), (u'r', 8, 2)], '', [(u'i', 9, 1)], '', '', [(u'i', 3, 1), (u't', 3, 2), (u'y', 3, 3)], '', '', [(u'.', 6, 0)], [(u'(', 5, 2)], '', '', '', '']]
        repl_free_text_container = [[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', u'very', u'very', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]
        redu_free_text_container = [[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', (u'very', {u'very': 1, u'ver^4y^5': 1, u'v^3er^8y': 1}), (u'pity', {u'pity': 2, u'pi^3t^3y^3': 1, u'pi^9ty': 1}), u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]
        mapping_redu = [[0, 1, 2, 3], [0, 1, 2, 3, 4, 7, 11, 12, 13, 14, 15, 16, 17, 18]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list,json.loads(self.test_dict_row_en_1["text"]),extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container,redu_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")
        #p(list(stats.statsdb.getall("replications")))
        #list(stats.statsdb.getall("replications")).should.be.equal([(1, 1111, u'[1, 4]', u'ver^4y^5', u'very', u'JJ', u'["negative", -0.1875]', u'r', 4, 2, u'.', u'symbol', u'but', u'CC', u'it', u'PRP', u'was', u'VBD', u'also', u'RB', u'very', u'NNP', u'very', u'RB', u'pity', u'JJ', u'pity', u'NN', u'pity', u'NN'), (2, 1111, u'[1, 4]', u'ver^4y^5', u'very', u'JJ', u'["negative", -0.1875]', u'y', 5, 3, u'.', u'symbol', u'but', u'CC', u'it', u'PRP', u'was', u'VBD', u'also', u'RB', u'very', u'NNP', u'very', u'RB', u'pity', u'JJ', u'pity', u'NN', u'pity', u'NN'), (3, 1111, u'[1, 5]', u'v^3er^8y', u'very', u'NNP', u'["negative", -0.1875]', u'v', 3, 0, u'but', u'CC', u'it', u'PRP', u'was', u'VBD', u'also', u'RB', u'very', u'JJ', u'very', u'RB', u'pity', u'JJ', u'pity', u'NN', u'pity', u'NN', u'pity', u'NN'), (4, 1111, u'[1, 5]', u'v^3er^8y', u'very', u'NNP', u'["negative", -0.1875]', u'r', 8, 2, u'but', u'CC', u'it', u'PRP', u'was', u'VBD', u'also', u'RB', u'very', u'JJ', u'very', u'RB', u'pity', u'JJ', u'pity', u'NN', u'pity', u'NN', u'pity', u'NN'), (5, 1111, u'[1, 7]', u'pi^9ty', u'pity', u'JJ', u'["negative", -0.1875]', u'i', 9, 1, u'was', u'VBD', u'also', u'RB', u'very', u'JJ', u'very', u'NNP', u'very', u'RB', u'pity', u'NN', u'pity', u'NN', u'pity', u'NN', u'for', u'IN', u'me', u'PRP'), (6, 1111, u'[1, 10]', u'pi^3t^3y^3', u'pity', u'NN', u'["negative", -0.1875]', u'i', 3, 1, u'very', u'NNP', u'very', u'RB', u'pity', u'JJ', u'pity', u'NN', u'pity', u'NN', u'for', u'IN', u'me', u'PRP', u'.', u'symbol', u':-(', u'EMOASC', u'@real_trump', u'mention'), (7, 1111, u'[1, 10]', u'pi^3t^3y^3', u'pity', u'NN', u'["negative", -0.1875]', u't', 3, 2, u'very', u'NNP', u'very', u'RB', u'pity', u'JJ', u'pity', u'NN', u'pity', u'NN', u'for', u'IN', u'me', u'PRP', u'.', u'symbol', u':-(', u'EMOASC', u'@real_trump', u'mention'), (8, 1111, u'[1, 10]', u'pi^3t^3y^3', u'pity', u'NN', u'["negative", -0.1875]', u'y', 3, 3, u'very', u'NNP', u'very', u'RB', u'pity', u'JJ', u'pity', u'NN', u'pity', u'NN', u'for', u'IN', u'me', u'PRP', u'.', u'symbol', u':-(', u'EMOASC', u'@real_trump', u'mention'), (9, 1111, u'[1, 13]', u'.^6', u'.', u'symbol', u'["negative", -0.1875]', u'.', 6, 0, u'pity', u'NN', u'pity', u'NN', u'pity', u'NN', u'for', u'IN', u'me', u'PRP', u':-(', u'EMOASC', u'@real_trump', u'mention', u'#shetlife', u'hashtag', u'#readytogo', u'hashtag', u'http://www.absurd.com', u'URL'), (10, 1111, u'[1, 14]', u':-(^5', u':-(', u'EMOASC', u'["negative", -0.1875]', u'(', 5, 2, u'pity', u'NN', u'pity', u'NN', u'for', u'IN', u'me', u'PRP', u'.', u'symbol', u'@real_trump', u'mention', u'#shetlife', u'hashtag', u'#readytogo', u'hashtag', u'http://www.absurd.com', u'URL', u'[]', u'[]')])


        # # ### ROW 2 ###
        text_list = [self.test_dict_row_en_2["id"],self.test_dict_row_en_2["text"]]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', u'expla^5nation', ''], [u'ri^6ght', ''], ['', '', u'you^6', '', '', '', u'?^4']]
        extracted_repl_in_text_container = [['', '', '', '', '', '', '', '', [(u'a', 5, 4)], ''], [[(u'i', 6, 1)], ''], ['', '', [(u'u', 6, 2)], '', '', '', [(u'?', 4, 0)]]]
        repl_free_text_container = [[u'tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]
        redu_free_text_container = [[u'tiny', u'model', u',', u'but', u'a', (u'big', {u'big': 3}), u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_repl_into_db(text_list,json.loads(self.test_dict_row_en_2["text"]),extracted_repl_in_text_container, repl_free_text_container, rle_for_repl_in_text_container,redu_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")
        #p(list(stats.statsdb.getall("replications")))
        right_output = [(1, 1111, u'[4, 14]', u'[1, 4]', u'[1, 4]', u'very', u'ver^4y^5', u'veri', u'r', 4, 2, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (
                        2, 1111, u'[4, 14]', u'[1, 4]', u'[1, 4]', u'very', u'ver^4y^5', u'veri', u'y', 5, 3, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (
                        3, 1111, u'[4, 14]', u'[1, 5]', u'[1, 4]', u'very', u'v^3er^8y', u'veri', u'v', 3, 0, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (
                        4, 1111, u'[4, 14]', u'[1, 5]', u'[1, 4]', u'very', u'v^3er^8y', u'veri', u'r', 8, 2, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (
                        5, 1111, u'[4, 14]', u'[1, 7]', u'[1, 5]', u'pity', u'pi^9ty', u'piti', u'i', 9, 1, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (
                        6, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u'i', 3, 1, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (
                        7, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u't', 3, 2, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (
                        8, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u'y', 3, 3, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (
                        9, 1111, u'[4, 14]', u'[1, 13]', u'[1, 8]', u'.', u'.^6', u'.', u'.', 6, 0, None, u'symbol', u'["negative", -0.1875]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]', u'#shetlife', u'["hashtag", null, "#shetlif"]', u'#readytogo', u'["hashtag", null, "#readytogo"]', u'http://www.absurd.com', u'["URL", null, "http://www.absurd.com"]'), (
                        10, 1111, u'[4, 14]', u'[1, 14]', u'[1, 9]', u':-(', u':-(^5', u':-(', u'(', 5, 2, None, u'EMOASC', u'["negative", -0.1875]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u'@real_trump', u'["mention", null, "@real_trump"]', u'#shetlife', u'["hashtag", null, "#shetlif"]', u'#readytogo', u'["hashtag", null, "#readytogo"]', u'http://www.absurd.com', u'["URL", null, "http://www.absurd.com"]', None, None), (
                        11, 5555, u'[8, 2, 7]', u'[0, 8]', u'[0, 6]', u'explanation', u'expla^5nation', u'explan', u'a', 5, 4, None, u'NN', u'["neutral", 0.0]', u'model', u'["NN", null, "model"]', u',', u'["symbol", null, ","]', u'but', u'["CC", null, "but"]', u'a', u'["DT", null, "a"]', u'big', u'["JJ", {"big": 3}, "big"]', u'.', u'["symbol", null, "."]', u'right', u'["UH", null, "right"]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]'), (
                        12, 5555, u'[8, 2, 7]', u'[1, 0]', u'[1, 0]', u'right', u'ri^6ght', u'right', u'i', 6, 1, None, u'UH', u'["neutral", 0.0]', u'but', u'["CC", null, "but"]', u'a', u'["DT", null, "a"]', u'big', u'["JJ", {"big": 3}, "big"]', u'explanation', u'["NN", null, "explan"]', u'.', u'["symbol", null, "."]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]', u'you', u'["PRP", null, "you"]', u'think', u'["VB", null, "think"]'), (
                        13, 5555, u'[8, 2, 7]', u'[2, 2]', u'[2, 2]', u'you', u'you^6', u'you', u'u', 6, 2, None, u'PRP', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'right', u'["UH", null, "right"]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]', u'think', u'["VB", null, "think"]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', u'?', u'["symbol", null, "?"]', None, None), (
                        14, 5555, u'[8, 2, 7]', u'[2, 6]', u'[2, 6]', u'?', u'?^4', u'?', u'?', 4, 0, None, u'symbol', u'["neutral", 0.0]', u'do', u'["VBP", null, "do"]', u'you', u'["PRP", null, "you"]', u'think', u'["VB", null, "think"]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', None, None, None, None, None, None, None, None, None, None)]

        stats.statsdb.getall("replications").should.be.equal(right_output)



    @attr(status='stable')
    #@wipd
    def test_extract_redu_lower_case_603(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode, )#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)

        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        #p(stats.statsdb, "stats.statsdb")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()



        ## DE####

        ### ROW 1 ###
        #p(json.loads(self.test_dict_row_de_1["text"]), "text_elem")
        #text_elem = [[ [[t[0].lower(), t[1]] for t in s[0] ], s[1]] for s in json.loads(self.test_dict_row_de_1["text"]) ]
        #p(text_elem, "text_elem")
        repl_free_de_row_lowercased_1 = [[u'klitze', u'klitze', u'kleine', u'kleine', u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]
        rle_for_repl_in_text_container = [['', u'kli^4tze', u'kle^5ine', u'klein^3e', '', ''], ['', '', '', '', '', '', '', u':-)^4', u'-)^3']]
        extracted_redu_in_text_container, redu_free_text_container,mapping_redu = stats.extract_reduplications(repl_free_de_row_lowercased_1,rle_for_repl_in_text_container)

        #p([t[0] for i in json.loads(self.test_dict_row_de_1["text"]) for t in i[0]])
        # p((len(extracted_redu_in_text_container),extracted_redu_in_text_container), "extracted_redu_in_text_container")
        #p((len(redu_free_text_container),redu_free_text_container), "redu_free_text_container")
        #p(mapping_redu, "mapping_redu")

        extracted_redu_in_text_container.should.be.equal([[{'start_index_in_orig': 0, 'length': 2, 'word': u'klitze', 'index_in_redu_free': 0}, {'start_index_in_orig': 2, 'length': 2, 'word': u'kleine', 'index_in_redu_free': 1}], []])
        redu_free_text_container.should.be.equal([[(u'klitze', {u'klitze': 1, u'kli^4tze': 1}), (u'kleine', {u'kle^5ine': 1, u'klein^3e': 1}), u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']])
        mapping_redu.should.be.equal([[0, 2, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]])
        

        # ### ROW 2 ###
        #text_elem = [[ [[t[0].lower(), t[1]] for t in s[0] ], s[1]] for s in json.loads(self.test_dict_row_de_1["text"]) ]
        repl_free_de_row_lowercased_2 = [[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [u'bleibt', u'bleibt', u'hungrig', u'.', u'\U0001f600', u'\U0001f308']]
        rle_for_repl_in_text_container = [['', '', u'ta^6g^6', '', '', '', ''], [u'genie^11s^2t', u'geni^13st', '', '', ''], [u'ble^8ibt', u'ble^4ibt', u'hu^12ngrig', '', u'\U0001f600^5', u'\U0001f308^7']]
        extracted_redu_in_text_container, redu_free_text_container,mapping_redu = stats.extract_reduplications(repl_free_de_row_lowercased_2,rle_for_repl_in_text_container)

        #p([t[0] for i in json.loads(self.test_dict_row_de_2["text"]) for t in i[0]])
        # #p((len(extracted_redu_in_text_container),extracted_redu_in_text_container), "extracted_redu_in_text_container")
        #p((len(redu_free_text_container),redu_free_text_container), "redu_free_text_container")
        #p(mapping_redu,"mapping_redu")

        extracted_redu_in_text_container.should.be.equal([[], [], [{'start_index_in_orig': 0, 'length': 2, 'word': u'bleibt', 'index_in_redu_free': 0}]])
        redu_free_text_container.should.be.equal([[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [(u'bleibt', {u'ble^4ibt': 1, u'ble^8ibt': 1}), u'hungrig', u'.', u'\U0001f600', u'\U0001f308']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [0, 2, 3, 4, 5]])
        
        # # # ########### EN ##############


        # ### ROW 1 ###
        repl_free_en_row_lowercased_1 =    [[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', u'very', u'very', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', u'ver^4y^5', u'v^3er^8y', '', u'pi^9ty', '', '', u'pi^3t^3y^3', '', '', u'.^6', u':-(^5', '', '', '', '']]
        extracted_redu_in_text_container, redu_free_text_container,mapping_redu = stats.extract_reduplications(repl_free_en_row_lowercased_1,rle_for_repl_in_text_container)

        #p([t[0] for i in json.loads(self.test_dict_row_en_1["text"]) for t in i[0]])
        # #p((len(extracted_redu_in_text_container),extracted_redu_in_text_container), "extracted_redu_in_text_container")
        #p((len(redu_free_text_container),redu_free_text_container), "redu_free_text_container")
        #p(mapping_redu,"mapping_redu")

        extracted_redu_in_text_container.should.be.equal([[], [{'start_index_in_orig': 4, 'length': 3, 'word': u'very', 'index_in_redu_free': 4}, {'start_index_in_orig': 7, 'length': 4, 'word': u'pity', 'index_in_redu_free': 5}]])
        redu_free_text_container.should.be.equal([[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', (u'very', {u'very': 1, u'ver^4y^5': 1, u'v^3er^8y': 1}), (u'pity', {u'pity': 2, u'pi^3t^3y^3': 1, u'pi^9ty': 1}), u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']])
        mapping_redu.should.be.equal([[0, 1, 2, 3], [0, 1, 2, 3, 4, 7, 11, 12, 13, 14, 15, 16, 17, 18]])
        
        # ### ROW 2 ###
        repl_free_en_row_lowercased_2 = [[u'tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]
        rle_for_repl_in_text_container =  [['', '', '', '', '', '', '', '', u'expla^5nation', ''], [u'ri^6ght', ''], ['', '', u'you^6', '', '', '', u'?^4']]
        extracted_redu_in_text_container, redu_free_text_container,mapping_redu = stats.extract_reduplications(repl_free_en_row_lowercased_2,rle_for_repl_in_text_container)

        #p([t[0] for i in json.loads(self.test_dict_row_en_2["text"]) for t in i[0]])
        # #p((len(extracted_redu_in_text_container),extracted_redu_in_text_container), "extracted_redu_in_text_container")
        #p((len(redu_free_text_container),redu_free_text_container), "redu_free_text_container")
        #p(mapping_redu,"mapping_redu")

        extracted_redu_in_text_container.should.be.equal([[{'start_index_in_orig': 5, 'length': 3, 'word': u'big', 'index_in_redu_free': 5}], [], []])
        redu_free_text_container.should.be.equal([[u'tiny', u'model', u',', u'but', u'a', (u'big', {u'big': 3}), u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]])






    @attr(status='stable')
    #@wipd
    def test_extract_redu_case_sensitive_604(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)

        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, case_sensitiv=True, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        #p(stats.statsdb, "stats.statsdb")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()

        ### DE####

        ### ROW 1 ###
        repl_free_de_row_case_sensitive_1 = [[u'Klitze', u'klitze', u'kleEine', u'kleine', u'\xdcberaschung', u'.'], [u'Trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]
        rle_for_repl_in_text_container = [['', u'kli^4tze', u'kleE^4ine', u'klein^3e', '', ''], ['', '', '', '', '', '', '', u':-)^4', u'-)^3']]
        extracted_redu_in_text_container, redu_free_text_container,mapping_redu = stats.extract_reduplications( repl_free_de_row_case_sensitive_1,rle_for_repl_in_text_container)

        #p([t[0] for i in json.loads(self.test_dict_row_de_1["text"]) for t in i[0]])
        #p((len(extracted_redu_in_text_container),extracted_redu_in_text_container), "extracted_redu_in_text_container")
        #p((len(redu_free_text_container),redu_free_text_container), "redu_free_text_container")
        #p(mapping_redu, "mapping_redu")

        extracted_redu_in_text_container.should.be.equal([[], []])
        redu_free_text_container.should.be.equal([[u'Klitze', u'klitze', u'kleEine', u'kleine', u'\xdcberaschung', u'.'], [u'Trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]])
        

        ### ROW 2 ###
        repl_free_de_row_case_sensitive_2 = [[u'einen', u'wundersch\xf6nen', u'Tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'Geniest', u'genist', u'das', u'Leben', u'.'], [u'Bleibt', u'bleibt', u'Hungrig', u'.', u'\U0001f600', u'\U0001f308']]
        rle_for_repl_in_text_container = [['', '', u'Ta^6g^6', '', '', '', ''], [u'Genie^11s^2t', u'geni^13st', '', '', ''], [u'Ble^8ibt', u'ble^4ibt', u'Hu^12ngrig', '', u'\U0001f600^5', u'\U0001f308^7']]
        extracted_redu_in_text_container, redu_free_text_container,mapping_redu = stats.extract_reduplications( repl_free_de_row_case_sensitive_2,rle_for_repl_in_text_container)

        #p([t[0] for i in json.loads(self.test_dict_row_de_2["text"]) for t in i[0]])
        #p((len(extracted_redu_in_text_container),extracted_redu_in_text_container), "extracted_redu_in_text_container")
        #p((len(redu_free_text_container),redu_free_text_container), "redu_free_text_container")
        #p(mapping_redu, "mapping_redu")

        extracted_redu_in_text_container.should.be.equal([[], [], []])
        redu_free_text_container.should.be.equal([[u'einen', u'wundersch\xf6nen', u'Tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'Geniest', u'genist', u'das', u'Leben', u'.'], [u'Bleibt', u'bleibt', u'Hungrig', u'.', u'\U0001f600', u'\U0001f308']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5]])
        
        # # # ########### EN ##############


        ### ROW 1 ###
        repl_free_en_row_case_sensitive_1 = [[u'I', u'loved', u'it', u'.'], [u'But', u'it', u'was', u'also', u'very', u'veRry', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', u'ver^4y^5', u'v^3eR^6r^2y', '', u'pi^9ty', '', '', u'pi^3t^3y^3', '', '', u'.^6', u':-(^5', '', '', '', '']]
        extracted_redu_in_text_container, redu_free_text_container,mapping_redu = stats.extract_reduplications( repl_free_en_row_case_sensitive_1,rle_for_repl_in_text_container)


        #p([t[0] for i in json.loads(self.test_dict_row_en_1["text"]) for t in i[0]])
        # p((len(extracted_redu_in_text_container),extracted_redu_in_text_container), "extracted_redu_in_text_container")
        #p((len(redu_free_text_container),redu_free_text_container), "redu_free_text_container")
        #p(mapping_redu, "mapping_redu")

        extracted_redu_in_text_container.should.be.equal([[], [{'start_index_in_orig': 7, 'length': 4, 'word': u'pity', 'index_in_redu_free': 7}]])
        redu_free_text_container.should.be.equal([[u'I', u'loved', u'it', u'.'], [u'But', u'it', u'was', u'also', u'very', u'veRry', u'very', (u'pity', {u'pity': 2, u'pi^3t^3y^3': 1, u'pi^9ty': 1}), u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']])
        mapping_redu.should.be.equal([[0, 1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18]])
        
        ### ROW 2 ###
        repl_free_en_row_case_sensitive_2 = [[u'Tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'Right', u'?'], [u'What', u'do', u'you', u'think', u'about', u'it', u'?']]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', u'expla^5nation', ''], [u'Ri^6ght', ''], ['', '', u'you^6', '', '', '', u'?^4']]
        extracted_redu_in_text_container, redu_free_text_container,mapping_redu = stats.extract_reduplications( repl_free_en_row_case_sensitive_2,rle_for_repl_in_text_container)

        #p([t[0] for i in json.loads(self.test_dict_row_en_2["text"]) for t in i[0]])
        # p((len(extracted_redu_in_text_container),extracted_redu_in_text_container), "extracted_redu_in_text_container")
        #p((len(redu_free_text_container),redu_free_text_container), "redu_free_text_container")
        #p(mapping_redu, "mapping_redu")

        extracted_redu_in_text_container.should.be.equal([[{'start_index_in_orig': 5, 'length': 3, 'word': u'big', 'index_in_redu_free': 5}], [], []])
        redu_free_text_container.should.be.equal([[u'Tiny', u'model', u',', u'but', u'a', (u'big', {u'big': 3}), u'explanation', u'.'], [u'Right', u'?'], [u'What', u'do', u'you', u'think', u'about', u'it', u'?']])
        mapping_redu.should.be.equal([[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]])

        
    # def compute_baseline_1(self, redu_free_text_container, context_right=5, context_left=5):
    #     inp_token_list = [token for sent in redu_free_text_container for token in sent]
    #     computed_baseline  = []
    #     ngramm_lenght = context_right+1+context_left
    #     for n in xrange(1,ngramm_lenght+1):
    #         computed_baseline += [tuple(inp_token_list[i:i+n]) for i in xrange(len(inp_token_list)-n+1)]
    #     return computed_baseline







    @attr(status='stable')
    #@wipd
    def test_insert_redu_into_db_lower_case_605(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode, )#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"



        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))






        ### DE####
        import Stemmer
        stemmer = Stemmer.Stemmer("de")
        ### ROW 1 ###
        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()


        repl_free_de_row_lowercased_1 = [[u'klitze', u'klitze', u'kleine', u'kleine', u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]
        
        #p([t[0] for i in json.loads(self.test_dict_row_de_1["text"]) for t in i[0]])
        #p(self.test_dict_row_de_1["text"])
        text_list = [self.test_dict_row_de_1["id"],self.test_dict_row_de_1["text"]]
        extracted_redu_in_text_container = [[{'start_index_in_orig': 0, 'length': 2, 'word': u'klitze', 'index_in_redu_free': 0}, {'start_index_in_orig': 2, 'length': 2, 'word': u'kleine', 'index_in_redu_free': 1}], []]
        redu_free_text_container = [[(u'klitze', {u'klitze': 1, u'kli^4tze': 1}), (u'kleine', {u'kle^5ine': 1, u'klein^3e': 1}), u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]
        rle_for_repl_in_text_container = [['', u'kli^4tze', u'kle^5ine', u'klein^3e', '', ''], ['', '', '', '', '', '', '', u':-)^4', u'-)^3']]
        repl_free_text_container = [[u'klitze', u'klitze', u'kleine', u'kleine', u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]
        mapping_redu = [[0, 2, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_redu_into_db(text_list,json.loads(self.test_dict_row_de_1["text"]),extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container,mapping_redu, stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")
        #p(list(stats.statsdb.getall("reduplications")))
        inserted_columns =list(stats.statsdb.getall("reduplications"))
        right_output = [(1, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'), (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]')]
        
        inserted_columns.should.be.equal(right_output)


        # ### ROW 2 ###

        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()

        repl_free_de_row_lowercased_2 = [[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [u'bleibt', u'bleibt', u'hungrig', u'.', u'\U0001f600', u'\U0001f308']]
    
        #p([t[0] for i in json.loads(self.test_dict_row_de_2["text"]) for t in i[0]], c="r")
        #p(json.loads(self.test_dict_row_de_2["text"]))
        text_list = [self.test_dict_row_de_1["id"],self.test_dict_row_de_1["text"]]
        extracted_redu_in_text_container = [[], [], [{'start_index_in_orig': 0, 'length': 2, 'word': u'bleibt', 'index_in_redu_free': 0}]]
        redu_free_text_container = [[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [(u'bleibt', {u'ble^4ibt': 1, u'ble^8ibt': 1}), u'hungrig', u'.', u'\U0001f600', u'\U0001f308']]
        rle_for_repl_in_text_container = [['', '', u'ta^6g^6', '', '', '', ''], [u'genie^11s^2t', u'geni^13st', '', '', ''], [u'ble^8ibt', u'ble^4ibt', u'hu^12ngrig', '', u'\U0001f600^5', u'\U0001f308^7']]
        repl_free_text_container = [[u'einen', u'wundersch\xf6nen', u'tag', u'w\xfcnsche', u'ich', u'euch', u'.'], [u'geniest', u'genist', u'das', u'leben', u'.'], [u'bleibt', u'bleibt', u'hungrig', u'.', u'\U0001f600', u'\U0001f308']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [0, 2, 3, 4, 5]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_redu_into_db(text_list,json.loads(self.test_dict_row_de_2["text"]),extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")

        #p(list(stats.statsdb.getall("reduplications")))
        inserted_columns =list(stats.statsdb.getall("reduplications"))
        right_output = [(1, 8888, u'[7, 5, 5]', u'[2, 0]', u'[2, 0]', u'bleibt', u'bleibt', u'{"ble^4ibt": 1, "ble^8ibt": 1}', 2, u'NN', u'["neutral", 0.0]', u'geniest', u'["NN", null, "geni"]', u'genist', u'["VVFIN", null, "genist"]', u'das', u'["ART", null, "das"]', u'leben', u'["NN", null, "leb"]', u'.', u'["symbol", null, "."]', u'hungrig', u'["NN", null, "hungrig"]', u'.', u'["symbol", null, "."]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', None, None)]
        inserted_columns.should.be.equal(right_output)





        
        # ########### EN ##############
        stemmer = Stemmer.Stemmer("en")
        # ### ROW 1 ###
        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()

        repl_free_en_row_lowercased_1 =    [[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', u'very', u'very', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]

        #p([t[0] for i in json.loads(self.test_dict_row_en_1["text"]) for t in i[0]])
        #p(json.loads(self.test_dict_row_en_1["text"]))
        text_list = [self.test_dict_row_en_1["id"],self.test_dict_row_en_1["text"]]
        extracted_redu_in_text_container = [[], [{'start_index_in_orig': 4, 'length': 3, 'word': u'very', 'index_in_redu_free': 4}, {'start_index_in_orig': 7, 'length': 4, 'word': u'pity', 'index_in_redu_free': 5}]]
        redu_free_text_container = [[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', (u'very', {u'very': 1, u'ver^4y^5': 1, u'v^3er^8y': 1}), (u'pity', {u'pity': 2, u'pi^3t^3y^3': 1, u'pi^9ty': 1}), u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]
        rle_for_repl_in_text_container = [['', '', '', ''], ['', '', '', '', u'ver^4y^5', u'v^3er^8y', '', u'pi^9ty', '', '', u'pi^3t^3y^3', '', '', u'.^6', u':-(^5', '', '', '', '']]
        repl_free_text_container =[[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', u'very', u'very', u'very', u'pity', u'pity', u'pity', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com']]
        mapping_redu = [[0, 1, 2, 3], [0, 1, 2, 3, 4, 7, 11, 12, 13, 14, 15, 16, 17, 18]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_redu_into_db(text_list,json.loads(self.test_dict_row_en_1["text"]),extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container,repl_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")

        #p(list(stats.statsdb.getall("reduplications")))
        inserted_columns =list(stats.statsdb.getall("reduplications"))
        right_output = [(1, 1111, u'[4, 14]', u'[1, 4]', u'[1, 4]', u'very', u'veri', u'{"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}', 3, u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (2, 1111, u'[4, 14]', u'[1, 7]', u'[1, 5]', u'pity', u'piti', u'{"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}', 4, u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]')]
        inserted_columns.should.be.equal(right_output)




        # ### ROW 2 ###
        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()


        repl_free_en_row_lowercased_2 = [[u'tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]
        

        #p([t[0] for i in json.loads(self.test_dict_row_en_2["text"]) for t in i[0]])
        #p(json.loads(self.test_dict_row_en_2["text"]))
        text_list = [self.test_dict_row_en_2["id"],self.test_dict_row_en_2["text"]]
        extracted_redu_in_text_container = [[{'start_index_in_orig': 5, 'length': 3, 'word': u'big', 'index_in_redu_free': 5}], [], []]
        redu_free_text_container = [[u'tiny', u'model', u',', u'but', u'a', (u'big', {u'big': 3}), u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]
        rle_for_repl_in_text_container = [['', '', '', '', '', '', '', '', u'expla^5nation', ''], [u'ri^6ght', ''], ['', '', u'you^6', '', '', '', u'?^4']]
        repl_free_text_container = [[u'tiny', u'model', u',', u'but', u'a', u'big', u'big', u'big', u'explanation', u'.'], [u'right', u'?'], [u'what', u'do', u'you', u'think', u'about', u'it', u'?']]
        mapping_redu = [[0, 1, 2, 3, 4, 5, 8, 9], [0, 1], [0, 1, 2, 3, 4, 5, 6]]
        stemmed_text_container = [ [stemmer.stemWord(token) if isinstance(token, (str, unicode) ) else stemmer.stemWord(token[0])  for token in sent] for sent in redu_free_text_container ]
        stats.insert_redu_into_db(text_list,json.loads(self.test_dict_row_en_2["text"]),extracted_redu_in_text_container, redu_free_text_container, rle_for_repl_in_text_container, repl_free_text_container,mapping_redu,stemmed_text_container)
        stats._write_repl_into_db(thread_name="Thread0")
        stats._write_redu_into_db(thread_name="Thread0")

        #p(list(stats.statsdb.getall("reduplications")))
        inserted_columns =list(stats.statsdb.getall("reduplications"))
        right_output = [(1, 5555, u'[8, 2, 7]', u'[0, 5]', u'[0, 5]', u'big', u'big', u'{"big": 3}', 3, u'JJ', u'["neutral", 0.0]', u'tiny', u'["JJ", null, "tini"]', u'model', u'["NN", null, "model"]', u',', u'["symbol", null, ","]', u'but', u'["CC", null, "but"]', u'a', u'["DT", null, "a"]', u'explanation', u'["NN", null, "explan"]', u'.', u'["symbol", null, "."]', u'right', u'["UH", null, "right"]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]')]

        inserted_columns.should.be.equal(right_output)








    @attr(status='stable')
    #@wipd
    def test_compute_baseline_lowercased_606(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode, )#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)

        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        #p(stats.statsdb, "stats.statsdb")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()



        # ##### FAKE SENT 1 #######
        inp = [[u'klitze', u'kleine', u'\xfcberaschung', u'.']]
        extracted_redu_in_text_container = [[{}]]
        #assert set(stats.compute_baseline(inp)) == set(self.compute_baseline_1(inp))
        #p( stats.compute_baseline(inp,extracted_redu_in_text_container))
        stats.compute_baseline(inp,extracted_redu_in_text_container).should.be.equal([(u'klitze',), (u'kleine',), (u'\xfcberaschung',), (u'.',), (u'klitze', u'kleine'), (u'kleine', u'\xfcberaschung'), (u'\xfcberaschung', u'.'), (u'klitze', u'kleine', u'\xfcberaschung'), (u'kleine', u'\xfcberaschung', u'.'), (u'klitze', u'kleine', u'\xfcberaschung', u'.')])


        # # ##### FAKE SENT 2#######
        inp = [[u'1', u'2', u'3', u'4', u'5', u'😂', u'🧑🏻']]
        extracted_redu_in_text_container = [[{}]]
        #assert set(stats.compute_baseline(inp)) == set(self.compute_baseline_1(inp))
        #p( stats.compute_baseline(inp))
        stats.compute_baseline(inp,extracted_redu_in_text_container).should.be.equal([(u'1',), (u'2',), (u'3',), (u'4',), (u'5',), (u'\U0001f602',), (u'\U0001f9d1\U0001f3fb',), (u'1', u'2'), (u'2', u'3'), (u'3', u'4'), (u'4', u'5'), (u'5', u'\U0001f602'), (u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3'), (u'2', u'3', u'4'), (u'3', u'4', u'5'), (u'4', u'5', u'\U0001f602'), (u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3', u'4'), (u'2', u'3', u'4', u'5'), (u'3', u'4', u'5', u'\U0001f602'), (u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3', u'4', u'5'), (u'2', u'3', u'4', u'5', u'\U0001f602'), (u'3', u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3', u'4', u'5', u'\U0001f602'), (u'2', u'3', u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb')])



        # ### DE####

        ## ROW 1 ###
        inp = [[(u'klitze', {u'klitze': 1, u'kli^4tze': 1}), (u'kleine', {u'kle^5ine': 1, u'klein^3e': 1}), u'\xfcberaschung', u'.'], [u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)']]
        extracted_redu_in_text_container = [[{'start_index_in_orig': 0, 'length': 2, 'word': u'klitze', 'index_in_redu_free': 0}, {'start_index_in_orig': 2, 'length': 2, 'word': u'kleine', 'index_in_redu_free': 1}], []]
        #p( stats.compute_baseline(inp,extracted_redu_in_text_container))
        set(stats.compute_baseline(inp,extracted_redu_in_text_container)).should.be.equal(set([(u'klitze',), (u'kleine',), (u'\xfcberaschung',), (u'.',), (u'trotzdem',), (u'hat',), (u'sie',), (u'mich',), (u'gl\xfccklich',), (u'gemacht',), (u'!',), (u':-)',), (u'-)',), (u'klitze', u'kleine'), (u'kleine', u'\xfcberaschung'), (u'\xfcberaschung', u'.'), (u'.', u'trotzdem'), (u'trotzdem', u'hat'), (u'hat', u'sie'), (u'sie', u'mich'), (u'mich', u'gl\xfccklich'), (u'gl\xfccklich', u'gemacht'), (u'gemacht', u'!'), (u'!', u':-)'), (u':-)', u'-)'), (u'klitze', u'kleine', u'\xfcberaschung'), (u'kleine', u'\xfcberaschung', u'.'), (u'\xfcberaschung', u'.', u'trotzdem'), (u'.', u'trotzdem', u'hat'), (u'trotzdem', u'hat', u'sie'), (u'hat', u'sie', u'mich'), (u'sie', u'mich', u'gl\xfccklich'), (u'mich', u'gl\xfccklich', u'gemacht'), (u'gl\xfccklich', u'gemacht', u'!'), (u'gemacht', u'!', u':-)'), (u'!', u':-)', u'-)'), (u'klitze', u'kleine', u'\xfcberaschung', u'.'), (u'kleine', u'\xfcberaschung', u'.', u'trotzdem'), (u'\xfcberaschung', u'.', u'trotzdem', u'hat'), (u'.', u'trotzdem', u'hat', u'sie'), (u'trotzdem', u'hat', u'sie', u'mich'), (u'hat', u'sie', u'mich', u'gl\xfccklich'), (u'sie', u'mich', u'gl\xfccklich', u'gemacht'), (u'mich', u'gl\xfccklich', u'gemacht', u'!'), (u'gl\xfccklich', u'gemacht', u'!', u':-)'), (u'gemacht', u'!', u':-)', u'-)'), (u'klitze', u'kleine', u'\xfcberaschung', u'.', u'trotzdem'), (u'kleine', u'\xfcberaschung', u'.', u'trotzdem', u'hat'), (u'\xfcberaschung', u'.', u'trotzdem', u'hat', u'sie'), (u'.', u'trotzdem', u'hat', u'sie', u'mich'), (u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich'), (u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht'), (u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!'), (u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)'), (u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)'), (u'klitze', u'kleine', u'\xfcberaschung', u'.', u'trotzdem', u'hat'), (u'kleine', u'\xfcberaschung', u'.', u'trotzdem', u'hat', u'sie'), (u'\xfcberaschung', u'.', u'trotzdem', u'hat', u'sie', u'mich'), (u'.', u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich'), (u'trotzdem', u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht'), (u'hat', u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!'), (u'sie', u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)'), (u'mich', u'gl\xfccklich', u'gemacht', u'!', u':-)', u'-)')]))


        # # # ########### EN ##############


        # ### ROW 1 ###
        inp = [[u'i', u'loved', u'it', u'.'], [u'but', u'it', u'was', u'also', u'very', u'pity', u'for', u'me', u'.', u':-(', u'@real_trump', u'#sheetlife', u'#readytogo', u'http://www.absurd.com']]
        extracted_redu_in_text_container = [[], [{'start_index_in_orig': 4, 'length': 3, 'word': u'very', 'index_in_redu_free': 4}, {'start_index_in_orig': 7, 'length': 4, 'word': u'pity', 'index_in_redu_free': 5}]]
        #p(stats.compute_baseline(inp,extracted_redu_in_text_container))
        set(stats.compute_baseline(inp,extracted_redu_in_text_container)).should.be.equal(set([(u'i',), (u'loved',), (u'it',), (u'.',), (u'but',), (u'it',), (u'was',), (u'also',), (u'very',), (u'pity',), (u'for',), (u'me',), (u'.',), (u':-(',), (u'@real_trump',), (u'#sheetlife',), (u'#readytogo',), (u'http://www.absurd.com',), (u'i', u'loved'), (u'loved', u'it'), (u'it', u'.'), (u'.', u'but'), (u'but', u'it'), (u'it', u'was'), (u'was', u'also'), (u'also', u'very'), (u'very', u'pity'), (u'pity', u'for'), (u'for', u'me'), (u'me', u'.'), (u'.', u':-('), (u':-(', u'@real_trump'), (u'@real_trump', u'#sheetlife'), (u'#sheetlife', u'#readytogo'), (u'#readytogo', u'http://www.absurd.com'), (u'i', u'loved', u'it'), (u'loved', u'it', u'.'), (u'it', u'.', u'but'), (u'.', u'but', u'it'), (u'but', u'it', u'was'), (u'it', u'was', u'also'), (u'was', u'also', u'very'), (u'also', u'very', u'pity'), (u'very', u'pity', u'for'), (u'pity', u'for', u'me'), (u'for', u'me', u'.'), (u'me', u'.', u':-('), (u'.', u':-(', u'@real_trump'), (u':-(', u'@real_trump', u'#sheetlife'), (u'@real_trump', u'#sheetlife', u'#readytogo'), (u'#sheetlife', u'#readytogo', u'http://www.absurd.com'), (u'i', u'loved', u'it', u'.'), (u'loved', u'it', u'.', u'but'), (u'it', u'.', u'but', u'it'), (u'.', u'but', u'it', u'was'), (u'but', u'it', u'was', u'also'), (u'it', u'was', u'also', u'very'), (u'was', u'also', u'very', u'pity'), (u'also', u'very', u'pity', u'for'), (u'very', u'pity', u'for', u'me'), (u'pity', u'for', u'me', u'.'), (u'for', u'me', u'.', u':-('), (u'me', u'.', u':-(', u'@real_trump'), (u'.', u':-(', u'@real_trump', u'#sheetlife'), (u':-(', u'@real_trump', u'#sheetlife', u'#readytogo'), (u'@real_trump', u'#sheetlife', u'#readytogo', u'http://www.absurd.com'), (u'i', u'loved', u'it', u'.', u'but'), (u'loved', u'it', u'.', u'but', u'it'), (u'it', u'.', u'but', u'it', u'was'), (u'.', u'but', u'it', u'was', u'also'), (u'but', u'it', u'was', u'also', u'very'), (u'it', u'was', u'also', u'very', u'pity'), (u'was', u'also', u'very', u'pity', u'for'), (u'also', u'very', u'pity', u'for', u'me'), (u'very', u'pity', u'for', u'me', u'.'), (u'pity', u'for', u'me', u'.', u':-('), (u'for', u'me', u'.', u':-(', u'@real_trump'), (u'me', u'.', u':-(', u'@real_trump', u'#sheetlife'), (u'.', u':-(', u'@real_trump', u'#sheetlife', u'#readytogo'), (u':-(', u'@real_trump', u'#sheetlife', u'#readytogo', u'http://www.absurd.com'), (u'i', u'loved', u'it', u'.', u'but', u'it'), (u'loved', u'it', u'.', u'but', u'it', u'was'), (u'it', u'.', u'but', u'it', u'was', u'also'), (u'.', u'but', u'it', u'was', u'also', u'very'), (u'but', u'it', u'was', u'also', u'very', u'pity'), (u'it', u'was', u'also', u'very', u'pity', u'for'), (u'was', u'also', u'very', u'pity', u'for', u'me'), (u'also', u'very', u'pity', u'for', u'me', u'.'), (u'very', u'pity', u'for', u'me', u'.', u':-('), (u'pity', u'for', u'me', u'.', u':-(', u'@real_trump'), (u'for', u'me', u'.', u':-(', u'@real_trump', u'#sheetlife'), (u'me', u'.', u':-(', u'@real_trump', u'#sheetlife', u'#readytogo'), (u'.', u':-(', u'@real_trump', u'#sheetlife', u'#readytogo', u'http://www.absurd.com'), (u'very',), (u'very',), (u'pity',), (u'pity',), (u'pity',)]))

        







    @attr(status='stable')
    #@wipd
    def test_temporize_baseline_lowercased_607_1(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode, )#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)



        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))


        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()



        # ##### FAKE SENT 1 #######

        stats._init_compution_variables()

        #inp = [[u'klitze', u'kleine', u'\xfcberaschung', u'.']]
        computed_baseline = [(u'klitze',), (u'kleine',), (u'\xfcberaschung',), (u'.',), (u'klitze', u'kleine'), (u'kleine', u'\xfcberaschung'), (u'\xfcberaschung', u'.'), (u'klitze', u'kleine', u'\xfcberaschung'), (u'kleine', u'\xfcberaschung', u'.'), (u'klitze', u'kleine', u'\xfcberaschung', u'.')]
        #assert set(stats.compute_baseline(inp)) == set(self.compute_baseline_1(inp))
        #p( stats.compute_baseline(inp))
        extracted_redu_in_text_container = ((),())
        stats.temporize_baseline(computed_baseline,extracted_redu_in_text_container)
        #p(dict(stats.temporized_baseline), "temporized_list ")
        stats.temporized_baseline.should.be.equal( {(u'.',): 1,
                                                 (u'kleine',): 1,
                                                 (u'kleine', u'\xfcberaschung'): 1,
                                                 (u'kleine', u'\xfcberaschung', u'.'): 1,
                                                 (u'klitze',): 1,
                                                 (u'klitze', u'kleine'): 1,
                                                 (u'klitze', u'kleine', u'\xfcberaschung'): 1,
                                                 (u'klitze', u'kleine', u'\xfcberaschung', u'.'): 1,
                                                 (u'\xfcberaschung',): 1,
                                                 (u'\xfcberaschung', u'.'): 1}
                                                )     


        stats.temporize_baseline(computed_baseline,extracted_redu_in_text_container)
        #p(dict(stats.temporized_baseline), "temporized_list ")
        stats.temporized_baseline.should.be.equal( {(u'.',): 2,
                                                 (u'kleine',): 2,
                                                 (u'kleine', u'\xfcberaschung'): 2,
                                                 (u'kleine', u'\xfcberaschung', u'.'): 2,
                                                 (u'klitze',): 2,
                                                 (u'klitze', u'kleine'): 2,
                                                 (u'klitze', u'kleine', u'\xfcberaschung'): 2,
                                                 (u'klitze', u'kleine', u'\xfcberaschung', u'.'): 2,
                                                 (u'\xfcberaschung',): 2,
                                                 (u'\xfcberaschung', u'.'): 2}
                                                 )





        # # ##### FAKE SENT 2#######
        stats._init_compution_variables()
        computed_baseline = [(u'1',), (u'2',), (u'3',), (u'4',), (u'5',), (u'\U0001f602',), (u'\U0001f9d1\U0001f3fb',), (u'1', u'2'), (u'2', u'3'), (u'3', u'4'), (u'4', u'5'), (u'5', u'\U0001f602'), (u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3'), (u'2', u'3', u'4'), (u'3', u'4', u'5'), (u'4', u'5', u'\U0001f602'), (u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3', u'4'), (u'2', u'3', u'4', u'5'), (u'3', u'4', u'5', u'\U0001f602'), (u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3', u'4', u'5'), (u'2', u'3', u'4', u'5', u'\U0001f602'), (u'3', u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3', u'4', u'5', u'\U0001f602'), (u'2', u'3', u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'), (u'1', u'2', u'3', u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb')]
        stats.temporize_baseline(computed_baseline,extracted_redu_in_text_container)
        #p(dict(stats.temporized_baseline), "temporized_list ")
        stats.temporized_baseline.should.be.equal( {(u'1',): 1,
                                                     (u'1', u'2'): 1,
                                                     (u'1', u'2', u'3'): 1,
                                                     (u'1', u'2', u'3', u'4'): 1,
                                                     (u'1', u'2', u'3', u'4', u'5'): 1,
                                                     (u'1', u'2', u'3', u'4', u'5', u'\U0001f602'): 1,
                                                     (u'1', u'2', u'3', u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'): 1,
                                                     (u'2',): 1,
                                                     (u'2', u'3'): 1,
                                                     (u'2', u'3', u'4'): 1,
                                                     (u'2', u'3', u'4', u'5'): 1,
                                                     (u'2', u'3', u'4', u'5', u'\U0001f602'): 1,
                                                     (u'2', u'3', u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'): 1,
                                                     (u'3',): 1,
                                                     (u'3', u'4'): 1,
                                                     (u'3', u'4', u'5'): 1,
                                                     (u'3', u'4', u'5', u'\U0001f602'): 1,
                                                     (u'3', u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'): 1,
                                                     (u'4',): 1,
                                                     (u'4', u'5'): 1,
                                                     (u'4', u'5', u'\U0001f602'): 1,
                                                     (u'4', u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'): 1,
                                                     (u'5',): 1,
                                                     (u'5', u'\U0001f602'): 1,
                                                     (u'5', u'\U0001f602', u'\U0001f9d1\U0001f3fb'): 1,
                                                     (u'\U0001f602',): 1,
                                                     (u'\U0001f602', u'\U0001f9d1\U0001f3fb'): 1,
                                                     (u'\U0001f9d1\U0001f3fb',): 1}
                                                     )  








    @attr(status='stable')
    #@wipd
    def test_baseline_lazyinsertion_into_db_lowercased_607_2(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode, )#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)



        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))


        stats = Stats(mode=self.mode, )#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        stats.corp = corp
        stats._corp_info = corp.info()



        # ##### FAKE SENT 1 #######
        stats._init_stemmer(stats._corp_info["language"])
        stats._init_compution_variables()

        #inp = [[u'klitze', u'kleine', u'\xfcberaschung', u'.']]
        computed_baseline = [(u'klitze',), (u'kleine',), (u'\xfcberaschung',), (u'.',), (u'klitze', u'kleine'), (u'kleine', u'\xfcberaschung'), (u'\xfcberaschung', u'.'), (u'klitze', u'kleine', u'\xfcberaschung'), (u'kleine', u'\xfcberaschung', u'.'), (u'klitze', u'kleine', u'\xfcberaschung', u'.')]
        extracted_redu_in_text_container = [[
                                                {"word":u'klitze',
                                                "length":2},
                                            ],]
        stats.baseline_lazyinsertion_into_db(computed_baseline,extracted_redu_in_text_container)
       
        ## 
        stats.statsdb.getall("baseline").should.be.equal([])

        ##
        stats.baseline_insert_left_over_data()
        inserted_baseline = stats.statsdb.getall("baseline")
        #p(inserted_baseline, "inserted_baseline1")
        
        baseline_should_be_in_the_db = [(u'\xfcberaschung', u'\xfcberaschung', 1, 1, None, None, None, None, None, None), 
                            (u'klitze++kleine++\xfcberaschung++.', u'klitz++klein++\xfcberaschung++.', 4, 1, None, None, None, None, None, None), 
                            (u'kleine++\xfcberaschung++.', u'klein++\xfcberaschung++.', 3, 1, None, None, None, None, None, None), 
                            (u'kleine++\xfcberaschung', u'klein++\xfcberaschung', 2, 1, None, None, None, None, None, None), 
                            (u'\xfcberaschung++.', u'\xfcberaschung++.', 2, 1, None, None, None, None, None, None), 
                            (u'klitze++kleine++\xfcberaschung', u'klitz++klein++\xfcberaschung', 3, 1, None, None, None, None, None, None), 
                            (u'klitze++kleine', u'klitz++klein', 2, 1, None, None, None, None, None, None), 
                            (u'.', u'.', 1, 1, None, None, None, None, None, None), 
                            (u'klitze', u'klitz', 1, 2, None, None, None, None, None, None), 
                            (u'kleine', u'klein', 1, 1, None, None, None, None, None, None)]


        set(inserted_baseline).should.be.equal(set(baseline_should_be_in_the_db))
        


        ### One More Time
        #stats.temporized_baseline = temporized_baseline
        stats.baseline_lazyinsertion_into_db(computed_baseline,extracted_redu_in_text_container,baseline_insertion_border=1)
        stats.baseline_lazyinsertion_into_db(computed_baseline, extracted_redu_in_text_container,baseline_insertion_border=1)
        
        stats.baseline_insert_left_over_data()
        
        inserted_baseline = stats.statsdb.getall("baseline")
        #p(inserted_baseline, "inserted_baseline2")

        baseline_should_be_in_the_db = [(u'kleine++\xfcberaschung', u'klein++\xfcberaschung', 2, 3, None, None, None, None, None, None), 
                            (u'\xfcberaschung', u'\xfcberaschung', 1, 3, None, None, None, None, None, None), 
                            (u'klitze++kleine++\xfcberaschung++.', u'klitz++klein++\xfcberaschung++.', 4, 3, None, None, None, None, None, None), 
                            (u'klitze++kleine', u'klitz++klein', 2, 3, None, None, None, None, None, None), 
                            (u'kleine++\xfcberaschung++.', u'klein++\xfcberaschung++.', 3, 3, None, None, None, None, None, None), 
                            (u'klitze', u'klitz', 1, 6, None, None, None, None, None, None), 
                            (u'\xfcberaschung++.', u'\xfcberaschung++.', 2, 3, None, None, None, None, None, None), 
                            (u'klitze++kleine++\xfcberaschung', u'klitz++klein++\xfcberaschung', 3, 3, None, None, None, None, None, None), 
                            (u'.', u'.', 1, 3, None, None, None, None, None, None), 
                            (u'kleine', u'klein', 1, 3, None, None, None, None, None, None)]
        
        set(inserted_baseline).should.be.equal(set(baseline_should_be_in_the_db))
        



    @attr(status='stable')
    #@wipd
    def test_intern_compute_function_lower_case_608(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,status_bar=False)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)
        
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")
        stats._init_compution_variables()
        stats._init_preprocessors()
        #p(stats.statsdb, "stats.statsdb")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        stats.corp = corp
        stats._corp_info = corp.info()

        stats._init_stemmer(stats._corp_info["language"])
        ## DE####
        import time
        ### ROW 1 ###
        ##### FIRST INSETION
        #stats._compute([copy.deepcopy(self.test_dict_row_de_1)])
        text_list = [self.test_dict_row_de_1["id"], self.test_dict_row_de_1["text"] ]
        stats._compute([copy.deepcopy(text_list)])
        #stats._compute([copy.deepcopy([self.test_dict_row_de_1[0], self.test_dict_row_de_1])])
        redu = stats.statsdb.getall("reduplications")
        repl = stats.statsdb.getall("replications")
        baseline = stats.statsdb.getall("baseline")


        #p(redu,"redu")
        #p(repl,"repl")
        #p(baseline,"baseline")
        #time.sleep(7)

        redu.should.be.equal(
                                [(1, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]'), (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]')]
                            )
        
        repl.should.be.equal(
                                [(1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]'), (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), (4, 8888, u'[4, 9]', u'[1, 7]', u'[1, 7]', u':-)', u':-)^4', u':-)', u')', 4, 2, None, u'EMOASC', u'["positive", 0.5]', u'sie', u'["PPER", null, "sie"]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "gl\\u00fccklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u'-)', u'["EMOASC", null, "-)"]', None, None, None, None, None, None, None, None), (5, 8888, u'[4, 9]', u'[1, 8]', u'[1, 8]', u'-)', u'-)^3', u'-)', u')', 3, 1, None, u'EMOASC', u'["positive", 0.5]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "gl\\u00fccklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', None, None, None, None, None, None, None, None, None, None)]
                            )
        
        baseline.should.be.equal([(u'.++trotzdem', u'.++trotzdem', 2, 1, None, None, None, None, None, None), (u'!', u'!', 1, 1, None, None, None, None, None, None), (u'hat++sie++mich', u'hat++sie++mich', 3, 1, None, None, None, None, None, None), (u'sie++mich++gl\xfccklich++gemacht++!', u'sie++mich++gl\xfccklich++gemacht++!', 5, 1, None, None, None, None, None, None), (u'gemacht++!', u'gemacht++!', 2, 1, None, None, None, None, None, None), (u'gl\xfccklich++gemacht', u'gl\xfccklich++gemacht', 2, 1, None, None, None, None, None, None), (u'sie++mich++gl\xfccklich', u'sie++mich++gl\xfccklich', 3, 1, None, None, None, None, None, None), (u':-)', u':-)', 1, 1, None, None, None, None, None, None), (u'mich++gl\xfccklich++gemacht++!++:-)++-)', u'mich++gl\xfccklich++gemacht++!++:-)++-)', 6, 1, None, None, None, None, None, None), (u'gl\xfccklich', u'gl\xfccklich', 1, 1, None, None, None, None, None, None), (u'gl\xfccklich++gemacht++!++:-)++-)', u'gl\xfccklich++gemacht++!++:-)++-)', 5, 1, None, None, None, None, None, None), (u'.++trotzdem++hat++sie++mich++gl\xfccklich', u'.++trotzdem++hat++sie++mich++gl\xfccklich', 6, 1, None, None, None, None, None, None), (u'gemacht++!++:-)++-)', u'gemacht++!++:-)++-)', 4, 1, None, None, None, None, None, None), (u'klitze++kleine++\xfcberaschung++.++trotzdem++hat', u'klitz++klein++\xfcberaschung++.++trotzdem++hat', 6, 1, None, None, None, None, None, None), (u'mich++gl\xfccklich++gemacht', u'mich++gl\xfccklich++gemacht', 3, 1, None, None, None, None, None, None), (u'gemacht', u'gemacht', 1, 1, None, None, None, None, None, None), (u'!++:-)', u'!++:-)', 2, 1, None, None, None, None, None, None), (u'.++trotzdem++hat++sie++mich', u'.++trotzdem++hat++sie++mich', 5, 1, None, None, None, None, None, None), (u'trotzdem++hat++sie++mich++gl\xfccklich++gemacht', u'trotzdem++hat++sie++mich++gl\xfccklich++gemacht', 6, 1, None, None, None, None, None, None), (u'\xfcberaschung++.++trotzdem', u'\xfcberaschung++.++trotzdem', 3, 1, None, None, None, None, None, None), (u'klitze++kleine++\xfcberaschung++.++trotzdem', u'klitz++klein++\xfcberaschung++.++trotzdem', 5, 1, None, None, None, None, None, None), (u':-)++-)', u':-)++-)', 2, 1, None, None, None, None, None, None), (u'gl\xfccklich++gemacht++!', u'gl\xfccklich++gemacht++!', 3, 1, None, None, None, None, None, None), (u'\xfcberaschung++.', u'\xfcberaschung++.', 2, 1, None, None, None, None, None, None), (u'hat++sie++mich++gl\xfccklich++gemacht', u'hat++sie++mich++gl\xfccklich++gemacht', 5, 1, None, None, None, None, None, None), (u'trotzdem++hat++sie++mich++gl\xfccklich', u'trotzdem++hat++sie++mich++gl\xfccklich', 5, 1, None, None, None, None, None, None), (u'klitze++kleine', u'klitz++klein', 2, 1, None, None, None, None, None, None), (u'sie++mich++gl\xfccklich++gemacht++!++:-)', u'sie++mich++gl\xfccklich++gemacht++!++:-)', 6, 1, None, None, None, None, None, None), (u'\xfcberaschung', u'\xfcberaschung', 1, 1, None, None, None, None, None, None), (u'trotzdem++hat++sie', u'trotzdem++hat++sie', 3, 1, None, None, None, None, None, None), (u'kleine', u'klein', 1, 2, None, None, None, None, None, None), (u'-)', u'-)', 1, 1, None, None, None, None, None, None), (u'trotzdem++hat++sie++mich', u'trotzdem++hat++sie++mich', 4, 1, None, None, None, None, None, None), (u'trotzdem++hat', u'trotzdem++hat', 2, 1, None, None, None, None, None, None), (u'.', u'.', 1, 1, None, None, None, None, None, None), (u'trotzdem', u'trotzdem', 1, 1, None, None, None, None, None, None), (u'hat', u'hat', 1, 1, None, None, None, None, None, None), (u'mich', u'mich', 1, 1, None, None, None, None, None, None), (u'.++trotzdem++hat', u'.++trotzdem++hat', 3, 1, None, None, None, None, None, None), (u'klitze', u'klitz', 1, 2, None, None, None, None, None, None), (u'hat++sie', u'hat++sie', 2, 1, None, None, None, None, None, None), (u'hat++sie++mich++gl\xfccklich++gemacht++!', u'hat++sie++mich++gl\xfccklich++gemacht++!', 6, 1, None, None, None, None, None, None), (u'gemacht++!++:-)', u'gemacht++!++:-)', 3, 1, None, None, None, None, None, None), (u'hat++sie++mich++gl\xfccklich', u'hat++sie++mich++gl\xfccklich', 4, 1, None, None, None, None, None, None), (u'kleine++\xfcberaschung++.++trotzdem', u'klein++\xfcberaschung++.++trotzdem', 4, 1, None, None, None, None, None, None), (u'kleine++\xfcberaschung++.++trotzdem++hat', u'klein++\xfcberaschung++.++trotzdem++hat', 5, 1, None, None, None, None, None, None), (u'.++trotzdem++hat++sie', u'.++trotzdem++hat++sie', 4, 1, None, None, None, None, None, None), (u'kleine++\xfcberaschung++.++trotzdem++hat++sie', u'klein++\xfcberaschung++.++trotzdem++hat++sie', 6, 1, None, None, None, None, None, None), (u'\xfcberaschung++.++trotzdem++hat++sie++mich', u'\xfcberaschung++.++trotzdem++hat++sie++mich', 6, 1, None, None, None, None, None, None), (u'mich++gl\xfccklich++gemacht++!++:-)', u'mich++gl\xfccklich++gemacht++!++:-)', 5, 1, None, None, None, None, None, None), (u'mich++gl\xfccklich', u'mich++gl\xfccklich', 2, 1, None, None, None, None, None, None), (u'\xfcberaschung++.++trotzdem++hat++sie', u'\xfcberaschung++.++trotzdem++hat++sie', 5, 1, None, None, None, None, None, None), (u'sie++mich', u'sie++mich', 2, 1, None, None, None, None, None, None), (u'sie', u'sie', 1, 1, None, None, None, None, None, None), (u'gl\xfccklich++gemacht++!++:-)', u'gl\xfccklich++gemacht++!++:-)', 4, 1, None, None, None, None, None, None), (u'klitze++kleine++\xfcberaschung', u'klitz++klein++\xfcberaschung', 3, 1, None, None, None, None, None, None), (u'\xfcberaschung++.++trotzdem++hat', u'\xfcberaschung++.++trotzdem++hat', 4, 1, None, None, None, None, None, None), (u'klitze++kleine++\xfcberaschung++.', u'klitz++klein++\xfcberaschung++.', 4, 1, None, None, None, None, None, None), (u'!++:-)++-)', u'!++:-)++-)', 3, 1, None, None, None, None, None, None), (u'mich++gl\xfccklich++gemacht++!', u'mich++gl\xfccklich++gemacht++!', 4, 1, None, None, None, None, None, None), (u'kleine++\xfcberaschung++.', u'klein++\xfcberaschung++.', 3, 1, None, None, None, None, None, None), (u'sie++mich++gl\xfccklich++gemacht', u'sie++mich++gl\xfccklich++gemacht', 4, 1, None, None, None, None, None, None), (u'kleine++\xfcberaschung', u'klein++\xfcberaschung', 2, 1, None, None, None, None, None, None)])

        

        ##### SECOND INSETION
        #stats._compute([copy.deepcopy(self.test_dict_row_de_1)])
        text_list = [self.test_dict_row_de_1["id"], self.test_dict_row_de_1["text"] ]
        stats._compute([copy.deepcopy(text_list)])

        redu = stats.statsdb.getall("reduplications")
        repl = stats.statsdb.getall("replications")
        baseline = stats.statsdb.getall("baseline")

        # p(redu,"redu")
        # p(repl,"repl")
        #p(baseline,"baseline")
        #time.sleep(7)

        redu.should.be.equal(
                                [(1, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]'), (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), (3, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]'), (4, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]')]
                            )
        
        repl.should.be.equal(
                                [(1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]'), (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), (4, 8888, u'[4, 9]', u'[1, 7]', u'[1, 7]', u':-)', u':-)^4', u':-)', u')', 4, 2, None, u'EMOASC', u'["positive", 0.5]', u'sie', u'["PPER", null, "sie"]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "gl\\u00fccklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u'-)', u'["EMOASC", null, "-)"]', None, None, None, None, None, None, None, None), (5, 8888, u'[4, 9]', u'[1, 8]', u'[1, 8]', u'-)', u'-)^3', u'-)', u')', 3, 1, None, u'EMOASC', u'["positive", 0.5]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "gl\\u00fccklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', None, None, None, None, None, None, None, None, None, None), (6, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]'), (7, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), (8, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "\\u00fcberaschung"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzdem"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'), (9, 8888, u'[4, 9]', u'[1, 7]', u'[1, 7]', u':-)', u':-)^4', u':-)', u')', 4, 2, None, u'EMOASC', u'["positive", 0.5]', u'sie', u'["PPER", null, "sie"]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "gl\\u00fccklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u'-)', u'["EMOASC", null, "-)"]', None, None, None, None, None, None, None, None), (10, 8888, u'[4, 9]', u'[1, 8]', u'[1, 8]', u'-)', u'-)^3', u'-)', u')', 3, 1, None, u'EMOASC', u'["positive", 0.5]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "gl\\u00fccklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', None, None, None, None, None, None, None, None, None, None)]
                            )
        
        baseline.should.be.equal([(u'.++trotzdem', u'.++trotzdem', 2, 2, None, None, None, None, None, None), (u'!', u'!', 1, 2, None, None, None, None, None, None), (u'hat++sie++mich', u'hat++sie++mich', 3, 2, None, None, None, None, None, None), (u'sie++mich++gl\xfccklich++gemacht++!', u'sie++mich++gl\xfccklich++gemacht++!', 5, 2, None, None, None, None, None, None), (u'gemacht++!', u'gemacht++!', 2, 2, None, None, None, None, None, None), (u'gl\xfccklich++gemacht', u'gl\xfccklich++gemacht', 2, 2, None, None, None, None, None, None), (u'sie++mich++gl\xfccklich', u'sie++mich++gl\xfccklich', 3, 2, None, None, None, None, None, None), (u':-)', u':-)', 1, 2, None, None, None, None, None, None), (u'mich++gl\xfccklich++gemacht++!++:-)++-)', u'mich++gl\xfccklich++gemacht++!++:-)++-)', 6, 2, None, None, None, None, None, None), (u'gl\xfccklich', u'gl\xfccklich', 1, 2, None, None, None, None, None, None), (u'gl\xfccklich++gemacht++!++:-)++-)', u'gl\xfccklich++gemacht++!++:-)++-)', 5, 2, None, None, None, None, None, None), (u'.++trotzdem++hat++sie++mich++gl\xfccklich', u'.++trotzdem++hat++sie++mich++gl\xfccklich', 6, 2, None, None, None, None, None, None), (u'gemacht++!++:-)++-)', u'gemacht++!++:-)++-)', 4, 2, None, None, None, None, None, None), (u'klitze++kleine++\xfcberaschung++.++trotzdem++hat', u'klitz++klein++\xfcberaschung++.++trotzdem++hat', 6, 2, None, None, None, None, None, None), (u'mich++gl\xfccklich++gemacht', u'mich++gl\xfccklich++gemacht', 3, 2, None, None, None, None, None, None), (u'gemacht', u'gemacht', 1, 2, None, None, None, None, None, None), (u'!++:-)', u'!++:-)', 2, 2, None, None, None, None, None, None), (u'.++trotzdem++hat++sie++mich', u'.++trotzdem++hat++sie++mich', 5, 2, None, None, None, None, None, None), (u'trotzdem++hat++sie++mich++gl\xfccklich++gemacht', u'trotzdem++hat++sie++mich++gl\xfccklich++gemacht', 6, 2, None, None, None, None, None, None), (u'\xfcberaschung++.++trotzdem', u'\xfcberaschung++.++trotzdem', 3, 2, None, None, None, None, None, None), (u'klitze++kleine++\xfcberaschung++.++trotzdem', u'klitz++klein++\xfcberaschung++.++trotzdem', 5, 2, None, None, None, None, None, None), (u':-)++-)', u':-)++-)', 2, 2, None, None, None, None, None, None), (u'gl\xfccklich++gemacht++!', u'gl\xfccklich++gemacht++!', 3, 2, None, None, None, None, None, None), (u'\xfcberaschung++.', u'\xfcberaschung++.', 2, 2, None, None, None, None, None, None), (u'hat++sie++mich++gl\xfccklich++gemacht', u'hat++sie++mich++gl\xfccklich++gemacht', 5, 2, None, None, None, None, None, None), (u'trotzdem++hat++sie++mich++gl\xfccklich', u'trotzdem++hat++sie++mich++gl\xfccklich', 5, 2, None, None, None, None, None, None), (u'klitze++kleine', u'klitz++klein', 2, 2, None, None, None, None, None, None), (u'sie++mich++gl\xfccklich++gemacht++!++:-)', u'sie++mich++gl\xfccklich++gemacht++!++:-)', 6, 2, None, None, None, None, None, None), (u'\xfcberaschung', u'\xfcberaschung', 1, 2, None, None, None, None, None, None), (u'trotzdem++hat++sie', u'trotzdem++hat++sie', 3, 2, None, None, None, None, None, None), (u'kleine', u'klein', 1, 4, None, None, None, None, None, None), (u'-)', u'-)', 1, 2, None, None, None, None, None, None), (u'trotzdem++hat++sie++mich', u'trotzdem++hat++sie++mich', 4, 2, None, None, None, None, None, None), (u'trotzdem++hat', u'trotzdem++hat', 2, 2, None, None, None, None, None, None), (u'.', u'.', 1, 2, None, None, None, None, None, None), (u'trotzdem', u'trotzdem', 1, 2, None, None, None, None, None, None), (u'hat', u'hat', 1, 2, None, None, None, None, None, None), (u'mich', u'mich', 1, 2, None, None, None, None, None, None), (u'.++trotzdem++hat', u'.++trotzdem++hat', 3, 2, None, None, None, None, None, None), (u'klitze', u'klitz', 1, 4, None, None, None, None, None, None), (u'hat++sie', u'hat++sie', 2, 2, None, None, None, None, None, None), (u'hat++sie++mich++gl\xfccklich++gemacht++!', u'hat++sie++mich++gl\xfccklich++gemacht++!', 6, 2, None, None, None, None, None, None), (u'gemacht++!++:-)', u'gemacht++!++:-)', 3, 2, None, None, None, None, None, None), (u'hat++sie++mich++gl\xfccklich', u'hat++sie++mich++gl\xfccklich', 4, 2, None, None, None, None, None, None), (u'kleine++\xfcberaschung++.++trotzdem', u'klein++\xfcberaschung++.++trotzdem', 4, 2, None, None, None, None, None, None), (u'kleine++\xfcberaschung++.++trotzdem++hat', u'klein++\xfcberaschung++.++trotzdem++hat', 5, 2, None, None, None, None, None, None), (u'.++trotzdem++hat++sie', u'.++trotzdem++hat++sie', 4, 2, None, None, None, None, None, None), (u'kleine++\xfcberaschung++.++trotzdem++hat++sie', u'klein++\xfcberaschung++.++trotzdem++hat++sie', 6, 2, None, None, None, None, None, None), (u'\xfcberaschung++.++trotzdem++hat++sie++mich', u'\xfcberaschung++.++trotzdem++hat++sie++mich', 6, 2, None, None, None, None, None, None), (u'mich++gl\xfccklich++gemacht++!++:-)', u'mich++gl\xfccklich++gemacht++!++:-)', 5, 2, None, None, None, None, None, None), (u'mich++gl\xfccklich', u'mich++gl\xfccklich', 2, 2, None, None, None, None, None, None), (u'\xfcberaschung++.++trotzdem++hat++sie', u'\xfcberaschung++.++trotzdem++hat++sie', 5, 2, None, None, None, None, None, None), (u'sie++mich', u'sie++mich', 2, 2, None, None, None, None, None, None), (u'sie', u'sie', 1, 2, None, None, None, None, None, None), (u'gl\xfccklich++gemacht++!++:-)', u'gl\xfccklich++gemacht++!++:-)', 4, 2, None, None, None, None, None, None), (u'klitze++kleine++\xfcberaschung', u'klitz++klein++\xfcberaschung', 3, 2, None, None, None, None, None, None), (u'\xfcberaschung++.++trotzdem++hat', u'\xfcberaschung++.++trotzdem++hat', 4, 2, None, None, None, None, None, None), (u'klitze++kleine++\xfcberaschung++.', u'klitz++klein++\xfcberaschung++.', 4, 2, None, None, None, None, None, None), (u'!++:-)++-)', u'!++:-)++-)', 3, 2, None, None, None, None, None, None), (u'mich++gl\xfccklich++gemacht++!', u'mich++gl\xfccklich++gemacht++!', 4, 2, None, None, None, None, None, None), (u'kleine++\xfcberaschung++.', u'klein++\xfcberaschung++.', 3, 2, None, None, None, None, None, None), (u'sie++mich++gl\xfccklich++gemacht', u'sie++mich++gl\xfccklich++gemacht', 4, 2, None, None, None, None, None, None), (u'kleine++\xfcberaschung', u'klein++\xfcberaschung', 2, 2, None, None, None, None, None, None)])

        # # ########### EN ##############






    @attr(status='stable')
    #@wipd
    def test_get_streams_from_corp_609(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode, status_bar = False)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)

        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        rownum = corp.corpdb.rownum("documents")
        stats._init_compution_variables()
        stats._text_field_name = corp.info()["text_field_name"]
        stats._id_field_name =  corp.info()["id_field_name"]
        #p((self._text_field_name, self._id_field_name))
        #p(rownum, "rownum")
        ### Try 1
        stream_num = 4
        streams = stats.get_streams_from_corpus(corp,stream_num )
        all_rows_from_corpus = []
        for stream in streams:
            rows = list(stream[1])
            all_rows_from_corpus += rows
            len(stream[1]).should.be.equal(len(rows))

        rows_as_text = [unicode(row) for row in all_rows_from_corpus]
        #p((rows_as_text,))
        len(rows_as_text).should.be.equal(rownum)
        len(rows_as_text).should.be.equal(len(set(rows_as_text)))


        ### Try 2
        stream_num = 1
        streams = stats.get_streams_from_corpus(corp,stream_num )
        all_rows_from_corpus = []
        #p(( streams, len(streams[0][1]), len(list(streams[0][1]))  ))
        for stream in streams:
            rows = list(stream[1])
            all_rows_from_corpus += rows
            len(stream[1]).should.be.equal(len(rows))

        rows_as_text = [unicode(row) for row in all_rows_from_corpus]
        len(rows_as_text).should.be.equal(rownum)
        len(rows_as_text).should.be.equal(len(set(rows_as_text)))



    @attr(status='stable')
    #@wipd
    def test_preprocess_610(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        

        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)


        #######without_closing_db_at_the_end #########
        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, baseline_delimiter="++",
                    encryption_key=encryption_key,
                    ignore_hashtag=True, force_cleaning=True,
                    ignore_url=True,  ignore_mention=True, ignore_punkt=True, ignore_num=True)

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))

        #stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False)
        stats.corp = corp
        stats._corp_info  = stats.corp.info()
        stats._init_compution_variables()
        stats._compute_cleaning_flags()
        text_elem = [[[[u'I', u'PRP'], [u'loved', u'VBD'], [u'it', u'PRP'], [u'.', u'symbol']], [u'positive', 0.7]], [[[u'But', u'CC'], [u'it', u'PRP'], [u'was', u'VBD'], [u'also', u'RB'], [u'verrrryyyyy', u'JJ'], [u'vvveRRRRRRrry', u'NNP'], [u'very', u'RB'], [u'piiiiiiiiity', u'JJ'], [u'pity', u'NN'], [u'pity', u'NN'], [u'piiitttyyy', u'NN'], [u'for', u'IN'], [u'me', u'PRP'], [u'......', u'symbol'], [u':-(((((', u'EMOASC'], [u'@real_trump', u'mention'], [u'#sheetlife', u'hashtag'], [u'#readytogo', u'hashtag'], [u'http://www.absurd.com', u'URL']], [u'negative', -0.1875]]]

        results = stats._preprocess(text_elem)
        #p(results, "results")
        right_results = [([(u'i', u'PRP'), (u'loved', u'VBD'), (u'it', u'PRP'), (None, ':symbol:')], [u'positive', 0.7]), ([(u'but', u'CC'), (u'it', u'PRP'), (u'was', u'VBD'), (u'also', u'RB'), (u'verrrryyyyy', u'JJ'), (u'vvverrrrrrrry', u'NNP'), (u'very', u'RB'), (u'piiiiiiiiity', u'JJ'), (u'pity', u'NN'), (u'pity', u'NN'), (u'piiitttyyy', u'NN'), (u'for', u'IN'), (u'me', u'PRP'), (None, ':symbol:'), (u':-(((((', u'EMOASC'), (None, ':mention:'), (None, ':hashtag:'), (None, ':hashtag:'), (None, ':URL:')], [u'negative', -0.1875])]
        results.should.be.equal(right_results)






    @attr(status='stable')
    #@wipd
    def test_main_compute_function_lower_case_for_1_stream__610_1(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
 

        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)


        #######without_closing_db_at_the_end #########
        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))

        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")

        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,self.configer._counted_reps["en"],repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

 
        #######with_closing_db_at_the_end #########

        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))

        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=True)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")
        
        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,self.configer._counted_reps["en"],repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False




    @attr(status='stable')
    #@wipd
    def test_main_compute_function_lower_case_for_4_streams_610_2(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
 

        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        #stats = Corpus(logger_level=logging.DEBUG)


        #######without_closing_db_at_the_end #########
        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))

        stats.compute(corp,stream_number=4,adjust_to_cpu=False, freeze_db=False)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")

        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,self.configer._counted_reps["en"],repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False



        #######with_closing_db_at_the_end #########

        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, baseline_delimiter="++")

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))

        stats.compute(corp,stream_number=4,adjust_to_cpu=False, freeze_db=True)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")

        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,self.configer._counted_reps["en"],repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False



    @attr(status='stable')
    #@wipd
    def test_main_compute_function_lower_case_for_1_stream_with_preprocessing_and_frozen_610_3(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        ### Compute Golden Standard Data ##
        precomputed_data = copy.deepcopy(self.configer._counted_reps["en"])
        del precomputed_data["1"]
        del precomputed_data[u'#shetlife']
        del precomputed_data[u'.']
        del precomputed_data[u'?']
        precomputed_data[":hashtag:"] = {'baseline': 4, 'redu': (2, 4)}
        right_rep_num = {
                            "repls":sum([data["repl"][1] for word, data in precomputed_data.items() if "repl" in data ]),
                            "redus":sum([data["redu"][0] for word, data in precomputed_data.items() if "redu" in data ]),
                        }

        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))

    ########################################################################################
    ##################################################################
    ######## full_repetativ_syntagma=False
    ########################################################################################
    ########################################################################################
        #self.mode = "prod+"
        #####NOT FREEZED #####
        #### baseline_insertion_border=10 ####
        stats = Stats(mode=self.mode,use_cash=True,status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, baseline_delimiter="++",
                    encryption_key=encryption_key,
                    ignore_hashtag=True, force_cleaning=True,
                    ignore_url=True,  ignore_mention=True, ignore_punkt=True, ignore_num=True)

        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False, baseline_insertion_border=10)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")

        #repls.should.be.equal(right_repls)
        #redus.should.be.equal(right_redus)

        #p(right_rep_num)
        self._check_correctnes(stats.col_index_orig,precomputed_data,repls=repls, redus=redus, baseline=baseline) 
        right_rep_num["repls"].should.be.equal(len(repls))
        right_rep_num["redus"].should.be.equal(len(redus))


        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False








    @attr(status='stable')
    #@wipd
    def test_main_compute_function_lower_case_for_1_stream_with_and_without_optimization_610_4(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)

        right_repls = [(1, 1111, u'[4, 14]', u'[1, 4]', u'[1, 4]', u'very', u'ver^4y^5', u'veri', u'r', 4, 2, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (2, 1111, u'[4, 14]', u'[1, 4]', u'[1, 4]', u'very', u'ver^4y^5', u'veri', u'y', 5, 3, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (3, 1111, u'[4, 14]', u'[1, 5]', u'[1, 4]', u'very', u'v^3er^8y', u'veri', u'v', 3, 0, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (4, 1111, u'[4, 14]', u'[1, 5]', u'[1, 4]', u'very', u'v^3er^8y', u'veri', u'r', 8, 2, u'[1, 4]', u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (5, 1111, u'[4, 14]', u'[1, 7]', u'[1, 5]', u'pity', u'pi^9ty', u'piti', u'i', 9, 1, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (6, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u'i', 3, 1, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (7, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u't', 3, 2, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (8, 1111, u'[4, 14]', u'[1, 10]', u'[1, 5]', u'pity', u'pi^3t^3y^3', u'piti', u'y', 3, 3, u'[1, 5]', u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (9, 1111, u'[4, 14]', u'[1, 13]', u'[1, 8]', u'.', u'.^6', u'.', u'.', 6, 0, None, u'symbol', u'["negative", -0.1875]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]', u'#shetlife', u'["hashtag", null, "#shetlif"]', u'#readytogo', u'["hashtag", null, "#readytogo"]', u'http://www.absurd.com', u'["URL", null, "http://www.absurd.com"]'), (10, 1111, u'[4, 14]', u'[1, 14]', u'[1, 9]', u':-(', u':-(^5', u':-(', u'(', 5, 2, None, u'EMOASC', u'["negative", -0.1875]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u'@real_trump', u'["mention", null, "@real_trump"]', u'#shetlife', u'["hashtag", null, "#shetlif"]', u'#readytogo', u'["hashtag", null, "#readytogo"]', u'http://www.absurd.com', u'["URL", null, "http://www.absurd.com"]', None, None), (11, 2222, u'[5]', u'[0, 0]', u'[0, 0]', u'glad', u'gla^7d', u'glad', u'a', 7, 2, None, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'to', u'["TO", null, "to"]', u'se', u'["VB", null, "se"]', u'you', u'["PRP", null, "you"]', u'-)', u'["EMOASC", null, "-)"]', None, None), (12, 2222, u'[5]', u'[0, 2]', u'[0, 2]', u'se', u'se^9', u'se', u'e', 9, 1, None, u'VB', u'["neutral", 0.0]', None, None, None, None, None, None, u'glad', u'["NN", null, "glad"]', u'to', u'["TO", null, "to"]', u'you', u'["PRP", null, "you"]', u'-)', u'["EMOASC", null, "-)"]', None, None, None, None, None, None), (13, 2222, u'[5]', u'[0, 4]', u'[0, 4]', u'-)', u'-)^4', u'-)', u')', 4, 1, None, u'EMOASC', u'["neutral", 0.0]', None, None, u'glad', u'["NN", null, "glad"]', u'to', u'["TO", null, "to"]', u'se', u'["VB", null, "se"]', u'you', u'["PRP", null, "you"]', None, None, None, None, None, None, None, None, None, None), (14, 3333, u'[15]', u'[0, 1]', u'[0, 1]', u'bad', u'bad^5', u'bad', u'd', 5, 2, u'[0, 1]', u'JJ', u'["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, u'a', u'["DT", null, "a"]', u'news', u'["NN", null, "news"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (15, 3333, u'[15]', u'[0, 3]', u'[0, 1]', u'bad', u'b^7a^6d', u'bad', u'b', 7, 0, u'[0, 1]', u'JJ', u'["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, u'a', u'["DT", null, "a"]', u'news', u'["NN", null, "news"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (16, 3333, u'[15]', u'[0, 3]', u'[0, 1]', u'bad', u'b^7a^6d', u'bad', u'a', 6, 1, u'[0, 1]', u'JJ', u'["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, u'a', u'["DT", null, "a"]', u'news', u'["NN", null, "news"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (17, 3333, u'[15]', u'[0, 4]', u'[0, 1]', u'bad', u'b^4a^4d^5', u'bad', u'b', 4, 0, u'[0, 1]', u'JJ', u'["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, u'a', u'["DT", null, "a"]', u'news', u'["NN", null, "news"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (18, 3333, u'[15]', u'[0, 4]', u'[0, 1]', u'bad', u'b^4a^4d^5', u'bad', u'a', 4, 1, u'[0, 1]', u'JJ', u'["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, u'a', u'["DT", null, "a"]', u'news', u'["NN", null, "news"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (19, 3333, u'[15]', u'[0, 4]', u'[0, 1]', u'bad', u'b^4a^4d^5', u'bad', u'd', 5, 2, u'[0, 1]', u'JJ', u'["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, u'a', u'["DT", null, "a"]', u'news', u'["NN", null, "news"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (20, 3333, u'[15]', u'[0, 5]', u'[0, 1]', u'bad', u'ba^7d', u'bad', u'a', 7, 1, u'[0, 1]', u'JJ', u'["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, u'a', u'["DT", null, "a"]', u'news', u'["NN", null, "news"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (21, 3333, u'[15]', u'[0, 14]', u'[0, 10]', u'-(', u'-(^4', u'-(', u'(', 4, 1, None, u'EMOASC', u'["negative", -0.7249999999999999]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]', u'not', u'["RB", null, "not"]', u'acept', u'["VB", null, "acept"]', u'.', u'["symbol", null, "."]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u':-(', u'["EMOASC", null, ":-("]', u'#shetlife', u'["hashtag", {"#shetlife": 2}, "#shetlif"]', u'http://www.noooo.com', u'["URL", null, "http://www.noooo.com"]', None, None), (22, 3333, u'[15]', u'[0, 15]', u'[0, 11]', u'\U0001f62b', u'\U0001f62b^12', u'\U0001f62b', u'\U0001f62b', 12, 0, None, u'EMOIMG', u'["negative", -0.7249999999999999]', u'can', u'["MD", null, "can"]', u'not', u'["RB", null, "not"]', u'acept', u'["VB", null, "acept"]', u'.', u'["symbol", null, "."]', u'-(', u'["EMOASC", null, "-("]', u':-(', u'["EMOASC", null, ":-("]', u'#shetlife', u'["hashtag", {"#shetlife": 2}, "#shetlif"]', u'http://www.noooo.com', u'["URL", null, "http://www.noooo.com"]', None, None, None, None), (23, 3333, u'[15]', u'[0, 16]', u'[0, 12]', u':-(', u':-(^5', u':-(', u'(', 5, 2, None, u'EMOASC', u'["negative", -0.7249999999999999]', u'not', u'["RB", null, "not"]', u'acept', u'["VB", null, "acept"]', u'.', u'["symbol", null, "."]', u'-(', u'["EMOASC", null, "-("]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u'#shetlife', u'["hashtag", {"#shetlife": 2}, "#shetlif"]', u'http://www.noooo.com', u'["URL", null, "http://www.noooo.com"]', None, None, None, None, None, None), (24, 4444, u'[13]', u'[0, 6]', u'[0, 1]', u'model', u'mo^7del^7', u'model', u'o', 7, 1, None, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'tiny', u'["JJ", {"tiny": 6}, "tini"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]', u'use', u'["VB", null, "use"]'), (25, 4444, u'[13]', u'[0, 6]', u'[0, 1]', u'model', u'mo^7del^7', u'model', u'l', 7, 4, None, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'tiny', u'["JJ", {"tiny": 6}, "tini"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]', u'use', u'["VB", null, "use"]'), (26, 4444, u'[13]', u'[0, 15]', u'[0, 10]', u'big', u'bi^3g', u'big', u'i', 3, 1, u'[0, 10]', u'NN', u'["neutral", 0.0]', u'can', u'["MD", null, "can"]', u'use', u'["VB", null, "use"]', u'for', u'["IN", null, "for"]', u'explain', u'["VB", null, "explain"]', u'a', u'["DT", null, "a"]', u'things', u'["NNS", null, "thing"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None), (27, 4444, u'[13]', u'[0, 16]', u'[0, 10]', u'big', u'bi^15g', u'big', u'i', 15, 1, u'[0, 10]', u'NN', u'["neutral", 0.0]', u'can', u'["MD", null, "can"]', u'use', u'["VB", null, "use"]', u'for', u'["IN", null, "for"]', u'explain', u'["VB", null, "explain"]', u'a', u'["DT", null, "a"]', u'things', u'["NNS", null, "thing"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None), (28, 5555, u'[8, 2, 11, 4]', u'[0, 8]', u'[0, 6]', u'explanation', u'expla^5nation', u'explan', u'a', 5, 4, None, u'NN', u'["neutral", 0.0]', u'model', u'["NN", null, "model"]', u',', u'["symbol", null, ","]', u'but', u'["CC", null, "but"]', u'a', u'["DT", null, "a"]', u'big', u'["JJ", {"big": 3}, "big"]', u'.', u'["symbol", null, "."]', u'right', u'["UH", null, "right"]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]'), (29, 5555, u'[8, 2, 11, 4]', u'[1, 0]', u'[1, 0]', u'right', u'ri^6ght', u'right', u'i', 6, 1, None, u'UH', u'["neutral", 0.0]', u'but', u'["CC", null, "but"]', u'a', u'["DT", null, "a"]', u'big', u'["JJ", {"big": 3}, "big"]', u'explanation', u'["NN", null, "explan"]', u'.', u'["symbol", null, "."]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]', u'you', u'["PRP", null, "you"]', u'think', u'["VB", null, "think"]'), (30, 5555, u'[8, 2, 11, 4]', u'[2, 2]', u'[2, 2]', u'you', u'you^6', u'you', u'u', 6, 2, None, u'PRP', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'right', u'["UH", null, "right"]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]', u'do', u'["VBP", null, "do"]', u'think', u'["VB", null, "think"]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]'), (31, 5555, u'[8, 2, 11, 4]', u'[2, 6]', u'[2, 6]', u'?', u'?^4', u'?', u'?', 4, 0, None, u'symbol', u'["neutral", 0.0]', u'do', u'["VBP", null, "do"]', u'you', u'["PRP", null, "you"]', u'think', u'["VB", null, "think"]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]'), (32, 5555, u'[8, 2, 11, 4]', u'[2, 7]', u'[2, 7]', u'1', u'1^6', u'1', u'1', 6, 0, None, u'number', u'["neutral", 0.0]', u'you', u'["PRP", null, "you"]', u'think', u'["VB", null, "think"]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', u'?', u'["symbol", null, "?"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]'), (33, 5555, u'[8, 2, 11, 4]', u'[2, 8]', u'[2, 8]', u'\U0001f62b', u'\U0001f62b^4', u'\U0001f62b', u'\U0001f62b', 4, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'think', u'["VB", null, "think"]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]'), (34, 5555, u'[8, 2, 11, 4]', u'[2, 9]', u'[2, 9]', u'1', u'1^8', u'1', u'1', 8, 0, None, u'number', u'["neutral", 0.0]', u'about', u'["IN", null, "about"]', u'it', u'["PRP", null, "it"]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]'), (35, 5555, u'[8, 2, 11, 4]', u'[3, 0]', u'[3, 0]', u'but', u'b^5u^4t^4', u'but', u'b', 5, 0, u'[3, 0]', u'NNP', u'["neutral", 0.0]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None), (36, 5555, u'[8, 2, 11, 4]', u'[3, 0]', u'[3, 0]', u'but', u'b^5u^4t^4', u'but', u'u', 4, 1, u'[3, 0]', u'NNP', u'["neutral", 0.0]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None), (37, 5555, u'[8, 2, 11, 4]', u'[3, 0]', u'[3, 0]', u'but', u'b^5u^4t^4', u'but', u't', 4, 2, u'[3, 0]', u'NNP', u'["neutral", 0.0]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None), (38, 5555, u'[8, 2, 11, 4]', u'[3, 1]', u'[3, 0]', u'but', u'bu^5t^4', u'but', u'u', 5, 1, u'[3, 0]', u'NNP', u'["neutral", 0.0]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None), (39, 5555, u'[8, 2, 11, 4]', u'[3, 1]', u'[3, 0]', u'but', u'bu^5t^4', u'but', u't', 4, 2, u'[3, 0]', u'NNP', u'["neutral", 0.0]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None), (40, 5555, u'[8, 2, 11, 4]', u'[3, 2]', u'[3, 1]', u'you', u'y^6ou', u'you', u'y', 6, 0, u'[3, 1]', u'NN', u'["neutral", 0.0]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None), (41, 5555, u'[8, 2, 11, 4]', u'[3, 3]', u'[3, 1]', u'you', u'yo^6u', u'you', u'o', 6, 1, u'[3, 1]', u'NN', u'["neutral", 0.0]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None), (42, 5555, u'[8, 2, 11, 4]', u'[3, 4]', u'[3, 2]', u'but', u'b^6ut', u'but', u'b', 6, 0, u'[3, 2]', u'FW', u'["neutral", 0.0]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None, None, None), (43, 5555, u'[8, 2, 11, 4]', u'[3, 5]', u'[3, 2]', u'but', u'b^5ut^4', u'but', u'b', 5, 0, u'[3, 2]', u'FW', u'["neutral", 0.0]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None, None, None), (44, 5555, u'[8, 2, 11, 4]', u'[3, 5]', u'[3, 2]', u'but', u'b^5ut^4', u'but', u't', 4, 2, u'[3, 2]', u'FW', u'["neutral", 0.0]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None, None, None), (45, 5555, u'[8, 2, 11, 4]', u'[3, 6]', u'[3, 2]', u'but', u'b^5u^5t', u'but', u'b', 5, 0, u'[3, 2]', u'FW', u'["neutral", 0.0]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None, None, None), (46, 5555, u'[8, 2, 11, 4]', u'[3, 6]', u'[3, 2]', u'but', u'b^5u^5t', u'but', u'u', 5, 1, u'[3, 2]', u'FW', u'["neutral", 0.0]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None, None, None), (47, 5555, u'[8, 2, 11, 4]', u'[3, 7]', u'[3, 3]', u'you', u'y^3o^2u^4', u'you', u'y', 3, 0, None, u'FW', u'["neutral", 0.0]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', None, None, None, None, None, None, None, None, None, None), (48, 5555, u'[8, 2, 11, 4]', u'[3, 7]', u'[3, 3]', u'you', u'y^3o^2u^4', u'you', u'u', 4, 2, None, u'FW', u'["neutral", 0.0]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', None, None, None, None, None, None, None, None, None, None), (49, 6666, u'[3, 9]', u'[0, 0]', u'[0, 0]', u'tiny', u'tin^3y^2', u'tini', u'n', 3, 2, u'[0, 0]', u'JJ', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]'), (50, 6666, u'[3, 9]', u'[1, 0]', u'[1, 0]', u'but', u'b^5ut', u'but', u'b', 5, 0, u'[1, 0]', u'NNP', u'["neutral", 0.0]', None, None, None, None, u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]'), (51, 6666, u'[3, 9]', u'[1, 1]', u'[1, 0]', u'but', u'bu^5t', u'but', u'u', 5, 1, u'[1, 0]', u'NNP', u'["neutral", 0.0]', None, None, None, None, u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]'), (52, 6666, u'[3, 9]', u'[1, 2]', u'[1, 1]', u'you', u'y^6ou', u'you', u'y', 6, 0, u'[1, 1]', u'JJ', u'["neutral", 0.0]', None, None, u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (53, 6666, u'[3, 9]', u'[1, 3]', u'[1, 1]', u'you', u'yo^6u', u'you', u'o', 6, 1, u'[1, 1]', u'JJ', u'["neutral", 0.0]', None, None, u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (54, 6666, u'[3, 9]', u'[1, 4]', u'[1, 2]', u'but', u'b^6ut', u'but', u'b', 6, 0, u'[1, 2]', u'CC', u'["neutral", 0.0]', u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]'), (55, 6666, u'[3, 9]', u'[1, 5]', u'[1, 2]', u'but', u'b^5ut', u'but', u'b', 5, 0, u'[1, 2]', u'CC', u'["neutral", 0.0]', u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]'), (56, 6666, u'[3, 9]', u'[1, 6]', u'[1, 2]', u'but', u'b^5ut', u'but', u'b', 5, 0, u'[1, 2]', u'CC', u'["neutral", 0.0]', u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]'), (57, 6666, u'[3, 9]', u'[1, 7]', u'[1, 3]', u'you', u'y^3o^2u^4', u'you', u'y', 3, 0, None, u'VBD', u'["neutral", 0.0]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (58, 6666, u'[3, 9]', u'[1, 7]', u'[1, 3]', u'you', u'y^3o^2u^4', u'you', u'u', 4, 2, None, u'VBD', u'["neutral", 0.0]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (59, 6666, u'[3, 9]', u'[1, 8]', u'[1, 4]', u'\U0001f600', u'\U0001f600^5', u'\U0001f600', u'\U0001f600', 5, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None), (60, 6666, u'[3, 9]', u'[1, 9]', u'[1, 5]', u'\U0001f308', u'\U0001f308^7', u'\U0001f308', u'\U0001f308', 7, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None), (61, 6666, u'[3, 9]', u'[1, 10]', u'[1, 6]', u'\U0001f600', u'\U0001f600^5', u'\U0001f600', u'\U0001f600', 5, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None), (62, 6666, u'[3, 9]', u'[1, 11]', u'[1, 7]', u'\U0001f308', u'\U0001f308^7', u'\U0001f308', u'\U0001f308', 7, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None), (63, 6666, u'[3, 9]', u'[1, 12]', u'[1, 8]', u'\U0001f600', u'\U0001f600^5', u'\U0001f600', u'\U0001f600', 5, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', None, None, None, None, None, None, None, None, None, None), (64, 7777, u'[19]', u'[0, 7]', u'[0, 7]', u'\U0001f62b', u'\U0001f62b^4', u'\U0001f62b', u'\U0001f62b', 4, 0, None, u'EMOIMG', u'["positive", 0.27]', u'realy', u'["RB", null, "reali"]', u'bad', u'["JJ", null, "bad"]', u'surprise', u'["NN", null, "surpris"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u',', u'["symbol", null, ","]', u'but', u'["MD", null, "but"]', u'i', u'["PRP", null, "i"]', u'realy', u'["RB", {"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}, "reali"]', u'liked', u'["VBD", null, "like"]'), (65, 7777, u'[19]', u'[0, 9]', u'[0, 9]', u'but', u'bu^10t', u'but', u'u', 10, 1, None, u'MD', u'["positive", 0.27]', u'surprise', u'["NN", null, "surpris"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u',', u'["symbol", null, ","]', u'i', u'["PRP", null, "i"]', u'realy', u'["RB", {"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}, "reali"]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]'), (66, 7777, u'[19]', u'[0, 12]', u'[0, 11]', u'realy', u'real^3y', u'reali', u'l', 3, 3, u'[0, 11]', u'RB', u'["positive", 0.27]', u'me', u'["PRP", null, "me"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u',', u'["symbol", null, ","]', u'but', u'["MD", null, "but"]', u'i', u'["PRP", null, "i"]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]', u'=)', u'["EMOASC", null, "=)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (67, 7777, u'[19]', u'[0, 13]', u'[0, 11]', u'realy', u're^5al^4y^3', u'reali', u'e', 5, 1, u'[0, 11]', u'RB', u'["positive", 0.27]', u'me', u'["PRP", null, "me"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u',', u'["symbol", null, ","]', u'but', u'["MD", null, "but"]', u'i', u'["PRP", null, "i"]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]', u'=)', u'["EMOASC", null, "=)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (68, 7777, u'[19]', u'[0, 13]', u'[0, 11]', u'realy', u're^5al^4y^3', u'reali', u'l', 4, 3, u'[0, 11]', u'RB', u'["positive", 0.27]', u'me', u'["PRP", null, "me"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u',', u'["symbol", null, ","]', u'but', u'["MD", null, "but"]', u'i', u'["PRP", null, "i"]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]', u'=)', u'["EMOASC", null, "=)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (69, 7777, u'[19]', u'[0, 13]', u'[0, 11]', u'realy', u're^5al^4y^3', u'reali', u'y', 3, 4, u'[0, 11]', u'RB', u'["positive", 0.27]', u'me', u'["PRP", null, "me"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u',', u'["symbol", null, ","]', u'but', u'["MD", null, "but"]', u'i', u'["PRP", null, "i"]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]', u'=)', u'["EMOASC", null, "=)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (70, 7777, u'[19]', u'[0, 17]', u'[0, 15]', u'=)', u'=)^10', u'=)', u')', 10, 1, None, u'EMOASC', u'["positive", 0.27]', u'i', u'["PRP", null, "i"]', u'realy', u'["RB", {"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}, "reali"]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None), (71, 7777, u'[19]', u'[0, 18]', u'[0, 16]', u'\U0001f600', u'\U0001f600^5', u'\U0001f600', u'\U0001f600', 5, 0, None, u'EMOIMG', u'["positive", 0.27]', u'realy', u'["RB", {"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}, "reali"]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]', u'=)', u'["EMOASC", null, "=)"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None), (72, 7777, u'[19]', u'[0, 19]', u'[0, 17]', u'\U0001f308', u'\U0001f308^7', u'\U0001f308', u'\U0001f308', 7, 0, None, u'EMOIMG', u'["positive", 0.27]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]', u'=)', u'["EMOASC", null, "=)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None)]


        right_redus = [(1, 1111, u'[4, 14]', u'[1, 4]', u'[1, 4]', u'very', u'veri', u'{"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}', 3, u'JJ', u'["negative", -0.1875]', u'.', u'["symbol", null, "."]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'pity', u'["JJ", {"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}, "piti"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]'), (2, 1111, u'[4, 14]', u'[1, 7]', u'[1, 5]', u'pity', u'piti', u'{"pity": 2, "pi^3t^3y^3": 1, "pi^9ty": 1}', 4, u'JJ', u'["negative", -0.1875]', u'but', u'["CC", null, "but"]', u'it', u'["PRP", null, "it"]', u'was', u'["VBD", null, "was"]', u'also', u'["RB", null, "also"]', u'very', u'["JJ", {"very": 1, "ver^4y^5": 1, "v^3er^8y": 1}, "veri"]', u'for', u'["IN", null, "for"]', u'me', u'["PRP", null, "me"]', u'.', u'["symbol", null, "."]', u':-(', u'["EMOASC", null, ":-("]', u'@real_trump', u'["mention", null, "@real_trump"]'), (3, 3333, u'[15]', u'[0, 1]', u'[0, 1]', u'bad', u'bad', u'{"bad": 1, "ba^7d": 1, "bad^5": 1, "b^4a^4d^5": 1, "b^7a^6d": 1}', 5, u'JJ', u'["negative", -0.7249999999999999]', None, None, None, None, None, None, None, None, u'a', u'["DT", null, "a"]', u'news', u'["NN", null, "news"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (4, 3333, u'[15]', u'[0, 17]', u'[0, 13]', u'#shetlife', u'#shetlif', u'{"#shetlife": 2}', 2, u'hashtag', u'["negative", -0.7249999999999999]', u'acept', u'["VB", null, "acept"]', u'.', u'["symbol", null, "."]', u'-(', u'["EMOASC", null, "-("]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u':-(', u'["EMOASC", null, ":-("]', u'http://www.noooo.com', u'["URL", null, "http://www.noooo.com"]', None, None, None, None, None, None, None, None), (5, 4444, u'[13]', u'[0, 0]', u'[0, 0]', u'tiny', u'tini', u'{"tiny": 6}', 6, u'JJ', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'model', u'["NN", null, "model"]', u',', u'["symbol", null, ","]', u'which', u'["WDT", null, "which"]', u'we', u'["PRP", null, "we"]', u'can', u'["MD", null, "can"]'), (6, 4444, u'[13]', u'[0, 15]', u'[0, 10]', u'big', u'big', u'{"bi^3g": 1, "bi^15g": 1}', 2, u'NN', u'["neutral", 0.0]', u'can', u'["MD", null, "can"]', u'use', u'["VB", null, "use"]', u'for', u'["IN", null, "for"]', u'explain', u'["VB", null, "explain"]', u'a', u'["DT", null, "a"]', u'things', u'["NNS", null, "thing"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None), (7, 5555, u'[8, 2, 11, 4]', u'[0, 5]', u'[0, 5]', u'big', u'big', u'{"big": 3}', 3, u'JJ', u'["neutral", 0.0]', u'tiny', u'["JJ", null, "tini"]', u'model', u'["NN", null, "model"]', u',', u'["symbol", null, ","]', u'but', u'["CC", null, "but"]', u'a', u'["DT", null, "a"]', u'explanation', u'["NN", null, "explan"]', u'.', u'["symbol", null, "."]', u'right', u'["UH", null, "right"]', u'?', u'["symbol", null, "?"]', u'what', u'["WP", null, "what"]'), (8, 5555, u'[8, 2, 11, 4]', u'[3, 0]', u'[3, 0]', u'but', u'but', u'{"bu^5t^4": 1, "b^5u^4t^4": 1}', 2, u'NNP', u'["neutral", 0.0]', u'?', u'["symbol", null, "?"]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None), (9, 5555, u'[8, 2, 11, 4]', u'[3, 2]', u'[3, 1]', u'you', u'you', u'{"yo^6u": 1, "y^6ou": 1}', 2, u'NN', u'["neutral", 0.0]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'but', u'["FW", {"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}, "but"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None), (10, 5555, u'[8, 2, 11, 4]', u'[3, 4]', u'[3, 2]', u'but', u'but', u'{"b^6ut": 1, "b^5ut^4": 1, "b^5u^5t": 1}', 3, u'FW', u'["neutral", 0.0]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t^4": 1, "b^5u^4t^4": 1}, "but"]', u'you', u'["NN", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["FW", null, "you"]', None, None, None, None, None, None, None, None), (11, 6666, u'[3, 9]', u'[0, 0]', u'[0, 0]', u'tiny', u'tini', u'{"tin^3y^2": 1, "tiny": 2}', 3, u'JJ', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]'), (12, 6666, u'[3, 9]', u'[1, 0]', u'[1, 0]', u'but', u'but', u'{"bu^5t": 1, "b^5ut": 1}', 2, u'NNP', u'["neutral", 0.0]', None, None, None, None, u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]'), (13, 6666, u'[3, 9]', u'[1, 2]', u'[1, 1]', u'you', u'you', u'{"yo^6u": 1, "y^6ou": 1}', 2, u'JJ', u'["neutral", 0.0]', None, None, u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'but', u'["CC", {"b^6ut": 1, "b^5ut": 2}, "but"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]'), (14, 6666, u'[3, 9]', u'[1, 4]', u'[1, 2]', u'but', u'but', u'{"b^6ut": 1, "b^5ut": 2}', 3, u'CC', u'["neutral", 0.0]', u'tiny', u'["JJ", {"tin^3y^2": 1, "tiny": 2}, "tini"]', u'surprise', u'["NN", null, "surpris"]', u'.', u'["symbol", null, "."]', u'but', u'["NNP", {"bu^5t": 1, "b^5ut": 1}, "but"]', u'you', u'["JJ", {"yo^6u": 1, "y^6ou": 1}, "you"]', u'you', u'["VBD", null, "you"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'\U0001f308', u'["EMOIMG", null, "\\ud83c\\udf08"]'), (15, 7777, u'[19]', u'[0, 11]', u'[0, 11]', u'realy', u'reali', u'{"realy": 1, "real^3y": 1, "re^5al^4y^3": 1}', 3, u'RB', u'["positive", 0.27]', u'me', u'["PRP", null, "me"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u',', u'["symbol", null, ","]', u'but', u'["MD", null, "but"]', u'i', u'["PRP", null, "i"]', u'liked', u'["VBD", null, "like"]', u'it', u'["PRP", null, "it"]', u':p', u'["EMOASC", null, ":p"]', u'=)', u'["EMOASC", null, "=)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]')]



        # right_baseline_not_freezed_not_full_repetativ =  [(u'also++very++pity++for++me', u'also++veri++piti++for++me', 5, 1, u'[0, 2, 2, 0, 0]', u'[0, 4, 4, 0, 0]', u'[0, 1, 1, 0, 0]', u'[0, 3, 4, 0, 0]', None, None), (u'it++was++also++very', u'it++was++also++veri', 4, 1, u'[0, 0, 0, 2]', u'[0, 0, 0, 4]', u'[0, 0, 0, 1]', u'[0, 0, 0, 3]', None, None), (u'.++:-(++@real_trump++#shetlife', u'.++:-(++@real_trump++#shetlif', 4, 1, u'[1, 1, 0, 0]', u'[1, 1, 0, 0]', None, None, None, None), (u'.++but++it', u'.++but++it', 3, 1, None, None, None, None, None, None), (u'to', u'to', 1, 1, None, None, None, None, None, None), (u':-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u':-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 5, 1, u'[1, 0, 0, 0, 0]', u'[1, 0, 0, 0, 0]', None, None, None, None), (u'glad++to++se++you++-)', u'glad++to++se++you++-)', 5, 1, u'[1, 0, 1, 0, 1]', u'[1, 0, 1, 0, 1]', None, None, None, None), (u'i++loved++it++.++but', u'i++love++it++.++but', 5, 1, None, None, None, None, None, None), (u'me++.', u'me++.', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'i++loved', u'i++love', 2, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump', u'.++:-(++@real_trump', 3, 1, u'[1, 1, 0]', u'[1, 1, 0]', None, None, None, None), (u'i++loved++it', u'i++love++it', 3, 1, None, None, None, None, None, None), (u'-)', u'-)', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++-)', u'you++-)', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'me++.++:-(', u'me++.++:-(', 3, 1, u'[0, 1, 1]', u'[0, 1, 1]', None, None, None, None), (u'.++:-(++@real_trump++#shetlife++#readytogo', u'.++:-(++@real_trump++#shetlif++#readytogo', 5, 1, u'[1, 1, 0, 0, 0]', u'[1, 1, 0, 0, 0]', None, None, None, None), (u'but++it', u'but++it', 2, 1, None, None, None, None, None, None), (u'pity++for++me++.', u'piti++for++me++.', 4, 1, u'[2, 0, 0, 1]', u'[4, 0, 0, 1]', u'[1, 0, 0, 0]', u'[4, 0, 0, 0]', None, None), (u'for++me++.++:-(', u'for++me++.++:-(', 4, 1, u'[0, 0, 1, 1]', u'[0, 0, 1, 1]', None, None, None, None), (u'me++.++:-(++@real_trump++#shetlife++#readytogo', u'me++.++:-(++@real_trump++#shetlif++#readytogo', 6, 1, u'[0, 1, 1, 0, 0, 0]', u'[0, 1, 1, 0, 0, 0]', None, None, None, None), (u'it++was++also++very++pity', u'it++was++also++veri++piti', 5, 1, u'[0, 0, 0, 2, 2]', u'[0, 0, 0, 4, 4]', u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 3, 4]', None, None), (u'very++pity++for++me++.++:-(', u'veri++piti++for++me++.++:-(', 6, 1, u'[2, 2, 0, 0, 1, 1]', u'[4, 4, 0, 0, 1, 1]', u'[1, 1, 0, 0, 0, 0]', u'[3, 4, 0, 0, 0, 0]', None, None), (u'to++se++you++-)', u'to++se++you++-)', 4, 1, u'[0, 1, 0, 1]', u'[0, 1, 0, 1]', None, None, None, None), (u'http://www.absurd.com', u'http://www.absurd.com', 1, 1, None, None, None, None, None, None), (u'it++was++also++very++pity++for', u'it++was++also++veri++piti++for', 6, 1, u'[0, 0, 0, 2, 2, 0]', u'[0, 0, 0, 4, 4, 0]', u'[0, 0, 0, 1, 1, 0]', u'[0, 0, 0, 3, 4, 0]', None, None), (u'very++pity++for', u'veri++piti++for', 3, 1, u'[2, 2, 0]', u'[4, 4, 0]', u'[1, 1, 0]', u'[3, 4, 0]', None, None), (u'it++.', u'it++.', 2, 1, None, None, None, None, None, None), (u'loved', u'love', 1, 1, None, None, None, None, None, None), (u'@real_trump', u'@real_trump', 1, 1, None, None, None, None, None, None), (u'se++you++-)', u'se++you++-)', 3, 1, u'[1, 0, 1]', u'[1, 0, 1]', None, None, None, None), (u'glad++to', u'glad++to', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'but++it++was++also++very', u'but++it++was++also++veri', 5, 1, u'[0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 4]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 3]', None, None), (u'also', u'also', 1, 1, None, None, None, None, None, None), (u'for++me++.', u'for++me++.', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'loved++it++.++but++it', u'love++it++.++but++it', 5, 1, None, None, None, None, None, None), (u'was++also', u'was++also', 2, 1, None, None, None, None, None, None), (u'it++was++also', u'it++was++also', 3, 1, None, None, None, None, None, None), (u'loved++it', u'love++it', 2, 1, None, None, None, None, None, None), (u'pity++for++me++.++:-(', u'piti++for++me++.++:-(', 5, 1, u'[2, 0, 0, 1, 1]', u'[4, 0, 0, 1, 1]', u'[1, 0, 0, 0, 0]', u'[4, 0, 0, 0, 0]', None, None), (u'loved++it++.++but', u'love++it++.++but', 4, 1, None, None, None, None, None, None), (u'@real_trump++#shetlife++#readytogo++http://www.absurd.com', u'@real_trump++#shetlif++#readytogo++http://www.absurd.com', 4, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u'.++:-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 6, 1, u'[1, 1, 0, 0, 0, 0]', u'[1, 1, 0, 0, 0, 0]', None, None, None, None), (u'pity', u'piti', 1, 4, u'2', u'4', u'1', u'4', u'2', u'1'), (u'me++.++:-(++@real_trump', u'me++.++:-(++@real_trump', 4, 1, u'[0, 1, 1, 0]', u'[0, 1, 1, 0]', None, None, None, None), (u'but++it++was++also++very++pity', u'but++it++was++also++veri++piti', 6, 1, u'[0, 0, 0, 0, 2, 2]', u'[0, 0, 0, 0, 4, 4]', u'[0, 0, 0, 0, 1, 1]', u'[0, 0, 0, 0, 3, 4]', None, None), (u'i++loved++it++.', u'i++love++it++.', 4, 1, None, None, None, None, None, None), (u'very++pity++for++me++.', u'veri++piti++for++me++.', 5, 1, u'[2, 2, 0, 0, 1]', u'[4, 4, 0, 0, 1]', u'[1, 1, 0, 0, 0]', u'[3, 4, 0, 0, 0]', None, None), (u'#readytogo++http://www.absurd.com', u'#readytogo++http://www.absurd.com', 2, 1, None, None, None, None, None, None), (u'#readytogo', u'#readytogo', 1, 1, None, None, None, None, None, None), (u'also++very++pity++for++me++.', u'also++veri++piti++for++me++.', 6, 1, u'[0, 2, 2, 0, 0, 1]', u'[0, 4, 4, 0, 0, 1]', u'[0, 1, 1, 0, 0, 0]', u'[0, 3, 4, 0, 0, 0]', None, None), (u'se++you', u'se++you', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'se', u'se', 1, 1, u'1', u'1', None, None, u'1', None), (u'for++me++.++:-(++@real_trump++#shetlife', u'for++me++.++:-(++@real_trump++#shetlif', 6, 1, u'[0, 0, 1, 1, 0, 0]', u'[0, 0, 1, 1, 0, 0]', None, None, None, None), (u'but++it++was', u'but++it++was', 3, 1, None, None, None, None, None, None), (u'glad++to++se++you', u'glad++to++se++you', 4, 1, u'[1, 0, 1, 0]', u'[1, 0, 1, 0]', None, None, None, None), (u'#shetlife++#readytogo', u'#shetlif++#readytogo', 2, 1, None, None, None, None, None, None), (u'very++pity++for++me', u'veri++piti++for++me', 4, 1, u'[2, 2, 0, 0]', u'[4, 4, 0, 0]', u'[1, 1, 0, 0]', u'[3, 4, 0, 0]', None, None), (u'@real_trump++#shetlife++#readytogo', u'@real_trump++#shetlif++#readytogo', 3, 1, None, None, None, None, None, None), (u'#shetlife++#readytogo++http://www.absurd.com', u'#shetlif++#readytogo++http://www.absurd.com', 3, 1, None, None, None, None, None, None), (u':-(++@real_trump', u':-(++@real_trump', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'pity++for++me++.++:-(++@real_trump', u'piti++for++me++.++:-(++@real_trump', 6, 1, u'[2, 0, 0, 1, 1, 0]', u'[4, 0, 0, 1, 1, 0]', u'[1, 0, 0, 0, 0, 0]', u'[4, 0, 0, 0, 0, 0]', None, None), (u'.++but++it++was++also', u'.++but++it++was++also', 5, 1, None, None, None, None, None, None), (u'it++.++but++it++was', u'it++.++but++it++was', 5, 1, None, None, None, None, None, None), (u'was++also++very++pity++for', u'was++also++veri++piti++for', 5, 1, u'[0, 0, 2, 2, 0]', u'[0, 0, 4, 4, 0]', u'[0, 0, 1, 1, 0]', u'[0, 0, 3, 4, 0]', None, None), (u'also++very', u'also++veri', 2, 1, u'[0, 2]', u'[0, 4]', u'[0, 1]', u'[0, 3]', None, None), (u'to++se', u'to++se', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'pity++for', u'piti++for', 2, 1, u'[2, 0]', u'[4, 0]', u'[1, 0]', u'[4, 0]', None, None), (u'to++se++you', u'to++se++you', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'for++me++.++:-(++@real_trump', u'for++me++.++:-(++@real_trump', 5, 1, u'[0, 0, 1, 1, 0]', u'[0, 0, 1, 1, 0]', None, None, None, None), (u'also++very++pity', u'also++veri++piti', 3, 1, u'[0, 2, 2]', u'[0, 4, 4]', u'[0, 1, 1]', u'[0, 3, 4]', None, None), (u'very', u'veri', 1, 3, u'2', u'4', u'1', u'3', u'2', u'1'), (u'it++.++but++it++was++also', u'it++.++but++it++was++also', 6, 1, None, None, None, None, None, None), (u'was++also++very', u'was++also++veri', 3, 1, u'[0, 0, 2]', u'[0, 0, 4]', u'[0, 0, 1]', u'[0, 0, 3]', None, None), (u'loved++it++.++but++it++was', u'love++it++.++but++it++was', 6, 1, None, None, None, None, None, None), (u'pity++for++me', u'piti++for++me', 3, 1, u'[2, 0, 0]', u'[4, 0, 0]', u'[1, 0, 0]', u'[4, 0, 0]', None, None), (u'me++.++:-(++@real_trump++#shetlife', u'me++.++:-(++@real_trump++#shetlif', 5, 1, u'[0, 1, 1, 0, 0]', u'[0, 1, 1, 0, 0]', None, None, None, None), (u'very++pity', u'veri++piti', 2, 1, u'[2, 2]', u'[4, 4]', u'[1, 1]', u'[3, 4]', None, None), (u'was++also++very++pity++for++me', u'was++also++veri++piti++for++me', 6, 1, u'[0, 0, 2, 2, 0, 0]', u'[0, 0, 4, 4, 0, 0]', u'[0, 0, 1, 1, 0, 0]', u'[0, 0, 3, 4, 0, 0]', None, None), (u'also++very++pity++for', u'also++veri++piti++for', 4, 1, u'[0, 2, 2, 0]', u'[0, 4, 4, 0]', u'[0, 1, 1, 0]', u'[0, 3, 4, 0]', None, None), (u'but++it++was++also', u'but++it++was++also', 4, 1, None, None, None, None, None, None), (u'@real_trump++#shetlife', u'@real_trump++#shetlif', 2, 1, None, None, None, None, None, None), (u'it++.++but++it', u'it++.++but++it', 4, 1, None, None, None, None, None, None), (u'.++but++it++was', u'.++but++it++was', 4, 1, None, None, None, None, None, None), (u':-(++@real_trump++#shetlife', u':-(++@real_trump++#shetlif', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', None, None, None, None), (u'glad++to++se', u'glad++to++se', 3, 1, u'[1, 0, 1]', u'[1, 0, 1]', None, None, None, None), (u':-(++@real_trump++#shetlife++#readytogo', u':-(++@real_trump++#shetlif++#readytogo', 4, 1, u'[1, 0, 0, 0]', u'[1, 0, 0, 0]', None, None, None, None), (u'.++:-(', u'.++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'loved++it++.', u'love++it++.', 3, 1, None, None, None, None, None, None), (u'glad', u'glad', 1, 1, u'1', u'1', None, None, u'1', None), (u'.++but++it++was++also++very', u'.++but++it++was++also++veri', 6, 1, u'[0, 0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 0, 4]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 3]', None, None), (u'was++also++very++pity', u'was++also++veri++piti', 4, 1, u'[0, 0, 2, 2]', u'[0, 0, 4, 4]', u'[0, 0, 1, 1]', u'[0, 0, 3, 4]', None, None), (u'i++loved++it++.++but++it', u'i++love++it++.++but++it', 6, 1, None, None, None, None, None, None), (u'it++.++but', u'it++.++but', 3, 1, None, None, None, None, None, None), (u',++which', u',++which', 2, 2, None, None, None, None, None, None), (u'bad++news++,++which', u'bad++news++,++which', 4, 1, u'[4, 0, 0, 0]', u'[7, 0, 0, 0]', u'[1, 0, 0, 0]', u'[5, 0, 0, 0]', None, None), (u',++which++we++can++not', u',++which++we++can++not', 5, 1, None, None, None, None, None, None), (u'tiny++model++,++which++we', u'tini++model++,++which++we', 5, 1, u'[0, 1, 0, 0, 0]', u'[0, 2, 0, 0, 0]', u'[1, 0, 0, 0, 0]', u'[6, 0, 0, 0, 0]', None, None), (u'acept++.++-(', u'acept++.++-(', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u',++which++we++can', u',++which++we++can', 4, 2, None, None, None, None, None, None), (u'acept++.', u'acept++.', 2, 1, None, None, None, None, None, None), (u',++which++we', u',++which++we', 3, 2, None, None, None, None, None, None), (u'not++acept++.++-(++\U0001f62b', u'not++acept++.++-(++\U0001f62b', 5, 1, u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 1, 1]', None, None, None, None), (u'tiny++model++,++which', u'tini++model++,++which', 4, 1, u'[0, 1, 0, 0]', u'[0, 2, 0, 0]', u'[1, 0, 0, 0]', u'[6, 0, 0, 0]', None, None), (u'a++bad++news++,', u'a++bad++news++,', 4, 1, u'[0, 4, 0, 0]', u'[0, 7, 0, 0]', u'[0, 1, 0, 0]', u'[0, 5, 0, 0]', None, None), (u'can++not++acept++.', u'can++not++acept++.', 4, 1, None, None, None, None, None, None), (u'-(++\U0001f62b', u'-(++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'which++we++can', u'which++we++can', 3, 2, None, None, None, None, None, None), (u'-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 5, 1, u'[1, 1, 1, 0, 0]', u'[1, 1, 1, 0, 0]', u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 2, 0]', None, None), (u'explain++a++big', u'explain++a++big', 3, 1, u'[0, 0, 2]', u'[0, 0, 2]', u'[0, 0, 1]', u'[0, 0, 2]', None, None), (u'we++can', u'we++can', 2, 2, None, None, None, None, None, None), (u'can++use', u'can++use', 2, 1, None, None, None, None, None, None), (u'we++can++use++for++explain', u'we++can++use++for++explain', 5, 1, None, None, None, None, None, None), (u',++which++we++can++use++for', u',++which++we++can++use++for', 6, 1, None, None, None, None, None, None), (u'use++for++explain', u'use++for++explain', 3, 1, None, None, None, None, None, None), (u'explain++a++big++things++.', u'explain++a++big++thing++.', 5, 1, u'[0, 0, 2, 0, 0]', u'[0, 0, 2, 0, 0]', u'[0, 0, 1, 0, 0]', u'[0, 0, 2, 0, 0]', None, None), (u'a++bad++news', u'a++bad++news', 3, 1, u'[0, 4, 0]', u'[0, 7, 0]', u'[0, 1, 0]', u'[0, 5, 0]', None, None), (u'bad++news++,++which++we', u'bad++news++,++which++we', 5, 1, u'[4, 0, 0, 0, 0]', u'[7, 0, 0, 0, 0]', u'[1, 0, 0, 0, 0]', u'[5, 0, 0, 0, 0]', None, None), (u'for++explain', u'for++explain', 2, 1, None, None, None, None, None, None), (u'can++use++for++explain++a', u'can++use++for++explain++a', 5, 1, None, None, None, None, None, None), (u'we++can++not', u'we++can++not', 3, 1, None, None, None, None, None, None), (u'explain', u'explain', 1, 1, None, None, None, None, None, None), (u'-(', u'-(', 1, 1, u'1', u'1', None, None, u'1', None), (u'bad++news++,++which++we++can', u'bad++news++,++which++we++can', 6, 1, u'[4, 0, 0, 0, 0, 0]', u'[7, 0, 0, 0, 0, 0]', u'[1, 0, 0, 0, 0, 0]', u'[5, 0, 0, 0, 0, 0]', None, None), (u'bad++news', u'bad++news', 2, 1, u'[4, 0]', u'[7, 0]', u'[1, 0]', u'[5, 0]', None, None), (u'news++,++which++we++can', u'news++,++which++we++can', 5, 1, None, None, None, None, None, None), (u'news++,++which++we', u'news++,++which++we', 4, 1, None, None, None, None, None, None), (u'a++bad++news++,++which', u'a++bad++news++,++which', 5, 1, u'[0, 4, 0, 0, 0]', u'[0, 7, 0, 0, 0]', u'[0, 1, 0, 0, 0]', u'[0, 5, 0, 0, 0]', None, None), (u'big++things++.', u'big++thing++.', 3, 1, u'[2, 0, 0]', u'[2, 0, 0]', u'[1, 0, 0]', u'[2, 0, 0]', None, None), (u'things++.', u'thing++.', 2, 1, None, None, None, None, None, None), (u'things', u'thing', 1, 1, None, None, None, None, None, None), (u'-(++\U0001f62b++:-(', u'-(++\U0001f62b++:-(', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, None, None), (u'model++,++which++we', u'model++,++which++we', 4, 1, u'[1, 0, 0, 0]', u'[2, 0, 0, 0]', None, None, None, None), (u'#shetlife', u'#shetlif', 1, 3, None, None, u'1', u'2', None, u'1'), (u'can++not++acept++.++-(++\U0001f62b', u'can++not++acept++.++-(++\U0001f62b', 6, 1, u'[0, 0, 0, 0, 1, 1]', u'[0, 0, 0, 0, 1, 1]', None, None, None, None), (u'we++can++not++acept++.', u'we++can++not++acept++.', 5, 1, None, None, None, None, None, None), (u'big++things', u'big++thing', 2, 1, u'[2, 0]', u'[2, 0]', u'[1, 0]', u'[2, 0]', None, None), (u'use++for++explain++a', u'use++for++explain++a', 4, 1, None, None, None, None, None, None), (u'not++acept', u'not++acept', 2, 1, None, None, None, None, None, None), (u'acept++.++-(++\U0001f62b++:-(', u'acept++.++-(++\U0001f62b++:-(', 5, 1, u'[0, 0, 1, 1, 1]', u'[0, 0, 1, 1, 1]', None, None, None, None), (u'for++explain++a++big++things++.', u'for++explain++a++big++thing++.', 6, 1, u'[0, 0, 0, 2, 0, 0]', u'[0, 0, 0, 2, 0, 0]', u'[0, 0, 0, 1, 0, 0]', u'[0, 0, 0, 2, 0, 0]', None, None), (u'\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'\U0001f62b++:-(++#shetlif++http://www.noooo.com', 4, 1, u'[1, 1, 0, 0]', u'[1, 1, 0, 0]', u'[0, 0, 1, 0]', u'[0, 0, 2, 0]', None, None), (u'we++can++use', u'we++can++use', 3, 1, None, None, None, None, None, None), (u'which++we++can++use++for++explain', u'which++we++can++use++for++explain', 6, 1, None, None, None, None, None, None), (u'not++acept++.++-(', u'not++acept++.++-(', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u':-(++#shetlife', u':-(++#shetlif', 2, 1, u'[1, 0]', u'[1, 0]', u'[0, 1]', u'[0, 2]', None, None), (u'which++we++can++use', u'which++we++can++use', 4, 1, None, None, None, None, None, None), (u'explain++a', u'explain++a', 2, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'.++-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 6, 1, u'[0, 1, 1, 1, 0, 0]', u'[0, 1, 1, 1, 0, 0]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 2, 0]', None, None), (u'not++acept++.', u'not++acept++.', 3, 1, None, None, None, None, None, None), (u'a++big++things', u'a++big++thing', 3, 1, u'[0, 2, 0]', u'[0, 2, 0]', u'[0, 1, 0]', u'[0, 2, 0]', None, None), (u'.++-(', u'.++-(', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'a++bad', u'a++bad', 2, 1, u'[0, 4]', u'[0, 7]', u'[0, 1]', u'[0, 5]', None, None), (u'use++for', u'use++for', 2, 1, None, None, None, None, None, None), (u'can++not++acept++.++-(', u'can++not++acept++.++-(', 5, 1, u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 1]', None, None, None, None), (u'a++big++things++.', u'a++big++thing++.', 4, 1, u'[0, 2, 0, 0]', u'[0, 2, 0, 0]', u'[0, 1, 0, 0]', u'[0, 2, 0, 0]', None, None), (u'news', u'news', 1, 1, None, None, None, None, None, None), (u'which++we++can++not', u'which++we++can++not', 4, 1, None, None, None, None, None, None), (u'http://www.noooo.com', u'http://www.noooo.com', 1, 1, None, None, None, None, None, None), (u'-(++\U0001f62b++:-(++#shetlife', u'-(++\U0001f62b++:-(++#shetlif', 4, 1, u'[1, 1, 1, 0]', u'[1, 1, 1, 0]', u'[0, 0, 0, 1]', u'[0, 0, 0, 2]', None, None), (u'acept++.++-(++\U0001f62b', u'acept++.++-(++\U0001f62b', 4, 1, u'[0, 0, 1, 1]', u'[0, 0, 1, 1]', None, None, None, None), (u'which++we++can++not++acept', u'which++we++can++not++acept', 5, 1, None, None, None, None, None, None), (u':-(', u':-(', 1, 2, u'2', u'2', None, None, u'2', None), (u'news++,++which++we++can++not', u'news++,++which++we++can++not', 6, 1, None, None, None, None, None, None), (u'can++use++for++explain', u'can++use++for++explain', 4, 1, None, None, None, None, None, None), (u':-(++#shetlife++http://www.noooo.com', u':-(++#shetlif++http://www.noooo.com', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', u'[0, 1, 0]', u'[0, 2, 0]', None, None), (u'not', u'not', 1, 1, None, None, None, None, None, None), (u',++which++we++can++not++acept', u',++which++we++can++not++acept', 6, 1, None, None, None, None, None, None), (u'which++we++can++use++for', u'which++we++can++use++for', 5, 1, None, None, None, None, None, None), (u'can++not++acept', u'can++not++acept', 3, 1, None, None, None, None, None, None), (u'explain++a++big++things', u'explain++a++big++thing', 4, 1, u'[0, 0, 2, 0]', u'[0, 0, 2, 0]', u'[0, 0, 1, 0]', u'[0, 0, 2, 0]', None, None), (u'can', u'can', 1, 2, None, None, None, None, None, None), (u'tiny++model++,++which++we++can', u'tini++model++,++which++we++can', 6, 1, u'[0, 1, 0, 0, 0, 0]', u'[0, 2, 0, 0, 0, 0]', u'[1, 0, 0, 0, 0, 0]', u'[6, 0, 0, 0, 0, 0]', None, None), (u'acept++.++-(++\U0001f62b++:-(++#shetlife', u'acept++.++-(++\U0001f62b++:-(++#shetlif', 6, 1, u'[0, 0, 1, 1, 1, 0]', u'[0, 0, 1, 1, 1, 0]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 2]', None, None), (u'use++for++explain++a++big++things', u'use++for++explain++a++big++thing', 6, 1, u'[0, 0, 0, 0, 2, 0]', u'[0, 0, 0, 0, 2, 0]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 2, 0]', None, None), (u'we++can++use++for++explain++a', u'we++can++use++for++explain++a', 6, 1, None, None, None, None, None, None), (u'use++for++explain++a++big', u'use++for++explain++a++big', 5, 1, u'[0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 2]', None, None), (u'model++,++which++we++can++use', u'model++,++which++we++can++use', 6, 1, u'[1, 0, 0, 0, 0, 0]', u'[2, 0, 0, 0, 0, 0]', None, None, None, None), (u'which++we', u'which++we', 2, 2, None, None, None, None, None, None), (u'not++acept++.++-(++\U0001f62b++:-(', u'not++acept++.++-(++\U0001f62b++:-(', 6, 1, u'[0, 0, 0, 1, 1, 1]', u'[0, 0, 0, 1, 1, 1]', None, None, None, None), (u'model++,++which++we++can', u'model++,++which++we++can', 5, 1, u'[1, 0, 0, 0, 0]', u'[2, 0, 0, 0, 0]', None, None, None, None), (u'we++can++not++acept', u'we++can++not++acept', 4, 1, None, None, None, None, None, None), (u'use', u'use', 1, 1, None, None, None, None, None, None), (u',++which++we++can++use', u',++which++we++can++use', 5, 1, None, None, None, None, None, None), (u'bad++news++,', u'bad++news++,', 3, 1, u'[4, 0, 0]', u'[7, 0, 0]', u'[1, 0, 0]', u'[5, 0, 0]', None, None), (u'can++use++for', u'can++use++for', 3, 1, None, None, None, None, None, None), (u'news++,', u'news++,', 2, 1, None, None, None, None, None, None), (u'can++not', u'can++not', 2, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(', u'.++-(++\U0001f62b++:-(', 4, 1, u'[0, 1, 1, 1]', u'[0, 1, 1, 1]', None, None, None, None), (u'we', u'we', 1, 2, None, None, None, None, None, None), (u'for++explain++a', u'for++explain++a', 3, 1, None, None, None, None, None, None), (u'acept', u'acept', 1, 1, None, None, None, None, None, None), (u'for++explain++a++big', u'for++explain++a++big', 4, 1, u'[0, 0, 0, 2]', u'[0, 0, 0, 2]', u'[0, 0, 0, 1]', u'[0, 0, 0, 2]', None, None), (u'a++bad++news++,++which++we', u'a++bad++news++,++which++we', 6, 1, u'[0, 4, 0, 0, 0, 0]', u'[0, 7, 0, 0, 0, 0]', u'[0, 1, 0, 0, 0, 0]', u'[0, 5, 0, 0, 0, 0]', None, None), (u'#shetlife++http://www.noooo.com', u'#shetlif++http://www.noooo.com', 2, 1, None, None, u'[1, 0]', u'[2, 0]', None, None), (u'\U0001f62b++:-(', u'\U0001f62b++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'.++-(++\U0001f62b', u'.++-(++\U0001f62b', 3, 1, u'[0, 1, 1]', u'[0, 1, 1]', None, None, None, None), (u'we++can++not++acept++.++-(', u'we++can++not++acept++.++-(', 6, 1, u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 1]', None, None, None, None), (u'news++,++which', u'news++,++which', 3, 1, None, None, None, None, None, None), (u'which', u'which', 1, 2, None, None, None, None, None, None), (u'model++,++which', u'model++,++which', 3, 1, u'[1, 0, 0]', u'[2, 0, 0]', None, None, None, None), (u'we++can++use++for', u'we++can++use++for', 4, 1, None, None, None, None, None, None), (u'which++we++can++not++acept++.', u'which++we++can++not++acept++.', 6, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(++#shetlife', u'.++-(++\U0001f62b++:-(++#shetlif', 5, 1, u'[0, 1, 1, 1, 0]', u'[0, 1, 1, 1, 0]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 2]', None, None), (u'can++use++for++explain++a++big', u'can++use++for++explain++a++big', 6, 1, u'[0, 0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 2]', None, None), (u'\U0001f62b++:-(++#shetlife', u'\U0001f62b++:-(++#shetlif', 3, 1, u'[1, 1, 0]', u'[1, 1, 0]', u'[0, 0, 1]', u'[0, 0, 2]', None, None), (u'for++explain++a++big++things', u'for++explain++a++big++thing', 5, 1, u'[0, 0, 0, 2, 0]', u'[0, 0, 0, 2, 0]', u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 2, 0]', None, None), (u'model', u'model', 1, 2, u'1', u'2', None, None, u'1', None), (u'but++a++big++explanation++.++right', u'but++a++big++explan++.++right', 6, 1, u'[0, 0, 0, 1, 0, 1]', u'[0, 0, 0, 1, 0, 1]', u'[0, 0, 1, 0, 0, 0]', u'[0, 0, 3, 0, 0, 0]', None, None), (u'what', u'what', 1, 1, None, None, None, None, None, None), (u'do++you++think++about', u'do++you++think++about', 4, 1, u'[0, 1, 0, 0]', u'[0, 1, 0, 0]', None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[2, 2, 1, "IGNOR"]', None, None, None, None), (u'it++?++1++\U0001f62b', u'it++?++1++\U0001f62b', 4, 1, u'[0, 1, 1, 1]', u'[0, 1, 1, 1]', None, None, None, None), (u'a++big', u'a++big', 2, 2, u'[0, 2]', u'[0, 2]', u'[0, 2]', u'[0, 5]', None, None), (u'1++\U0001f62b++1++.', u'1++\U0001f62b++1++.', 4, 1, u'[2, 1, "IGNOR", 0]', u'[2, 1, "IGNOR", 0]', None, None, None, None), (u'you++think', u'you++think', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u',++but++a++big++explanation++.', u',++but++a++big++explan++.', 6, 1, u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 1, 0, 0]', u'[0, 0, 0, 3, 0, 0]', None, None), (u'what++do++you++think++about++it', u'what++do++you++think++about++it', 6, 1, u'[0, 0, 1, 0, 0, 0]', u'[0, 0, 1, 0, 0, 0]', None, None, None, None), (u'think++about++it++?++1++\U0001f62b', u'think++about++it++?++1++\U0001f62b', 6, 1, u'[0, 0, 0, 1, 1, 1]', u'[0, 0, 0, 1, 1, 1]', None, None, None, None), (u'but++you', u'but++you', 2, 4, u'[10, 6]', u'[15, 8]', u'[4, 2]', u'[10, 4]', None, None), (u'but++you++\U0001f600++\U0001f308++\U0001f600', u'but++you++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 1, 2, 1, "IGNOR"]', u'[3, 2, 2, 1, "IGNOR"]', u'[1, 0, 0, 0, "IGNOR"]', u'[3, 0, 0, 0, "IGNOR"]', None, None), (u'.++but', u'.++but', 2, 3, u'[0, 4]', u'[0, 7]', u'[0, 2]', u'[0, 4]', None, None), (u'big++explanation++.++right++?++what', u'big++explan++.++right++?++what', 6, 1, u'[0, 1, 0, 1, 0, 0]', u'[0, 1, 0, 1, 0, 0]', u'[1, 0, 0, 0, 0, 0]', u'[3, 0, 0, 0, 0, 0]', None, None), (u'tiny++surprise++.++but', u'tini++surpris++.++but', 4, 1, u'[1, 0, 0, 2]', u'[1, 0, 0, 2]', u'[1, 0, 0, 1]', u'[3, 0, 0, 2]', None, None), (u'about++it++?++1++\U0001f62b++1', u'about++it++?++1++\U0001f62b++1', 6, 1, u'[0, 0, 1, 2, 1, "IGNOR"]', u'[0, 0, 1, 2, 1, "IGNOR"]', None, None, None, None), (u'you++think++about++it++?', u'you++think++about++it++?', 5, 1, u'[1, 0, 0, 0, 1]', u'[1, 0, 0, 0, 1]', None, None, None, None), (u'?++what++do', u'?++what++do', 3, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, None, None), (u'what++do++you', u'what++do++you', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'but++a++big++explanation++.', u'but++a++big++explan++.', 5, 1, u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 1, 0]', u'[0, 0, 1, 0, 0]', u'[0, 0, 3, 0, 0]', None, None), (u',++but++a', u',++but++a', 3, 1, None, None, None, None, None, None), (u'1', u'1', 1, 2, u'2', u'2', None, None, u'2', None), (u'model++,', u'model++,', 2, 2, u'[1, 0]', u'[2, 0]', None, None, None, None), (u'?++what++do++you++think++about', u'?++what++do++you++think++about', 6, 1, u'[0, 0, 0, 1, 0, 0]', u'[0, 0, 0, 1, 0, 0]', None, None, None, None), (u'what++do++you++think', u'what++do++you++think', 4, 1, u'[0, 0, 1, 0]', u'[0, 0, 1, 0]', None, None, None, None), (u'right++?++what++do', u'right++?++what++do', 4, 1, u'[1, 0, 0, 0]', u'[1, 0, 0, 0]', None, None, None, None), (u'what++do', u'what++do', 2, 1, None, None, None, None, None, None), (u'.++right++?++what', u'.++right++?++what', 4, 1, u'[0, 1, 0, 0]', u'[0, 1, 0, 0]', None, None, None, None), (u'.++but++you', u'.++but++you', 3, 2, u'[0, 4, 4]', u'[0, 7, 4]', u'[0, 2, 2]', u'[0, 4, 4]', None, None), (u'about++it++?++1', u'about++it++?++1', 4, 1, u'[0, 0, 1, 1]', u'[0, 0, 1, 1]', None, None, None, None), (u'tiny', u'tini', 1, 10, u'1', u'1', u'2', u'9', u'1', u'2'), (u'tiny++model', u'tini++model', 2, 2, u'[0, 1]', u'[0, 2]', u'[1, 0]', u'[6, 0]', None, None), (u'think++about', u'think++about', 2, 1, None, None, None, None, None, None), (u'surprise++.++but++you', u'surpris++.++but++you', 4, 1, u'[0, 0, 2, 2]', u'[0, 0, 2, 2]', u'[0, 0, 1, 1]', u'[0, 0, 2, 2]', None, None), (u'explanation++.++right++?++what', u'explan++.++right++?++what', 5, 1, u'[1, 0, 1, 0, 0]', u'[1, 0, 1, 0, 0]', None, None, None, None), (u'1++.++but++you++but', u'1++.++but++you++but', 5, 1, u'[1, 0, 5, 2, "IGNOR"]', u'[1, 0, 10, 2, "IGNOR"]', u'[0, 0, 2, 1, "IGNOR"]', u'[0, 0, 5, 2, "IGNOR"]', None, None), (u'model++,++but++a++big++explanation', u'model++,++but++a++big++explan', 6, 1, u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 3, 0]', None, None), (u'?++1++\U0001f62b++1++.++but', u'?++1++\U0001f62b++1++.++but', 6, 1, u'[1, 2, 1, "IGNOR", 0, 2]', u'[1, 2, 1, "IGNOR", 0, 5]', u'[0, 0, 0, "IGNOR", 0, 1]', u'[0, 0, 0, "IGNOR", 0, 2]', None, None), (u'a++big++explanation', u'a++big++explan', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', u'[0, 1, 0]', u'[0, 3, 0]', None, None), (u'explanation++.++right++?++what++do', u'explan++.++right++?++what++do', 6, 1, u'[1, 0, 1, 0, 0, 0]', u'[1, 0, 1, 0, 0, 0]', None, None, None, None), (u'?++what', u'?++what', 2, 1, None, None, None, None, None, None), (u'right', u'right', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++but++you', u'you++but++you', 3, 2, u'[6, 6, "IGNOR"]', u'[8, 8, "IGNOR"]', u'[2, 2, "IGNOR"]', u'[4, 6, "IGNOR"]', None, None), (u'big++explanation++.++right++?', u'big++explan++.++right++?', 5, 1, u'[0, 1, 0, 1, 0]', u'[0, 1, 0, 1, 0]', u'[1, 0, 0, 0, 0]', u'[3, 0, 0, 0, 0]', None, None), (u'it++?', u'it++?', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'what++do++you++think++about', u'what++do++you++think++about', 5, 1, u'[0, 0, 1, 0, 0]', u'[0, 0, 1, 0, 0]', None, None, None, None), (u'but++you++but++you++\U0001f600++\U0001f308', u'but++you++but++you++\U0001f600++\U0001f308', 6, 1, u'[5, 3, "IGNOR", "IGNOR", 1, 1]', u'[5, 4, "IGNOR", "IGNOR", 1, 1]', u'[2, 1, "IGNOR", "IGNOR", 0, 0]', u'[5, 2, "IGNOR", "IGNOR", 0, 0]', None, None), (u'\U0001f308++\U0001f600++\U0001f308', u'\U0001f308++\U0001f600++\U0001f308', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, None, None), (u'explanation++.++right', u'explan++.++right', 3, 1, u'[1, 0, 1]', u'[1, 0, 1]', None, None, None, None), (u'.', u'.', 1, 7, u'1', u'1', None, None, u'1', None), (u'you', u'you', 1, 8, u'7', u'9', u'2', u'4', u'7', u'2'), (u'surprise++.++but', u'surpris++.++but', 3, 1, u'[0, 0, 2]', u'[0, 0, 2]', u'[0, 0, 1]', u'[0, 0, 2]', None, None), (u'?', u'?', 1, 2, u'1', u'1', None, None, u'1', None), (u'explanation++.++right++?', u'explan++.++right++?', 4, 1, u'[1, 0, 1, 0]', u'[1, 0, 1, 0]', None, None, None, None), (u'it++?++1', u'it++?++1', 3, 1, u'[0, 1, 1]', u'[0, 1, 1]', None, None, None, None), (u'tiny++model++,++but', u'tini++model++,++but', 4, 1, None, None, None, None, None, None), (u'you++think++about++it++?++1', u'you++think++about++it++?++1', 6, 1, u'[1, 0, 0, 0, 1, 1]', u'[1, 0, 0, 0, 1, 1]', None, None, None, None), (u'but++you++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308', 4, 1, u'[3, 1, 1, 1]', u'[3, 2, 1, 1]', u'[1, 0, 0, 0]', u'[3, 0, 0, 0]', None, None), (u'but++a++big', u'but++a++big', 3, 1, None, None, u'[0, 0, 1]', u'[0, 0, 3]', None, None), (u'tiny++surprise++.++but++you++but', u'tini++surpris++.++but++you++but', 6, 1, u'[1, 0, 0, 5, 2, "IGNOR"]', u'[1, 0, 0, 5, 2, "IGNOR"]', u'[1, 0, 0, 2, 1, "IGNOR"]', u'[3, 0, 0, 5, 2, "IGNOR"]', None, None), (u'do++you++think++about++it', u'do++you++think++about++it', 5, 1, u'[0, 1, 0, 0, 0]', u'[0, 1, 0, 0, 0]', None, None, None, None), (u'big++explanation++.', u'big++explan++.', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', u'[1, 0, 0]', u'[3, 0, 0]', None, None), (u'think++about++it++?++1', u'think++about++it++?++1', 5, 1, u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 1, 1]', None, None, None, None), (u'.++right', u'.++right', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'explanation++.', u'explan++.', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'but++you++but', u'but++you++but', 3, 2, u'[10, 4, "IGNOR"]', u'[15, 4, "IGNOR"]', u'[4, 2, "IGNOR"]', u'[10, 4, "IGNOR"]', None, None), (u'.++but++you++but++you++\U0001f600', u'.++but++you++but++you++\U0001f600', 6, 1, u'[0, 5, 3, "IGNOR", "IGNOR", 1]', u'[0, 5, 4, "IGNOR", "IGNOR", 1]', u'[0, 2, 1, "IGNOR", "IGNOR", 0]', u'[0, 5, 2, "IGNOR", "IGNOR", 0]', None, None), (u'tiny++surprise', u'tini++surpris', 2, 1, u'[1, 0]', u'[1, 0]', u'[1, 0]', u'[3, 0]', None, None), (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, None, None), (u'model++,++but++a', u'model++,++but++a', 4, 1, None, None, None, None, None, None), (u'you++think++about', u'you++think++about', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', None, None, None, None), (u'?++what++do++you', u'?++what++do++you', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u'explanation', u'explan', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++but++you++\U0001f600++\U0001f308++\U0001f600', u'you++but++you++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[3, 3, "IGNOR", 2, 1, "IGNOR"]', u'[4, 3, "IGNOR", 2, 1, "IGNOR"]', u'[1, 1, "IGNOR", 0, 0, "IGNOR"]', u'[2, 3, "IGNOR", 0, 0, "IGNOR"]', None, None), (u'?++1', u'?++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'do++you++think++about++it++?', u'do++you++think++about++it++?', 6, 1, u'[0, 1, 0, 0, 0, 1]', u'[0, 1, 0, 0, 0, 1]', None, None, None, None), (u'do++you++think', u'do++you++think', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'model++,++but', u'model++,++but', 3, 1, None, None, None, None, None, None), (u'tiny++model++,++but++a', u'tini++model++,++but++a', 5, 1, None, None, None, None, None, None), (u'.++but++you++but++you', u'.++but++you++but++you', 5, 2, u'[0, 10, 6, "IGNOR", "IGNOR"]', u'[0, 15, 8, "IGNOR", "IGNOR"]', u'[0, 4, 2, "IGNOR", "IGNOR"]', u'[0, 10, 4, "IGNOR", "IGNOR"]', None, None), (u'\U0001f62b++1++.++but', u'\U0001f62b++1++.++but', 4, 1, u'[1, 1, 0, 2]', u'[1, 1, 0, 5]', u'[0, 0, 0, 1]', u'[0, 0, 0, 2]', None, None), (u'right++?', u'right++?', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'but++you++\U0001f600', u'but++you++\U0001f600', 3, 1, u'[3, 1, 1]', u'[3, 2, 1]', u'[1, 0, 0]', u'[3, 0, 0]', None, None), (u'model++,++but++a++big', u'model++,++but++a++big', 5, 1, None, None, u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 3]', None, None), (u'\U0001f62b++1++.++but++you++but', u'\U0001f62b++1++.++but++you++but', 6, 1, u'[1, 1, 0, 5, 2, "IGNOR"]', u'[1, 1, 0, 10, 2, "IGNOR"]', u'[0, 0, 0, 2, 1, "IGNOR"]', u'[0, 0, 0, 5, 2, "IGNOR"]', None, None), (u'tiny++surprise++.', u'tini++surpris++.', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', u'[1, 0, 0]', u'[3, 0, 0]', None, None), (u'?++what++do++you++think', u'?++what++do++you++think', 5, 1, u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 1, 0]', None, None, None, None), (u'.++but++you++but', u'.++but++you++but', 4, 2, u'[0, 10, 4, "IGNOR"]', u'[0, 15, 4, "IGNOR"]', u'[0, 4, 2, "IGNOR"]', u'[0, 10, 4, "IGNOR"]', None, None), (u',++but++a++big++explanation', u',++but++a++big++explan', 5, 1, u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 3, 0]', None, None), (u'\U0001f62b++1++.', u'\U0001f62b++1++.', 3, 1, u'[1, 1, 0]', u'[1, 1, 0]', None, None, None, None), (u'about', u'about', 1, 1, None, None, None, None, None, None), (u'it++?++1++\U0001f62b++1', u'it++?++1++\U0001f62b++1', 5, 1, u'[0, 1, 2, 1, "IGNOR"]', u'[0, 1, 2, 1, "IGNOR"]', None, None, None, None), (u'tiny++model++,++but++a++big', u'tini++model++,++but++a++big', 6, 1, None, None, u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 3]', None, None), (u'you++but', u'you++but', 2, 2, u'[4, 6]', u'[4, 8]', u'[2, 2]', u'[4, 6]', None, None), (u'right++?++what', u'right++?++what', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', None, None, None, None), (u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, None, None), (u'but++you++but++you++\U0001f600', u'but++you++but++you++\U0001f600', 5, 1, u'[5, 3, "IGNOR", "IGNOR", 1]', u'[5, 4, "IGNOR", "IGNOR", 1]', u'[2, 1, "IGNOR", "IGNOR", 0]', u'[5, 2, "IGNOR", "IGNOR", 0]', None, None), (u'\U0001f62b++1++.++but++you', u'\U0001f62b++1++.++but++you', 5, 1, u'[1, 1, 0, 2, 2]', u'[1, 1, 0, 5, 2]', u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 2, 2]', None, None), (u'surprise++.++but++you++but++you', u'surpris++.++but++you++but++you', 6, 1, u'[0, 0, 5, 3, "IGNOR", "IGNOR"]', u'[0, 0, 5, 4, "IGNOR", "IGNOR"]', u'[0, 0, 2, 1, "IGNOR", "IGNOR"]', u'[0, 0, 5, 2, "IGNOR", "IGNOR"]', None, None), (u'a++big++explanation++.++right', u'a++big++explan++.++right', 5, 1, u'[0, 0, 1, 0, 1]', u'[0, 0, 1, 0, 1]', u'[0, 1, 0, 0, 0]', u'[0, 3, 0, 0, 0]', None, None), (u'1++.++but', u'1++.++but', 3, 1, u'[1, 0, 2]', u'[1, 0, 5]', u'[0, 0, 1]', u'[0, 0, 2]', None, None), (u'you++but++you++\U0001f600++\U0001f308', u'you++but++you++\U0001f600++\U0001f308', 5, 1, u'[3, 3, "IGNOR", 1, 1]', u'[4, 3, "IGNOR", 1, 1]', u'[1, 1, "IGNOR", 0, 0]', u'[2, 3, "IGNOR", 0, 0]', None, None), (u'\U0001f62b++1', u'\U0001f62b++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'surprise++.', u'surpris++.', 2, 1, None, None, None, None, None, None), (u'tiny++model++,', u'tini++model++,', 3, 2, u'[0, 1, 0]', u'[0, 2, 0]', u'[1, 0, 0]', u'[6, 0, 0]', None, None), (u'right++?++what++do++you++think', u'right++?++what++do++you++think', 6, 1, u'[1, 0, 0, 0, 1, 0]', u'[1, 0, 0, 0, 1, 0]', None, None, None, None), (u'?++1++\U0001f62b', u'?++1++\U0001f62b', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[1, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[2, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, None, None), (u'you++but++you++\U0001f600', u'you++but++you++\U0001f600', 4, 1, u'[3, 3, "IGNOR", 1]', u'[4, 3, "IGNOR", 1]', u'[1, 1, "IGNOR", 0]', u'[2, 3, "IGNOR", 0]', None, None), (u'about++it++?', u'about++it++?', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'think++about++it', u'think++about++it', 3, 1, None, None, None, None, None, None), (u'surprise++.++but++you++but', u'surpris++.++but++you++but', 5, 1, u'[0, 0, 5, 2, "IGNOR"]', u'[0, 0, 5, 2, "IGNOR"]', u'[0, 0, 2, 1, "IGNOR"]', u'[0, 0, 5, 2, "IGNOR"]', None, None), (u'about++it', u'about++it', 2, 1, None, None, None, None, None, None), (u'1++.++but++you', u'1++.++but++you', 4, 1, u'[1, 0, 2, 2]', u'[1, 0, 5, 2]', u'[0, 0, 1, 1]', u'[0, 0, 2, 2]', None, None), (u'but++you++but++you', u'but++you++but++you', 4, 2, u'[10, 6, "IGNOR", "IGNOR"]', u'[15, 8, "IGNOR", "IGNOR"]', u'[4, 2, "IGNOR", "IGNOR"]', u'[10, 4, "IGNOR", "IGNOR"]', None, None), (u'about++it++?++1++\U0001f62b', u'about++it++?++1++\U0001f62b', 5, 1, u'[0, 0, 1, 1, 1]', u'[0, 0, 1, 1, 1]', None, None, None, None), (u'.++right++?', u'.++right++?', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'tiny++surprise++.++but++you', u'tini++surpris++.++but++you', 5, 1, u'[1, 0, 0, 2, 2]', u'[1, 0, 0, 2, 2]', u'[1, 0, 0, 1, 1]', u'[3, 0, 0, 2, 2]', None, None), (u'you++think++about++it', u'you++think++about++it', 4, 1, u'[1, 0, 0, 0]', u'[1, 0, 0, 0]', None, None, None, None), (u'do++you', u'do++you', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'1++\U0001f62b', u'1++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'.++right++?++what++do', u'.++right++?++what++do', 5, 1, u'[0, 1, 0, 0, 0]', u'[0, 1, 0, 0, 0]', None, None, None, None), (u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 6, 1, u'[3, 1, 2, 2, "IGNOR", "IGNOR"]', u'[3, 2, 2, 2, "IGNOR", "IGNOR"]', u'[1, 0, 0, 0, "IGNOR", "IGNOR"]', u'[3, 0, 0, 0, "IGNOR", "IGNOR"]', None, None), (u'1++\U0001f62b++1', u'1++\U0001f62b++1', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, None, None), (u'big++explanation++.++right', u'big++explan++.++right', 4, 1, u'[0, 1, 0, 1]', u'[0, 1, 0, 1]', u'[1, 0, 0, 0]', u'[3, 0, 0, 0]', None, None), (u'it++?++1++\U0001f62b++1++.', u'it++?++1++\U0001f62b++1++.', 6, 1, u'[0, 1, 2, 1, "IGNOR", 0]', u'[0, 1, 2, 1, "IGNOR", 0]', None, None, None, None), (u'?++1++\U0001f62b++1++.', u'?++1++\U0001f62b++1++.', 5, 1, u'[1, 2, 1, "IGNOR", 0]', u'[1, 2, 1, "IGNOR", 0]', None, None, None, None), (u'you++\U0001f600', u'you++\U0001f600', 2, 1, u'[1, 1]', u'[2, 1]', None, None, None, None), (u'a', u'a', 1, 3, None, None, None, None, None, None), (u'1++\U0001f62b++1++.++but++you', u'1++\U0001f62b++1++.++but++you', 6, 1, u'[2, 1, "IGNOR", 0, 2, 2]', u'[2, 1, "IGNOR", 0, 5, 2]', u'[0, 0, "IGNOR", 0, 1, 1]', u'[0, 0, "IGNOR", 0, 2, 2]', None, None), (u'you++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[2, 1, 1]', None, None, None, None), (u'.++right++?++what++do++you', u'.++right++?++what++do++you', 6, 1, u'[0, 1, 0, 0, 0, 1]', u'[0, 1, 0, 0, 0, 1]', None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 5, 1, u'[1, 2, 2, "IGNOR", "IGNOR"]', u'[2, 2, 2, "IGNOR", "IGNOR"]', None, None, None, None), (u'think', u'think', 1, 1, None, None, None, None, None, None), (u'1++\U0001f62b++1++.++but', u'1++\U0001f62b++1++.++but', 5, 1, u'[2, 1, "IGNOR", 0, 2]', u'[2, 1, "IGNOR", 0, 5]', u'[0, 0, "IGNOR", 0, 1]', u'[0, 0, "IGNOR", 0, 2]', None, None), (u'think++about++it++?', u'think++about++it++?', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u'big', u'big', 1, 5, u'2', u'2', u'2', u'5', u'2', u'2'), (u'big++explanation', u'big++explan', 2, 1, u'[0, 1]', u'[0, 1]', u'[1, 0]', u'[3, 0]', None, None), (u'1++.++but++you++but++you', u'1++.++but++you++but++you', 6, 1, u'[1, 0, 5, 3, "IGNOR", "IGNOR"]', u'[1, 0, 10, 4, "IGNOR", "IGNOR"]', u'[0, 0, 2, 1, "IGNOR", "IGNOR"]', u'[0, 0, 5, 2, "IGNOR", "IGNOR"]', None, None), (u'right++?++what++do++you', u'right++?++what++do++you', 5, 1, u'[1, 0, 0, 0, 1]', u'[1, 0, 0, 0, 1]', None, None, None, None), (u'but++a++big++explanation', u'but++a++big++explan', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', u'[0, 0, 1, 0]', u'[0, 0, 3, 0]', None, None), (u'?++1++\U0001f62b++1', u'?++1++\U0001f62b++1', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[1, 2, 1, "IGNOR"]', None, None, None, None), (u'do', u'do', 1, 1, None, None, None, None, None, None), (u'a++big++explanation++.', u'a++big++explan++.', 4, 1, u'[0, 0, 1, 0]', u'[0, 0, 1, 0]', u'[0, 1, 0, 0]', u'[0, 3, 0, 0]', None, None), (u'a++big++explanation++.++right++?', u'a++big++explan++.++right++?', 6, 1, u'[0, 0, 1, 0, 1, 0]', u'[0, 0, 1, 0, 1, 0]', u'[0, 1, 0, 0, 0, 0]', u'[0, 3, 0, 0, 0, 0]', None, None), (u'but++a', u'but++a', 2, 1, None, None, None, None, None, None), (u'1++.', u'1++.', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u',++but++a++big', u',++but++a++big', 4, 1, None, None, u'[0, 0, 0, 1]', u'[0, 0, 0, 3]', None, None), (u'but++i++realy++liked', u'but++i++reali++like', 4, 1, u'[1, 0, 2, 0]', u'[1, 0, 4, 0]', u'[0, 0, 1, 0]', u'[0, 0, 3, 0]', None, None), (u'liked++it++:p++=)++\U0001f600++\U0001f308', u'like++it++:p++=)++\U0001f600++\U0001f308', 6, 1, u'[0, 0, 0, 1, 1, 1]', u'[0, 0, 0, 1, 1, 1]', None, None, None, None), (u'was++realy', u'was++reali', 2, 1, None, None, None, None, None, None), (u',++but++i++realy', u',++but++i++reali', 4, 1, u'[0, 1, 0, 2]', u'[0, 1, 0, 4]', u'[0, 0, 0, 1]', u'[0, 0, 0, 3]', None, None), (u'bad++surprise++for++me++\U0001f62b++,', u'bad++surpris++for++me++\U0001f62b++,', 6, 1, u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 1, 0]', None, None, None, None), (u'i++realy++liked++it++:p', u'i++reali++like++it++:p', 5, 1, u'[0, 2, 0, 0, 0]', u'[0, 4, 0, 0, 0]', u'[0, 1, 0, 0, 0]', u'[0, 3, 0, 0, 0]', None, None), (u'it', u'it', 1, 5, None, None, None, None, None, None), (u'but', u'but', 1, 13, u'11', u'16', u'4', u'10', u'11', u'4'), (u'realy++liked', u'reali++like', 2, 1, u'[2, 0]', u'[4, 0]', u'[1, 0]', u'[3, 0]', None, None), (u':p++=)++\U0001f600++\U0001f308++\U0001f600', u':p++=)++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[0, 1, 1, 1, "IGNOR"]', u'[0, 1, 1, 1, "IGNOR"]', None, None, None, None), (u'realy++bad++surprise++for', u'reali++bad++surpris++for', 4, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,++but++i', u'me++\U0001f62b++,++but++i', 5, 1, u'[0, 1, 0, 1, 0]', u'[0, 1, 0, 1, 0]', None, None, None, None), (u'me', u'me', 1, 2, None, None, None, None, None, None), (u'was++realy++bad++surprise++for++me', u'was++reali++bad++surpris++for++me', 6, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,', u'me++\U0001f62b++,', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'liked++it++:p++=)++\U0001f600', u'like++it++:p++=)++\U0001f600', 5, 1, u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 1, 1]', None, None, None, None), (u'\U0001f62b++,++but', u'\U0001f62b++,++but', 3, 1, u'[1, 0, 1]', u'[1, 0, 1]', None, None, None, None), (u'realy', u'reali', 1, 4, u'2', u'4', u'1', u'3', u'2', u'1'), (u'surprise++for++me++\U0001f62b', u'surpris++for++me++\U0001f62b', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u'i++realy++liked++it++:p++=)', u'i++reali++like++it++:p++=)', 6, 1, u'[0, 2, 0, 0, 0, 1]', u'[0, 4, 0, 0, 0, 1]', u'[0, 1, 0, 0, 0, 0]', u'[0, 3, 0, 0, 0, 0]', None, None), (u'\U0001f600', u'\U0001f600', 1, 5, u'4', u'4', None, None, u'4', None), (u'\U0001f308++\U0001f600', u'\U0001f308++\U0001f600', 2, 3, u'[3, 2]', u'[3, 2]', None, None, None, None), (u'=)', u'=)', 1, 1, u'1', u'1', None, None, u'1', None), (u':p', u':p', 1, 1, None, None, None, None, None, None), (u'i++realy++liked++it', u'i++reali++like++it', 4, 1, u'[0, 2, 0, 0]', u'[0, 4, 0, 0]', u'[0, 1, 0, 0]', u'[0, 3, 0, 0]', None, None), (u'me++\U0001f62b++,++but', u'me++\U0001f62b++,++but', 4, 1, u'[0, 1, 0, 1]', u'[0, 1, 0, 1]', None, None, None, None), (u'it++was', u'it++was', 2, 2, None, None, None, None, None, None), (u'surprise++for++me', u'surpris++for++me', 3, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but++i++realy', u'\U0001f62b++,++but++i++reali', 5, 1, u'[1, 0, 1, 0, 2]', u'[1, 0, 1, 0, 4]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 3]', None, None), (u'=)++\U0001f600++\U0001f308', u'=)++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, None, None), (u',++but++i', u',++but++i', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'it++:p++=)++\U0001f600', u'it++:p++=)++\U0001f600', 4, 1, u'[0, 0, 1, 1]', u'[0, 0, 1, 1]', None, None, None, None), (u'but++i++realy++liked++it++:p', u'but++i++reali++like++it++:p', 6, 1, u'[1, 0, 2, 0, 0, 0]', u'[1, 0, 4, 0, 0, 0]', u'[0, 0, 1, 0, 0, 0]', u'[0, 0, 3, 0, 0, 0]', None, None), (u'realy++liked++it++:p++=)', u'reali++like++it++:p++=)', 5, 1, u'[2, 0, 0, 0, 1]', u'[4, 0, 0, 0, 1]', u'[1, 0, 0, 0, 0]', u'[3, 0, 0, 0, 0]', None, None), (u'=)++\U0001f600++\U0001f308++\U0001f600', u'=)++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[1, 1, 1, "IGNOR"]', u'[1, 1, 1, "IGNOR"]', None, None, None, None), (u'liked++it', u'like++it', 2, 1, None, None, None, None, None, None), (u'it++:p++=)', u'it++:p++=)', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'realy++bad++surprise++for++me', u'reali++bad++surpris++for++me', 5, 1, None, None, None, None, None, None), (u'\U0001f62b++,', u'\U0001f62b++,', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'but++i++realy++liked++it', u'but++i++reali++like++it', 5, 1, u'[1, 0, 2, 0, 0]', u'[1, 0, 4, 0, 0]', u'[0, 0, 1, 0, 0]', u'[0, 0, 3, 0, 0]', None, None), (u'for++me', u'for++me', 2, 2, None, None, None, None, None, None), (u'\U0001f308', u'\U0001f308', 1, 3, u'3', u'3', None, None, u'3', None), (u'for++me++\U0001f62b', u'for++me++\U0001f62b', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'but++i', u'but++i', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'bad++surprise', u'bad++surpris', 2, 1, None, None, None, None, None, None), (u'i++realy++liked', u'i++reali++like', 3, 1, u'[0, 2, 0]', u'[0, 4, 0]', u'[0, 1, 0]', u'[0, 3, 0]', None, None), (u'bad++surprise++for++me', u'bad++surpris++for++me', 4, 1, None, None, None, None, None, None), (u'for++me++\U0001f62b++,++but', u'for++me++\U0001f62b++,++but', 5, 1, u'[0, 0, 1, 0, 1]', u'[0, 0, 1, 0, 1]', None, None, None, None), (u'realy++liked++it', u'reali++like++it', 3, 1, u'[2, 0, 0]', u'[4, 0, 0]', u'[1, 0, 0]', u'[3, 0, 0]', None, None), (u'\U0001f600++\U0001f308', u'\U0001f600++\U0001f308', 2, 3, u'[3, 3]', u'[3, 3]', None, None, None, None), (u'it++:p', u'it++:p', 2, 1, None, None, None, None, None, None), (u'liked++it++:p', u'like++it++:p', 3, 1, None, None, None, None, None, None), (u'for', u'for', 1, 3, None, None, None, None, None, None), (u'for++me++\U0001f62b++,', u'for++me++\U0001f62b++,', 4, 1, u'[0, 0, 1, 0]', u'[0, 0, 1, 0]', None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600', 3, 3, u'[4, 3, "IGNOR"]', u'[5, 3, "IGNOR"]', None, None, None, None), (u'realy++bad++surprise', u'reali++bad++surpris', 3, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but++i++realy++liked', u'\U0001f62b++,++but++i++reali++like', 6, 1, u'[1, 0, 1, 0, 2, 0]', u'[1, 0, 1, 0, 4, 0]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 3, 0]', None, None), (u'was++realy++bad++surprise', u'was++reali++bad++surpris', 4, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,++but++i++realy', u'me++\U0001f62b++,++but++i++reali', 6, 1, u'[0, 1, 0, 1, 0, 2]', u'[0, 1, 0, 1, 0, 4]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 3]', None, None), (u',', u',', 1, 4, None, None, None, None, None, None), (u',++but', u',++but', 2, 2, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'it++:p++=)++\U0001f600++\U0001f308', u'it++:p++=)++\U0001f600++\U0001f308', 5, 1, u'[0, 0, 1, 1, 1]', u'[0, 0, 1, 1, 1]', None, None, None, None), (u'was++realy++bad++surprise++for', u'was++reali++bad++surpris++for', 5, 1, None, None, None, None, None, None), (u'=)++\U0001f600', u'=)++\U0001f600', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'bad++surprise++for++me++\U0001f62b', u'bad++surpris++for++me++\U0001f62b', 5, 1, u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 1]', None, None, None, None), (u':p++=)', u':p++=)', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'\U0001f62b++,++but++i', u'\U0001f62b++,++but++i', 4, 1, u'[1, 0, 1, 0]', u'[1, 0, 1, 0]', None, None, None, None), (u'realy++bad++surprise++for++me++\U0001f62b', u'reali++bad++surpris++for++me++\U0001f62b', 6, 1, u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 1]', None, None, None, None), (u':p++=)++\U0001f600', u':p++=)++\U0001f600', 3, 1, u'[0, 1, 1]', u'[0, 1, 1]', None, None, None, None), (u'me++\U0001f62b', u'me++\U0001f62b', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'realy++liked++it++:p', u'reali++like++it++:p', 4, 1, u'[2, 0, 0, 0]', u'[4, 0, 0, 0]', u'[1, 0, 0, 0]', u'[3, 0, 0, 0]', None, None), (u'surprise', u'surpris', 1, 2, None, None, None, None, None, None), (u'it++was++realy++bad++surprise', u'it++was++reali++bad++surpris', 5, 1, None, None, None, None, None, None), (u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[0, 0, 1, 1, 1, "IGNOR"]', u'[0, 0, 1, 1, 1, "IGNOR"]', None, None, None, None), (u'\U0001f62b', u'\U0001f62b', 1, 3, u'3', u'3', None, None, u'3', None), (u'but++i++realy', u'but++i++reali', 3, 1, u'[1, 0, 2]', u'[1, 0, 4]', u'[0, 0, 1]', u'[0, 0, 3]', None, None), (u'it++was++realy++bad++surprise++for', u'it++was++reali++bad++surpris++for', 6, 1, None, None, None, None, None, None), (u':p++=)++\U0001f600++\U0001f308', u':p++=)++\U0001f600++\U0001f308', 4, 1, u'[0, 1, 1, 1]', u'[0, 1, 1, 1]', None, None, None, None), (u'bad', u'bad', 1, 6, u'4', u'7', u'1', u'5', u'4', u'1'), (u'surprise++for++me++\U0001f62b++,', u'surpris++for++me++\U0001f62b++,', 5, 1, u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 1, 0]', None, None, None, None), (u'surprise++for++me++\U0001f62b++,++but', u'surpris++for++me++\U0001f62b++,++but', 6, 1, u'[0, 0, 0, 1, 0, 1]', u'[0, 0, 0, 1, 0, 1]', None, None, None, None), (u'it++was++realy++bad', u'it++was++reali++bad', 4, 1, None, None, None, None, None, None), (u'it++was++realy', u'it++was++reali', 3, 1, None, None, None, None, None, None), (u'bad++surprise++for', u'bad++surpris++for', 3, 1, None, None, None, None, None, None), (u'liked++it++:p++=)', u'like++it++:p++=)', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u'i', u'i', 1, 2, None, None, None, None, None, None), (u'surprise++for', u'surpris++for', 2, 1, None, None, None, None, None, None), (u'realy++liked++it++:p++=)++\U0001f600', u'reali++like++it++:p++=)++\U0001f600', 6, 1, u'[2, 0, 0, 0, 1, 1]', u'[4, 0, 0, 0, 1, 1]', u'[1, 0, 0, 0, 0, 0]', u'[3, 0, 0, 0, 0, 0]', None, None), (u',++but++i++realy++liked', u',++but++i++reali++like', 5, 1, u'[0, 1, 0, 2, 0]', u'[0, 1, 0, 4, 0]', u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 3, 0]', None, None), (u'realy++bad', u'reali++bad', 2, 1, None, None, None, None, None, None), (u'for++me++\U0001f62b++,++but++i', u'for++me++\U0001f62b++,++but++i', 6, 1, u'[0, 0, 1, 0, 1, 0]', u'[0, 0, 1, 0, 1, 0]', None, None, None, None), (u'was++realy++bad', u'was++reali++bad', 3, 1, None, None, None, None, None, None), (u'was', u'was', 1, 2, None, None, None, None, None, None), (u'liked', u'like', 1, 1, None, None, None, None, None, None), (u'i++realy', u'i++reali', 2, 1, u'[0, 2]', u'[0, 4]', u'[0, 1]', u'[0, 3]', None, None), (u',++but++i++realy++liked++it', u',++but++i++reali++like++it', 6, 1, u'[0, 1, 0, 2, 0, 0]', u'[0, 1, 0, 4, 0, 0]', u'[0, 0, 0, 1, 0, 0]', u'[0, 0, 0, 3, 0, 0]', None, None)]

        # right_baseline_not_freezed_full_repetativ = [(u'also++very++pity++for++me', u'also++veri++piti++for++me', 5, 1, None, None, None, None, None, None), (u'it++was++also++very', u'it++was++also++veri', 4, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump++#shetlife', u'.++:-(++@real_trump++#shetlif', 4, 1, None, None, None, None, None, None), (u'.++but++it', u'.++but++it', 3, 1, None, None, None, None, None, None), (u'to', u'to', 1, 1, None, None, None, None, None, None), (u':-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u':-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 5, 1, None, None, None, None, None, None), (u'glad++to++se++you++-)', u'glad++to++se++you++-)', 5, 1, None, None, None, None, None, None), (u'i++loved++it++.++but', u'i++love++it++.++but', 5, 1, None, None, None, None, None, None), (u'me++.', u'me++.', 2, 1, None, None, None, None, None, None), (u'i++loved', u'i++love', 2, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump', u'.++:-(++@real_trump', 3, 1, None, None, None, None, None, None), (u'i++loved++it', u'i++love++it', 3, 1, None, None, None, None, None, None), (u'-)', u'-)', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++-)', u'you++-)', 2, 1, None, None, None, None, None, None), (u'me++.++:-(', u'me++.++:-(', 3, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump++#shetlife++#readytogo', u'.++:-(++@real_trump++#shetlif++#readytogo', 5, 1, None, None, None, None, None, None), (u'but++it', u'but++it', 2, 1, None, None, None, None, None, None), (u'pity++for++me++.', u'piti++for++me++.', 4, 1, None, None, None, None, None, None), (u'for++me++.++:-(', u'for++me++.++:-(', 4, 1, None, None, None, None, None, None), (u'me++.++:-(++@real_trump++#shetlife++#readytogo', u'me++.++:-(++@real_trump++#shetlif++#readytogo', 6, 1, None, None, None, None, None, None), (u'it++was++also++very++pity', u'it++was++also++veri++piti', 5, 1, None, None, None, None, None, None), (u'very++pity++for++me++.++:-(', u'veri++piti++for++me++.++:-(', 6, 1, None, None, None, None, None, None), (u'to++se++you++-)', u'to++se++you++-)', 4, 1, None, None, None, None, None, None), (u'http://www.absurd.com', u'http://www.absurd.com', 1, 1, None, None, None, None, None, None), (u'it++was++also++very++pity++for', u'it++was++also++veri++piti++for', 6, 1, None, None, None, None, None, None), (u'very++pity++for', u'veri++piti++for', 3, 1, None, None, None, None, None, None), (u'it++.', u'it++.', 2, 1, None, None, None, None, None, None), (u'loved', u'love', 1, 1, None, None, None, None, None, None), (u'@real_trump', u'@real_trump', 1, 1, None, None, None, None, None, None), (u'se++you++-)', u'se++you++-)', 3, 1, None, None, None, None, None, None), (u'glad++to', u'glad++to', 2, 1, None, None, None, None, None, None), (u'but++it++was++also++very', u'but++it++was++also++veri', 5, 1, None, None, None, None, None, None), (u'also', u'also', 1, 1, None, None, None, None, None, None), (u'for++me++.', u'for++me++.', 3, 1, None, None, None, None, None, None), (u'loved++it++.++but++it', u'love++it++.++but++it', 5, 1, None, None, None, None, None, None), (u'was++also', u'was++also', 2, 1, None, None, None, None, None, None), (u'it++was++also', u'it++was++also', 3, 1, None, None, None, None, None, None), (u'loved++it', u'love++it', 2, 1, None, None, None, None, None, None), (u'pity++for++me++.++:-(', u'piti++for++me++.++:-(', 5, 1, None, None, None, None, None, None), (u'loved++it++.++but', u'love++it++.++but', 4, 1, None, None, None, None, None, None), (u'@real_trump++#shetlife++#readytogo++http://www.absurd.com', u'@real_trump++#shetlif++#readytogo++http://www.absurd.com', 4, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u'.++:-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 6, 1, None, None, None, None, None, None), (u'pity', u'piti', 1, 4, u'2', u'4', u'1', u'4', u'2', u'1'), (u'me++.++:-(++@real_trump', u'me++.++:-(++@real_trump', 4, 1, None, None, None, None, None, None), (u'but++it++was++also++very++pity', u'but++it++was++also++veri++piti', 6, 1, None, None, None, None, None, None), (u'i++loved++it++.', u'i++love++it++.', 4, 1, None, None, None, None, None, None), (u'very++pity++for++me++.', u'veri++piti++for++me++.', 5, 1, None, None, None, None, None, None), (u'#readytogo++http://www.absurd.com', u'#readytogo++http://www.absurd.com', 2, 1, None, None, None, None, None, None), (u'#readytogo', u'#readytogo', 1, 1, None, None, None, None, None, None), (u'also++very++pity++for++me++.', u'also++veri++piti++for++me++.', 6, 1, None, None, None, None, None, None), (u'se++you', u'se++you', 2, 1, None, None, None, None, None, None), (u'se', u'se', 1, 1, u'1', u'1', None, None, u'1', None), (u'for++me++.++:-(++@real_trump++#shetlife', u'for++me++.++:-(++@real_trump++#shetlif', 6, 1, None, None, None, None, None, None), (u'but++it++was', u'but++it++was', 3, 1, None, None, None, None, None, None), (u'glad++to++se++you', u'glad++to++se++you', 4, 1, None, None, None, None, None, None), (u'#shetlife++#readytogo', u'#shetlif++#readytogo', 2, 1, None, None, None, None, None, None), (u'very++pity++for++me', u'veri++piti++for++me', 4, 1, None, None, None, None, None, None), (u'@real_trump++#shetlife++#readytogo', u'@real_trump++#shetlif++#readytogo', 3, 1, None, None, None, None, None, None), (u'#shetlife++#readytogo++http://www.absurd.com', u'#shetlif++#readytogo++http://www.absurd.com', 3, 1, None, None, None, None, None, None), (u':-(++@real_trump', u':-(++@real_trump', 2, 1, None, None, None, None, None, None), (u'pity++for++me++.++:-(++@real_trump', u'piti++for++me++.++:-(++@real_trump', 6, 1, None, None, None, None, None, None), (u'.++but++it++was++also', u'.++but++it++was++also', 5, 1, None, None, None, None, None, None), (u'it++.++but++it++was', u'it++.++but++it++was', 5, 1, None, None, None, None, None, None), (u'was++also++very++pity++for', u'was++also++veri++piti++for', 5, 1, None, None, None, None, None, None), (u'also++very', u'also++veri', 2, 1, None, None, None, None, None, None), (u'to++se', u'to++se', 2, 1, None, None, None, None, None, None), (u'pity++for', u'piti++for', 2, 1, None, None, None, None, None, None), (u'to++se++you', u'to++se++you', 3, 1, None, None, None, None, None, None), (u'for++me++.++:-(++@real_trump', u'for++me++.++:-(++@real_trump', 5, 1, None, None, None, None, None, None), (u'also++very++pity', u'also++veri++piti', 3, 1, None, None, None, None, None, None), (u'very', u'veri', 1, 3, u'2', u'4', u'1', u'3', u'2', u'1'), (u'it++.++but++it++was++also', u'it++.++but++it++was++also', 6, 1, None, None, None, None, None, None), (u'was++also++very', u'was++also++veri', 3, 1, None, None, None, None, None, None), (u'loved++it++.++but++it++was', u'love++it++.++but++it++was', 6, 1, None, None, None, None, None, None), (u'pity++for++me', u'piti++for++me', 3, 1, None, None, None, None, None, None), (u'me++.++:-(++@real_trump++#shetlife', u'me++.++:-(++@real_trump++#shetlif', 5, 1, None, None, None, None, None, None), (u'very++pity', u'veri++piti', 2, 1, u'[2, 2]', u'[4, 4]', u'[1, 1]', u'[3, 4]', u'1', u'1'), (u'was++also++very++pity++for++me', u'was++also++veri++piti++for++me', 6, 1, None, None, None, None, None, None), (u'also++very++pity++for', u'also++veri++piti++for', 4, 1, None, None, None, None, None, None), (u'but++it++was++also', u'but++it++was++also', 4, 1, None, None, None, None, None, None), (u'@real_trump++#shetlife', u'@real_trump++#shetlif', 2, 1, None, None, None, None, None, None), (u'it++.++but++it', u'it++.++but++it', 4, 1, None, None, None, None, None, None), (u'.++but++it++was', u'.++but++it++was', 4, 1, None, None, None, None, None, None), (u':-(++@real_trump++#shetlife', u':-(++@real_trump++#shetlif', 3, 1, None, None, None, None, None, None), (u'glad++to++se', u'glad++to++se', 3, 1, None, None, None, None, None, None), (u':-(++@real_trump++#shetlife++#readytogo', u':-(++@real_trump++#shetlif++#readytogo', 4, 1, None, None, None, None, None, None), (u'.++:-(', u'.++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'loved++it++.', u'love++it++.', 3, 1, None, None, None, None, None, None), (u'glad', u'glad', 1, 1, u'1', u'1', None, None, u'1', None), (u'.++but++it++was++also++very', u'.++but++it++was++also++veri', 6, 1, None, None, None, None, None, None), (u'was++also++very++pity', u'was++also++veri++piti', 4, 1, None, None, None, None, None, None), (u'i++loved++it++.++but++it', u'i++love++it++.++but++it', 6, 1, None, None, None, None, None, None), (u'it++.++but', u'it++.++but', 3, 1, None, None, None, None, None, None), (u',++which', u',++which', 2, 2, None, None, None, None, None, None), (u'bad++news++,++which', u'bad++news++,++which', 4, 1, None, None, None, None, None, None), (u',++which++we++can++not', u',++which++we++can++not', 5, 1, None, None, None, None, None, None), (u'tiny++model++,++which++we', u'tini++model++,++which++we', 5, 1, None, None, None, None, None, None), (u'acept++.++-(', u'acept++.++-(', 3, 1, None, None, None, None, None, None), (u',++which++we++can', u',++which++we++can', 4, 2, None, None, None, None, None, None), (u'acept++.', u'acept++.', 2, 1, None, None, None, None, None, None), (u',++which++we', u',++which++we', 3, 2, None, None, None, None, None, None), (u'not++acept++.++-(++\U0001f62b', u'not++acept++.++-(++\U0001f62b', 5, 1, None, None, None, None, None, None), (u'tiny++model++,++which', u'tini++model++,++which', 4, 1, None, None, None, None, None, None), (u'a++bad++news++,', u'a++bad++news++,', 4, 1, None, None, None, None, None, None), (u'can++not++acept++.', u'can++not++acept++.', 4, 1, None, None, None, None, None, None), (u'-(++\U0001f62b', u'-(++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'which++we++can', u'which++we++can', 3, 2, None, None, None, None, None, None), (u'-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 5, 1, None, None, None, None, None, None), (u'explain++a++big', u'explain++a++big', 3, 1, None, None, None, None, None, None), (u'we++can', u'we++can', 2, 2, None, None, None, None, None, None), (u'can++use', u'can++use', 2, 1, None, None, None, None, None, None), (u'we++can++use++for++explain', u'we++can++use++for++explain', 5, 1, None, None, None, None, None, None), (u',++which++we++can++use++for', u',++which++we++can++use++for', 6, 1, None, None, None, None, None, None), (u'use++for++explain', u'use++for++explain', 3, 1, None, None, None, None, None, None), (u'explain++a++big++things++.', u'explain++a++big++thing++.', 5, 1, None, None, None, None, None, None), (u'a++bad++news', u'a++bad++news', 3, 1, None, None, None, None, None, None), (u'bad++news++,++which++we', u'bad++news++,++which++we', 5, 1, None, None, None, None, None, None), (u'for++explain', u'for++explain', 2, 1, None, None, None, None, None, None), (u'can++use++for++explain++a', u'can++use++for++explain++a', 5, 1, None, None, None, None, None, None), (u'we++can++not', u'we++can++not', 3, 1, None, None, None, None, None, None), (u'explain', u'explain', 1, 1, None, None, None, None, None, None), (u'-(', u'-(', 1, 1, u'1', u'1', None, None, u'1', None), (u'bad++news++,++which++we++can', u'bad++news++,++which++we++can', 6, 1, None, None, None, None, None, None), (u'bad++news', u'bad++news', 2, 1, None, None, None, None, None, None), (u'news++,++which++we++can', u'news++,++which++we++can', 5, 1, None, None, None, None, None, None), (u'news++,++which++we', u'news++,++which++we', 4, 1, None, None, None, None, None, None), (u'a++bad++news++,++which', u'a++bad++news++,++which', 5, 1, None, None, None, None, None, None), (u'big++things++.', u'big++thing++.', 3, 1, None, None, None, None, None, None), (u'things++.', u'thing++.', 2, 1, None, None, None, None, None, None), (u'things', u'thing', 1, 1, None, None, None, None, None, None), (u'-(++\U0001f62b++:-(', u'-(++\U0001f62b++:-(', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), (u'model++,++which++we', u'model++,++which++we', 4, 1, None, None, None, None, None, None), (u'#shetlife', u'#shetlif', 1, 3, None, None, u'1', u'2', None, u'1'), (u'can++not++acept++.++-(++\U0001f62b', u'can++not++acept++.++-(++\U0001f62b', 6, 1, None, None, None, None, None, None), (u'we++can++not++acept++.', u'we++can++not++acept++.', 5, 1, None, None, None, None, None, None), (u'big++things', u'big++thing', 2, 1, None, None, None, None, None, None), (u'use++for++explain++a', u'use++for++explain++a', 4, 1, None, None, None, None, None, None), (u'not++acept', u'not++acept', 2, 1, None, None, None, None, None, None), (u'acept++.++-(++\U0001f62b++:-(', u'acept++.++-(++\U0001f62b++:-(', 5, 1, None, None, None, None, None, None), (u'for++explain++a++big++things++.', u'for++explain++a++big++thing++.', 6, 1, None, None, None, None, None, None), (u'\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'\U0001f62b++:-(++#shetlif++http://www.noooo.com', 4, 1, None, None, None, None, None, None), (u'we++can++use', u'we++can++use', 3, 1, None, None, None, None, None, None), (u'which++we++can++use++for++explain', u'which++we++can++use++for++explain', 6, 1, None, None, None, None, None, None), (u'not++acept++.++-(', u'not++acept++.++-(', 4, 1, None, None, None, None, None, None), (u':-(++#shetlife', u':-(++#shetlif', 2, 1, None, None, None, None, None, None), (u'which++we++can++use', u'which++we++can++use', 4, 1, None, None, None, None, None, None), (u'explain++a', u'explain++a', 2, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'.++-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 6, 1, None, None, None, None, None, None), (u'not++acept++.', u'not++acept++.', 3, 1, None, None, None, None, None, None), (u'a++big++things', u'a++big++thing', 3, 1, None, None, None, None, None, None), (u'.++-(', u'.++-(', 2, 1, None, None, None, None, None, None), (u'a++bad', u'a++bad', 2, 1, None, None, None, None, None, None), (u'use++for', u'use++for', 2, 1, None, None, None, None, None, None), (u'can++not++acept++.++-(', u'can++not++acept++.++-(', 5, 1, None, None, None, None, None, None), (u'a++big++things++.', u'a++big++thing++.', 4, 1, None, None, None, None, None, None), (u'news', u'news', 1, 1, None, None, None, None, None, None), (u'which++we++can++not', u'which++we++can++not', 4, 1, None, None, None, None, None, None), (u'http://www.noooo.com', u'http://www.noooo.com', 1, 1, None, None, None, None, None, None), (u'-(++\U0001f62b++:-(++#shetlife', u'-(++\U0001f62b++:-(++#shetlif', 4, 1, None, None, None, None, None, None), (u'acept++.++-(++\U0001f62b', u'acept++.++-(++\U0001f62b', 4, 1, None, None, None, None, None, None), (u'which++we++can++not++acept', u'which++we++can++not++acept', 5, 1, None, None, None, None, None, None), (u':-(', u':-(', 1, 2, u'2', u'2', None, None, u'2', None), (u'news++,++which++we++can++not', u'news++,++which++we++can++not', 6, 1, None, None, None, None, None, None), (u'can++use++for++explain', u'can++use++for++explain', 4, 1, None, None, None, None, None, None), (u':-(++#shetlife++http://www.noooo.com', u':-(++#shetlif++http://www.noooo.com', 3, 1, None, None, None, None, None, None), (u'not', u'not', 1, 1, None, None, None, None, None, None), (u',++which++we++can++not++acept', u',++which++we++can++not++acept', 6, 1, None, None, None, None, None, None), (u'which++we++can++use++for', u'which++we++can++use++for', 5, 1, None, None, None, None, None, None), (u'can++not++acept', u'can++not++acept', 3, 1, None, None, None, None, None, None), (u'explain++a++big++things', u'explain++a++big++thing', 4, 1, None, None, None, None, None, None), (u'can', u'can', 1, 2, None, None, None, None, None, None), (u'tiny++model++,++which++we++can', u'tini++model++,++which++we++can', 6, 1, None, None, None, None, None, None), (u'acept++.++-(++\U0001f62b++:-(++#shetlife', u'acept++.++-(++\U0001f62b++:-(++#shetlif', 6, 1, None, None, None, None, None, None), (u'use++for++explain++a++big++things', u'use++for++explain++a++big++thing', 6, 1, None, None, None, None, None, None), (u'we++can++use++for++explain++a', u'we++can++use++for++explain++a', 6, 1, None, None, None, None, None, None), (u'use++for++explain++a++big', u'use++for++explain++a++big', 5, 1, None, None, None, None, None, None), (u'model++,++which++we++can++use', u'model++,++which++we++can++use', 6, 1, None, None, None, None, None, None), (u'which++we', u'which++we', 2, 2, None, None, None, None, None, None), (u'not++acept++.++-(++\U0001f62b++:-(', u'not++acept++.++-(++\U0001f62b++:-(', 6, 1, None, None, None, None, None, None), (u'model++,++which++we++can', u'model++,++which++we++can', 5, 1, None, None, None, None, None, None), (u'we++can++not++acept', u'we++can++not++acept', 4, 1, None, None, None, None, None, None), (u'use', u'use', 1, 1, None, None, None, None, None, None), (u',++which++we++can++use', u',++which++we++can++use', 5, 1, None, None, None, None, None, None), (u'bad++news++,', u'bad++news++,', 3, 1, None, None, None, None, None, None), (u'can++use++for', u'can++use++for', 3, 1, None, None, None, None, None, None), (u'news++,', u'news++,', 2, 1, None, None, None, None, None, None), (u'can++not', u'can++not', 2, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(', u'.++-(++\U0001f62b++:-(', 4, 1, None, None, None, None, None, None), (u'we', u'we', 1, 2, None, None, None, None, None, None), (u'for++explain++a', u'for++explain++a', 3, 1, None, None, None, None, None, None), (u'acept', u'acept', 1, 1, None, None, None, None, None, None), (u'for++explain++a++big', u'for++explain++a++big', 4, 1, None, None, None, None, None, None), (u'a++bad++news++,++which++we', u'a++bad++news++,++which++we', 6, 1, None, None, None, None, None, None), (u'#shetlife++http://www.noooo.com', u'#shetlif++http://www.noooo.com', 2, 1, None, None, None, None, None, None), (u'\U0001f62b++:-(', u'\U0001f62b++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'.++-(++\U0001f62b', u'.++-(++\U0001f62b', 3, 1, None, None, None, None, None, None), (u'we++can++not++acept++.++-(', u'we++can++not++acept++.++-(', 6, 1, None, None, None, None, None, None), (u'news++,++which', u'news++,++which', 3, 1, None, None, None, None, None, None), (u'which', u'which', 1, 2, None, None, None, None, None, None), (u'model++,++which', u'model++,++which', 3, 1, None, None, None, None, None, None), (u'we++can++use++for', u'we++can++use++for', 4, 1, None, None, None, None, None, None), (u'which++we++can++not++acept++.', u'which++we++can++not++acept++.', 6, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(++#shetlife', u'.++-(++\U0001f62b++:-(++#shetlif', 5, 1, None, None, None, None, None, None), (u'can++use++for++explain++a++big', u'can++use++for++explain++a++big', 6, 1, None, None, None, None, None, None), (u'\U0001f62b++:-(++#shetlife', u'\U0001f62b++:-(++#shetlif', 3, 1, None, None, None, None, None, None), (u'for++explain++a++big++things', u'for++explain++a++big++thing', 5, 1, None, None, None, None, None, None), (u'model', u'model', 1, 2, u'1', u'2', None, None, u'1', None), (u'but++a++big++explanation++.++right', u'but++a++big++explan++.++right', 6, 1, None, None, None, None, None, None), (u'what', u'what', 1, 1, None, None, None, None, None, None), (u'do++you++think++about', u'do++you++think++about', 4, 1, None, None, None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[2, 2, 1, "IGNOR"]', None, None, u'1', None), (u'it++?++1++\U0001f62b', u'it++?++1++\U0001f62b', 4, 1, None, None, None, None, None, None), (u'a++big', u'a++big', 2, 2, None, None, None, None, None, None), (u'1++\U0001f62b++1++.', u'1++\U0001f62b++1++.', 4, 1, None, None, None, None, None, None), (u'you++think', u'you++think', 2, 1, None, None, None, None, None, None), (u',++but++a++big++explanation++.', u',++but++a++big++explan++.', 6, 1, None, None, None, None, None, None), (u'what++do++you++think++about++it', u'what++do++you++think++about++it', 6, 1, None, None, None, None, None, None), (u'think++about++it++?++1++\U0001f62b', u'think++about++it++?++1++\U0001f62b', 6, 1, None, None, None, None, None, None), (u'but++you', u'but++you', 2, 4, u'[10, 6]', u'[15, 8]', u'[2, 2]', u'[4, 4]', u'4', u'2'), (u'but++you++\U0001f600++\U0001f308++\U0001f600', u'but++you++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 1, 2, 1, "IGNOR"]', u'[3, 2, 2, 1, "IGNOR"]', None, None, u'1', None), (u'.++but', u'.++but', 2, 3, None, None, None, None, None, None), (u'big++explanation++.++right++?++what', u'big++explan++.++right++?++what', 6, 1, None, None, None, None, None, None), (u'tiny++surprise++.++but', u'tini++surpris++.++but', 4, 1, None, None, None, None, None, None), (u'about++it++?++1++\U0001f62b++1', u'about++it++?++1++\U0001f62b++1', 6, 1, None, None, None, None, None, None), (u'you++think++about++it++?', u'you++think++about++it++?', 5, 1, None, None, None, None, None, None), (u'?++what++do', u'?++what++do', 3, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), (u'what++do++you', u'what++do++you', 3, 1, None, None, None, None, None, None), (u'but++a++big++explanation++.', u'but++a++big++explan++.', 5, 1, None, None, None, None, None, None), (u',++but++a', u',++but++a', 3, 1, None, None, None, None, None, None), (u'1', u'1', 1, 2, u'2', u'2', None, None, u'2', None), (u'model++,', u'model++,', 2, 2, None, None, None, None, None, None), (u'?++what++do++you++think++about', u'?++what++do++you++think++about', 6, 1, None, None, None, None, None, None), (u'what++do++you++think', u'what++do++you++think', 4, 1, None, None, None, None, None, None), (u'right++?++what++do', u'right++?++what++do', 4, 1, None, None, None, None, None, None), (u'what++do', u'what++do', 2, 1, None, None, None, None, None, None), (u'.++right++?++what', u'.++right++?++what', 4, 1, None, None, None, None, None, None), (u'.++but++you', u'.++but++you', 3, 2, None, None, None, None, None, None), (u'about++it++?++1', u'about++it++?++1', 4, 1, None, None, None, None, None, None), (u'tiny', u'tini', 1, 10, u'1', u'1', u'2', u'9', u'1', u'2'), (u'tiny++model', u'tini++model', 2, 2, None, None, None, None, None, None), (u'think++about', u'think++about', 2, 1, None, None, None, None, None, None), (u'surprise++.++but++you', u'surpris++.++but++you', 4, 1, None, None, None, None, None, None), (u'explanation++.++right++?++what', u'explan++.++right++?++what', 5, 1, None, None, None, None, None, None), (u'1++.++but++you++but', u'1++.++but++you++but', 5, 1, None, None, None, None, None, None), (u'model++,++but++a++big++explanation', u'model++,++but++a++big++explan', 6, 1, None, None, None, None, None, None), (u'?++1++\U0001f62b++1++.++but', u'?++1++\U0001f62b++1++.++but', 6, 1, None, None, None, None, None, None), (u'a++big++explanation', u'a++big++explan', 3, 1, None, None, None, None, None, None), (u'explanation++.++right++?++what++do', u'explan++.++right++?++what++do', 6, 1, None, None, None, None, None, None), (u'?++what', u'?++what', 2, 1, None, None, None, None, None, None), (u'right', u'right', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++but++you', u'you++but++you', 3, 2, u'[6, 6, "IGNOR"]', u'[8, 8, "IGNOR"]', None, None, u'2', None), (u'big++explanation++.++right++?', u'big++explan++.++right++?', 5, 1, None, None, None, None, None, None), (u'it++?', u'it++?', 2, 1, None, None, None, None, None, None), (u'what++do++you++think++about', u'what++do++you++think++about', 5, 1, None, None, None, None, None, None), (u'but++you++but++you++\U0001f600++\U0001f308', u'but++you++but++you++\U0001f600++\U0001f308', 6, 1, u'[5, 3, "IGNOR", "IGNOR", 1, 1]', u'[5, 4, "IGNOR", "IGNOR", 1, 1]', None, None, u'1', None), (u'\U0001f308++\U0001f600++\U0001f308', u'\U0001f308++\U0001f600++\U0001f308', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, u'1', None), (u'explanation++.++right', u'explan++.++right', 3, 1, None, None, None, None, None, None), (u'.', u'.', 1, 7, u'1', u'1', None, None, u'1', None), (u'you', u'you', 1, 8, u'7', u'9', u'2', u'4', u'7', u'2'), (u'surprise++.++but', u'surpris++.++but', 3, 1, None, None, None, None, None, None), (u'?', u'?', 1, 2, u'1', u'1', None, None, u'1', None), (u'explanation++.++right++?', u'explan++.++right++?', 4, 1, None, None, None, None, None, None), (u'it++?++1', u'it++?++1', 3, 1, None, None, None, None, None, None), (u'tiny++model++,++but', u'tini++model++,++but', 4, 1, None, None, None, None, None, None), (u'you++think++about++it++?++1', u'you++think++about++it++?++1', 6, 1, None, None, None, None, None, None), (u'but++you++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308', 4, 1, u'[3, 1, 1, 1]', u'[3, 2, 1, 1]', None, None, u'1', None), (u'but++a++big', u'but++a++big', 3, 1, None, None, None, None, None, None), (u'tiny++surprise++.++but++you++but', u'tini++surpris++.++but++you++but', 6, 1, None, None, None, None, None, None), (u'do++you++think++about++it', u'do++you++think++about++it', 5, 1, None, None, None, None, None, None), (u'big++explanation++.', u'big++explan++.', 3, 1, None, None, None, None, None, None), (u'think++about++it++?++1', u'think++about++it++?++1', 5, 1, None, None, None, None, None, None), (u'.++right', u'.++right', 2, 1, None, None, None, None, None, None), (u'explanation++.', u'explan++.', 2, 1, None, None, None, None, None, None), (u'but++you++but', u'but++you++but', 3, 2, u'[10, 4, "IGNOR"]', u'[15, 4, "IGNOR"]', u'[4, 2, "IGNOR"]', u'[10, 4, "IGNOR"]', u'2', u'2'), (u'.++but++you++but++you++\U0001f600', u'.++but++you++but++you++\U0001f600', 6, 1, None, None, None, None, None, None), (u'tiny++surprise', u'tini++surpris', 2, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, u'1', None), (u'model++,++but++a', u'model++,++but++a', 4, 1, None, None, None, None, None, None), (u'you++think++about', u'you++think++about', 3, 1, None, None, None, None, None, None), (u'?++what++do++you', u'?++what++do++you', 4, 1, None, None, None, None, None, None), (u'explanation', u'explan', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++but++you++\U0001f600++\U0001f308++\U0001f600', u'you++but++you++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[3, 3, "IGNOR", 2, 1, "IGNOR"]', u'[4, 3, "IGNOR", 2, 1, "IGNOR"]', None, None, u'1', None), (u'?++1', u'?++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'do++you++think++about++it++?', u'do++you++think++about++it++?', 6, 1, None, None, None, None, None, None), (u'do++you++think', u'do++you++think', 3, 1, None, None, None, None, None, None), (u'model++,++but', u'model++,++but', 3, 1, None, None, None, None, None, None), (u'tiny++model++,++but++a', u'tini++model++,++but++a', 5, 1, None, None, None, None, None, None), (u'.++but++you++but++you', u'.++but++you++but++you', 5, 2, None, None, None, None, None, None), (u'\U0001f62b++1++.++but', u'\U0001f62b++1++.++but', 4, 1, None, None, None, None, None, None), (u'right++?', u'right++?', 2, 1, None, None, None, None, None, None), (u'but++you++\U0001f600', u'but++you++\U0001f600', 3, 1, u'[3, 1, 1]', u'[3, 2, 1]', None, None, u'1', None), (u'model++,++but++a++big', u'model++,++but++a++big', 5, 1, None, None, None, None, None, None), (u'\U0001f62b++1++.++but++you++but', u'\U0001f62b++1++.++but++you++but', 6, 1, None, None, None, None, None, None), (u'tiny++surprise++.', u'tini++surpris++.', 3, 1, None, None, None, None, None, None), (u'?++what++do++you++think', u'?++what++do++you++think', 5, 1, None, None, None, None, None, None), (u'.++but++you++but', u'.++but++you++but', 4, 2, None, None, None, None, None, None), (u',++but++a++big++explanation', u',++but++a++big++explan', 5, 1, None, None, None, None, None, None), (u'\U0001f62b++1++.', u'\U0001f62b++1++.', 3, 1, None, None, None, None, None, None), (u'about', u'about', 1, 1, None, None, None, None, None, None), (u'it++?++1++\U0001f62b++1', u'it++?++1++\U0001f62b++1', 5, 1, None, None, None, None, None, None), (u'tiny++model++,++but++a++big', u'tini++model++,++but++a++big', 6, 1, None, None, None, None, None, None), (u'you++but', u'you++but', 2, 2, u'[4, 6]', u'[4, 8]', u'[2, 2]', u'[4, 6]', u'2', u'2'), (u'right++?++what', u'right++?++what', 3, 1, None, None, None, None, None, None), (u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), (u'but++you++but++you++\U0001f600', u'but++you++but++you++\U0001f600', 5, 1, u'[5, 3, "IGNOR", "IGNOR", 1]', u'[5, 4, "IGNOR", "IGNOR", 1]', None, None, u'1', None), (u'\U0001f62b++1++.++but++you', u'\U0001f62b++1++.++but++you', 5, 1, None, None, None, None, None, None), (u'surprise++.++but++you++but++you', u'surpris++.++but++you++but++you', 6, 1, None, None, None, None, None, None), (u'a++big++explanation++.++right', u'a++big++explan++.++right', 5, 1, None, None, None, None, None, None), (u'1++.++but', u'1++.++but', 3, 1, None, None, None, None, None, None), (u'you++but++you++\U0001f600++\U0001f308', u'you++but++you++\U0001f600++\U0001f308', 5, 1, u'[3, 3, "IGNOR", 1, 1]', u'[4, 3, "IGNOR", 1, 1]', None, None, u'1', None), (u'\U0001f62b++1', u'\U0001f62b++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'surprise++.', u'surpris++.', 2, 1, None, None, None, None, None, None), (u'tiny++model++,', u'tini++model++,', 3, 2, None, None, None, None, None, None), (u'right++?++what++do++you++think', u'right++?++what++do++you++think', 6, 1, None, None, None, None, None, None), (u'?++1++\U0001f62b', u'?++1++\U0001f62b', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[1, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[2, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, u'1', None), (u'you++but++you++\U0001f600', u'you++but++you++\U0001f600', 4, 1, u'[3, 3, "IGNOR", 1]', u'[4, 3, "IGNOR", 1]', None, None, u'1', None), (u'about++it++?', u'about++it++?', 3, 1, None, None, None, None, None, None), (u'think++about++it', u'think++about++it', 3, 1, None, None, None, None, None, None), (u'surprise++.++but++you++but', u'surpris++.++but++you++but', 5, 1, None, None, None, None, None, None), (u'about++it', u'about++it', 2, 1, None, None, None, None, None, None), (u'1++.++but++you', u'1++.++but++you', 4, 1, None, None, None, None, None, None), (u'but++you++but++you', u'but++you++but++you', 4, 2, u'[10, 6, "IGNOR", "IGNOR"]', u'[15, 8, "IGNOR", "IGNOR"]', None, None, u'2', None), (u'about++it++?++1++\U0001f62b', u'about++it++?++1++\U0001f62b', 5, 1, None, None, None, None, None, None), (u'.++right++?', u'.++right++?', 3, 1, None, None, None, None, None, None), (u'tiny++surprise++.++but++you', u'tini++surpris++.++but++you', 5, 1, None, None, None, None, None, None), (u'you++think++about++it', u'you++think++about++it', 4, 1, None, None, None, None, None, None), (u'do++you', u'do++you', 2, 1, None, None, None, None, None, None), (u'1++\U0001f62b', u'1++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'.++right++?++what++do', u'.++right++?++what++do', 5, 1, None, None, None, None, None, None), (u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 6, 1, u'[3, 1, 2, 2, "IGNOR", "IGNOR"]', u'[3, 2, 2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), (u'1++\U0001f62b++1', u'1++\U0001f62b++1', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, u'1', None), (u'big++explanation++.++right', u'big++explan++.++right', 4, 1, None, None, None, None, None, None), (u'it++?++1++\U0001f62b++1++.', u'it++?++1++\U0001f62b++1++.', 6, 1, None, None, None, None, None, None), (u'?++1++\U0001f62b++1++.', u'?++1++\U0001f62b++1++.', 5, 1, None, None, None, None, None, None), (u'you++\U0001f600', u'you++\U0001f600', 2, 1, u'[1, 1]', u'[2, 1]', None, None, u'1', None), (u'a', u'a', 1, 3, None, None, None, None, None, None), (u'1++\U0001f62b++1++.++but++you', u'1++\U0001f62b++1++.++but++you', 6, 1, None, None, None, None, None, None), (u'you++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[2, 1, 1]', None, None, u'1', None), (u'.++right++?++what++do++you', u'.++right++?++what++do++you', 6, 1, None, None, None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 5, 1, u'[1, 2, 2, "IGNOR", "IGNOR"]', u'[2, 2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), (u'think', u'think', 1, 1, None, None, None, None, None, None), (u'1++\U0001f62b++1++.++but', u'1++\U0001f62b++1++.++but', 5, 1, None, None, None, None, None, None), (u'think++about++it++?', u'think++about++it++?', 4, 1, None, None, None, None, None, None), (u'big', u'big', 1, 5, u'2', u'2', u'2', u'5', u'2', u'2'), (u'big++explanation', u'big++explan', 2, 1, None, None, None, None, None, None), (u'1++.++but++you++but++you', u'1++.++but++you++but++you', 6, 1, None, None, None, None, None, None), (u'right++?++what++do++you', u'right++?++what++do++you', 5, 1, None, None, None, None, None, None), (u'but++a++big++explanation', u'but++a++big++explan', 4, 1, None, None, None, None, None, None), (u'?++1++\U0001f62b++1', u'?++1++\U0001f62b++1', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[1, 2, 1, "IGNOR"]', None, None, u'1', None), (u'do', u'do', 1, 1, None, None, None, None, None, None), (u'a++big++explanation++.', u'a++big++explan++.', 4, 1, None, None, None, None, None, None), (u'a++big++explanation++.++right++?', u'a++big++explan++.++right++?', 6, 1, None, None, None, None, None, None), (u'but++a', u'but++a', 2, 1, None, None, None, None, None, None), (u'1++.', u'1++.', 2, 1, None, None, None, None, None, None), (u',++but++a++big', u',++but++a++big', 4, 1, None, None, None, None, None, None), (u'but++i++realy++liked', u'but++i++reali++like', 4, 1, None, None, None, None, None, None), (u'liked++it++:p++=)++\U0001f600++\U0001f308', u'like++it++:p++=)++\U0001f600++\U0001f308', 6, 1, None, None, None, None, None, None), (u'was++realy', u'was++reali', 2, 1, None, None, None, None, None, None), (u',++but++i++realy', u',++but++i++reali', 4, 1, None, None, None, None, None, None), (u'bad++surprise++for++me++\U0001f62b++,', u'bad++surpris++for++me++\U0001f62b++,', 6, 1, None, None, None, None, None, None), (u'i++realy++liked++it++:p', u'i++reali++like++it++:p', 5, 1, None, None, None, None, None, None), (u'it', u'it', 1, 5, None, None, None, None, None, None), (u'but', u'but', 1, 13, u'11', u'16', u'4', u'10', u'11', u'4'), (u'realy++liked', u'reali++like', 2, 1, None, None, None, None, None, None), (u':p++=)++\U0001f600++\U0001f308++\U0001f600', u':p++=)++\U0001f600++\U0001f308++\U0001f600', 5, 1, None, None, None, None, None, None), (u'realy++bad++surprise++for', u'reali++bad++surpris++for', 4, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,++but++i', u'me++\U0001f62b++,++but++i', 5, 1, None, None, None, None, None, None), (u'me', u'me', 1, 2, None, None, None, None, None, None), (u'was++realy++bad++surprise++for++me', u'was++reali++bad++surpris++for++me', 6, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,', u'me++\U0001f62b++,', 3, 1, None, None, None, None, None, None), (u'liked++it++:p++=)++\U0001f600', u'like++it++:p++=)++\U0001f600', 5, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but', u'\U0001f62b++,++but', 3, 1, None, None, None, None, None, None), (u'realy', u'reali', 1, 4, u'2', u'4', u'1', u'3', u'2', u'1'), (u'surprise++for++me++\U0001f62b', u'surpris++for++me++\U0001f62b', 4, 1, None, None, None, None, None, None), (u'i++realy++liked++it++:p++=)', u'i++reali++like++it++:p++=)', 6, 1, None, None, None, None, None, None), (u'\U0001f600', u'\U0001f600', 1, 5, u'4', u'4', None, None, u'4', None), (u'\U0001f308++\U0001f600', u'\U0001f308++\U0001f600', 2, 3, u'[2, 2]', u'[2, 2]', None, None, u'2', None), (u'=)', u'=)', 1, 1, u'1', u'1', None, None, u'1', None), (u':p', u':p', 1, 1, None, None, None, None, None, None), (u'i++realy++liked++it', u'i++reali++like++it', 4, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,++but', u'me++\U0001f62b++,++but', 4, 1, None, None, None, None, None, None), (u'it++was', u'it++was', 2, 2, None, None, None, None, None, None), (u'surprise++for++me', u'surpris++for++me', 3, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but++i++realy', u'\U0001f62b++,++but++i++reali', 5, 1, None, None, None, None, None, None), (u'=)++\U0001f600++\U0001f308', u'=)++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), (u',++but++i', u',++but++i', 3, 1, None, None, None, None, None, None), (u'it++:p++=)++\U0001f600', u'it++:p++=)++\U0001f600', 4, 1, None, None, None, None, None, None), (u'but++i++realy++liked++it++:p', u'but++i++reali++like++it++:p', 6, 1, None, None, None, None, None, None), (u'realy++liked++it++:p++=)', u'reali++like++it++:p++=)', 5, 1, None, None, None, None, None, None), (u'=)++\U0001f600++\U0001f308++\U0001f600', u'=)++\U0001f600++\U0001f308++\U0001f600', 4, 1, None, None, None, None, None, None), (u'liked++it', u'like++it', 2, 1, None, None, None, None, None, None), (u'it++:p++=)', u'it++:p++=)', 3, 1, None, None, None, None, None, None), (u'realy++bad++surprise++for++me', u'reali++bad++surpris++for++me', 5, 1, None, None, None, None, None, None), (u'\U0001f62b++,', u'\U0001f62b++,', 2, 1, None, None, None, None, None, None), (u'but++i++realy++liked++it', u'but++i++reali++like++it', 5, 1, None, None, None, None, None, None), (u'for++me', u'for++me', 2, 2, None, None, None, None, None, None), (u'\U0001f308', u'\U0001f308', 1, 3, u'3', u'3', None, None, u'3', None), (u'for++me++\U0001f62b', u'for++me++\U0001f62b', 3, 1, None, None, None, None, None, None), (u'but++i', u'but++i', 2, 1, None, None, None, None, None, None), (u'bad++surprise', u'bad++surpris', 2, 1, None, None, None, None, None, None), (u'i++realy++liked', u'i++reali++like', 3, 1, None, None, None, None, None, None), (u'bad++surprise++for++me', u'bad++surpris++for++me', 4, 1, None, None, None, None, None, None), (u'for++me++\U0001f62b++,++but', u'for++me++\U0001f62b++,++but', 5, 1, None, None, None, None, None, None), (u'realy++liked++it', u'reali++like++it', 3, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308', u'\U0001f600++\U0001f308', 2, 3, u'[3, 3]', u'[3, 3]', None, None, u'3', None), (u'it++:p', u'it++:p', 2, 1, None, None, None, None, None, None), (u'liked++it++:p', u'like++it++:p', 3, 1, None, None, None, None, None, None), (u'for', u'for', 1, 3, None, None, None, None, None, None), (u'for++me++\U0001f62b++,', u'for++me++\U0001f62b++,', 4, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600', 3, 3, u'[2, 1, "IGNOR"]', u'[3, 1, "IGNOR"]', None, None, u'1', None), (u'realy++bad++surprise', u'reali++bad++surpris', 3, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but++i++realy++liked', u'\U0001f62b++,++but++i++reali++like', 6, 1, None, None, None, None, None, None), (u'was++realy++bad++surprise', u'was++reali++bad++surpris', 4, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,++but++i++realy', u'me++\U0001f62b++,++but++i++reali', 6, 1, None, None, None, None, None, None), (u',', u',', 1, 4, None, None, None, None, None, None), (u',++but', u',++but', 2, 2, None, None, None, None, None, None), (u'it++:p++=)++\U0001f600++\U0001f308', u'it++:p++=)++\U0001f600++\U0001f308', 5, 1, None, None, None, None, None, None), (u'was++realy++bad++surprise++for', u'was++reali++bad++surpris++for', 5, 1, None, None, None, None, None, None), (u'=)++\U0001f600', u'=)++\U0001f600', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'bad++surprise++for++me++\U0001f62b', u'bad++surpris++for++me++\U0001f62b', 5, 1, None, None, None, None, None, None), (u':p++=)', u':p++=)', 2, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but++i', u'\U0001f62b++,++but++i', 4, 1, None, None, None, None, None, None), (u'realy++bad++surprise++for++me++\U0001f62b', u'reali++bad++surpris++for++me++\U0001f62b', 6, 1, None, None, None, None, None, None), (u':p++=)++\U0001f600', u':p++=)++\U0001f600', 3, 1, None, None, None, None, None, None), (u'me++\U0001f62b', u'me++\U0001f62b', 2, 1, None, None, None, None, None, None), (u'realy++liked++it++:p', u'reali++like++it++:p', 4, 1, None, None, None, None, None, None), (u'surprise', u'surpris', 1, 2, None, None, None, None, None, None), (u'it++was++realy++bad++surprise', u'it++was++reali++bad++surpris', 5, 1, None, None, None, None, None, None), (u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', 6, 1, None, None, None, None, None, None), (u'\U0001f62b', u'\U0001f62b', 1, 3, u'3', u'3', None, None, u'3', None), (u'but++i++realy', u'but++i++reali', 3, 1, None, None, None, None, None, None), (u'it++was++realy++bad++surprise++for', u'it++was++reali++bad++surpris++for', 6, 1, None, None, None, None, None, None), (u':p++=)++\U0001f600++\U0001f308', u':p++=)++\U0001f600++\U0001f308', 4, 1, None, None, None, None, None, None), (u'bad', u'bad', 1, 6, u'4', u'7', u'1', u'5', u'4', u'1'), (u'surprise++for++me++\U0001f62b++,', u'surpris++for++me++\U0001f62b++,', 5, 1, None, None, None, None, None, None), (u'surprise++for++me++\U0001f62b++,++but', u'surpris++for++me++\U0001f62b++,++but', 6, 1, None, None, None, None, None, None), (u'it++was++realy++bad', u'it++was++reali++bad', 4, 1, None, None, None, None, None, None), (u'it++was++realy', u'it++was++reali', 3, 1, None, None, None, None, None, None), (u'bad++surprise++for', u'bad++surpris++for', 3, 1, None, None, None, None, None, None), (u'liked++it++:p++=)', u'like++it++:p++=)', 4, 1, None, None, None, None, None, None), (u'i', u'i', 1, 2, None, None, None, None, None, None), (u'surprise++for', u'surpris++for', 2, 1, None, None, None, None, None, None), (u'realy++liked++it++:p++=)++\U0001f600', u'reali++like++it++:p++=)++\U0001f600', 6, 1, None, None, None, None, None, None), (u',++but++i++realy++liked', u',++but++i++reali++like', 5, 1, None, None, None, None, None, None), (u'realy++bad', u'reali++bad', 2, 1, None, None, None, None, None, None), (u'for++me++\U0001f62b++,++but++i', u'for++me++\U0001f62b++,++but++i', 6, 1, None, None, None, None, None, None), (u'was++realy++bad', u'was++reali++bad', 3, 1, None, None, None, None, None, None), (u'was', u'was', 1, 2, None, None, None, None, None, None), (u'liked', u'like', 1, 1, None, None, None, None, None, None), (u'i++realy', u'i++reali', 2, 1, None, None, None, None, None, None), (u',++but++i++realy++liked++it', u',++but++i++reali++like++it', 6, 1, None, None, None, None, None, None)]

        # right_baseline_freezed_not_full_repetativ = [(u'also++very++pity++for++me', u'also++veri++piti++for++me', 5, 1, u'[0, 2, 2, 0, 0]', u'[0, 4, 4, 0, 0]', u'[0, 1, 1, 0, 0]', u'[0, 3, 4, 0, 0]', None, None), (u'it++was++also++very', u'it++was++also++veri', 4, 1, u'[0, 0, 0, 2]', u'[0, 0, 0, 4]', u'[0, 0, 0, 1]', u'[0, 0, 0, 3]', None, None), (u'.++:-(++@real_trump++#shetlife', u'.++:-(++@real_trump++#shetlif', 4, 1, u'[1, 1, 0, 0]', u'[1, 1, 0, 0]', None, None, None, None), (u':-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u':-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 5, 1, u'[1, 0, 0, 0, 0]', u'[1, 0, 0, 0, 0]', None, None, None, None), (u'glad++to++se++you++-)', u'glad++to++se++you++-)', 5, 1, u'[1, 0, 1, 0, 1]', u'[1, 0, 1, 0, 1]', None, None, None, None), (u'me++.', u'me++.', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'.++:-(++@real_trump', u'.++:-(++@real_trump', 3, 1, u'[1, 1, 0]', u'[1, 1, 0]', None, None, None, None), (u'-)', u'-)', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++-)', u'you++-)', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'me++.++:-(', u'me++.++:-(', 3, 1, u'[0, 1, 1]', u'[0, 1, 1]', None, None, None, None), (u'.++:-(++@real_trump++#shetlife++#readytogo', u'.++:-(++@real_trump++#shetlif++#readytogo', 5, 1, u'[1, 1, 0, 0, 0]', u'[1, 1, 0, 0, 0]', None, None, None, None), (u'pity++for++me++.', u'piti++for++me++.', 4, 1, u'[2, 0, 0, 1]', u'[4, 0, 0, 1]', u'[1, 0, 0, 0]', u'[4, 0, 0, 0]', None, None), (u'for++me++.++:-(', u'for++me++.++:-(', 4, 1, u'[0, 0, 1, 1]', u'[0, 0, 1, 1]', None, None, None, None), (u'me++.++:-(++@real_trump++#shetlife++#readytogo', u'me++.++:-(++@real_trump++#shetlif++#readytogo', 6, 1, u'[0, 1, 1, 0, 0, 0]', u'[0, 1, 1, 0, 0, 0]', None, None, None, None), (u'it++was++also++very++pity', u'it++was++also++veri++piti', 5, 1, u'[0, 0, 0, 2, 2]', u'[0, 0, 0, 4, 4]', u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 3, 4]', None, None), (u'very++pity++for++me++.++:-(', u'veri++piti++for++me++.++:-(', 6, 1, u'[2, 2, 0, 0, 1, 1]', u'[4, 4, 0, 0, 1, 1]', u'[1, 1, 0, 0, 0, 0]', u'[3, 4, 0, 0, 0, 0]', None, None), (u'to++se++you++-)', u'to++se++you++-)', 4, 1, u'[0, 1, 0, 1]', u'[0, 1, 0, 1]', None, None, None, None), (u'it++was++also++very++pity++for', u'it++was++also++veri++piti++for', 6, 1, u'[0, 0, 0, 2, 2, 0]', u'[0, 0, 0, 4, 4, 0]', u'[0, 0, 0, 1, 1, 0]', u'[0, 0, 0, 3, 4, 0]', None, None), (u'very++pity++for', u'veri++piti++for', 3, 1, u'[2, 2, 0]', u'[4, 4, 0]', u'[1, 1, 0]', u'[3, 4, 0]', None, None), (u'se++you++-)', u'se++you++-)', 3, 1, u'[1, 0, 1]', u'[1, 0, 1]', None, None, None, None), (u'glad++to', u'glad++to', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'but++it++was++also++very', u'but++it++was++also++veri', 5, 1, u'[0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 4]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 3]', None, None), (u'for++me++.', u'for++me++.', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'pity++for++me++.++:-(', u'piti++for++me++.++:-(', 5, 1, u'[2, 0, 0, 1, 1]', u'[4, 0, 0, 1, 1]', u'[1, 0, 0, 0, 0]', u'[4, 0, 0, 0, 0]', None, None), (u'.++:-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u'.++:-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 6, 1, u'[1, 1, 0, 0, 0, 0]', u'[1, 1, 0, 0, 0, 0]', None, None, None, None), (u'pity', u'piti', 1, 4, u'2', u'4', u'1', u'4', u'2', u'1'), (u'me++.++:-(++@real_trump', u'me++.++:-(++@real_trump', 4, 1, u'[0, 1, 1, 0]', u'[0, 1, 1, 0]', None, None, None, None), (u'but++it++was++also++very++pity', u'but++it++was++also++veri++piti', 6, 1, u'[0, 0, 0, 0, 2, 2]', u'[0, 0, 0, 0, 4, 4]', u'[0, 0, 0, 0, 1, 1]', u'[0, 0, 0, 0, 3, 4]', None, None), (u'very++pity++for++me++.', u'veri++piti++for++me++.', 5, 1, u'[2, 2, 0, 0, 1]', u'[4, 4, 0, 0, 1]', u'[1, 1, 0, 0, 0]', u'[3, 4, 0, 0, 0]', None, None), (u'also++very++pity++for++me++.', u'also++veri++piti++for++me++.', 6, 1, u'[0, 2, 2, 0, 0, 1]', u'[0, 4, 4, 0, 0, 1]', u'[0, 1, 1, 0, 0, 0]', u'[0, 3, 4, 0, 0, 0]', None, None), (u'se++you', u'se++you', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'se', u'se', 1, 1, u'1', u'1', None, None, u'1', None), (u'for++me++.++:-(++@real_trump++#shetlife', u'for++me++.++:-(++@real_trump++#shetlif', 6, 1, u'[0, 0, 1, 1, 0, 0]', u'[0, 0, 1, 1, 0, 0]', None, None, None, None), (u'glad++to++se++you', u'glad++to++se++you', 4, 1, u'[1, 0, 1, 0]', u'[1, 0, 1, 0]', None, None, None, None), (u'very++pity++for++me', u'veri++piti++for++me', 4, 1, u'[2, 2, 0, 0]', u'[4, 4, 0, 0]', u'[1, 1, 0, 0]', u'[3, 4, 0, 0]', None, None), (u':-(++@real_trump', u':-(++@real_trump', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'pity++for++me++.++:-(++@real_trump', u'piti++for++me++.++:-(++@real_trump', 6, 1, u'[2, 0, 0, 1, 1, 0]', u'[4, 0, 0, 1, 1, 0]', u'[1, 0, 0, 0, 0, 0]', u'[4, 0, 0, 0, 0, 0]', None, None), (u'was++also++very++pity++for', u'was++also++veri++piti++for', 5, 1, u'[0, 0, 2, 2, 0]', u'[0, 0, 4, 4, 0]', u'[0, 0, 1, 1, 0]', u'[0, 0, 3, 4, 0]', None, None), (u'also++very', u'also++veri', 2, 1, u'[0, 2]', u'[0, 4]', u'[0, 1]', u'[0, 3]', None, None), (u'to++se', u'to++se', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'pity++for', u'piti++for', 2, 1, u'[2, 0]', u'[4, 0]', u'[1, 0]', u'[4, 0]', None, None), (u'to++se++you', u'to++se++you', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'for++me++.++:-(++@real_trump', u'for++me++.++:-(++@real_trump', 5, 1, u'[0, 0, 1, 1, 0]', u'[0, 0, 1, 1, 0]', None, None, None, None), (u'also++very++pity', u'also++veri++piti', 3, 1, u'[0, 2, 2]', u'[0, 4, 4]', u'[0, 1, 1]', u'[0, 3, 4]', None, None), (u'very', u'veri', 1, 3, u'2', u'4', u'1', u'3', u'2', u'1'), (u'was++also++very', u'was++also++veri', 3, 1, u'[0, 0, 2]', u'[0, 0, 4]', u'[0, 0, 1]', u'[0, 0, 3]', None, None), (u'pity++for++me', u'piti++for++me', 3, 1, u'[2, 0, 0]', u'[4, 0, 0]', u'[1, 0, 0]', u'[4, 0, 0]', None, None), (u'me++.++:-(++@real_trump++#shetlife', u'me++.++:-(++@real_trump++#shetlif', 5, 1, u'[0, 1, 1, 0, 0]', u'[0, 1, 1, 0, 0]', None, None, None, None), (u'very++pity', u'veri++piti', 2, 1, u'[2, 2]', u'[4, 4]', u'[1, 1]', u'[3, 4]', None, None), (u'was++also++very++pity++for++me', u'was++also++veri++piti++for++me', 6, 1, u'[0, 0, 2, 2, 0, 0]', u'[0, 0, 4, 4, 0, 0]', u'[0, 0, 1, 1, 0, 0]', u'[0, 0, 3, 4, 0, 0]', None, None), (u'also++very++pity++for', u'also++veri++piti++for', 4, 1, u'[0, 2, 2, 0]', u'[0, 4, 4, 0]', u'[0, 1, 1, 0]', u'[0, 3, 4, 0]', None, None), (u':-(++@real_trump++#shetlife', u':-(++@real_trump++#shetlif', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', None, None, None, None), (u'glad++to++se', u'glad++to++se', 3, 1, u'[1, 0, 1]', u'[1, 0, 1]', None, None, None, None), (u':-(++@real_trump++#shetlife++#readytogo', u':-(++@real_trump++#shetlif++#readytogo', 4, 1, u'[1, 0, 0, 0]', u'[1, 0, 0, 0]', None, None, None, None), (u'.++:-(', u'.++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'glad', u'glad', 1, 1, u'1', u'1', None, None, u'1', None), (u'.++but++it++was++also++very', u'.++but++it++was++also++veri', 6, 1, u'[0, 0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 0, 4]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 3]', None, None), (u'was++also++very++pity', u'was++also++veri++piti', 4, 1, u'[0, 0, 2, 2]', u'[0, 0, 4, 4]', u'[0, 0, 1, 1]', u'[0, 0, 3, 4]', None, None), (u'bad++news++,++which', u'bad++news++,++which', 4, 1, u'[4, 0, 0, 0]', u'[7, 0, 0, 0]', u'[1, 0, 0, 0]', u'[5, 0, 0, 0]', None, None), (u'tiny++model++,++which++we', u'tini++model++,++which++we', 5, 1, u'[0, 1, 0, 0, 0]', u'[0, 2, 0, 0, 0]', u'[1, 0, 0, 0, 0]', u'[6, 0, 0, 0, 0]', None, None), (u'acept++.++-(', u'acept++.++-(', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'not++acept++.++-(++\U0001f62b', u'not++acept++.++-(++\U0001f62b', 5, 1, u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 1, 1]', None, None, None, None), (u'tiny++model++,++which', u'tini++model++,++which', 4, 1, u'[0, 1, 0, 0]', u'[0, 2, 0, 0]', u'[1, 0, 0, 0]', u'[6, 0, 0, 0]', None, None), (u'a++bad++news++,', u'a++bad++news++,', 4, 1, u'[0, 4, 0, 0]', u'[0, 7, 0, 0]', u'[0, 1, 0, 0]', u'[0, 5, 0, 0]', None, None), (u'-(++\U0001f62b', u'-(++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 5, 1, u'[1, 1, 1, 0, 0]', u'[1, 1, 1, 0, 0]', u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 2, 0]', None, None), (u'explain++a++big', u'explain++a++big', 3, 1, u'[0, 0, 2]', u'[0, 0, 2]', u'[0, 0, 1]', u'[0, 0, 2]', None, None), (u'explain++a++big++things++.', u'explain++a++big++thing++.', 5, 1, u'[0, 0, 2, 0, 0]', u'[0, 0, 2, 0, 0]', u'[0, 0, 1, 0, 0]', u'[0, 0, 2, 0, 0]', None, None), (u'a++bad++news', u'a++bad++news', 3, 1, u'[0, 4, 0]', u'[0, 7, 0]', u'[0, 1, 0]', u'[0, 5, 0]', None, None), (u'bad++news++,++which++we', u'bad++news++,++which++we', 5, 1, u'[4, 0, 0, 0, 0]', u'[7, 0, 0, 0, 0]', u'[1, 0, 0, 0, 0]', u'[5, 0, 0, 0, 0]', None, None), (u'-(', u'-(', 1, 1, u'1', u'1', None, None, u'1', None), (u'bad++news++,++which++we++can', u'bad++news++,++which++we++can', 6, 1, u'[4, 0, 0, 0, 0, 0]', u'[7, 0, 0, 0, 0, 0]', u'[1, 0, 0, 0, 0, 0]', u'[5, 0, 0, 0, 0, 0]', None, None), (u'bad++news', u'bad++news', 2, 1, u'[4, 0]', u'[7, 0]', u'[1, 0]', u'[5, 0]', None, None), (u'a++bad++news++,++which', u'a++bad++news++,++which', 5, 1, u'[0, 4, 0, 0, 0]', u'[0, 7, 0, 0, 0]', u'[0, 1, 0, 0, 0]', u'[0, 5, 0, 0, 0]', None, None), (u'big++things++.', u'big++thing++.', 3, 1, u'[2, 0, 0]', u'[2, 0, 0]', u'[1, 0, 0]', u'[2, 0, 0]', None, None), (u'-(++\U0001f62b++:-(', u'-(++\U0001f62b++:-(', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, None, None), (u'model++,++which++we', u'model++,++which++we', 4, 1, u'[1, 0, 0, 0]', u'[2, 0, 0, 0]', None, None, None, None), (u'#shetlife', u'#shetlif', 1, 3, None, None, u'1', u'2', None, u'1'), (u'can++not++acept++.++-(++\U0001f62b', u'can++not++acept++.++-(++\U0001f62b', 6, 1, u'[0, 0, 0, 0, 1, 1]', u'[0, 0, 0, 0, 1, 1]', None, None, None, None), (u'big++things', u'big++thing', 2, 1, u'[2, 0]', u'[2, 0]', u'[1, 0]', u'[2, 0]', None, None), (u'acept++.++-(++\U0001f62b++:-(', u'acept++.++-(++\U0001f62b++:-(', 5, 1, u'[0, 0, 1, 1, 1]', u'[0, 0, 1, 1, 1]', None, None, None, None), (u'for++explain++a++big++things++.', u'for++explain++a++big++thing++.', 6, 1, u'[0, 0, 0, 2, 0, 0]', u'[0, 0, 0, 2, 0, 0]', u'[0, 0, 0, 1, 0, 0]', u'[0, 0, 0, 2, 0, 0]', None, None), (u'\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'\U0001f62b++:-(++#shetlif++http://www.noooo.com', 4, 1, u'[1, 1, 0, 0]', u'[1, 1, 0, 0]', u'[0, 0, 1, 0]', u'[0, 0, 2, 0]', None, None), (u'not++acept++.++-(', u'not++acept++.++-(', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u':-(++#shetlife', u':-(++#shetlif', 2, 1, u'[1, 0]', u'[1, 0]', u'[0, 1]', u'[0, 2]', None, None), (u'.++-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'.++-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 6, 1, u'[0, 1, 1, 1, 0, 0]', u'[0, 1, 1, 1, 0, 0]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 2, 0]', None, None), (u'a++big++things', u'a++big++thing', 3, 1, u'[0, 2, 0]', u'[0, 2, 0]', u'[0, 1, 0]', u'[0, 2, 0]', None, None), (u'.++-(', u'.++-(', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'a++bad', u'a++bad', 2, 1, u'[0, 4]', u'[0, 7]', u'[0, 1]', u'[0, 5]', None, None), (u'can++not++acept++.++-(', u'can++not++acept++.++-(', 5, 1, u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 1]', None, None, None, None), (u'a++big++things++.', u'a++big++thing++.', 4, 1, u'[0, 2, 0, 0]', u'[0, 2, 0, 0]', u'[0, 1, 0, 0]', u'[0, 2, 0, 0]', None, None), (u'-(++\U0001f62b++:-(++#shetlife', u'-(++\U0001f62b++:-(++#shetlif', 4, 1, u'[1, 1, 1, 0]', u'[1, 1, 1, 0]', u'[0, 0, 0, 1]', u'[0, 0, 0, 2]', None, None), (u'acept++.++-(++\U0001f62b', u'acept++.++-(++\U0001f62b', 4, 1, u'[0, 0, 1, 1]', u'[0, 0, 1, 1]', None, None, None, None), (u':-(', u':-(', 1, 2, u'2', u'2', None, None, u'2', None), (u':-(++#shetlife++http://www.noooo.com', u':-(++#shetlif++http://www.noooo.com', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', u'[0, 1, 0]', u'[0, 2, 0]', None, None), (u'explain++a++big++things', u'explain++a++big++thing', 4, 1, u'[0, 0, 2, 0]', u'[0, 0, 2, 0]', u'[0, 0, 1, 0]', u'[0, 0, 2, 0]', None, None), (u'tiny++model++,++which++we++can', u'tini++model++,++which++we++can', 6, 1, u'[0, 1, 0, 0, 0, 0]', u'[0, 2, 0, 0, 0, 0]', u'[1, 0, 0, 0, 0, 0]', u'[6, 0, 0, 0, 0, 0]', None, None), (u'acept++.++-(++\U0001f62b++:-(++#shetlife', u'acept++.++-(++\U0001f62b++:-(++#shetlif', 6, 1, u'[0, 0, 1, 1, 1, 0]', u'[0, 0, 1, 1, 1, 0]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 2]', None, None), (u'use++for++explain++a++big++things', u'use++for++explain++a++big++thing', 6, 1, u'[0, 0, 0, 0, 2, 0]', u'[0, 0, 0, 0, 2, 0]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 2, 0]', None, None), (u'use++for++explain++a++big', u'use++for++explain++a++big', 5, 1, u'[0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 2]', None, None), (u'model++,++which++we++can++use', u'model++,++which++we++can++use', 6, 1, u'[1, 0, 0, 0, 0, 0]', u'[2, 0, 0, 0, 0, 0]', None, None, None, None), (u'not++acept++.++-(++\U0001f62b++:-(', u'not++acept++.++-(++\U0001f62b++:-(', 6, 1, u'[0, 0, 0, 1, 1, 1]', u'[0, 0, 0, 1, 1, 1]', None, None, None, None), (u'model++,++which++we++can', u'model++,++which++we++can', 5, 1, u'[1, 0, 0, 0, 0]', u'[2, 0, 0, 0, 0]', None, None, None, None), (u'bad++news++,', u'bad++news++,', 3, 1, u'[4, 0, 0]', u'[7, 0, 0]', u'[1, 0, 0]', u'[5, 0, 0]', None, None), (u'.++-(++\U0001f62b++:-(', u'.++-(++\U0001f62b++:-(', 4, 1, u'[0, 1, 1, 1]', u'[0, 1, 1, 1]', None, None, None, None), (u'for++explain++a++big', u'for++explain++a++big', 4, 1, u'[0, 0, 0, 2]', u'[0, 0, 0, 2]', u'[0, 0, 0, 1]', u'[0, 0, 0, 2]', None, None), (u'a++bad++news++,++which++we', u'a++bad++news++,++which++we', 6, 1, u'[0, 4, 0, 0, 0, 0]', u'[0, 7, 0, 0, 0, 0]', u'[0, 1, 0, 0, 0, 0]', u'[0, 5, 0, 0, 0, 0]', None, None), (u'#shetlife++http://www.noooo.com', u'#shetlif++http://www.noooo.com', 2, 1, None, None, u'[1, 0]', u'[2, 0]', None, None), (u'\U0001f62b++:-(', u'\U0001f62b++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'.++-(++\U0001f62b', u'.++-(++\U0001f62b', 3, 1, u'[0, 1, 1]', u'[0, 1, 1]', None, None, None, None), (u'we++can++not++acept++.++-(', u'we++can++not++acept++.++-(', 6, 1, u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 1]', None, None, None, None), (u'model++,++which', u'model++,++which', 3, 1, u'[1, 0, 0]', u'[2, 0, 0]', None, None, None, None), (u'.++-(++\U0001f62b++:-(++#shetlife', u'.++-(++\U0001f62b++:-(++#shetlif', 5, 1, u'[0, 1, 1, 1, 0]', u'[0, 1, 1, 1, 0]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 2]', None, None), (u'can++use++for++explain++a++big', u'can++use++for++explain++a++big', 6, 1, u'[0, 0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 0, 2]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 2]', None, None), (u'\U0001f62b++:-(++#shetlife', u'\U0001f62b++:-(++#shetlif', 3, 1, u'[1, 1, 0]', u'[1, 1, 0]', u'[0, 0, 1]', u'[0, 0, 2]', None, None), (u'for++explain++a++big++things', u'for++explain++a++big++thing', 5, 1, u'[0, 0, 0, 2, 0]', u'[0, 0, 0, 2, 0]', u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 2, 0]', None, None), (u'model', u'model', 1, 2, u'1', u'2', None, None, u'1', None), (u'but++a++big++explanation++.++right', u'but++a++big++explan++.++right', 6, 1, u'[0, 0, 0, 1, 0, 1]', u'[0, 0, 0, 1, 0, 1]', u'[0, 0, 1, 0, 0, 0]', u'[0, 0, 3, 0, 0, 0]', None, None), (u'do++you++think++about', u'do++you++think++about', 4, 1, u'[0, 1, 0, 0]', u'[0, 1, 0, 0]', None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[2, 2, 1, "IGNOR"]', None, None, None, None), (u'it++?++1++\U0001f62b', u'it++?++1++\U0001f62b', 4, 1, u'[0, 1, 1, 1]', u'[0, 1, 1, 1]', None, None, None, None), (u'a++big', u'a++big', 2, 2, u'[0, 2]', u'[0, 2]', u'[0, 2]', u'[0, 5]', None, None), (u'1++\U0001f62b++1++.', u'1++\U0001f62b++1++.', 4, 1, u'[2, 1, "IGNOR", 0]', u'[2, 1, "IGNOR", 0]', None, None, None, None), (u'you++think', u'you++think', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u',++but++a++big++explanation++.', u',++but++a++big++explan++.', 6, 1, u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 1, 0, 0]', u'[0, 0, 0, 3, 0, 0]', None, None), (u'what++do++you++think++about++it', u'what++do++you++think++about++it', 6, 1, u'[0, 0, 1, 0, 0, 0]', u'[0, 0, 1, 0, 0, 0]', None, None, None, None), (u'think++about++it++?++1++\U0001f62b', u'think++about++it++?++1++\U0001f62b', 6, 1, u'[0, 0, 0, 1, 1, 1]', u'[0, 0, 0, 1, 1, 1]', None, None, None, None), (u'but++you', u'but++you', 2, 4, u'[10, 6]', u'[15, 8]', u'[4, 2]', u'[10, 4]', None, None), (u'but++you++\U0001f600++\U0001f308++\U0001f600', u'but++you++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 1, 2, 1, "IGNOR"]', u'[3, 2, 2, 1, "IGNOR"]', u'[1, 0, 0, 0, "IGNOR"]', u'[3, 0, 0, 0, "IGNOR"]', None, None), (u'.++but', u'.++but', 2, 3, u'[0, 4]', u'[0, 7]', u'[0, 2]', u'[0, 4]', None, None), (u'big++explanation++.++right++?++what', u'big++explan++.++right++?++what', 6, 1, u'[0, 1, 0, 1, 0, 0]', u'[0, 1, 0, 1, 0, 0]', u'[1, 0, 0, 0, 0, 0]', u'[3, 0, 0, 0, 0, 0]', None, None), (u'tiny++surprise++.++but', u'tini++surpris++.++but', 4, 1, u'[1, 0, 0, 2]', u'[1, 0, 0, 2]', u'[1, 0, 0, 1]', u'[3, 0, 0, 2]', None, None), (u'about++it++?++1++\U0001f62b++1', u'about++it++?++1++\U0001f62b++1', 6, 1, u'[0, 0, 1, 2, 1, "IGNOR"]', u'[0, 0, 1, 2, 1, "IGNOR"]', None, None, None, None), (u'you++think++about++it++?', u'you++think++about++it++?', 5, 1, u'[1, 0, 0, 0, 1]', u'[1, 0, 0, 0, 1]', None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, None, None), (u'what++do++you', u'what++do++you', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'but++a++big++explanation++.', u'but++a++big++explan++.', 5, 1, u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 1, 0]', u'[0, 0, 1, 0, 0]', u'[0, 0, 3, 0, 0]', None, None), (u'1', u'1', 1, 2, u'2', u'2', None, None, u'2', None), (u'model++,', u'model++,', 2, 2, u'[1, 0]', u'[2, 0]', None, None, None, None), (u'?++what++do++you++think++about', u'?++what++do++you++think++about', 6, 1, u'[0, 0, 0, 1, 0, 0]', u'[0, 0, 0, 1, 0, 0]', None, None, None, None), (u'what++do++you++think', u'what++do++you++think', 4, 1, u'[0, 0, 1, 0]', u'[0, 0, 1, 0]', None, None, None, None), (u'right++?++what++do', u'right++?++what++do', 4, 1, u'[1, 0, 0, 0]', u'[1, 0, 0, 0]', None, None, None, None), (u'.++right++?++what', u'.++right++?++what', 4, 1, u'[0, 1, 0, 0]', u'[0, 1, 0, 0]', None, None, None, None), (u'.++but++you', u'.++but++you', 3, 2, u'[0, 4, 4]', u'[0, 7, 4]', u'[0, 2, 2]', u'[0, 4, 4]', None, None), (u'about++it++?++1', u'about++it++?++1', 4, 1, u'[0, 0, 1, 1]', u'[0, 0, 1, 1]', None, None, None, None), (u'tiny', u'tini', 1, 10, u'1', u'1', u'2', u'9', u'1', u'2'), (u'tiny++model', u'tini++model', 2, 2, u'[0, 1]', u'[0, 2]', u'[1, 0]', u'[6, 0]', None, None), (u'surprise++.++but++you', u'surpris++.++but++you', 4, 1, u'[0, 0, 2, 2]', u'[0, 0, 2, 2]', u'[0, 0, 1, 1]', u'[0, 0, 2, 2]', None, None), (u'explanation++.++right++?++what', u'explan++.++right++?++what', 5, 1, u'[1, 0, 1, 0, 0]', u'[1, 0, 1, 0, 0]', None, None, None, None), (u'1++.++but++you++but', u'1++.++but++you++but', 5, 1, u'[1, 0, 5, 2, "IGNOR"]', u'[1, 0, 10, 2, "IGNOR"]', u'[0, 0, 2, 1, "IGNOR"]', u'[0, 0, 5, 2, "IGNOR"]', None, None), (u'model++,++but++a++big++explanation', u'model++,++but++a++big++explan', 6, 1, u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 3, 0]', None, None), (u'?++1++\U0001f62b++1++.++but', u'?++1++\U0001f62b++1++.++but', 6, 1, u'[1, 2, 1, "IGNOR", 0, 2]', u'[1, 2, 1, "IGNOR", 0, 5]', u'[0, 0, 0, "IGNOR", 0, 1]', u'[0, 0, 0, "IGNOR", 0, 2]', None, None), (u'a++big++explanation', u'a++big++explan', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', u'[0, 1, 0]', u'[0, 3, 0]', None, None), (u'explanation++.++right++?++what++do', u'explan++.++right++?++what++do', 6, 1, u'[1, 0, 1, 0, 0, 0]', u'[1, 0, 1, 0, 0, 0]', None, None, None, None), (u'right', u'right', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++but++you', u'you++but++you', 3, 2, u'[6, 6, "IGNOR"]', u'[8, 8, "IGNOR"]', u'[2, 2, "IGNOR"]', u'[4, 6, "IGNOR"]', None, None), (u'big++explanation++.++right++?', u'big++explan++.++right++?', 5, 1, u'[0, 1, 0, 1, 0]', u'[0, 1, 0, 1, 0]', u'[1, 0, 0, 0, 0]', u'[3, 0, 0, 0, 0]', None, None), (u'it++?', u'it++?', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'what++do++you++think++about', u'what++do++you++think++about', 5, 1, u'[0, 0, 1, 0, 0]', u'[0, 0, 1, 0, 0]', None, None, None, None), (u'but++you++but++you++\U0001f600++\U0001f308', u'but++you++but++you++\U0001f600++\U0001f308', 6, 1, u'[5, 3, "IGNOR", "IGNOR", 1, 1]', u'[5, 4, "IGNOR", "IGNOR", 1, 1]', u'[2, 1, "IGNOR", "IGNOR", 0, 0]', u'[5, 2, "IGNOR", "IGNOR", 0, 0]', None, None), (u'\U0001f308++\U0001f600++\U0001f308', u'\U0001f308++\U0001f600++\U0001f308', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, None, None), (u'explanation++.++right', u'explan++.++right', 3, 1, u'[1, 0, 1]', u'[1, 0, 1]', None, None, None, None), (u'.', u'.', 1, 7, u'1', u'1', None, None, u'1', None), (u'you', u'you', 1, 8, u'7', u'9', u'2', u'4', u'7', u'2'), (u'surprise++.++but', u'surpris++.++but', 3, 1, u'[0, 0, 2]', u'[0, 0, 2]', u'[0, 0, 1]', u'[0, 0, 2]', None, None), (u'?', u'?', 1, 2, u'1', u'1', None, None, u'1', None), (u'explanation++.++right++?', u'explan++.++right++?', 4, 1, u'[1, 0, 1, 0]', u'[1, 0, 1, 0]', None, None, None, None), (u'it++?++1', u'it++?++1', 3, 1, u'[0, 1, 1]', u'[0, 1, 1]', None, None, None, None), (u'you++think++about++it++?++1', u'you++think++about++it++?++1', 6, 1, u'[1, 0, 0, 0, 1, 1]', u'[1, 0, 0, 0, 1, 1]', None, None, None, None), (u'but++you++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308', 4, 1, u'[3, 1, 1, 1]', u'[3, 2, 1, 1]', u'[1, 0, 0, 0]', u'[3, 0, 0, 0]', None, None), (u'but++a++big', u'but++a++big', 3, 1, None, None, u'[0, 0, 1]', u'[0, 0, 3]', None, None), (u'tiny++surprise++.++but++you++but', u'tini++surpris++.++but++you++but', 6, 1, u'[1, 0, 0, 5, 2, "IGNOR"]', u'[1, 0, 0, 5, 2, "IGNOR"]', u'[1, 0, 0, 2, 1, "IGNOR"]', u'[3, 0, 0, 5, 2, "IGNOR"]', None, None), (u'do++you++think++about++it', u'do++you++think++about++it', 5, 1, u'[0, 1, 0, 0, 0]', u'[0, 1, 0, 0, 0]', None, None, None, None), (u'big++explanation++.', u'big++explan++.', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', u'[1, 0, 0]', u'[3, 0, 0]', None, None), (u'think++about++it++?++1', u'think++about++it++?++1', 5, 1, u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 1, 1]', None, None, None, None), (u'.++right', u'.++right', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'explanation++.', u'explan++.', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'but++you++but', u'but++you++but', 3, 2, u'[10, 4, "IGNOR"]', u'[15, 4, "IGNOR"]', u'[4, 2, "IGNOR"]', u'[10, 4, "IGNOR"]', None, None), (u'.++but++you++but++you++\U0001f600', u'.++but++you++but++you++\U0001f600', 6, 1, u'[0, 5, 3, "IGNOR", "IGNOR", 1]', u'[0, 5, 4, "IGNOR", "IGNOR", 1]', u'[0, 2, 1, "IGNOR", "IGNOR", 0]', u'[0, 5, 2, "IGNOR", "IGNOR", 0]', None, None), (u'tiny++surprise', u'tini++surpris', 2, 1, u'[1, 0]', u'[1, 0]', u'[1, 0]', u'[3, 0]', None, None), (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, None, None), (u'you++think++about', u'you++think++about', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', None, None, None, None), (u'?++what++do++you', u'?++what++do++you', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u'explanation', u'explan', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++but++you++\U0001f600++\U0001f308++\U0001f600', u'you++but++you++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[3, 3, "IGNOR", 2, 1, "IGNOR"]', u'[4, 3, "IGNOR", 2, 1, "IGNOR"]', u'[1, 1, "IGNOR", 0, 0, "IGNOR"]', u'[2, 3, "IGNOR", 0, 0, "IGNOR"]', None, None), (u'?++1', u'?++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'do++you++think++about++it++?', u'do++you++think++about++it++?', 6, 1, u'[0, 1, 0, 0, 0, 1]', u'[0, 1, 0, 0, 0, 1]', None, None, None, None), (u'do++you++think', u'do++you++think', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'.++but++you++but++you', u'.++but++you++but++you', 5, 2, u'[0, 10, 6, "IGNOR", "IGNOR"]', u'[0, 15, 8, "IGNOR", "IGNOR"]', u'[0, 4, 2, "IGNOR", "IGNOR"]', u'[0, 10, 4, "IGNOR", "IGNOR"]', None, None), (u'\U0001f62b++1++.++but', u'\U0001f62b++1++.++but', 4, 1, u'[1, 1, 0, 2]', u'[1, 1, 0, 5]', u'[0, 0, 0, 1]', u'[0, 0, 0, 2]', None, None), (u'right++?', u'right++?', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'but++you++\U0001f600', u'but++you++\U0001f600', 3, 1, u'[3, 1, 1]', u'[3, 2, 1]', u'[1, 0, 0]', u'[3, 0, 0]', None, None), (u'model++,++but++a++big', u'model++,++but++a++big', 5, 1, None, None, u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 3]', None, None), (u'\U0001f62b++1++.++but++you++but', u'\U0001f62b++1++.++but++you++but', 6, 1, u'[1, 1, 0, 5, 2, "IGNOR"]', u'[1, 1, 0, 10, 2, "IGNOR"]', u'[0, 0, 0, 2, 1, "IGNOR"]', u'[0, 0, 0, 5, 2, "IGNOR"]', None, None), (u'tiny++surprise++.', u'tini++surpris++.', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', u'[1, 0, 0]', u'[3, 0, 0]', None, None), (u'?++what++do++you++think', u'?++what++do++you++think', 5, 1, u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 1, 0]', None, None, None, None), (u'.++but++you++but', u'.++but++you++but', 4, 2, u'[0, 10, 4, "IGNOR"]', u'[0, 15, 4, "IGNOR"]', u'[0, 4, 2, "IGNOR"]', u'[0, 10, 4, "IGNOR"]', None, None), (u',++but++a++big++explanation', u',++but++a++big++explan', 5, 1, u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 3, 0]', None, None), (u'\U0001f62b++1++.', u'\U0001f62b++1++.', 3, 1, u'[1, 1, 0]', u'[1, 1, 0]', None, None, None, None), (u'it++?++1++\U0001f62b++1', u'it++?++1++\U0001f62b++1', 5, 1, u'[0, 1, 2, 1, "IGNOR"]', u'[0, 1, 2, 1, "IGNOR"]', None, None, None, None), (u'tiny++model++,++but++a++big', u'tini++model++,++but++a++big', 6, 1, None, None, u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 3]', None, None), (u'you++but', u'you++but', 2, 2, u'[4, 6]', u'[4, 8]', u'[2, 2]', u'[4, 6]', None, None), (u'right++?++what', u'right++?++what', 3, 1, u'[1, 0, 0]', u'[1, 0, 0]', None, None, None, None), (u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, None, None), (u'but++you++but++you++\U0001f600', u'but++you++but++you++\U0001f600', 5, 1, u'[5, 3, "IGNOR", "IGNOR", 1]', u'[5, 4, "IGNOR", "IGNOR", 1]', u'[2, 1, "IGNOR", "IGNOR", 0]', u'[5, 2, "IGNOR", "IGNOR", 0]', None, None), (u'\U0001f62b++1++.++but++you', u'\U0001f62b++1++.++but++you', 5, 1, u'[1, 1, 0, 2, 2]', u'[1, 1, 0, 5, 2]', u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 2, 2]', None, None), (u'surprise++.++but++you++but++you', u'surpris++.++but++you++but++you', 6, 1, u'[0, 0, 5, 3, "IGNOR", "IGNOR"]', u'[0, 0, 5, 4, "IGNOR", "IGNOR"]', u'[0, 0, 2, 1, "IGNOR", "IGNOR"]', u'[0, 0, 5, 2, "IGNOR", "IGNOR"]', None, None), (u'a++big++explanation++.++right', u'a++big++explan++.++right', 5, 1, u'[0, 0, 1, 0, 1]', u'[0, 0, 1, 0, 1]', u'[0, 1, 0, 0, 0]', u'[0, 3, 0, 0, 0]', None, None), (u'1++.++but', u'1++.++but', 3, 1, u'[1, 0, 2]', u'[1, 0, 5]', u'[0, 0, 1]', u'[0, 0, 2]', None, None), (u'you++but++you++\U0001f600++\U0001f308', u'you++but++you++\U0001f600++\U0001f308', 5, 1, u'[3, 3, "IGNOR", 1, 1]', u'[4, 3, "IGNOR", 1, 1]', u'[1, 1, "IGNOR", 0, 0]', u'[2, 3, "IGNOR", 0, 0]', None, None), (u'\U0001f62b++1', u'\U0001f62b++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'tiny++model++,', u'tini++model++,', 3, 2, u'[0, 1, 0]', u'[0, 2, 0]', u'[1, 0, 0]', u'[6, 0, 0]', None, None), (u'right++?++what++do++you++think', u'right++?++what++do++you++think', 6, 1, u'[1, 0, 0, 0, 1, 0]', u'[1, 0, 0, 0, 1, 0]', None, None, None, None), (u'?++1++\U0001f62b', u'?++1++\U0001f62b', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[1, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[2, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, None, None), (u'you++but++you++\U0001f600', u'you++but++you++\U0001f600', 4, 1, u'[3, 3, "IGNOR", 1]', u'[4, 3, "IGNOR", 1]', u'[1, 1, "IGNOR", 0]', u'[2, 3, "IGNOR", 0]', None, None), (u'about++it++?', u'about++it++?', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'surprise++.++but++you++but', u'surpris++.++but++you++but', 5, 1, u'[0, 0, 5, 2, "IGNOR"]', u'[0, 0, 5, 2, "IGNOR"]', u'[0, 0, 2, 1, "IGNOR"]', u'[0, 0, 5, 2, "IGNOR"]', None, None), (u'1++.++but++you', u'1++.++but++you', 4, 1, u'[1, 0, 2, 2]', u'[1, 0, 5, 2]', u'[0, 0, 1, 1]', u'[0, 0, 2, 2]', None, None), (u'but++you++but++you', u'but++you++but++you', 4, 2, u'[10, 6, "IGNOR", "IGNOR"]', u'[15, 8, "IGNOR", "IGNOR"]', u'[4, 2, "IGNOR", "IGNOR"]', u'[10, 4, "IGNOR", "IGNOR"]', None, None), (u'about++it++?++1++\U0001f62b', u'about++it++?++1++\U0001f62b', 5, 1, u'[0, 0, 1, 1, 1]', u'[0, 0, 1, 1, 1]', None, None, None, None), (u'.++right++?', u'.++right++?', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'tiny++surprise++.++but++you', u'tini++surpris++.++but++you', 5, 1, u'[1, 0, 0, 2, 2]', u'[1, 0, 0, 2, 2]', u'[1, 0, 0, 1, 1]', u'[3, 0, 0, 2, 2]', None, None), (u'you++think++about++it', u'you++think++about++it', 4, 1, u'[1, 0, 0, 0]', u'[1, 0, 0, 0]', None, None, None, None), (u'do++you', u'do++you', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'1++\U0001f62b', u'1++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'.++right++?++what++do', u'.++right++?++what++do', 5, 1, u'[0, 1, 0, 0, 0]', u'[0, 1, 0, 0, 0]', None, None, None, None), (u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 6, 1, u'[3, 1, 2, 2, "IGNOR", "IGNOR"]', u'[3, 2, 2, 2, "IGNOR", "IGNOR"]', u'[1, 0, 0, 0, "IGNOR", "IGNOR"]', u'[3, 0, 0, 0, "IGNOR", "IGNOR"]', None, None), (u'1++\U0001f62b++1', u'1++\U0001f62b++1', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, None, None), (u'big++explanation++.++right', u'big++explan++.++right', 4, 1, u'[0, 1, 0, 1]', u'[0, 1, 0, 1]', u'[1, 0, 0, 0]', u'[3, 0, 0, 0]', None, None), (u'it++?++1++\U0001f62b++1++.', u'it++?++1++\U0001f62b++1++.', 6, 1, u'[0, 1, 2, 1, "IGNOR", 0]', u'[0, 1, 2, 1, "IGNOR", 0]', None, None, None, None), (u'?++1++\U0001f62b++1++.', u'?++1++\U0001f62b++1++.', 5, 1, u'[1, 2, 1, "IGNOR", 0]', u'[1, 2, 1, "IGNOR", 0]', None, None, None, None), (u'you++\U0001f600', u'you++\U0001f600', 2, 1, u'[1, 1]', u'[2, 1]', None, None, None, None), (u'1++\U0001f62b++1++.++but++you', u'1++\U0001f62b++1++.++but++you', 6, 1, u'[2, 1, "IGNOR", 0, 2, 2]', u'[2, 1, "IGNOR", 0, 5, 2]', u'[0, 0, "IGNOR", 0, 1, 1]', u'[0, 0, "IGNOR", 0, 2, 2]', None, None), (u'you++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[2, 1, 1]', None, None, None, None), (u'.++right++?++what++do++you', u'.++right++?++what++do++you', 6, 1, u'[0, 1, 0, 0, 0, 1]', u'[0, 1, 0, 0, 0, 1]', None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 5, 1, u'[1, 2, 2, "IGNOR", "IGNOR"]', u'[2, 2, 2, "IGNOR", "IGNOR"]', None, None, None, None), (u'1++\U0001f62b++1++.++but', u'1++\U0001f62b++1++.++but', 5, 1, u'[2, 1, "IGNOR", 0, 2]', u'[2, 1, "IGNOR", 0, 5]', u'[0, 0, "IGNOR", 0, 1]', u'[0, 0, "IGNOR", 0, 2]', None, None), (u'think++about++it++?', u'think++about++it++?', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u'big', u'big', 1, 5, u'2', u'2', u'2', u'5', u'2', u'2'), (u'big++explanation', u'big++explan', 2, 1, u'[0, 1]', u'[0, 1]', u'[1, 0]', u'[3, 0]', None, None), (u'1++.++but++you++but++you', u'1++.++but++you++but++you', 6, 1, u'[1, 0, 5, 3, "IGNOR", "IGNOR"]', u'[1, 0, 10, 4, "IGNOR", "IGNOR"]', u'[0, 0, 2, 1, "IGNOR", "IGNOR"]', u'[0, 0, 5, 2, "IGNOR", "IGNOR"]', None, None), (u'right++?++what++do++you', u'right++?++what++do++you', 5, 1, u'[1, 0, 0, 0, 1]', u'[1, 0, 0, 0, 1]', None, None, None, None), (u'but++a++big++explanation', u'but++a++big++explan', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', u'[0, 0, 1, 0]', u'[0, 0, 3, 0]', None, None), (u'?++1++\U0001f62b++1', u'?++1++\U0001f62b++1', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[1, 2, 1, "IGNOR"]', None, None, None, None), (u'a++big++explanation++.', u'a++big++explan++.', 4, 1, u'[0, 0, 1, 0]', u'[0, 0, 1, 0]', u'[0, 1, 0, 0]', u'[0, 3, 0, 0]', None, None), (u'a++big++explanation++.++right++?', u'a++big++explan++.++right++?', 6, 1, u'[0, 0, 1, 0, 1, 0]', u'[0, 0, 1, 0, 1, 0]', u'[0, 1, 0, 0, 0, 0]', u'[0, 3, 0, 0, 0, 0]', None, None), (u'1++.', u'1++.', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u',++but++a++big', u',++but++a++big', 4, 1, None, None, u'[0, 0, 0, 1]', u'[0, 0, 0, 3]', None, None), (u'but++i++realy++liked', u'but++i++reali++like', 4, 1, u'[1, 0, 2, 0]', u'[1, 0, 4, 0]', u'[0, 0, 1, 0]', u'[0, 0, 3, 0]', None, None), (u'liked++it++:p++=)++\U0001f600++\U0001f308', u'like++it++:p++=)++\U0001f600++\U0001f308', 6, 1, u'[0, 0, 0, 1, 1, 1]', u'[0, 0, 0, 1, 1, 1]', None, None, None, None), (u',++but++i++realy', u',++but++i++reali', 4, 1, u'[0, 1, 0, 2]', u'[0, 1, 0, 4]', u'[0, 0, 0, 1]', u'[0, 0, 0, 3]', None, None), (u'bad++surprise++for++me++\U0001f62b++,', u'bad++surpris++for++me++\U0001f62b++,', 6, 1, u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 1, 0]', None, None, None, None), (u'i++realy++liked++it++:p', u'i++reali++like++it++:p', 5, 1, u'[0, 2, 0, 0, 0]', u'[0, 4, 0, 0, 0]', u'[0, 1, 0, 0, 0]', u'[0, 3, 0, 0, 0]', None, None), (u'but', u'but', 1, 13, u'11', u'16', u'4', u'10', u'11', u'4'), (u'realy++liked', u'reali++like', 2, 1, u'[2, 0]', u'[4, 0]', u'[1, 0]', u'[3, 0]', None, None), (u':p++=)++\U0001f600++\U0001f308++\U0001f600', u':p++=)++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[0, 1, 1, 1, "IGNOR"]', u'[0, 1, 1, 1, "IGNOR"]', None, None, None, None), (u'me++\U0001f62b++,++but++i', u'me++\U0001f62b++,++but++i', 5, 1, u'[0, 1, 0, 1, 0]', u'[0, 1, 0, 1, 0]', None, None, None, None), (u'me++\U0001f62b++,', u'me++\U0001f62b++,', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'liked++it++:p++=)++\U0001f600', u'like++it++:p++=)++\U0001f600', 5, 1, u'[0, 0, 0, 1, 1]', u'[0, 0, 0, 1, 1]', None, None, None, None), (u'\U0001f62b++,++but', u'\U0001f62b++,++but', 3, 1, u'[1, 0, 1]', u'[1, 0, 1]', None, None, None, None), (u'realy', u'reali', 1, 4, u'2', u'4', u'1', u'3', u'2', u'1'), (u'surprise++for++me++\U0001f62b', u'surpris++for++me++\U0001f62b', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u'i++realy++liked++it++:p++=)', u'i++reali++like++it++:p++=)', 6, 1, u'[0, 2, 0, 0, 0, 1]', u'[0, 4, 0, 0, 0, 1]', u'[0, 1, 0, 0, 0, 0]', u'[0, 3, 0, 0, 0, 0]', None, None), (u'\U0001f600', u'\U0001f600', 1, 5, u'4', u'4', None, None, u'4', None), (u'\U0001f308++\U0001f600', u'\U0001f308++\U0001f600', 2, 3, u'[3, 2]', u'[3, 2]', None, None, None, None), (u'=)', u'=)', 1, 1, u'1', u'1', None, None, u'1', None), (u'i++realy++liked++it', u'i++reali++like++it', 4, 1, u'[0, 2, 0, 0]', u'[0, 4, 0, 0]', u'[0, 1, 0, 0]', u'[0, 3, 0, 0]', None, None), (u'me++\U0001f62b++,++but', u'me++\U0001f62b++,++but', 4, 1, u'[0, 1, 0, 1]', u'[0, 1, 0, 1]', None, None, None, None), (u'\U0001f62b++,++but++i++realy', u'\U0001f62b++,++but++i++reali', 5, 1, u'[1, 0, 1, 0, 2]', u'[1, 0, 1, 0, 4]', u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 3]', None, None), (u'=)++\U0001f600++\U0001f308', u'=)++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, None, None), (u',++but++i', u',++but++i', 3, 1, u'[0, 1, 0]', u'[0, 1, 0]', None, None, None, None), (u'it++:p++=)++\U0001f600', u'it++:p++=)++\U0001f600', 4, 1, u'[0, 0, 1, 1]', u'[0, 0, 1, 1]', None, None, None, None), (u'but++i++realy++liked++it++:p', u'but++i++reali++like++it++:p', 6, 1, u'[1, 0, 2, 0, 0, 0]', u'[1, 0, 4, 0, 0, 0]', u'[0, 0, 1, 0, 0, 0]', u'[0, 0, 3, 0, 0, 0]', None, None), (u'realy++liked++it++:p++=)', u'reali++like++it++:p++=)', 5, 1, u'[2, 0, 0, 0, 1]', u'[4, 0, 0, 0, 1]', u'[1, 0, 0, 0, 0]', u'[3, 0, 0, 0, 0]', None, None), (u'=)++\U0001f600++\U0001f308++\U0001f600', u'=)++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[1, 1, 1, "IGNOR"]', u'[1, 1, 1, "IGNOR"]', None, None, None, None), (u'it++:p++=)', u'it++:p++=)', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'\U0001f62b++,', u'\U0001f62b++,', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'but++i++realy++liked++it', u'but++i++reali++like++it', 5, 1, u'[1, 0, 2, 0, 0]', u'[1, 0, 4, 0, 0]', u'[0, 0, 1, 0, 0]', u'[0, 0, 3, 0, 0]', None, None), (u'\U0001f308', u'\U0001f308', 1, 3, u'3', u'3', None, None, u'3', None), (u'for++me++\U0001f62b', u'for++me++\U0001f62b', 3, 1, u'[0, 0, 1]', u'[0, 0, 1]', None, None, None, None), (u'but++i', u'but++i', 2, 1, u'[1, 0]', u'[1, 0]', None, None, None, None), (u'i++realy++liked', u'i++reali++like', 3, 1, u'[0, 2, 0]', u'[0, 4, 0]', u'[0, 1, 0]', u'[0, 3, 0]', None, None), (u'for++me++\U0001f62b++,++but', u'for++me++\U0001f62b++,++but', 5, 1, u'[0, 0, 1, 0, 1]', u'[0, 0, 1, 0, 1]', None, None, None, None), (u'realy++liked++it', u'reali++like++it', 3, 1, u'[2, 0, 0]', u'[4, 0, 0]', u'[1, 0, 0]', u'[3, 0, 0]', None, None), (u'\U0001f600++\U0001f308', u'\U0001f600++\U0001f308', 2, 3, u'[3, 3]', u'[3, 3]', None, None, None, None), (u'for++me++\U0001f62b++,', u'for++me++\U0001f62b++,', 4, 1, u'[0, 0, 1, 0]', u'[0, 0, 1, 0]', None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600', 3, 3, u'[4, 3, "IGNOR"]', u'[5, 3, "IGNOR"]', None, None, None, None), (u'\U0001f62b++,++but++i++realy++liked', u'\U0001f62b++,++but++i++reali++like', 6, 1, u'[1, 0, 1, 0, 2, 0]', u'[1, 0, 1, 0, 4, 0]', u'[0, 0, 0, 0, 1, 0]', u'[0, 0, 0, 0, 3, 0]', None, None), (u'me++\U0001f62b++,++but++i++realy', u'me++\U0001f62b++,++but++i++reali', 6, 1, u'[0, 1, 0, 1, 0, 2]', u'[0, 1, 0, 1, 0, 4]', u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 3]', None, None), (u',++but', u',++but', 2, 2, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'it++:p++=)++\U0001f600++\U0001f308', u'it++:p++=)++\U0001f600++\U0001f308', 5, 1, u'[0, 0, 1, 1, 1]', u'[0, 0, 1, 1, 1]', None, None, None, None), (u'=)++\U0001f600', u'=)++\U0001f600', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None), (u'bad++surprise++for++me++\U0001f62b', u'bad++surpris++for++me++\U0001f62b', 5, 1, u'[0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 1]', None, None, None, None), (u':p++=)', u':p++=)', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'\U0001f62b++,++but++i', u'\U0001f62b++,++but++i', 4, 1, u'[1, 0, 1, 0]', u'[1, 0, 1, 0]', None, None, None, None), (u'realy++bad++surprise++for++me++\U0001f62b', u'reali++bad++surpris++for++me++\U0001f62b', 6, 1, u'[0, 0, 0, 0, 0, 1]', u'[0, 0, 0, 0, 0, 1]', None, None, None, None), (u':p++=)++\U0001f600', u':p++=)++\U0001f600', 3, 1, u'[0, 1, 1]', u'[0, 1, 1]', None, None, None, None), (u'me++\U0001f62b', u'me++\U0001f62b', 2, 1, u'[0, 1]', u'[0, 1]', None, None, None, None), (u'realy++liked++it++:p', u'reali++like++it++:p', 4, 1, u'[2, 0, 0, 0]', u'[4, 0, 0, 0]', u'[1, 0, 0, 0]', u'[3, 0, 0, 0]', None, None), (u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[0, 0, 1, 1, 1, "IGNOR"]', u'[0, 0, 1, 1, 1, "IGNOR"]', None, None, None, None), (u'\U0001f62b', u'\U0001f62b', 1, 3, u'3', u'3', None, None, u'3', None), (u'but++i++realy', u'but++i++reali', 3, 1, u'[1, 0, 2]', u'[1, 0, 4]', u'[0, 0, 1]', u'[0, 0, 3]', None, None), (u':p++=)++\U0001f600++\U0001f308', u':p++=)++\U0001f600++\U0001f308', 4, 1, u'[0, 1, 1, 1]', u'[0, 1, 1, 1]', None, None, None, None), (u'bad', u'bad', 1, 6, u'4', u'7', u'1', u'5', u'4', u'1'), (u'surprise++for++me++\U0001f62b++,', u'surpris++for++me++\U0001f62b++,', 5, 1, u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 1, 0]', None, None, None, None), (u'surprise++for++me++\U0001f62b++,++but', u'surpris++for++me++\U0001f62b++,++but', 6, 1, u'[0, 0, 0, 1, 0, 1]', u'[0, 0, 0, 1, 0, 1]', None, None, None, None), (u'liked++it++:p++=)', u'like++it++:p++=)', 4, 1, u'[0, 0, 0, 1]', u'[0, 0, 0, 1]', None, None, None, None), (u'realy++liked++it++:p++=)++\U0001f600', u'reali++like++it++:p++=)++\U0001f600', 6, 1, u'[2, 0, 0, 0, 1, 1]', u'[4, 0, 0, 0, 1, 1]', u'[1, 0, 0, 0, 0, 0]', u'[3, 0, 0, 0, 0, 0]', None, None), (u',++but++i++realy++liked', u',++but++i++reali++like', 5, 1, u'[0, 1, 0, 2, 0]', u'[0, 1, 0, 4, 0]', u'[0, 0, 0, 1, 0]', u'[0, 0, 0, 3, 0]', None, None), (u'for++me++\U0001f62b++,++but++i', u'for++me++\U0001f62b++,++but++i', 6, 1, u'[0, 0, 1, 0, 1, 0]', u'[0, 0, 1, 0, 1, 0]', None, None, None, None), (u'i++realy', u'i++reali', 2, 1, u'[0, 2]', u'[0, 4]', u'[0, 1]', u'[0, 3]', None, None), (u',++but++i++realy++liked++it', u',++but++i++reali++like++it', 6, 1, u'[0, 1, 0, 2, 0, 0]', u'[0, 1, 0, 4, 0, 0]', u'[0, 0, 0, 1, 0, 0]', u'[0, 0, 0, 3, 0, 0]', None, None)]
        # right_baseline_freezed_full_repetativ =  [(u'also++very++pity++for++me', u'also++veri++piti++for++me', 5, 1, None, None, None, None, None, None), (u'it++was++also++very', u'it++was++also++veri', 4, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump++#shetlife', u'.++:-(++@real_trump++#shetlif', 4, 1, None, None, None, None, None, None), (u':-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u':-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 5, 1, None, None, None, None, None, None), (u'glad++to++se++you++-)', u'glad++to++se++you++-)', 5, 1, None, None, None, None, None, None), (u'me++.', u'me++.', 2, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump', u'.++:-(++@real_trump', 3, 1, None, None, None, None, None, None), (u'-)', u'-)', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++-)', u'you++-)', 2, 1, None, None, None, None, None, None), (u'me++.++:-(', u'me++.++:-(', 3, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump++#shetlife++#readytogo', u'.++:-(++@real_trump++#shetlif++#readytogo', 5, 1, None, None, None, None, None, None), (u'pity++for++me++.', u'piti++for++me++.', 4, 1, None, None, None, None, None, None), (u'for++me++.++:-(', u'for++me++.++:-(', 4, 1, None, None, None, None, None, None), (u'me++.++:-(++@real_trump++#shetlife++#readytogo', u'me++.++:-(++@real_trump++#shetlif++#readytogo', 6, 1, None, None, None, None, None, None), (u'it++was++also++very++pity', u'it++was++also++veri++piti', 5, 1, None, None, None, None, None, None), (u'very++pity++for++me++.++:-(', u'veri++piti++for++me++.++:-(', 6, 1, None, None, None, None, None, None), (u'to++se++you++-)', u'to++se++you++-)', 4, 1, None, None, None, None, None, None), (u'it++was++also++very++pity++for', u'it++was++also++veri++piti++for', 6, 1, None, None, None, None, None, None), (u'very++pity++for', u'veri++piti++for', 3, 1, None, None, None, None, None, None), (u'se++you++-)', u'se++you++-)', 3, 1, None, None, None, None, None, None), (u'glad++to', u'glad++to', 2, 1, None, None, None, None, None, None), (u'but++it++was++also++very', u'but++it++was++also++veri', 5, 1, None, None, None, None, None, None), (u'for++me++.', u'for++me++.', 3, 1, None, None, None, None, None, None), (u'pity++for++me++.++:-(', u'piti++for++me++.++:-(', 5, 1, None, None, None, None, None, None), (u'.++:-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u'.++:-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 6, 1, None, None, None, None, None, None), (u'pity', u'piti', 1, 4, u'2', u'4', u'1', u'4', u'2', u'1'), (u'me++.++:-(++@real_trump', u'me++.++:-(++@real_trump', 4, 1, None, None, None, None, None, None), (u'but++it++was++also++very++pity', u'but++it++was++also++veri++piti', 6, 1, None, None, None, None, None, None), (u'very++pity++for++me++.', u'veri++piti++for++me++.', 5, 1, None, None, None, None, None, None), (u'also++very++pity++for++me++.', u'also++veri++piti++for++me++.', 6, 1, None, None, None, None, None, None), (u'se++you', u'se++you', 2, 1, None, None, None, None, None, None), (u'se', u'se', 1, 1, u'1', u'1', None, None, u'1', None), (u'for++me++.++:-(++@real_trump++#shetlife', u'for++me++.++:-(++@real_trump++#shetlif', 6, 1, None, None, None, None, None, None), (u'glad++to++se++you', u'glad++to++se++you', 4, 1, None, None, None, None, None, None), (u'very++pity++for++me', u'veri++piti++for++me', 4, 1, None, None, None, None, None, None), (u':-(++@real_trump', u':-(++@real_trump', 2, 1, None, None, None, None, None, None), (u'pity++for++me++.++:-(++@real_trump', u'piti++for++me++.++:-(++@real_trump', 6, 1, None, None, None, None, None, None), (u'was++also++very++pity++for', u'was++also++veri++piti++for', 5, 1, None, None, None, None, None, None), (u'also++very', u'also++veri', 2, 1, None, None, None, None, None, None), (u'to++se', u'to++se', 2, 1, None, None, None, None, None, None), (u'pity++for', u'piti++for', 2, 1, None, None, None, None, None, None), (u'to++se++you', u'to++se++you', 3, 1, None, None, None, None, None, None), (u'for++me++.++:-(++@real_trump', u'for++me++.++:-(++@real_trump', 5, 1, None, None, None, None, None, None), (u'also++very++pity', u'also++veri++piti', 3, 1, None, None, None, None, None, None), (u'very', u'veri', 1, 3, u'2', u'4', u'1', u'3', u'2', u'1'), (u'was++also++very', u'was++also++veri', 3, 1, None, None, None, None, None, None), (u'pity++for++me', u'piti++for++me', 3, 1, None, None, None, None, None, None), (u'me++.++:-(++@real_trump++#shetlife', u'me++.++:-(++@real_trump++#shetlif', 5, 1, None, None, None, None, None, None), (u'very++pity', u'veri++piti', 2, 1, u'[2, 2]', u'[4, 4]', u'[1, 1]', u'[3, 4]', u'1', u'1'), (u'was++also++very++pity++for++me', u'was++also++veri++piti++for++me', 6, 1, None, None, None, None, None, None), (u'also++very++pity++for', u'also++veri++piti++for', 4, 1, None, None, None, None, None, None), (u':-(++@real_trump++#shetlife', u':-(++@real_trump++#shetlif', 3, 1, None, None, None, None, None, None), (u'glad++to++se', u'glad++to++se', 3, 1, None, None, None, None, None, None), (u':-(++@real_trump++#shetlife++#readytogo', u':-(++@real_trump++#shetlif++#readytogo', 4, 1, None, None, None, None, None, None), (u'.++:-(', u'.++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'glad', u'glad', 1, 1, u'1', u'1', None, None, u'1', None), (u'.++but++it++was++also++very', u'.++but++it++was++also++veri', 6, 1, None, None, None, None, None, None), (u'was++also++very++pity', u'was++also++veri++piti', 4, 1, None, None, None, None, None, None), (u'bad++news++,++which', u'bad++news++,++which', 4, 1, None, None, None, None, None, None), (u'tiny++model++,++which++we', u'tini++model++,++which++we', 5, 1, None, None, None, None, None, None), (u'acept++.++-(', u'acept++.++-(', 3, 1, None, None, None, None, None, None), (u'not++acept++.++-(++\U0001f62b', u'not++acept++.++-(++\U0001f62b', 5, 1, None, None, None, None, None, None), (u'tiny++model++,++which', u'tini++model++,++which', 4, 1, None, None, None, None, None, None), (u'a++bad++news++,', u'a++bad++news++,', 4, 1, None, None, None, None, None, None), (u'-(++\U0001f62b', u'-(++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 5, 1, None, None, None, None, None, None), (u'explain++a++big', u'explain++a++big', 3, 1, None, None, None, None, None, None), (u'explain++a++big++things++.', u'explain++a++big++thing++.', 5, 1, None, None, None, None, None, None), (u'a++bad++news', u'a++bad++news', 3, 1, None, None, None, None, None, None), (u'bad++news++,++which++we', u'bad++news++,++which++we', 5, 1, None, None, None, None, None, None), (u'-(', u'-(', 1, 1, u'1', u'1', None, None, u'1', None), (u'bad++news++,++which++we++can', u'bad++news++,++which++we++can', 6, 1, None, None, None, None, None, None), (u'bad++news', u'bad++news', 2, 1, None, None, None, None, None, None), (u'a++bad++news++,++which', u'a++bad++news++,++which', 5, 1, None, None, None, None, None, None), (u'big++things++.', u'big++thing++.', 3, 1, None, None, None, None, None, None), (u'-(++\U0001f62b++:-(', u'-(++\U0001f62b++:-(', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), (u'model++,++which++we', u'model++,++which++we', 4, 1, None, None, None, None, None, None), (u'#shetlife', u'#shetlif', 1, 3, None, None, u'1', u'2', None, u'1'), (u'can++not++acept++.++-(++\U0001f62b', u'can++not++acept++.++-(++\U0001f62b', 6, 1, None, None, None, None, None, None), (u'big++things', u'big++thing', 2, 1, None, None, None, None, None, None), (u'acept++.++-(++\U0001f62b++:-(', u'acept++.++-(++\U0001f62b++:-(', 5, 1, None, None, None, None, None, None), (u'for++explain++a++big++things++.', u'for++explain++a++big++thing++.', 6, 1, None, None, None, None, None, None), (u'\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'\U0001f62b++:-(++#shetlif++http://www.noooo.com', 4, 1, None, None, None, None, None, None), (u'not++acept++.++-(', u'not++acept++.++-(', 4, 1, None, None, None, None, None, None), (u':-(++#shetlife', u':-(++#shetlif', 2, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'.++-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 6, 1, None, None, None, None, None, None), (u'a++big++things', u'a++big++thing', 3, 1, None, None, None, None, None, None), (u'.++-(', u'.++-(', 2, 1, None, None, None, None, None, None), (u'a++bad', u'a++bad', 2, 1, None, None, None, None, None, None), (u'can++not++acept++.++-(', u'can++not++acept++.++-(', 5, 1, None, None, None, None, None, None), (u'a++big++things++.', u'a++big++thing++.', 4, 1, None, None, None, None, None, None), (u'-(++\U0001f62b++:-(++#shetlife', u'-(++\U0001f62b++:-(++#shetlif', 4, 1, None, None, None, None, None, None), (u'acept++.++-(++\U0001f62b', u'acept++.++-(++\U0001f62b', 4, 1, None, None, None, None, None, None), (u':-(', u':-(', 1, 2, u'2', u'2', None, None, u'2', None), (u':-(++#shetlife++http://www.noooo.com', u':-(++#shetlif++http://www.noooo.com', 3, 1, None, None, None, None, None, None), (u'explain++a++big++things', u'explain++a++big++thing', 4, 1, None, None, None, None, None, None), (u'tiny++model++,++which++we++can', u'tini++model++,++which++we++can', 6, 1, None, None, None, None, None, None), (u'acept++.++-(++\U0001f62b++:-(++#shetlife', u'acept++.++-(++\U0001f62b++:-(++#shetlif', 6, 1, None, None, None, None, None, None), (u'use++for++explain++a++big++things', u'use++for++explain++a++big++thing', 6, 1, None, None, None, None, None, None), (u'use++for++explain++a++big', u'use++for++explain++a++big', 5, 1, None, None, None, None, None, None), (u'model++,++which++we++can++use', u'model++,++which++we++can++use', 6, 1, None, None, None, None, None, None), (u'not++acept++.++-(++\U0001f62b++:-(', u'not++acept++.++-(++\U0001f62b++:-(', 6, 1, None, None, None, None, None, None), (u'model++,++which++we++can', u'model++,++which++we++can', 5, 1, None, None, None, None, None, None), (u'bad++news++,', u'bad++news++,', 3, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(', u'.++-(++\U0001f62b++:-(', 4, 1, None, None, None, None, None, None), (u'for++explain++a++big', u'for++explain++a++big', 4, 1, None, None, None, None, None, None), (u'a++bad++news++,++which++we', u'a++bad++news++,++which++we', 6, 1, None, None, None, None, None, None), (u'#shetlife++http://www.noooo.com', u'#shetlif++http://www.noooo.com', 2, 1, None, None, None, None, None, None), (u'\U0001f62b++:-(', u'\U0001f62b++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'.++-(++\U0001f62b', u'.++-(++\U0001f62b', 3, 1, None, None, None, None, None, None), (u'we++can++not++acept++.++-(', u'we++can++not++acept++.++-(', 6, 1, None, None, None, None, None, None), (u'model++,++which', u'model++,++which', 3, 1, None, None, None, None, None, None), (u'.++-(++\U0001f62b++:-(++#shetlife', u'.++-(++\U0001f62b++:-(++#shetlif', 5, 1, None, None, None, None, None, None), (u'can++use++for++explain++a++big', u'can++use++for++explain++a++big', 6, 1, None, None, None, None, None, None), (u'\U0001f62b++:-(++#shetlife', u'\U0001f62b++:-(++#shetlif', 3, 1, None, None, None, None, None, None), (u'for++explain++a++big++things', u'for++explain++a++big++thing', 5, 1, None, None, None, None, None, None), (u'model', u'model', 1, 2, u'1', u'2', None, None, u'1', None), (u'but++a++big++explanation++.++right', u'but++a++big++explan++.++right', 6, 1, None, None, None, None, None, None), (u'do++you++think++about', u'do++you++think++about', 4, 1, None, None, None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[2, 2, 1, "IGNOR"]', None, None, u'1', None), (u'it++?++1++\U0001f62b', u'it++?++1++\U0001f62b', 4, 1, None, None, None, None, None, None), (u'a++big', u'a++big', 2, 2, None, None, None, None, None, None), (u'1++\U0001f62b++1++.', u'1++\U0001f62b++1++.', 4, 1, None, None, None, None, None, None), (u'you++think', u'you++think', 2, 1, None, None, None, None, None, None), (u',++but++a++big++explanation++.', u',++but++a++big++explan++.', 6, 1, None, None, None, None, None, None), (u'what++do++you++think++about++it', u'what++do++you++think++about++it', 6, 1, None, None, None, None, None, None), (u'think++about++it++?++1++\U0001f62b', u'think++about++it++?++1++\U0001f62b', 6, 1, None, None, None, None, None, None), (u'but++you', u'but++you', 2, 4, u'[10, 6]', u'[15, 8]', u'[2, 2]', u'[4, 4]', u'4', u'2'), (u'but++you++\U0001f600++\U0001f308++\U0001f600', u'but++you++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 1, 2, 1, "IGNOR"]', u'[3, 2, 2, 1, "IGNOR"]', None, None, u'1', None), (u'.++but', u'.++but', 2, 3, None, None, None, None, None, None), (u'big++explanation++.++right++?++what', u'big++explan++.++right++?++what', 6, 1, None, None, None, None, None, None), (u'tiny++surprise++.++but', u'tini++surpris++.++but', 4, 1, None, None, None, None, None, None), (u'about++it++?++1++\U0001f62b++1', u'about++it++?++1++\U0001f62b++1', 6, 1, None, None, None, None, None, None), (u'you++think++about++it++?', u'you++think++about++it++?', 5, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), (u'what++do++you', u'what++do++you', 3, 1, None, None, None, None, None, None), (u'but++a++big++explanation++.', u'but++a++big++explan++.', 5, 1, None, None, None, None, None, None), (u'1', u'1', 1, 2, u'2', u'2', None, None, u'2', None), (u'model++,', u'model++,', 2, 2, None, None, None, None, None, None), (u'?++what++do++you++think++about', u'?++what++do++you++think++about', 6, 1, None, None, None, None, None, None), (u'what++do++you++think', u'what++do++you++think', 4, 1, None, None, None, None, None, None), (u'right++?++what++do', u'right++?++what++do', 4, 1, None, None, None, None, None, None), (u'.++right++?++what', u'.++right++?++what', 4, 1, None, None, None, None, None, None), (u'.++but++you', u'.++but++you', 3, 2, None, None, None, None, None, None), (u'about++it++?++1', u'about++it++?++1', 4, 1, None, None, None, None, None, None), (u'tiny', u'tini', 1, 10, u'1', u'1', u'2', u'9', u'1', u'2'), (u'tiny++model', u'tini++model', 2, 2, None, None, None, None, None, None), (u'surprise++.++but++you', u'surpris++.++but++you', 4, 1, None, None, None, None, None, None), (u'explanation++.++right++?++what', u'explan++.++right++?++what', 5, 1, None, None, None, None, None, None), (u'1++.++but++you++but', u'1++.++but++you++but', 5, 1, None, None, None, None, None, None), (u'model++,++but++a++big++explanation', u'model++,++but++a++big++explan', 6, 1, None, None, None, None, None, None), (u'?++1++\U0001f62b++1++.++but', u'?++1++\U0001f62b++1++.++but', 6, 1, None, None, None, None, None, None), (u'a++big++explanation', u'a++big++explan', 3, 1, None, None, None, None, None, None), (u'explanation++.++right++?++what++do', u'explan++.++right++?++what++do', 6, 1, None, None, None, None, None, None), (u'right', u'right', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++but++you', u'you++but++you', 3, 2, u'[6, 6, "IGNOR"]', u'[8, 8, "IGNOR"]', None, None, u'2', None), (u'big++explanation++.++right++?', u'big++explan++.++right++?', 5, 1, None, None, None, None, None, None), (u'it++?', u'it++?', 2, 1, None, None, None, None, None, None), (u'what++do++you++think++about', u'what++do++you++think++about', 5, 1, None, None, None, None, None, None), (u'but++you++but++you++\U0001f600++\U0001f308', u'but++you++but++you++\U0001f600++\U0001f308', 6, 1, u'[5, 3, "IGNOR", "IGNOR", 1, 1]', u'[5, 4, "IGNOR", "IGNOR", 1, 1]', None, None, u'1', None), (u'\U0001f308++\U0001f600++\U0001f308', u'\U0001f308++\U0001f600++\U0001f308', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, u'1', None), (u'explanation++.++right', u'explan++.++right', 3, 1, None, None, None, None, None, None), (u'.', u'.', 1, 7, u'1', u'1', None, None, u'1', None), (u'you', u'you', 1, 8, u'7', u'9', u'2', u'4', u'7', u'2'), (u'surprise++.++but', u'surpris++.++but', 3, 1, None, None, None, None, None, None), (u'?', u'?', 1, 2, u'1', u'1', None, None, u'1', None), (u'explanation++.++right++?', u'explan++.++right++?', 4, 1, None, None, None, None, None, None), (u'it++?++1', u'it++?++1', 3, 1, None, None, None, None, None, None), (u'you++think++about++it++?++1', u'you++think++about++it++?++1', 6, 1, None, None, None, None, None, None), (u'but++you++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308', 4, 1, u'[3, 1, 1, 1]', u'[3, 2, 1, 1]', None, None, u'1', None), (u'but++a++big', u'but++a++big', 3, 1, None, None, None, None, None, None), (u'tiny++surprise++.++but++you++but', u'tini++surpris++.++but++you++but', 6, 1, None, None, None, None, None, None), (u'do++you++think++about++it', u'do++you++think++about++it', 5, 1, None, None, None, None, None, None), (u'big++explanation++.', u'big++explan++.', 3, 1, None, None, None, None, None, None), (u'think++about++it++?++1', u'think++about++it++?++1', 5, 1, None, None, None, None, None, None), (u'.++right', u'.++right', 2, 1, None, None, None, None, None, None), (u'explanation++.', u'explan++.', 2, 1, None, None, None, None, None, None), (u'but++you++but', u'but++you++but', 3, 2, u'[10, 4, "IGNOR"]', u'[15, 4, "IGNOR"]', u'[4, 2, "IGNOR"]', u'[10, 4, "IGNOR"]', u'2', u'2'), (u'.++but++you++but++you++\U0001f600', u'.++but++you++but++you++\U0001f600', 6, 1, None, None, None, None, None, None), (u'tiny++surprise', u'tini++surpris', 2, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, u'1', None), (u'you++think++about', u'you++think++about', 3, 1, None, None, None, None, None, None), (u'?++what++do++you', u'?++what++do++you', 4, 1, None, None, None, None, None, None), (u'explanation', u'explan', 1, 1, u'1', u'1', None, None, u'1', None), (u'you++but++you++\U0001f600++\U0001f308++\U0001f600', u'you++but++you++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[3, 3, "IGNOR", 2, 1, "IGNOR"]', u'[4, 3, "IGNOR", 2, 1, "IGNOR"]', None, None, u'1', None), (u'?++1', u'?++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'do++you++think++about++it++?', u'do++you++think++about++it++?', 6, 1, None, None, None, None, None, None), (u'do++you++think', u'do++you++think', 3, 1, None, None, None, None, None, None), (u'.++but++you++but++you', u'.++but++you++but++you', 5, 2, None, None, None, None, None, None), (u'\U0001f62b++1++.++but', u'\U0001f62b++1++.++but', 4, 1, None, None, None, None, None, None), (u'right++?', u'right++?', 2, 1, None, None, None, None, None, None), (u'but++you++\U0001f600', u'but++you++\U0001f600', 3, 1, u'[3, 1, 1]', u'[3, 2, 1]', None, None, u'1', None), (u'model++,++but++a++big', u'model++,++but++a++big', 5, 1, None, None, None, None, None, None), (u'\U0001f62b++1++.++but++you++but', u'\U0001f62b++1++.++but++you++but', 6, 1, None, None, None, None, None, None), (u'tiny++surprise++.', u'tini++surpris++.', 3, 1, None, None, None, None, None, None), (u'?++what++do++you++think', u'?++what++do++you++think', 5, 1, None, None, None, None, None, None), (u'.++but++you++but', u'.++but++you++but', 4, 2, None, None, None, None, None, None), (u',++but++a++big++explanation', u',++but++a++big++explan', 5, 1, None, None, None, None, None, None), (u'\U0001f62b++1++.', u'\U0001f62b++1++.', 3, 1, None, None, None, None, None, None), (u'it++?++1++\U0001f62b++1', u'it++?++1++\U0001f62b++1', 5, 1, None, None, None, None, None, None), (u'tiny++model++,++but++a++big', u'tini++model++,++but++a++big', 6, 1, None, None, None, None, None, None), (u'you++but', u'you++but', 2, 2, u'[4, 6]', u'[4, 8]', u'[2, 2]', u'[4, 6]', u'2', u'2'), (u'right++?++what', u'right++?++what', 3, 1, None, None, None, None, None, None), (u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), (u'but++you++but++you++\U0001f600', u'but++you++but++you++\U0001f600', 5, 1, u'[5, 3, "IGNOR", "IGNOR", 1]', u'[5, 4, "IGNOR", "IGNOR", 1]', None, None, u'1', None), (u'\U0001f62b++1++.++but++you', u'\U0001f62b++1++.++but++you', 5, 1, None, None, None, None, None, None), (u'surprise++.++but++you++but++you', u'surpris++.++but++you++but++you', 6, 1, None, None, None, None, None, None), (u'a++big++explanation++.++right', u'a++big++explan++.++right', 5, 1, None, None, None, None, None, None), (u'1++.++but', u'1++.++but', 3, 1, None, None, None, None, None, None), (u'you++but++you++\U0001f600++\U0001f308', u'you++but++you++\U0001f600++\U0001f308', 5, 1, u'[3, 3, "IGNOR", 1, 1]', u'[4, 3, "IGNOR", 1, 1]', None, None, u'1', None), (u'\U0001f62b++1', u'\U0001f62b++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'tiny++model++,', u'tini++model++,', 3, 2, None, None, None, None, None, None), (u'right++?++what++do++you++think', u'right++?++what++do++you++think', 6, 1, None, None, None, None, None, None), (u'?++1++\U0001f62b', u'?++1++\U0001f62b', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[1, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[2, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, u'1', None), (u'you++but++you++\U0001f600', u'you++but++you++\U0001f600', 4, 1, u'[3, 3, "IGNOR", 1]', u'[4, 3, "IGNOR", 1]', None, None, u'1', None), (u'about++it++?', u'about++it++?', 3, 1, None, None, None, None, None, None), (u'surprise++.++but++you++but', u'surpris++.++but++you++but', 5, 1, None, None, None, None, None, None), (u'1++.++but++you', u'1++.++but++you', 4, 1, None, None, None, None, None, None), (u'but++you++but++you', u'but++you++but++you', 4, 2, u'[10, 6, "IGNOR", "IGNOR"]', u'[15, 8, "IGNOR", "IGNOR"]', None, None, u'2', None), (u'about++it++?++1++\U0001f62b', u'about++it++?++1++\U0001f62b', 5, 1, None, None, None, None, None, None), (u'.++right++?', u'.++right++?', 3, 1, None, None, None, None, None, None), (u'tiny++surprise++.++but++you', u'tini++surpris++.++but++you', 5, 1, None, None, None, None, None, None), (u'you++think++about++it', u'you++think++about++it', 4, 1, None, None, None, None, None, None), (u'do++you', u'do++you', 2, 1, None, None, None, None, None, None), (u'1++\U0001f62b', u'1++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'.++right++?++what++do', u'.++right++?++what++do', 5, 1, None, None, None, None, None, None), (u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 6, 1, u'[3, 1, 2, 2, "IGNOR", "IGNOR"]', u'[3, 2, 2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), (u'1++\U0001f62b++1', u'1++\U0001f62b++1', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, u'1', None), (u'big++explanation++.++right', u'big++explan++.++right', 4, 1, None, None, None, None, None, None), (u'it++?++1++\U0001f62b++1++.', u'it++?++1++\U0001f62b++1++.', 6, 1, None, None, None, None, None, None), (u'?++1++\U0001f62b++1++.', u'?++1++\U0001f62b++1++.', 5, 1, None, None, None, None, None, None), (u'you++\U0001f600', u'you++\U0001f600', 2, 1, u'[1, 1]', u'[2, 1]', None, None, u'1', None), (u'1++\U0001f62b++1++.++but++you', u'1++\U0001f62b++1++.++but++you', 6, 1, None, None, None, None, None, None), (u'you++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[2, 1, 1]', None, None, u'1', None), (u'.++right++?++what++do++you', u'.++right++?++what++do++you', 6, 1, None, None, None, None, None, None), (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 5, 1, u'[1, 2, 2, "IGNOR", "IGNOR"]', u'[2, 2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), (u'1++\U0001f62b++1++.++but', u'1++\U0001f62b++1++.++but', 5, 1, None, None, None, None, None, None), (u'think++about++it++?', u'think++about++it++?', 4, 1, None, None, None, None, None, None), (u'big', u'big', 1, 5, u'2', u'2', u'2', u'5', u'2', u'2'), (u'big++explanation', u'big++explan', 2, 1, None, None, None, None, None, None), (u'1++.++but++you++but++you', u'1++.++but++you++but++you', 6, 1, None, None, None, None, None, None), (u'right++?++what++do++you', u'right++?++what++do++you', 5, 1, None, None, None, None, None, None), (u'but++a++big++explanation', u'but++a++big++explan', 4, 1, None, None, None, None, None, None), (u'?++1++\U0001f62b++1', u'?++1++\U0001f62b++1', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[1, 2, 1, "IGNOR"]', None, None, u'1', None), (u'a++big++explanation++.', u'a++big++explan++.', 4, 1, None, None, None, None, None, None), (u'a++big++explanation++.++right++?', u'a++big++explan++.++right++?', 6, 1, None, None, None, None, None, None), (u'1++.', u'1++.', 2, 1, None, None, None, None, None, None), (u',++but++a++big', u',++but++a++big', 4, 1, None, None, None, None, None, None), (u'but++i++realy++liked', u'but++i++reali++like', 4, 1, None, None, None, None, None, None), (u'liked++it++:p++=)++\U0001f600++\U0001f308', u'like++it++:p++=)++\U0001f600++\U0001f308', 6, 1, None, None, None, None, None, None), (u',++but++i++realy', u',++but++i++reali', 4, 1, None, None, None, None, None, None), (u'bad++surprise++for++me++\U0001f62b++,', u'bad++surpris++for++me++\U0001f62b++,', 6, 1, None, None, None, None, None, None), (u'i++realy++liked++it++:p', u'i++reali++like++it++:p', 5, 1, None, None, None, None, None, None), (u'but', u'but', 1, 13, u'11', u'16', u'4', u'10', u'11', u'4'), (u'realy++liked', u'reali++like', 2, 1, None, None, None, None, None, None), (u':p++=)++\U0001f600++\U0001f308++\U0001f600', u':p++=)++\U0001f600++\U0001f308++\U0001f600', 5, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,++but++i', u'me++\U0001f62b++,++but++i', 5, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,', u'me++\U0001f62b++,', 3, 1, None, None, None, None, None, None), (u'liked++it++:p++=)++\U0001f600', u'like++it++:p++=)++\U0001f600', 5, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but', u'\U0001f62b++,++but', 3, 1, None, None, None, None, None, None), (u'realy', u'reali', 1, 4, u'2', u'4', u'1', u'3', u'2', u'1'), (u'surprise++for++me++\U0001f62b', u'surpris++for++me++\U0001f62b', 4, 1, None, None, None, None, None, None), (u'i++realy++liked++it++:p++=)', u'i++reali++like++it++:p++=)', 6, 1, None, None, None, None, None, None), (u'\U0001f600', u'\U0001f600', 1, 5, u'4', u'4', None, None, u'4', None), (u'\U0001f308++\U0001f600', u'\U0001f308++\U0001f600', 2, 3, u'[2, 2]', u'[2, 2]', None, None, u'2', None), (u'=)', u'=)', 1, 1, u'1', u'1', None, None, u'1', None), (u'i++realy++liked++it', u'i++reali++like++it', 4, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,++but', u'me++\U0001f62b++,++but', 4, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but++i++realy', u'\U0001f62b++,++but++i++reali', 5, 1, None, None, None, None, None, None), (u'=)++\U0001f600++\U0001f308', u'=)++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), (u',++but++i', u',++but++i', 3, 1, None, None, None, None, None, None), (u'it++:p++=)++\U0001f600', u'it++:p++=)++\U0001f600', 4, 1, None, None, None, None, None, None), (u'but++i++realy++liked++it++:p', u'but++i++reali++like++it++:p', 6, 1, None, None, None, None, None, None), (u'realy++liked++it++:p++=)', u'reali++like++it++:p++=)', 5, 1, None, None, None, None, None, None), (u'=)++\U0001f600++\U0001f308++\U0001f600', u'=)++\U0001f600++\U0001f308++\U0001f600', 4, 1, None, None, None, None, None, None), (u'it++:p++=)', u'it++:p++=)', 3, 1, None, None, None, None, None, None), (u'\U0001f62b++,', u'\U0001f62b++,', 2, 1, None, None, None, None, None, None), (u'but++i++realy++liked++it', u'but++i++reali++like++it', 5, 1, None, None, None, None, None, None), (u'\U0001f308', u'\U0001f308', 1, 3, u'3', u'3', None, None, u'3', None), (u'for++me++\U0001f62b', u'for++me++\U0001f62b', 3, 1, None, None, None, None, None, None), (u'but++i', u'but++i', 2, 1, None, None, None, None, None, None), (u'i++realy++liked', u'i++reali++like', 3, 1, None, None, None, None, None, None), (u'for++me++\U0001f62b++,++but', u'for++me++\U0001f62b++,++but', 5, 1, None, None, None, None, None, None), (u'realy++liked++it', u'reali++like++it', 3, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308', u'\U0001f600++\U0001f308', 2, 3, u'[3, 3]', u'[3, 3]', None, None, u'3', None), (u'for++me++\U0001f62b++,', u'for++me++\U0001f62b++,', 4, 1, None, None, None, None, None, None), (u'\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600', 3, 3, u'[2, 1, "IGNOR"]', u'[3, 1, "IGNOR"]', None, None, u'1', None), (u'\U0001f62b++,++but++i++realy++liked', u'\U0001f62b++,++but++i++reali++like', 6, 1, None, None, None, None, None, None), (u'me++\U0001f62b++,++but++i++realy', u'me++\U0001f62b++,++but++i++reali', 6, 1, None, None, None, None, None, None), (u',++but', u',++but', 2, 2, None, None, None, None, None, None), (u'it++:p++=)++\U0001f600++\U0001f308', u'it++:p++=)++\U0001f600++\U0001f308', 5, 1, None, None, None, None, None, None), (u'=)++\U0001f600', u'=)++\U0001f600', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), (u'bad++surprise++for++me++\U0001f62b', u'bad++surpris++for++me++\U0001f62b', 5, 1, None, None, None, None, None, None), (u':p++=)', u':p++=)', 2, 1, None, None, None, None, None, None), (u'\U0001f62b++,++but++i', u'\U0001f62b++,++but++i', 4, 1, None, None, None, None, None, None), (u'realy++bad++surprise++for++me++\U0001f62b', u'reali++bad++surpris++for++me++\U0001f62b', 6, 1, None, None, None, None, None, None), (u':p++=)++\U0001f600', u':p++=)++\U0001f600', 3, 1, None, None, None, None, None, None), (u'me++\U0001f62b', u'me++\U0001f62b', 2, 1, None, None, None, None, None, None), (u'realy++liked++it++:p', u'reali++like++it++:p', 4, 1, None, None, None, None, None, None), (u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', 6, 1, None, None, None, None, None, None), (u'\U0001f62b', u'\U0001f62b', 1, 3, u'3', u'3', None, None, u'3', None), (u'but++i++realy', u'but++i++reali', 3, 1, None, None, None, None, None, None), (u':p++=)++\U0001f600++\U0001f308', u':p++=)++\U0001f600++\U0001f308', 4, 1, None, None, None, None, None, None), (u'bad', u'bad', 1, 6, u'4', u'7', u'1', u'5', u'4', u'1'), (u'surprise++for++me++\U0001f62b++,', u'surpris++for++me++\U0001f62b++,', 5, 1, None, None, None, None, None, None), (u'surprise++for++me++\U0001f62b++,++but', u'surpris++for++me++\U0001f62b++,++but', 6, 1, None, None, None, None, None, None), (u'liked++it++:p++=)', u'like++it++:p++=)', 4, 1, None, None, None, None, None, None), (u'realy++liked++it++:p++=)++\U0001f600', u'reali++like++it++:p++=)++\U0001f600', 6, 1, None, None, None, None, None, None), (u',++but++i++realy++liked', u',++but++i++reali++like', 5, 1, None, None, None, None, None, None), (u'for++me++\U0001f62b++,++but++i', u'for++me++\U0001f62b++,++but++i', 6, 1, None, None, None, None, None, None), (u'i++realy', u'i++reali', 2, 1, None, None, None, None, None, None), (u',++but++i++realy++liked++it', u',++but++i++reali++like++it', 6, 1, None, None, None, None, None, None)]



        # assert right_baseline_not_freezed_not_full_repetativ !=  right_baseline_not_freezed_full_repetativ 
        # assert right_baseline_freezed_not_full_repetativ != right_baseline_freezed_full_repetativ
        # assert right_baseline_not_freezed_not_full_repetativ != right_baseline_freezed_not_full_repetativ
        # assert right_baseline_not_freezed_not_full_repetativ != right_baseline_freezed_full_repetativ
        # assert right_baseline_not_freezed_full_repetativ != right_baseline_freezed_not_full_repetativ



        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        

        precomputed_data = self.configer._counted_reps["en"]
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))

    ########################################################################################
    ##################################################################
    ######## full_repetativ_syntagma=False
    ########################################################################################
    ########################################################################################
        import sys
        #self.mode = "prod+"
        #####NOT FREEZED #####
        #### baseline_insertion_border=10 ####
        stats = Stats(mode=self.mode,use_cash=True,status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, baseline_delimiter="++",
                    encryption_key=encryption_key, full_repetativ_syntagma=False,
                    ignore_hashtag=False, force_cleaning=False,
                    ignore_url=False,  ignore_mention=False, ignore_punkt=False, ignore_num=False)

        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False, baseline_insertion_border=10)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")
        #p(baseline,"baseline")
        #p(repls, "repls")
        #p(redus, "redus")
        #p(baseline,"baseline")
        #sys.exit()
        
        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        #sorted(baseline).should.be.equal(sorted(right_baseline_not_freezed_not_full_repetativ))
        #baseline.should.be.equal(right_baseline_not_freezed_not_full_repetativ)
        #
        
        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,precomputed_data,repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False


        # #####baseline_insertion_border=10000000
        stats = Stats(mode=self.mode,use_cash=True,status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, baseline_delimiter="++",
                    encryption_key=encryption_key,
                    ignore_hashtag=False, force_cleaning=False,
                    ignore_url=False,  ignore_mention=False, ignore_punkt=False, ignore_num=False)

        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False, baseline_insertion_border=100000000)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")



        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        #sorted(baseline).should.be.equal(sorted(right_baseline_not_freezed_not_full_repetativ))
        #p(baseline,"baseline")
        
        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,precomputed_data,repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False


    #––––––––––––––––––––––––––––––– 
    #––––––––––––––––––––––––––––––– 
    #––––––––––––––––––––––––––––––– 



        ##### FREEZED #####
        stats = Stats(mode=self.mode,use_cash=True,status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, baseline_delimiter="++",
                    encryption_key=encryption_key,
                    ignore_hashtag=False, force_cleaning=False,
                    ignore_url=False,  ignore_mention=False, ignore_punkt=False, ignore_num=False)

        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=True, baseline_insertion_border=10)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")
        #p(list(stats.get_data([u':hashtag:'], repl=True, redu=True, baseline=True)))
        
        #p(baseline,"right_baseline_freezed_not_full_repetativ")
        #sys.exit()
        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        #sorted(baseline).should.be.equal(sorted(right_baseline_freezed_not_full_repetativ))
        #
        
        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,precomputed_data,repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False




    # ########################################################################################
    # ##################################################################
    # ######## full_repetativ_syntagma=True
    # ########################################################################################
    # ########################################################################################



        #self.mode = "prod+"
        #####NOT FREEZED #####
        #### baseline_insertion_border=10 ####
        stats = Stats(mode=self.mode,use_cash=True,status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, baseline_delimiter="++",
                    encryption_key=encryption_key, full_repetativ_syntagma=True,
                    ignore_hashtag=False, force_cleaning=False,
                    ignore_url=False,  ignore_mention=False, ignore_punkt=False, ignore_num=False)

        
        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False, baseline_insertion_border=10)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")

        #p(repls,"repls")
        #p(redus, "redus")


        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        #sorted(baseline).should.be.equal(sorted(right_baseline_not_freezed_full_repetativ))
        #p(baseline,"right_baseline_not_freezed_full_repetativ")
        #sys.exit()
        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,precomputed_data,repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False



    # #–––––––––––––––––––––––––––––––                


        ##### FREEZED #####
        stats = Stats(mode=self.mode,use_cash=True,status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, baseline_delimiter="++",
                    encryption_key=encryption_key,full_repetativ_syntagma=True,
                    ignore_hashtag=False, force_cleaning=False,
                    ignore_url=False,  ignore_mention=False, ignore_punkt=False, ignore_num=False)

        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=True, baseline_insertion_border=10)
        baseline = stats.statsdb.getall("baseline")
        repls = stats.statsdb.getall("replications")
        redus = stats.statsdb.getall("reduplications")
        #p(list(stats.get_data([u':hashtag:'], repl=True, redu=True, baseline=True)))
        
        repls.should.be.equal(right_repls)
        redus.should.be.equal(right_redus)
        #sorted(baseline).should.be.equal(sorted(right_baseline_freezed_full_repetativ))
        #p(baseline,"right_baseline_freezed_full_repetativ")
        
        self.configer.right_rep_num["en"]["repls"].should.be.equal(len(repls))
        self.configer.right_rep_num["en"]["redus"].should.be.equal(len(redus))
        self._check_correctnes(stats.col_index_orig,precomputed_data,repls=repls, redus=redus, baseline=baseline)

        bas_synts = [bs[0] for bs in  baseline]
        for r in  redus:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False

        for r in  repls:
            if r[5] not in bas_synts:
                p(r[5],"ERROR", c="r")
                assert False



    def _check_correctnes(self,indexes, precomputed_data,repls=False, redus=False, baseline=False):
        import copy
        ### Step 1: Summerizing 
        dict_repls = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        dict_redus = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        dict_baseline = defaultdict()
        if repls:
            ix_repl = indexes["repl"]
            for r in repls:
                doc_id = r[ix_repl["doc_id"]]
                index_in_corpus = r[ix_repl["index_in_corpus"]]
                word = r[ix_repl["normalized_word"]]
                dict_repls[word][doc_id][index_in_corpus] += 1

        if redus:
            ix_redu = indexes["redu"]
            for r in redus:
                doc_id = r[ix_redu["doc_id"]]
                index_in_corpus = r[ix_redu["index_in_corpus"]]
                word = r[ix_redu["normalized_word"]]
                redu_length = r[ix_redu["redu_length"]]
                dict_redus[word][doc_id][index_in_corpus] += redu_length

        #p(baseline)
        if baseline:

            ix_b = indexes["baseline"]
            for b in baseline:
                syntagma = b[ix_b["syntagma"]]
                scope = b[ix_b["scope"]]
                occur_syntagma_all = b[ix_b["occur_syntagma_all"]]
                if int(scope) == 1:
                    dict_baseline[syntagma] = occur_syntagma_all

        ##### Step 2: Counts
        computed_counts = defaultdict(lambda:defaultdict(lambda:[0,0]))
        if repls:
            for word, word_data in  dict_repls.items():
                for doc_id, doc_data in word_data.items():
                    #current_doc_id = doc_id
                    for index_in_corpus, counter in doc_data.items():
                        #if current_doc_id == doc_id:
                        #    if 
                        computed_counts[word]["repl"][0] += 1
                        computed_counts[word]["repl"][1] += counter


        if redus:
            for word, word_data in  dict_redus.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]["redu"][0] += 1
                        computed_counts[word]["redu"][1] += counter


        if baseline:
            for syntagma, counter  in dict_baseline.items():
                computed_counts[syntagma]["baseline"] = counter
        


        ### Step 3: Comparation 
        precounted_reps = precomputed_data
        computed_counts = { word:{ phanomen: tuple(counter) if isinstance(counter, (list, tuple)) else counter   for phanomen, counter in data.items()} for word, data in computed_counts.items() }                        
        precounted_reps = { word:{ phanomen: tuple(counter) if isinstance(counter, (list, tuple)) else counter   for phanomen, counter in data.items()} for word, data in precounted_reps.items() }                        
        copy_precounted_reps = copy.deepcopy(precounted_reps)
        copy_computed_counts = copy.deepcopy(computed_counts)
        if (repls and  baseline) or (redus and baseline):
            computed_counts = { word:data for word, data in computed_counts.items() if ("repl" in data and "baseline" in data) or ("redu" in data and "baseline" in data) }                        
        
        #p((computed_counts))
        for word, data in precounted_reps.items():
            for phanomen, counts in data.items():
                if phanomen == "baseline":
                    if baseline:
                        if counts != computed_counts[word][phanomen]:
                            precomputed = counts
                            extracted = computed_counts[word][phanomen]
                            #p((word, precomputed,extracted), "ERROR",c="c")
                            #assert False
                        else:
                            del copy_computed_counts[word][phanomen]
                            del copy_precounted_reps[word][phanomen]

                else:
                    if not (phanomen == "repl" and repls):
                        continue

                    elif not (phanomen == "redu" and redus):
                        continue

                    if tuple(counts) != tuple(computed_counts[word][phanomen]):
                        precomputed = tuple(counts)
                        extracted = tuple(computed_counts[word][phanomen])
                        #p((word, precomputed,extracted), "ERROR",c="c")
                        ##assert False
                    else:
                        del copy_computed_counts[word][phanomen]
                        del copy_precounted_reps[word][phanomen]


        # for item in sorted(computed_counts.items()):
        #     print "   " + str(item)
        
        # p("fghjk\n", c="r")
        # for item in sorted(precounted_reps.items()):
        #     print "   " + str(item)

        for word, data in precounted_reps.items():
            if computed_counts[word] == data:
                del copy_computed_counts[word]
                del copy_precounted_reps[word]
            else:
                msg = u"Not Equal Data for word: '{}' >>>> '{}' != '{}' <<<<".format(word, data, computed_counts[word])
                #p(msg)

        copy_computed_counts = {word:data for word, data in copy_computed_counts.items() if len(data)>1}
        if copy_computed_counts:
            #p(copy_computed_counts, "copy_computed_counts")
            assert False

        copy_computed_counts = {word:data for word, data in copy_precounted_reps.items() if len(data)>1}
        if copy_precounted_reps:
            #p(copy_precounted_reps, "copy_precounted_reps")
            assert False

        assert True





    def pretty_print_uniq(self,item, syn_order=False, baseline_small=True ):
        if syn_order:
            #print "fghjk"
            print "\n\n\n"
            for k,v in item.iteritems():
                #print "fghjk111"
                #print v
                print "\n"
                #print "--------------- {} -------------------".format(k)
                #p((k,v))
                if v and k not in ["syntagma", "baseline", "stem_syn"]:
                    main_open_tag = "(" if isinstance(v, tuple) else "["
                    print "\t\tright_{} = {}".format(k,main_open_tag)

                    if len(v) == 3 and v[1] in [True, False]:
                        main_open_tag1 ="(" if isinstance( v[0], tuple) else "["
                        print "\t\t\t\t\t\t {}".format(main_open_tag1)

                        for data_for_syntagmas_part in v[0]:
                            word = data_for_syntagmas_part[0]
                            reps = data_for_syntagmas_part[1]
                            #p((word, reps))
                            #p(data_for_syntagmas_part, "data_for_syntagmas_part")
                            #print "%%"
                            main_open_tag_2 = "(" if isinstance(data_for_syntagmas_part, tuple) else "["
                            open_tag = "(" if isinstance(reps, tuple) else "["
                            #print "\t\t\t\t\t {}, {}".format(repr(word),open_tag)
                            print "\t\t\t\t\t\t\t{}{}, {}".format( main_open_tag_2,repr(word),open_tag)
                            # #print open_tag
                            # open_tag = "(" if isinstance(reps[0], tuple) else "["
                            # print "\t\t\t\t\t\t\t\t\t {}".format(open_tag)
                            for row in reps:

                                print "\t\t\t\t\t\t\t\t\t\t\t {},".format(row)
                                #for row in rows:
                                #    print "\t\t\t\t\t\t\t\t {},".format(row)
                            # close_tag = ")" if isinstance(reps[0], tuple) else "]"
                            # print "\t\t\t\t\t\t\t\t\t {},".format(close_tag)
                            # print "\t\t\t\t\t\t\t\t\t {},".format(reps[1])
                            # print "\t\t\t\t\t\t\t\t\t {},".format(reps[2])
                            main_close_tag_2 = ")" if isinstance(data_for_syntagmas_part, tuple) else "]"
                            close_tag = ")" if isinstance(reps, tuple) else "]"
                            # #print "\t\t\t\t\t\t {}".format(close_tag)
                            print "\t\t\t\t\t\t\t\t\t\t {}\n\t\t\t\t\t\t\t\t  {},".format(close_tag,main_close_tag_2)
                        # main_close_tag = ")" if isinstance(v, tuple) else "]"
                        # print "\t\t\t {}".format(main_close_tag)
                        main_close_tag1 =")" if isinstance( v[0], tuple) else "]"
                        print "\t\t\t\t\t\t {},".format(main_close_tag1)
                        print "\t\t\t\t\t\t {},".format(v[1])
                        print "\t\t\t\t\t\t {},".format(v[2])
                    else:
                        #p("fghjkl")
                        for data in v: 
                            word = data[0]
                            reps = data[1]
                            #print "ff§"
                            main_open_tag_2 = "(" if isinstance(data, tuple) else "["
                            open_tag = "(" if isinstance(reps, tuple) else "["
                            #print "\t\t\t\t\tright_{} = {}".format(k,open_tag)
                            print "\t\t\t\t\t{}{}, {}".format( main_open_tag_2,repr(word),open_tag)
                            #print open_tag
                            #p(reps,"reps")
                            for row in reps:
                                print "\t\t\t\t\t\t\t\t {},".format(row)
                            close_tag = ")" if isinstance(reps, tuple) else "]"
                            main_close_tag_2 = ")" if isinstance(data, tuple) else "]"
                            print "\t\t\t\t\t\t\t {}\n\t\t\t\t\t  {},".format(close_tag,main_close_tag_2)

                            
                            #print "\t\t\t\t {}".format(main_close_tag_2)

                    main_close_tag = ")" if isinstance(v, tuple) else "]"
                    print "\t\t\t\t {}".format(main_close_tag)

                else:
                    #print "fghjk333"
                    #open_tag = "(" if isinstance(reps, tuple) else "["
                    #close_tag = ")" if isinstance(reps, tuple) else "]"
                    #print "\t\tright_{} = {} {} {}".format(k,open_tag, reps, close_tag)
                    print "\t\tright_{} = {}".format(k, v)
        else:
            print "\n\n\n"
            for k,v in item.iteritems():
                #print v
                print "\n"
                #print "--------------- {} -------------------".format(k)
                l = len(v)
                #p((l,v))
                if len(v) >= 2 and k not in ["syntagma", "stem_syn"]:
                    if k == "baseline" and baseline_small:
                        print "\t\tright_{} = {}".format(k, v,)
                        continue

                    if len(v) == 3 and v[1] in [True, False]:
                        open_tag = "(" if isinstance(v, tuple) else "["
                        print "\t\tright_{} = {}".format(k,open_tag)
                        #print open_tag
                        open_tag = "(" if isinstance(v[0], tuple) else "["
                        print "\t\t\t\t\t\t {}".format(open_tag)
                        for row in v[0]:

                            print "\t\t\t\t\t\t\t {},".format(row)
                            #for row in rows:
                            #    print "\t\t\t\t\t {},".format(row)
                        close_tag = ")" if isinstance(v[0], tuple) else "]"
                        print "\t\t\t\t\t\t {},".format(close_tag)
                        print "\t\t\t\t\t\t {},".format(v[1])
                        print "\t\t\t\t\t\t {},".format(v[2])
                        close_tag = ")" if isinstance(v, tuple) else "]"
                        print "\t\t\t {}".format(close_tag)
                    else:
                        open_tag = "(" if isinstance(v, tuple) else "["
                        print "\t\tright_{} = {}".format(k,open_tag)
                        #print open_tag
                        for row in v:
                            print "\t\t\t\t\t {},".format(row)
                        close_tag = ")" if isinstance(v, tuple) else "]"
                        print "\t\t\t\t {}".format(close_tag)

                else:
                    #open_tag = "(" if isinstance(v, tuple) else "["
                    #close_tag = ")" if isinstance(v, tuple) else "]"
                    #print "\t\tright_{} = {} {} {}".format(k,open_tag, v, close_tag)
                    print "\t\tright_{} = {}".format(k, v,)





    def _summerize_reps(self,indexes,repls, redus, baseline):
        import copy
        ### Step 1: Summerizing 
        dict_repls = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        dict_redus = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        dict_baseline = defaultdict()
        if repls:
            ix_repl = indexes["repl"]
            for r in repls:
                doc_id = r[ix_repl["doc_id"]]
                index_in_corpus = r[ix_repl["index_in_corpus"]]
                word = r[ix_repl["normalized_word"]]
                dict_repls[word][doc_id][index_in_corpus] += 1

        if redus:
            ix_redu = indexes["redu"]
            for r in redus:
                doc_id = r[ix_redu["doc_id"]]
                index_in_corpus = r[ix_redu["index_in_corpus"]]
                word = r[ix_redu["normalized_word"]]
                redu_length = r[ix_redu["redu_length"]]
                dict_redus[word][doc_id][index_in_corpus] += redu_length

        #p(baseline)
        if baseline:
            ix_b = indexes["baseline"]
            for b in baseline:
                syntagma = b[ix_b["syntagma"]][0]
                scope = b[ix_b["scope"]]
                occur_syntagma_all = b[ix_b["occur_syntagma_all"]]
                if int(scope) == 1:
                    dict_baseline[syntagma] = occur_syntagma_all

        ##### Step 2: Counts
        computed_counts = defaultdict(lambda:defaultdict(lambda:[0,0]))
        if repls:
            for word, word_data in  dict_repls.items():
                for doc_id, doc_data in word_data.items():
                    #current_doc_id = doc_id
                    for index_in_corpus, counter in doc_data.items():
                        #if current_doc_id == doc_id:
                        #    if 
                        computed_counts[word]["repl"][0] += 1
                        computed_counts[word]["repl"][1] += counter


        if redus:
            for word, word_data in  dict_redus.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]["redu"][0] += 1
                        computed_counts[word]["redu"][1] += counter


        if baseline:
            for syntagma, counter  in dict_baseline.items():
                computed_counts[syntagma]["baseline"] = counter
        
        out_repls = computed_counts[word]["repl"] if repls else None
        out_redus = computed_counts[word]["redu"] if redus else None
        out_baseline = computed_counts[syntagma]["baseline"]  if baseline else None
        
        output = {}
        if out_repls and out_repls[0] > 0:
            output["repl"] = tuple(out_repls)

        if out_redus and out_redus[0] > 0:
            output["redu"] = tuple(out_redus)

        if out_baseline and out_baseline > 0:
            output["baseline"] = out_baseline


        return  output



    def _summerize_reps2(self,indexes,repls, redus, baseline):
        import copy
        ### Step 1: Summerizing 
        dict_repls = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        dict_redus = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        dict_baseline = defaultdict()
        if repls:
            ix_repl = indexes["repl"]
            for r in repls:
                doc_id = r[ix_repl["doc_id"]]
                index_in_corpus = r[ix_repl["index_in_corpus"]]
                word = r[ix_repl["normalized_word"]]
                dict_repls[word][doc_id][index_in_corpus] += 1

        if redus:
            ix_redu = indexes["redu"]
            for r in redus:
                doc_id = r[ix_redu["doc_id"]]
                index_in_corpus = r[ix_redu["index_in_corpus"]]
                word = r[ix_redu["normalized_word"]]
                redu_length = r[ix_redu["redu_length"]]
                dict_redus[word][doc_id][index_in_corpus] += redu_length

        #p(baseline)
        if baseline:
            ix_b = indexes["baseline"]
            for b in baseline:
                syntagma = tuple(b[ix_b["syntagma"]])
                scope = b[ix_b["scope"]]
                occur_syntagma_all = b[ix_b["occur_syntagma_all"]]
                #if int(scope) == 1:
                dict_baseline[syntagma] = occur_syntagma_all

        ##### Step 2: Counts
        computed_counts = defaultdict(lambda:defaultdict(lambda:[0,0]))
        if repls:
            for word, word_data in  dict_repls.items():
                for doc_id, doc_data in word_data.items():
                    #current_doc_id = doc_id
                    for index_in_corpus, counter in doc_data.items():
                        #if current_doc_id == doc_id:
                        #    if 
                        computed_counts["repl"][word][0] += 1
                        computed_counts["repl"][word][1] += counter


        if redus:
            for word, word_data in  dict_redus.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts["redu"][word][0] += 1
                        computed_counts["redu"][word][1] += counter


        if baseline:
            #p(baseline,"baseline")
            for syntagma, counter  in dict_baseline.items():
                #p(syntagma)
                computed_counts["baseline"][tuple(syntagma)] = counter
        



        return  { phanomen:{word:counts for word, counts in data.items()} for phanomen, data in computed_counts.items()}


    @attr(status='stable')
     # @wipd
    def test_get_data_for_one_syntagma_compared_with_gold_stabdard_611_0(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()

        #### DE ######
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_en))
        gold_standard_data = self.configer._counted_reps["en"]

    ################################################################################################################################################
    ################################################ I. FullRepetativnes= True   #################################################################################
    ########################################################################################################################################
        stats.recompute_syntagma_repetativity_scope(True)


        ## Case 1###
        syntagma = ["bad"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")

        right_data = gold_standard_data[syntagma[0]]
        #p(right_data)
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")

        repl_num = right_data["repl"][1]  #= sum([counts[1] for word, counts in  right_data["repl"] ])
        redu_num = right_data["redu"][0] #sum([counts[0] for word, counts in  right_data["redu"].items() ])

        right_data.should.be.equal(answer)
        
        len(item["repl"]).should.be.equal(repl_num)
        len(item["redu"]).should.be.equal(redu_num)





        ## Case 2###
        syntagma = ["-("]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)


        ## Case 3###
        syntagma = ["-)"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)



        ## Case 4###
        syntagma = ["=)"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)


        ## Case 5###
        syntagma = ["."]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)



        ## Case 6###
        syntagma = [u'\U0001f600']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)




        ## Case 7###
        syntagma = [u'\U0001f62b']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)


        ## Case 8###
        syntagma = [ u'but']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)



        ## Case 9###
        syntagma = [u'se']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)

        ## Case 10###
        syntagma = [u'big']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)


        ## Case 11###
        syntagma = [u'se']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)

        ## Case 12###
        syntagma = [u'right']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = gold_standard_data[syntagma[0]]
        answer = self._summerize_reps(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)


        ## Case 12###
        syntagma = [u'EMOASC']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos")
        #self.pretty_print_uniq(item)

        right_data =  {
                        'repl': {
                                    u'=)': [1, 1], 
                                    u':-(': [2, 2], 
                                    u'-)': [1, 1], 
                                    u'-(': [1, 1]}, 

                        'baseline': {
                                        (u':-(', u'@real_trump', u'#shetlife'): 1, 
                                        (u'-(', u'\U0001f62b', u':-(', u'#shetlife', u'http://www.noooo.com'): 1, 
                                        (u'=)',): 1, (u':-(',): 2, 
                                        (u':-(', u'@real_trump', u'#shetlife', u'#readytogo'): 1, 
                                        (u':-(', u'#shetlife', u'http://www.noooo.com'): 1, 
                                        (u'=)', u'\U0001f600', u'\U0001f308'): 1, 
                                        (u'=)', u'\U0001f600', u'\U0001f308', u'\U0001f600'): 1, 
                                        (u'=)', u'\U0001f600'): 1, (u':-(', u'@real_trump'): 1, 
                                        (u'-(', u'\U0001f62b'): 1, 
                                        (u'-)',): 1, 
                                        (u'-(',): 1, 
                                        (u'-(', u'\U0001f62b', u':-('): 1, 
                                        (u':-(', u'@real_trump', u'#shetlife', u'#readytogo', u'http://www.absurd.com'): 1, 
                                        (u'-(', u'\U0001f62b', u':-(', u'#shetlife'): 1, 
                                        (u':-(', u'#shetlife'): 1}}
        
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)
        len(item["repl"]).should.be.equal(repl_num)



        ## Case 12###
        syntagma = [u'number']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos")
        #self.pretty_print_uniq(item)

        right_data =  {
                        'repl': {u'1': [2, 2]}, 

                        'baseline': {(u'1', u'.', u'but', u'you', u'but'): 1, (u'1', u'\U0001f62b', u'1', u'.'): 1, (u'1', u'\U0001f62b', u'1', u'.', u'but', u'you'): 1, (u'1', u'\U0001f62b'): 1, (u'1', u'.', u'but'): 1, (u'1', u'\U0001f62b', u'1', u'.', u'but'): 1, (u'1', u'.', u'but', u'you', u'but', u'you'): 1, (u'1',): 2, (u'1', u'.', u'but', u'you'): 1, (u'1', u'\U0001f62b', u'1'): 1, (u'1', u'.'): 1}}
        
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])
        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)
        len(item["repl"]).should.be.equal(repl_num)


 
 


        ## Case 15###
        syntagma = ["very","pity"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = {
                    "repl":{
                            "very": [2,4],
                            "pity": [2,4],
                            },    
                    "redu":{
                            "very": [1,3],
                            "pity": [1,4],
                            }, 
                    "baseline":{
                            ("very","pity"): 1,
                            },   
                    }
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])
        redu_num = sum([counts[0] for word, counts in  right_data["redu"].items() ])

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data["repl"].should.be.equal(answer["repl"])
        right_data["redu"].should.be.equal(answer["redu"])
        right_data["baseline"].should.be.equal(answer["baseline"])
        len(item["repl"]).should.be.equal(repl_num)
        len(item["redu"]).should.be.equal(redu_num)




        #right_data.should.be.equal(answer)


        ## Case 14###
        syntagma = ["bad","news"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        right_data = {
                    "baseline":{
                            ("bad","news"): 1,
                            },   
                    }
        
        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)







        ## Case 15###
        syntagma = ["but","you"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        right_data = {
                        'repl': {
                                    u'you': [6, 8], 
                                    u'but': [10, 15]}, 
                        
                        'baseline': {
                                    (u'but', u'you'): 4}, 
                        
                        'redu': {
                                    u'you': [2, 4], 
                                    u'but': [2, 4]}

                    }
        
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])
        redu_num = sum([counts[0] for word, counts in  right_data["redu"].items() ])

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)
        len(item["repl"]).should.be.equal(repl_num)
        len(item["redu"]).should.be.equal(redu_num)




        ## Case 16###
        syntagma = [u"😀",u"🌈"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        right_data = {
                        'repl': 
                                {u'\U0001f600': [3, 3], 
                                u'\U0001f308': [3, 3]}, 
                        
                        'baseline': {
                                        (u'\U0001f600', u'\U0001f308'): 3}}
        
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])
        #redu_num = sum([counts[0] for word, counts in  right_data["redu"].items() ])

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)
        len(item["repl"]).should.be.equal(repl_num)
        #len(item["redu"]).should.be.equal(redu_num)


        ## Case 34###
        syntagma = [u"🌈",u"😀"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        right_data = {
                        'repl': {
                                    u'\U0001f600': [2, 2], 
                                    u'\U0001f308': [2, 2]}, 
                        
                        'baseline': {
                                        (u'\U0001f308', u'\U0001f600'): 3}

                        }
        
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])
        

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)
        len(item["repl"]).should.be.equal(repl_num)


        stats.recompute_syntagma_repetativity_scope(False)


        ## Case 30###
        syntagma = ["bad","news"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = {
                        'repl': {
                                    u'bad': [4, 7]}, 
                        
                        'baseline': {
                                        (u'bad', u'news'): 1}, 
                        
                        'redu': {
                                    u'bad': [1, 5]}}
        
        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)


        ## Case 31###
        syntagma = ["tiny","model"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        
        right_data = {
                        'repl': {u'model': [1, 2]}, 
                        'baseline': {(u'tiny', u'model'): 2}, 
                        'redu': {u'tiny': [1, 6]}}
        

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        # #p(answer, "answer")
        right_data.should.be.equal(answer)




        ## Case 15###
        syntagma = ["but","you"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        right_data = {
                        'repl': {
                                    u'you': [6, 8], 
                                    u'but': [10, 15]}, 
                        
                        'baseline': {
                                        (u'but', u'you'): 4}, 
                        
                        'redu': {
                                    u'you': [2, 4], 
                                    u'but': [4, 10]}}
        
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])
        redu_num = sum([counts[0] for word, counts in  right_data["redu"].items() ])

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)
        len(item["repl"]).should.be.equal(repl_num)
        len(item["redu"]).should.be.equal(redu_num)


        ## Case 33###
        syntagma = [u"😀",u"🌈"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        right_data = {
                        'repl': 
                                {u'\U0001f600': [3, 3], 
                                u'\U0001f308': [3, 3]}, 
                        
                        'baseline': {
                                        (u'\U0001f600', u'\U0001f308'): 3}}
        
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])
        #redu_num = sum([counts[0] for word, counts in  right_data["redu"].items() ])

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)
        len(item["repl"]).should.be.equal(repl_num)
        #len(item["redu"]).should.be.equal(redu_num)


        ## Case 34###
        syntagma = [u"🌈",u"😀"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        right_data = {
                        'repl': {
                                    u'\U0001f600': [2, 2], 
                                    u'\U0001f308': [3, 3]}, 
                        
                        'baseline': {
                                        (u'\U0001f308', u'\U0001f600'): 3}
                    }
        
        repl_num = sum([counts[1] for word, counts in  right_data["repl"].items() ])
        

        answer = self._summerize_reps2(stats.col_index_orig, item["repl"], item["redu"],item["baseline"])
        #p(answer, "answer")
        right_data.should.be.equal(answer)
        len(item["repl"]).should.be.equal(repl_num)

    
    def convert_all_lists_to_tuples(self, giv_object):
        new_obj = []
        for item in giv_object:
            try:
                new_item = []
                for underitem in item: 
                    new_item.append(tuple(underitem) )
                new_obj.append(tuple(new_item))
            except:
                try:
                    new_obj.append(tuple(item))
                except:
                    new_obj.append(item)

        return tuple(new_obj)




    @attr(status='stable')
    #@wipd
    def test_get_data_for_one_syntagma_611_1(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()

        #### DE ######
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))


    ################################################################################################################################################
    ################################################ I. FullRepetativnes= True   #################################################################################
    ########################################################################################################################################
        stats.recompute_syntagma_repetativity_scope(True)


    ################################################################################################################################################
    ################################################################################################################################################
    ##### return_full_tuple = False #######################################################################################################+
    ###########################################################################################################################################
    ################################################################################################################################################

    ############################
    ####### SCOPE 1 ##############
    ############################


        ###################### syntagma_type="lexem" #############################

        # ########stemmed_search=False #
        #p(stats.statsdb.rownum("replications"))
        ### Case 1.1:
        syntagma = ["klitze"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        #p(item,"item")
        #p(stats.statsdb.rownum("replications"))


        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]

        right_repl = [
                     (54, 11111, u'[5, 6, 15, 3]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'sache', u'["NN", null, "sach"]', u'.', u'["symbol", null, "."]', u'die', u'["PDS", null, "die"]', u'aber', u'["ADV", null, "aber"]'),
                     (1, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (2, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'e', 7, 5, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (20, 10000, u'[12, 3, 8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]'),
                 ]


        right_syntagma = ['klitze']


        right_baseline = [[[u'klitze'], u'klitz', 1, 8, u'3', u'4', u'2', u'6', u'3', u'2']]


        right_redu = [
                     (18, 12222, u'[24]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitz', u'{"klitze": 4}', 4, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u',', u'["symbol", null, ","]', u'die', u'["PRELS", null, "die"]', u'ich', u'["PPER", null, "ich"]'),
                     (1, 8888, u'[4, 11]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze^7": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                 ]



        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        ##item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})

 
        # ########stemmed_search=False #

        ### Case 1.2:
        syntagma = ["kleine"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #self.pretty_print_uniq(item)
        #p(item,"item")


        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]


        right_repl = [
                     (82, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 4, 2, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (83, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'i', 5, 3, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (84, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (85, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 8, 5, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                     (57, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (58, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (59, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 5, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                 ]


        right_syntagma = ['kleine']


        right_baseline = [[[u'kleine'], u'klein', 1, 7, u'5', u'11', u'1', u'2', u'5', u'1']]


        right_redu = [(2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]')]
        
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        ##item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})




    #     ########stemmed_search=True #

        ### Case 1.3:
        syntagma = ["klein"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",stemmed_search=True)
        #self.pretty_print_uniq(item)
        #p(item,"item")


        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]


        right_repl = [
                     (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                     (26, 10000, u'[12, 3, 8]', u'[1, 0]', u'[1, 0]', u'kleines', u'kleine^4s^7', u'klein', u'e', 4, 5, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (27, 10000, u'[12, 3, 8]', u'[1, 0]', u'[1, 0]', u'kleines', u'kleine^4s^7', u'klein', u's', 7, 6, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (28, 10000, u'[12, 3, 8]', u'[1, 1]', u'[1, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u'n', 4, 4, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (29, 10000, u'[12, 3, 8]', u'[1, 1]', u'[1, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u'e', 3, 5, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (30, 10000, u'[12, 3, 8]', u'[1, 1]', u'[1, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u's', 4, 6, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (31, 10000, u'[12, 3, 8]', u'[1, 2]', u'[1, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'e', 4, 2, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (32, 10000, u'[12, 3, 8]', u'[1, 2]', u'[1, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'i', 5, 3, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (33, 10000, u'[12, 3, 8]', u'[1, 2]', u'[1, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'n', 3, 4, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (34, 10000, u'[12, 3, 8]', u'[1, 2]', u'[1, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u's', 3, 6, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (37, 10000, u'[12, 3, 8]', u'[2, 0]', u'[2, 0]', u'kleinere', u'kleinere^5', u'klein', u'e', 5, 7, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                     (38, 10000, u'[12, 3, 8]', u'[2, 1]', u'[2, 0]', u'kleinere', u'kleine^3r^2e^5', u'klein', u'e', 3, 5, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                     (39, 10000, u'[12, 3, 8]', u'[2, 1]', u'[2, 0]', u'kleinere', u'kleine^3r^2e^5', u'klein', u'e', 5, 7, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                     (45, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'e', 3, 2, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (46, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'i', 3, 3, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (47, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'n', 3, 4, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (48, 10000, u'[12, 3, 8]', u'[2, 8]', u'[2, 4]', u'klein', u'klein^5', u'klein', u'n', 5, 4, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (52, 10000, u'[12, 3, 8]', u'[2, 12]', u'[2, 7]', u'kleines', u'klein^3e^2s', u'klein', u'n', 3, 4, u'[2, 7]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                     (53, 10000, u'[12, 3, 8]', u'[2, 13]', u'[2, 7]', u'kleines', u'kleines^4', u'klein', u's', 4, 6, u'[2, 7]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                     (57, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (58, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (59, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 5, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (66, 11111, u'[5, 6, 15, 3]', u'[3, 0]', u'[3, 0]', u'kleines', u'kleine^4s^7', u'klein', u'e', 4, 5, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (67, 11111, u'[5, 6, 15, 3]', u'[3, 0]', u'[3, 0]', u'kleines', u'kleine^4s^7', u'klein', u's', 7, 6, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (68, 11111, u'[5, 6, 15, 3]', u'[3, 1]', u'[3, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u'n', 4, 4, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (69, 11111, u'[5, 6, 15, 3]', u'[3, 1]', u'[3, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u'e', 3, 5, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (70, 11111, u'[5, 6, 15, 3]', u'[3, 1]', u'[3, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u's', 4, 6, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (71, 11111, u'[5, 6, 15, 3]', u'[3, 2]', u'[3, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'e', 4, 2, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (72, 11111, u'[5, 6, 15, 3]', u'[3, 2]', u'[3, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'i', 5, 3, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (73, 11111, u'[5, 6, 15, 3]', u'[3, 2]', u'[3, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'n', 3, 4, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (74, 11111, u'[5, 6, 15, 3]', u'[3, 2]', u'[3, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u's', 3, 6, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (82, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 4, 2, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (83, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'i', 5, 3, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (84, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (85, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 8, 5, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                 ]


        right_syntagma = [u'klein']


        right_baseline = [[[u'kleines'], u'klein', 1, 8, u'8', u'20', u'3', u'8', u'8', u'3'], [[u'kleinere'], u'klein', 1, 2, u'2', u'3', u'1', u'2', u'2', u'1'], [[u'kleine'], u'klein', 1, 7, u'5', u'11', u'1', u'2', u'5', u'1'], [[u'klein'], u'klein', 1, 2, u'2', u'4', u'1', u'2', u'2', u'1']]


        right_redu = [
                     (2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (11, 10000, u'[12, 3, 8]', u'[1, 0]', u'[1, 0]', u'kleines', u'klein', u'{"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}', 3, u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                     (12, 10000, u'[12, 3, 8]', u'[2, 0]', u'[2, 0]', u'kleinere', u'klein', u'{"kleinere^5": 1, "kleine^3r^2e^5": 1}', 2, u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                     (14, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'klein', u'{"kle^3i^3n^3": 1, "klein^5": 1}', 2, u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (16, 10000, u'[12, 3, 8]', u'[2, 12]', u'[2, 7]', u'kleines', u'klein', u'{"klein^3e^2s": 1, "kleines^4": 1}', 2, u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                     (17, 11111, u'[5, 6, 15, 3]', u'[3, 0]', u'[3, 0]', u'kleines', u'klein', u'{"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}', 3, u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                 ]

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        ##item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})






    # # ############################
    # # ####### SCOPE 2 ##############
    # # ############################


        ####################### syntagma_type="lexem" #############################

        ########stemmed_search=False #
        ### Case 1.1:
        syntagma = ["klitze", "kleine"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #p(item,"item")
        #self.pretty_print_uniq(item)


        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]


        right_repl = [
                     (1, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (2, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'e', 7, 5, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (20, 10000, u'[12, 3, 8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]'),
                     (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                 ]


        right_syntagma = ['klitze', 'kleine']


        right_baseline = [[[u'klitze', u'kleine'], u'klitz++klein', 2, 4, u'[2, 3]', u'[3, 4]', u'[1, 1]', u'[2, 2]', u'2', u'1']]


        right_redu = [
                     (1, 8888, u'[4, 11]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze^7": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                 ]
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))  
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        ##item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})



        ########stemmed_search=Truee #
        ### Case 1.2:
        syntagma = ["klitz", "klein"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",stemmed_search=True)
        #p(item,"item")
        #self.pretty_print_uniq(item)


        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]


        right_repl = [
                     (1, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (2, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'e', 7, 5, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (20, 10000, u'[12, 3, 8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]'),
                     (42, 10000, u'[12, 3, 8]', u'[2, 5]', u'[2, 3]', u'klitz', u'kli^4tz', u'klitz', u'i', 4, 2, u'[2, 3]', u'NE', u'["neutral", 0.0]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                     (43, 10000, u'[12, 3, 8]', u'[2, 6]', u'[2, 3]', u'klitz', u'kli^4tz^3', u'klitz', u'i', 4, 2, u'[2, 3]', u'NE', u'["neutral", 0.0]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                     (44, 10000, u'[12, 3, 8]', u'[2, 6]', u'[2, 3]', u'klitz', u'kli^4tz^3', u'klitz', u'z', 3, 4, u'[2, 3]', u'NE', u'["neutral", 0.0]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                     (49, 10000, u'[12, 3, 8]', u'[2, 10]', u'[2, 6]', u'klitzes', u'klitzes^4', u'klitz', u's', 4, 6, u'[2, 6]', u'FM', u'["neutral", 0.0]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                     (50, 10000, u'[12, 3, 8]', u'[2, 11]', u'[2, 6]', u'klitzes', u'kli^3tzes^3', u'klitz', u'i', 3, 2, u'[2, 6]', u'FM', u'["neutral", 0.0]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                     (51, 10000, u'[12, 3, 8]', u'[2, 11]', u'[2, 6]', u'klitzes', u'kli^3tzes^3', u'klitz', u's', 3, 6, u'[2, 6]', u'FM', u'["neutral", 0.0]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                     (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                     (45, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'e', 3, 2, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (46, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'i', 3, 3, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (47, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'n', 3, 4, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (48, 10000, u'[12, 3, 8]', u'[2, 8]', u'[2, 4]', u'klein', u'klein^5', u'klein', u'n', 5, 4, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (52, 10000, u'[12, 3, 8]', u'[2, 12]', u'[2, 7]', u'kleines', u'klein^3e^2s', u'klein', u'n', 3, 4, u'[2, 7]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                     (53, 10000, u'[12, 3, 8]', u'[2, 13]', u'[2, 7]', u'kleines', u'kleines^4', u'klein', u's', 4, 6, u'[2, 7]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                 ]


        right_syntagma = [u'klitz', u'klein']


        right_baseline = [[[u'klitzes', u'kleines'], u'klitz++klein', 2, 1, u'[2, 2]', u'[3, 2]', u'[1, 1]', u'[2, 2]', u'1', u'1'], [[u'klitz', u'klein'], u'klitz++klein', 2, 1, u'[2, 2]', u'[3, 4]', u'[1, 1]', u'[3, 2]', u'1', u'1'], [[u'klitze', u'kleine'], u'klitz++klein', 2, 4, u'[2, 3]', u'[3, 4]', u'[1, 1]', u'[2, 2]', u'2', u'1']]


        right_redu = [
                     (1, 8888, u'[4, 11]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze^7": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (13, 10000, u'[12, 3, 8]', u'[2, 4]', u'[2, 3]', u'klitz', u'klitz', u'{"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}', 3, u'NE', u'["neutral", 0.0]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                     (15, 10000, u'[12, 3, 8]', u'[2, 10]', u'[2, 6]', u'klitzes', u'klitz', u'{"klitzes^4": 1, "kli^3tzes^3": 1}', 2, u'FM', u'["neutral", 0.0]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                     (2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (14, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'klein', u'{"kle^3i^3n^3": 1, "klein^5": 1}', 2, u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                     (16, 10000, u'[12, 3, 8]', u'[2, 12]', u'[2, 7]', u'kleines', u'klein', u'{"klein^3e^2s": 1, "kleines^4": 1}', 2, u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                 ]


        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))  
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        ##item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})




        ########get_also_non_full_repetativ_result=True #
        ### Case 1.3:
        syntagma = [u'.', u'kleinere', u'auswahl']
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",stemmed_search=False,get_also_non_full_repetativ_result=True)
        #p(item,"item")
        #self.pretty_print_uniq(item)


        right_repl = [
                     (36, 10000, u'[12, 3, 8]', u'[1, 4]', u'[1, 2]', u'.', u'.^5', u'.', u'.', 5, 0, None, u'symbol', u'["neutral", 0.0]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]'),
                     (37, 10000, u'[12, 3, 8]', u'[2, 0]', u'[2, 0]', u'kleinere', u'kleinere^5', u'klein', u'e', 5, 7, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                     (38, 10000, u'[12, 3, 8]', u'[2, 1]', u'[2, 0]', u'kleinere', u'kleine^3r^2e^5', u'klein', u'e', 3, 5, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                     (39, 10000, u'[12, 3, 8]', u'[2, 1]', u'[2, 0]', u'kleinere', u'kleine^3r^2e^5', u'klein', u'e', 5, 7, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                     (40, 10000, u'[12, 3, 8]', u'[2, 2]', u'[2, 1]', u'auswahl', u'auswah^3l^4', u'auswahl', u'h', 3, 5, None, u'NN', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]'),
                     (41, 10000, u'[12, 3, 8]', u'[2, 2]', u'[2, 1]', u'auswahl', u'auswah^3l^4', u'auswahl', u'l', 4, 6, None, u'NN', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]'),
                 ]


        right_syntagma = [u'.', u'kleinere', u'auswahl']


        right_baseline = [[[u'.', u'kleinere', u'auswahl'], u'.++klein++auswahl', 3, 1, u'[1, 2, 1]', u'[1, 3, 2]', None, None, u'1', None]]


        right_redu = [(12, 10000, u'[12, 3, 8]', u'[2, 0]', u'[2, 0]', u'kleinere', u'klein', u'{"kleinere^5": 1, "kleine^3r^2e^5": 1}', 2, u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]')]




        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]


        # set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))  
        # set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        # list( lunicode(str(elem) for elem in  item ) for item in extracted_baseline).should.be.equal(list( list(  unicode(elem) for elem in  item ) for item in right_baseline))
        # extracted_syntagma.should.be.equal(right_syntagma)

        #item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})










    # # ################################################################################################################################################
    # # ################################################################################################################################################
    # # ##### return_full_tuple = True #######################################################################################################+
    # # ###########################################################################################################################################
    # # ################################################################################################################################################



    # # ############################
    # # ####### SCOPE 1 ##############
    # # ############################


        ####################### syntagma_type="lexem" #############################

        ### Case 1.1:
        syntagma = ["klitze"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem", return_full_tuple=True)
        #self.pretty_print_uniq(item)
        #p(item,"item")

        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]


        right_repl = (
                         [
                             (54, 11111, u'[5, 6, 15, 3]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'sache', u'["NN", null, "sach"]', u'.', u'["symbol", null, "."]', u'die', u'["PDS", null, "die"]', u'aber', u'["ADV", null, "aber"]'),
                             (1, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                             (2, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'e', 7, 5, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                             (20, 10000, u'[12, 3, 8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]'),
                         ],
                         True,
                         None,
             )


        right_syntagma = ['klitze']


        right_baseline = [[[u'klitze'], u'klitz', 1, 8, u'3', u'4', u'2', u'6', u'3', u'2']]


        right_redu = (
                         [
                             (18, 12222, u'[24]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitz', u'{"klitze": 4}', 4, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u',', u'["symbol", null, ","]', u'die', u'["PRELS", null, "die"]', u'ich', u'["PPER", null, "ich"]'),
                             (1, 8888, u'[4, 11]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze^7": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                         ],
                         True,
                         None,
             )

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        ##item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})



    # # # ############################
    # # # ####### SCOPE 2 ##############
    # # # ############################


        ####################### syntagma_type="lexem" #############################

        ### Case 1.1:
        syntagma = ["klitze", "kleine"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem", return_full_tuple=True)
        #p(item,"item")
        #self.pretty_print_uniq(item)


        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]


        right_repl = (
                         [
                             (1, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                             (2, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'e', 7, 5, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                             (20, 10000, u'[12, 3, 8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]'),
                             (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                         ],
                         True,
                         2,
             )


        right_syntagma = ['klitze', 'kleine']


        right_baseline = [[[u'klitze', u'kleine'], u'klitz++klein', 2, 4, u'[2, 3]', u'[3, 4]', u'[1, 1]', u'[2, 2]', u'2', u'1']]


        right_redu = (
                         [
                             (1, 8888, u'[4, 11]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze^7": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                             (2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                         ],
                         True,
                         1,
             )

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        ##item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})







    # # ################################################################################################################################################
    # # ################################################ II. FullRepetativnes= False   #################################################################################
    # # ########################################################################################################################################
        stats.recompute_syntagma_repetativity_scope(False)

    # # # ############################
    # # # ####### SCOPE 2 ##############
    # # # ############################


        ####################### syntagma_type="lexem" #############################

        ### Case 1.1:
        syntagma = ["klitze", "kleine"]
        item = stats._get_data_for_one_syntagma(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #p(item,"item")
        #self.pretty_print_uniq(item)


        extracted_repl = item["repl"]
        extracted_redu = item["redu"]
        extracted_baseline = item["baseline"]
        extracted_syntagma = item["syntagma"]



        right_repl = [
                     (54, 11111, u'[5, 6, 15, 3]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'sache', u'["NN", null, "sach"]', u'.', u'["symbol", null, "."]', u'die', u'["PDS", null, "die"]', u'aber', u'["ADV", null, "aber"]'),
                     (1, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (2, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'e', 7, 5, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (20, 10000, u'[12, 3, 8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]'),
                     (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                 ]


        right_syntagma = ['klitze', 'kleine']


        right_baseline = [[[u'klitze', u'kleine'], u'klitz++klein', 2, 4, u'[3, 3]', u'[4, 4]', u'[2, 1]', u'[6, 2]', None, None]]


        right_redu = [
                     (18, 12222, u'[24]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitz', u'{"klitze": 4}', 4, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u',', u'["symbol", null, ","]', u'die', u'["PRELS", null, "die"]', u'ich', u'["PPER", null, "ich"]'),
                     (1, 8888, u'[4, 11]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze^7": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                 ]


        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        ##item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma})



        ####################### syntagma_type="pos" #############################








    @attr(status='stable')
    #@wipd
    def test_get_data_611_2(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()

        #### DE ######
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True, status_bar=True)#, )
        

        ######### EN ########

        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_en))

        ###### 3
        syntagma = ["EMOIMG","EMOIMG"]
        data1 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=False,if_type_pos_return_lexem_syn=False))
        repl1 = sorted(data1[0]["repl"])
        redu1 = sorted(data1[0]["redu"])

        data2 =  list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=False,if_type_pos_return_lexem_syn=True))
        ext_id = []
        repl2 = []
        for item in data2:
            for r in item["repl"]:
                if r[0] not in ext_id:
                    ext_id.append(r[0])
                    repl2.append(r)

        ext_id = []
        redu2 = []
        for item in data2:
            for r in item["redu"]:
                if r[0] not in ext_id:
                    ext_id.append(r[0])
                    redu2.append(r)


        #repl2 = sorted([r for item in data2  )
        #redu2 = sorted([r for item in data2  for r in item["redu"]])

        assert len(repl1)<= len(repl2)
        assert len(redu1)<= len(redu2)
        #p((repl1, repl2))
        #p((redu1, redu2))





        #--------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------

        ######### DE #######
        stats.close()
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))
        
    ################################################################################################
    ################################################################################################
    ###################################################################################################
    ############################stemmed_search = False #########################################
    #################################################################################################
    ################################################################################################
    ################################################################################################
#
 

    ################################################################################################################################################
    ################################################ II. FullRepetativnes= True   #################################################################################
    ########################################################################################################################################
        stats.recompute_syntagma_repetativity_scope(True)

        ### Case 0:
        syntagma = ["big"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem"))
        #p(data,"data")
        data.should.be.equal([])


        # # # # ####################################################################################
        # # # # ####################################################################################
        # # # # #################################################################################


        ### Case 1.1:
        syntagma = ["kleine"]
        data = stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem")
        #p()
        len1 = len(data)
        data = list(data)
        len2 = len(data)
        len1.should.be.equal(len2)
        #p(data,"data")
        #self.pretty_print_uniq(data[0])


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]



        right_repl = [
                     (82, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 4, 2, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (83, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'i', 5, 3, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (84, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (85, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 8, 5, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                     (57, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (58, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (59, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 5, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                 ]


        right_syntagma = [u'kleine']


        right_baseline = [[[u'kleine'], u'klein', 1, 7, u'5', u'11', u'1', u'2', u'5', u'1']]


        right_redu = [(2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]')]



        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])




        # # # ####################################################################################
        # # # ######################GET JUST FEW COLUMNS ##################################
        # # # ################################################################################

        ### Case 1.2:
        columns_repl=['doc_id', 'redufree_len','index_in_redufree','index_in_corpus']
        columns_redu = ['doc_id', 'redufree_len','index_in_redufree', 'index_in_corpus',"redu_length"]
        columns_baseline = ['syntagma', 'occur_syntagma_all', "scope"]
        #columns_baseline = 
        syntagma = ["kleine"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem", get_columns_repl=columns_repl , get_columns_redu=columns_redu, get_columns_baseline=columns_baseline ))
        #p(data,"data")
        #self.pretty_print_uniq(data[0])


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]

        right_repl = [
                     [12222, u'[24]', u'[0, 21]', u'[0, 24]'],
                     [12222, u'[24]', u'[0, 21]', u'[0, 24]'],
                     [12222, u'[24]', u'[0, 21]', u'[0, 24]'],
                     [12222, u'[24]', u'[0, 21]', u'[0, 24]'],
                     [8888, u'[4, 11]', u'[0, 1]', u'[0, 2]'],
                     [8888, u'[4, 11]', u'[0, 1]', u'[0, 2]'],
                     [8888, u'[4, 11]', u'[0, 1]', u'[0, 3]'],
                     [10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]'],
                     [11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]'],
                     [11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]'],
                     [11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]'],
                 ]


        right_syntagma = [u'kleine']


        right_baseline = [[[u'kleine'], 7, 1]]


        right_redu = [[8888, u'[4, 11]', u'[0, 1]', u'[0, 2]', 2]]
        #p(self.convert_all_lists_to_tuples(extracted_repl))
        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])




        # # # ####################################################################################
        # # # ##################### #GET ORDERED SYNTAGMA (SCOPE 1) ##################################
        # # # ##############################################################################

        ### Case 1.3: #order_output_by_syntagma_order
        syntagma = ["kleine"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",order_output_by_syntagma_order=True))
        #p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=True)

        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]


        right_repl = [
                    (u'kleine', (
                                 (82, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 4, 2, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                 (83, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'i', 5, 3, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                 (84, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                 (85, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 8, 5, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                 (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                                 (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                                 (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                                 (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                                 (57, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                                 (58, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                                 (59, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 5, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                             )
                      ),
                 ]


        right_syntagma = [u'kleine']


        right_baseline = [[[u'kleine'], u'klein', 1, 7, u'5', u'11', u'1', u'2', u'5', u'1']]


        right_redu = [
                    (u'kleine', (
                                 (2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             )
                      ),
                 ]

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])






        # # # ####################################################################################
        # # # ######################GET JUST FEW PHENOMENA AND NOT ALL#########################
        # # # ####################################################################################

        ### Case 2.1:
        ### repl=True,redu=False, baseline=False
        syntagma = ["kleine"]
        data = list(stats.get_data(syntagma, repl=True, redu=False, baseline=False, sentiment=False, syntagma_type="lexem"))
        #p(data,"data")
        #self.pretty_print_uniq(data[0])


        right_repl = [
                     (82, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 4, 2, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (83, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'i', 5, 3, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (84, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (85, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 8, 5, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                     (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                     (57, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (58, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                     (59, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 5, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                 ]


        right_syntagma = [u'kleine']


        right_baseline = []


        right_redu = []

        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]



        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])




        ### Case 2.2:
        ### repl=False,redu=True, baseline=False
        syntagma = ["kleine"]
        data = list(stats.get_data(syntagma, repl=False, redu=True, baseline=False, sentiment=False, syntagma_type="lexem"))
        #p(data,"data")
        #self.pretty_print_uniq(data[0])


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]





        right_repl = []


        right_syntagma = [u'kleine']


        right_baseline = []


        right_redu = [(2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]')]

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])





        ### Case 2.3:
        ### repl=False,redu=False, baseline=True
        syntagma = ["kleine"]
        data = list(stats.get_data(syntagma, repl=False, redu=False, baseline=True, sentiment=False, syntagma_type="lexem"))
        #p(data,"data")
        #self.pretty_print_uniq(data[0])


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]


        right_repl = []


        right_syntagma = [u'kleine']


        right_baseline = [[[u'kleine'], u'klein', 1, 7, u'5', u'11', u'1', u'2', u'5', u'1']]


        right_redu = []

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])





        # # # ####################################################################################
        # # # #################. GET ORDERED/UNORDERED OUTPUT #################################
        # # # # #################################################################################

        ### Case 3.1: 
        #order_output_by_syntagma_order = True
        # full_tuple = False
        syntagma = ["kleine","Überaschung"] 
        data = stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",order_output_by_syntagma_order=True,return_full_tuple=False)
        len1 = len(data)
        data = list(data)
        len2 = len(data)
        len1.should.be.equal(len2)
        #p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=True)


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]


        right_repl = [
                    (u'kleine', (
                                 (82, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 4, 2, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                 (83, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'i', 5, 3, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                 (84, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                 (85, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 8, 5, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                 (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                                 (57, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                                 (58, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                                 (59, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 5, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                             )
                      ),
                    (u'\xfcberaschung', (
                                 (86, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'e', 4, 2, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                 (87, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'r', 5, 3, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                 (88, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'a', 3, 4, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                 (89, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'n', 6, 9, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                 (90, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'g', 3, 10, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                 (22, 10000, u'[12, 3, 8]', u'[0, 3]', u'[0, 3]', u'\xfcberaschung', u'\xfcber^4aschung', u'uberasch', u'r', 4, 3, None, u'NN', u'["neutral", 0.0]', None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'kleine', u'["ADJA", null, "klein"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]'),
                                 (60, 11111, u'[5, 6, 15, 3]', u'[2, 5]', u'[2, 5]', u'\xfcberaschung', u'\xfcber^5aschung', u'uberasch', u'r', 5, 3, None, u'NN', u'["neutral", 0.0]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]'),
                             )
                      ),
                 ]


        right_syntagma = [u'kleine', u'\xfcberaschung']


        right_baseline = [[[u'kleine', u'\xfcberaschung'], u'klein++uberasch', 2, 5, u'[3, 3]', u'[8, 7]', None, None, u'3', None]]


        right_redu = ()

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])


        ### Case 3.2: 
        #order_output_by_syntagma_order = True
        # full_tuple = True
        syntagma = ["kleine","Überaschung"] 
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",order_output_by_syntagma_order=True,return_full_tuple=True))
        #p(data,"data")
        #p(data[0],"data[0]")
        #self.pretty_print_uniq(data[0],syn_order=True)



        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]




        right_repl = (
                         [
                            (u'kleine', (
                                         (82, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 4, 2, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                         (83, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'i', 5, 3, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                         (84, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                         (85, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 8, 5, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                                         (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                                         (57, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                                         (58, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                                         (59, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 5, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                                         )
                                  ),
                            (u'\xfcberaschung', (
                                         (86, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'e', 4, 2, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                         (87, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'r', 5, 3, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                         (88, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'a', 3, 4, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                         (89, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'n', 6, 9, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                         (90, 12222, u'[24]', u'[0, 25]', u'[0, 22]', u'\xfcberaschung', u'\xfcbe^4r^5a^3schun^6g^3', u'uberasch', u'g', 3, 10, None, u'NN', u'["neutral", 0.0]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None, None, None),
                                         (22, 10000, u'[12, 3, 8]', u'[0, 3]', u'[0, 3]', u'\xfcberaschung', u'\xfcber^4aschung', u'uberasch', u'r', 4, 3, None, u'NN', u'["neutral", 0.0]', None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'kleine', u'["ADJA", null, "klein"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]'),
                                         (60, 11111, u'[5, 6, 15, 3]', u'[2, 5]', u'[2, 5]', u'\xfcberaschung', u'\xfcber^5aschung', u'uberasch', u'r', 5, 3, None, u'NN', u'["neutral", 0.0]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]'),
                                         )
                                  ),
                         ],
                         True,
                         3,
                 )


        right_syntagma = [u'kleine', u'\xfcberaschung']


        right_baseline = [[[u'kleine', u'\xfcberaschung'], u'klein++uberasch', 2, 5, u'[3, 3]', u'[8, 7]', None, None, u'3', None]]


        right_redu = None



        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        extracted_redu.should.be.equal(right_redu)
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])





        ### Case 3.3:
        #order_output_by_syntagma_order
        syntagma = ["klitze","kleine", "überaschung"] 
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",order_output_by_syntagma_order=True))
        #p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=True)


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]


        right_repl = [
                    (u'klitze', (
                                 (20, 10000, u'[12, 3, 8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]'),
                             )
                      ),
                    (u'kleine', (
                                 (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                             )
                      ),
                    (u'\xfcberaschung', (
                                 (22, 10000, u'[12, 3, 8]', u'[0, 3]', u'[0, 3]', u'\xfcberaschung', u'\xfcber^4aschung', u'uberasch', u'r', 4, 3, None, u'NN', u'["neutral", 0.0]', None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'kleine', u'["ADJA", null, "klein"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]'),
                             )
                      ),
                 ]


        right_syntagma = [u'klitze', u'kleine', u'\xfcberaschung']


        right_baseline = [[[u'klitze', u'kleine', u'\xfcberaschung'], u'klitz++klein++uberasch', 3, 3, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None]]


        right_redu = ()




        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)

        # #data.should.be.equal([{"repl":right_repl, "redu":right_redu,"baseline":right_baseline, "syntagma":right_syntagma}])



        # # # ####################################################################################
        # # # #################. WORK WITH POS   #########################################
        # # # ##############################################################################


        # ### Case 5.1:
        #full_repetativ_syntagma=False
        syntagma = ["NN", "NE"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos"))
        #p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=False)

        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]




        right_repl = [
                     (1, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (2, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'e', 7, 5, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                     (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                 ]


        right_syntagma = [u'NN', u'NE']


        right_baseline = [[[u'klitze', u'kleine', u'\xfcberaschung'], u'klitz++klein++uberasch', 3, 3, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'klitze', u'kleine'], u'klitz++klein', 2, 4, u'[2, 3]', u'[3, 4]', u'[1, 1]', u'[2, 2]', u'2', u'1'], [[u'klitze'], u'klitz', 1, 8, u'3', u'4', u'2', u'6', u'3', u'2'], [[u'klitze', u'kleine', u'\xfcberaschung', u'.'], u'klitz++klein++uberasch++.', 4, 1, None, None, None, None, None, None], [[u'kleine'], u'klein', 1, 7, u'5', u'11', u'1', u'2', u'5', u'1'], [[u'klitze', u'kleine', u'\xfcberaschung', u'.', u'trotzdem', u'hat'], u'klitz++klein++uberasch++.++trotzd++hat', 6, 1, None, None, None, None, None, None], [[u'kleine', u'\xfcberaschung', u'.', u'trotzdem'], u'klein++uberasch++.++trotzd', 4, 1, None, None, None, None, None, None], [[u'kleine', u'\xfcberaschung', u'.'], u'klein++uberasch++.', 3, 2, None, None, None, None, None, None], [[u'kleine', u'\xfcberaschung', u'.', u'trotzdem', u'hat'], u'klein++uberasch++.++trotzd++hat', 5, 1, None, None, None, None, None, None], [[u'klitze', u'kleine', u'\xfcberaschung', u'.', u'trotzdem'], u'klitz++klein++uberasch++.++trotzd', 5, 1, None, None, None, None, None, None], [[u'kleine', u'\xfcberaschung', u'.', u'trotzdem', u'hat', u'sie'], u'klein++uberasch++.++trotzd++hat++sie', 6, 1, None, None, None, None, None, None], [[u'kleine', u'\xfcberaschung'], u'klein++uberasch', 2, 5, u'[3, 3]', u'[8, 7]', None, None, u'3', None]]


        right_redu = [
                     (1, 8888, u'[4, 11]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze^7": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                     (2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                 ]


        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)









        # # # ####################################################################################
        # # # ################ #WORK WITH NUMBERS##########################################
        # # # #################################################################################


        # ### Case 6.1:
        syntagma = ["number"]
        data = stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos")
        len1 = len(data)
        data = list(data)
        len2 = len(data)
        len1.should.be.equal(len2)
        #p((len1, len2))
        # p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=False)


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]



        right_repl = [
                     (78, 12222, u'[24]', u'[0, 14]', u'[0, 11]', u'1', u'1^6', u'1', u'1', 6, 0, None, u'number', u'["neutral", 0.0]', u'ich', u'["PPER", null, "ich"]', u'mal', u'["PTKMA", null, "mal"]', u'gerne', u'["ADV", null, "gern"]', u'hate', u'["VAFIN", null, "hat"]', u'.', u'["symbol", null, "."]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', 1, u'["number", null, "1"]', u'du', u'["PPER", null, "du"]', u'meintest', u'["VVFIN", null, "meint"]', u',', u'["symbol", null, ","]'),
                     (80, 12222, u'[24]', u'[0, 16]', u'[0, 13]', u'1', u'1^8', u'1', u'1', 8, 0, None, u'number', u'["neutral", 0.0]', u'gerne', u'["ADV", null, "gern"]', u'hate', u'["VAFIN", null, "hat"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', u'\U0001f62b', u'["EMOIMG", null, "\\ud83d\\ude2b"]', u'du', u'["PPER", null, "du"]', u'meintest', u'["VVFIN", null, "meint"]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]'),
                     (61, 11111, u'[5, 6, 15, 3]', u'[2, 8]', u'[2, 8]', u'1', u'1^5', u'1', u'1', 5, 0, None, u'number', u'["neutral", 0.0]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]'),
                     (62, 11111, u'[5, 6, 15, 3]', u'[2, 9]', u'[2, 9]', u'2', u'2^4', u'2', u'2', 4, 0, None, u'number', u'["neutral", 0.0]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]'),
                     (63, 11111, u'[5, 6, 15, 3]', u'[2, 10]', u'[2, 10]', u'3', u'3^5', u'3', u'3', 5, 0, None, u'number', u'["neutral", 0.0]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]'),
                     (64, 11111, u'[5, 6, 15, 3]', u'[2, 11]', u'[2, 11]', u'4', u'4^4', u'4', u'4', 4, 0, None, u'number', u'["neutral", 0.0]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]'),
                     (65, 11111, u'[5, 6, 15, 3]', u'[2, 12]', u'[2, 12]', u'5', u'5^5', u'5', u'5', 5, 0, None, u'number', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]'),
                 ]


        right_syntagma = [u'number']


        right_baseline = [[[u'1', u'\U0001f62b', u'1', u'du', u'meintest'], u'1++\U0001f62b++1++du++meint', 5, 1, None, None, None, None, None, None], [[u'3', u'4', u'5', u'6', u'.', u'kleines'], u'3++4++5++6++.++klein', 6, 1, None, None, None, None, None, None], [[u'3', u'4', u'5', u'6'], u'3++4++5++6', 4, 1, None, None, None, None, None, None], [[u'1', u'2'], u'1++2', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'5', u'6'], u'5++6', 2, 1, None, None, None, None, None, None], [[u'1', u'\U0001f62b', u'1', u'du', u'meintest', u','], u'1++\U0001f62b++1++du++meint++,', 6, 1, None, None, None, None, None, None], [[u'2'], u'2', 1, 1, u'1', u'1', None, None, u'1', None], [[u'1', u'2', u'3', u'4'], u'1++2++3++4', 4, 1, u'[1, 1, 1, 1]', u'[1, 1, 1, 1]', None, None, u'1', None], [[u'2', u'3', u'4', u'5', u'6'], u'2++3++4++5++6', 5, 1, None, None, None, None, None, None], [[u'1', u'\U0001f62b'], u'1++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'5', u'6', u'.', u'kleines'], u'5++6++.++klein', 4, 1, None, None, None, None, None, None], [[u'3', u'4'], u'3++4', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'1', u'du', u'meintest', u','], u'1++du++meint++,', 4, 1, None, None, None, None, None, None], [[u'1', u'2', u'3', u'4', u'5', u'6'], u'1++2++3++4++5++6', 6, 1, None, None, None, None, None, None], [[u'4', u'5', u'6', u'.', u'kleines', u'm\xe4dchen'], u'4++5++6++.++klein++madch', 6, 1, None, None, None, None, None, None], [[u'1', u'\U0001f62b', u'1', u'du'], u'1++\U0001f62b++1++du', 4, 1, None, None, None, None, None, None], [[u'2', u'3', u'4'], u'2++3++4', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'3', u'4', u'5'], u'3++4++5', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'4', u'5', u'6', u'.'], u'4++5++6++.', 4, 1, None, None, None, None, None, None], [[u'4'], u'4', 1, 1, u'1', u'1', None, None, u'1', None], [[u'1', u'2', u'3'], u'1++2++3', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'1', u'du'], u'1++du', 2, 1, None, None, None, None, None, None], [[u'1'], u'1', 1, 3, u'3', u'3', None, None, u'3', None], [[u'2', u'3'], u'2++3', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'3'], u'3', 1, 1, u'1', u'1', None, None, u'1', None], [[u'4', u'5', u'6'], u'4++5++6', 3, 1, None, None, None, None, None, None], [[u'1', u'\U0001f62b', u'1'], u'1++\U0001f62b++1', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, u'1', None], [[u'5'], u'5', 1, 1, u'1', u'1', None, None, u'1', None], [[u'4', u'5', u'6', u'.', u'kleines'], u'4++5++6++.++klein', 5, 1, None, None, None, None, None, None], [[u'5', u'6', u'.'], u'5++6++.', 3, 1, None, None, None, None, None, None], [[u'2', u'3', u'4', u'5', u'6', u'.'], u'2++3++4++5++6++.', 6, 1, None, None, None, None, None, None], [[u'1', u'du', u'meintest', u',', u'es'], u'1++du++meint++,++es', 5, 1, None, None, None, None, None, None], [[u'5', u'6', u'.', u'kleines', u'm\xe4dchen', u'.'], u'5++6++.++klein++madch++.', 6, 1, None, None, None, None, None, None], [[u'3', u'4', u'5', u'6', u'.'], u'3++4++5++6++.', 5, 1, None, None, None, None, None, None], [[u'1', u'du', u'meintest', u',', u'es', u'war'], u'1++du++meint++,++es++war', 6, 1, None, None, None, None, None, None], [[u'2', u'3', u'4', u'5'], u'2++3++4++5', 4, 1, u'[1, 1, 1, 1]', u'[1, 1, 1, 1]', None, None, u'1', None], [[u'1', u'du', u'meintest'], u'1++du++meint', 3, 1, None, None, None, None, None, None], [[u'1', u'2', u'3', u'4', u'5'], u'1++2++3++4++5', 5, 1, u'[1, 1, 1, 1, 1]', u'[1, 1, 1, 1, 1]', None, None, u'1', None], [[u'5', u'6', u'.', u'kleines', u'm\xe4dchen'], u'5++6++.++klein++madch', 5, 1, None, None, None, None, None, None], [[u'4', u'5'], u'4++5', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None]]


        right_redu = ()

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)






        # ### Case 6.2:
        #### Problem, by repetativ syntagmas -> repetativ rep_ids
        syntagma = ["number","number"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos"))
        # p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=False)


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]



        right_repl = [
                     (61, 11111, u'[5, 6, 15, 3]', u'[2, 8]', u'[2, 8]', u'1', u'1^5', u'1', u'1', 5, 0, None, u'number', u'["neutral", 0.0]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]'),
                     (62, 11111, u'[5, 6, 15, 3]', u'[2, 9]', u'[2, 9]', u'2', u'2^4', u'2', u'2', 4, 0, None, u'number', u'["neutral", 0.0]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]'),
                     (63, 11111, u'[5, 6, 15, 3]', u'[2, 10]', u'[2, 10]', u'3', u'3^5', u'3', u'3', 5, 0, None, u'number', u'["neutral", 0.0]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]'),
                     (64, 11111, u'[5, 6, 15, 3]', u'[2, 11]', u'[2, 11]', u'4', u'4^4', u'4', u'4', 4, 0, None, u'number', u'["neutral", 0.0]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]'),
                 ]


        right_syntagma = [u'number', u'number']


        right_baseline = [[[u'3', u'4', u'5', u'6', u'.', u'kleines'], u'3++4++5++6++.++klein', 6, 1, None, None, None, None, None, None], [[u'3', u'4', u'5', u'6'], u'3++4++5++6', 4, 1, None, None, None, None, None, None], [[u'1', u'2'], u'1++2', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'2'], u'2', 1, 1, u'1', u'1', None, None, u'1', None], [[u'1', u'2', u'3', u'4'], u'1++2++3++4', 4, 1, u'[1, 1, 1, 1]', u'[1, 1, 1, 1]', None, None, u'1', None], [[u'2', u'3', u'4', u'5', u'6'], u'2++3++4++5++6', 5, 1, None, None, None, None, None, None], [[u'3', u'4'], u'3++4', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'1', u'2', u'3', u'4', u'5', u'6'], u'1++2++3++4++5++6', 6, 1, None, None, None, None, None, None], [[u'4', u'5', u'6', u'.', u'kleines', u'm\xe4dchen'], u'4++5++6++.++klein++madch', 6, 1, None, None, None, None, None, None], [[u'2', u'3', u'4'], u'2++3++4', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'3', u'4', u'5'], u'3++4++5', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'4', u'5', u'6', u'.'], u'4++5++6++.', 4, 1, None, None, None, None, None, None], [[u'4'], u'4', 1, 1, u'1', u'1', None, None, u'1', None], [[u'1', u'2', u'3'], u'1++2++3', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'1'], u'1', 1, 3, u'3', u'3', None, None, u'3', None], [[u'2', u'3'], u'2++3', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'3'], u'3', 1, 1, u'1', u'1', None, None, u'1', None], [[u'4', u'5', u'6', u'.', u'kleines'], u'4++5++6++.++klein', 5, 1, None, None, None, None, None, None], [[u'2', u'3', u'4', u'5', u'6', u'.'], u'2++3++4++5++6++.', 6, 1, None, None, None, None, None, None], [[u'4', u'5', u'6'], u'4++5++6', 3, 1, None, None, None, None, None, None], [[u'3', u'4', u'5', u'6', u'.'], u'3++4++5++6++.', 5, 1, None, None, None, None, None, None], [[u'2', u'3', u'4', u'5'], u'2++3++4++5', 4, 1, u'[1, 1, 1, 1]', u'[1, 1, 1, 1]', None, None, u'1', None], [[u'1', u'2', u'3', u'4', u'5'], u'1++2++3++4++5', 5, 1, u'[1, 1, 1, 1, 1]', u'[1, 1, 1, 1, 1]', None, None, u'1', None], [[u'4', u'5'], u'4++5', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None]]


        right_redu = ()




        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)





        # ### Case 6.3:
        syntagma = ["number","number","number"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos"))
        # p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=False)


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]



        right_repl = [
                     (61, 11111, u'[5, 6, 15, 3]', u'[2, 8]', u'[2, 8]', u'1', u'1^5', u'1', u'1', 5, 0, None, u'number', u'["neutral", 0.0]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]'),
                     (62, 11111, u'[5, 6, 15, 3]', u'[2, 9]', u'[2, 9]', u'2', u'2^4', u'2', u'2', 4, 0, None, u'number', u'["neutral", 0.0]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]'),
                     (63, 11111, u'[5, 6, 15, 3]', u'[2, 10]', u'[2, 10]', u'3', u'3^5', u'3', u'3', 5, 0, None, u'number', u'["neutral", 0.0]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]'),
                 ]


        right_syntagma = [u'number', u'number', u'number']


        right_baseline = [[[u'1', u'2', u'3', u'4'], u'1++2++3++4', 4, 1, u'[1, 1, 1, 1]', u'[1, 1, 1, 1]', None, None, u'1', None], [[u'2', u'3', u'4'], u'2++3++4', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'2', u'3', u'4', u'5', u'6'], u'2++3++4++5++6', 5, 1, None, None, None, None, None, None], [[u'2', u'3', u'4', u'5', u'6', u'.'], u'2++3++4++5++6++.', 6, 1, None, None, None, None, None, None], [[u'3', u'4', u'5', u'6', u'.', u'kleines'], u'3++4++5++6++.++klein', 6, 1, None, None, None, None, None, None], [[u'1', u'2'], u'1++2', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'3', u'4', u'5', u'6'], u'3++4++5++6', 4, 1, None, None, None, None, None, None], [[u'3', u'4'], u'3++4', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'1', u'2', u'3'], u'1++2++3', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'1'], u'1', 1, 3, u'3', u'3', None, None, u'3', None], [[u'2', u'3'], u'2++3', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'1', u'2', u'3', u'4', u'5', u'6'], u'1++2++3++4++5++6', 6, 1, None, None, None, None, None, None], [[u'2', u'3', u'4', u'5'], u'2++3++4++5', 4, 1, u'[1, 1, 1, 1]', u'[1, 1, 1, 1]', None, None, u'1', None], [[u'3'], u'3', 1, 1, u'1', u'1', None, None, u'1', None], [[u'2'], u'2', 1, 1, u'1', u'1', None, None, u'1', None], [[u'1', u'2', u'3', u'4', u'5'], u'1++2++3++4++5', 5, 1, u'[1, 1, 1, 1, 1]', u'[1, 1, 1, 1, 1]', None, None, u'1', None], [[u'3', u'4', u'5'], u'3++4++5', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'3', u'4', u'5', u'6', u'.'], u'3++4++5++6++.', 5, 1, None, None, None, None, None, None]]


        right_redu = ()


        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)





        # ### Case 6.4:#
        syntagma = ["number","number","number"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=True))
        #p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=False)

        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]



        right_repl = [
                     (u'number', ((61, 11111, u'[5, 6, 15, 3]', u'[2, 8]', u'[2, 8]', u'1', u'1^5', u'1', u'1', 5, 0, None, u'number', u'["neutral", 0.0]', u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 2, u'["number", null, "2"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]'),)),
                     (u'number', ((62, 11111, u'[5, 6, 15, 3]', u'[2, 9]', u'[2, 9]', u'2', u'2^4', u'2', u'2', 4, 0, None, u'number', u'["neutral", 0.0]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]'),)),
                     (u'number', ((63, 11111, u'[5, 6, 15, 3]', u'[2, 10]', u'[2, 10]', u'3', u'3^5', u'3', u'3', 5, 0, None, u'number', u'["neutral", 0.0]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]'),)),
                 ]


        right_syntagma = [u'number', u'number', u'number']


        right_baseline = [[[u'1', u'2', u'3', u'4'], u'1++2++3++4', 4, 1, u'[1, 1, 1, 1]', u'[1, 1, 1, 1]', None, None, u'1', None], [[u'2', u'3', u'4'], u'2++3++4', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'2', u'3', u'4', u'5', u'6'], u'2++3++4++5++6', 5, 1, None, None, None, None, None, None], [[u'2', u'3', u'4', u'5', u'6', u'.'], u'2++3++4++5++6++.', 6, 1, None, None, None, None, None, None], [[u'3', u'4', u'5', u'6', u'.', u'kleines'], u'3++4++5++6++.++klein', 6, 1, None, None, None, None, None, None], [[u'1', u'2'], u'1++2', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'3', u'4', u'5', u'6'], u'3++4++5++6', 4, 1, None, None, None, None, None, None], [[u'3', u'4'], u'3++4', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'1', u'2', u'3'], u'1++2++3', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'1'], u'1', 1, 3, u'3', u'3', None, None, u'3', None], [[u'2', u'3'], u'2++3', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None], [[u'1', u'2', u'3', u'4', u'5', u'6'], u'1++2++3++4++5++6', 6, 1, None, None, None, None, None, None], [[u'2', u'3', u'4', u'5'], u'2++3++4++5', 4, 1, u'[1, 1, 1, 1]', u'[1, 1, 1, 1]', None, None, u'1', None], [[u'3'], u'3', 1, 1, u'1', u'1', None, None, u'1', None], [[u'2'], u'2', 1, 1, u'1', u'1', None, None, u'1', None], [[u'1', u'2', u'3', u'4', u'5'], u'1++2++3++4++5', 5, 1, u'[1, 1, 1, 1, 1]', u'[1, 1, 1, 1, 1]', None, None, u'1', None], [[u'3', u'4', u'5'], u'3++4++5', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None], [[u'3', u'4', u'5', u'6', u'.'], u'3++4++5++6++.', 5, 1, None, None, None, None, None, None]]


        right_redu = ()



        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)






        ### Case 6.5:#
        ###### 1
        syntagma = ["EMOIMG"]
        data1 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=False,if_type_pos_return_lexem_syn=False))
        repl1 = sorted(data1[0]["repl"])
        redu1 = sorted(data1[0]["redu"])

        data2 =  list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=False,if_type_pos_return_lexem_syn=True))
        repl2 = sorted([r for item in data2  for r in item["repl"]])
        redu2 = sorted([r for item in data2  for r in item["redu"]])

        repl1.should.be.equal(repl2)
        redu1.should.be.equal(redu2)
        #p((repl1, repl2))
        #p((redu1, redu2))

        ###### 2
        syntagma = ["EMOIMG","EMOASC"]
        data1 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=False,if_type_pos_return_lexem_syn=False))
        repl1 = sorted(data1[0]["repl"])
        redu1 = sorted(data1[0]["redu"])

        data2 =  list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=False,if_type_pos_return_lexem_syn=True))
        repl2 = sorted([r for item in data2  for r in item["repl"]])
        redu2 = sorted([r for item in data2  for r in item["redu"]])

        repl1.should.be.equal(repl2)
        redu1.should.be.equal(redu2)
        #p((repl1, repl2))
        #p((redu1, redu2))

        ###### 3
        syntagma = ["EMOASC"]
        data1 = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=False,if_type_pos_return_lexem_syn=False))
        repl1 = sorted(data1[0]["repl"])
        redu1 = sorted(data1[0]["redu"])

        data2 =  list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos", order_output_by_syntagma_order=False,if_type_pos_return_lexem_syn=True))
        ext_id = []
        repl2 = []
        for item in data2:
            for r in item["repl"]:
                if r[0] not in ext_id:
                    ext_id.append(r[0])
                    repl2.append(r)
        repl2 = sorted(repl2)

        ext_id = []
        redu2 = []
        for item in data2:
            for r in item["redu"]:
                if r[0] not in ext_id:
                    ext_id.append(r[0])
                    redu2.append(r)
        redu2 = sorted(redu2)


        if len(repl1) == len(repl2):
            assert repl1 == repl2
        else:
            assert len(repl1)<= len(repl2)

        if len(redu1) == len(redu2):
            assert redu1 == redu2
        else:
            assert len(redu1)<= len(redu2)


        #p((repl1, repl2))
        #p((redu1, redu2))


    ################################################################################################
    ################################################################################################
    ###################################################################################################
    ############################stemmed_search = True #########################################
    #################################################################################################
    ################################################################################################
    ################################################################################################


        ########stemmed_search=True #

        ### Case 10.1:
        syntagma = ["klitze","kleines"]
        items = stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",stemmed_search=True, )
        len1 = len(items)
        items = list(items)
        len2 = len(items)
        len1.should.be.equal(len2)
        #p((len1, len2))
        #self.pretty_print_uniq(item)
        #p(items,"item")

        for item in items:
            #p(item["syntagma"])

            if item["syntagma"] == [u'klitzes', u'kleines']:
                #self.pretty_print_uniq(item)


                right_stem_syn = [u'klitz', u'klein']


                right_repl = [
                             (49, 10000, u'[12, 3, 8]', u'[2, 10]', u'[2, 6]', u'klitzes', u'klitzes^4', u'klitz', u's', 4, 6, u'[2, 6]', u'FM', u'["neutral", 0.0]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                             (50, 10000, u'[12, 3, 8]', u'[2, 11]', u'[2, 6]', u'klitzes', u'kli^3tzes^3', u'klitz', u'i', 3, 2, u'[2, 6]', u'FM', u'["neutral", 0.0]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                             (51, 10000, u'[12, 3, 8]', u'[2, 11]', u'[2, 6]', u'klitzes', u'kli^3tzes^3', u'klitz', u's', 3, 6, u'[2, 6]', u'FM', u'["neutral", 0.0]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                             (52, 10000, u'[12, 3, 8]', u'[2, 12]', u'[2, 7]', u'kleines', u'klein^3e^2s', u'klein', u'n', 3, 4, u'[2, 7]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                             (53, 10000, u'[12, 3, 8]', u'[2, 13]', u'[2, 7]', u'kleines', u'kleines^4', u'klein', u's', 4, 6, u'[2, 7]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                         ]


                right_syntagma = [u'klitzes', u'kleines']


                right_baseline = ([[u'klitzes', u'kleines'], u'klitz++klein', 2, 1, u'[2, 2]', u'[3, 2]', u'[1, 1]', u'[2, 2]', u'1', u'1'],)


                right_redu = [
                             (15, 10000, u'[12, 3, 8]', u'[2, 10]', u'[2, 6]', u'klitzes', u'klitz', u'{"klitzes^4": 1, "kli^3tzes^3": 1}', 2, u'FM', u'["neutral", 0.0]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None, None, None, None, None),
                             (16, 10000, u'[12, 3, 8]', u'[2, 12]', u'[2, 7]', u'kleines', u'klein', u'{"klein^3e^2s": 1, "kleines^4": 1}', 2, u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                         ]



            elif item["syntagma"] == [u'klitz', u'klein']:
                #self.pretty_print_uniq(item)

                right_stem_syn = [u'klitz', u'klein']


                right_repl = [
                             (42, 10000, u'[12, 3, 8]', u'[2, 5]', u'[2, 3]', u'klitz', u'kli^4tz', u'klitz', u'i', 4, 2, u'[2, 3]', u'NE', u'["neutral", 0.0]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                             (43, 10000, u'[12, 3, 8]', u'[2, 6]', u'[2, 3]', u'klitz', u'kli^4tz^3', u'klitz', u'i', 4, 2, u'[2, 3]', u'NE', u'["neutral", 0.0]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                             (44, 10000, u'[12, 3, 8]', u'[2, 6]', u'[2, 3]', u'klitz', u'kli^4tz^3', u'klitz', u'z', 3, 4, u'[2, 3]', u'NE', u'["neutral", 0.0]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                             (45, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'e', 3, 2, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                             (46, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'i', 3, 3, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                             (47, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'n', 3, 4, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                             (48, 10000, u'[12, 3, 8]', u'[2, 8]', u'[2, 4]', u'klein', u'klein^5', u'klein', u'n', 5, 4, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                         ]


                right_syntagma = [u'klitz', u'klein']


                right_baseline = ([[u'klitz', u'klein'], u'klitz++klein', 2, 1, u'[2, 2]', u'[3, 4]', u'[1, 1]', u'[3, 2]', u'1', u'1'],)


                right_redu = [
                             (13, 10000, u'[12, 3, 8]', u'[2, 4]', u'[2, 3]', u'klitz', u'klitz', u'{"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}', 3, u'NE', u'["neutral", 0.0]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None),
                             (14, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'klein', u'{"kle^3i^3n^3": 1, "klein^5": 1}', 2, u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                         ]





            elif  item["syntagma"] == [u'klitze', u'kleine']:
                #self.pretty_print_uniq(item)
                
                right_stem_syn = [u'klitz', u'klein']


                right_repl = [
                             (1, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'i', 4, 2, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                             (2, 8888, u'[4, 11]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze^7', u'klitz', u'e', 7, 5, u'[0, 0]', u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                             (20, 10000, u'[12, 3, 8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'klitz', u'e', 4, 5, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'kleine', u'["ADJA", null, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]'),
                             (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                         ]


                right_syntagma = [u'klitze', u'kleine']


                right_baseline = ([[u'klitze', u'kleine'], u'klitz++klein', 2, 4, u'[2, 3]', u'[3, 4]', u'[1, 1]', u'[2, 2]', u'2', u'1'],)


                right_redu = [
                             (1, 8888, u'[4, 11]', u'[0, 0]', u'[0, 0]', u'klitze', u'klitz', u'{"klitze": 1, "kli^4tze^7": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5in^5e": 1, "klein^3e": 1}, "klein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]'),
                             (2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                         ]



            else:
                assert False



            extracted_repl = item["repl"]
            extracted_redu = item["redu"]
            extracted_baseline = item["baseline"]
            extracted_syntagma = item["syntagma"]

            assert item["stem_syn"] == ["klitz", "klein"]
            set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
            set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
            set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
            extracted_syntagma.should.be.equal(right_syntagma)

            #p(type(item), "item")
            #p(item["baseline"])
            #sys.exit()
            #item["baseline"] = [unicode(item) for item in item["baseline"] ]
            #item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":[unicode(item) for item in right_baseline ], "syntagma":right_syntagma, "stem_syn":item["stem_syn"]})









    ###############################################################################################################################################
    ############################################### II. FullRepetativnes= False   #################################################################################
    #######################################################################################################################################
        #p(stats._language)
        stats.recompute_syntagma_repetativity_scope(False)


        # # ####################################################################################
        # # #################. WORK WITH EMOJIS   #########################################
        # # ####################################################################################

        ### Case 2.1:
        syntagma = ["EMOIMG"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos"))
        #p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=False)


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]


        right_repl = [
                     (8, 8888, u'[4, 11]', u'[1, 9]', u'[1, 9]', u'\U0001f600', u'\U0001f600^5', u'\U0001f600', u'\U0001f600', 5, 0, None, u'EMOIMG', u'["positive", 0.5]', u'gl\xfccklich', u'["ADJD", null, "glucklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', u'-)', u'["EMOASC", null, "-)"]', u'-)', u'["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None, None, None, None, None),
                     (79, 12222, u'[24]', u'[0, 15]', u'[0, 12]', u'\U0001f62b', u'\U0001f62b^4', u'\U0001f62b', u'\U0001f62b', 4, 0, None, u'EMOIMG', u'["neutral", 0.0]', u'mal', u'["PTKMA", null, "mal"]', u'gerne', u'["ADV", null, "gern"]', u'hate', u'["VAFIN", null, "hat"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 1, u'["number", null, "1"]', u'du', u'["PPER", null, "du"]', u'meintest', u'["VVFIN", null, "meint"]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]'),
                 ]


        right_syntagma = [u'EMOIMG']


        right_baseline = [[[u'\U0001f62b', u'1', u'du'], u'\U0001f62b++1++du', 3, 1, u'[1, 1, 0]', u'[1, 1, 0]', None, None, None, None], [[u'\U0001f600'], u'\U0001f600', 1, 1, u'1', u'1', None, None, u'1', None], [[u'\U0001f62b', u'1', u'du', u'meintest', u',', u'es'], u'\U0001f62b++1++du++meint++,++es', 6, 1, u'[1, 1, 0, 0, 0, 0]', u'[1, 1, 0, 0, 0, 0]', None, None, None, None], [[u'\U0001f62b', u'1', u'du', u'meintest'], u'\U0001f62b++1++du++meint', 4, 1, u'[1, 1, 0, 0]', u'[1, 1, 0, 0]', None, None, None, None], [[u'\U0001f62b'], u'\U0001f62b', 1, 1, u'1', u'1', None, None, u'1', None], [[u'\U0001f62b', u'1'], u'\U0001f62b++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None], [[u'\U0001f62b', u'1', u'du', u'meintest', u','], u'\U0001f62b++1++du++meint++,', 5, 1, u'[1, 1, 0, 0, 0]', u'[1, 1, 0, 0, 0]', None, None, None, None], [[u'\U0001f600', u'-)'], u'\U0001f600++-)', 2, 1, u'[1, 2]', u'[1, 2]', u'[0, 1]', u'[0, 2]', None, None]]


        right_redu = []




        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)



        # # # ####################################################################################
        # # # ####################################################################################
        # # # #################################################################################
  



        ### Case 2.3:
        syntagma = ["EMOASC","EMOIMG"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="pos"))
        #p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=False)


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]



        right_repl = [
                     (7, 8888, u'[4, 11]', u'[1, 8]', u'[1, 8]', u'-)', u'-)^3', u'-)', u')', 3, 1, None, u'EMOASC', u'["positive", 0.5]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "glucklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'-)', u'["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None, None, None),
                     (8, 8888, u'[4, 11]', u'[1, 9]', u'[1, 9]', u'\U0001f600', u'\U0001f600^5', u'\U0001f600', u'\U0001f600', 5, 0, None, u'EMOIMG', u'["positive", 0.5]', u'gl\xfccklich', u'["ADJD", null, "glucklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', u'-)', u'["EMOASC", null, "-)"]', u'-)', u'["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None, None, None, None, None),
                 ]


        right_syntagma = [u'EMOASC', u'EMOIMG']


        right_baseline = [[[u'-)', u'\U0001f600'], u'-)++\U0001f600', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None], [[u'\U0001f600'], u'\U0001f600', 1, 1, u'1', u'1', None, None, u'1', None], [[u'\U0001f600', u'-)'], u'\U0001f600++-)', 2, 1, u'[1, 2]', u'[1, 2]', u'[0, 1]', u'[0, 2]', None, None], [[u'-)', u'\U0001f600', u'-)'], u'-)++\U0001f600++-)', 3, 1, u'[3, 1, "IGNOR"]', u'[3, 1, "IGNOR"]', u'[1, 0, "IGNOR"]', u'[2, 0, "IGNOR"]', None, None], [[u'-)'], u'-)', 1, 3, u'3', u'3', u'1', u'2', u'3', u'1']]


        right_redu = []

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        extracted_syntagma.should.be.equal(right_syntagma)



        # # ####################################################################################
        # # #################. WORK WITH SENTIMENT   #########################################
        # # #################################################################################



        ### Case 3.1:
        #- sentiment="positive"
        syntagma = ["EMOASC"]
        data = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment="positive", syntagma_type="pos"))
        #p(data,"data")
        #self.pretty_print_uniq(data[0],syn_order=False)


        extracted_repl = data[0]["repl"]
        extracted_redu = data[0]["redu"]
        extracted_baseline = data[0]["baseline"]
        extracted_syntagma = data[0]["syntagma"]


        right_repl = [
                     (9, 8888, u'[4, 11]', u'[1, 10]', u'[1, 10]', u'-)', u'-)^3', u'-)', u')', 3, 1, u'[1, 10]', u'EMOASC', u'["positive", 0.5]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', u'-)', u'["EMOASC", null, "-)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None, None, None),
                     (10, 8888, u'[4, 11]', u'[1, 11]', u'[1, 10]', u'-)', u'-)^3', u'-)', u')', 3, 1, u'[1, 10]', u'EMOASC', u'["positive", 0.5]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', u'-)', u'["EMOASC", null, "-)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None, None, None),
                     (6, 8888, u'[4, 11]', u'[1, 7]', u'[1, 7]', u':-)', u':-)^4', u':-)', u')', 4, 2, None, u'EMOASC', u'["positive", 0.5]', u'sie', u'["PPER", null, "sie"]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "glucklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u'-)', u'["EMOASC", null, "-)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'-)', u'["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None),
                     (7, 8888, u'[4, 11]', u'[1, 8]', u'[1, 8]', u'-)', u'-)^3', u'-)', u')', 3, 1, None, u'EMOASC', u'["positive", 0.5]', u'mich', u'["PPER", null, "mich"]', u'gl\xfccklich', u'["ADJD", null, "glucklich"]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', u'-)', u'["EMOASC", {"-)^3": 2}, "-)"]', None, None, None, None, None, None),
                 ]


        right_syntagma = [u'EMOASC']


        right_baseline = [[[u'-)', u'\U0001f600'], u'-)++\U0001f600', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None], [[u':-)', u'-)', u'\U0001f600'], u':-)++-)++\U0001f600', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, None, None], [[u':-)', u'-)'], u':-)++-)', 2, 1, u'[1, 1]', u'[1, 1]', None, None, None, None], [[u'-)'], u'-)', 1, 3, u'3', u'3', u'1', u'2', u'3', u'1'], [[u':-)'], u':-)', 1, 1, u'1', u'1', None, None, u'1', None], [[u':-)', u'-)', u'\U0001f600', u'-)'], u':-)++-)++\U0001f600++-)', 4, 1, u'[1, 3, 1, "IGNOR"]', u'[1, 3, 1, "IGNOR"]', u'[0, 1, 0, "IGNOR"]', u'[0, 2, 0, "IGNOR"]', None, None], [[u'-)', u'\U0001f600', u'-)'], u'-)++\U0001f600++-)', 3, 1, u'[3, 1, "IGNOR"]', u'[3, 1, "IGNOR"]', u'[1, 0, "IGNOR"]', u'[2, 0, "IGNOR"]', None, None]]


        right_redu = [(3, 8888, u'[4, 11]', u'[1, 10]', u'[1, 10]', u'-)', u'-)', u'{"-)^3": 2}', 2, u'EMOASC', u'["positive", 0.5]', u'gemacht', u'["VVPP", null, "gemacht"]', u'!', u'["symbol", null, "!"]', u':-)', u'["EMOASC", null, ":-)"]', u'-)', u'["EMOASC", null, "-)"]', u'\U0001f600', u'["EMOIMG", null, "\\ud83d\\ude00"]', None, None, None, None, None, None, None, None, None, None)]
        

        set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
        set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
        set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
        #p((extracted_syntagma, right_syntagma))
        extracted_syntagma.should.be.equal(right_syntagma)



    ################################################################################################
    ################################################################################################
    ###################################################################################################
    ############################stemmed_search = True #########################################
    #################################################################################################
    ################################################################################################
    ################################################################################################



        ########stemmed_search=True #

        ### Case 10.1:
        syntagma = ["klein"]
        items = list(stats.get_data(syntagma, repl=True, redu=True, baseline=True, sentiment=False, syntagma_type="lexem",stemmed_search=True))
        for item in items:
            #p(item["syntagma"])

            if item["syntagma"] == [u'kleines']:
                #self.pretty_print_uniq(item)


                right_stem_syn = [u'klein']


                right_repl = [
                             (52, 10000, u'[12, 3, 8]', u'[2, 12]', u'[2, 7]', u'kleines', u'klein^3e^2s', u'klein', u'n', 3, 4, u'[2, 7]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                             (53, 10000, u'[12, 3, 8]', u'[2, 13]', u'[2, 7]', u'kleines', u'kleines^4', u'klein', u's', 4, 6, u'[2, 7]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                             (66, 11111, u'[5, 6, 15, 3]', u'[3, 0]', u'[3, 0]', u'kleines', u'kleine^4s^7', u'klein', u'e', 4, 5, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (67, 11111, u'[5, 6, 15, 3]', u'[3, 0]', u'[3, 0]', u'kleines', u'kleine^4s^7', u'klein', u's', 7, 6, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (68, 11111, u'[5, 6, 15, 3]', u'[3, 1]', u'[3, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u'n', 4, 4, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (69, 11111, u'[5, 6, 15, 3]', u'[3, 1]', u'[3, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u'e', 3, 5, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (70, 11111, u'[5, 6, 15, 3]', u'[3, 1]', u'[3, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u's', 4, 6, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (71, 11111, u'[5, 6, 15, 3]', u'[3, 2]', u'[3, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'e', 4, 2, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (72, 11111, u'[5, 6, 15, 3]', u'[3, 2]', u'[3, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'i', 5, 3, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (73, 11111, u'[5, 6, 15, 3]', u'[3, 2]', u'[3, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'n', 3, 4, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (74, 11111, u'[5, 6, 15, 3]', u'[3, 2]', u'[3, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u's', 3, 6, u'[3, 0]', u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (26, 10000, u'[12, 3, 8]', u'[1, 0]', u'[1, 0]', u'kleines', u'kleine^4s^7', u'klein', u'e', 4, 5, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                             (27, 10000, u'[12, 3, 8]', u'[1, 0]', u'[1, 0]', u'kleines', u'kleine^4s^7', u'klein', u's', 7, 6, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                             (28, 10000, u'[12, 3, 8]', u'[1, 1]', u'[1, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u'n', 4, 4, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                             (29, 10000, u'[12, 3, 8]', u'[1, 1]', u'[1, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u'e', 3, 5, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                             (30, 10000, u'[12, 3, 8]', u'[1, 1]', u'[1, 0]', u'kleines', u'klein^4e^3s^4', u'klein', u's', 4, 6, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                             (31, 10000, u'[12, 3, 8]', u'[1, 2]', u'[1, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'e', 4, 2, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                             (32, 10000, u'[12, 3, 8]', u'[1, 2]', u'[1, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'i', 5, 3, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                             (33, 10000, u'[12, 3, 8]', u'[1, 2]', u'[1, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u'n', 3, 4, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                             (34, 10000, u'[12, 3, 8]', u'[1, 2]', u'[1, 0]', u'kleines', u'kle^4i^5n^3e^2s^3', u'klein', u's', 3, 6, u'[1, 0]', u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                         ]


                right_syntagma = [u'kleines']


                right_baseline = ([[u'kleines'], u'klein', 1, 8, u'8', u'20', u'3', u'8', u'8', u'3'],)


                right_redu = [
                             (16, 10000, u'[12, 3, 8]', u'[2, 12]', u'[2, 7]', u'kleines', u'klein', u'{"klein^3e^2s": 1, "kleines^4": 1}', 2, u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', None, None, None, None, None, None, None, None, None, None),
                             (17, 11111, u'[5, 6, 15, 3]', u'[3, 0]', u'[3, 0]', u'kleines', u'klein', u'{"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}', 3, u'NN', u'["neutral", 0.0]', 3, u'["number", null, "3"]', 4, u'["number", null, "4"]', 5, u'["number", null, "5"]', 6, u'["number", null, "6"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (11, 10000, u'[12, 3, 8]', u'[1, 0]', u'[1, 0]', u'kleines', u'klein', u'{"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}', 3, u'NN', u'["neutral", 0.0]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]', u'beser', u'["ADJD", null, "bes"]', u'kan', u'["FM", {"ka^4n^5": 1, "kan^6": 1}, "kan"]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]'),
                         ]



            elif item["syntagma"] == [u'kleinere']:
                #self.pretty_print_uniq(item)

                right_stem_syn = [u'klein']


                right_repl = [
                             (37, 10000, u'[12, 3, 8]', u'[2, 0]', u'[2, 0]', u'kleinere', u'kleinere^5', u'klein', u'e', 5, 7, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                             (38, 10000, u'[12, 3, 8]', u'[2, 1]', u'[2, 0]', u'kleinere', u'kleine^3r^2e^5', u'klein', u'e', 3, 5, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                             (39, 10000, u'[12, 3, 8]', u'[2, 1]', u'[2, 0]', u'kleinere', u'kleine^3r^2e^5', u'klein', u'e', 5, 7, u'[2, 0]', u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]'),
                         ]


                right_syntagma = [u'kleinere']


                right_baseline = ([[u'kleinere'], u'klein', 1, 2, u'2', u'3', u'1', u'2', u'2', u'1'],)


                right_redu = [(12, 10000, u'[12, 3, 8]', u'[2, 0]', u'[2, 0]', u'kleinere', u'klein', u'{"kleinere^5": 1, "kleine^3r^2e^5": 1}', 2, u'NE', u'["neutral", 0.0]', u'es', u'["VVFIN", null, "es"]', u'.', u'["symbol", null, "."]', u'kleines', u'["NN", {"kle^4i^5n^3e^2s^3": 1, "klein^4e^3s^4": 1, "kleine^4s^7": 1}, "klein"]', u'm\xe4dchen', u'["NN", null, "madch"]', u'.', u'["symbol", null, "."]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'klein', u'["FM", {"kle^3i^3n^3": 1, "klein^5": 1}, "klein"]', u'.', u'["symbol", null, "."]')]




            elif  item["syntagma"] == [u'kleine']:
                #self.pretty_print_uniq(item)

                right_stem_syn = [u'klein']


                right_repl = [
                             (82, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 4, 2, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (83, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'i', 5, 3, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (84, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (85, 12222, u'[24]', u'[0, 24]', u'[0, 21]', u'kleine', u'kle^4i^5n^4e^8', u'klein', u'e', 8, 5, None, u'ADJA', u'["neutral", 0.0]', u',', u'["symbol", null, ","]', u'es', u'["PPER", null, "es"]', u'war', u'["VAFIN", null, "war"]', u'so', u'["ADV", null, "so"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', None, None, None, None, None, None),
                             (3, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'e', 5, 2, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (4, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5in^5e', u'klein', u'n', 5, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (5, 8888, u'[4, 11]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'klein', u'n', 3, 4, u'[0, 1]', u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]'),
                             (21, 10000, u'[12, 3, 8]', u'[0, 2]', u'[0, 2]', u'kleine', u'kle^5ine', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', None, None, None, None, None, None, u'eine', u'["ART", null, "ein"]', u'klitze', u'["ADJA", null, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'@sch\xf6nesleben', u'["mention", null, "@schonesleb"]', u'#machwasdaraus', u'["hashtag", null, "#machwasdaraus"]', u'#bewegedeinarsch', u'["hashtag", null, "#bewegedeinarsch"]', u'https://www.freiesinternet.de', u'["URL", null, "https://www.freiesinternet.d"]'),
                             (57, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 2, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                             (58, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'n', 4, 4, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                             (59, 11111, u'[5, 6, 15, 3]', u'[2, 4]', u'[2, 4]', u'kleine', u'kle^5i^2n^4e^5', u'klein', u'e', 5, 5, None, u'ADJA', u'["neutral", 0.0]', u'!', u'["symbol", null, "!"]', u'weil', u'["KOUS", null, "weil"]', u'es', u'["PPER", null, "es"]', u'ja', u'["PTKMA", null, "ja"]', u'eine', u'["ART", null, "ein"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'ist', u'["VAFIN", null, "ist"]', u'.', u'["symbol", null, "."]', 1, u'["number", null, "1"]', 2, u'["number", null, "2"]'),
                         ]


                right_syntagma = [u'kleine']


                right_baseline = ([[u'kleine'], u'klein', 1, 7, u'5', u'11', u'1', u'2', u'5', u'1'],)


                right_redu = [(2, 8888, u'[4, 11]', u'[0, 2]', u'[0, 1]', u'kleine', u'klein', u'{"kle^5in^5e": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze^7": 1}, "klitz"]', u'\xfcberaschung', u'["NN", null, "uberasch"]', u'.', u'["symbol", null, "."]', u'trotzdem', u'["PAV", null, "trotzd"]', u'hat', u'["VAFIN", null, "hat"]', u'sie', u'["PPER", null, "sie"]')]





            elif  item["syntagma"] == [u'klein']:
                #self.pretty_print_uniq(item)

                right_stem_syn = [u'klein']


                right_repl = [
                             (45, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'e', 3, 2, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                             (46, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'i', 3, 3, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                             (47, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'kle^3i^3n^3', u'klein', u'n', 3, 4, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                             (48, 10000, u'[12, 3, 8]', u'[2, 8]', u'[2, 4]', u'klein', u'klein^5', u'klein', u'n', 5, 4, u'[2, 4]', u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None),
                         ]


                right_syntagma = [u'klein']


                right_baseline = ([[u'klein'], u'klein', 1, 2, u'2', u'4', u'1', u'2', u'2', u'1'],)


                right_redu = [(14, 10000, u'[12, 3, 8]', u'[2, 7]', u'[2, 4]', u'klein', u'klein', u'{"kle^3i^3n^3": 1, "klein^5": 1}', 2, u'FM', u'["neutral", 0.0]', u'.', u'["symbol", null, "."]', u'kleinere', u'["NE", {"kleinere^5": 1, "kleine^3r^2e^5": 1}, "klein"]', u'auswahl', u'["NN", null, "auswahl"]', u'.', u'["symbol", null, "."]', u'klitz', u'["NE", {"kli^4tz": 1, "klitz": 1, "kli^4tz^3": 1}, "klitz"]', u'.', u'["symbol", null, "."]', u'klitzes', u'["FM", {"klitzes^4": 1, "kli^3tzes^3": 1}, "klitz"]', u'kleines', u'["FM", {"klein^3e^2s": 1, "kleines^4": 1}, "klein"]', None, None, None, None)]

            else:
                assert False



            extracted_repl = item["repl"]
            extracted_redu = item["redu"]
            extracted_baseline = item["baseline"]
            extracted_syntagma = item["syntagma"]

            item["stem_syn"] = ["klein"]
            set(self.convert_all_lists_to_tuples(extracted_repl)).should.be.equal(set(self.convert_all_lists_to_tuples(right_repl)))
            set(self.convert_all_lists_to_tuples(extracted_redu)).should.be.equal(set(self.convert_all_lists_to_tuples(right_redu)))
            set(list( tuple(unicode(elem) for elem in  item ) for item in extracted_baseline)).should.be.equal(set(list( tuple(  unicode(elem) for elem in  item ) for item in right_baseline)))
            extracted_syntagma.should.be.equal(right_syntagma)

            #item["baseline"] = [unicode(item) for item in item["baseline"] ]
            #item.should.be.equal({"repl":right_repl, "redu":right_redu,"baseline":[unicode(item) for item in right_baseline ], "syntagma":right_syntagma, "stem_syn":item["stem_syn"]})










    @attr(status='stable')
    #@wipd
    def test_test_get_header_for_exhausted_output_table_type_612_1(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode="silent",use_cash=True)#, )
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))


        ## Case 1:
        cols = stats._get_header_exhausted(repl=False, redu=False, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        #p(cols, "cols")
        assert not cols
        #for k,v in cols.iteritems():
        #    assert not v


        ###### repl = True

        ## Case 2.1:
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        #p(cols, "cols")
        assert not cols
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        # print cols["document"]
        # print cols["context"]

        # cols["repl"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'repl_letter', 'repl_length', 'index_of_repl', 'in_redu'))
        # assert not cols["redu"] 
        # cols["word"].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos', 'polarity'))
        # cols["document"].should.be.equal((('doc_id', 'redufree_len'),))
        # cols["context"].should.be.equal(('contextL5', 'context_infoL5', 'contextL4', 'context_infoL4', 'contextL3', 'context_infoL3', 'contextL2', 'context_infoL2', 'contextL1', 'context_infoL1', 'contextR1', 'context_infoR1', 'contextR2', 'context_infoR2', 'contextR3', 'context_infoR3', 'contextR4', 'context_infoR4', 'contextR5', 'context_infoR5'))
        # assert not cols["baseline"] 



        ## Case 2.2:
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        #p(cols, "cols")
        assert not cols
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        # print cols["document"]
        # print cols["context"]

        # cols["repl"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'repl_letter', 'repl_length', 'index_of_repl', 'in_redu'))
        # assert not cols["redu"] 
        # cols["word"].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos', 'polarity'))
        # cols["document"].should.be.equal((('doc_id', 'redufree_len'),))
        # cols["context"].should.be.equal(('contextL5', 'context_infoL5', 'contextL4', 'context_infoL4', 'contextL3', 'context_infoL3', 'contextL2', 'context_infoL2', 'contextL1', 'context_infoL1', 'contextR1', 'context_infoR1', 'contextR2', 'context_infoR2', 'contextR3', 'context_infoR3', 'contextR4', 'context_infoR4', 'contextR5', 'context_infoR5'))
        # assert not cols["baseline"] 


        ## Case 2.3:
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=True, additional_doc_cols=False, context_len_left=1, context_len_right=1)
        #p(cols, "cols")
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        # print cols["document"]
        #print cols["context"]
        #print cols["baseline"]

        cols["repl"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'repl_letter', 'repl_length', 'index_of_repl', 'in_redu'))
        assert not cols["redu"] 
        cols["word"].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos', 'polarity'))
        cols["document"].should.be.equal((('doc_id', 'redufree_len'), None))
        cols["context"].should.be.equal(('contextL1', 'context_infoL1', 'contextR1', 'context_infoR1'))
        cols["baseline"].should.be.equal(('syntagma', 'stemmed', 'scope', 'occur_syntagma_all', 'occur_repl_uniq', 'occur_repl_exhausted', 'occur_full_syn_repl'))


        ## Case 2.4:
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=False, additional_doc_cols=False, context_len_left=False, context_len_right=False)
        assert not cols
        #p(cols, "cols")
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        # print cols["document"]
        #print cols["context"]

        # cols["repl"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'repl_letter', 'repl_length', 'index_of_repl', 'in_redu'))
        # assert not cols["redu"] 
        # cols["word"].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos', 'polarity'))
        # cols["document"].should.be.equal((('doc_id', 'redufree_len'),))
        # assert not cols["context"]
        # assert not cols["baseline"] 



        ## Case 2.5:
        #additional_doc_cols = True
        cols = stats._get_header_exhausted(repl=True, redu=False, baseline=False, additional_doc_cols=["gender", "sex"], context_len_left=False, context_len_right=False)
        assert not cols
        #p(cols, "cols")
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        #print cols["document"]
        #print cols["context"]

        # cols["repl"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'repl_letter', 'repl_length', 'index_of_repl', 'in_redu'))
        # assert not cols["redu"] 
        # cols["word"].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos', 'polarity'))
        # cols["document"].should.be.equal((('doc_id', 'redufree_len'), ('gender', 'sex')))
        # assert not cols["context"]
        # assert not cols["baseline"] 




        ###### redu ; baseline

        ## Case 2.1:
        cols = stats._get_header_exhausted(repl=False, redu=True, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        assert not cols
        #p(cols, "cols")
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        # print cols["document"]
        # print cols["context"]
        # print cols["baseline"]


        # assert not cols["repl"] 
        # cols["redu"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'orig_words', 'redu_length'))
        # cols["word"].should.be.equal(('normalized_word', 'stemmed', 'pos', 'polarity'))
        # cols["document"].should.be.equal((('doc_id', 'redufree_len'),))
        # cols["context"].should.be.equal(('contextL5', 'context_infoL5', 'contextL4', 'context_infoL4', 'contextL3', 'context_infoL3', 'contextL2', 'context_infoL2', 'contextL1', 'context_infoL1', 'contextR1', 'context_infoR1', 'contextR2', 'context_infoR2', 'contextR3', 'context_infoR3', 'contextR4', 'context_infoR4', 'contextR5', 'context_infoR5'))
        # assert not cols["baseline"]


        ###### redu  baseline
        ## Case 2.2:
        cols = stats._get_header_exhausted(repl=False, redu=True, baseline=True, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        #p(cols, "cols")
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        # print cols["document"]
        # print cols["context"]
        #print cols["baseline"]

        assert not cols["repl"] 
        cols["redu"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'orig_words', 'redu_length'))
        cols["word"].should.be.equal(('normalized_word', 'stemmed', 'pos', 'polarity'))
        cols["document"].should.be.equal((('doc_id', 'redufree_len'), None))
        cols["context"].should.be.equal(('contextL5', 'context_infoL5', 'contextL4', 'context_infoL4', 'contextL3', 'context_infoL3', 'contextL2', 'context_infoL2', 'contextL1', 'context_infoL1', 'contextR1', 'context_infoR1', 'contextR2', 'context_infoR2', 'contextR3', 'context_infoR3', 'contextR4', 'context_infoR4', 'contextR5', 'context_infoR5'))
        cols["baseline"].should.be.equal(('syntagma', 'stemmed', 'scope', 'occur_syntagma_all', 'occur_redu_uniq', 'occur_redu_exhausted', 'occur_full_syn_redu'))





        ###### repl=True; redu = True; 

        ## Case 3.1:
        cols = stats._get_header_exhausted(repl=True, redu=True, baseline=False, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        assert not cols
        #p(cols, "cols")
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        # print cols["document"]
        # print cols["context"]
        # print cols["baseline"]

        # cols["repl"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'repl_letter', 'repl_length', 'index_of_repl', 'in_redu')) 
        # cols["redu"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'orig_words', 'redu_length'))
        # cols["word"].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos', 'polarity'))
        # cols["document"].should.be.equal((('doc_id', 'redufree_len'),))
        # cols["context"].should.be.equal(('contextL5', 'context_infoL5', 'contextL4', 'context_infoL4', 'contextL3', 'context_infoL3', 'contextL2', 'context_infoL2', 'contextL1', 'context_infoL1', 'contextR1', 'context_infoR1', 'contextR2', 'context_infoR2', 'contextR3', 'context_infoR3', 'contextR4', 'context_infoR4', 'contextR5', 'context_infoR5'))
        # assert not cols["baseline"]


        ###### repl=True; redu = True; baseline=True;

        ## Case 4.1:
        cols = stats._get_header_exhausted(repl=True, redu=True, baseline=True, additional_doc_cols=False, context_len_left=True, context_len_right=True)
        
        #p(cols, "cols")
        # print cols["repl"]
        # print cols["redu"]
        # print cols["word"]
        # print cols["document"]
        # print cols["context"]
        #print cols["baseline"]


        cols["repl"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'repl_letter', 'repl_length', 'index_of_repl', 'in_redu')) 
        cols["redu"].should.be.equal(('id', 'index_in_corpus', 'index_in_redufree', 'orig_words', 'redu_length'))
        cols["word"].should.be.equal(('normalized_word', 'rle_word', 'stemmed', 'pos', 'polarity'))
        cols["document"].should.be.equal((('doc_id', 'redufree_len'), None))
        cols["context"].should.be.equal(('contextL5', 'context_infoL5', 'contextL4', 'context_infoL4', 'contextL3', 'context_infoL3', 'contextL2', 'context_infoL2', 'contextL1', 'context_infoL1', 'contextR1', 'context_infoR1', 'contextR2', 'context_infoR2', 'contextR3', 'context_infoR3', 'contextR4', 'context_infoR4', 'contextR5', 'context_infoR5'))
        cols["baseline"].should.be.equal(('syntagma', 'stemmed', 'scope', 'occur_syntagma_all', 'occur_repl_uniq', 'occur_repl_exhausted', 'occur_redu_uniq', 'occur_redu_exhausted', 'occur_full_syn_repl', 'occur_full_syn_redu'))







    @attr(status='stable')
    # @wipd
    def test_test_get_header_for_sum_output_table_type_612_2(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))


        ## Case 1:
        cols = stats._get_header_sum(repl=False, redu=False, word_examples_sum_table=True)
        #p(cols, "cols")
        cols.should.be.equal(False)


        #### repl #####
        ## Case 2.1:
        cols = stats._get_header_sum(repl=True, redu=False, word_examples_sum_table=True)
        #p(cols, "cols")
        cols.should.be.equal(('letter', 'NrOfRepl', 'Occur', 'Examples'))

        ## Case 2.2:
        cols = stats._get_header_sum(repl=True, redu=False, word_examples_sum_table=False)
        #p(cols, "cols")
        cols.should.be.equal(('letter', 'NrOfRepl', 'Occur'))



        #### redu #####
        ## Case 2.1:
        cols = stats._get_header_sum(repl=False, redu=True, word_examples_sum_table=True)
        #p(cols, "cols")
        cols.should.be.equal(('word', 'ReduLength', 'Occur'))

        ## Case 2.2:
        cols = stats._get_header_sum(repl=False, redu=True, word_examples_sum_table=False)
        #p(cols, "cols")
        cols.should.be.equal(('word', 'ReduLength', 'Occur'))





    @attr(status='stable')
    #@wipd
    def test_export_613_1(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True, status_bar=True)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        

        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))
        
        #stats.export(self.tempdir_project_folder, redu=True, repl=True, export_file_type="csv", max_scope=3)

        #p( stats.statsdb.getall("replications"))
        ########################################
        ######## EXHAUSTED TYPE ###########
        ########################################
        rewrite= True
        #self.tempdir_project_folder = "./export"
        ######### I FOR ALL SYNTAGMA ##############
        ##### Export in dirr formats
        #stats.recompute_syntagma_repetativity_scope(False)
        stats.export(self.tempdir_project_folder, repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=False,max_scope=2)
        stats.export(self.tempdir_project_folder, repl=True, redu=True,export_file_type="xml",output_table_type="exhausted",rewrite=rewrite,)
        stats.export(self.tempdir_project_folder, repl=True, redu=True,export_file_type="json",output_table_type="exhausted",rewrite=rewrite,)
        
        

        # #### Export with additional columns from CorpusDB
        stats.export(self.tempdir_project_folder, repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
            additional_doc_cols=["gender", "working_area", "age"],  fname="WITH_ADDIT_COLS_FROM_CORP",
            path_to_corpdb=os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_de))


        #### Export with NULL Kontext
        stats.export(self.tempdir_project_folder, repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
                    context_len_left=False, context_len_right=False, fname="NULL_KONTEXT")
        stats.export(self.tempdir_project_folder, repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
                    context_len_left=1, context_len_right=2, fname="1_2_KONTEXT_")


        #### Export with NULL Kontext
        stats.export(self.tempdir_project_folder, repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
                    max_scope=1, fname="MAX_SCOPE_VON_ONE")
# 


#         # # ######### II FOR FEW SYNTAGMA #############

        ##### stemmed search 
        stats.export(self.tempdir_project_folder, syntagma=["klitze"], repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
                   stemmed_search=True, fname="STEMMED_FOR_KLITZE")

        stats.export(self.tempdir_project_folder, syntagma=["klitze", "kleine"], repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
            stemmed_search=True, fname="STEMMED_FOR_KLITZE_KLEINE")

        stats.export(self.tempdir_project_folder, syntagma=["klitze", "kleine"], repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
            stemmed_search=False, fname="UN_STEMMED_FOR_KLITZE_KLEINE")

        stats.export(self.tempdir_project_folder, syntagma=[["klitze", "kleine"],["klitzes", "kleines"],["klitz", "klein"]], repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
            stemmed_search=False, fname="UN_STEMMED_FOR_ALL_KLITZ_KLEIN")

        # ##### pos search 
        stats.export(self.tempdir_project_folder, syntagma=["EMOIMG", "EMOASC"], repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
            stemmed_search=False, fname="EMOIMG_EMOASC", syntagma_type="pos")


        stats.export(self.tempdir_project_folder, syntagma=["EMOIMG"], repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
            stemmed_search=False, fname="EMOIMG", syntagma_type="pos")


        stats.export(self.tempdir_project_folder, syntagma=["EMOASC"], repl=True, redu=True,export_file_type="csv",output_table_type="exhausted",rewrite=rewrite,
            stemmed_search=False, fname="EMOASC", syntagma_type="pos")

        # # ########################################
        # # ######## SUM TYPE ###########
        # # ########################################
        stats.export(self.tempdir_project_folder, repl=True, redu=False,export_file_type="csv", output_table_type="sum", fname="SUM_REPL",rewrite=rewrite,)
        stats.export(self.tempdir_project_folder, repl=False, redu=True,export_file_type="csv", output_table_type="sum", fname="SUM_REDU",rewrite=rewrite,)

        stats.export(self.tempdir_project_folder,syntagma=["EMOIMG"], repl=True, redu=False,export_file_type="csv", rewrite=rewrite,
            output_table_type="sum", fname="SUM_REPL_EMOIMG",syntagma_type="pos")
        stats.export(self.tempdir_project_folder,syntagma=["EMOASC"], repl=False, redu=True,export_file_type="csv", rewrite=rewrite,
            output_table_type="sum", fname="SUM_REDU_EMOASC",syntagma_type="pos")




        files = os.listdir(self.tempdir_project_folder)
        #p(files)
        len(files).should.be.equal(18)



    @attr(status='stable')
    #@wipd
    def test_test_export_generator_structure_613_2(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True, status_bar=True)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        

        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))
        stats.attach_corpdb(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_de))
        


        # ##################
        # #### Case 1.1 ######
        # ##################
        # repl = True
        # redu = True
        # baseline = True
        # output_table_type = "exhausted"
        # max_scope = False
        # additional_doc_cols = ()
        # context_len_left = True
        # context_len_right = True
        # word_examples_sum_table = True

        # header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        # col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        # #p(col_num, "col_num")
        # assert col_num == 49
        # #p(header, "header")
        # #syntagma = ["kleine"]
        # #syntagma = "*"
        # syntagma = "*"
        # stemmed_search = False

        # data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search, max_scope=3)

        # for i,row in enumerate(data):
        #     if not row: continue
        #     len(row).should.be.equal(col_num)
        #     #p(row, "row")

        # p(i, "i")




        ############################################################
        ####### output_table_type = "exhausted" ########
        ##################################################################

        ##################
        #### Case 1.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 49
        #p(header, "header")
        #syntagma = ["kleine"]
        #syntagma = "*"
        syntagma = ["klitze","kleine"]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")




        ##################
        #### Case 1.2 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 49
        #p(header, "header")
        #syntagma = ["kleine"]
        #syntagma = "*"
        syntagma = ["klitze","kleine"]
        stemmed_search = True

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")




        ##################
        #### Case 1.3 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 49
        #p(header, "header")
        #syntagma = ["kleine"]
        syntagma = "*"
        #syntagma = ["klitze","kleine"]
        stemmed_search = True

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")


        ##################
        #### Case 1.3 ######
        ##################
        repl = False
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 38
        #p(header, "header")
        #syntagma = ["kleine"]
        syntagma = "*"
        #syntagma = ["klitze","kleine"]
        stemmed_search = True

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")


        ##################
        #### Case 1.4 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 49
        #p(header, "header")
        #syntagma = ["kleine"]
        syntagma = "*"
        #syntagma = ["klitze","kleine"]
        stemmed_search = True

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search,sentiment="positive")

        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")



        ##################
        #### Case 1.4 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True
        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 49
        #p(header, "header")
        #syntagma = ["kleine"]
        #syntagma = "*"

        rows_equal = []
        rows_not_equal = []

        counter2 = 0
        syntagma = [["klitzes","kleines"], ["klitz","klein"], ["klitze","kleine"]]
        stemmed_search = False
        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        for row in data:
            if row:
                rows_equal.append(row)
                counter2 += 1
                len(row).should.be.equal(col_num)
            #p(row, "row")

    

        counter1 = 0
        syntagma = ["klitze","kleine"]
        stemmed_search = True
        
        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)
        #list(data)
        # if not data:
        #    assert False
        rows = []
        for row in data:
            if row:
                #rows.add(row)#
                if not row: continue
                counter1 += 1
                len(row).should.be.equal(col_num)
                if row not in rows_equal:
                    rows_not_equal.append(row)
            #p(row, "row")

        counter1.should.be.equal(counter2)
        assert not rows_not_equal
        #p((counter1, counter2))





        # #################
        # ### Case 1.4 ######
        # ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 49
        #p(header, "header")
        #syntagma = ["kleine"]
        #syntagma = "*"
        syntagma = [["klitze","kleine"]]
        #syntagma = ["klitze","kleine"]
        stemmed_search = True

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search,sentiment="neutral")
        #p(data, "data")
        if not data:
           assert False

        i = 0 
        for row in data:
            #p(row, "row")
            if not row: continue
            i+= 1
            len(row).should.be.equal(col_num)
            #p(row, "row")
        #assert i == 0


        #p(list(stats.get_data([["klitze","kleine"]], repl=True, redu=True, baseline=True,send_empty_marker=True ) ))

        ##################
        #### Case 2 ######
        ##################
        repl = True
        redu = False
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True



        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 41
        #p(header, "header")
        #syntagma = ["kleine"]
        #syntagma = "*"
        syntagma = ["klitze","kleine"]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")



        ##################
        #### Case 3 ######
        ##################
        repl = False
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 38
        #p(header, "header")
        #syntagma = ["kleine"]
        #syntagma = "*"
        syntagma = ["klitze","kleine"]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")



        ##################
        #### Case 4 ######
        ##################
        repl = False
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        #additional_doc_cols = ()
        additional_doc_cols = ("gender", "age", "working_area")
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        #p(col_num, "col_num")
        assert col_num == 41
        stats.cols_exists_in_corpb(additional_doc_cols)
        #p(header, "header")
        #syntagma = ["kleine"]
        #syntagma = "*"
        syntagma = ["klitze","kleine"]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")




        ##########################################################
        ##########################################################
        ##########################################################
        ############################################################
        ####### output_table_type = "sum" ########
        ##################################################################
        ##########################################################


        ##################
        #### Case 1.1 ######
        ##################
        repl = False
        redu = True
        baseline = True
        output_table_type = "sum"
        max_scope = False
        word_examples_sum_table = True
        additional_doc_cols = False
        context_len_right =True
        context_len_left = True
        reptype_sum_table = "redu"
        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = len(header)
        #p(header, "header")
        #assert col_num == 41
        #stats.cols_exists_in_corpb(additional_doc_cols)
        #p(header, "header")
        #syntagma = ["kleine"]
        syntagma = "*"
        #syntagma = ["klitze","kleine"]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search,output_table_type=output_table_type, reptype_sum_table=reptype_sum_table)


        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")




        ##################
        #### Case 1.2 ######
        ##################
        repl = False
        redu = True
        baseline = True
        output_table_type = "sum"
        max_scope = False
        word_examples_sum_table = True
        additional_doc_cols = False
        context_len_right =True
        context_len_left = True
        reptype_sum_table = "redu"
        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = len(header)
        sentiment = "positive"
        #p(header, "header")
        #assert col_num == 41
        #stats.cols_exists_in_corpb(additional_doc_cols)
        #p(header, "header")
        #syntagma = ["kleine"]
        syntagma = "*"
        #syntagma = ["klitze","kleine"]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search,output_table_type=output_table_type, reptype_sum_table=reptype_sum_table,sentiment=sentiment)


        for row in data:
            if not row: continue
            len(row).should.be.equal(col_num)
            #p(row, "row")



        ##################
        #### Case 2.1 ######
        ##################
        repl = True
        redu = False
        baseline = True
        output_table_type = "sum"
        max_scope = False
        word_examples_sum_table = True
        additional_doc_cols = False
        context_len_right =True
        context_len_left = True
        reptype_sum_table = "repl"
        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = len(header)

        syntagma = "*"
        #syntagma = ["klitze","kleine"]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search,output_table_type=output_table_type, reptype_sum_table=reptype_sum_table)


        for row in data:
            #print "ghjk"
            #p(row, "row")
            if not row: continue
            len(row).should.be.equal(col_num)
            



        ##################
        #### Case 2.2 ######
        ##################
        repl = True
        redu = False
        baseline = True
        output_table_type = "sum"
        max_scope = False
        word_examples_sum_table = True
        additional_doc_cols = False
        context_len_right =True
        context_len_left = True
        reptype_sum_table = "repl"
        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        col_num = len(header)
        sentiment = "positive"
        syntagma = "*"
        #syntagma = ["klitze","kleine"]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search,output_table_type=output_table_type, reptype_sum_table=reptype_sum_table,sentiment=sentiment)

        for row in data:
            #print "ghjk"
            #p(row, "row")
            if not row: continue
            len(row).should.be.equal(col_num)
            





    def _summerize_reps3(self,header,data,redu=False, repl=True):
        import copy
        ### Step 1: Summerizing 
        dict_repls = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        dict_redus = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        dict_baseline = defaultdict(dict)

        
        if repl:
            ix_repl_index = header.index("[repl].index_in_corpus")
            ix_repl_id = header.index("[repl].id")
            ix_occur_repl_uniq = header.index('[baseline].occur_repl_uniq')
            ix_occur_repl_exhausted = header.index('[baseline].occur_repl_exhausted')
            ix_occur_full_syn_repl = header.index('[baseline].occur_full_syn_repl')
        if redu:
            dict_redus = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
            ix_redu_index = header.index("[redu].index_in_corpus")
            ix_redu_lenght = header.index("[redu].redu_length")
            ix_occur_redu_uniq = header.index('[baseline].occur_redu_uniq')
            ix_occur_redu_exhausted = header.index('[baseline].occur_redu_exhausted')
            ix_occur_full_syn_redu = header.index('[baseline].occur_full_syn_redu')
            ix_redu_id = header.index("[redu].id")

        ix_doc_id = header.index('[document].doc_id')
        ix_syn = header.index("[baseline].syntagma")
        ix_occur = header.index('[baseline].occur_syntagma_all')
        ix_scope = header.index("[baseline].scope")
        ix_word = header.index("[word].normalized_word")

        ### REPLS
        if repl:
            for row in data:
                #word = row{}
                repl_id = row[ix_repl_id]
                if repl_id:
                    doc_id = row[ix_doc_id]
                    index_in_corpus = row[ix_repl_index]
                    word = row[ix_word]
                    dict_repls[word][doc_id][index_in_corpus] += 1
                    #p((doc_id, index_in_corpus,word,repl_id),c="m")

        ### REDUS
        if redu:
            for row in data:
                redu_id = row[ix_redu_id]
                if redu_id:
                    #p(row, "redu")
                    doc_id = row[ix_doc_id]
                    index_in_corpus = row[ix_redu_index]
                    word = row[ix_word]
                    redu_lenght = row[ix_redu_lenght]
                    #p((redu_id,doc_id,index_in_corpus,word,redu_lenght),c="c")
                    dict_redus[word][doc_id][index_in_corpus] = redu_lenght

        ### baseline
        for row in data:
            #word = row{}
            syntagma = row[ix_syn]
            scope = row[ix_scope]
            occur_all = row[ix_occur]


            dict_baseline[syntagma]["occur_all"] = occur_all
            dict_baseline[syntagma]["scope"] = scope
            if repl:
                occur_repl_uniq= row[ix_occur_repl_uniq]
                occur_repl_exhausted = row[ix_occur_repl_exhausted]
                occur_full_syn_repl = row[ix_occur_full_syn_repl]
                dict_baseline[syntagma]["occur_repl_uniq"] = occur_repl_uniq
                dict_baseline[syntagma]["occur_repl_exhausted"] = occur_repl_exhausted
                dict_baseline[syntagma]["occur_full_syn_repl"] = occur_full_syn_repl

            if redu:
                occur_redu_uniq= row[ix_occur_redu_uniq]
                occur_redu_exhausted = row[ix_occur_redu_exhausted]
                occur_full_syn_redu = row[ix_occur_full_syn_redu]
                dict_baseline[syntagma]["occur_redu_uniq"] = occur_redu_uniq
                dict_baseline[syntagma]["occur_redu_exhausted"] = occur_redu_exhausted
                dict_baseline[syntagma]["occur_full_syn_redu"] = occur_full_syn_redu


        ##### Step 2: Counts
        computed_counts = defaultdict(lambda:defaultdict(lambda:[0,0]))
        if repl:
            for word, word_data in  dict_repls.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]["repl"][0] += 1
                        computed_counts[word]["repl"][1] += counter


        if redu:
            for word, word_data in  dict_redus.items():
                for doc_id, doc_data in word_data.items():
                    for index_in_corpus, counter in doc_data.items():
                        computed_counts[word]["redu"][0] += 1
                        computed_counts[word]["redu"][1] += counter


        temp_dict = {}
        for syntagma, counter_data  in dict_baseline.items():
            for counter_name, num in counter_data.items():
                temp_dict[counter_name] = num
        
        computed_counts[syntagma]["baseline"] = temp_dict
        

        return  computed_counts



    @attr(status='stable')
    #@wipd
    def test_test_export_generator_content_correctnes_613_3(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True, status_bar=True)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"

        
        gold_standard_data = self.configer._counted_reps["en"]

        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_en))
        stats.attach_corpdb(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        
        # # ############################################################
        # # ####### output_table_type = "exhausted" ########
        # # ##################################################################

        ##################
        #### Case 1.1 ######
        ##################
        repl = True
        redu = False
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = ["bad"]
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]

        #p(answer, "answer")
        
            #len(data).should.be.equal()

        tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
        baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
        tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
        len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
        #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']



        ##################
        #### Case 2.1 ######
        ##################
        repl = True
        redu = False
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'big']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")
        len(data).should.be.equal(right_data["repl"][1])

        tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
        baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
        tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
        len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
        #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']




        ##################
        #### Case 2.2 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'big']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
        baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
        tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
        len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
        #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
        baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
        tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
        len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])





        ##################
        #### Case 3.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'\U0001f308']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        if "repl" in right_data:
            tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
            baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
            tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
            #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        if "redu" in right_data:
            tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
            baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
            tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])





        ##################
        #### Case 3.2 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'\U0001f600']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        if "repl" in right_data:
            tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
            baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
            tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
            #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        if "redu" in right_data:
            tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
            baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
            tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])


        ##################
        #### Case 4.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u':-(']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        if "repl" in right_data:
            tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
            baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
            tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
            #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        if "redu" in right_data:
            tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
            baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
            tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])


        ##################
        #### Case 4.2 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'1']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        if "repl" in right_data:
            tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
            baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
            tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
            #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        if "redu" in right_data:
            tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
            baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
            tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])


        ##################
        #### Case 5.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'tiny']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        if "repl" in right_data:
            tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
            baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
            tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
            #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        if "redu" in right_data:
            tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
            baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
            tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])



        ##################
        #### Case 5.1 ######
        ##################
        repl = False
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'tiny']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        if "repl" in right_data and repl:
            tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
            baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
            tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
            #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        if "redu" in right_data and redu:
            tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
            baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
            tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])



        ##################
        #### Case 5.1 ######
        ##################
        repl = False
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'bad']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        if "repl" in right_data and repl:
            tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
            baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
            tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
            #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        if "redu" in right_data and redu:
            tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
            baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
            tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])



        ##################
        #### Case 6.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'but']
        right_data = gold_standard_data[syntagma[0]]
        repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        if repl:
            assert len(data) >= right_data["repl"][1]
        #p(answer, "answer")

        ### REPL
        if "repl" in right_data and repl:
            tuple(right_data["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
            baseline_entry_repl = (int(answer[syntagma[0]]["baseline"]['occur_repl_uniq']), int(answer[syntagma[0]]["baseline"]['occur_repl_exhausted']))
            tuple(right_data["repl"]).should.be.equal(tuple(baseline_entry_repl))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])
            #answer[syntagma[0]]["baseline"]['occur_full_syn_repl']

        ### REDU
        if "redu" in right_data and redu:
            tuple(right_data["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
            baseline_entry_redu = (int(answer[syntagma[0]]["baseline"]['occur_redu_uniq']), int(answer[syntagma[0]]["baseline"]['occur_redu_exhausted']))
            tuple(right_data["redu"]).should.be.equal(tuple(baseline_entry_redu))
            len(syntagma).should.be.equal(answer[syntagma[0]]["baseline"]['scope'])

        #p(list(stats.get_data(syntagma, repl=True, redu=True,baseline=True))[0]["redu"])




        ##################
        #### Case 6.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'EMOIMG']
        
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search, syntagma_type="pos")

        data = list(data)
        #p(data)
        
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        repl_num = sum([_data["repl"][1] for word, _data in answer.items() if word != 'baseline'])
        #p((len(data),repl_num))
        if repl:
           assert len(data) >= repl_num
        answer = {word: {phanomen:counts for  phanomen,counts in _data.items()} for word, _data in answer.items()}
        #p(answer, "answer")

        for  word, _data in answer.items():
            if word != "baseline":
               if tuple(_data["repl"]) != gold_standard_data[word]["repl"]:
                assert False





        ##################
        #### Case 6.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'number']
        
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search, syntagma_type="pos")

        data = list(data)
        #p(data)
        
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        repl_num = sum([_data["repl"][1] for word, _data in answer.items() if word != 'baseline'])
        #p((len(data),repl_num))
        if repl:
           assert len(data) >= repl_num
        answer = {word: {phanomen:counts for  phanomen,counts in _data.items()} for word, _data in answer.items()}
        #p(answer, "answer")

        for  word, _data in answer.items():
            if word != "baseline":
               if tuple(_data["repl"]) != gold_standard_data[word]["repl"]:
                assert False




        ##################
        #### Case 6.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'EMOASC']
        
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search, syntagma_type="pos")

        data = list(data)
        #p(data)
        
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        repl_num = sum([_data["repl"][1] for word, _data in answer.items() if word != 'baseline'])
        #p((len(data),repl_num))
        if repl:
           assert len(data) >= repl_num
        answer = {word: {phanomen:counts for  phanomen,counts in _data.items()} for word, _data in answer.items()}
        #p(answer, "answer")

        for  word, _data in answer.items():
            if word != "baseline":
               if tuple(_data["repl"]) != gold_standard_data[word]["repl"]:
                assert False








        ##################
        #### Case 6.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])

        syntagma = [u'very', "pity"]
        right_data = {
                        u'very': 
                                {
                                    'repl': [2, 4], 
                                    'redu': [1, 3]}, 

                        u'pity': 
                                {
                                    'repl': [2, 4], 
                                    'redu': [1, 4]}, 
                        u'very || pity': 
                                    {'baseline': {
                                                'occur_repl_uniq': u'[2, 2]', 
                                                'occur_all': 1, 
                                                'occur_repl_exhausted': u'[4, 4]', 
                                                'occur_full_syn_redu': u'1', 
                                                'occur_redu_exhausted': u'[3, 4]', 
                                                'scope': 2, 
                                                'occur_full_syn_repl': u'1', 
                                                'occur_redu_uniq': u'[1, 1]'}}}
        

        #repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        #if repl:
        #    assert len(data) >= right_data["repl"][1]
        answer = {word:{phanomen:counts for phanomen, counts in data.items()} for word, data in answer.items() }
        #p(answer, "answer")

        ### REPL
        joined_syn = u" || ".join(syntagma)
        #p(joined_syn )
        if repl:
            if "repl" in right_data[syntagma[0]]:
                tuple(right_data[syntagma[0]]["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
                baseline_entry_repl_word_1 = (
                                                json.loads(
                                                            answer[joined_syn]["baseline"]['occur_repl_uniq']
                                                            )[0], 
                                                json.loads( 
                                                            answer[joined_syn]["baseline"]['occur_repl_exhausted']
                                                            )[0]
                                            )
                tuple(right_data[syntagma[0]]["repl"]).should.be.equal(tuple(baseline_entry_repl_word_1))
            if "repl" in right_data[syntagma[1]]:
                baseline_entry_repl_word_2 = (
                                                json.loads(
                                                            answer[joined_syn]["baseline"]['occur_repl_uniq']
                                                            )[1], 
                                                json.loads( 
                                                            answer[joined_syn]["baseline"]['occur_repl_exhausted']
                                                            )[1]
                                            )
                tuple(right_data[syntagma[1]]["repl"]).should.be.equal(tuple(baseline_entry_repl_word_2))
                len(syntagma).should.be.equal(answer[joined_syn]["baseline"]['scope'])
            int(answer[joined_syn]["baseline"]['occur_full_syn_repl']).should.be.equal(int(right_data[joined_syn]["baseline"]['occur_full_syn_repl']))

        # ### REDU
        if  redu:
            if "redu" in right_data[syntagma[0]]:
                tuple(right_data[syntagma[0]]["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
                baseline_entry_redu_word_1 = (
                                                json.loads(
                                                            answer[joined_syn]["baseline"]['occur_redu_uniq']
                                                            )[0], 
                                                json.loads( 
                                                            answer[joined_syn]["baseline"]['occur_redu_exhausted']
                                                            )[0]
                                            )
                tuple(right_data[syntagma[0]]["redu"]).should.be.equal(tuple(baseline_entry_redu_word_1))
            if "redu" in right_data[syntagma[1]]:
                baseline_entry_redu_word_2 = (
                                                json.loads(
                                                            answer[joined_syn]["baseline"]['occur_redu_uniq']
                                                            )[1], 
                                                json.loads( 
                                                            answer[joined_syn]["baseline"]['occur_redu_exhausted']
                                                            )[1]
                                            )
                tuple(right_data[syntagma[1]]["redu"]).should.be.equal(tuple(baseline_entry_redu_word_2))
                len(syntagma).should.be.equal(answer[joined_syn]["baseline"]['scope'])
            int(answer[joined_syn]["baseline"]['occur_full_syn_redu']).should.be.equal(int(right_data[joined_syn]["baseline"]['occur_full_syn_redu']))

        # #p(list(stats.get_data(syntagma, redu=True, redu=True,baseline=True))[0]["redu"])




        #stats.recompute_syntagma_repetativity_scope(False)


        ##################
        #### Case 6.1 ######
        ##################
        repl = True
        redu = True
        baseline = True
        output_table_type = "exhausted"
        max_scope = False
        additional_doc_cols = ()
        context_len_left = True
        context_len_right = True
        word_examples_sum_table = True

        header = stats._get_header( repl=repl, redu=redu, baseline=baseline, output_table_type=output_table_type,  max_scope=max_scope, additional_doc_cols=additional_doc_cols, context_len_left=context_len_left, context_len_right=context_len_right,word_examples_sum_table=word_examples_sum_table)
        ordered_header = stats.order_header(header, False,"csv")
        col_num = sum([sum([len(doc_cols) for doc_cols in cols if doc_cols]) if tables_part_name == "document" else  len(cols) for tables_part_name, cols in header.iteritems() if cols ])
        syntagma = [u'but', "you"]
        #p(stats._get_data_for_one_syntagma(syntagma, redu=True, repl=True, baseline=True,get_also_non_full_repetativ_result=True)["redu"])
        
        right_data = {
                        u'but || you': 
                                    {'baseline': {
                                            'occur_repl_uniq': u'[10, 6]', 
                                            'occur_all': 4, 
                                            'occur_repl_exhausted': u'[15, 8]', 
                                            'occur_full_syn_redu': u'2', 
                                            'occur_redu_exhausted': u'[4, 4]', 
                                            'scope': 2, 'occur_full_syn_repl': u'4', 
                                            'occur_redu_uniq': u'[2, 2]'}}, 
                        u'you': {
                                    'repl': [6, 8], 
                                    'redu': [2, 4]}, 

                        u'but': {
                                    'repl': [10, 15], 
                                    'redu': [4, 10]}}

        #repl_num = right_data["repl"][1]
        stemmed_search = False

        data = stats._export_generator(header,inp_syntagma=syntagma,  stemmed_search=stemmed_search)

        data = list(data)
        #p(data)
        #p((len(data),repl_num))
        answer = self._summerize_reps3(ordered_header, data, redu=redu, repl=repl)
        #if repl:
        #    assert len(data) >= right_data["repl"][1]
        answer = {word:{phanomen:counts for phanomen, counts in data.items()} for word, data in answer.items() }
        #p(answer, "answer")

        ### REPL
        joined_syn = u" || ".join(syntagma)
        #p(joined_syn )
        if repl:
            if "repl" in right_data[syntagma[0]]:
                tuple(right_data[syntagma[0]]["repl"]).should.be.equal(tuple(answer[syntagma[0]]["repl"]))
                baseline_entry_repl_word_1 = (
                                                json.loads(
                                                            answer[joined_syn]["baseline"]['occur_repl_uniq']
                                                            )[0], 
                                                json.loads( 
                                                            answer[joined_syn]["baseline"]['occur_repl_exhausted']
                                                            )[0]
                                            )
                tuple(right_data[syntagma[0]]["repl"]).should.be.equal(tuple(baseline_entry_repl_word_1))
            if "repl" in right_data[syntagma[1]]:
                baseline_entry_repl_word_2 = (
                                                json.loads(
                                                            answer[joined_syn]["baseline"]['occur_repl_uniq']
                                                            )[1], 
                                                json.loads( 
                                                            answer[joined_syn]["baseline"]['occur_repl_exhausted']
                                                            )[1]
                                            )
                tuple(right_data[syntagma[1]]["repl"]).should.be.equal(tuple(baseline_entry_repl_word_2))
                len(syntagma).should.be.equal(answer[joined_syn]["baseline"]['scope'])
            int(answer[joined_syn]["baseline"]['occur_full_syn_repl']).should.be.equal(int(right_data[joined_syn]["baseline"]['occur_full_syn_repl']))

        # ### REDU
        if  redu:
            if "redu" in right_data[syntagma[0]]:
                tuple(right_data[syntagma[0]]["redu"]).should.be.equal(tuple(answer[syntagma[0]]["redu"]))
                baseline_entry_redu_word_1 = (
                                                json.loads(
                                                            answer[joined_syn]["baseline"]['occur_redu_uniq']
                                                            )[0], 
                                                json.loads( 
                                                            answer[joined_syn]["baseline"]['occur_redu_exhausted']
                                                            )[0]
                                            )
                #tuple(right_data[syntagma[0]]["redu"]).should.be.equal(tuple(baseline_entry_redu_word_1))
            if "redu" in right_data[syntagma[1]]:
                baseline_entry_redu_word_2 = (
                                                json.loads(
                                                            answer[joined_syn]["baseline"]['occur_redu_uniq']
                                                            )[1], 
                                                json.loads( 
                                                            answer[joined_syn]["baseline"]['occur_redu_exhausted']
                                                            )[1]
                                            )
                tuple(right_data[syntagma[1]]["redu"]).should.be.equal(tuple(baseline_entry_redu_word_2))
                len(syntagma).should.be.equal(answer[joined_syn]["baseline"]['scope'])
            int(answer[joined_syn]["baseline"]['occur_full_syn_redu']).should.be.equal(int(right_data[joined_syn]["baseline"]['occur_full_syn_redu']))

        # #p(list(stats.get_data(syntagma, redu=True, redu=True,baseline=True))[0]["redu"])












    @attr(status='stable')
    #@wipd
    def test_get_where_statement_type_614(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"


        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))

        ################################################################################
        ##############################LEXEM############################################
        ################################################################################

        #########################
        ####1. with_context#####
        ########################
        ### Case 1.0.1
     
        inp_syntagma_splitted = [u"😀"]
        inp_syntagma_unsplitted = u'😀'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
     
        #p(where, "where")#
        assert where == [[u"normalized_word='\U0001f600' "]]
     

        ### Case 1.0.2
        inp_syntagma_splitted = ["😀"]
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='\U0001f600' "]]
        #p(where, "where")#

        ### Case 1.0.3
        inp_syntagma_splitted = [u"😀"]
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='\U0001f600' "]]
        #p(where, "where")#

        ### Case 1.0.4
        inp_syntagma_splitted = ["😀"]
        inp_syntagma_unsplitted = u'😀'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='\U0001f600' "]]
        #p(where, "where")#


     
        ### Case 1.0.5
        inp_syntagma_splitted = ["😀"]
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='\U0001f600' "]]
        #p(where, "where")#


        ### Case 1.0.6
        inp_syntagma_splitted = [u"😀"]
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='\U0001f600' "]]
        #p(where, "where")#


        ### Case 1.1
        inp_syntagma_splitted = [u'.']
        inp_syntagma_unsplitted = u'.'
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='.' "]]
        #p(where, "where")



        ### Case 1.2
        inp_syntagma_splitted = ['klitze', 'kleine']
        inp_syntagma_unsplitted = 'klitze++kleine'
        scope = 2
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='klitze' ", u"contextR1='kleine'"], [u"contextL1='klitze'", u"normalized_word='kleine' "]]
        #p(where, "where")


        ### Case 1.3
        inp_syntagma_splitted = ['klitze', 'kleine', "überaschung"]
        inp_syntagma_unsplitted = 'klitze++kleine++überaschung'
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='klitze' ", u"contextR1='kleine'", u"contextR2='\xfcberaschung'"], [u"contextL1='klitze'", u"normalized_word='kleine' ", u"contextR1='\xfcberaschung'"], [u"contextL2='klitze'", u"contextL1='kleine'", u"normalized_word='\xfcberaschung' "]]
        #p(where, "where")



        ### Case 1.3.1
        inp_syntagma_splitted = ['1', 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='1' ", u"contextR1='2'", u"contextR2='3'"], [u"contextL1='1'", u"normalized_word='2' ", u"contextR1='3'"], [u"contextL2='1'", u"contextL1='2'", u"normalized_word='3' "]]
        #p(where, "where")

        ### Case 1.3.2
        inp_syntagma_splitted = [u'1', 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='1' ", u"contextR1='2'", u"contextR2='3'"], [u"contextL1='1'", u"normalized_word='2' ", u"contextR1='3'"], [u"contextL2='1'", u"contextL1='2'", u"normalized_word='3' "]]
        #p(where, "where")

     

        ### Case 1.3.3
        inp_syntagma_splitted = [u'1', 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='1' ", u"contextR1='2'", u"contextR2='3'"], [u"contextL1='1'", u"normalized_word='2' ", u"contextR1='3'"], [u"contextL2='1'", u"contextL1='2'", u"normalized_word='3' "]]
        #p(where, "where")

     


        ### Case 1.3.4
        inp_syntagma_splitted = ['1', 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='1' ", u"contextR1='2'", u"contextR2='3'"], [u"contextL1='1'", u"normalized_word='2' ", u"contextR1='3'"], [u"contextL2='1'", u"contextL1='2'", u"normalized_word='3' "]]
        #p(where, "where")
     

        ### Case 1.3.5
        inp_syntagma_splitted = [1, 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='1' ", u"contextR1='2'", u"contextR2='3'"], [u"contextL1='1'", u"normalized_word='2' ", u"contextR1='3'"], [u"contextL2='1'", u"contextL1='2'", u"normalized_word='3' "]]
        #p(where, "where")

     
        ### Case 1.3.5
        inp_syntagma_splitted = [1, 2, 3]
        inp_syntagma_unsplitted = "1++2++3"
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='1' ", u"contextR1='2'", u"contextR2='3'"], [u"contextL1='1'", u"normalized_word='2' ", u"contextR1='3'"], [u"contextL2='1'", u"contextL1='2'", u"normalized_word='3' "]]
        #p(where, "where")
     

        ### Case 1.3.5
        inp_syntagma_splitted = [1, 2, 3]
        inp_syntagma_unsplitted = u"1++2++3"
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [[u"normalized_word='1' ", u"contextR1='2'", u"contextR2='3'"], [u"contextL1='1'", u"normalized_word='2' ", u"contextR1='3'"], [u"contextL2='1'", u"contextL1='2'", u"normalized_word='3' "]]
        #p(where, "where")
     

        #########################
        ##2. without_context####
        #########################
     
        ### Case 2.0.1
        inp_syntagma_splitted = [u"😀"]
        inp_syntagma_unsplitted = u'😀'
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= '\U0001f600'"]
        #p(where)
     
        ### Case 2.0.2
        inp_syntagma_splitted = ["😀"]
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        #p(where)
        assert where == [u"syntagma= '\U0001f600'"]
     
        ### Case 2.0.3
        inp_syntagma_splitted = ["😀"]
        inp_syntagma_unsplitted = u'😀'
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        #p(where)
        assert where == [u"syntagma= '\U0001f600'"]
     
        ### Case 2.0.4
        inp_syntagma_splitted = [u"😀"]
        inp_syntagma_unsplitted = '😀'
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        #p(where)
        assert where == [u"syntagma= '\U0001f600'"]
     
        ### Case 2.0.5
        inp_syntagma_splitted = [u"😀"]
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        #p(where)
        assert where == [u"syntagma= '\U0001f600'"]
     
        ### Case 2.0.6
        inp_syntagma_splitted = ["😀"]
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        #p(where)
        assert where == [u"syntagma= '\U0001f600'"]

     

        ### Case 2.1
        inp_syntagma_splitted = ['klitze', 'kleine']
        inp_syntagma_unsplitted = 'klitze++kleine'
        scope = 2
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= 'klitze++kleine'"]
        #p(where, "where")


        ### Case 2.2
        inp_syntagma_splitted = ['klitze', 'kleine', "überaschung"]
        inp_syntagma_unsplitted = 'klitze++kleine++überaschung'
        scope = 3
        with_context =False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= 'klitze++kleine++\xfcberaschung'"]
        #p(where, "where")



        ### Case 1.3.1
        inp_syntagma_splitted = ['1', 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= '1++2++3'"]
        # p(where, "where")

        ### Case 1.3.2
        inp_syntagma_splitted = [u'1', 2, 3]
        inp_syntagma_unsplitted = '1++2++3'
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= '1++2++3'"]
        # p(where, "where")

     
        ### Case 1.3.3
        inp_syntagma_splitted = [u'1', 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= '1++2++3'"]
        # p(where, "where")



        ### Case 1.3.4
        inp_syntagma_splitted = ['1', 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= '1++2++3'"]
        # p(where, "where")


        ### Case 1.3.5
        inp_syntagma_splitted = [1, 2, 3]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= '1++2++3'"]
        # p(where, "where")


        ### Case 1.3.5
        inp_syntagma_splitted = [1, 2, 3]
        inp_syntagma_unsplitted = "1++2++3"
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= '1++2++3'"]
        # p(where, "where")


        ### Case 1.3.5
        inp_syntagma_splitted = [1, 2, 3]
        inp_syntagma_unsplitted = u"1++2++3"
        scope = 3
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context))
        assert where == [u"syntagma= '1++2++3'"]
        # p(where, "where")

     





        ################################################################################
        ###########################OTHERS###############################################
        ###############################################################################
        #########################
        ####1. with_context#####
        ########################
        ### Case 1.0.1
        inp_syntagma_splitted = ["JJ"]
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context, syntagma_type="pos"))
        assert where == [[u"pos='JJ' "]]
        #p(where, "where")#

        ### Case 1.0.2
        inp_syntagma_splitted = ["JJ", "JJ"]
        inp_syntagma_unsplitted = False
        scope = 2
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context, syntagma_type="pos"))
        assert where == [[u"pos='JJ' ", u'json_extract("context_infoR1", "$[0]")  = "JJ"'], [u'json_extract("context_infoL1", "$[0]")  = "JJ"', u"pos='JJ' "]]
        #p(where, "where")#

        ### Case 1.0.3
        inp_syntagma_splitted = ["JJ", "JJ", "JJ"]
        inp_syntagma_unsplitted = False
        scope = 3
        with_context = True
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context, syntagma_type="pos"))
        assert where == [[u"pos='JJ' ", u'json_extract("context_infoR1", "$[0]")  = "JJ"', u'json_extract("context_infoR2", "$[0]")  = "JJ"'], [u'json_extract("context_infoL1", "$[0]")  = "JJ"', u"pos='JJ' ", u'json_extract("context_infoR1", "$[0]")  = "JJ"'], [u'json_extract("context_infoL2", "$[0]")  = "JJ"', u'json_extract("context_infoL1", "$[0]")  = "JJ"', u"pos='JJ' "]]
        #p(where, "where")#



        ### Case 1.0.4
        inp_syntagma_splitted = ["JJ"]
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        sentiment = "positive"
        syntagma_type = "pos"
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context, syntagma_type=syntagma_type, sentiment=sentiment))
        assert where == [[u"pos='JJ' ", u"polarity LIKE '%positive%'"]]
        #p(where, "where")#


        ### Case 1.0.5
        inp_syntagma_splitted = ["JJ", "JJ"]
        inp_syntagma_unsplitted = False
        scope = 2
        with_context = True
        sentiment = "positive"
        syntagma_type = "pos"
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context, syntagma_type=syntagma_type, sentiment=sentiment))
        assert where == [[u"pos='JJ' ", u'json_extract("context_infoR1", "$[0]")  = "JJ"', u"polarity LIKE '%positive%'"], [u'json_extract("context_infoL1", "$[0]")  = "JJ"', u"pos='JJ' ", u"polarity LIKE '%positive%'"]]
        #p(where, "where")#



        ### Case 1.0.6
        inp_syntagma_splitted = ["like",]
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = True
        sentiment = "positive"
        syntagma_type = "lexem"
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context, syntagma_type=syntagma_type, sentiment=sentiment))
        assert where == [[u"normalized_word='like' ", u"polarity LIKE '%positive%'"]]
        #p(where, "where")#


        ### Case 1.0.7
        inp_syntagma_splitted = ["like","you"]
        inp_syntagma_unsplitted = False
        scope = 2
        with_context = True
        sentiment = "positive"
        syntagma_type = "lexem"
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context, syntagma_type=syntagma_type, sentiment=sentiment))
        assert where == [[u"normalized_word='like' ", u"contextR1='you'", u"polarity LIKE '%positive%'"], [u"contextL1='like'", u"normalized_word='you' ", u"polarity LIKE '%positive%'"]]
        #p(where, "where")#

        #########################
        ##2. without_context###
        #######################

        ### Case 2.0.1
        stats = Stats(mode="free",use_cash=True,  logger_usage=False)#, )
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))
        inp_syntagma_splitted = ["JJ"]
        inp_syntagma_unsplitted = False
        scope = 1
        with_context = False
        where = list(stats._get_where_statement(inp_syntagma_splitted, inp_syntagma_unsplitted,scope, with_context= with_context, syntagma_type="pos"))
        #p(where, "where", c="r")#
        assert not where
        
        #stats



     





    @attr(status='stable')
    # @wipd
    def test_clean_baseline_table_615(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)

        stats = Stats(mode=self.mode,use_cash=True, status_bar=True)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"


        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))
        #stats.hhh()

        baseline_rownum_bevore = stats.statsdb.rownum("baseline")
        #p((baseline_rownum_bevore))
        assert stats.clean_baseline_table()
        stats.statsdb.commit()
        assert stats.clean_baseline_table()
        stats.statsdb.commit()
        #assert stats._clean_baseline_table()


        baseline_rownum_after = stats.statsdb.rownum("baseline")


        assert baseline_rownum_bevore > baseline_rownum_after



    @attr(status='stable')
    #@wipd
    def test_drop_indexes_616(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True)#, )


        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"




        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_en))
        #stats.hhh()

        assert stats._get_created_indexes()
        
        stats._drop_created_indexes()

        assert not stats._get_created_indexes()
        #assert 




    @attr(status='stable')
    #@wipd
    def test_create_indexes_617(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True)#, )

        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_en))


        ##### Case 1
        ##### optimized_for_long_syntagmas=True #####
        ################################################
        stats._drop_created_indexes()        
        #indexes_bevore = stats._get_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created = stats.create_additional_indexes(optimized_for_long_syntagmas=True)
        #indexes_after = stats._get_created_indexes()
        number_indexes_after = stats._get_number_created_indexes()

        assert (number_indexes_after - number_indexes_bevore) == number_should_be_created


        ### Case 2
        ##### optimized_for_long_syntagmas=False #####
        ################################################
        stats._drop_created_indexes()        
        #indexes_bevore = stats._get_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created = stats.create_additional_indexes(optimized_for_long_syntagmas=False)
        #indexes_after = stats._get_created_indexes()
        number_indexes_after = stats._get_number_created_indexes()

        assert (number_indexes_after - number_indexes_bevore) == number_should_be_created



        ### Case 3
        ##### scope=3 #####
        ################################################
        stats._drop_created_indexes()        
        #indexes_bevore = stats._get_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created = stats.create_additional_indexes(scope=3, optimized_for_long_syntagmas=False)
        #indexes_after = stats._get_created_indexes()
        number_indexes_after = stats._get_number_created_indexes()

        assert (number_indexes_after - number_indexes_bevore) == number_should_be_created



        ### Case 4
        ##### indexes upgrade #####
        ################################################
        stats._drop_created_indexes()        
        #indexes_bevore = stats._get_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created = stats.create_additional_indexes(scope=2, optimized_for_long_syntagmas=False)
        stats._drop_created_indexes() 
        number_should_be_created = stats.create_additional_indexes(scope=3, optimized_for_long_syntagmas=False)
        #indexes_after = stats._get_created_indexes()
        # number_indexes_after = stats._get_number_created_indexes()

        # assert (number_indexes_after - number_indexes_bevore) == number_should_be_created




        ## Case 5
        ################################################
        ##### creation of the same indexes #####
        stats._drop_created_indexes()        
        #indexes_bevore = stats._get_created_indexes()
        number_indexes_bevore = stats._get_number_created_indexes()
        number_should_be_created1 = stats.create_additional_indexes()
        number_indexes_after1 = stats._get_number_created_indexes()
        
        ### repetativ creation of the same indexes
        number_should_be_created2 = stats.create_additional_indexes()
        #indexes_after = stats._get_created_indexes()
        number_indexes_after2 = stats._get_number_created_indexes()

        assert (number_indexes_after2 - number_indexes_bevore) == number_should_be_created1






    @attr(status='stable')
    #@wipd
    def test_clean_baseline_table_618(self):
        self.prj_folder()

        #self.blogger_corpus()
        self.test_dbs()
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True)#, )

        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_en))
        #stats.hhh()

        assert stats.optimize_db()

        

    @attr(status='stable')
    #@wipd
    def test_compute_baseline_sum_619(self):
        
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"


    ################################################
    ############ full_repetativ_syntagma=True
    #################################################

        ##### EN ######
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True, status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, full_repetativ_syntagma=True, baseline_delimiter="++")
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_en))
        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False, optimized_for_long_syntagmas=True)
        stats.optimize_db()

        ### RepCompution 
        stats._compute_baseline_sum()
        stats.statsdb.commit()

        baseline = stats.statsdb.getall("baseline")

        right_baseline  =  [(u':-(++#shetlife++http://www.noooo.com', u':-(++#shetlif++http://www.noooo.com', 3, 1, None, None, None, None, None, None), 
                            (u'tiny++model++,++which++we', u'tini++model++,++which++we', 5, 1, None, None, None, None, None, None), 
                            (u'.++:-(++@real_trump++#shetlife', u'.++:-(++@real_trump++#shetlif', 4, 1, None, None, None, None, None, None), 
                            (u'pity++for++me++.++:-(', u'piti++for++me++.++:-(', 5, 1, None, None, None, None, None, None), 
                            (u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f308++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), 
                            (u'tiny++model++,++which', u'tini++model++,++which', 4, 1, None, None, None, None, None, None), 
                            (u'a++bad++news++,', u'a++bad++news++,', 4, 1, None, None, None, None, None, None), 
                            (u'.++but', u'.++but', 2, 3, None, None, None, None, None, None), 
                            (u'.++:-(++@real_trump', u'.++:-(++@real_trump', 3, 1, None, None, None, None, None, None), 
                            (u'about++it++?++1++\U0001f62b++1', u'about++it++?++1++\U0001f62b++1', 6, 1, None, None, None, None, None, None), 
                            (u'explain++a++big', u'explain++a++big', 3, 1, None, None, None, None, None, None), 
                            (u'me++\U0001f62b++,', u'me++\U0001f62b++,', 3, 1, None, None, None, None, None, None), 
                            (u'liked++it++:p++=)++\U0001f600', u'like++it++:p++=)++\U0001f600', 5, 1, None, None, None, None, None, None), 
                            (u'realy', u'reali', 1, 4, u'2', u'4', u'1', u'3', u'2', u'1'), 
                            (u'to++se++you++-)', u'to++se++you++-)', 4, 1, None, None, None, None, None, None), 
                            (u'about++it++?++1', u'about++it++?++1', 4, 1, None, None, None, None, None, None), 
                            (u'tiny', u'tini', 1, 10, u'1', u'1', u'2', u'9', u'1', u'2'), 
                            (u'but++it++was++also++very', u'but++it++was++also++veri', 5, 1, None, None, None, None, None, None), 
                            (u'surprise++.++but++you', u'surpris++.++but++you', 4, 1, None, None, None, None, None, None), 
                            (u'\U0001f308++\U0001f600++\U0001f308', u'\U0001f308++\U0001f600++\U0001f308', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, u'1', None), 
                            (u'explanation++.++right++?++what++do', u'explan++.++right++?++what++do', 6, 1, None, None, None, None, None, None), 
                            (u'=)++\U0001f600++\U0001f308++\U0001f600', u'=)++\U0001f600++\U0001f308++\U0001f600', 4, 1, None, None, None, None, None, None), 
                            (u'what++do++you++think++about', u'what++do++you++think++about', 5, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++,', u'\U0001f62b++,', 2, 1, None, None, None, None, None, None), 
                            (u'surprise++.++but', u'surpris++.++but', 3, 1, None, None, None, None, None, None), 
                            (u'can++not++acept++.++-(++\U0001f62b', u'can++not++acept++.++-(++\U0001f62b', 6, 1, None, None, None, None, None, None), 
                            (u'\U0001f308', u'\U0001f308', 1, 3, u'3', u'3', None, None, u'3', None), 
                            (u'but++it++was++also++very++pity', u'but++it++was++also++veri++piti', 6, 1, None, None, None, None, None, None), 
                            (u'i++realy++liked', u'i++reali++like', 3, 1, None, None, None, None, None, None), 
                            (u'but++you++but', u'but++you++but', 3, 2, u'[10, 4, "IGNOR"]', u'[15, 4, "IGNOR"]', u'[4, 2, "IGNOR"]', u'[10, 4, "IGNOR"]', u'2', u'2'), 
                            (u':-(++#shetlife', u':-(++#shetlif', 2, 1, None, None, None, None, None, None), 
                            (u'a++big++things', u'a++big++thing', 3, 1, None, None, None, None, None, None), 
                            (u'?++what++do++you', u'?++what++do++you', 4, 1, None, None, None, None, None, None), 
                            (u'se', u'se', 1, 1, u'1', u'1', None, None, u'1', None), 
                            (u'.++but++you++but++you', u'.++but++you++but++you', 5, 2, None, None, None, None, None, None), 
                            (u'very++pity++for++me', u'veri++piti++for++me', 4, 1, None, None, None, None, None, None), 
                            (u'tiny++surprise++.', u'tini++surpris++.', 3, 1, None, None, None, None, None, None), 
                            (u':-(++@real_trump', u':-(++@real_trump', 2, 1, None, None, None, None, None, None), 
                            (u'-(++\U0001f62b++:-(++#shetlife', u'-(++\U0001f62b++:-(++#shetlif', 4, 1, None, None, None, None, None, None), 
                            (u'.++but++you++but', u'.++but++you++but', 4, 2, None, None, None, None, None, None), 
                            (u',++but++a++big++explanation', u',++but++a++big++explan', 5, 1, None, None, None, None, None, None), 
                            (u'=)++\U0001f600', u'=)++\U0001f600', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), 
                            (u'for++me++.++:-(++@real_trump', u'for++me++.++:-(++@real_trump', 5, 1, None, None, None, None, None, None), 
                            (u'tiny++model++,', u'tini++model++,', 3, 2, None, None, None, None, None, None), 
                            (u'you++think++about++it++?++1', u'you++think++about++it++?++1', 6, 1, None, None, None, None, None, None), 
                            (u'use++for++explain++a++big++things', u'use++for++explain++a++big++thing', 6, 1, None, None, None, None, None, None), 
                            (u'use++for++explain++a++big', u'use++for++explain++a++big', 5, 1, None, None, None, None, None, None), 
                            (u'model++,++which++we++can', u'model++,++which++we++can', 5, 1, None, None, None, None, None, None), 
                            (u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', u'it++:p++=)++\U0001f600++\U0001f308++\U0001f600', 6, 1, None, None, None, None, None, None), 
                            (u'?++what++do++you++think', u'?++what++do++you++think', 5, 1, None, None, None, None, None, None), 
                            (u'bad++news++,', u'bad++news++,', 3, 1, None, None, None, None, None, None), 
                            (u'but++you++but++you', u'but++you++but++you', 4, 2, u'[10, 6, "IGNOR", "IGNOR"]', u'[15, 8, "IGNOR", "IGNOR"]', None, None, u'2', None), 
                            (u'bad', u'bad', 1, 6, u'4', u'7', u'1', u'5', u'4', u'1'), 
                            (u'pity++for++me', u'piti++for++me', 3, 1, None, None, None, None, None, None), 
                            (u'.++-(++\U0001f62b++:-(', u'.++-(++\U0001f62b++:-(', 4, 1, None, None, None, None, None, None), 
                            (u'tiny++surprise++.++but++you', u'tini++surpris++.++but++you', 5, 1, None, None, None, None, None, None), 
                            (u'but++i++realy++liked', u'but++i++reali++like', 4, 1, None, None, None, None, None, None), 
                            (u',++but++i++realy++liked', u',++but++i++reali++like', 5, 1, None, None, None, None, None, None), 
                            (u'.++right++?', u'.++right++?', 3, 1, None, None, None, None, None, None), 
                            (u'1++\U0001f62b++1++.++but++you', u'1++\U0001f62b++1++.++but++you', 6, 1, None, None, None, None, None, None), 
                            (u'a++bad++news++,++which++we', u'a++bad++news++,++which++we', 6, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++:-(', u'\U0001f62b++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), 
                            (u'?++1++\U0001f62b++1', u'?++1++\U0001f62b++1', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[1, 2, 1, "IGNOR"]', None, None, u'1', None), 
                            (u'.++but++it++was++also++very', u'.++but++it++was++also++veri', 6, 1, None, None, None, None, None, None), 
                            (u',++but++a++big', u',++but++a++big', 4, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++:-(++#shetlife', u'\U0001f62b++:-(++#shetlif', 3, 1, None, None, None, None, None, None), 
                            (u'also++very++pity++for++me', u'also++veri++piti++for++me', 5, 1, None, None, None, None, None, None), 
                            (u'but++a++big++explanation++.++right', u'but++a++big++explan++.++right', 6, 1, None, None, None, None, None, None), 
                            (u'it++was++also++very', u'it++was++also++veri', 4, 1, None, None, None, None, None, None), 
                            (u'but++a++big++explanation++.', u'but++a++big++explan++.', 5, 1, None, None, None, None, None, None), 
                            (u',++but++i++realy', u',++but++i++reali', 4, 1, None, None, None, None, None, None), 
                            (u'it++?++1++\U0001f62b', u'it++?++1++\U0001f62b', 4, 1, None, None, None, None, None, None), 
                            (u'a++big', u'a++big', 2, 2, None, None, None, None, None, None), 
                            (u'acept++.++-(', u'acept++.++-(', 3, 1, None, None, None, None, None, None), 
                            (u'but', u'but', 1, 13, u'11', u'16', u'4', u'10', u'11', u'4'), 
                            (u'tiny++surprise', u'tini++surpris', 2, 1, None, None, None, None, None, None), 
                            (u'realy++liked', u'reali++like', 2, 1, None, None, None, None, None, None), 
                            (u'what++do++you++think++about++it', u'what++do++you++think++about++it', 6, 1, None, None, None, None, None, None), 
                            (u':p++=)++\U0001f600++\U0001f308++\U0001f600', u':p++=)++\U0001f600++\U0001f308++\U0001f600', 5, 1, None, None, None, None, None, None), 
                            (u'you++-)', u'you++-)', 2, 1, None, None, None, None, None, None), 
                            (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308', 4, 1, u'[2, 2, "IGNOR", "IGNOR"]', u'[2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), 
                            (u'.++:-(++@real_trump++#shetlife++#readytogo', u'.++:-(++@real_trump++#shetlif++#readytogo', 5, 1, None, None, None, None, None, None), 
                            (u'what++do++you', u'what++do++you', 3, 1, None, None, None, None, None, None), 
                            (u'surprise++for++me++\U0001f62b', u'surpris++for++me++\U0001f62b', 4, 1, None, None, None, None, None, None), 
                            (u'?++what++do++you++think++about', u'?++what++do++you++think++about', 6, 1, None, None, None, None, None, None), 
                            (u'a++bad++news', u'a++bad++news', 3, 1, None, None, None, None, None, None), 
                            (u'very++pity++for', u'veri++piti++for', 3, 1, None, None, None, None, None, None), 
                            (u',++but++i', u',++but++i', 3, 1, None, None, None, None, None, None), 
                            (u'glad++to', u'glad++to', 2, 1, None, None, None, None, None, None), 
                            (u'big++things++.', u'big++thing++.', 3, 1, None, None, None, None, None, None), 
                            (u'for++me++\U0001f62b++,', u'for++me++\U0001f62b++,', 4, 1, None, None, None, None, None, None), 
                            (u':-(++@real_trump++#shetlife++#readytogo', u':-(++@real_trump++#shetlif++#readytogo', 4, 1, None, None, None, None, None, None), 
                            (u'.++:-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u'.++:-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 6, 1, None, None, None, None, None, None), 
                            (u'.', u'.', 1, 7, u'1', u'1', None, None, u'1', None), 
                            (u'but++i++realy++liked++it', u'but++i++reali++like++it', 5, 1, None, None, None, None, None, None), 
                            (u'pity', u'piti', 1, 4, u'2', u'4', u'1', u'4', u'2', u'1'), 
                            (u'explanation++.++right++?', u'explan++.++right++?', 4, 1, None, None, None, None, None, None), 
                            (u'do++you++think++about++it', u'do++you++think++about++it', 5, 1, None, None, None, None, None, None), 
                            (u'think++about++it++?++1', u'think++about++it++?++1', 5, 1, None, None, None, None, None, None), 
                            (u'also++very++pity++for++me++.', u'also++veri++piti++for++me++.', 6, 1, None, None, None, None, None, None), 
                            (u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, u'1', None), 
                            (u'se++you', u'se++you', 2, 1, None, None, None, None, None, None), 
                            (u'realy++liked++it', u'reali++like++it', 3, 1, None, None, None, None, None, None), 
                            (u'me++\U0001f62b++,++but', u'me++\U0001f62b++,++but', 4, 1, None, None, None, None, None, None), 
                            (u'for++me++.++:-(++@real_trump++#shetlife', u'for++me++.++:-(++@real_trump++#shetlif', 6, 1, None, None, None, None, None, None), 
                            (u'\U0001f600++\U0001f308++\U0001f600', u'\U0001f600++\U0001f308++\U0001f600', 3, 3, u'[2, 1, "IGNOR"]', u'[3, 1, "IGNOR"]', None, None, u'1', None), 
                            (u'big++explanation++.++right++?', u'big++explan++.++right++?', 5, 1, None, None, None, None, None, None), 
                            (u'bad++news', u'bad++news', 2, 1, None, None, None, None, None, None), 
                            (u'glad++to++se++you', u'glad++to++se++you', 4, 1, None, None, None, None, None, None), 
                            (u'model++,++but++a++big', u'model++,++but++a++big', 5, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++1++.', u'\U0001f62b++1++.', 3, 1, None, None, None, None, None, None), 
                            (u'it++:p++=)++\U0001f600++\U0001f308', u'it++:p++=)++\U0001f600++\U0001f308', 5, 1, None, None, None, None, None, None), 
                            (u'explain++a++big++things', u'explain++a++big++thing', 4, 1, None, None, None, None, None, None), 
                            (u'also++very', u'also++veri', 2, 1, None, None, None, None, None, None), 
                            (u'to++se', u'to++se', 2, 1, None, None, None, None, None, None), 
                            (u'you++but++you++\U0001f600++\U0001f308', u'you++but++you++\U0001f600++\U0001f308', 5, 1, u'[3, 3, "IGNOR", 1, 1]', u'[4, 3, "IGNOR", 1, 1]', None, None, u'1', None), 
                            (u'to++se++you', u'to++se++you', 3, 1, None, None, None, None, None, None), 
                            (u'realy++bad++surprise++for++me++\U0001f62b', u'reali++bad++surpris++for++me++\U0001f62b', 6, 1, None, None, None, None, None, None), 
                            (u'realy++liked++it++:p', u'reali++like++it++:p', 4, 1, None, None, None, None, None, None), 
                            (u'you++but++you++\U0001f600', u'you++but++you++\U0001f600', 4, 1, u'[3, 3, "IGNOR", 1]', u'[4, 3, "IGNOR", 1]', None, None, u'1', None), 
                            (u'not++acept++.++-(++\U0001f62b++:-(', u'not++acept++.++-(++\U0001f62b++:-(', 6, 1, None, None, None, None, None, None), 
                            (u'very', u'veri', 1, 3, u'2', u'4', u'1', u'3', u'2', u'1'), 
                            (u'1++.++but++you', u'1++.++but++you', 4, 1, None, None, None, None, None, None), 
                            (u'surprise++for++me++\U0001f62b++,', u'surpris++for++me++\U0001f62b++,', 5, 1, None, None, None, None, None, None), 
                            (u'.++right++?++what++do', u'.++right++?++what++do', 5, 1, None, None, None, None, None, None), 
                            (u'was++also++very++pity', u'was++also++veri++piti', 4, 1, None, None, None, None, None, None), 
                            (u'1++\U0001f62b++1', u'1++\U0001f62b++1', 3, 1, u'[2, 1, "IGNOR"]', u'[2, 1, "IGNOR"]', None, None, u'1', None), 
                            (u'big++explanation++.++right', u'big++explan++.++right', 4, 1, None, None, None, None, None, None), 
                            (u'for++explain++a++big', u'for++explain++a++big', 4, 1, None, None, None, None, None, None), 
                            (u'for++me++\U0001f62b++,++but++i', u'for++me++\U0001f62b++,++but++i', 6, 1, None, None, None, None, None, None), 
                            (u':-(++@real_trump++#shetlife', u':-(++@real_trump++#shetlif', 3, 1, None, None, None, None, None, None), 
                            (u'?++1++\U0001f62b++1++.++but', u'?++1++\U0001f62b++1++.++but', 6, 1, None, None, None, None, None, None), 
                            (u'1++\U0001f62b++1++.++but', u'1++\U0001f62b++1++.++but', 5, 1, None, None, None, None, None, None), 
                            (u'think++about++it++?', u'think++about++it++?', 4, 1, None, None, None, None, None, None), 
                            (u'big', u'big', 1, 5, u'2', u'2', u'2', u'5', u'2', u'2'), 
                            (u'realy++liked++it++:p++=)', u'reali++like++it++:p++=)', 5, 1, None, None, None, None, None, None), 
                            (u'we++can++not++acept++.++-(', u'we++can++not++acept++.++-(', 6, 1, None, None, None, None, None, None), 
                            (u'a++big++explanation++.', u'a++big++explan++.', 4, 1, None, None, None, None, None, None), 
                            (u'for++explain++a++big++things', u'for++explain++a++big++thing', 5, 1, None, None, None, None, None, None), 
                            (u'model', u'model', 1, 2, u'1', u'2', None, None, u'1', None), 
                            (u'bad++news++,++which', u'bad++news++,++which', 4, 1, None, None, None, None, None, None), 
                            (u'you++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600', 4, 1, u'[1, 2, 1, "IGNOR"]', u'[2, 2, 1, "IGNOR"]', None, None, u'1', None), 
                            (u'i++realy++liked++it++:p', u'i++reali++like++it++:p', 5, 1, None, None, None, None, None, None), 
                            (u'but++i++realy++liked++it++:p', u'but++i++reali++like++it++:p', 6, 1, None, None, None, None, None, None), 
                            (u'glad++to++se++you++-)', u'glad++to++se++you++-)', 5, 1, None, None, None, None, None, None), 
                            (u'1++\U0001f62b++1++.', u'1++\U0001f62b++1++.', 4, 1, None, None, None, None, None, None), 
                            (u'you++think', u'you++think', 2, 1, None, None, None, None, None, None), 
                            (u'not++acept++.++-(++\U0001f62b', u'not++acept++.++-(++\U0001f62b', 5, 1, None, None, None, None, None, None), 
                            (u',++but++a++big++explanation++.', u',++but++a++big++explan++.', 6, 1, None, None, None, None, None, None), 
                            (u'think++about++it++?++1++\U0001f62b', u'think++about++it++?++1++\U0001f62b', 6, 1, None, None, None, None, None, None), 
                            (u'but++you', u'but++you', 2, 4, u'[10, 6]', u'[15, 8]', u'[2, 2]', u'[4, 4]', u'4', u'2'), 
                            (u'-)', u'-)', 1, 1, u'1', u'1', None, None, u'1', None), 
                            (u'-(++\U0001f62b', u'-(++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), 
                            (u'big++explanation++.++right++?++what', u'big++explan++.++right++?++what', 6, 1, None, None, None, None, None, None), 
                            (u'me++.++:-(', u'me++.++:-(', 3, 1, None, None, None, None, None, None), 
                            (u'tiny++surprise++.++but', u'tini++surpris++.++but', 4, 1, None, None, None, None, None, None), 
                            (u'-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 5, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++1++.++but++you', u'\U0001f62b++1++.++but++you', 5, 1, None, None, None, None, None, None), 
                            (u'it++?', u'it++?', 2, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++,++but', u'\U0001f62b++,++but', 3, 1, None, None, None, None, None, None), 
                            (u'model++,', u'model++,', 2, 2, None, None, None, None, None, None), 
                            (u'me++.++:-(++@real_trump++#shetlife++#readytogo', u'me++.++:-(++@real_trump++#shetlif++#readytogo', 6, 1, None, None, None, None, None, None), 
                            (u'right++?++what++do', u'right++?++what++do', 4, 1, None, None, None, None, None, None), 
                            (u'\U0001f308++\U0001f600', u'\U0001f308++\U0001f600', 2, 3, u'[2, 2]', u'[2, 2]', None, None, u'2', None), 
                            (u'=)', u'=)', 1, 1, u'1', u'1', None, None, u'1', None), 
                            (u'it++was++also++very++pity', u'it++was++also++veri++piti', 5, 1, None, None, None, None, None, None), 
                            (u'i++realy++liked++it', u'i++reali++like++it', 4, 1, None, None, None, None, None, None), 
                            (u'se++you++-)', u'se++you++-)', 3, 1, None, None, None, None, None, None), 
                            (u'tiny++model', u'tini++model', 2, 2, None, None, None, None, None, None), 
                            (u'it++:p++=)++\U0001f600', u'it++:p++=)++\U0001f600', 4, 1, None, None, None, None, None, None), 
                            (u'a++bad++news++,++which', u'a++bad++news++,++which', 5, 1, None, None, None, None, None, None), 
                            (u'it++?++1++\U0001f62b++1++.', u'it++?++1++\U0001f62b++1++.', 6, 1, None, None, None, None, None, None), 
                            (u'1++.++but++you++but', u'1++.++but++you++but', 5, 1, None, None, None, None, None, None), 
                            (u'right', u'right', 1, 1, u'1', u'1', None, None, u'1', None), 
                            (u'it++:p++=)', u'it++:p++=)', 3, 1, None, None, None, None, None, None), 
                            (u'model++,++which++we', u'model++,++which++we', 4, 1, None, None, None, None, None, None), 
                            (u'but++you++but++you++\U0001f600++\U0001f308', u'but++you++but++you++\U0001f600++\U0001f308', 6, 1, u'[5, 3, "IGNOR", "IGNOR", 1, 1]', u'[5, 4, "IGNOR", "IGNOR", 1, 1]', None, None, u'1', None), 
                            (u'#shetlife', u'#shetlif', 1, 3, None, None, u'1', u'2', None, u'1'), 
                            (u'?', u'?', 1, 2, u'1', u'1', None, None, u'1', None), 
                            (u'me++.++:-(++@real_trump', u'me++.++:-(++@real_trump', 4, 1, None, None, None, None, None, None), 
                            (u'acept++.++-(++\U0001f62b++:-(', u'acept++.++-(++\U0001f62b++:-(', 5, 1, None, None, None, None, None, None), 
                            (u'but++you++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308', 4, 1, u'[3, 1, 1, 1]', u'[3, 2, 1, 1]', None, None, u'1', None), 
                            (u'very++pity++for++me++.', u'veri++piti++for++me++.', 5, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'\U0001f62b++:-(++#shetlif++http://www.noooo.com', 4, 1, None, None, None, None, None, None), 
                            (u'explanation++.', u'explan++.', 2, 1, None, None, None, None, None, None), 
                            (u'.++but++you++but++you++\U0001f600', u'.++but++you++but++you++\U0001f600', 6, 1, None, None, None, None, None, None), 
                            (u'.++-(++\U0001f62b++:-(++#shetlife++http://www.noooo.com', u'.++-(++\U0001f62b++:-(++#shetlif++http://www.noooo.com', 6, 1, None, None, None, None, None, None), 
                            (u'.++-(', u'.++-(', 2, 1, None, None, None, None, None, None), 
                            (u'i++realy++liked++it++:p++=)', u'i++reali++like++it++:p++=)', 6, 1, None, None, None, None, None, None), 
                            (u'\U0001f600++\U0001f308', u'\U0001f600++\U0001f308', 2, 3, u'[3, 3]', u'[3, 3]', None, None, u'3', None), 
                            (u'explanation', u'explan', 1, 1, u'1', u'1', None, None, u'1', None), 
                            (u'you++but++you++\U0001f600++\U0001f308++\U0001f600', u'you++but++you++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[3, 3, "IGNOR", 2, 1, "IGNOR"]', u'[4, 3, "IGNOR", 2, 1, "IGNOR"]', None, None, u'1', None), 
                            (u'do++you++think', u'do++you++think', 3, 1, None, None, None, None, None, None), 
                            (u'acept++.++-(++\U0001f62b++:-(++#shetlife', u'acept++.++-(++\U0001f62b++:-(++#shetlif', 6, 1, None, None, None, None, None, None), 
                            (u'but++i', u'but++i', 2, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++,++but++i++realy++liked', u'\U0001f62b++,++but++i++reali++like', 6, 1, None, None, None, None, None, None), 
                            (u'me++\U0001f62b++,++but++i++realy', u'me++\U0001f62b++,++but++i++reali', 6, 1, None, None, None, None, None, None), 
                            (u'but++you++but++you++\U0001f600', u'but++you++but++you++\U0001f600', 5, 1, u'[5, 3, "IGNOR", "IGNOR", 1]', u'[5, 4, "IGNOR", "IGNOR", 1]', None, None, u'1', None), 
                            (u'acept++.++-(++\U0001f62b', u'acept++.++-(++\U0001f62b', 4, 1, None, None, None, None, None, None), 
                            (u',++but', u',++but', 2, 2, None, None, None, None, None, None), 
                            (u'was++also++very++pity++for', u'was++also++veri++piti++for', 5, 1, None, None, None, None, None, None), 
                            (u'surprise++.++but++you++but', u'surpris++.++but++you++but', 5, 1, None, None, None, None, None, None), 
                            (u'surprise++.++but++you++but++you', u'surpris++.++but++you++but++you', 6, 1, None, None, None, None, None, None), 
                            (u'a++big++explanation++.++right', u'a++big++explan++.++right', 5, 1, None, None, None, None, None, None), 
                            (u':p++=)', u':p++=)', 2, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++,++but++i', u'\U0001f62b++,++but++i', 4, 1, None, None, None, None, None, None), 
                            (u'tiny++model++,++which++we++can', u'tini++model++,++which++we++can', 6, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++1', u'\U0001f62b++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), 
                            (u'?++1++\U0001f62b', u'?++1++\U0001f62b', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), 
                            (u'was++also++very', u'was++also++veri', 3, 1, None, None, None, None, None, None), 
                            (u':p++=)++\U0001f600++\U0001f308', u':p++=)++\U0001f600++\U0001f308', 4, 1, None, None, None, None, None, None), 
                            (u'surprise++for++me++\U0001f62b++,++but', u'surpris++for++me++\U0001f62b++,++but', 6, 1, None, None, None, None, None, None), 
                            (u'about++it++?++1++\U0001f62b', u'about++it++?++1++\U0001f62b', 5, 1, None, None, None, None, None, None), 
                            (u'me++.++:-(++@real_trump++#shetlife', u'me++.++:-(++@real_trump++#shetlif', 5, 1, None, None, None, None, None, None), 
                            (u'you++think++about++it', u'you++think++about++it', 4, 1, None, None, None, None, None, None), 
                            (u'but++you++\U0001f600++\U0001f308++\U0001f600', u'but++you++\U0001f600++\U0001f308++\U0001f600', 5, 1, u'[3, 1, 2, 1, "IGNOR"]', u'[3, 2, 2, 1, "IGNOR"]', None, None, u'1', None), 
                            (u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'but++you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 6, 1, u'[3, 1, 2, 2, "IGNOR", "IGNOR"]', u'[3, 2, 2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), 
                            (u'also++very++pity++for', u'also++veri++piti++for', 4, 1, None, None, None, None, None, None), 
                            (u'you++\U0001f600', u'you++\U0001f600', 2, 1, u'[1, 1]', u'[2, 1]', None, None, u'1', None), 
                            (u'glad++to++se', u'glad++to++se', 3, 1, None, None, None, None, None, None), 
                            (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308', 5, 1, u'[1, 2, 2, "IGNOR", "IGNOR"]', u'[2, 2, 2, "IGNOR", "IGNOR"]', None, None, u'1', None), 
                            (u'#shetlife++http://www.noooo.com', u'#shetlif++http://www.noooo.com', 2, 1, None, None, None, None, None, None), 
                            (u'1++.++but++you++but++you', u'1++.++but++you++but++you', 6, 1, None, None, None, None, None, None), 
                            (u'was++also++very++pity++for++me', u'was++also++veri++piti++for++me', 6, 1, None, None, None, None, None, None), 
                            (u'.++-(++\U0001f62b++:-(++#shetlife', u'.++-(++\U0001f62b++:-(++#shetlif', 5, 1, None, None, None, None, None, None), 
                            (u'1++.', u'1++.', 2, 1, None, None, None, None, None, None), 
                            (u'i++realy', u'i++reali', 2, 1, None, None, None, None, None, None), 
                            (u'can++use++for++explain++a++big', u'can++use++for++explain++a++big', 6, 1, None, None, None, None, None, None), 
                            (u'very++pity', u'veri++piti', 2, 1, u'[2, 2]', u'[4, 4]', u'[1, 1]', u'[3, 4]', u'1', u'1'), 
                            (u'liked++it++:p++=)++\U0001f600++\U0001f308', u'like++it++:p++=)++\U0001f600++\U0001f308', 6, 1, None, None, None, None, None, None), 
                            (u'do++you++think++about', u'do++you++think++about', 4, 1, None, None, None, None, None, None), 
                            (u'bad++surprise++for++me++\U0001f62b++,', u'bad++surpris++for++me++\U0001f62b++,', 6, 1, None, None, None, None, None, None), 
                            (u':-(++@real_trump++#shetlife++#readytogo++http://www.absurd.com', u':-(++@real_trump++#shetlif++#readytogo++http://www.absurd.com', 5, 1, None, None, None, None, None, None), 
                            (u'me++.', u'me++.', 2, 1, None, None, None, None, None, None), 
                            (u'me++\U0001f62b++,++but++i', u'me++\U0001f62b++,++but++i', 5, 1, None, None, None, None, None, None), 
                            (u'you++think++about++it++?', u'you++think++about++it++?', 5, 1, None, None, None, None, None, None), 
                            (u'right++?++what++do++you', u'right++?++what++do++you', 5, 1, None, None, None, None, None, None), 
                            (u'1', u'1', 1, 2, u'2', u'2', None, None, u'2', None), 
                            (u'pity++for++me++.', u'piti++for++me++.', 4, 1, None, None, None, None, None, None), 
                            (u'explain++a++big++things++.', u'explain++a++big++thing++.', 5, 1, None, None, None, None, None, None), 
                            (u'what++do++you++think', u'what++do++you++think', 4, 1, None, None, None, None, None, None), 
                            (u'for++me++.++:-(', u'for++me++.++:-(', 4, 1, None, None, None, None, None, None), 
                            (u'\U0001f600', u'\U0001f600', 1, 5, u'4', u'4', None, None, u'4', None), 
                            (u'you++but', u'you++but', 2, 2, u'[4, 6]', u'[4, 8]', u'[2, 2]', u'[4, 6]', u'2', u'2'), 
                            (u'bad++news++,++which++we', u'bad++news++,++which++we', 5, 1, None, None, None, None, None, None), 
                            (u'very++pity++for++me++.++:-(', u'veri++piti++for++me++.++:-(', 6, 1, None, None, None, None, None, None), 
                            (u'.++right++?++what', u'.++right++?++what', 4, 1, None, None, None, None, None, None), 
                            (u'.++but++you', u'.++but++you', 3, 2, None, None, None, None, None, None), 
                            (u'but++a++big', u'but++a++big', 3, 1, None, None, None, None, None, None), 
                            (u'it++was++also++very++pity++for', u'it++was++also++veri++piti++for', 6, 1, None, None, None, None, None, None), 
                            (u'bad++news++,++which++we++can', u'bad++news++,++which++we++can', 6, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++,++but++i++realy', u'\U0001f62b++,++but++i++reali', 5, 1, None, None, None, None, None, None), 
                            (u'=)++\U0001f600++\U0001f308', u'=)++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), 
                            (u'for++me++.', u'for++me++.', 3, 1, None, None, None, None, None, None), 
                            (u'realy++liked++it++:p++=)++\U0001f600', u'reali++like++it++:p++=)++\U0001f600', 6, 1, None, None, None, None, None, None), 
                            (u'explanation++.++right++?++what', u'explan++.++right++?++what', 5, 1, None, None, None, None, None, None), 
                            (u'model++,++but++a++big++explanation', u'model++,++but++a++big++explan', 6, 1, None, None, None, None, None, None), 
                            (u'a++big++explanation', u'a++big++explan', 3, 1, None, None, None, None, None, None), 
                            (u'you++but++you', u'you++but++you', 3, 2, u'[6, 6, "IGNOR"]', u'[8, 8, "IGNOR"]', None, None, u'2', None), 
                            (u'-(++\U0001f62b++:-(', u'-(++\U0001f62b++:-(', 3, 1, u'[1, 1, 1]', u'[1, 1, 1]', None, None, u'1', None), 
                            (u'explanation++.++right', u'explan++.++right', 3, 1, None, None, None, None, None, None), 
                            (u'you', u'you', 1, 8, u'7', u'9', u'2', u'4', u'7', u'2'), 
                            (u'big++things', u'big++thing', 2, 1, None, None, None, None, None, None), 
                            (u'it++?++1', u'it++?++1', 3, 1, None, None, None, None, None, None), 
                            (u'for++me++\U0001f62b', u'for++me++\U0001f62b', 3, 1, None, None, None, None, None, None), 
                            (u'-(', u'-(', 1, 1, u'1', u'1', None, None, u'1', None), 
                            (u'tiny++surprise++.++but++you++but', u'tini++surpris++.++but++you++but', 6, 1, None, None, None, None, None, None), 
                            (u'right++?++what++do++you++think', u'right++?++what++do++you++think', 6, 1, None, None, None, None, None, None), 
                            (u'big++explanation++.', u'big++explan++.', 3, 1, None, None, None, None, None, None), 
                            (u'for++explain++a++big++things++.', u'for++explain++a++big++thing++.', 6, 1, None, None, None, None, None, None), 
                            (u'.++right', u'.++right', 2, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b', u'\U0001f62b', 1, 3, u'3', u'3', None, None, u'3', None), 
                            (u'not++acept++.++-(', u'not++acept++.++-(', 4, 1, None, None, None, None, None, None), 
                            (u'for++me++\U0001f62b++,++but', u'for++me++\U0001f62b++,++but', 5, 1, None, None, None, None, None, None), 
                            (u'you++think++about', u'you++think++about', 3, 1, None, None, None, None, None, None), 
                            (u'a++bad', u'a++bad', 2, 1, None, None, None, None, None, None), 
                            (u'?++1', u'?++1', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), 
                            (u'do++you++think++about++it++?', u'do++you++think++about++it++?', 6, 1, None, None, None, None, None, None), 
                            (u'can++not++acept++.++-(', u'can++not++acept++.++-(', 5, 1, None, None, None, None, None, None), 
                            (u'a++big++things++.', u'a++big++thing++.', 4, 1, None, None, None, None, None, None), 
                            (u'but++you++\U0001f600', u'but++you++\U0001f600', 3, 1, u'[3, 1, 1]', u'[3, 2, 1]', None, None, u'1', None), 
                            (u'\U0001f62b++1++.++but', u'\U0001f62b++1++.++but', 4, 1, None, None, None, None, None, None), 
                            (u'right++?', u'right++?', 2, 1, None, None, None, None, None, None), 
                            (u'\U0001f62b++1++.++but++you++but', u'\U0001f62b++1++.++but++you++but', 6, 1, None, None, None, None, None, None), 
                            (u'pity++for++me++.++:-(++@real_trump', u'piti++for++me++.++:-(++@real_trump', 6, 1, None, None, None, None, None, None), 
                            (u'it++?++1++\U0001f62b++1', u'it++?++1++\U0001f62b++1', 5, 1, None, None, None, None, None, None), 
                            (u'tiny++model++,++but++a++big', u'tini++model++,++but++a++big', 6, 1, None, None, None, None, None, None), 
                            (u'right++?++what', u'right++?++what', 3, 1, None, None, None, None, None, None), 
                            (u'bad++surprise++for++me++\U0001f62b', u'bad++surpris++for++me++\U0001f62b', 5, 1, None, None, None, None, None, None), 
                            (u'model++,++which', u'model++,++which', 3, 1, None, None, None, None, None, None), 
                            (u'1++.++but', u'1++.++but', 3, 1, None, None, None, None, None, None), 
                            (u'pity++for', u'piti++for', 2, 1, None, None, None, None, None, None), 
                            (u':p++=)++\U0001f600', u':p++=)++\U0001f600', 3, 1, None, None, None, None, None, None), 
                            (u'me++\U0001f62b', u'me++\U0001f62b', 2, 1, None, None, None, None, None, None), 
                            (u'also++very++pity', u'also++veri++piti', 3, 1, None, None, None, None, None, None), 
                            (u'model++,++which++we++can++use', u'model++,++which++we++can++use', 6, 1, None, None, None, None, None, None), 
                            (u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', u'you++\U0001f600++\U0001f308++\U0001f600++\U0001f308++\U0001f600', 6, 1, u'[1, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', u'[2, 3, 2, "IGNOR", "IGNOR", "IGNOR"]', None, None, u'1', None), 
                            (u'about++it++?', u'about++it++?', 3, 1, None, None, None, None, None, None), 
                            (u'but++i++realy', u'but++i++reali', 3, 1, None, None, None, None, None, None), 
                            (u'liked++it++:p++=)', u'like++it++:p++=)', 4, 1, None, None, None, None, None, None), 
                            (u'do++you', u'do++you', 2, 1, None, None, None, None, None, None), 
                            (u'1++\U0001f62b', u'1++\U0001f62b', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), 
                            (u':-(', u':-(', 1, 2, u'2', u'2', None, None, u'2', None), 
                            (u'?++1++\U0001f62b++1++.', u'?++1++\U0001f62b++1++.', 5, 1, None, None, None, None, None, None), 
                            (u'.++right++?++what++do++you', u'.++right++?++what++do++you', 6, 1, None, None, None, None, None, None), 
                            (u'big++explanation', u'big++explan', 2, 1, None, None, None, None, None, None), 
                            (u'.++-(++\U0001f62b', u'.++-(++\U0001f62b', 3, 1, None, None, None, None, None, None), 
                            (u'but++a++big++explanation', u'but++a++big++explan', 4, 1, None, None, None, None, None, None), 
                            (u'.++:-(', u'.++:-(', 2, 1, u'[1, 1]', u'[1, 1]', None, None, u'1', None), 
                            (u'glad', u'glad', 1, 1, u'1', u'1', None, None, u'1', None), 
                            (u'a++big++explanation++.++right++?', u'a++big++explan++.++right++?', 6, 1, None, None, None, None, None, None), 
                            (u'you++\U0001f600++\U0001f308', u'you++\U0001f600++\U0001f308', 3, 1, u'[1, 1, 1]', u'[2, 1, 1]', None, None, u'1', None), 
                            (u',++but++i++realy++liked++it', u',++but++i++reali++like++it', 6, 1, None, None, None, None, None, None)]
        #p(baseline ,"baseline")
    
        set([ tuple(unicode(item) for item in b ) for b in baseline]).should.be.equal(set([ tuple(unicode(item) for item in b ) for b in right_baseline]))
        assert stats._compute_baseline_sum() > 0




    @attr(status='stable')
    #@wipd
    def test_recompute_syntagma_repetativity_scope_621(self):
        
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        name = self.configer.init_info_data["blogger"]["name"]
        language = self.configer.init_info_data["blogger"]["language"]
        visibility = self.configer.init_info_data["blogger"]["visibility"]
        platform_name = self.configer.init_info_data["blogger"]["platform_name"]
        license = self.configer.init_info_data["blogger"]["license"]
        template_name = self.configer.init_info_data["blogger"]["template_name"]
        version = self.configer.init_info_data["blogger"]["version"]
        source = self.configer.init_info_data["blogger"]["source"]
        encryption_key = self.configer.init_info_data["blogger"]["encryption_key"]["stats"]
        corpus_id = self.configer.init_info_data["blogger"]["id"]["corpus"]
        stats_id = self.configer.init_info_data["blogger"]["id"]["stats"]
        typ= "stats"



        
        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True, status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, full_repetativ_syntagma=True, baseline_delimiter="++")
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_de))
        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False)
        stats.optimize_db()

        ### RepCompution 
        assert stats._full_repetativ_syntagma == True
        assert stats.recompute_syntagma_repetativity_scope(False)
        assert stats._full_repetativ_syntagma == False
        assert stats.recompute_syntagma_repetativity_scope(True)
        assert stats._full_repetativ_syntagma == True
 




        #stats = Stats(mode=self.mode)
        stats = Stats(mode=self.mode,use_cash=True, status_bar=True)#, )
        stats.init(self.tempdir_project_folder, name, language, visibility,  corpus_id=corpus_id,  version= version, encryption_key=encryption_key, full_repetativ_syntagma=False, baseline_delimiter="++")
        corp = Corpus(mode=self.mode)
        corp.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_corp_de))
        stats.compute(corp,stream_number=1,adjust_to_cpu=False, freeze_db=False)
        stats.optimize_db()

        ### RepCompution 
        assert stats._full_repetativ_syntagma == False
        assert stats.recompute_syntagma_repetativity_scope(True)
        assert stats._full_repetativ_syntagma == True
        assert stats.recompute_syntagma_repetativity_scope(False)
        assert stats._full_repetativ_syntagma == False




    @attr(status='stable')
    #@wipd
    def test_reconstruct_syntagma_630(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))
        
        indexes = {'repl': {u'pos': 10, u'index_of_repl': 9, u'id': 0, u'polarity': 11, u'in_redu': 12, u'context_infoL2': 20, u'context_infoL3': 18, u'context_infoL1': 22, u'context_infoL4': 16, u'context_infoL5': 14, u'contextR2': 25, u'contextR3': 27, u'contextR1': 23, u'contextR4': 29, u'contextR5': 31, u'rle_word': 6, u'index_in_redufree': 4, u'contextL1': 21, u'contextL4': 15, u'contextL5': 13, u'redufree_len': 2, u'repl_length': 8, u'contextL2': 19, u'contextL3': 17, u'context_infoR1': 24, u'context_infoR2': 26, u'context_infoR3': 28, u'context_infoR4': 30, u'context_infoR5': 32, u'index_in_corpus': 3, u'normalized_word': 5, u'doc_id': 1, u'repl_letter': 7}, 'baseline': {u'occur_repl_uniq': 3, u'syntagma': 0, u'hight_scope_uniq_occur_redu': 8, u'occur_redu_exhausted': 6, u'occur_redu_uniq': 5, u'hight_scope_uniq_occur_repl': 7, u'occur_syntagma_all': 1, u'scope': 2, u'occur_repl_exhausted': 4}, 'redu': {u'orig_words': 6, u'pos': 8, u'id': 0, u'polarity': 9, u'redu_length': 7, u'context_infoL2': 17, u'context_infoL3': 15, u'context_infoL1': 19, u'context_infoL4': 13, u'context_infoL5': 11, u'contextR2': 22, u'contextR3': 24, u'contextR1': 20, u'contextR4': 26, u'contextR5': 28, u'index_in_redufree': 4, u'contextL4': 12, u'contextL5': 10, u'redufree_len': 2, u'contextL1': 18, u'contextL2': 16, u'contextL3': 14, u'context_infoR1': 21, u'context_infoR2': 23, u'context_infoR3': 25, u'context_infoR4': 27, u'context_infoR5': 29, u'index_in_corpus': 3, u'normalized_word': 5, u'doc_id': 1}}

        ######## rep_type = 'repl'##########

        ########################
        ##### order_output_by_syntagma_order = False ######
        #######################
        
        ######## rep_type = 'repl'##########

        ### Case 1.1 
        rep_type = 'repl'
        reps = [
                    (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                    (15, 10000, u'[8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u'@sch\xf6nesleben', u'["mention"]', u'#machwasdaraus', u'["hashtag"]', u'#bewegedeinarsch', u'["hashtag"]'), 
                    (17, 11111, u'[5, 12]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'sache', u'["NN"]', u'.', u'["symbol"]', u'die', u'["PDS"]', u'aber', u'["ADV"]'), 
                    (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
                    (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
                ]
        
        inp_syntagma_splitted = [u'klitze', u'kleine']
        scope = 2 
        minimum_columns = False
        #indexes = self.col_index_min if minimum_columns else self.col_index_orig
        order_output_by_syntagma_order = False
        right_output = {
                            8888: {
                                    0: {
                                            0: [u'klitze', (1,)], 
                                            1: [u'kleine', (2, 3)]
                                        }}, 
                            10000: {
                                    0: {
                                            1: [u'klitze', (15,)]}}, 
                            11111: {0: {1: [u'klitze', (17,)]
                                    }}}

        right_length = {8888: [4, 9], 10000: [8], 11111: [5, 12]}

        output_raw,length = stats._reconstruct_syntagma(rep_type, reps,order_output_by_syntagma_order,indexes)
        #p((output_raw,length))
        preparated_output  = {d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in output_raw.iteritems()}
        #p(preparated_output, "preparated_output")
        preparated_output.should.be.equal(right_output)
        length.should.be.equal(right_length)




        ######## rep_type = 'redu'##########
        
        ### Case 1.1 
        rep_type = 'redu'
        reps = [
                    (1, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                    (4, 12222, u'[11]', u'[0, 1]', u'[0, 1]', u'klitze', u'{"klitze": 4}', 4, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u',', u'["symbol"]', u'die', u'["PRELS"]', u'ich', u'["PPER"]'), 
                    (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
                ]
        
        inp_syntagma_splitted = [u'klitze', u'kleine']
        scope = 2 
        minimum_columns = False
        order_output_by_syntagma_order = False
        right_output = {
                            8888: {0: 
                                    {
                                        0: [u'klitze', (1,)], 
                                        1: [u'kleine', (2,)]}}, 
                            12222: {0: 
                                    {
                                        1: [u'klitze', (4,)]}}}

        right_length ={8888: [4, 9], 12222: [11]}

        output_raw,length = stats._reconstruct_syntagma(rep_type, reps, order_output_by_syntagma_order,indexes)
        #p((output_raw,length))
        preparated_output  = {d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in output_raw.iteritems()}
        #p(preparated_output, "preparated_output")
        preparated_output.should.be.equal(right_output)
        length.should.be.equal(right_length)



        # #####################################################################################################################
        


        ########################
        ##### order_output_by_syntagma_order = True ######
        #######################

        ######## rep_type = 'repl'##########

        ### Case 1.1 
        rep_type = 'repl'
        reps = [
                    (u'klitze', 
                        [
                            (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                            (15, 10000, u'[8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u'@sch\xf6nesleben', u'["mention"]', u'#machwasdaraus', u'["hashtag"]', u'#bewegedeinarsch', u'["hashtag"]'), 
                            (17, 11111, u'[5, 12]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'sache', u'["NN"]', u'.', u'["symbol"]', u'die', u'["PDS"]', u'aber', u'["ADV"]')]), 
                    (u'kleine', 
                        [
                            (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
                            (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')])]
        
        inp_syntagma_splitted = [u'klitze', u'kleine']
        scope = 2 
        minimum_columns = False
        order_output_by_syntagma_order = True
        right_output = {
                            8888: 
                                {0: 
                                    {
                                        0: [u'klitze', (1,)], 
                                        1: [u'kleine', (2, 3)]}}, 
                            10000: {0: {
                                        1: [u'klitze', (15,)]}}, 
                            11111: {0: {
                                        1: [u'klitze', (17,)]}}}

        right_length = {8888: [4, 9], 10000: [8], 11111: [5, 12]}

        output_raw,length = stats._reconstruct_syntagma(rep_type, reps, order_output_by_syntagma_order,indexes)
        #p((output_raw,length))
        preparated_output  = {d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in output_raw.iteritems()}
        #p(preparated_output, "preparated_output")
        preparated_output.should.be.equal(right_output)
        length.should.be.equal(right_length)



        ### Case 1.2
        rep_type = 'repl'

        reps = (
                        ('number', 
                            (
                                (20, 11111, u'[5, 12]', u'[1, 6]', u'[1, 6]', u'1', u'1^5', u'1', 5, 0, u'number', u'["neutral", 0.0]', None, u'aber', u'["ADV"]', u'trotzdem', u'["PAV"]', u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 2, u'["number"]', 3, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]'), 
                                (21, 11111, u'[5, 12]', u'[1, 7]', u'[1, 7]', u'2', u'2^4', u'2', 4, 0, u'number', u'["neutral", 0.0]', None, u'trotzdem', u'["PAV"]', u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 3, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None), 
                                (22, 11111, u'[5, 12]', u'[1, 8]', u'[1, 8]', u'3', u'3^5', u'3', 5, 0, u'number', u'["neutral", 0.0]', None, u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None), 
                                (23, 11111, u'[5, 12]', u'[1, 9]', u'[1, 9]', u'4', u'4^4', u'4', 4, 0, u'number', u'["neutral", 0.0]', None, u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None, None, None))), 
                        ('number', 
                            (
                                (21, 11111, u'[5, 12]', u'[1, 7]', u'[1, 7]', u'2', u'2^4', u'2', 4, 0, u'number', u'["neutral", 0.0]', None, u'trotzdem', u'["PAV"]', u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 3, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None), 
                                (22, 11111, u'[5, 12]', u'[1, 8]', u'[1, 8]', u'3', u'3^5', u'3', 5, 0, u'number', u'["neutral", 0.0]', None, u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None), 
                                (23, 11111, u'[5, 12]', u'[1, 9]', u'[1, 9]', u'4', u'4^4', u'4', 4, 0, u'number', u'["neutral", 0.0]', None, u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None, None, None), 
                                (24, 11111, u'[5, 12]', u'[1, 10]', u'[1, 10]', u'5', u'5^5', u'5', 5, 0, u'number', u'["neutral", 0.0]', None, u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 4, u'["number"]', 6, u'["number"]', None, None, None, None, None, None, None, None))), 
                        ('number', 
                            (
                                (22, 11111, u'[5, 12]', u'[1, 8]', u'[1, 8]', u'3', u'3^5', u'3', 5, 0, u'number', u'["neutral", 0.0]', None, u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None), 
                                (23, 11111, u'[5, 12]', u'[1, 9]', u'[1, 9]', u'4', u'4^4', u'4', 4, 0, u'number', u'["neutral", 0.0]', None, u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None, None, None), 
                                (24, 11111, u'[5, 12]', u'[1, 10]', u'[1, 10]', u'5', u'5^5', u'5', 5, 0, u'number', u'["neutral", 0.0]', None, u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 4, u'["number"]', 6, u'["number"]', None, None, None, None, None, None, None, None))))



        
        scope = 3 
        minimum_columns = False
        order_output_by_syntagma_order = True
        right_output = {
                            11111: {
                                        1: {
                                                8: [u'number', (22, 22, 22)], 
                                                9: [u'number', (23, 23, 23)], 
                                                10: [u'number', (24, 24)], 
                                                6: [u'number', (20,)], 
                                                7: [u'number', (21, 21)]
                                                }}}


        right_length = {11111: [5, 12]}

        output_raw,length = stats._reconstruct_syntagma(rep_type, reps, order_output_by_syntagma_order,indexes,syntagma_type="pos")
        #p((output_raw,length))
        preparated_output  = {d:{s:{t:ids for t, ids in s_data.iteritems()} for s, s_data in doc_data.iteritems()} for d, doc_data in output_raw.iteritems()}
        #p(preparated_output, "preparated_output")
        preparated_output.should.be.equal(right_output)
        length.should.be.equal(right_length)








    @attr(status='stable')
    #@wipd
    def test_exctract_full_syntagmas_631(self):
        stats = Stats(mode=self.mode)


        ########################
        ##### scope = 1 ######
        #######################


        #####################
        ## scope = 1 ######
        ###################

        ### Case 1.1 
        inp_syntagma_splitted = ("klitze",)
        redu_free_elem_length = { 10000:[5,1,1], 11111:[2,5,6]}
        scope = 1
        reconstructed_syntagmas = {
                                    11111:{
                                            0:{
                                                1:["klitze",(18,)],
                                               },
                                            1:{
                                                1:["klitze",(20,)],
                                                2:["kleine",(22,)],
                                               },
                                            2:{
                                                0:["klitze",(29,)],
                                                2:["klitze",(26,)],
                                                4:["klitze",(27,)],
                                               }
                                           }
                                  }


        right_full_syntagmas = (((0, 1),), ((1, 1),), ((2, 0),), ((2, 2),), ((2, 4),))
        right_allow_ids = (18, 27, 20, 26, 29)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        #p(set([ True if len(syn)== scope else False for syn in  full_syntagmas ,),)
        assert False not in set([ True if len(syn)>= scope else False for syn in  full_syntagmas ])



        ########################
        ##### scope = 2 ######
        ########################


        ### Case 2.0
        inp_syntagma_splitted = ("klitze","kleine")
        redu_free_elem_length = { 10000:[5,1,1], 11111:[2,5,4]}
        scope = 2
        reconstructed_syntagmas = {
                                    11111:{
                                            0:{
                                                1:["klitze",(18,)],
                                                2:["kleine",(19,)],
                                               },

                                           }
                                  }


        right_full_syntagmas = (((0, 1), (0, 2)),)
        right_allow_ids = (18, 19)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p(full_syntagmas, allow_ids)
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        #p(set([ True if len(syn)== scope else False for syn in  full_syntagmas ,),)
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])




        ### Case 2.1 
        inp_syntagma_splitted = ("klitze","kleine")
        redu_free_elem_length = { 10000:[5,1,1], 11111:[2,5,4]}
        scope = 2
        reconstructed_syntagmas = {
                                    11111:{
                                            0:{
                                                1:["klitze",(18,)],
                                                2:["kleine",(19,)],
                                               },
                                            1:{
                                                1:["klitze",(20,)],
                                                2:["kleine",(22,)],
                                               }
                                           }
                                  }


        right_full_syntagmas = (((0, 1), (0, 2)), ((1, 1), (1, 2)))
        right_allow_ids = (18, 19, 20, 22)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)

        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        #p(set([ True if len(syn)== scope else False for syn in  full_syntagmas ,),)
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])




        ### Case 2.2
        inp_syntagma_splitted = ("klitze","kleine")
        redu_free_elem_length = {  11111:[2,5,4]}
        scope = 2
        reconstructed_syntagmas = {
                                    11111:{
                                            0:{
                                                1:["klitze",(18,)],
                                                2:["kleine",(19,)],
                                               },
                                            1:{
                                                1:["klitze",(20,)],
                                                4:["klitze",(22,)],
                                               },
                                            2:{
                                                0:["kleine",(24,554,)],
                                                2:["kleine",(29,56,)],
                                               }
                                           }
                                  }


        right_full_syntagmas = (((0, 1), (0, 2)), ((1, 4), (2, 0)))
        right_allow_ids = (18, 19, 22, 24, 554)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        #p(set([ True if len(syn)== scope else False for syn in  full_syntagmas ,),)
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])




        ### Case 2.3
        
        # inp_syntagma_splitted  = [u'klitze', u'kleine']

        # _rep  = [
        #             (u'klitze', 
        #                 [
        #                     (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
        #                     (15, 10000, u'[8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u'@sch\xf6nesleben', u'["mention"]', u'#machwasdaraus', u'["hashtag"]', u'#bewegedeinarsch', u'["hashtag"]'), 
        #                     (17, 11111, u'[5, 12]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'sache', u'["NN"]', u'.', u'["symbol"]', u'die', u'["PDS"]', u'aber', u'["ADV"]'),), 
        #             (u'kleine', 
        #                 [
        #                     (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
        #                     (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
        #                     ,)]
        inp_syntagma_splitted  = [u'klitze', u'kleine']
        redu_free_elem_length = {8888: [4, 9], 10000: [8], 11111: [5, 12]}
        scope = 2
        reconstructed_syntagmas = {
                                    8888: {0: {
                                                0:["klitze",(1,)], 
                                                1:["kleine",(2, 3,)]
                                               }
                                           }, 
                                    10000: {0: {
                                                1:["klitze",(15,)]
                                                }
                                            }, 
                                    11111: {0: {
                                                1:["klitze",(17,)]
                                                }
                                            }
                                    }


        right_full_syntagmas = (((0, 0), (0, 1)),)
        right_allow_ids = (1, 2, 3)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        #p(set([ True if len(syn)== scope else False for syn in  full_syntagmas ,),)
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])





        ### Case 2.4
        #
        # inp_syntagma_splitted  = [u'klitze', u'kleine']

        # _rep  = [
        #             (u'klitze', 
        #                 [
        #                     (1, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
        #                     (4, 12222, u'[11]', u'[0, 1]', u'[0, 1]', u'klitze', u'{"klitze": 4}', 4, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u',', u'["symbol"]', u'die', u'["PRELS"]', u'ich', u'["PPER"]'),), 
        #             (u'kleine', 
        #                 [
        #                     (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
        #                     ,)]
        inp_syntagma_splitted  = [u'klitze', u'kleine']
        redu_free_elem_length = {8888: [4, 9], 12222: [11]}
        scope = 2
        reconstructed_syntagmas = {
                                    8888: {0: {
                                                0:["klitze",(1,)], 
                                                1:["kleine",(2,)]
                                                }
                                          }, 
                                    12222: {0: {
                                                1:["klitze",(4,)]
                                                }
                                            }
                                  }


        right_full_syntagmas = (((0, 0), (0, 1)),)
        right_allow_ids = (1, 2)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        #p(set([ True if len(syn)== scope else False for syn in  full_syntagmas ,),)
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])





        ### Case 2.5
        # inp_syntagma_splitted  = [u'klitze', u'kleine']

        # _rep  = [
        #             (u'klitze', 
        #                 [
        #                     (1, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
        #                     (4, 12222, u'[11]', u'[0, 1]', u'[0, 1]', u'klitze', u'{"klitze": 4}', 4, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u',', u'["symbol"]', u'die', u'["PRELS"]', u'ich', u'["PPER"]'),), 
        #             (u'kleine', 
        #                 [
        #                     (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
        #                     ,)]
        inp_syntagma_splitted  = [u'klitze', u'kleine']
        redu_free_elem_length = {8888: [4, 9], 12222: [11]}
        scope = 2
        reconstructed_syntagmas = {
                                    8888: {0: {
                                                0:["klitze",(1,)], 
                                                1:["kleine",(2,)],
                                                2:["klitze",(2,)], 
                                                3:["kleine",(3,)],
                                                }
                                          }, 
                                    12222: {0: {
                                                1:["klitze",(4,)]
                                                }
                                            }
                                  }


        right_full_syntagmas = (((0, 0), (0, 1)), ((0, 2), (0, 3)))
        right_allow_ids = (1, 2, 3)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        #p(set([ True if len(syn)== scope else False for syn in  full_syntagmas ,),)
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])





        ########################
        ##### scope = 3 ######
        ########################

        ### Case 3.1
        inp_syntagma_splitted = ("klitze","kleine","iii")
        redu_free_elem_length = {8888:[2, 3], 10000:[3,4], 11111:[2,5,4]}
        scope = 3
        reconstructed_syntagmas = {
                                    8888:{
                                            0:{
                                                0:["klitze",(1,)], 
                                                1:["kleine",(2, 3,)]
                                               }, 
                                            1:{
                                                0:["iii",(10,)]
                                               }, 
                                          },
                                    10000:{
                                            0: {
                                                1:["kleine",(15,)]
                                                }
                                           }, 
                                    11111:{
                                            0:{
                                                1:["kleine",(17,)]
                                               }
                                           }
                                  }
#
        right_full_syntagmas = (((0, 0), (0, 1), (1, 0)),)
        right_allow_ids = (1, 2, 3, 10)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])

        


        ########################
        ##### scope = 3 ######
        ########################

        ### Case 3.2
        inp_syntagma_splitted = ("klitze","kleine","iii")
        redu_free_elem_length = {8888:[4, 5], 10000:[5,1,1], 11111:[2,5,4]}
        scope = 3
        reconstructed_syntagmas = {
                                    8888:{
                                            0:{
                                                0:["klitze",(1,)], 
                                                1:["kleine",(2, 3,)],
                                                2:["iii",(4, 5,)],
                                               }, 
                                            1:{
                                                1:["klitze",(10,)],
                                                2:["kleine",(11,)],
                                                3:["i",(12,)],
                                               }, 
                                          },
                                  }
#
        right_full_syntagmas = (((0, 0), (0, 1), (0, 2)), ((1, 1), (1, 2), (1, 3)))
        right_allow_ids = (1, 2, 3, 4, 5, 10, 11, 12)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])





        ########################
        ##### scope = 3 ######
        ########################

        ### Case 3.3
        inp_syntagma_splitted = ("klitze","kleine","iii")
        redu_free_elem_length = { 10000:[5,1,1], 11111:[2,5,4]}
        scope = 3
        reconstructed_syntagmas = {
                                    10000:{
                                            0: {
                                                4:["klitze",(15,)],
                                                },
                                            1: {
                                                0:["kleine",(16,)],
                                                },
                                            2: {
                                                0:["iii",(17,)],
                                                },
                                           }
                                  }


        right_full_syntagmas = (((0, 4), (1, 0), (2, 0)),)
        right_allow_ids = (15, 16, 17)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)

        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])





        ########################
        ##### scope = 6 ######
        ########################

        ### Case 6.1
        inp_syntagma_splitted = ("klitze","kleine","iii",",","oder","wie")
        redu_free_elem_length = { 10000:[5,2,2,1], 11111:[2,5,4]}
        scope = 6
        reconstructed_syntagmas = {
                                    10000:{
                                            0: {
                                                4:["klitze",(15,)],
                                                },
                                            1: {
                                                0:["kleine",(16,)],
                                                1:["iii",(19,)],
                                                },
                                            2: {
                                                0:[",",(17,)],
                                                1:["oder",(34,)],
                                                },
                                            3: {
                                                0:["wie",(17,)],
                                                },
                                           }
                                  }


        right_full_syntagmas = (((0, 4), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0)),)
        right_allow_ids = (15, 16, 19, 17, 34, 17)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])


        ### Case 6.2
        inp_syntagma_splitted = ("klitze","kleine","iii",",","oder","wie")
        redu_free_elem_length = { 10000:[10,3,4,5], 11111:[7,4,2,1]}
        scope = 6
        reconstructed_syntagmas = {
                                    10000:{
                                            0: {
                                                0:["klitze",(15,)],
                                                1:["kleine",(16,)],
                                                2:["iii",(17,)],
                                                3:[",",(18,)],
                                                4:["oder",(19,)],
                                                5:["wie",(20,)],
                                                },
                                            1: {
                                                0:["klitze",(164,)],
                                                1:["kleine",(193,)],
                                                },
                                            2: {
                                                0:["klitze",(172,)],
                                                1:["kleine",(343,)],
                                                },
                                           },
                                    11111:{
                                            0: {
                                                4:["klitze",(23,)],
                                                5:["kleine",(25,)],
                                                6:["iii",(64,)],
                                                },
                                            1: {
                                                0:[",",(152,)],
                                                1:["oder",(114,)],
                                                2:["wie",(1,)],
                                                },
                                            2: {
                                                0:["klitze",(147,)],
                                                1:["kleine",(344,)],
                                                },
                                            3: {
                                                0:["iii",(178,)],
                                                },
                                           }
                                  }


        right_full_syntagmas = (((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)), ((0, 4), (0, 5), (0, 6), (1, 0), (1, 1), (1, 2)))
        right_allow_ids = (15, 16, 17, 18, 19, 20, 23, 25, 64, 152, 114, 1)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])




        # ### Case 6.3
        inp_syntagma_splitted = ("klitze","kleine","iii",",","oder","wie")
        redu_free_elem_length = { 10000:[10,10,10,10], 11111:[7,4,2,1]}
        scope = 6
        reconstructed_syntagmas = {
                                    10000:{
                                            0: {
                                                2:["klitze",(15,)],
                                                3:["kleine",(16,)],
                                                4:["iii",(17,)],
                                                6:[",",(18,)],
                                                7:["oder",(19,)],
                                                8:["wie",(20,)],
                                                },
                                            2: {
                                                4:["klitze",(152,)],
                                                5:["kleine",(163,)],
                                                6:["iii",(174,)],
                                                7:[",",(185,)],
                                                8:["oder",(196,)],
                                                9:["wie",(207,)],
                                                },
                                            3: {
                                                1:["klitze",(150,)],
                                                2:["kleine",(160,)],
                                                3:["iii",(170,)],
                                                4:[",",(180,)],
                                                5:["oder",(190,)],
                                                6:["wie",(200,)],
                                                },
                                           },
                                  }


        right_full_syntagmas = (((2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9)), ((3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)))
        right_allow_ids = (160, 163, 196, 200, 170, 174, 207, 180, 150, 152, 185, 190)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)== scope else False for syn in  full_syntagmas ])




        ###############################
        ##############################
        ### mixes scope ############


        ### Case __.1
        syntagma_type = "pos"
        inp_syntagma_splitted = [u'number', u'number', u'number']
        redu_free_elem_length = {11111: [5, 6, 14]}
        scope = 3
        reconstructed_syntagmas = {
                                    11111: {
                                                2: {
                                                        8: [u'number', (33,)], 
                                                        9: [u'number', (34, 34)], 
                                                        10: [u'number', (35, 35, 35)], 
                                                        11: [u'number', (36, 36, 36)], 
                                                        12: [u'number', (37, 37)]
                                                    }
                                            }
                                   }



        right_full_syntagmas = (((2, 8), (2, 9), (2, 10)),)
        right_allow_ids = (33, 34, 35)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted,syntagma_type=syntagma_type)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)>= scope else False for syn in  full_syntagmas ])


        ### Case __.2
        syntagma_type = "pos"
        inp_syntagma_splitted = ("NN","NP","NN")
        redu_free_elem_length = {11111: [5, 12]}
        scope = 3
        reconstructed_syntagmas = {
                                        11111: {
                                                    1: {
                                                            6: ["NN",(22, 22, 22)], 
                                                            7: ["NP",(23, 23, 23)], 
                                                            8: ["NN",(24, 24)], 
                                                            9: ["NN",(221, 221, 221)], 
                                                            10: ["NP",(232, 233, 236)], 
                                                            11: ["NN",(240, 248)], 
                                                        }
                                                }
                                    }


        right_full_syntagmas = (((1, 6), (1, 7), (1, 8)), ((1, 9), (1, 10), (1, 11)))
        right_allow_ids = (232, 233, 236, 240, 24, 22, 23, 248, 221)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted,syntagma_type=syntagma_type)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)>= scope else False for syn in  full_syntagmas ])




        ### Case __.3
        syntagma_type = "pos"
        inp_syntagma_splitted = ("NN","NP","NN","NP")
        redu_free_elem_length = {11111: [5, 12]}
        scope = 4
        reconstructed_syntagmas = {
                                        11111: {
                                                    1: {
                                                            6: ["NN",(22, 22, 22)], 
                                                            7: ["NP",(23, 23, 23)], 
                                                            8: ["NN",(24, 24)], 
                                                            9: ["NP",(221, 221, 221)], 
                                                            10: ["NN",(232, 233, 236)], 
                                                            11: ["NP",(240, 248)], 
                                                        }
                                                }
                                    }


        right_full_syntagmas = (((1, 6), (1, 7), (1, 8), (1, 9)),)
        right_allow_ids = (24, 221, 22, 23)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted,syntagma_type=syntagma_type)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)>= scope else False for syn in  full_syntagmas ])



        ### Case __.4
        syntagma_type = "lexem"
        inp_syntagma_splitted = ("klitze","kleine", "klitze")
        redu_free_elem_length = {11111: [5, 15]}
        scope = 3
        reconstructed_syntagmas = {
                                        11111: {
                                                    1: {
                                                            6: ["klitze",(22, 22, 22)], 
                                                            7: ["kleine",(23, 23, 23)], 
                                                            8: ["klitze",(24, 24)], 
                                                            9: ["klitze",(22, 22, 22)], 
                                                            10: ["kleine",(23, 23, 23)], 
                                                            11: ["klitze",(24, 24)],  
                                                        }
                                                }
                                    }


        right_full_syntagmas = (((1, 6), (1, 7), (1, 8)), ((1, 9), (1, 10), (1, 11)))
        right_allow_ids = (24, 22, 23)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted,syntagma_type=syntagma_type)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)>= scope else False for syn in  full_syntagmas ])


        ### Case __.4
        syntagma_type = "lexem"
        inp_syntagma_splitted = ("klitze","kleine", "klitze", "kleine")
        redu_free_elem_length = {11111: [5, 15]}
        scope = 4
        reconstructed_syntagmas = {
                                        11111: {
                                                    1: {
                                                            6: ["klitze",(22, 22, 22)], 
                                                            7: ["kleine",(23, 23, 23)], 
                                                            8: ["klitze",(22, 22, 22)], 
                                                            9: ["kleine",(23, 23, 23)],
                                                            10: ["klitze",(22, 22, 22)], 
                                                            11: ["kleine",(23, 23, 23)], 
                                                        }
                                                }
                                    }


        right_full_syntagmas = (((1, 6), (1, 7), (1, 8), (1, 9)),)
        right_allow_ids = (22, 23)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted,syntagma_type=syntagma_type)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)>= scope else False for syn in  full_syntagmas ])


        ### Case __.5
        syntagma_type = "lexem"
        inp_syntagma_splitted = ("klitze","kleine",)
        redu_free_elem_length = {11111: [5, 15]}
        scope = 2
        reconstructed_syntagmas = {
                                        11111: {
                                                    1: {
                                                            6: ["klitze",(22, 22, 22)], 
                                                            7: ["kleine",(23, 23, 23)], 
                                                            8: ["klitze",(22, 22, 22)], 
                                                            9: ["kleine",(23, 23, 23)],
                                                            10: ["klitze",(22, 22, 22)], 
                                                            11: ["kleine",(23, 23, 23)], 
                                                        }
                                                }
                                    }


        right_full_syntagmas = (((1, 6), (1, 7)), ((1, 8), (1, 9)), ((1, 10), (1, 11)))
        right_allow_ids = (22, 23)

        full_syntagmas, allow_ids = stats._exctract_full_syntagmas(reconstructed_syntagmas, scope,redu_free_elem_length,inp_syntagma_splitted,syntagma_type=syntagma_type)
        #p((full_syntagmas, allow_ids))
        full_syntagmas.should.be.equal(right_full_syntagmas)
        set(allow_ids).should.be.equal(set(right_allow_ids))
        assert False not in set([ True if len(syn)>= scope else False for syn in  full_syntagmas ])












    @attr(status='stable')
    #@wipd
    def test_filter_full_rep_syn_632(self):
        stats = Stats(mode=self.mode)

        #############################################################
        ####### order_output_by_syntagma_order = True ####
        ###############################################################

        #####rep_type = 'repl'######

        ### Case 1.1 
        rep_type = 'repl'
        _rep = (
                    (u'klitze', 
                        (
                            (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                            (15, 10000, u'[8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u'@sch\xf6nesleben', u'["mention"]', u'#machwasdaraus', u'["hashtag"]', u'#bewegedeinarsch', u'["hashtag"]'), 
                            (17, 11111, u'[5, 12]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'sache', u'["NN"]', u'.', u'["symbol"]', u'die', u'["PDS"]', u'aber', u'["ADV"]'))), 
                    (u'kleine', 
                        (
                            (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
                            (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
                            )))
        
        allowed_ids = set((1, 2, 3))

        order_output_by_syntagma_order = True

        right_filtered_reps = (
                                (u'klitze', 
                                    (
                                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),)), 
                                (u'kleine', 
                                    (
                                        (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
                                        (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
                                        )))


        filtered_reps = stats._filter_full_rep_syn(rep_type,_rep, allowed_ids,order_output_by_syntagma_order, 0)
        #p((filtered_reps))
        tuple(filtered_reps).should.be.equal(tuple(right_filtered_reps))





        #####rep_type = 'redu'######

        ### Case 2.1 
        rep_type = 'redu'
        _rep = (
                (u'klitze', 
                    (
                        (1, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                        (4, 12222, u'[11]', u'[0, 1]', u'[0, 1]', u'klitze', u'{"klitze": 4}', 4, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u',', u'["symbol"]', u'die', u'["PRELS"]', u'ich', u'["PPER"]'))), 
                (u'kleine', 
                    (
                        (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'),
                        )))
        
        allowed_ids = set((1, 2))

        order_output_by_syntagma_order = True

        right_filtered_reps = (
                                (u'klitze', 
                                    (
                                        (1, 8888, u'[4, 9]', u'[0, 0]', u'[0, 0]', u'klitze', u'{"klitze": 1, "kli^4tze": 1}', 2, u'NN', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),)), 
                                (u'kleine', 
                                    (
                                        (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'{"kle^5ine": 1, "klein^3e": 1}', 2, u'NE', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'),
                                        )))

        filtered_reps = stats._filter_full_rep_syn(rep_type,_rep, allowed_ids,order_output_by_syntagma_order, 0)
        #p((filtered_reps))
        tuple(filtered_reps).should.be.equal(tuple(right_filtered_reps))






        # ########################################################################################################################
        # ########################################################################################################################
        # ########################################################################################################################




        # #############################################################
        # ####### order_output_by_syntagma_order = False ####
        # ############################################################



        # #####rep_type = 'redu'######

        ### Case 1.1 
        rep_type = 'redu'
        _rep = (
                    (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                    (15, 10000, u'[8]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'\xfcberaschung', u'["NN"]', u'@sch\xf6nesleben', u'["mention"]', u'#machwasdaraus', u'["hashtag"]', u'#bewegedeinarsch', u'["hashtag"]'), 
                    (17, 11111, u'[5, 12]', u'[0, 1]', u'[0, 1]', u'klitze', u'klitze^4', u'e', 4, 5, u'VAPPER', u'["neutral", 0.0]', None, None, None, None, None, None, None, None, None, u'eine', u'["ART"]', u'kleine', u'["ADJA"]', u'sache', u'["NN"]', u'.', u'["symbol"]', u'die', u'["PDS"]', u'aber', u'["ADV"]'), 
                    (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
                    (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
                )
        
        allowed_ids = set((1, 2))

        order_output_by_syntagma_order = False

        right_filtered_reps = (
                                (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                                (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
                              )

        filtered_reps = stats._filter_full_rep_syn(rep_type,_rep, allowed_ids,order_output_by_syntagma_order, 0)
        #p((filtered_reps))
        tuple(filtered_reps).should.be.equal(tuple(right_filtered_reps))







    @attr(status='stable')
    #@wipd 
    def test_delete_dublicats_in_reps_633(self):
        stats = Stats(mode=self.mode)

        #############################################################
        ####### order_output_by_syntagma_order = True ####
        ###############################################################

        ### Case 1.1 
        order_output_by_syntagma_order = True
        _rep = (
                (u'klitze', 
                    (
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),

                        )), 

                (u'kleine', 
                    (
                        (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
                        (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'),
                        (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
                        )))

        right_dublicates_free = (
                                    (u'klitze', 
                                        (
                                            (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                                            )), 
                                    (u'kleine', 
                                        (
                                            (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
                                            (3, 8888, u'[4, 9]', u'[0, 3]', u'[0, 1]', u'kleine', u'klein^3e', u'n', 3, 4, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]')
                                            )))

        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        #p((dublicats_free))
        tuple(right_dublicates_free).should.be.equal(tuple(dublicats_free))




        ### Case 1.2
        stats._full_repetativ_syntagma = True
        order_output_by_syntagma_order = True
        _rep = (
                (u'klitze', 
                    (
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),

                        )), 

                (u'kleine', 
                    (
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        )))

        right_dublicates_free = ()

        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        #p((dublicats_free))
        tuple(right_dublicates_free).should.be.equal(tuple(dublicats_free))







        ### Case 1.3
        stats._full_repetativ_syntagma = False
        order_output_by_syntagma_order = True
        _rep = (
                (u'klitze', 
                    (
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),

                        )), 

                (u'kleine', 
                    (
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                        )))

        right_dublicates_free = (
                                    (u'klitze', ()), 
                                    (u'kleine', 
                                        (
                                            (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                                            )))

        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        #p((dublicats_free))
        tuple(right_dublicates_free).should.be.equal(tuple(dublicats_free))




        ### Case 1.4
        stats._full_repetativ_syntagma = True
        order_output_by_syntagma_order = True
        _rep = (
                        ('number', 
                            (
                                (20, 11111, u'[5, 12]', u'[1, 6]', u'[1, 6]', u'1', u'1^5', u'1', 5, 0, u'number', u'["neutral", 0.0]', None, u'aber', u'["ADV"]', u'trotzdem', u'["PAV"]', u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 2, u'["number"]', 3, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]'), 
                                (21, 11111, u'[5, 12]', u'[1, 7]', u'[1, 7]', u'2', u'2^4', u'2', 4, 0, u'number', u'["neutral", 0.0]', None, u'trotzdem', u'["PAV"]', u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 3, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None), 
                                (22, 11111, u'[5, 12]', u'[1, 8]', u'[1, 8]', u'3', u'3^5', u'3', 5, 0, u'number', u'["neutral", 0.0]', None, u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None), 
                                (23, 11111, u'[5, 12]', u'[1, 9]', u'[1, 9]', u'4', u'4^4', u'4', 4, 0, u'number', u'["neutral", 0.0]', None, u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None, None, None))), 
                        ('number', 
                            (
                                (21, 11111, u'[5, 12]', u'[1, 7]', u'[1, 7]', u'2', u'2^4', u'2', 4, 0, u'number', u'["neutral", 0.0]', None, u'trotzdem', u'["PAV"]', u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 3, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None), 
                                (22, 11111, u'[5, 12]', u'[1, 8]', u'[1, 8]', u'3', u'3^5', u'3', 5, 0, u'number', u'["neutral", 0.0]', None, u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None), 
                                (23, 11111, u'[5, 12]', u'[1, 9]', u'[1, 9]', u'4', u'4^4', u'4', 4, 0, u'number', u'["neutral", 0.0]', None, u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None, None, None), 
                                (24, 11111, u'[5, 12]', u'[1, 10]', u'[1, 10]', u'5', u'5^5', u'5', 5, 0, u'number', u'["neutral", 0.0]', None, u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 4, u'["number"]', 6, u'["number"]', None, None, None, None, None, None, None, None))), 
                        ('number', 
                            (
                                (22, 11111, u'[5, 12]', u'[1, 8]', u'[1, 8]', u'3', u'3^5', u'3', 5, 0, u'number', u'["neutral", 0.0]', None, u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None), 
                                (23, 11111, u'[5, 12]', u'[1, 9]', u'[1, 9]', u'4', u'4^4', u'4', 4, 0, u'number', u'["neutral", 0.0]', None, u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None, None, None), 
                                (24, 11111, u'[5, 12]', u'[1, 10]', u'[1, 10]', u'5', u'5^5', u'5', 5, 0, u'number', u'["neutral", 0.0]', None, u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 4, u'["number"]', 6, u'["number"]', None, None, None, None, None, None, None, None))))


        right_dublicates_free = (
                                    ('number', 
                                        (
                                            (20, 11111, u'[5, 12]', u'[1, 6]', u'[1, 6]', u'1', u'1^5', u'1', 5, 0, u'number', u'["neutral", 0.0]', None, u'aber', u'["ADV"]', u'trotzdem', u'["PAV"]', u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 2, u'["number"]', 3, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]'),)), 
                                    ('number', 
                                        (
                                            (21, 11111, u'[5, 12]', u'[1, 7]', u'[1, 7]', u'2', u'2^4', u'2', 4, 0, u'number', u'["neutral", 0.0]', None, u'trotzdem', u'["PAV"]', u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 3, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None),)), 
                                    ('number', 
                                        (
                                            (22, 11111, u'[5, 12]', u'[1, 8]', u'[1, 8]', u'3', u'3^5', u'3', 5, 0, u'number', u'["neutral", 0.0]', None, u'wichtig', u'["ADJA"]', u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 4, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None), 
                                            (23, 11111, u'[5, 12]', u'[1, 9]', u'[1, 9]', u'4', u'4^4', u'4', 4, 0, u'number', u'["neutral", 0.0]', None, u'ist', u'["NN"]', u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 5, u'["number"]', 6, u'["number"]', None, None, None, None, None, None), 
                                            (24, 11111, u'[5, 12]', u'[1, 10]', u'[1, 10]', u'5', u'5^5', u'5', 5, 0, u'number', u'["neutral", 0.0]', None, u'!', u'["symbol"]', 1, u'["number"]', 2, u'["number"]', 3, u'["number"]', 4, u'["number"]', 6, u'["number"]', None, None, None, None, None, None, None, None)
                                            )))

        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
        #p((dublicats_free))
        tuple(right_dublicates_free).should.be.equal(tuple(dublicats_free))





        # #############################################################
        # ####### order_output_by_syntagma_order = False ####
        # ############################################################



        # #####rep_type = 'redu'######

        ### Case 2.1 
        order_output_by_syntagma_order = False
        _rep = (
                    (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                    (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'),
                    (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'),
                    (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'),
                    (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'),
                    (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'), 
                )

        right_dublicates_free = (
                                    (1, 8888, u'[4, 9]', u'[0, 1]', u'[0, 0]', u'klitze', u'kli^4tze', u'i', 4, 2, u'NN', u'["neutral", 0.0]', u'[0, 0]', None, None, None, None, None, None, None, None, None, None, u'kleine', u'["NE", {"kle^5ine": 1, "klein^3e": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]'),
                                    (2, 8888, u'[4, 9]', u'[0, 2]', u'[0, 1]', u'kleine', u'kle^5ine', u'e', 5, 2, u'NE', u'["neutral", 0.0]', u'[0, 2]', None, None, None, None, None, None, None, None, u'klitze', u'["NN", {"klitze": 1, "kli^4tze": 1}]', u'\xfcberaschung', u'["NN"]', u'.', u'["symbol"]', u'trotzdem', u'["PAV"]', u'hat', u'["VAFIN"]', u'sie', u'["PPER"]'), 
                                )
        
        dublicats_free = stats._delete_dublicats_in_reps(_rep, order_output_by_syntagma_order, 0)
         
        #p((dublicats_free))
        tuple(dublicats_free).should.be.equal(tuple(right_dublicates_free))









    def get_dict_rows_from_csv(self,fname):
         with open(fname+".csv") as csvfile:
             readCSV = csv.reader(csvfile, delimiter=';')
             #print readCSV
             columns =  readCSV.next()
             for row in readCSV:
                 if row[0]:
                     #print(row)
                     yield {k:v for k,v in zip(columns, row)  if k}


    def get_list_rows_from_csv(self,fname):
         with open(fname+".csv") as csvfile:
             readCSV = csv.reader(csvfile, delimiter=';')
             #print readCSV
             columns =  readCSV.next()
             for row in readCSV:
                 if row[0]:
                     #print(row)
                     yield row



    ####### 700 #######


    @attr(status='stable')
    #@wipd
    def test_compute_rep_sum_700(self):
        self.prj_folder()
        #self.blogger_corpus()
        self.test_dbs()
        stats = Stats(mode=self.mode,use_cash=True)#, )
        stats.open(os.path.join(self.tempdir_testdbs,self.db_blogger_plaintext_stats_de))
        
        ################################################
        #### "repl" ####
        ################################################
        ## Case 1.1
        summery = stats.compute_rep_sum("*", "repl")
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'a': {3: [1, {u'\xfcbe^4r^5a^3schun^6g^3': 1}], 4: [1, {u'ka^4n^5': 1}], 6: [1, {u'ta^6g^6': 1}]}, u'z': {3: [1, {u'kli^4tz^3': 1}]}, u'e': {8: [2, {u'kle^4i^5n^4e^8': 1, u'ble^8ibt': 1}], 3: [4, {u'kle^3i^3n^3': 1, u'klein^4e^3s^4': 2, u'kleine^3r^2e^5': 1}], 4: [10, {u'\xfcbe^4r^5a^3schun^6g^3': 1, u'ble^4ibt': 1, u'kle^4i^5n^4e^8': 1, u'kle^4i^5n^3e^2s^3': 2, u'eine^4': 1, u'kleine^4s^7': 2, u'klitze^4': 2}], 5: [6, {u'kle^5ine': 1, u'kleinere^5': 1, u'kle^5in^5e': 1, u'kle^5i^2n^4e^5': 2, u'kleine^3r^2e^5': 1}], 7: [1, {u'kli^4tze^7': 1}]}, u'g': {3: [1, {u'\xfcbe^4r^5a^3schun^6g^3': 1}], 6: [1, {u'ta^6g^6': 1}]}, u'4': {4: [1, {u'4^4': 1}]}, u')': {3: [3, {u'-)^3': 3}], 4: [1, {u':-)^4': 1}]}, u'h': {3: [1, {u'auswah^3l^4': 1}]}, u'l': {4: [1, {u'auswah^3l^4': 1}]}, u'n': {3: [5, {u'kle^4i^5n^3e^2s^3': 2, u'kle^3i^3n^3': 1, u'klein^3e^2s': 1, u'klein^3e': 1}], 4: [4, {u'kle^4i^5n^4e^8': 1, u'klein^4e^3s^4': 2, u'kle^5i^2n^4e^5': 1}], 5: [5, {u'klein^5': 1, u'ka^4n^5': 1, u'kle^5in^5e': 1, u'm\xe4dchen^5': 2}], 6: [2, {u'\xfcbe^4r^5a^3schun^6g^3': 1, u'kan^6': 1}]}, u'1': {8: [1, {u'1^8': 1}], 5: [1, {u'1^5': 1}], 6: [1, {u'1^6': 1}]}, u'i': {8: [1, {u'wichti^8g': 1}], 3: [2, {u'kle^3i^3n^3': 1, u'kli^3tzes^3': 1}], 4: [3, {u'kli^4tz': 1, u'kli^4tze^7': 1, u'kli^4tz^3': 1}], 5: [4, {u'kle^4i^5n^3e^2s^3': 2, u'kle^4i^5n^4e^8': 1, u'geni^5es^8t^5': 1}]}, u'3': {5: [1, {u'3^5': 1}]}, u'r': {4: [2, {u'\xfcber^4aschung': 2}], 5: [2, {u'\xfcbe^4r^5a^3schun^6g^3': 1, u'\xfcber^5aschung': 1}]}, u'5': {5: [1, {u'5^5': 1}]}, u'\U0001f600': {5: [1, {u'\U0001f600^5': 1}]}, u'2': {4: [1, {u'2^4': 1}]}, u's': {8: [1, {u'geni^5es^8t^5': 1}], 3: [3, {u'kle^4i^5n^3e^2s^3': 2, u'kli^3tzes^3': 1}], 4: [5, {u'kleines^4': 1, u'klitzes^4': 1, u'genies^4t^2': 1, u'klein^4e^3s^4': 2}], 6: [1, {u'is^6t': 1}], 7: [2, {u'kleine^4s^7': 2}]}, u'.': {5: [2, {u'.^5': 2}]}, u'u': {12: [1, {u'hu^12ngrig': 1}]}, u'\U0001f62b': {4: [1, {u'\U0001f62b^4': 1}]}, u't': {5: [1, {u'geni^5es^8t^5': 1}]}}
        summery.should.be.equal(right_summery)
        # i=0
        # for letter, letter_data in summery.iteritems():
        #     for rep_num, rep_num_data in letter_data.iteritems():
        #         i+=1
        #         #print repr(letter), rep_num,rep_num_data
        #         print i, letter,rep_num, rep_num_data
        # print "\n\n\n"


        #### "repl" ####
        ## Case 1.2
        summery = stats.compute_rep_sum("*", "repl", ignore_num=True, ignore_symbol=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'a': {3: [1, {u'\xfcbe^4r^5a^3schun^6g^3': 1}], 4: [1, {u'ka^4n^5': 1}], 6: [1, {u'ta^6g^6': 1}]}, u'e': {8: [2, {u'kle^4i^5n^4e^8': 1, u'ble^8ibt': 1}], 3: [4, {u'kle^3i^3n^3': 1, u'klein^4e^3s^4': 2, u'kleine^3r^2e^5': 1}], 4: [10, {u'\xfcbe^4r^5a^3schun^6g^3': 1, u'ble^4ibt': 1, u'kle^4i^5n^4e^8': 1, u'kle^4i^5n^3e^2s^3': 2, u'eine^4': 1, u'kleine^4s^7': 2, u'klitze^4': 2}], 5: [6, {u'kle^5ine': 1, u'kleinere^5': 1, u'kle^5in^5e': 1, u'kle^5i^2n^4e^5': 2, u'kleine^3r^2e^5': 1}], 7: [1, {u'kli^4tze^7': 1}]}, u'g': {3: [1, {u'\xfcbe^4r^5a^3schun^6g^3': 1}], 6: [1, {u'ta^6g^6': 1}]}, u'i': {8: [1, {u'wichti^8g': 1}], 3: [2, {u'kle^3i^3n^3': 1, u'kli^3tzes^3': 1}], 4: [3, {u'kli^4tz': 1, u'kli^4tze^7': 1, u'kli^4tz^3': 1}], 5: [4, {u'kle^4i^5n^3e^2s^3': 2, u'kle^4i^5n^4e^8': 1, u'geni^5es^8t^5': 1}]}, u'h': {3: [1, {u'auswah^3l^4': 1}]}, u'l': {4: [1, {u'auswah^3l^4': 1}]}, u'n': {3: [5, {u'kle^4i^5n^3e^2s^3': 2, u'kle^3i^3n^3': 1, u'klein^3e^2s': 1, u'klein^3e': 1}], 4: [4, {u'kle^4i^5n^4e^8': 1, u'klein^4e^3s^4': 2, u'kle^5i^2n^4e^5': 1}], 5: [5, {u'klein^5': 1, u'ka^4n^5': 1, u'kle^5in^5e': 1, u'm\xe4dchen^5': 2}], 6: [2, {u'\xfcbe^4r^5a^3schun^6g^3': 1, u'kan^6': 1}]}, u')': {3: [3, {u'-)^3': 3}], 4: [1, {u':-)^4': 1}]}, u's': {8: [1, {u'geni^5es^8t^5': 1}], 3: [3, {u'kle^4i^5n^3e^2s^3': 2, u'kli^3tzes^3': 1}], 4: [5, {u'kleines^4': 1, u'klitzes^4': 1, u'genies^4t^2': 1, u'klein^4e^3s^4': 2}], 6: [1, {u'is^6t': 1}], 7: [2, {u'kleine^4s^7': 2}]}, u'r': {4: [2, {u'\xfcber^4aschung': 2}], 5: [2, {u'\xfcbe^4r^5a^3schun^6g^3': 1, u'\xfcber^5aschung': 1}]}, u'u': {12: [1, {u'hu^12ngrig': 1}]}, u'\U0001f600': {5: [1, {u'\U0001f600^5': 1}]}, u'z': {3: [1, {u'kli^4tz^3': 1}]}, u'\U0001f62b': {4: [1, {u'\U0001f62b^4': 1}]}, u't': {5: [1, {u'geni^5es^8t^5': 1}]}}
        summery.should.be.equal(right_summery)



        #### "repl" ####
        ## Case 1.3
        summery = stats.compute_rep_sum("*", "repl", ignore_num=True, ignore_symbol=True, word_examples_sum_table=False)
        summery = {letter:{rep_num:[rep_num_data[0]] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'a': {3: [1], 4: [1], 6: [1]}, u'e': {8: [2], 3: [4], 4: [10], 5: [6], 7: [1]}, u'g': {3: [1], 6: [1]}, u'i': {8: [1], 3: [2], 4: [3], 5: [4]}, u'h': {3: [1]}, u'l': {4: [1]}, u'n': {3: [5], 4: [4], 5: [5], 6: [2]}, u')': {3: [3], 4: [1]}, u's': {8: [1], 3: [3], 4: [5], 6: [1], 7: [2]}, u'r': {4: [2], 5: [2]}, u'u': {12: [1]}, u'\U0001f600': {5: [1]}, u'z': {3: [1]}, u'\U0001f62b': {4: [1]}, u't': {5: [1]}}
        summery.should.be.equal(right_summery)


        #### "repl" ####
        ## Case 1.4
        summery = stats.compute_rep_sum("*", "repl", ignore_num=True, ignore_symbol=True,sentiment="positive")
        summery = summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u')': {3: [3, {u'-)^3': 3}], 4: [1, {u':-)^4': 1}]}, u'\U0001f600': {5: [1, {u'\U0001f600^5': 1}]}}
        summery.should.be.equal(right_summery)
       


        #### "repl" ####
        ## Case 1.5
        summery = stats.compute_rep_sum(["klitze"], "repl", ignore_num=True, ignore_symbol=True,word_examples_sum_table=True)
        summery = summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'i': {4: [1, {u'kli^4tze^7': 1}]}, u'e': {4: [2, {u'klitze^4': 2}], 7: [1, {u'kli^4tze^7': 1}]}}
        summery.should.be.equal(right_summery)


        #### "repl" ####
        ## Case 1.6
        summery = stats.compute_rep_sum(["klitze", "kleine"], "repl", ignore_num=True, ignore_symbol=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'i': {4: [1, {u'kli^4tze^7': 1}]}, u'e': {4: [1, {u'klitze^4': 1}], 5: [2, {u'kle^5ine': 1, u'kle^5in^5e': 1}], 7: [1, {u'kli^4tze^7': 1}]}, u'n': {3: [1, {u'klein^3e': 1}], 5: [1, {u'kle^5in^5e': 1}]}}
        summery.should.be.equal(right_summery)



        #### "repl" ####
        ## Case 1.7
        summery = stats.compute_rep_sum(["klitze", "kleine"], "repl", ignore_num=True, ignore_symbol=True,stemmed_search=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'i': {3: [2, {u'kle^3i^3n^3': 1, u'kli^3tzes^3': 1}], 4: [3, {u'kli^4tz': 1, u'kli^4tze^7': 1, u'kli^4tz^3': 1}]}, u's': {3: [1, {u'kli^3tzes^3': 1}], 4: [2, {u'klitzes^4': 1, u'kleines^4': 1}]}, u'z': {3: [1, {u'kli^4tz^3': 1}]}, u'e': {3: [1, {u'kle^3i^3n^3': 1}], 4: [1, {u'klitze^4': 1}], 5: [2, {u'kle^5ine': 1, u'kle^5in^5e': 1}], 7: [1, {u'kli^4tze^7': 1}]}, u'n': {3: [3, {u'klein^3e^2s': 1, u'kle^3i^3n^3': 1, u'klein^3e': 1}], 5: [2, {u'kle^5in^5e': 1, u'klein^5': 1}]}}
        summery.should.be.equal(right_summery)


        #### "repl" ####
        ## Case 1.5
        summery = stats.compute_rep_sum(["klitze"], "repl", ignore_num=True, ignore_symbol=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'i': {4: [1, {u'kli^4tze^7': 1}]}, u'e': {4: [2, {u'klitze^4': 2}], 7: [1, {u'kli^4tze^7': 1}]}}
        summery.should.be.equal(right_summery)


        #### "repl" ####
        ## Case 1.6 
        summery = stats.compute_rep_sum(["klitze", "kleine"], "repl", ignore_num=True, ignore_symbol=True,stemmed_search=True)
        summery = {letter:{rep_num:[rep_num_data[0], dict(rep_num_data[1])] for rep_num, rep_num_data in letter_data.iteritems()} for letter, letter_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'i': {3: [2, {u'kle^3i^3n^3': 1, u'kli^3tzes^3': 1}], 4: [3, {u'kli^4tz': 1, u'kli^4tze^7': 1, u'kli^4tz^3': 1}]}, u's': {3: [1, {u'kli^3tzes^3': 1}], 4: [2, {u'klitzes^4': 1, u'kleines^4': 1}]}, u'z': {3: [1, {u'kli^4tz^3': 1}]}, u'e': {3: [1, {u'kle^3i^3n^3': 1}], 4: [1, {u'klitze^4': 1}], 5: [2, {u'kle^5ine': 1, u'kle^5in^5e': 1}], 7: [1, {u'kli^4tze^7': 1}]}, u'n': {3: [3, {u'klein^3e^2s': 1, u'kle^3i^3n^3': 1, u'klein^3e': 1}], 5: [2, {u'kle^5in^5e': 1, u'klein^5': 1}]}}
        summery.should.be.equal(right_summery)
        


        # ################################################
        # #### "redu" ####
        # ##############################################
        ## Case 2.1
        summery = stats.compute_rep_sum("*", "redu")
        summery = {word:{redu_length:occur for redu_length, occur in word_data.iteritems()} for word, word_data in summery.iteritems()}
        #p(summery)
        right_summery = {u'-)': {2: 1}, u'baseline': {3: 2}, u'bleibt': {2: 1}, u'geniest': {2: 1}, u'in': {4: 2}, u'kan': {2: 1}, u'klein': {2: 1}, u'kleine': {2: 1}, u'kleinere': {2: 1}, u'kleines': {2: 1, 3: 2}, u'klitz': {3: 1}, u'klitze': {2: 1, 4: 1}, u'klitzes': {2: 1}}
        summery.should.be.equal(right_summery)
        # i=0
        # for word, word_data in summery.iteritems():
        #     for redu_length, occur in word_data.iteritems():
        #         i+= 1
        #         print word,redu_length, occur
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







