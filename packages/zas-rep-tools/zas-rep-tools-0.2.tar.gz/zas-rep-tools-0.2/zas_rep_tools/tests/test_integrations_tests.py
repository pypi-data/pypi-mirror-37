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
from zas_rep_tools.src.classes.reader import Reader
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



class TestZASIntergrationTests(BaseTester,unittest.TestCase):
    #_multiprocess_can_split_ = True
    _multiprocess_shared_  = True
    #@classmethod 
    def setUp(self):
        super(type(self), self).setUp()



    #@classmethod 
    def tearDown(self):
        super(type(self), self).tearDown()


####################################################################################################
####################################################################################################
###################### START STABLE TESTS #########################################################
####################################################################################################
####################################################################################################




    ###### xxx: 000 ######




    ##### xx :0== ######


    @attr(status='stable')
    #@wipd
    def test_data_insertion_000(self):
        #reader = Reader(mode=self.mode)
        corpus = Corpus(mode=self.mode)
        stats = Stats(mode=self.mode)
        stats.should.be.a(Stats)

        

    ##### throws_exceptions:050  ######



    def _get_basic_info_about_reps(self, data):
        extracted = {}
        for item in data:
            temp_item = []
            #p(item)
            #temp_item.append(item["baseline"])
            temp = [ [unicode(el) for el in _item ] for _item in item["baseline"]]
            extracted[tuple(item["syntagma"])] = temp
            #item["baseline"]
        return extracted


    def convert(self,inp):
        return  [ [unicode(el) for el in _item ] for _item in inp]

#################################Beginn##############################################
############################EXTERN METHODS###########################################
#####################################################################################


