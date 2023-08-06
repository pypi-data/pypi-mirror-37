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


#from zas_rep_tools.src.classes.configer import Configer
from zas_rep_tools.src.classes.stats import Stats
from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.basetester import BaseTester
from zas_rep_tools.src.utils.helpers import  Rle



import platform
if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama



class TestZASHelpersRLE(BaseTester,unittest.TestCase):
    #_multiprocess_can_split_ = True
    _multiprocess_shared_  = True
    #@classmethod 
    def setUp(self):
        super(type(self), self).setUp()

        self.test_byte_str1_decoded = "biggggggggg fatttttttt pooooonnnnnnnyyyyyyyyyyy..... Or how to beeeeee haaaaapppy!!!!!"
        self.test_byte_str2_decoded = "So beautiful life 😀😀😀😀😀😀😀😀😜😜😜😜😜😜 😇😇😇😇😇"
        self.test_byte_str3_decoded = "mit Üüüüüüüberzeugung hat er aaaallllles gestäääämt!!!"
        self.test_byte_str4_decoded = "нууууу как бы мооооооооооожно лиииииии????"
       
        self.test_unicode_str1_decoded = u"biggggggggg fatttttttt pooooonnnnnnnyyyyyyyyyyy..... Or how to beeeeee haaaaapppy!!!!!"
        self.test_unicode_str2_decoded = u"So beautiful life 😀😀😀😀😀😀😀😀😜😜😜😜😜😜 😇😇😇😇😇"
        self.test_unicode_str3_decoded = u"mit Üüüüüüüberzeugung hat er aaaallllles gestäääämt!!!"
        self.test_unicode_str4_decoded = u"нууууу как бы мооооооооооожно лиииииии????"


        self.test_byte_str1_repfree = "big fat pony. Or how to be hapy!"
        self.test_byte_str2_repfree = "So beautiful life 😀😜 😇"
        self.test_byte_str3_repfree = "mit Üüberzeugung hat er ales gestämt!"
        self.test_byte_str4_repfree = "ну как бы можно ли?"


        self.test_byte_str1_encoded_to_tuples = [(u'b', 1), (u'i', 1), (u'g', 9), (u' ', 1), (u'f', 1), (u'a', 1), (u't', 8), (u' ', 1), (u'p', 1), (u'o', 5), (u'n', 7), (u'y', 11), (u'.', 5), (u' ', 1), (u'O', 1), (u'r', 1), (u' ', 1), (u'h', 1), (u'o', 1), (u'w', 1), (u' ', 1), (u't', 1), (u'o', 1), (u' ', 1), (u'b', 1), (u'e', 6), (u' ', 1), (u'h', 1), (u'a', 5), (u'p', 3), (u'y', 1), (u'!', 5)]
        self.test_byte_str2_encoded_to_tuples = [(u'S', 1), (u'o', 1), (u' ', 1), (u'b', 1), (u'e', 1), (u'a', 1), (u'u', 1), (u't', 1), (u'i', 1), (u'f', 1), (u'u', 1), (u'l', 1), (u' ', 1), (u'l', 1), (u'i', 1), (u'f', 1), (u'e', 1), (u' ', 1), (u'\U0001f600', 8), (u'\U0001f61c', 6), (u' ', 1), (u'\U0001f607', 5)]
        self.test_byte_str3_encoded_to_tuples = [(u'm', 1), (u'i', 1), (u't', 1), (u' ', 1), (u'\xdc', 1), (u'\xfc', 6), (u'b', 1), (u'e', 1), (u'r', 1), (u'z', 1), (u'e', 1), (u'u', 1), (u'g', 1), (u'u', 1), (u'n', 1), (u'g', 1), (u' ', 1), (u'h', 1), (u'a', 1), (u't', 1), (u' ', 1), (u'e', 1), (u'r', 1), (u' ', 1), (u'a', 4), (u'l', 5), (u'e', 1), (u's', 1), (u' ', 1), (u'g', 1), (u'e', 1), (u's', 1), (u't', 1), (u'\xe4', 4), (u'm', 1), (u't', 1), (u'!', 3)]
        self.test_byte_str4_encoded_to_tuples = [(u'\u043d', 1), (u'\u0443', 5), (u' ', 1), (u'\u043a', 1), (u'\u0430', 1), (u'\u043a', 1), (u' ', 1), (u'\u0431', 1), (u'\u044b', 1), (u' ', 1), (u'\u043c', 1), (u'\u043e', 11), (u'\u0436', 1), (u'\u043d', 1), (u'\u043e', 1), (u' ', 1), (u'\u043b', 1), (u'\u0438', 7), (u'?', 4)]


        self.test_byte_str1_encoded_to_str = "b1i1g9 1f1a1t8 1p1o5n7y11.5 1O1r1 1h1o1w1 1t1o1 1b1e6 1h1a5p3y1!5"
        self.test_byte_str2_encoded_to_str = "S1o1 1b1e1a1u1t1i1f1u1l1 1l1i1f1e1 1😀8😜6 1😇5"
        self.test_byte_str3_encoded_to_str = "m1i1t1 1Ü1ü6b1e1r1z1e1u1g1u1n1g1 1h1a1t1 1e1r1 1a4l5e1s1 1g1e1s1t1ä4m1t1!3"
        self.test_byte_str4_encoded_to_str = "н1у5 1к1а1к1 1б1ы1 1м1о11ж1н1о1 1л1и7?4"


        self.test_byte_sent1_decoded = ["big", "big", "big",  "big", "fat", "pony", "pony"]
        self.test_byte_sent2_decoded = ["😀","😀","😀","😀","😀" , "😍"]

        self.test_byte_sent1_decoded_to_str = "big big big big fat pony pony"
        self.test_byte_sent2_decoded_to_str = "😀 😀 😀 😀 😀 😍"

        self.test_byte_sent1_encoded = [('big', 4), ('fat', 1), ('pony', 2)]
        self.test_byte_sent2_encoded = [('\xf0\x9f\x98\x80', 5), ('\xf0\x9f\x98\x8d', 1)]

        self.test_byte_sent1_encoded_mapping = [0, 4, 5]
        self.test_byte_sent2_encoded_mapping = [0, 5]

        self.test_byte_sent1_repfree = "big fat pony"
        self.test_byte_sent2_repfree = "😀 😍"

