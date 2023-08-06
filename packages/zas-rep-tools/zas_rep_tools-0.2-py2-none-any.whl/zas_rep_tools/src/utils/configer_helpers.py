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

import json
from collections import defaultdict

from nltk.tokenize import TweetTokenizer
import zas_rep_tools.src.utils.db_helper as db_helper

class ConfigerData(object):
    def __init__(self):      
        self._suported_user_info = ["error_tracking", "project_folder", "twitter_creditials", "email"]

        self._path_to_testdbs =  "data/tests_data/testDBs/testFolder"

        self._path_to_testsets = {
                    "blogger":"data/tests_data/Corpora/BloggerCorpus",
                    "twitter":"data/tests_data/Corpora/TwitterCorpus"
                    }

        self._types_folder_names_of_testsets = {
                                "txt":{
                                        "highrepetativ":"txt/HighRepetativSubSet",
                                        "fake":"txt/SmallFakeSubset",
                                        "small":"txt/SmallSubset"
                                    },
                                "csv":{
                                    "highrepetativ":"csv/HighRepetativSubSet",
                                    "fake":"csv/SmallFakeSubset",
                                    "small":"csv/SmallSubset"
                                },
                                "xml":{
                                    "highrepetativ":"xml/HighRepetativSubSet",
                                    "fake":"xml/SmallFakeSubset",
                                    "small":"xml/SmallSubset"
                                },
                                "json":{
                                    "highrepetativ":"json/HighRepetativSubSet",
                                    "fake":"json/SmallFakeSubset",
                                    "small":"json/SmallSubset"
                                },
                                "sqlite":{
                                    "highrepetativ":"sqlite/HighRepetativSubSet",
                                    "fake":"sqlite/SmallFakeSubset",
                                    "small":"sqlite/SmallSubset"
                                }
                            }


        self._test_dbs = {
                    "plaintext":{
                                "blogger":{
                                            "en":{
                                                    "corpus":"7614_corpus_blogs_bloggerCorpus_en_extern_plaintext.db",
                                                    "stats":"7614_3497_stats_bloggerCorpus_en_extern_plaintext.db"
                                                  },

                                            "de":{
                                                    "corpus":"7614_corpus_blogs_bloggerCorpus_de_extern_plaintext.db",
                                                    "stats":"7614_3497_stats_bloggerCorpus_de_extern_plaintext.db"
                                                 },

                                            "ru":{},
                                            "test":{
                                                    "corpus":"7614_corpus_blogs_bloggerCorpus_test_extern_plaintext.db",
                                                    "stats":"7614_3497_stats_bloggerCorpus_test_extern_plaintext.db"
                                                   },


                                        },
                                "twitter":{
                                            "en":{},
                                            "de":{
                                                    #"corpus":"9588_corpus_twitter_streamed_de_intern_plaintext.db",
                                                    #"stats": "9588_6361_stats_streamed_de_intern_plaintext.db"
                                                  },
                                            "ru":{},
                                            "test":{},

                                        }
                                },
                    "encrypted":{
                                "blogger":{
                                            "en":{
                                                    #"corpus":"7614_corpus_blogs_bloggerCorpus_en_extern_encrypted.db",
                                                    #"stats":"7614_3497_stats_bloggerCorpus_en_extern_encrypted.db"
                                                 },
                                            "de":{},
                                            "ru":{},
                                            "test":{},

                                        },
                                "twitter":{
                                            "en":{},
                                            "de":{
                                                    "corpus":"9588_corpus_twitter_streamed_de_intern_encrypted.db",
                                                    "stats": "9588_6361_stats_streamed_de_intern_encrypted.db"
                                                 },
                                            "ru":{},
                                            "test":{},

                                        }
                                }
                    }
                


        self._init_info_data = {
                "blogger":{ "id":{"corpus":7614, "stats":3497},
                            "name":"bloggerCorpus",
                            "platform_name":"blogs",
                            "version":"1",
                            "language":"en",
                            "created_at":None,
                            "source":"LanguageGoldMine",
                            "license":"CreativCommon",
                            "visibility":"extern",
                            "template_name":"blogger",
                            "encryption_key": {"corpus":"corpus", "stats":"stats"}
                          },

                "twitter":{ "id":{"corpus":9588, "stats":6361},
                            "name":"streamed",
                            "platform_name":"twitter",
                            "version":"1",
                            "language":"de",
                            "created_at":None,
                            "source":"Twitter API",
                            "license":"Twitter Developer Agreement",
                            "visibility":"intern",
                            "template_name":"twitter",
                            "encryption_key": {"corpus":"corpus", "stats":"stats"}
                          },
                }




        self._columns_in_doc_table = {
                    "blogger": [column[0]  for column in db_helper.default_columns_and_types_for_corpus_documents+db_helper.extended_columns_and_types_for_corpus_documents_blogger],
                    "twitter": [column[0]  for column in db_helper.default_columns_and_types_for_corpus_documents+db_helper.extended_columns_and_types_for_corpus_documents_twitter]
                        }
        #p(self._columns_in_doc_table )
        self._columns_in_info_tabel = {
                    "corpus": [column[0]  for column in db_helper.attributs_names_corpus],
                    "stats": [column[0]  for column in db_helper.attributs_names_stats]
                        }

        self._columns_in_stats_tables = {
                        "redu": [column[0]  for column in db_helper.default_columns_and_types_for_stats_reduplications],
                        "repl" : [column[0]  for column in db_helper.default_columns_and_types_for_stats_replications],
                        "baseline": [column[0]  for column in db_helper.default_columns_and_types_for_stats_baseline],
                        #"baseline":{
                        #            "repl":[column[0]  for column in db_helper.default_columns_and_types_for_stats_repl_baseline],
                        #            "redu":[column[0]  for column in db_helper.default_columns_and_types_for_redu_baseline]
                        #            }
                        }
        

        self._tokenizer = TweetTokenizer()

        self._lang_order = ["en", "de", "ru", "other"]
        self._text_elements_collection = {
                "en":[
                        "I loved it. But it was also verrrryyyyy vvveRRRRRRrry very piiiiiiiiity pity pity piiitttyyy for me...... :-(((((  @real_trump #sheetlife #readytogo http://www.absurd.com", # [u'It', u'was', u'verrrryyyyy', u'vvveRRRRRRrry', u'very', u'piiiiiiiiity', u'for', u'me', u'-', u'(', u'(', u'(', u'@real_trump', u'#sheetlife', u'#readytogo', u'http://www.absurd.com']
                        "glaaaaaaad to seeeeeeeee you -))))", #[u'glaaaaaaad', u'to', u'seeeeeeeee', u'you', u'-', u')', u')', u')']
                        "a baddddd bad bbbbbbbaaaaaad bbbbaaaaddddd baaaaaaad news, which we can not accept. -(((( 😫😫😫😫 😫😫😫😫😫 😫😫😫 :-(((((  #sheetlife #sheetlife http://www.noooo.com", #[u'a', u'baddddd', u'bad', u'bbbbbbbaaaaaa', u'bbbbaaaaddddd', u'baaaaaaad', u'news', u'-', u'(', u'(', u'(', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'\ud83d', u'\ude2b', u'#sheetlife', u'#sheetlife', u'http://www.noooo.com']
                        "Tiny tiny tiny tiny tiny tiny mooooooodelllllll, which we can use for explain a biiig biiiiiiiiiiiiiiig things.", #[u'Tiny', u'tiny', u'tiny', u'tiny', u'tiny', u'tiny', u'mooooooodelllllll']
                        "Tiny model, but a big big big explaaaaanation. Riiiiiight? What do youuuuuu think about it???? 111111 😫😫😫😫 11111111. Bbbbbuuuutttt buuuuutttt yyyyyyou yoooooou bbbbbbut bbbbbutttt bbbbbuuuuut yyyoouuuu",
                        "tinnnyy tiny tiny surprise. Bbbbbut buuuuut yyyyyyou yoooooou bbbbbbut bbbbbut bbbbbut yyyoouuuu 😀😀😀😀😀🌈🌈🌈🌈🌈🌈🌈😀😀😀😀😀🌈🌈🌈🌈🌈🌈🌈😀😀😀😀😀",
                        "it was really bad surprise for me 😫😫😫😫, buuuuuuuuuut i really reallly reeeeeallllyyy liked it :P =))))))))))  😀😀😀😀😀🌈🌈🌈🌈🌈🌈🌈😀",
                    ],

                "de":[
                        "Klitze kliiiitzeeeeeee kleEEEEinnnnne kleinnne Überaschung. Trotzdem hat sie mich glücklich gemacht! :-)))) -))) 😀😀😀😀😀-))) -)))",  # [u'Klitze', u'kliiiitze', u'kleEEEEine', u'\xdcberaschung', u'-', u')', u')', u')', u'-', u')', u')', u')']
                        "einen wunderschönen Taaaaaagggggg wünsche ich euch. Geniesssstt geniiiiiessssssssttttt das Leben. Bleeeeeeeeibt bleeeeibt Huuuuuuuuuuuungrig. baseline baseline baseline in in in in baseline baseline baseline in in in in", #[u'einnennnnnn', u'toooolllleeeeen', u'Taaaaaagggggg', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83c', u'\udf08', u'\ud83c', u'\udf08', u'\ud83c', u'\udf08', u'\ud83c', u'\udf08', u'\ud83c', u'\udf08', u'\ud83c', u'\udf08', u'\ud83c', u'\udf08'], [u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00', u'\ud83d', u'\ude00']
                        "eine klitzeeee kleeeeeine Überrrraschung @schönesleben #machwasdaraus #bewegedeinArsch https://www.freiesinternet.de Besser kannnnnn kaaaannnnn ess. Kleineeeesssssss kleinnnneeessss kleeeeiiiiinnneesss Mädchennnnn.....  Kleinereeeee kleineeerreeeee Auswahhhllll. klitz kliiiitz kliiiitzzz kleeeiiinnn kleinnnnn. klitzessss kliiitzesss kleinnnees kleinessss",
                        "eine klitzeeee kleine Sache. Die aber trotzdem wichtiiiiiiiig isssssst! Weil es ja eine kleeeeeiinnnneeeee Überrrrraschung ist. 11111 2222 33333 4444 55555  6 . Kleineeeesssssss kleinnnneeessss kleeeeiiiiinnneesss Mädchennnnn.....",
                        "Eine klitze klitze klitze klitze kleine Überrrraschung, die ich mal gerne hatte. 111111 😫😫😫😫 11111111  Du meintest, es war so eineeee kleeeeiiiiinnnneeeeeeee Übeeeerrrrraaaschunnnnnnggg. ",
                    ],

                "ru":[
                        "Oчень оооооченнннь ооооччччееееннннньььь хорошееего дняяяяяяяяя", #[u'O\u0447\u0435\u043d\u044c', u'\u043e\u043e\u043e\u0447\u0435\u043d\u043d\u043d\u044c', u'\u043e\u043e\u043e\u0447\u0447\u0447\u0435\u0435\u0435\u043d\u043d\u043d\u044c\u044c\u044c', u'\u0445\u043e\u0440\u043e\u0448\u0435\u0435\u0435\u0433\u043e', u'\u0434\u043d\u044f\u044f\u044f']
                        "самммооово сааамово  приятногооооо прииииииииятного  ужииииина 🥡🍽🍽🍽🍽🍽🍽🍽🍽🍽🍽", #[u'\u0441\u0430\u043c\u043c\u043c\u043e\u043e\u043e\u0432\u043e', u'\u0441\u0430\u0430\u0430\u043c\u043e\u0432\u043e', u'\u043f\u0440\u0438\u044f\u0442\u043d\u043e\u0433\u043e\u043e\u043e', u'\u043f\u0440\u0438\u0438\u0438\u044f\u0442\u043d\u043e\u0433\u043e', u'\u0443\u0436\u0438\u0438\u0438\u043d\u0430', u'\ud83e', u'\udd61', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d', u'\ud83c', u'\udf7d']
                    ],

                "other":[
                        "اللغة العربية رائعة",
                    ],

                }


        self._counted_reps = {
                                "en": {
                                            u'#shetlife': {'baseline': 3, 'redu': [1, 2]},
                                             u'-(': {'baseline': 1, 'repl': (1, 1)},
                                             u'-)': {'baseline': 1, 'repl': (1, 1)},
                                             u'.': {'baseline': 7, 'repl': (1, 1)},
                                             u'1': {'baseline': 2, 'repl': (2, 2)},
                                             u':-(': {'baseline': 2, 'repl': (2, 2)},
                                             u'=)': {'baseline': 1, 'repl': (1, 1)},
                                             u'?': {'repl': (1, 1), 'baseline': 2},
                                             u'bad': {'baseline': 6, 'redu': (1, 5), 'repl': (4, 7)},
                                             u'big': {'baseline': 5, 'redu': (2, 5), 'repl': (2, 2)},
                                             u'but': {'baseline': 13, 'redu': (4, 10), 'repl': (11, 16)},
                                             u'explanation': {'baseline': 1, 'repl': (1, 1)},
                                             u'glad': {'baseline': 1, 'repl': (1, 1)},
                                             u'model': {'baseline': 2, 'repl': (1, 2)},
                                             u'pity': {'baseline': 4, 'redu': (1, 4), 'repl': (2, 4)},
                                             u'realy': {'baseline': 4, 'redu': (1, 3), 'repl': (2, 4)},
                                             u'right': {'baseline': 1, 'repl': (1, 1)},
                                             u'se': {'baseline': 1, 'repl': (1, 1)},
                                             u'tiny': {'baseline': 10, 'redu': (2, 9), 'repl': (1, 1)},
                                             u'very': {'baseline': 3, 'redu': (1, 3), 'repl': (2, 4)},
                                             u'you': {'baseline': 8, 'redu': (2, 4), 'repl': (7, 9)},
                                             u'\U0001f308': {'baseline': 3, 'repl': (3, 3)},
                                             u'\U0001f600': {'baseline': 5, 'repl': (4, 4)},
                                             u'\U0001f62b': {'baseline': 3, 'repl': (3, 3)}
                                      },
                            }

        self.right_rep_num = {
                                "en": {
                                        "repls":sum([data["repl"][1] for word, data in self._counted_reps["en"].items() if "repl" in data ]),
                                        "redus":sum([data["redu"][0] for word, data in self._counted_reps["en"].items() if "redu" in data ]),
                                        },   
                             }


    def _row_text_elements(self, lang="all"):
        if lang == "test":
            lang ="all"
        if lang == "all":
            return [text_item for lang in self._lang_order for text_item in self._text_elements_collection[lang]]
        else:
            if lang in self._text_elements_collection:
                return self._text_elements_collection[lang]
            else:
                self.logger.error("No test-text-elements exist for given language: '{}'.".format(lang))


    def _text_elements(self, token=True, unicode_str=True, lang="all"):
        if lang == "test":
            lang ="all"
        if token:
            if unicode_str:
                    #sys.exit()
                return [t_elem.split()  for t_elem in self._text_elements(token=False, unicode_str=True,lang=lang)]
                #return [self._tokenizer.tokenize(t_elem)  for t_elem in self._text_elements(token=False, unicode_str=True,lang=lang)]
                #return self._text_elements_as_unicode_str_tokenized
            else:
                return [t_elem.split()  for t_elem in self._text_elements(token=False, unicode_str=False,lang=lang)]
                #return [self._tokenizer.tokenize(t_elem)  for t_elem in self._text_elements(token=False, unicode_str=False,lang=lang)]
                #return self._text_elements_as_byte_str_tokenized

        elif not token:
            if unicode_str:
                #for t_elem in self._row_text_elements(lang=lang):
                #    p((t_elem, type(t_elem)))
                #sys.exit()
                #json.loads(t_elem)
                return [json.loads(r'"{}"'.format(t_elem)) for t_elem in self._row_text_elements(lang=lang) ]
                #return [t_elem.decode("utf-8") for t_elem in self._row_text_elements(lang=lang) ]
                #return self._text_elements_as_unicode_str_untokenized
            else:
                return self._row_text_elements(lang=lang)




    def _docs_row_values(self,token=True, unicode_str=True, lang="all"):
        if lang == "test":
            lang ="all"
        text_element = self._text_elements(token=token, unicode_str=unicode_str, lang=lang)
        #self.logger.critical(text_element)
        if lang == "en":
            text_element = self._text_elements(token=token, unicode_str=unicode_str, lang=lang)
            docs_row_values_en = {
                    "blogger":[
                        [1, 1111, text_element[0], u'w', 37, u'IT', u'lion' ],
                        [2, 2222, text_element[1], u'm', 23, u'Care', u'fish' ],
                        [3, 3333, text_element[2], u'w', 22, u'Finance', u'aquarius' ],
                        [4, 4444, text_element[3], u'm', 27, u'IT', u'gemini' ],
                        [5, 5555, text_element[4], u'w', 35, u'Air Industry', u'lion' ],
                        [6, 6666, text_element[5], u'm', 21, u'Industry', "crawfish"  ],
                        [7, 7777, text_element[6], u'w', 37, u'IT', u'lion' ],
                        ],

                    "twitter":[
                        [1 ,1111, text_element[0], u"20/06/2014", u"en", u"Iphone", u"22/03/2014", u"Die Welt ist schön", 45, 76, 765, 34567890, u"en", u"MotherFucker", u"realBro", u"True", "planet Earth", False, False, False ],
                        [2 ,2222, text_element[1], u"03/02/2013", u"en", u"Iphone", u"29/06/2012", u"Kein Plan", 45, 76, 765, 34567890, u"en", u"MotherFucker", u"realBro", u"True", "planet Earth", False, False, False ],
                        [3 ,3333, text_element[2], u"21/06/2014", u"en", u"WebAPI", u"21/07/2017", u"Neiiiiin", 45, 76, 765, 34567890, u"en", u"MotherFucker", u"realBro", u"True", "planet Earth", False, False, False ],
                        [4 ,4444, text_element[3], u"20/04/2014", u"fr", u"Iphone", u"12/06/2011", u"Nööö", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        [5 ,5555, text_element[4], u"20/06/2011", u"ru", u"Android", u"12/06/2012", u"Was willste, alter?", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        [6 ,6666, text_element[5], u"30/09/2014", u"ru", u"Iphone", u"20/03/2013", u"Neiiiiin", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        [7 ,7777, text_element[6], u"01/06/2014", u"de", u"Android", u"22/06/2011", u"Neiiiiin", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        ]
                    }
            return docs_row_values_en
        
        elif lang == "de":
            text_element = self._text_elements(token=token, unicode_str=unicode_str, lang=lang)
            #p((text_element))
            docs_row_values_de = {
                    "blogger":[
                        [8, 8888, text_element[0], u'm', 23, u'Care', u'fish' ],
                        [9, 9999, text_element[1], u'w', 22, u'Finance', u'aquarius' ],
                        [10, 10000, text_element[2], u'w', 35, u'Air Industry', u'lion' ],
                        [11, 11111, text_element[3], u'm', 21, u'Industry', "crawfish"  ],
                        [12, 12222, text_element[4], u'w', 37, u'IT', u'lion' ],
                        ],

                    "twitter":[
                        [8 ,8888, text_element[0], u"20/06/2007", u"de", u"Iphone", u"20/02/2009", u"Jööööö", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        [9 ,9999, text_element[1], u"20/04/2014", u"it", u"WebAPI", u"01/06/2011", u"Neiiiiin", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        [10 ,10000, text_element[2], u"21/06/2014", u"en", u"WebAPI", u"21/07/2017", u"Neiiiiin", 45, 76, 765, 34567890, u"en", u"MotherFucker", u"realBro", u"True", "planet Earth", False, False, False ],
                        [11 ,11111, text_element[3], u"20/04/2014", u"fr", u"Iphone", u"12/06/2011", u"Nööö", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        [12 ,12222, text_element[4], u"20/06/2011", u"ru", u"Android", u"12/06/2012", u"Was willste, alter?", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        ]
                    }
            return docs_row_values_de

        elif lang == "ru":
            text_element = self._text_elements(token=token, unicode_str=unicode_str, lang=lang)
            docs_row_values_ru = {
                    "blogger":[
                        [13, 13333, text_element[0], u'm', 23, u'Care', u'fish' ],
                        [14, 14444, text_element[1], u'w', 22, u'Finance', u'aquarius' ],
                        ],

                    "twitter":[
                        [13 ,13333, text_element[0], u"30/09/2014", u"ru", u"Iphone", u"20/03/2013", u"Neiiiiin", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        [14 ,14444, text_element[1], u"01/06/2014", u"de", u"Android", u"22/06/2011", u"Neiiiiin", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ],
                        ]
                    }
            return docs_row_values_ru

        elif lang == "other":
            text_element = self._text_elements(token=token, unicode_str=unicode_str, lang=lang)
            docs_row_values_other = {
                "blogger":[
                    [15, 15555, text_element[0], u'w', 22, u'Finance', u'aquarius' ],
                    ],

                "twitter":[
                    [15 ,16666, text_element[0], u"20/04/2014", u"it", u"WebAPI", u"01/06/2011", u"Neiiiiin", 45, 76, 765, 98765, u"en", u"Lighter", u"LivelyLife", u"True", "planet Earth", False, False, False ]
                    ]
                }
            return docs_row_values_other

        elif lang == "all":
            temp_dict = defaultdict(list)
            for language in ["en", "de", "ru", "other"]:
                output_for_current_lang = self._docs_row_values(token=token, unicode_str=unicode_str, lang=language)

                for k,v in output_for_current_lang.iteritems():
                    temp_dict[k] += v

            return temp_dict





    def _docs_row_dict(self, token=True, unicode_str=True, all_values=True , lang="all"):
        '''
        just one dict with colums as key and list of all values as values for each columns()key
        '''
        if lang == "test":
            lang ="all"
        docs_row_values = self._docs_row_values(token=token, unicode_str=unicode_str, lang=lang)
        #p(docs_row_values,"docs_row_values")
        if all_values:
            return {template_name:{k:v for k,v in zip(columns, zip(*docs_row_values[template_name]))} for template_name, columns in  self._columns_in_doc_table.iteritems()}
        else:
            return {template_name:{col:row[0] for col, row in data.iteritems()}  for template_name, data in  self._docs_row_dict(token=token, unicode_str=unicode_str,lang=lang,all_values=True).iteritems()}



    def _docs_row_dicts(self, token=True, unicode_str=True, lang="all"):
        '''
        list of dicts  with colums and values for each row
        '''
        if lang == "test":
            lang ="all"
        docs_row_values = self._docs_row_values(token=token, unicode_str=unicode_str, lang=lang)
        docs_row_dicts = { template_name:[dict(zip(columns, row)) for row in docs_row_values[template_name]] for template_name, columns in  self._columns_in_doc_table.iteritems()}
        return docs_row_dicts