###################  Corpus Initialization :500############################################ 


    ###### test the workflow ######

    @attr(status='stable')
    #@wipd
    def test_work_flow_with_basic_reps_500(self):
        #reader = Reader(mode=self.mode)
        self.prj_folder()
        self.input_list = [
                            {
                                'rowid':'1' ,
                                'star_constellation': 'Capricorn', 
                                'text': "Klitze klitze kleine kleine Menge...",
                                'working_area': 'IT Consulting', 
                                'age': '46', 
                                'id': '324114', 
                                'gender': 'female'
                            }, 
                            
                            {
                                'rowid':'2' ,
                                'star_constellation': 'Fish', 
                                'text': "Klitze klitze kleine kleine Menge...",
                                'working_area': 'IT Developing', 
                                'age': '23', 
                                'id': '8765', 
                                'gender': 'male'
                            }, 
                            
                        ]

        ### Corp Meta Data ####
        name = "test_corp"
        language = "de"
        visibility = "intern"
        platform_name = "blogger"
        source="test"
        license="test"
        template_name = "blogger"
        version= 1
        corp_typ= "corpus"

        #### Preprocessing Settings #######
        preprocession = True
        tokenizer = True
        pos_tagger = False
        sent_splitter = True
        sentiment_analyzer = True
        lang_classification = False
        del_url = False
        del_punkt = False
        del_num = False
        del_html = False
        del_mention = False
        del_hashtag = False
        case_sensitiv = True


        corp = Corpus(logger_level=logging.DEBUG,mode=self.mode)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, 
                    source=source, license=license, template_name=template_name,  version= version,
                    preprocession=preprocession, tokenizer=tokenizer, pos_tagger=pos_tagger, sent_splitter=sent_splitter,
                    sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification,
                    del_url=del_url,  del_punkt=del_punkt, del_num=del_num, del_html=del_html, 
                    del_mention=del_mention, del_hashtag=del_hashtag,case_sensitiv=case_sensitiv, )
        corp.insert(self.input_list)
        list(corp.docs(columns="text"))[0].should.be.equal((u'[[[["Klitze", "regular"], ["klitze", "regular"], ["kleine", "regular"], ["kleine", "regular"], ["Menge", "regular"], ["...", "symbol"]], ["neutral", 0.0]]]',))
        list(corp.docs(columns="text"))[1].should.be.equal((u'[[[["Klitze", "regular"], ["klitze", "regular"], ["kleine", "regular"], ["kleine", "regular"], ["Menge", "regular"], ["...", "symbol"]], ["neutral", 0.0]]]',))
        corp.corpdb.get_attr("token_num").should.be.equal(12)
        corp.corpdb.get_attr("doc_num").should.be.equal(2)
        corp.corpdb.get_attr("sent_num").should.be.equal(2)



        #### full_repetativ_syntagma=True + case_sensitiv_stat=False  ######
        case_sensitiv_stat = False
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility,  version= version, full_repetativ_syntagma=True,case_sensitiv=case_sensitiv_stat,baseline_delimiter="++",)
        stats.compute(corp)
        #print 
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[("klitze",)].should.be.equal(self.convert(([[u'klitze'], u'klitz', 1, 4, None, None, u'2', u'4', None, u'2'],)))
        basic_info[("kleine",)].should.be.equal(self.convert(([[u'kleine'], u'klein', 1, 4, None, None, u'2', u'4', None, u'2'],)))
        basic_info[("klitze","kleine")].should.be.equal(self.convert(([[u'klitze', u'kleine'], u'klitz++klein', 2, 2, None, None, u'[2, 2]', u'[4, 4]', None, u'2'],)))
        basic_info[(".",)].should.be.equal(self.convert(([[u'.'], u'.', 1, 2, u'2', u'2', None, None, u'2', None],)))
        len(basic_info).should.be.equal(4)

        ### check right summerizing 
        right_sum_repl = {
                            u'.': {
                                    3: [2, {u'.^3': 2}]
                                   }
                        }


        right_sum_redu = {
                            u'kleine': {2: 2}, 
                            u'klitze': {2: 2}
                        }
        
        extracted_repl = { word:{nr_rep:[occur[0],{rle:count  for rle, count in occur[1].items() }] for nr_rep, occur in data.items()} for word, data in  stats.compute_rep_sum("*", "repl").items()}
        extracted_redu = { word:{nr_rep:occur for nr_rep, occur in data.items()} for word, data in  stats.compute_rep_sum("*", "redu").items()}
        extracted_repl.should.be.equal(right_sum_repl)
        extracted_redu.should.be.equal(right_sum_redu)


        #sys.exit()
        #### full_repetativ_syntagma=True + case_sensitiv_stat=True  ######
        case_sensitiv_stat = True
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility,  version= version, full_repetativ_syntagma=True,case_sensitiv=case_sensitiv_stat,baseline_delimiter="++",)
        stats.compute(corp)
        #print stats.statsdb.getall("replications")
        #print stats.statsdb.getall("reduplications")
        #print stats.statsdb.getall("replications")
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[(u'.',)].should.be.equal(self.convert(([[u'.'], u'.', 1, 2, u'2', u'2', None, None, u'2', None],)))
        basic_info[(u'kleine',)].should.be.equal(self.convert(([[u'kleine'], u'klein', 1, 4, None, None, u'2', u'4', None, u'2'],)))
        len(basic_info).should.be.equal(2)
        #p(basic_info.keys(), "basic_info")




        #### full_repetativ_syntagma=False ######
        case_sensitiv_stat = False
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility,  version= version, full_repetativ_syntagma=False,case_sensitiv=case_sensitiv_stat,baseline_delimiter="++")
        stats.compute(corp)
        #print 
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        
        basic_info[("klitze",)].should.be.equal(self.convert(([[u'klitze'], u'klitz', 1, 4, None, None, u'2', u'4', None, u'2'],)))
        basic_info[("kleine",)].should.be.equal(self.convert(([[u'kleine'], u'klein', 1, 4, None, None, u'2', u'4', None, u'2'],)))
        basic_info[("klitze","kleine")].should.be.equal(self.convert(([[u'klitze', u'kleine'], u'klitz++klein', 2, 2, None, None, u'[2, 2]', u'[4, 4]', None, None],)))
        basic_info[(".",)].should.be.equal(self.convert(([[u'.'], u'.', 1, 2, u'2', u'2', None, None, u'2', None],)))
        basic_info[(u'kleine', u'menge', u'.')].should.be.equal(self.convert(([[u'kleine', u'menge', u'.'], u'klein++meng++.', 3, 2, u'[0, 0, 2]', u'[0, 0, 2]', u'[2, 0, 0]', u'[4, 0, 0]', None, None],)))
        basic_info[(u'klitze', u'kleine', u'menge', u'.')].should.be.equal(self.convert(([[u'klitze', u'kleine', u'menge', u'.'], u'klitz++klein++meng++.', 4, 2, u'[0, 0, 0, 2]', u'[0, 0, 0, 2]', u'[2, 2, 0, 0]', u'[4, 4, 0, 0]', None, None],)))
        basic_info[(u'klitze', u'kleine', u'menge')].should.be.equal(self.convert(([[u'klitze', u'kleine', u'menge'], u'klitz++klein++meng', 3, 2, None, None, u'[2, 2, 0]', u'[4, 4, 0]', None, None],)))
        basic_info[(u'kleine', u'menge')].should.be.equal(self.convert(([[u'kleine', u'menge'], u'klein++meng', 2, 2, None, None, u'[2, 0]', u'[4, 0]', None, None],)))
        basic_info[(u'menge', u'.')].should.be.equal(self.convert(([[u'menge', u'.'], u'meng++.', 2, 2, u'[0, 2]', u'[0, 2]', None, None, None, None],)))
        len(basic_info).should.be.equal(9)
        #p(basic_info.keys(), "basic_info")





    @attr(status='stable')
    #@wipd
    def test_work_flow_with_white_trash_and_ignore_option_501(self):
        #reader = Reader(mode=self.mode)
        self.prj_folder()
        self.input_list = [
                            {
                                'rowid':'1' ,
                                'star_constellation': 'Capricorn', 
                                'text': "@buuuussy_guyyyy @buuuussy_guyyyy ...... #hhhaaaavy #hhhaaaavy www.trash.de http://trash.de",
                                'working_area': 'IT Consulting', 
                                'age': '46', 
                                'id': '324114', 
                                'gender': 'female'
                            }, 
                            
                            {
                                'rowid':'2' ,
                                'star_constellation': 'Fish', 
                                'text': "@buuuussy_guyyyy @buuuussy_guyyyy ...... #hhhaaaavy #hhhaaaavy www.trash.de http://trash.de",
                                'working_area': 'IT Developing', 
                                'age': '23', 
                                'id': '8765', 
                                'gender': 'male'
                            }, 
                            
                        ]

        ### Corp Meta Data ####
        name = "test_corp"
        language = "de"
        visibility = "intern"
        platform_name = "blogger"
        source="test"
        license="test"
        template_name = "blogger"
        version= 1
        corp_typ= "corpus"

        #### Preprocessing Settings #######
        preprocession = True
        tokenizer = True
        pos_tagger = False
        sent_splitter = True
        sentiment_analyzer = True
        lang_classification = False
        del_url = False
        del_punkt = False
        del_num = False
        del_html = False
        del_mention = False
        del_hashtag = False
        case_sensitiv = True


        corp = Corpus(logger_level=logging.DEBUG,mode=self.mode)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, 
                    source=source, license=license, template_name=template_name,  version= version,
                    preprocession=preprocession, tokenizer=tokenizer, pos_tagger=pos_tagger, sent_splitter=sent_splitter,
                    sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification,
                    del_url=del_url,  del_punkt=del_punkt, del_num=del_num, del_html=del_html, 
                    del_mention=del_mention, del_hashtag=del_hashtag,case_sensitiv=case_sensitiv, )
        corp.insert(self.input_list)
        list(corp.docs(columns="text"))[0].should.be.equal((u'[[[["@buuuussy_guyyyy", "mention"], ["@buuuussy_guyyyy", "mention"], ["......", "symbol"], ["#hhhaaaavy", "hashtag"], ["#hhhaaaavy", "hashtag"], ["www.trash.de", "URL"], ["http://trash.de", "URL"]], ["neutral", 0.0]]]',))
        list(corp.docs(columns="text"))[1].should.be.equal((u'[[[["@buuuussy_guyyyy", "mention"], ["@buuuussy_guyyyy", "mention"], ["......", "symbol"], ["#hhhaaaavy", "hashtag"], ["#hhhaaaavy", "hashtag"], ["www.trash.de", "URL"], ["http://trash.de", "URL"]], ["neutral", 0.0]]]',))
        corp.corpdb.get_attr("token_num").should.be.equal(14)
        corp.corpdb.get_attr("doc_num").should.be.equal(2)
        corp.corpdb.get_attr("sent_num").should.be.equal(2)




        #### full_repetativ_syntagma=True + case_sensitiv_stat=False + ignore=False ######
        case_sensitiv_stat = True
        ignore_hashtag = False
        ignore_url = False
        ignore_mention = False
        ignore_punkt = False
        ignore_num = False
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility,  version= version,baseline_delimiter="++",
                    full_repetativ_syntagma=True,case_sensitiv=case_sensitiv_stat,
                    ignore_hashtag=ignore_hashtag, ignore_url=ignore_url, ignore_mention=ignore_mention,
                    ignore_punkt=ignore_punkt, ignore_num=ignore_num)
        stats.compute(corp)
        #print stats.statsdb.getall("replications")
        #print stats.statsdb.getall("reduplications")
        #print stats.statsdb.getall("replications")
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[(u'.',)].should.be.equal(self.convert(([[u'.'], u'.', 1, 2, u'2', u'2', None, None, u'2', None],)))
        basic_info[(u'.', u'#havy')].should.be.equal(self.convert(([[u'.', u'#havy'], u'.++#havy', 2, 2, u'[2, 4]', u'[2, 8]', None, None, u'2', None],)))
        basic_info[(u'@busy_guy', u'.', u'#havy')].should.be.equal(self.convert(([[u'@busy_guy', u'.', u'#havy'], u'@busy_guy++.++#havy', 3, 2, u'[4, 2, 4]', u'[8, 2, 8]', None, None, u'2', None],)))
        basic_info[(u'@busy_guy', u'.')].should.be.equal(self.convert(([[u'@busy_guy', u'.'], u'@busy_guy++.', 2, 2, u'[4, 2]', u'[8, 2]', None, None, u'2', None],)))
        basic_info[(u'@busy_guy',)].should.be.equal(self.convert(([[u'@busy_guy'], u'@busy_guy', 1, 4, u'4', u'8', u'2', u'4', u'4', u'2'],)))
        basic_info[(u'#havy',)].should.be.equal(self.convert(([[u'#havy'], u'#havy', 1, 4, u'4', u'8', u'2', u'4', u'4', u'2'],)))
        len(basic_info).should.be.equal(6)
        #p(basic_info.keys(), "basic_info")
        

        #### full_repetativ_syntagma=True + case_sensitiv_stat=False + ignore=True ######
        case_sensitiv_stat = False
        ignore_hashtag = True
        ignore_url = True
        ignore_mention = True
        ignore_punkt = True
        ignore_num = True
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility,  version= version,baseline_delimiter="++",
                    full_repetativ_syntagma=True,case_sensitiv=case_sensitiv_stat,
                    ignore_hashtag=ignore_hashtag, ignore_url=ignore_url, ignore_mention=ignore_mention,
                    ignore_punkt=ignore_punkt, ignore_num=ignore_num)
        stats.compute(corp)
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[(u':hashtag:', u':URL:')].should.be.equal(self.convert(([[u':hashtag:', u':URL:'], u':hashtag:++:uRL:', 2, 2, None, None, u'[2, 2]', u'[4, 4]', None, u'2'],)))
        basic_info[(u':URL:',)].should.be.equal(self.convert(([[u':URL:'], u':uRL:', 1, 4, None, None, u'2', u'4', None, u'2'],)))
        basic_info[(u':mention:',)].should.be.equal(self.convert(([[u':mention:'], u':mention:', 1, 4, None, None, u'2', u'4', None, u'2'],)))
        basic_info[(u':hashtag:',)].should.be.equal(self.convert(([[u':hashtag:'], u':hashtag:', 1, 4, None, None, u'2', u'4', None, u'2'],)))
        len(basic_info).should.be.equal(4)
        #p(basic_info.keys(), "basic_info")
        
        



    @attr(status='stable')
    #@wipd
    def test_work_flow_with_EMOIMG_EMOASC_502(self):
        #reader = Reader(mode=self.mode)
        self.prj_folder()
        self.input_list = [
                            {
                                'rowid':'1' ,
                                'star_constellation': 'Capricorn', 
                                'text': u"-))))) -))))))))) 😀😀😀😀😀😀 🌈🌈🌈🌈 🧑🏻🧑🏻🧑🏻🧑🏻🧑🏻 💁🏿‍♀️💁🏿‍♀️💁🏿‍♀️💁🏿‍♀️💁🏿‍♀️ 🇧🇭🇧🇭🇧🇭🇧🇭",
                                'working_area': 'IT Consulting', 
                                'age': '46', 
                                'id': '324114', 
                                'gender': 'female'
                            }, 
                            
                            {
                                'rowid':'2' ,
                                'star_constellation': 'Capricorn', 
                                'text': u"-))))) -))))))))) 😀😀😀😀😀😀 🌈🌈🌈🌈 🧑🏻🧑🏻🧑🏻🧑🏻🧑🏻 💁🏿‍♀️💁🏿‍♀️💁🏿‍♀️💁🏿‍♀️💁🏿‍♀️ 🇧🇭🇧🇭🇧🇭🇧🇭",
                                'working_area': 'IT Support', 
                                'age': '24', 
                                'id': '3241436543', 
                                'gender': 'male'
                            }, 
                        ]

        ### Corp Meta Data ####
        name = "test_corp"
        language = "de"
        visibility = "intern"
        platform_name = "blogger"
        source="test"
        license="test"
        template_name = "blogger"
        version= 1
        corp_typ= "corpus"

        #### Preprocessing Settings #######
        preprocession = True
        tokenizer = True
        pos_tagger = False
        sent_splitter = True
        sentiment_analyzer = True
        lang_classification = False
        del_url = False
        del_punkt = False
        del_num = False
        del_html = False
        del_mention = False
        del_hashtag = False
        case_sensitiv = False


        corp = Corpus(logger_level=logging.DEBUG,mode=self.mode, status_bar=True)
        corp.init(self.tempdir_project_folder, name, language, visibility, platform_name, 
                    source=source, license=license, template_name=template_name,  version= version,
                    preprocession=preprocession, tokenizer=tokenizer, pos_tagger=pos_tagger, sent_splitter=sent_splitter,
                    sentiment_analyzer=sentiment_analyzer, lang_classification=lang_classification,
                    del_url=del_url,  del_punkt=del_punkt, del_num=del_num, del_html=del_html, 
                    del_mention=del_mention, del_hashtag=del_hashtag,case_sensitiv=case_sensitiv, )
        corp.insert(self.input_list)
        #p(list(corp.docs(columns="text")))
        list(corp.docs(columns="text"))[0].should.be.equal((u'[[[["-)))))", "EMOASC"], ["-)))))))))", "EMOASC"], ["\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00", "EMOIMG"], ["\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded", "regular"]], ["neutral", 0.0]]]',))
        list(corp.docs(columns="text"))[1].should.be.equal((u'[[[["-)))))", "EMOASC"], ["-)))))))))", "EMOASC"], ["\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00\\ud83d\\ude00", "EMOIMG"], ["\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08\\ud83c\\udf08", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83e\\uddd1", "EMOIMG"], ["\\ud83c\\udffb", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83d\\udc81", "EMOIMG"], ["\\ud83c\\udfff", "EMOIMG"], ["\\u2640", "EMOIMG"], ["\\ufe0f", "EMOIMG"], ["\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded\\ud83c\\udde7\\ud83c\\udded", "regular"]], ["neutral", 0.0]]]',))
        corp.corpdb.get_attr("token_num").should.be.equal(70)
        corp.corpdb.get_attr("doc_num").should.be.equal(2)
        corp.corpdb.get_attr("sent_num").should.be.equal(2)




        #### full_repetativ_syntagma=True  ######
        case_sensitiv_stat = False
        ignore_hashtag = False
        ignore_url = False
        ignore_mention = False
        ignore_punkt = False
        ignore_num = False
        stats = Stats(mode=self.mode)
        stats.init(self.tempdir_project_folder, name, language, visibility,  version= version,baseline_delimiter="++",
                    full_repetativ_syntagma=True,case_sensitiv=case_sensitiv_stat,
                    ignore_hashtag=ignore_hashtag, ignore_url=ignore_url, ignore_mention=ignore_mention,
                    ignore_punkt=ignore_punkt, ignore_num=ignore_num)
        stats.compute(corp)
        #print stats.statsdb.getall("replications")
        #print stats.statsdb.getall("reduplications")
        #print stats.statsdb.getall("replications")
        basic_info = self._get_basic_info_about_reps(stats.get_data(redu=True, repl=True, baseline=True))
        basic_info[(u'-)', u'\U0001f600')].should.be.equal(self.convert(([[u'-)', u'\U0001f600'], u'-)++\U0001f600', 2, 2, u'[4, 2]', u'[4, 2]', None, None, u'2', None],)))
        basic_info[(u'\U0001f600',)].should.be.equal(self.convert(([[u'\U0001f600'], u'\U0001f600', 1, 2, u'2', u'2', None, None, u'2', None],)))
        basic_info[(u'-)',)].should.be.equal(self.convert(([[u'-)'], u'-)', 1, 4, u'4', u'4', u'2', u'4', u'4', u'2'],)))
        basic_info[(u'\U0001f308',)].should.be.equal(self.convert(([[u'\U0001f308'], u'\U0001f308', 1, 2, u'2', u'2', None, None, u'2', None],)))
        basic_info[(u'\U0001f600', u'\U0001f308')].should.be.equal(self.convert(([[u'\U0001f600', u'\U0001f308'], u'\U0001f600++\U0001f308', 2, 2, u'[2, 2]', u'[2, 2]', None, None, u'2', None],)))
        basic_info[(u'-)', u'\U0001f600', u'\U0001f308')].should.be.equal(self.convert(([[u'-)', u'\U0001f600', u'\U0001f308'], u'-)++\U0001f600++\U0001f308', 3, 2, u'[4, 2, 2]', u'[4, 2, 2]', None, None, u'2', None],)))
        len(basic_info).should.be.equal(6)
        #p(basic_info.keys(), "basic_info")

        basic_info = self._get_basic_info_about_reps(stats.get_data(inp_syntagma=["EMOIMG"],redu=True, repl=True, baseline=True,syntagma_type="pos", if_type_pos_return_lexem_syn=True))
        basic_info[(u'\U0001f600',)].should.be.equal(self.convert([[[u'\U0001f600'], u'\U0001f600', 1, 2, u'2', u'2', None, None, u'2', None]]))
        basic_info[(u'\U0001f308',)].should.be.equal(self.convert([[[u'\U0001f308'], u'\U0001f308', 1, 2, u'2', u'2', None, None, u'2', None]]))
        len(basic_info).should.be.equal(2) 
        #p(basic_info.keys(), "basic_info"  )     

        basic_info = self._get_basic_info_about_reps(stats.get_data(inp_syntagma=["EMOASC"],redu=True, repl=True, baseline=True,syntagma_type="pos", if_type_pos_return_lexem_syn=True))
        basic_info[(u'-)',)].should.be.equal(self.convert([[[u'-)'], u'-)', 1, 4, u'4', u'4', u'2', u'4', u'4', u'2']]))
        len(basic_info).should.be.equal(1) 
        #p(basic_info.keys(), "basic_info"  )  


        ### check right summerizing 
        right_sum_repl = {
                            u')': {
                                    9: [2, {u'-)^9': 2}], 
                                    5: [2, {u'-)^5': 2}]}, 
                            
                            u'\U0001f600': {
                                    6: [2, {u'\U0001f600^6': 2}]}, 
                            
                            u'\U0001f308': {
                                    4: [2, {u'\U0001f308^4': 2}]}
                        }


        right_sum_redu = {u'-)': {2: 2}}
        
        extracted_repl = { word:{nr_rep:[occur[0],{rle:count  for rle, count in occur[1].items() }] for nr_rep, occur in data.items()} for word, data in  stats.compute_rep_sum("*", "repl").items()}
        extracted_redu = { word:{nr_rep:occur for nr_rep, occur in data.items()} for word, data in  stats.compute_rep_sum("*", "redu").items()}
        extracted_repl.should.be.equal(right_sum_repl)
        extracted_redu.should.be.equal(right_sum_redu)

        #p((extracted_repl, extracted_redu))
        #sys.exit()

#################################END##################################################
############################EXTERN METHODS############################################
######################################################################################








#################################Beginn##############################################
############################INTERN METHODS###########################################
#####################################################################################

###################    :100############################################ 

    



    ###### ***** ######


    ###### ***** ######






#################################END#################################################
############################INTERN METHODS###########################################
#####################################################################################





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