#repfree

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
    def test_rle_initialization_000(self):
        rle = Rle()

        

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
    def test_del_rep_from_byte_str_500(self):
        rle = Rle()
        rle.del_rep(self.test_byte_str1_decoded).encode("utf-8").should.be.equal(self.test_byte_str1_repfree)
        rle.del_rep(self.test_byte_str2_decoded).encode("utf-8").should.be.equal(self.test_byte_str2_repfree)
        rle.del_rep(self.test_byte_str3_decoded).encode("utf-8").should.be.equal(self.test_byte_str3_repfree)
        rle.del_rep(self.test_byte_str4_decoded).encode("utf-8").should.be.equal(self.test_byte_str4_repfree)

    @attr(status='stable')
    #@wipd
    def test_del_rep_from_unicode_str_501(self):
        rle = Rle()
        rle.del_rep(self.test_unicode_str1_decoded).encode("utf-8").should.be.equal(self.test_byte_str1_repfree)
        rle.del_rep(self.test_unicode_str2_decoded).encode("utf-8").should.be.equal(self.test_byte_str2_repfree)
        rle.del_rep(self.test_unicode_str3_decoded).encode("utf-8").should.be.equal(self.test_byte_str3_repfree)
        rle.del_rep(self.test_unicode_str4_decoded).encode("utf-8").should.be.equal(self.test_byte_str4_repfree)

    @attr(status='stable')
    #@wipd
    def test_del_rep_from_list_with_words_502(self):
        rle = Rle()
        rle.del_rep_from_sent(self.test_byte_sent1_decoded).encode("utf-8").should.be.equal(self.test_byte_sent1_repfree)
        rle.del_rep_from_sent(self.test_byte_sent2_decoded).encode("utf-8").should.be.equal(self.test_byte_sent2_repfree)


    @attr(status='stable')
    #@wipd
    def test_encode_rle_of_words_to_tuples_as_byte_str_503_1(self):
        rle = Rle()
        rle.encode_to_tuples(self.test_byte_str1_decoded).should.be.equal(self.test_byte_str1_encoded_to_tuples) 
        rle.encode_to_tuples(self.test_byte_str2_decoded).should.be.equal(self.test_byte_str2_encoded_to_tuples) 
        rle.encode_to_tuples(self.test_byte_str3_decoded).should.be.equal(self.test_byte_str3_encoded_to_tuples) 
        rle.encode_to_tuples(self.test_byte_str4_decoded).should.be.equal(self.test_byte_str4_encoded_to_tuples) 

    @attr(status='stable')
    #@wipd
    def test_encode_rle_of_words_to_tuples_with_additional_start_index_as_byte_str_503_2(self):
        rle = Rle()
        # p(rle.encode_to_tuples(self.test_byte_str1_decoded, mapping=True), "str1")
        # p(rle.encode_to_tuples(self.test_byte_str2_decoded, mapping=True), "str2")
        # p(rle.encode_to_tuples(self.test_byte_str3_decoded, mapping=True), "str3")
        # p(rle.encode_to_tuples(self.test_byte_str4_decoded, mapping=True), "str4")
        rle.encode_to_tuples(self.test_byte_str1_decoded, mapping=True).should.be.equal(([(u'b', 1), (u'i', 1), (u'g', 9), (u' ', 1), (u'f', 1), (u'a', 1), (u't', 8), (u' ', 1), (u'p', 1), (u'o', 5), (u'n', 7), (u'y', 11), (u'.', 5), (u' ', 1), (u'O', 1), (u'r', 1), (u' ', 1), (u'h', 1), (u'o', 1), (u'w', 1), (u' ', 1), (u't', 1), (u'o', 1), (u' ', 1), (u'b', 1), (u'e', 6), (u' ', 1), (u'h', 1), (u'a', 5), (u'p', 3), (u'y', 1), (u'!', 5)], [0, 1, 2, 11, 12, 13, 14, 22, 23, 24, 29, 36, 47, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 70, 71, 72, 77, 80, 81]))
        rle.encode_to_tuples(self.test_byte_str2_decoded, mapping=True).should.be.equal(([(u'S', 1), (u'o', 1), (u' ', 1), (u'b', 1), (u'e', 1), (u'a', 1), (u'u', 1), (u't', 1), (u'i', 1), (u'f', 1), (u'u', 1), (u'l', 1), (u' ', 1), (u'l', 1), (u'i', 1), (u'f', 1), (u'e', 1), (u' ', 1), (u'\U0001f600', 8), (u'\U0001f61c', 6), (u' ', 1), (u'\U0001f607', 5)], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 26, 32, 33]))
        rle.encode_to_tuples(self.test_byte_str3_decoded, mapping=True).should.be.equal(([(u'm', 1), (u'i', 1), (u't', 1), (u' ', 1), (u'\xdc', 1), (u'\xfc', 6), (u'b', 1), (u'e', 1), (u'r', 1), (u'z', 1), (u'e', 1), (u'u', 1), (u'g', 1), (u'u', 1), (u'n', 1), (u'g', 1), (u' ', 1), (u'h', 1), (u'a', 1), (u't', 1), (u' ', 1), (u'e', 1), (u'r', 1), (u' ', 1), (u'a', 4), (u'l', 5), (u'e', 1), (u's', 1), (u' ', 1), (u'g', 1), (u'e', 1), (u's', 1), (u't', 1), (u'\xe4', 4), (u'm', 1), (u't', 1), (u'!', 3)], [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33, 38, 39, 40, 41, 42, 43, 44, 45, 49, 50, 51]))
        rle.encode_to_tuples(self.test_byte_str4_decoded, mapping=True).should.be.equal(([(u'\u043d', 1), (u'\u0443', 5), (u' ', 1), (u'\u043a', 1), (u'\u0430', 1), (u'\u043a', 1), (u' ', 1), (u'\u0431', 1), (u'\u044b', 1), (u' ', 1), (u'\u043c', 1), (u'\u043e', 11), (u'\u0436', 1), (u'\u043d', 1), (u'\u043e', 1), (u' ', 1), (u'\u043b', 1), (u'\u0438', 7), (u'?', 4)], [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 26, 27, 28, 29, 30, 31, 38]))



    @attr(status='stable')
    #@wipd
    def test_encode_sent_to_tuples_504_1(self):
        rle = Rle()
        rle.encode_to_tuples(self.test_byte_sent1_decoded).should.be.equal(self.test_byte_sent1_encoded)
        rle.encode_to_tuples(self.test_byte_sent2_decoded).should.be.equal(self.test_byte_sent2_encoded)


    @attr(status='stable')
    #@wipd
    def test_encode_sent_to_tuples_504_2(self):
        rle = Rle()
        #p(rle.encode_to_tuples(self.test_byte_sent1_decoded, mapping=True))
        #p(rle.encode_to_tuples(self.test_byte_sent2_decoded, mapping=True))
        #self.test_byte_sent1_encoded,self.test_byte_sent1_encoded_mapping
        (rle.encode_to_tuples(self.test_byte_sent1_decoded, mapping=True)).should.be.equal((self.test_byte_sent1_encoded,self.test_byte_sent1_encoded_mapping))
        (rle.encode_to_tuples(self.test_byte_sent2_decoded, mapping=True)).should.be.equal((self.test_byte_sent2_encoded,self.test_byte_sent2_encoded_mapping))





    @attr(status='stable')
    #@wipd
    def test_decode_list_of_words_in_tuples_to_list_506(self):
        rle = Rle()
        rle.decode_words_to_list(self.test_byte_sent1_encoded).should.be.equal(self.test_byte_sent1_decoded)
        rle.decode_words_to_list(self.test_byte_sent2_encoded).should.be.equal(self.test_byte_sent2_decoded)


    @attr(status='stable')
    #@wipd
    def test_decode_letters_to_str_507(self):
        rle = Rle()
        rle.decode_letters_to_str(self.test_byte_str1_encoded_to_tuples).encode("utf-8").should.be.equal(self.test_byte_str1_decoded) 
        rle.decode_letters_to_str(self.test_byte_str2_encoded_to_tuples).encode("utf-8").should.be.equal(self.test_byte_str2_decoded) 
        rle.decode_letters_to_str(self.test_byte_str3_encoded_to_tuples).encode("utf-8").should.be.equal(self.test_byte_str3_decoded) 
        rle.decode_letters_to_str(self.test_byte_str4_encoded_to_tuples).encode("utf-8").should.be.equal(self.test_byte_str4_decoded) 


    @attr(status='stable')
    #@wipd
    def test_decode_words_to_str_508(self):
        rle = Rle()
        rle.decode_words_to_str(self.test_byte_sent1_encoded).should.be.equal(self.test_byte_sent1_decoded_to_str) 
        rle.decode_words_to_str(self.test_byte_sent2_encoded).should.be.equal(self.test_byte_sent2_decoded_to_str) 


    @attr(status='stable')
    #@wipd
    def test_encode_str_to_str_509(self):
        rle = Rle()
        rle.encode_str_to_str(self.test_byte_str1_decoded).encode("utf-8").should.be.equal(self.test_byte_str1_encoded_to_str)
        rle.encode_str_to_str(self.test_byte_str2_decoded).encode("utf-8").should.be.equal(self.test_byte_str2_encoded_to_str)
        rle.encode_str_to_str(self.test_byte_str3_decoded).encode("utf-8").should.be.equal(self.test_byte_str3_encoded_to_str)
        rle.encode_str_to_str(self.test_byte_str4_decoded).encode("utf-8").should.be.equal(self.test_byte_str4_encoded_to_str)


    @attr(status='stable')
    #@wipd
    def test_decode_str_from_str_510(self):
        rle = Rle()
        rle.decode_str_from_str(self.test_byte_str1_encoded_to_str).should.be.equal(self.test_byte_str1_decoded)
        rle.decode_str_from_str(self.test_byte_str2_encoded_to_str).should.be.equal(self.test_byte_str2_decoded)
        rle.decode_str_from_str(self.test_byte_str3_encoded_to_str).should.be.equal(self.test_byte_str3_decoded)
        rle.decode_str_from_str(self.test_byte_str4_encoded_to_str).should.be.equal(self.test_byte_str4_decoded)





    @attr(status='stable')
    #@wipd
    def test_get_rep_free_word_from_rle_as_tuples_as_bytestr_511(self):
        rle = Rle()

        #p(rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str1_encoded_to_tuples))
        rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str1_encoded_to_tuples).should.be.equal(u'big fat pony. Or how to be hapy!')
        #p(rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str2_encoded_to_tuples))
        rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str2_encoded_to_tuples).should.be.equal(u'So beautiful life \U0001f600\U0001f61c \U0001f607')
        #p(rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str3_encoded_to_tuples))
        rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str3_encoded_to_tuples).should.be.equal(u'mit \xdc\xfcberzeugung hat er ales gest\xe4mt!')
        #p(rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str4_encoded_to_tuples))
        rle.get_rep_free_word_from_rle_in_tuples(self.test_byte_str4_encoded_to_tuples).should.be.equal(u'\u043d\u0443 \u043a\u0430\u043a \u0431\u044b \u043c\u043e\u0436\u043d\u043e \u043b\u0438?')





    @attr(status='stable')
    #@wipd
    def test_encode_rle_of_sent_to_tuples_512(self):
        rle = Rle()
        #p(self.test_byte_sent1_encoded)
        #p(rle.get_rep_free_sent_from_rle_in_tuples(self.test_byte_sent1_encoded))
        rle.get_rep_free_sent_from_rle_in_tuples(self.test_byte_sent1_encoded).should.be.equal(u'big fat pony')
        #p(rle.get_rep_free_sent_from_rle_in_tuples(self.test_byte_sent2_encoded))
        rle.get_rep_free_sent_from_rle_in_tuples(self.test_byte_sent2_encoded).should.be.equal(u'\U0001f600 \U0001f60d')
        #p(self.test_byte_sent2_encoded)






    @attr(status='stable')
    #@wipd
    def test_get_repetativ_elems_513(self):
        rle = Rle()

        #p(rle.get_repetativ_elems(self.test_byte_str1_encoded_to_tuples))
        rle.get_repetativ_elems(self.test_byte_str1_encoded_to_tuples).should.be.equal([(u'g', 9, 2), (u't', 8, 6), (u'o', 5, 9), (u'n', 7, 10), (u'y', 11, 11), (u'.', 5, 12), (u'e', 6, 25), (u'a', 5, 28), (u'p', 3, 29), (u'!', 5, 31)])
        #p(rle.get_repetativ_elems(self.test_byte_str2_encoded_to_tuples))
        rle.get_repetativ_elems(self.test_byte_str2_encoded_to_tuples).should.be.equal([(u'\U0001f600', 8, 18), (u'\U0001f61c', 6, 19), (u'\U0001f607', 5, 21)])
        #p(rle.get_repetativ_elems(self.test_byte_str3_encoded_to_tuples))
        rle.get_repetativ_elems(self.test_byte_str3_encoded_to_tuples).should.be.equal([(u'\xfc', 6, 5), (u'a', 4, 24), (u'l', 5, 25), (u'\xe4', 4, 33), (u'!', 3, 36)])
        
        #p(self.test_unicode_str4_decoded)
        #p(rle.get_repetativ_elems(self.test_byte_str4_encoded_to_tuples))
        rle.get_repetativ_elems(self.test_byte_str4_encoded_to_tuples).should.be.equal([(u'\u0443', 5, 1), (u'\u043e', 11, 11), (u'\u0438', 7, 17), (u'?', 4, 18)])



    @attr(status='stable')
    #@wipd
    def test_rep_extraction_word_without_rle_514(self):
        rle = Rle()
        #p(rle.rep_extraction_word(self.test_byte_str1_encoded_to_tuples))
        rle.rep_extraction_word(self.test_byte_str1_encoded_to_tuples).should.be.equal(([(u'g', 9, 2), (u't', 8, 6), (u'o', 5, 9), (u'n', 7, 10), (u'y', 11, 11), (u'.', 5, 12), (u'e', 6, 25), (u'a', 5, 28), (u'p', 3, 29), (u'!', 5, 31)], u'big fat pony. Or how to be hapy!'))
        #p(rle.rep_extraction_word(self.test_byte_str2_encoded_to_tuples))
        rle.rep_extraction_word(self.test_byte_str2_encoded_to_tuples).should.be.equal(([(u'\U0001f600', 8, 18), (u'\U0001f61c', 6, 19), (u'\U0001f607', 5, 21)], u'So beautiful life \U0001f600\U0001f61c \U0001f607'))
        #p(rle.rep_extraction_word(self.test_byte_str3_encoded_to_tuples))
        rle.rep_extraction_word(self.test_byte_str3_encoded_to_tuples).should.be.equal(([(u'\xfc', 6, 5), (u'a', 4, 24), (u'l', 5, 25), (u'\xe4', 4, 33), (u'!', 3, 36)], u'mit \xdc\xfcberzeugung hat er ales gest\xe4mt!'))

        #p(self.test_unicode_str4_decoded)
        #p(rle.rep_extraction_word(self.test_byte_str4_encoded_to_tuples))
        rle.rep_extraction_word(self.test_byte_str4_encoded_to_tuples).should.be.equal(([(u'\u0443', 5, 1), (u'\u043e', 11, 11), (u'\u0438', 7, 17), (u'?', 4, 18)], u'\u043d\u0443 \u043a\u0430\u043a \u0431\u044b \u043c\u043e\u0436\u043d\u043e \u043b\u0438?'))



    @attr(status='stable')
    #@wipd
    def test_rep_extraction_word_with_rle_515(self):
        rle = Rle()
        # p(rle.rep_extraction_word(self.test_byte_str1_encoded_to_tuples, get_rle_as_str=True))
        rle.rep_extraction_word(self.test_byte_str1_encoded_to_tuples, get_rle_as_str=True).should.be.equal(([(u'g', 9, 2), (u't', 8, 6), (u'o', 5, 9), (u'n', 7, 10), (u'y', 11, 11), (u'.', 5, 12), (u'e', 6, 25), (u'a', 5, 28), (u'p', 3, 29), (u'!', 5, 31)], u'big fat pony. Or how to be hapy!', u'big^9 fat^8 po^5n^7y^11.^5 Or how to be^6 ha^5p^3y!^5'))
        # p(rle.rep_extraction_word(self.test_byte_str2_encoded_to_tuples, get_rle_as_str=True))
        rle.rep_extraction_word(self.test_byte_str2_encoded_to_tuples, get_rle_as_str=True).should.be.equal(([(u'\U0001f600', 8, 18), (u'\U0001f61c', 6, 19), (u'\U0001f607', 5, 21)], u'So beautiful life \U0001f600\U0001f61c \U0001f607', u'So beautiful life \U0001f600^8\U0001f61c^6 \U0001f607^5'))
        # p(rle.rep_extraction_word(self.test_byte_str3_encoded_to_tuples, get_rle_as_str=True))
        rle.rep_extraction_word(self.test_byte_str3_encoded_to_tuples, get_rle_as_str=True).should.be.equal(([(u'\xfc', 6, 5), (u'a', 4, 24), (u'l', 5, 25), (u'\xe4', 4, 33), (u'!', 3, 36)], u'mit \xdc\xfcberzeugung hat er ales gest\xe4mt!', u'mit \xdc\xfc^6berzeugung hat er a^4l^5es gest\xe4^4mt!^3'))

        #p(self.test_unicode_str4_decoded)
        # p(rle.rep_extraction_word(self.test_byte_str4_encoded_to_tuples, get_rle_as_str=True))
        rle.rep_extraction_word(self.test_byte_str4_encoded_to_tuples, get_rle_as_str=True).should.be.equal(([(u'\u0443', 5, 1), (u'\u043e', 11, 11), (u'\u0438', 7, 17), (u'?', 4, 18)], u'\u043d\u0443 \u043a\u0430\u043a \u0431\u044b \u043c\u043e\u0436\u043d\u043e \u043b\u0438?', u'\u043d\u0443^5 \u043a\u0430\u043a \u0431\u044b \u043c\u043e^11\u0436\u043d\u043e \u043b\u0438^7?^4'))




    @attr(status='stable')
    #@wipd
    def test_rep_extraction_sent_515(self):
        rle = Rle()
        self.test_byte_sent1_encoded,self.test_byte_sent1_encoded_mapping
        #p(repr(rle.rep_extraction_sent(self.test_byte_sent1_encoded_with_start_index)))
        rle.rep_extraction_sent(self.test_byte_sent1_encoded,self.test_byte_sent1_encoded_mapping).should.be.equal(([{'start_index_in_orig': 0, 'length': 4, 'word': 'big', 'index_in_redu_free': 0}, {'start_index_in_orig': 5, 'length': 2, 'word': 'pony', 'index_in_redu_free': 2}], ['big', 'fat', 'pony']))
        #p(repr(rle.rep_extraction_sent(self.test_byte_sent2_encoded_with_start_index)))
        rle.rep_extraction_sent(self.test_byte_sent2_encoded,self.test_byte_sent2_encoded_mapping).should.be.equal(([{'start_index_in_orig': 0, 'length': 5, 'word': '\xf0\x9f\x98\x80', 'index_in_redu_free': 0}], ['\xf0\x9f\x98\x80', '\xf0\x9f\x98\x8d']))


    # @attr(status='stable')
    # #@wipd
    # def test_rep_extraction_sent_with_rle_516(self):
    #     rle = Rle()
    #     #p(rle.rep_extraction_sent(self.test_byte_sent1_encoded, get_rle_as_str=True))
    #     rle.rep_extraction_sent(self.test_byte_sent1_encoded, get_rle_as_str=True).should.be.equal(([('big', 4, 0), ('pony', 2, 2)], 'big fat pony', '(big)^4 fat (pony)^2'))
    #     #p(rle.rep_extraction_sent(self.test_byte_sent2_encoded, get_rle_as_str=True))
    #     rle.rep_extraction_sent(self.test_byte_sent2_encoded, get_rle_as_str=True).should.be.equal(([('\xf0\x9f\x98\x80', 5, 0)], '\xf0\x9f\x98\x80 \xf0\x9f\x98\x8d', '(\xf0\x9f\x98\x80)^5 \xf0\x9f\x98\x8d'))




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







