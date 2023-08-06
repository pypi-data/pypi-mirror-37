#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : Command Line Interface  
# Author:
# c(Student) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###Programm Info######


import click
import shutil
import os
import inspect
import sys
import logging
import ast
import json
from blessings import Terminal
import enlighten
import time
import itertools

#from zas_rep_tools.src.utils.zaslogger import ZASLogger
from zas_rep_tools.src.utils.cli_helper import set_main_folders, get_cli_logger, validate_corp,validate_stats, strtobool, get_corp_fname, _get_status_bars_manager, _get_new_status_bar,get_stats_fname
from zas_rep_tools.src.utils.helpers import set_class_mode
import zas_rep_tools.src.utils.helpers as helpers
from zas_rep_tools.src.classes.reader import  Reader
from zas_rep_tools.src.classes.corpus import  Corpus
from zas_rep_tools.src.utils.corpus_helpers import  CorpusData

from zas_rep_tools.src.classes.stats import  Stats
from zas_rep_tools.src.classes.exporter import  Exporter
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.classes.streamer import Streamer
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.classes.ToolConfiger import ToolConfiger



answer_error_tracking = None
project_folder = None
email = None
twitter_creditials = None
configer_obj = None
#logger = None
main_folders = set_main_folders(project_folder)
end_file_marker = -1
configer_obj = ToolConfiger(mode="error")



supported_commands = {
        "configer": {
                        "prjdir":["clean", "set", "reset", "print"],
                        "error_track":["set", "reset", "respeak","print"],
                        "twitter":["set", "reset", "respeak","print"],
                        "email":["set", "reset", "respeak","print"],
                        "user_data":["clean", "location","print"],

                    },
        "corpora": ["add", "del", "names", "meta", "basic_stats", "update_attr", "export", "used_tools", "clean_dir","cols", "doc", "ids"],
        "stats": ["compute", "del", "names", "meta", "basic_stats", "update_attr", "export", "clean_dir", "recompute","optimize", "recreate_indexes"],
        'streamer':[]
        }





@click.group()
def main():
    global answer_error_tracking
    global project_folder
    global email
    global twitter_creditials
    global configer_obj
    global main_folders


     
    configer_obj.get_data_from_user(rewrite=False)

    answer_error_tracking = configer_obj._user_data['error_tracking']
    project_folder = configer_obj._user_data['project_folder']
    if not project_folder:
        configer_obj.logger.error("ProjectDirectory wasn't given. Please Give first a new ProjectDirectory, before starting to use this tool.")
        sys.exit()
        return False
    
    else:
        if not os.path.isdir(project_folder):
            configer_obj.logger.error("ProjectDirectory is not exist or given path to this directory is illegal. ('{}') Please give one ProjectDirectory, which are also exist".format(project_folder))
            return False
    
    main_folders = set_main_folders(project_folder)

    email = configer_obj._user_data['email']
    twitter_creditials = configer_obj._user_data['twitter_creditials']





@main.command('configer')
@click.argument('command1')
@click.argument('command2')
@click.option('--mode', '-m', default="prod" ,help="Set one of the Tool Modus", type=click.Choice(helpers.modi))
@click.option('--logdir', '-ld', default="logs", help="Choose the name of the Directory for log data.")
def configer(command1,command2,  mode,logdir ):
    # $ zas-vot-tools strat1 sets/train_set sets/eval_set  segments voiceless voiced vlwindow vcwindow experiments
    logger = get_cli_logger(mode,logdir)
    #p(command,"command")
    func_name = "configer"
    if command1 not in supported_commands[func_name]:
        logger.error(" Given Command ('{}') is illegal for '{}'. Please use one of the following commands: '{}' ".format(command1,func_name,supported_commands[func_name] ))
        return False
    if command2 not in supported_commands[func_name][command1]:
        logger.error(" Given Command ('{}') is illegal for '{}'->{}. Please use one of the following commands: '{}' ".format(command2,func_name,command1,supported_commands[func_name][command1] ))
        return False

    if command1 == "prjdir":
        if command2 in ["set", "reset"]:
            #p(configer_obj, "configer_obj")
            configer_obj._cli_menu_get_from_user_project_folder()
        elif command2 == "clean":
            if os.isdir(project_folder):
                os.remove(project_folder)
                os.makedirs(project_folder)
            else:
                logger.error("Current ProjectDirectory is not exist.")
                return False
        elif command2 == "print":
            print "ProjectDirectory: '{}'. ".format(project_folder)

    elif command1 == "error_track":
        if command2 in ["set", "reset", "respeak"]:
            configer_obj._cli_menu_error_agreement()
        elif command2 == "print":
            print ">>> Error_tracking: {};".format( configer_obj._user_data["error_tracking"])
    
    elif command1 == "twitter":
        if command2 in ["set", "reset", "respeak"]:
            configer_obj._cli_menu_get_from_user_twitter_credentials()
        elif command2 == "print":
            print ">>> Twitter_creditials: {};".format( configer_obj._user_data["twitter_creditials"])
    

    elif command1 == "email":
        if command2 in ["set", "reset", "respeak"]:
            configer_obj._cli_menu_get_from_user_emails()
        elif command2 == "print":
            print ">>> Email: {};".format( configer_obj._user_data["email"])
    
    
    elif command1 == "user_data":
        if command2 == "clean":
            configer_obj._user_data.clean()
        elif command2 == "location":
            print "ProjectDirectory: '{}'. ".format(project_folder)
            print "ConfigsData: '{}'. ".format(configer_obj._path_to_user_config_data)
        elif command2 == "print":
            #import json
            for cat in configer_obj._user_data:
                print ">>> {}: '{}';".format(cat.upper(), configer_obj._user_data[cat])



### all DB


@main.command('corpora')
@click.argument('command1')
### DB ###
@click.option('--status_bar', '-sb', default=True,type=bool, help="Enable/Disable the Status Bat")
#@click.option('--end_file_marker', '-efm', default=-1, help="Setup the end_file_marker for better matching the file end")
@click.option('--use_end_file_marker', '-uefm', default=False,type=bool, help="Enable/Disable usage of endfilemarker to change the couter unit from rows to files in the status bar")
@click.option('--tok_split_camel_case', '-tscc', default=True,type=bool, help="Enable/Disable the option for Tokenizer to convertion and split of the CamelCase (ex. 'CamelCase')")
@click.option('--make_backup', '-backup', default=True,type=bool, help="Enable/Disable making BackUp of the whole Corpus before the new Insetions")
@click.option('--lazyness_border', '-lb', default=50000, help="Set the number of the border, which ensure when exactly data collector should save data on the disk. If you have a big RAM than select the high number, to ensure the hight performance.")
@click.option('--rewrite', '-rw', default=False,type=bool, help="Enable/Disable rewrite option, which ensure the file replacing/rewriting during the export, if the same filename was found in the same directory.")
@click.option('--use_cash', '-uc', default=True,type=bool, help="Enable/Disable during the insertion process write direct on the disk or first into cash. It is a good performance booster, but just in the case of the big RAM.")
@click.option('--optimizer', '-opt', default="ljs", help="Enable/Disable DB Optimizer, which makes current DB much faster, but less safety.")
@click.option('--optimizer_page_size', '-optps', default=4096, help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_cache_size', '-optcs', default=1024000, help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_locking_mode', '-optlm', default="exclusive", type=click.Choice(DBHandler.non_mapped_states["locking_mode"]), help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.") #, type=click.Choice(['md5', 'sha1'])
@click.option('--optimizer_synchronous', '-optsyn', default="off", type=click.Choice(DBHandler.mapped_states["synchronous"].keys()+DBHandler.mapped_states["synchronous"].values()), help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_journal_mode', '-optjm', default="memory", type=click.Choice(DBHandler.non_mapped_states["journal_mode"]), help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_temp_store', '-optts', default="memory", type=click.Choice(DBHandler.mapped_states["temp_store"].keys()+DBHandler.mapped_states["temp_store"].values()), help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--gready', '-gr', default=False,type=bool, help="If False -> Stop Process immediately if error was returned. If True -> Try to execute script so long as possible, without stopping the main process.")


## Corp ####
@click.option('--corp_fname', '-cn', default=False, help="File Name of the CorpusDB (with or without extention)")
@click.option('--language', '-lang', default="False", help="Give language acronym according to standard ISO639_2.", type=click.Choice(CorpusData.tokenizer_for_languages.keys()+["False"]))
@click.option('--visibility', '-vis', default='False', help="Is that an intern or extern Corpus?", type=click.Choice(["extern", "intern", "False"]))
@click.option('--platform_name', '-platf', default=False)
@click.option('--encryption_key', '-encrkey', default=False, help="For encryption of the current DB please given an key. If key is not given, than the current DB will be not encrypted.")
@click.option('--corp_intern_dbname', '-cname', default=False, help="Intern Name of the DB, which will be saved as tag inside the DB.")
@click.option('--source', '-src', default=False, help="Source of the text collection.")
@click.option('--license', '-lic', default=False, help="License, under which this corpus will be used.")
@click.option('--template_name', '-templ', default='False', help="Templates are there for initialization of the preinitialized Document Table in the DB. Every Columns in the DocumentTable should be initialized. For this you can use Templates (which contain preinitialized Information)  or initialize manually those columns manually with the   '--cols_and_types_in_doc'-Option.", type=click.Choice(list(DBHandler.templates.keys())+["False"]))
@click.option('--version', '-ver', default=1, help="Version Number of the DB")
@click.option('--cols_and_types_in_doc', '-additcols', default=False, help="Additional Columns from input text Collections. Every Columns in the DocumentTable should be initialized. Every Document Table has already two default columns (id, text) if you want to insert also other columns, please define them here with the type names. The colnames should correspond to the colnames in the input text data and be given in the following form: 'colname1:coltype1,colname2:coltype2,colname3:coltype3' ")
@click.option('--corpus_id_to_init', '-cid', default=False, help="Manually given corpid")
@click.option('--tokenizer', '-tok', default='True', help="Select Tokenizer by name", type=click.Choice(list(CorpusData.supported_tokenizer)+["False", "True"]) ) 
@click.option('--pos_tagger', '-ptager', default='False', help="Select POS-Tagger by name", type=click.Choice(list(CorpusData.supported_pos_tagger)+["False", "True"]))
@click.option('--sentiment_analyzer', '-sentim', default='False', help="Select Sentiment Analyzer by name", type=click.Choice(list(CorpusData.supported_sentiment_analyzer)+["False", "True"]))
@click.option('--sent_splitter', '-sentspl', default='True', help="Select Stemmer by name", type=click.Choice(list(CorpusData.supported_stemmer)+["False", "True"]))
@click.option('--preprocession', '-preproc', default=True,type=bool, help="Enable/disable Proprocessing of the text elements.")
@click.option('--lang_classification', '-langclas', default=False, help="Enable/disable Language Classification")
@click.option('--del_url', '-durl', default=False,type=bool,  help="Enable/disable Hiding of all URLs")
@click.option('--del_punkt', '-dpnkt', default=False,type=bool,  help="Enable/disable Hiding of all Punctuation")
@click.option('--del_num', '-dnum', default=False,type=bool,  help="Enable/disable Hiding of all Numbers")
@click.option('--del_mention', '-dment', default=False,type=bool,  help="Enable/disable Hiding of all Mentions")
@click.option('--del_hashtag', '-dhash', default=False,type=bool,  help="Enable/disable Hiding of all Hashtags")
@click.option('--del_html', '-dhtml', default=False,type=bool,  help="Enable/disable cleaning of all  not needed html tags")
@click.option('--case_sensitiv', '-case', default=False,type=bool,  help="Enable/disable the case sensitivity in the Corpus during initialization.")
@click.option('--emojis_normalization', '-emojnorm', default=True,type=bool,  help="Enable/disable restructure of all Emojis. (could cost much time)")
@click.option('--text_field_name', '-texname', default="text", help="If new input data has different name with text or id information, than use this options to ensure correct use of data. ")
@click.option('--id_field_name', '-idname', default="id", help="If new input data has different name with text or id information, than use this options to ensure correct use of data. ")
@click.option('--heal_me_if_possible', '-heal', default=True,type=bool, help="If '--template_name' and  '--cols_and_types_in_doc' wasn't selected, than with this option ('--heal_me_if_possible') DB will try to initialize those information automatically. But be careful with this option, because it could also return unexpected  errors. ")


## Reader
@click.option('--path_to_read', '-ptr', default=False, help="Path to folder with text collection, which should be collected and transformed into CorpusDB.")
@click.option('--file_format_to_read', '-readtyp', default='False', help="File Format which should be read.", type=click.Choice(Reader.supported_file_types[:]+["False"]))
@click.option('--reader_regex_template', '-readregextempl', default='False', type=click.Choice(Reader.regex_templates.keys()+["False"] ), help="Name of the template for Reading of the TXT Files.")
@click.option('--reader_regex_for_fname', '-readregexpattern', default=False, help="Regex Pattern for Extraction of the Columns from the filenames.")
@click.option('--read_from_zip', '-zipread', default=False,type=bool, help="Enable/Disable the possibly also to search and read automatically from *.zip Achieves.")
@click.option('--formatter_name', '-formatter', default='False', type=click.Choice(["twitterstreamapi", "sifter", "False"]), help="Give the name of the predefined Formatters and Preprocessors for different text collections.")
@click.option('--reader_ignore_retweets', '-retweetsignr', default=True,type=bool, help="Ignore Retweets, if original JsonTweet was given.")
@click.option('--min_files_pro_stream', '-minfile', default=1000, help="The Limit, when Multiprocessing will be start to create a new stream.")
@click.option('--csvdelimiter', '-csvd', default=',', help="CSV Files has offten different dialects and delimiters. With this option, it is possible, to set an delimiter, which ensure correct processing of the CSV File Data. ")
@click.option('--encoding', '-enc', default="utf-8", help="All Text Files are encoded with help of the EncodingTables. If you input files are not unicode-compatible, please give the encoding name, which was used for encoding the input data. ", type=click.Choice(Reader.supported_encodings_types))


@click.option('--doc_id', '-docid', default=False, help="Document ID in the Corpus DB. ")
@click.option('--attr_name', '-attr', default=False, help="Stats and Corpus DBs has intern Attributes. For changing of getting them you need to get the name of this attribute. ")
@click.option('--value', '-val', default=False, help="For setting of the new Value for one Attribute.")
@click.option('--type_to_export', '-exptyp', default="False", help="FileType for the export function." , type=click.Choice(Reader.supported_file_types_to_export[:]+["False"]))
@click.option('--export_dir', '-expdir', default=False, help="Directory where Exports will be saved. If False, than they will be saved in the default ProjectDirectory.")
@click.option('--export_name', '-expname', default=False, help="FileName for ExportData." )
@click.option('--rows_limit_in_file', '-rowlim', default=50000, help="Number of the Rows Max in the Files to export." )


@click.option('--stream_number', '-sn', default=1, help="Enable or Disable the Multiprocessing. If Number > 1, than tool try to compute every thing parallel. This function could bring much better performance on the PC with multi cores and big Operation Memory.")
@click.option('--mode', '-m', default="prod" ,help="Set one of the Tool Modus. Modi ensure the communication behavior of this Tool.", type=click.Choice(helpers.modi))
@click.option('--logdir', '-ld', default="logs", help="Choose the name of the Directory for log data.")
def corpora(command1,
            status_bar,  use_end_file_marker, tok_split_camel_case, make_backup, lazyness_border, 
            rewrite, use_cash, optimizer, optimizer_page_size, 
            optimizer_cache_size, optimizer_locking_mode, optimizer_synchronous, optimizer_journal_mode, optimizer_temp_store,gready,
            
            corp_fname,language, visibility, platform_name,encryption_key, corp_intern_dbname,source,  license, 
            template_name, version,cols_and_types_in_doc,corpus_id_to_init,
            tokenizer, pos_tagger, sentiment_analyzer, sent_splitter, preprocession, lang_classification, del_url, del_punkt, 
            del_num, del_mention, del_hashtag, del_html, case_sensitiv, emojis_normalization, text_field_name, id_field_name,
            heal_me_if_possible, 

            path_to_read, file_format_to_read, reader_regex_template, reader_regex_for_fname, read_from_zip, 
            formatter_name, reader_ignore_retweets,min_files_pro_stream, csvdelimiter,encoding,

            stream_number, value, attr_name,type_to_export, export_dir, export_name,doc_id,rows_limit_in_file,

            mode,logdir ):
    # $ zas-vot-tools strat1 sets/train_set sets/eval_set  segments voiceless voiced vlwindow vcwindow experiments
    
    #p(template_name, "template_name")
    #if configer.
    formatter_name = strtobool(formatter_name)
    path_to_read = strtobool(path_to_read)
    file_format_to_read = strtobool(file_format_to_read)
    corp_intern_dbname = strtobool(corp_intern_dbname)
    visibility = strtobool(visibility)
    platform_name =  strtobool(platform_name)
    optimizer = strtobool(optimizer)
    cols_and_types_in_doc = strtobool(cols_and_types_in_doc) 
    corpus_id_to_init = strtobool(corpus_id_to_init)
    tokenizer = strtobool(tokenizer)
    pos_tagger = strtobool(pos_tagger)
    sentiment_analyzer = strtobool(sentiment_analyzer)
    sent_splitter = strtobool(sent_splitter)
    lang_classification = strtobool(lang_classification)
    template_name = strtobool(template_name)
    reader_regex_template = strtobool(reader_regex_template)
    type_to_export = strtobool(type_to_export)
    language = strtobool(language)
    doc_id = strtobool(doc_id)
    status_bar = strtobool(status_bar)


    try:
        doc_id = doc_id.strip("'") if doc_id and doc_id[0] == ["'"] else doc_id.strip('"')
    except:
        pass

    text_field_name=text_field_name.strip("'") if text_field_name[0] == "'" else text_field_name.strip('"')
    id_field_name=text_field_name.strip("'") if id_field_name[0] == "'" else id_field_name.strip('"')


    logger = get_cli_logger(mode,logdir)
    func_name = "corpora"
    #p(command,"command")
    if command1 not in supported_commands[func_name]:
        logger.error(" Given Command ('{}') is illegal for '{}'. Please use one of the following commands: '{}' ".format(command1,func_name,supported_commands[func_name] ))
        return False


    if command1 == "add":
        if not path_to_read or not file_format_to_read:
            logger.error("ObligatoryMetaDataForReaderMissing: If you want to add new Corpus, you need first give location to the raw text collection, from which than a new corpus will be created and also the file_type of those input text elements. For doing that please use following options: ['path_to_read', 'file_format_to_read']\n For example: 'zas-rep-tools corpora add --path_to_read . --file_format_to_read json'. ")
            return False

        if not corp_intern_dbname or not language or not  visibility or not  platform_name:
            logger.error("ObligatoryMetaDataForCorpusMissing: If you want to add new Corpus, you need to set also following obligatory meta data: ['corp_fname', 'language',  'visibility', 'platform_name']\n For example: 'zas-rep-tools corpora add --corp_intern_dbname streamed --language de  --visibility intern --platform_name twitter'. ")
            return False


        if file_format_to_read == "json":
            if not formatter_name:
                logger.warning("If you want to create TwitterCorpus from original TwitterJSON, than set following Option:  '--formatter_name twitterstreamapi'. Otherwise ignore this warning.  ")

        if file_format_to_read == "csv":
            if not formatter_name:
                logger.warning("If you want to create TwitterCorpus from Sifter-CSV-Files, than set following Option:  '--formatter_name sifter'. Otherwise ignore this warning.  ")


        ### Option preprocession 
        stop_process_if_possible = False if gready else True
        if cols_and_types_in_doc:
            cols_and_types_in_doc = cols_and_types_in_doc.strip("'") if cols_and_types_in_doc[0] == "'" else cols_and_types_in_doc.strip('"')
            cols_and_types_in_doc = cols_and_types_in_doc.split(",")
            temp_cols_and_types_in_doc = []
            for item in cols_and_types_in_doc:
                if item:
                    splitted = item.split(":")

                    if len(splitted) == 2:
                        temp_cols_and_types_in_doc.append((splitted[0],splitted[1]))

                    else:
                        logger.error("Given '--cols_and_types_in_doc' is incomplete or invalid. Please give this without white spaces in the following form 'colname1:coltype1,colname2:coltype2,colname3:coltype3' ")
                        return False
                else:
                    logger.error("Given '--cols_and_types_in_doc' is incomplete or invalid. Please give this without white spaces in the following form 'colname1:coltype1,colname2:coltype2,colname3:coltype3' ")
                    return False

            cols_and_types_in_doc = temp_cols_and_types_in_doc
        #p(cols_and_types_in_doc, "cols_and_types_in_doc")
        #p(reader_regex_for_fname, "reader_regex_for_fname")
        try:
            reader_regex_for_fname = reader_regex_for_fname.strip("'") if reader_regex_for_fname[0] == "'" else reader_regex_for_fname.strip('"')
        except:
            pass

        ### Main Part of the Script
        reader = Reader(path_to_read, file_format_to_read,  regex_template=reader_regex_template,
                        regex_for_fname=reader_regex_for_fname, read_from_zip=read_from_zip,
                        end_file_marker = end_file_marker, send_end_file_marker=use_end_file_marker, stop_process_if_possible=stop_process_if_possible,
                        formatter_name=formatter_name, text_field_name = text_field_name, id_field_name=id_field_name,
                        ignore_retweets=reader_ignore_retweets, mode=mode)
        if reader._get_number_of_left_over_files() == 0:
            logger.error("No one file was found in the given path ('{}'). Please check the correctness of the given path or  give other (correct one) path to the text data. If you want to search also in zips, than set following option: '--read_from_zip True'".format(reader._inp_path))
            return False
        stop_if_db_already_exist = False if rewrite else True
        corp = Corpus(mode=mode, error_tracking=answer_error_tracking, status_bar=status_bar,
                end_file_marker=end_file_marker, use_end_file_marker=use_end_file_marker, tok_split_camel_case=tok_split_camel_case,
                make_backup=make_backup, lazyness_border=lazyness_border, thread_safe=True, rewrite=rewrite, stop_if_db_already_exist=stop_if_db_already_exist,
                use_cash=use_cash, optimizer=optimizer,optimizer_page_size=optimizer_page_size, 
                optimizer_cache_size=optimizer_cache_size, optimizer_locking_mode=optimizer_locking_mode, optimizer_synchronous=optimizer_synchronous,
                optimizer_journal_mode=optimizer_journal_mode, optimizer_temp_store=optimizer_temp_store,stop_process_if_possible=stop_process_if_possible,
                heal_me_if_possible=heal_me_if_possible)
                

        #p((text_field_name, id_field_name), c="m")
        

        corp.init(main_folders["corp"], corp_intern_dbname, language,  visibility, platform_name,
                    encryption_key=encryption_key, fileName=corp_fname, source=source, license=license,
                    template_name=template_name, version=version, cols_and_types_in_doc=cols_and_types_in_doc,
                    corpus_id=corpus_id_to_init, text_field_name=text_field_name,id_field_name=id_field_name,
                    tokenizer=tokenizer,pos_tagger=pos_tagger,sentiment_analyzer=sentiment_analyzer,
                    sent_splitter=sent_splitter,preprocession=preprocession, lang_classification=lang_classification,
                    del_url=del_url,del_punkt=del_punkt,del_num=del_num,del_mention=del_mention,del_hashtag=del_hashtag,del_html=del_html,
                    case_sensitiv=case_sensitiv, emojis_normalization=emojis_normalization)
        
        #csvdelimiter,encoding,
        csvdelimiter = csvdelimiter.strip("'") if csvdelimiter[0] == "'" else csvdelimiter.strip('"')
        status = corp.insert(reader.getlazy(stream_number=stream_number,min_files_pro_stream=min_files_pro_stream,csvdelimiter=csvdelimiter,encoding=encoding),  create_def_indexes=True)
        
        if not status or corp.corpdb.rownum("documents") == 0:
            corp_fname = corp.corpdb.fname()
            #corp.corpdb.commit()
            #import shutil
            
            corp._close()
            os.remove(os.path.join(main_folders["corp"],corp_fname))
            logger.info("InsertionProecess into '{}'-CorpDB is failed. Corpus was deleted.".format(corp_fname))
        else:
            corp.corpdb.commit()
            corp.close()




    elif command1 == "del":
        if not corp_fname:
            logger.error("'--corp_fname' is not given. (you can also give tag 'all' instead of the corp_fname)")
        if corp_fname == "all":
            #os.remove()
            shutil.rmtree(main_folders["corp"], ignore_errors=True)
            logger.info("All CorpDB was removed.")
        else:
            files = get_corp_fname(main_folders)
            if corp_fname in files:
                os.remove(os.path.join(main_folders["corp"], corp_fname))
                logger.info("'{}'-CorpDB was removed".format(corp_fname))
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                os.remove(os.path.join(main_folders["corp"], corp_fname)+".db")
                logger.info("'{}'-CorpDB was removed".format(corp_fname))
            else:
                logger.error("Given fname ('{}') wasn't found and can not be removed.".format(corp_fname))
                return False


    elif command1 == "clean_dir":
        #if not corp_fname:
        #    logger.error("'--corp_fname' is not given. (you can also give tag 'all' instead of the corp_fname)")
        #if corp_fname == "all":
        files = get_corp_fname(main_folders)
        validated,possibly_encrypted,wrong,opened_db = validate_corp(main_folders,files)
        deleted = []
        for temp_dbname in validated:
            corp = Corpus(mode="blind")
            corp.open(os.path.join(main_folders["corp"], temp_dbname))
            
            if corp.corpdb:
                if corp.corpdb.get_attr("locked"):
                    deleted.append(temp_dbname)
                    os.remove(os.path.join(main_folders["corp"], temp_dbname))

        files = os.listdir(main_folders["corp"])
        for journal_fname in [fname for fname in files if".db-journal" in fname]:
            #deleted.append(temp_dbname)
            os.remove(os.path.join(main_folders["stats"], journal_fname))

        if deleted:
            print " Following not finished and locked CorpDBs was deleted:"
            for dn in deleted:
                print "   |-> '{}';".format(dn)
            return True
        else:
            print " Locked or not finished CorpDBs wasn't found."
            return False


    elif command1 == "names":
        files = get_corp_fname(main_folders)
        validated,possibly_encrypted,wrong,opened_db = validate_corp(main_folders,files)
        print ">>> {} DBs was found <<<  ".format(len(files))
        print " '{}'-From them was validated:".format(len(validated))
        for i, fname in enumerate(validated):
            print "       {}. '{}';".format(i, fname)
        if possibly_encrypted:
            print "\n  '{}'-From them are possibly encrypted/damaged/invalid:".format(len(possibly_encrypted))
            for i, fname in enumerate(possibly_encrypted):
                print "       {}. '{}';".format(i, fname)

        #p(files)

    elif command1 == "meta":
        if not corp_fname:
            logger.error("'--corp_fname' is not given. (you can also give tag 'all' instead of the corp_fname)")
            return False

        files = get_corp_fname(main_folders)
        validated,possibly_encrypted,wrong,opened_db = validate_corp(main_folders,files)
        if corp_fname == "all":
            for db in opened_db:
                print("\n >>>> {} <<<<".format(db.fname()))
                for k,v in db.get_all_attr().items():
                    print "    {} = '{}';".format(k,v)


            print "\n\nNotice! with 'all'-Argument could be checked just not-encrypted DBs. If you want to check encrypted DB use additional to corp_fname also  '--encryption_key'"

        else:
            if corp_fname in files:
                if corp_fname in validated:
                    ix = validated.index(corp_fname)
                    db = opened_db[ix]
                    print("\n >>>> {} <<<<".format(db.fname()))
                    for k,v in db.get_all_attr().items():
                        print "    {} = '{}';".format(k,v)
                elif corp_fname in possibly_encrypted:
                    if not encryption_key:
                        logger.error("Current DBFile is possibly encrypted/damaged. Please use '--encryption_key'-Option to decrypt it. ")
                        return False
                    else:
                        h = DBHandler(mode="blind")
                        h.connect(os.path.join(main_folders["corp"],corp_fname),encryption_key=encryption_key)
                        try:
                            if h.typ() == "corpus":
                                print("\n >>>> {} <<<<".format(h.fname()))
                                for k,v in h.get_all_attr().items():
                                    print "    {} = '{}';".format(k,v)
                            else:
                                logger.error("'{}'-DB is not an CorpusDB or given encryption key ('{}') is wrong. ".format(corp_fname,encryption_key))
                                return False
                        except:
                            logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                            return False
                
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                spl1 = [os.path.splitext(fname)[0] for fname in validated]
                spl2 = [os.path.splitext(fname)[0] for fname in possibly_encrypted]
                if corp_fname in spl1:
                    ix = spl1.index(corp_fname)
                    db = opened_db[ix]
                    print("\n >>>> {} <<<<".format(db.fname()))
                    for k,v in db.get_all_attr().items():
                        print "    {} = '{}';".format(k,v)
                
                elif corp_fname in spl2:
                    if not encryption_key:
                        logger.error("Current DBFile is possibly encrypted/damaged. Please use '--encryption_key'-Option to decrypt it. ")
                    else:
                        h = DBHandler(mode="blind")
                        h.connect(os.path.join(main_folders["corp"],corp_fname)+".db",encryption_key=encryption_key)
                        try:
                            if h.typ() == "corpus":
                                print("\n >>>> {} <<<<".format(h.fname()))
                                for k,v in h.get_all_attr().items():
                                    print "    {} = '{}';".format(k,v)
                            else:
                                logger.error("'{}'-DB is not an CorpusDB or given encryption key ('{}') is wrong. ".format(corp_fname,encryption_key))
                                return False
                        except:
                            logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                            return False


                else:
                    logger.error("Given fname ('{}') wasn't validated. It means, that possibly it is not a CorpusDB or it is just encrypted!".format(corp_fname))
                    return False
            else:
                logger.error("Given fname ('{}') wasn't found!".format(corp_fname))
                return False


    elif command1 == "basic_stats":
        if not corp_fname:
            logger.error("'--corp_fname' is not given. (you can also give tag 'all' instead of the corp_fname)")
            return False

        files = get_corp_fname(main_folders)
        validated,possibly_encrypted,wrong,opened_db = validate_corp(main_folders,files)
        if corp_fname == "all":
            for db in opened_db:
                print("\n >>>> {} <<<<".format(db.fname()))
                print "    doc_num = '{}';".format(db.get_attr("doc_num"))
                print "    sent_num = '{}';".format(db.get_attr("sent_num"))
                print "    token_num = '{}';".format(db.get_attr("token_num"))

            print "\n\nNotice! with 'all'-Argument could be checked just not-encrypted DBs. If you want to check encrypted DB use additional to corp_fname also  '--encryption_key'"

        else:
            if corp_fname in files:
                if corp_fname in validated:
                    ix = validated.index(corp_fname)
                    db = opened_db[ix]
                    print("\n >>>> {} <<<<".format(db.fname()))
                    print "    doc_num = '{}';".format(db.get_attr("doc_num"))
                    print "    sent_num = '{}';".format(db.get_attr("sent_num"))
                    print "    token_num = '{}';".format(db.get_attr("token_num"))
                elif corp_fname in possibly_encrypted:
                    if not encryption_key:
                        logger.error("Current DBFile is possibly encrypted/damaged. Please use '--encryption_key'-Option to decrypt it. ")
                    else:
                        h = DBHandler(mode="blind")
                        h.connect(os.path.join(main_folders["corp"],corp_fname),encryption_key=encryption_key)
                        try:
                            if h.typ() == "corpus":
                                print("\n >>>> {} <<<<".format(h.fname()))
                                print "    doc_num = '{}';".format(h.get_attr("doc_num"))
                                print "    sent_num = '{}';".format(h.get_attr("sent_num"))
                                print "    token_num = '{}';".format(h.get_attr("token_num"))
                            else:
                                logger.error("'{}'-DB is not an CorpusDB or given encryption key ('{}') is wrong. ".format(corp_fname,encryption_key))
                                return False
                        except:
                            logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                            return False
                
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                spl1 = [os.path.splitext(fname)[0] for fname in validated]
                spl2 = [os.path.splitext(fname)[0] for fname in possibly_encrypted]
                if corp_fname in spl1:
                    ix = spl1.index(corp_fname)
                    db = opened_db[ix]
                    print("\n >>>> {} <<<<".format(db.fname()))
                    print "    doc_num = '{}';".format(db.get_attr("doc_num"))
                    print "    sent_num = '{}';".format(db.get_attr("sent_num"))
                    print "    token_num = '{}';".format(db.get_attr("token_num"))
                
                elif corp_fname in spl2:
                    if not encryption_key:
                        logger.error("Current DBFile is possibly encrypted/damaged. Please use '--encryption_key'-Option to decrypt it. ")
                    else:
                        h = DBHandler(mode="blind")
                        h.connect(os.path.join(main_folders["corp"],corp_fname)+".db",encryption_key=encryption_key)
                        try:
                            if h.typ() == "corpus":
                                print("\n >>>> {} <<<<".format(h.fname()))
                                print "    doc_num = '{}';".format(h.get_attr("doc_num"))
                                print "    sent_num = '{}';".format(h.get_attr("sent_num"))
                                print "    token_num = '{}';".format(h.get_attr("token_num"))
                            else:
                                logger.error("'{}'-DB is not an CorpusDB or given encryption key ('{}') is wrong. ".format(corp_fname,encryption_key))
                                return False
                        except:
                            logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                            return False


                else:
                    logger.error("Given fname ('{}') wasn't validated. It means, that possibly it is not a CorpusDB or it is just encrypted!".format(corp_fname))
                    return False
            else:
                logger.error("Given fname ('{}') wasn't found!".format(corp_fname))
                return False


    elif command1 == "update_attr":
        if not corp_fname or  not attr_name or not value:
            logger.error("Command is incomplete: '--corp_fname' or '--attr_name' or '--value' is not given.")
        else:
            files = get_corp_fname(main_folders)
            if corp_fname in files:
                pass
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                corp_fname = corp_fname+".db"
            else:
                logger.error("Given fname ('{}') wasn't found and can not be removed.".format(corp_fname))
                return False
            
            try:
                db = DBHandler(mode="error")
                db.connect(os.path.join(main_folders["corp"],corp_fname),encryption_key=encryption_key)
                if db._db:
                    if db.typ() == "corpus":
                        if attr_name not in db.get_all_attr():
                            logger.error("Given Attribute ('{}') is not exist in this DataBase.".format(attr_name))
                            return False

                        db.update_attr(attr_name,value)
                        db._commit()
                        updated_attr = db.get_attr(attr_name)
                        #p((updated_attr, value))
                        if str(value) != str(updated_attr):
                            logger.error("Update of the given Attribute ('{}') failed.".format(attr_name))
                            return 
                        else:
                            logger.info("Given Attribute ('{}') in the '{}'-DB was updated to '{}'.".format(attr_name,corp_fname, value))
                            return True
                    else:
                        logger.error("'{}'-DB is not an CorpusDB or given encryption key ('{}') is wrong. ".format(corp_fname,encryption_key))
                        return False
                else:
                    #p(type(strtobool(encryption_key)), "strtobool(encryption_key)")
                    if strtobool(encryption_key):
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                    else:
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                    return False
            except:
                if strtobool(encryption_key):
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                else:
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                return False

    elif command1 == "export":
        if not corp_fname or  not type_to_export:
            logger.error("Command is incomplete:   '--corp_fname' or '--type_to_export'  is not given.")
            return False
        else:
            files = get_corp_fname(main_folders)
            export_dir = export_dir if export_dir else main_folders["export"]
            export_name = export_name if export_name else "Export{}".format(int(time.time()))
            if corp_fname in files:
                pass
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                corp_fname = corp_fname+".db"
            else:
                logger.error("Given fname ('{}') wasn't found and can not be removed.".format(corp_fname))
                return False

            corp = Corpus(mode="error")
            corp.open(os.path.join(main_folders["corp"],corp_fname),encryption_key=encryption_key)

            def intern_getter():
                if status_bar:
                    status_bars_manager = _get_status_bars_manager()
                    status_bar_start = _get_new_status_bar(None, status_bars_manager.term.center("Exporter") , "", counter_format=status_bars_manager.term.bold_white_on_green("{fill}{desc}{fill}"),status_bars_manager=status_bars_manager)
                    status_bar_start.refresh()
                #if status_bar:
                    status_bar_current = _get_new_status_bar(num, "Exporting:", "row",status_bars_manager=status_bars_manager)
                
                for item in corp.docs(output="dict"):
                    if status_bar:
                        status_bar_current.update(incr=1)
                    yield item

                if status_bar:
                    status_bar_total_summary = _get_new_status_bar(None, status_bars_manager.term.center("Exported:  Rows: '{}'; ".format(num) ), "",  counter_format=status_bars_manager.term.bold_white_on_green('{fill}{desc}{fill}\n'),status_bars_manager=status_bars_manager)
                    status_bar_total_summary.refresh()
                    status_bars_manager.stop()


            if corp.corpdb._db:
                num = corp.corpdb.rownum("documents")
                exporter = Exporter(intern_getter(),rewrite=False,silent_ignore=False , mode=mode)
                if type_to_export not in Exporter.supported_file_formats:
                    logger.error("Given Export Type ('{}') is not supported.".format(type_to_export))
                    return False
 
                if type_to_export == "csv":
                    #p(cols,"cols")
                    cols = corp.corpdb.col("documents")
                    exporter.tocsv(export_dir, export_name, cols, rows_limit_in_file=rows_limit_in_file)
                elif type_to_export == "xml":
                    exporter.toxml(export_dir, export_name, rows_limit_in_file=rows_limit_in_file)
                elif type_to_export == "json":
                    exporter.tojson(export_dir, export_name, rows_limit_in_file=rows_limit_in_file)
                else:
                    logger.error("Given Export Type ('{}') is not supported.".format(type_to_export))
                    return False


            else:
                #p(type(strtobool(encryption_key)), "strtobool(encryption_key)")
                if strtobool(encryption_key):
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is locked or damaged or given  encryption key ('{}') is wrong. ".format(corp_fname,encryption_key))
                else:
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                return False


    elif command1 == "used_tools":
        term = Terminal()
        for tool_name, data in CorpusData.info.items():
            print "\n\n\n\n"
            print term.bold_white_on_magenta("   >>>>>  {}  <<<<< ".format(tool_name))
            if tool_name == "tagger":
                for tagger_name, infos in data.items():
                    print term.bold_white_on_cyan("      TaggerName:  {}  ".format(tagger_name))
                    print "\t\t"+json.dumps(CorpusData.info[tool_name][tagger_name], sort_keys=True, indent=5).replace("\n", "\n\t")
                    print "\n\n"
            else:
                print "\t"+json.dumps(CorpusData.info[tool_name], sort_keys=True, indent=5).replace("\n", "\n\t")

    elif command1 == "cols":
        if not corp_fname :
            logger.error("Command is incomplete: '--corp_fname' is not given.")
        else:
            files = get_corp_fname(main_folders)
            if corp_fname in files:
                pass
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                corp_fname = corp_fname+".db"
            else:
                logger.error("Given fname ('{}') wasn't found and can not be removed.".format(corp_fname))
                return False
            
            try:
                db = DBHandler(mode="error")
                db.connect(os.path.join(main_folders["corp"],corp_fname),encryption_key=encryption_key)
                if db._db:
                    if db.typ() == "corpus":
                        print " Columns in the DocumentTable for  {} :".format(db.fname())
                        i =  0
                        temp = []
                        for col in db.col("documents"):
                            i += 1
                            if i < 4:
                                temp.append(col)
                            else:
                                print "   {}".format(temp)
                                temp = []
                                i = 0
                        if temp:     
                            print "   {}".format(temp)

                    else:
                        logger.error("'{}'-DB is not an CorpusDB or given encryption key ('{}') is wrong. ".format(corp_fname,encryption_key))
                        return False
                else:
                    #p(type(strtobool(encryption_key)), "strtobool(encryption_key)")
                    if strtobool(encryption_key):
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                    else:
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                    return False
            except:
                if strtobool(encryption_key):
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                else:
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                return False

    elif command1 == "doc":
        if not corp_fname  or not doc_id:
            logger.error("Command is incomplete: '--corp_fname' , '--doc_id' is not given.")
            return False
        else:
            files = get_corp_fname(main_folders)
            if corp_fname in files:
                pass
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                corp_fname = corp_fname+".db"
            else:
                logger.error("Given fname ('{}') wasn't found and can not be removed.".format(corp_fname))
                return False
            
            try:
                corp = Corpus(mode="error")
                corp.open(os.path.join(main_folders["corp"],corp_fname),encryption_key=encryption_key)
                if corp.corpdb:
                    #p(corp._id_field_name, "corp._id_field_name")
                    getted_docs =  list(corp.docs( where="{}='{}'".format(corp._id_field_name, doc_id), output="dict"))
                    #p(getted_docs, "getted_docs")
                    
                    print "\n >>> {} <<< :".format(corp.corpdb.fname())
                    print " (Matched DocItems for doc_id: '{}') ".format(doc_id)
                    if getted_docs:
                        
                        for i, doc_item in enumerate(getted_docs):
                            if i > 0:
                                print "\n"
                            if doc_item:
                                for k,v in doc_item.items():
                                    print "    {} : {}".format(k,repr(v))
                    else:
                        print "\n     !!!!NO ONE DOC WAS FOUND FOR GIVEN DOCID!!!"

                else:
                    #p(type(strtobool(encryption_key)), "strtobool(encryption_key)")
                    if strtobool(encryption_key):
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                    else:
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                    return False
            except:
                if strtobool(encryption_key):
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                else:
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                return False
    elif command1 == "ids":
        if not corp_fname  :
            logger.error("Command is incomplete: '--corp_fname' is not given.")
            return False
        else:
            files = get_corp_fname(main_folders)
            if corp_fname in files:
                pass
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                corp_fname = corp_fname+".db"
            else:
                logger.error("Given fname ('{}') wasn't found and can not be removed.".format(corp_fname))
                return False
            
            try:
                corp = Corpus(mode="error")
                corp.open(os.path.join(main_folders["corp"],corp_fname),encryption_key=encryption_key)
                if corp.corpdb:
                    #p(corp._id_field_name, "corp._id_field_name")
                    ids = [item[0] for item in corp.docs(columns=corp._id_field_name)]
                    print " IDs in the DocumentTable for  {} :".format(corp.corpdb.fname())
                    print ids
                    # i =  0
                    # temp = []
                    # for col in ids:
                    #     i += 1
                    #     if i < 5:
                    #         temp.append(col)
                    #     else:
                    #         temp_str = ""
                    #         for id_item in temp:
                    #             temp_str += "{}, ".format(id_item)
                    #         print " {}".format(temp_str)
                    #         temp = []
                    #         i = 0

                else:
                    #p(type(strtobool(encryption_key)), "strtobool(encryption_key)")
                    if strtobool(encryption_key):
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                    else:
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                    return False
            except:
                if strtobool(encryption_key):
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(corp_fname,encryption_key))
                else:
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(corp_fname,encryption_key))
                return False

#"stats": ["compute", "recompute", "optimize", "recreate_indexes", "del", "names", "meta", "basic_stats", "update_attr", "export", ],



@main.command('stats')
@click.argument('command1')
### DB ###
@click.option('--status_bar', '-sb', default=True,type=bool, help="Enable/Disable the Status Bat")
@click.option('--use_end_file_marker', '-uefm', default=False,type=bool, help="Enable/Disable usage of endfilemarker to change the couter unit from rows to files in the status bar")
@click.option('--make_backup', '-backup', default=True,type=bool, help="Enable/Disable making BackUp of the whole Corpus before the new Insetions")
@click.option('--lazyness_border', '-lb', default=50000, help="Set the number of the border, which ensure when exactly data collector should save data on the disk. If you have a big RAM than select the high number, to ensure the hight performance.")
@click.option('--rewrite', '-rw', default=False,type=bool, help="Enable/Disable rewrite option, which ensure the file replacing/rewriting during the export, if the same filename was found in the same directory.")
@click.option('--use_cash', '-uc', default=True,type=bool, help="Enable/Disable during the insertion process write direct on the disk or first into cash. It is a good performance booster, but just in the case of the big RAM.")
#@click.option('--optimizer', '-opt', default=False, help="Enable/Disable DB Optimizer, which makes current DB much faster, but less safety. See more: https://www.sqlite.org/pragma.html")
@click.option('--optimizer', '-opt', default="ljs", help="Enable/Disable DB Optimizer, which makes current DB much faster, but less safety. See more: https://www.sqlite.org/pragma.html")
@click.option('--optimizer_page_size', '-optps', default=4096, help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_cache_size', '-optcs', default=1024000, help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_locking_mode', '-optlm', default="exclusive", type=click.Choice(DBHandler.non_mapped_states["locking_mode"]), help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_synchronous', '-optsyn', default="off", type=click.Choice(DBHandler.mapped_states["synchronous"].keys()+DBHandler.mapped_states["synchronous"].values()), help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_journal_mode', '-optjm', default="memory", type=click.Choice(DBHandler.non_mapped_states["journal_mode"]), help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--optimizer_temp_store', '-optts', default="memory", type=click.Choice(DBHandler.mapped_states["temp_store"].keys()+DBHandler.mapped_states["temp_store"].values()), help="Setting for DBOptimizer. See more in the Hell-text for  optimizer.")
@click.option('--gready', '-gr', default=False,type=bool, help="If False -> Stop Process immediately if error was returned. If True -> Try to execute script so long as possible, without stopping the main process.")



## Stats ####
@click.option('--corp_fname', '-cn', default=False, help="File Name of the CorpusDB (with or without extention)")
@click.option('--stream_number','-sn', default=1, help="Enable or Disable the Multiprocessing. If Number > 1, than tool try to compute every thing parallel. This function could bring much better performance on the PC with multi cores and big Operation Memory.")
@click.option('--create_indexes', '-crtix', default=True,type=bool, help="For better performance it is highly recommended to create indexes. But their creation could also cost time  once during their creation and also space.")
@click.option('--freeze_db', '-freeze', default=True,type=bool, help="Freeze current DB and close for all next possible insertion of the new data. This option also triggers the DB Optimization Porcess, which could cost a lost of time, but make this DB much space and time efficient. Once this process is done, it is not possible anymore to decline it.")
@click.option('--optimized_for_long_syntagmas', '-optlongsyn', default=True,type=bool, help="If you are planing to search in the big syntagmas, than set this to True. It will optimize DB to be fast with long syntagmas.")
@click.option('--min_files_pro_stream', '-minfile', default=1000, help="The Limit, when Multiprocessing will be start to create a new stream.")
@click.option('--baseline_delimiter', '-basdelim', default="|+|", help="Delimiter for Syntagmas in intern Baseline Table. Change here if you really know, that you need it.")


@click.option('--stats_fname', '-sfn', default=False, help="File Name of the StatsDB.")
@click.option('--visibility', '-vis', default="False", help="Is that an intern or extern Corpus?", type=click.Choice(["extern", "intern", "False"]))
@click.option('--encryption_key', '-encrkey', default=False, help="For encryption of the current DB please given an key. If key is not given, than the current DB will be not encrypted.")
@click.option('--version', '-ver', default=1, help="Version Number of the DB")
@click.option('--stats_id', '-stats_id', default=False, help="Possibilty to set StatsId manually. Otherwise it will be setted automatically.")
@click.option('--stats_intern_dbname', '-cname', default=False, help="Intern Name of the DB, which will be saved as tag inside the DB.")
@click.option('--context_lenght', '-conlen', default=5, help="This number mean how much tokens left and right will be also captured and saved for each found re(du)plication. This number should be >=3")
@click.option('--full_repetativ_syntagma', '-fullrep', default=True,type=bool, help="Disable/Enable FullRepetativnes. If it is True, than just full repetativ syntagmas would be considered.  FullRepetativ syntagma is those one, where all words was ongoing either replicated or replicated. (ex.: FullRepRedu: 'klitze klitze kleine kleine' , FullRepRepl: 'kliiitzeee kleeeinee') (See more about it in Readme -> Definitions) ")
@click.option('--repl_up', '-ru', default=3, help="Up this number this tool recognize repetativ letter as replication.")
@click.option('--ignore_hashtag', '-ignht', default=False,type=bool, help="Enable/disable Hiding of all Hashtags, if it wasn't done during CorpusCreationProcess.")
@click.option('--case_sensitiv','-case', default=False,type=bool,  help="Enable/disable the case sensitivity during Stats Computation Process.")
@click.option('--ignore_url', '-ignurl', default=False,type=bool, help="Enable/disable Hiding of all URLS, if it wasn't done during CorpusCreationProcess.")
@click.option('--ignore_mention', '-ignment', default=False,type=bool, help="Enable/disable Hiding of all Mentions, if it wasn't done during CorpusCreationProcess.")
@click.option('--ignore_punkt', '-ignp', default=False,type=bool, help="Enable/disable Hiding of all Punctuation, if it wasn't done during CorpusCreationProcess.")
@click.option('--ignore_num', '-ignnum', default=False,type=bool, help="Enable/disable Hiding of all Numbers, if it wasn't done during CorpusCreationProcess.")
@click.option('--baseline_insertion_border', '-bliti', default=1000000, help="Number of the limit, when syntagmas will be delete from cash and saved on the disk.")

## Export
@click.option('--export_dir', '-expdir', default=False, help="Set Path to export dir. If it is not given, than all export will be saved into ProjectFolder.")
@click.option('--export_name', '-exp_fname', default=False, help="Set fname for export files.")
@click.option('--syntagma_for_export', '-syn', default="*", help="Set Syntagmas for search/extract. Default: '*'-match all syntagmas. Example: 'very|huge|highly,pitty|hard|happy,man|woman|boy|person' ('|' - as delimiter in paradigm; ',' - as delimiter of the syntagmas part.)  Notice: Now white space is allow.")
@click.option('--exp_repl', '-repl', default=False,type=bool, help="Disable/Enable Replications Extraction ")
@click.option('--exp_redu', '-redu', default=False,type=bool, help="Disable/Enable Reduplications Extraction ")
@click.option('--exp_syntagma_typ', '-styp', default="lexem", help="Ensure type of the given components in Syntagma_to_search. It is possible to search in pos-tags or in lexems.", type=click.Choice(["pos", "lexem"]))
@click.option('--exp_sentiment', '-sent', default="False", help="Search in Sentiment tagged data.",  type=click.Choice(["neutral", "positive","negative", "False"]))
@click.option('--export_file_type', '-ftyp', default="csv", type=click.Choice(['csv', 'json', "xml"]))
@click.option('--rows_limit_in_file', '-rowlim', default=50000, help="Number of the Rows Max in the Files to export." )
@click.option('--encryption_key_corp', '-exp_encrkey', default=False, help="For export additional columns (--additional_doc_cols) from encrypted CorpDB or for compution of the new StatsDb from the encrypted CorpDB")
@click.option('--output_table_type', '-ott', default="exhausted", type=click.Choice(["exhausted", "sum"]))
@click.option('--additional_doc_cols', '-doccols', default=False, help="For export of stats with additional columns from document from CorpDB. Don't forget to give also the FName of CorpusDB for which current statsDB was computed. (--corp_fname) Please give it in the following Form: 'gender,age,' (NO WHITE SPACES ARE ALLOW) ")
@click.option('--max_scope', '-mscope', default=False, help="Upper Limit of the syntagma length to search. Example: if max_scope = 1, than tool will search just in those syntagmas, which contain just 1 word.")
@click.option('--stemmed_search', '-stemm', default=False,type=bool, help="Search in lemantisated/stemmed syntagmas. Be careful and don't give different conjugations of one lemma, if current options is True.  Because you could get duplicates.")
@click.option('--context_len_left', '-conleft', default=True, help="The length of context In Output Tables. Could be also Disabled (False).")
@click.option('--context_len_right', '-conright', default=False,help="The length of context In Output Tables. Could be also Disabled (False).")
@click.option('--separator_syn', '-sepsyn', default=" || ", help="Separator inside syntagma in baseline.")
@click.option('--word_examples_sum_table', '-wordex', default=True,type=bool, help="Enable/disable Word Examples in Exported Output. (Just For SumOutputTables) ")
@click.option('--ignore_symbol', '-ignsym', default=False, help="Enable/disable Symbols in Exported Outputs. (Just For SumOutputTables)")




@click.option('--recompute_flag', '-recflag', default=None,help="For 'recompute' command. This command recompute the FullRepetativnes in given StatsDB. True - full_repetativnes, False - no_full_repetativnes/all_syntagmas ")
@click.option('--attr_name', '-attr', default=False, help="Stats and Corpus DBs has intern Attributes. For changing of getting them you need to get the name of this attribute. ")
@click.option('--value', '-val', default=False, help="For setting of the new Value for one Attribute.")


@click.option('--mode', '-m', default="prod" ,help="Set one of the Tool Modus", type=click.Choice(helpers.modi))
@click.option('--logdir', '-ld', default="logs", help="Choose the name of the Directory for log data.")
def stats(command1,
            status_bar,  use_end_file_marker,  make_backup, lazyness_border, 
            rewrite, use_cash, optimizer, optimizer_page_size, 
            optimizer_cache_size, optimizer_locking_mode, optimizer_synchronous, optimizer_journal_mode, optimizer_temp_store,
            gready,min_files_pro_stream,baseline_delimiter,

            corp_fname, stream_number,create_indexes,  freeze_db, optimized_for_long_syntagmas,

            stats_fname,stats_intern_dbname,visibility, encryption_key , version, stats_id, context_lenght, full_repetativ_syntagma,
            repl_up, ignore_hashtag, case_sensitiv, ignore_url, ignore_mention, ignore_punkt, ignore_num,
            recompute_flag,value, attr_name, baseline_insertion_border,

            export_dir, syntagma_for_export, exp_repl, exp_redu,  exp_sentiment, export_name, export_file_type, rows_limit_in_file, 
            encryption_key_corp, output_table_type, additional_doc_cols,  max_scope, stemmed_search, context_len_left, context_len_right, 
            separator_syn, word_examples_sum_table, exp_syntagma_typ,ignore_symbol,

            mode,logdir ):
    # $ zas-vot-tools strat1 sets/train_set sets/eval_set  segments voiceless voiced vlwindow vcwindow experiments
    logger = get_cli_logger(mode,logdir)
    func_name = "stats"
    #p(command,"command")

    if syntagma_for_export != "*":
        temp_syn = []
        syntagma_for_export = syntagma_for_export.strip("'") if syntagma_for_export[0] == "'" else syntagma_for_export.strip('"')
        exctracted_syn = syntagma_for_export.split(",")
        for syntagma_part in  exctracted_syn:
            temp_syn.append(syntagma_part.split("|"))

        ### combinatoric 
        if len(temp_syn) == 0:
            logger.error("No one syntagma was exctracted. Probably wrong structure was given. Please give syntagma in the following structure 'very|huge|highly,pitty|hard|happy,man|woman|boy|person'")
            return False
        else:
            #p(temp_syn,"temp_syn")
            syntagma_for_export = list(itertools.product(*temp_syn))



    optimizer =  strtobool(optimizer)
    stats_intern_dbname = strtobool(stats_intern_dbname)
    visibility = strtobool(visibility)
    #cols_and_types_in_doc = strtobool(cols_and_types_in_doc) 
    #type_to_export = strtobool(type_to_export)
    exp_sentiment = strtobool(exp_sentiment)
    recompute_flag = strtobool(recompute_flag) if recompute_flag  is not None else None
    status_bar = strtobool(status_bar)
    stats_fname = strtobool(stats_fname)
    try:
        max_scope = int(max_scope)
    except:
        max_scope = False

    #p(status_bar,"status_bar")
    #p(type(status_bar),"status_bar")


    if command1 not in supported_commands[func_name]:
        logger.error(" Given Command ('{}') is illegal for '{}'. Please use one of the following commands: '{}' ".format(command1,func_name,supported_commands[func_name] ))
        return False


    if command1 == "compute":
        if not corp_fname or not stats_intern_dbname or not visibility:
            logger.error("Command is incomplete: One of the following options is empty  '--corp_fname', '--stats_intern_dbname', '--visibility'  ")
            return False
        else:
            files = get_corp_fname(main_folders)
            if corp_fname in files:
                pass
            elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                corp_fname = corp_fname+".db"
            else:
                logger.error("Given corp_fname ('{}') wasn't found and can not be opened.".format(corp_fname))
                return False

        corp = Corpus(mode="error")
        corp.open(os.path.join(main_folders["corp"],corp_fname), encryption_key=encryption_key_corp)
        #p(("+++++",corp.corpdb))
        if corp.corpdb:
            if not corp.corpdb._db:
                #p("----")
                logger.error("CorpDB-Opening is failed. (CorpFname: ('{}')) If this corpus is encrypted, please use option '--encryption_key_corp'.  ".format(corp))
                return False
        else:
            logger.error("CorpDB-Opening is failed. (CorpFname: ('{}')) If this corpus is encrypted, please use option '--encryption_key_corp'.  ".format(corp))
            return False
        #p("....")
        language = corp.corpdb.get_attr("language")
        corpus_id = corp.corpdb.get_attr("id")
        stop_if_db_already_exist = False if rewrite else True
        stop_process_if_possible = False if gready else True
        stats = Stats(mode=mode, error_tracking=answer_error_tracking, status_bar=status_bar,
                make_backup=strtobool(make_backup),  lazyness_border=lazyness_border, thread_safe=True, rewrite=strtobool(rewrite), stop_if_db_already_exist=stop_if_db_already_exist,
                use_cash=strtobool(use_cash), optimizer=strtobool(optimizer),optimizer_page_size=optimizer_page_size, 
                optimizer_cache_size=optimizer_cache_size, optimizer_locking_mode=optimizer_locking_mode, optimizer_synchronous=optimizer_synchronous,
                optimizer_journal_mode=optimizer_journal_mode, optimizer_temp_store=optimizer_temp_store,stop_process_if_possible=stop_process_if_possible)

        stats.init(main_folders["stats"], stats_intern_dbname, language,  visibility, corpus_id=corpus_id, 
                        encryption_key=encryption_key,fileName=stats_fname,  version=version, stats_id=stats_id,
                        context_lenght=context_lenght, full_repetativ_syntagma=strtobool(full_repetativ_syntagma),
                        min_scope_for_indexes=2, repl_up=repl_up, ignore_hashtag=strtobool(ignore_hashtag), force_cleaning=False,
                        case_sensitiv=strtobool(case_sensitiv), ignore_url=strtobool(ignore_url),  ignore_mention=strtobool(ignore_mention),
                        ignore_punkt=strtobool(ignore_punkt), ignore_num=strtobool(ignore_num),baseline_delimiter=baseline_delimiter,)
        #p(stream_number, "stream_number")
        stats.compute(corp, stream_number=stream_number, datatyp="dict", 
                        adjust_to_cpu=True,min_files_pro_stream=min_files_pro_stream,cpu_percent_to_get=50,
                        create_indexes=create_indexes, freeze_db=freeze_db,baseline_insertion_border=baseline_insertion_border,
                        drop_indexes=True,optimized_for_long_syntagmas=optimized_for_long_syntagmas)


    elif command1 == "recompute":
        #p((stats_fname, recompute_flag))
        if not stats_fname or recompute_flag is None:
            logger.error("Command is incomplete: One of the following options is empty  '--stats_fname', '--recompute_flag' ")
            return False
        else:
            files = get_stats_fname(main_folders)
            if stats_fname in files:
                pass
            elif stats_fname in [os.path.splitext(fname)[0] for fname in files]:
                stats_fname = stats_fname+".db"
            else:
                logger.error("Given stats_fname ('{}') wasn't found and can not be opened.".format(stats_fname))
                return False

        stats = Stats(mode=mode)
        stats.open(os.path.join(main_folders["stats"],stats_fname), encryption_key=encryption_key)
        if not stats.statsdb:
            logger.error("StatsDB-Opening is failed. (StatsFname: ('{}')) If this statsus is encrypted, please use option '--encryption_key'.  ".format(stats))
            return False

        stats.recompute_syntagma_repetativity_scope(recompute_flag, _check_statsdb_consistency=True)


    elif command1 == "optimize":
        if not stats_fname:
            logger.error("Command is incomplete: One of the following options is empty  '--stats_fname' ")
            return False
        else:
            files = get_stats_fname(main_folders)
            if stats_fname in files:
                pass
            elif stats_fname in [os.path.splitext(fname)[0] for fname in files]:
                stats_fname = stats_fname+".db"
            else:
                logger.error("Given stats_fname ('{}') wasn't found and can not be opened.".format(stats_fname))
                return False

        stats = Stats(mode=mode)
        stats.open(os.path.join(main_folders["stats"],stats_fname), encryption_key=encryption_key)
        if not stats.statsdb:
            logger.error("StatsDB-Opening is failed. (StatsFname: ('{}')) If this statsus is encrypted, please use option '--encryption_key'.  ".format(stats))
            return False

        stats.optimize_db( stream_number=stream_number, optimized_for_long_syntagmas=optimized_for_long_syntagmas, )


    elif command1 == "recreate_indexes":
        if not stats_fname:
            logger.error("Command is incomplete: One of the following options is empty  '--stats_fname' ")
            return False
        else:
            files = get_stats_fname(main_folders)
            if stats_fname in files:
                pass
            elif stats_fname in [os.path.splitext(fname)[0] for fname in files]:
                stats_fname = stats_fname+".db"
            else:
                logger.error("Given stats_fname ('{}') wasn't found and can not be opened.".format(stats_fname))
                return False

        stats = Stats(mode=mode)
        stats.open(os.path.join(main_folders["stats"],stats_fname), encryption_key=encryption_key)
        if not stats.statsdb:
            logger.error("StatsDB-Opening is failed. (StatsFname: ('{}')) If this statsus is encrypted, please use option '--encryption_key'.  ".format(stats))
            return False

        #stats.optimize_db( stream_number=stream_number, optimized_for_long_syntagmas=optimized_for_long_syntagmas, )
        stats.create_additional_indexes(optimized_for_long_syntagmas=optimized_for_long_syntagmas)

    elif command1 == "del":
        if not stats_fname:
            logger.error("'--stats_fname' is not given. (you can also give tag 'all' instead of the stats_fname)")
            return False
        if stats_fname == "all":
            #os.remove()
            shutil.rmtree(main_folders["stats"], ignore_errors=True)
            logger.info("All StatsDB was removed.")
        else:
            files = get_stats_fname(main_folders)
            if stats_fname in files:
                os.remove(os.path.join(main_folders["stats"], stats_fname))
                logger.info("'{}'-StatsDB was removed".format(stats_fname))
            elif stats_fname in [os.path.splitext(fname)[0] for fname in files]:
                os.remove(os.path.join(main_folders["stats"], stats_fname)+".db")
                logger.info("'{}'-StatsDB was removed".format(stats_fname))
            else:
                logger.error("Given fname ('{}') wasn't found and can not be removed.".format(stats_fname))
                return False

    elif command1 == "clean_dir":
        #if not corp_fname:
        #    logger.error("'--corp_fname' is not given. (you can also give tag 'all' instead of the corp_fname)")
        #if corp_fname == "all":
        files = get_stats_fname(main_folders)
        validated,possibly_encrypted,wrong,opened_db = validate_stats(main_folders,files)
        deleted = []
        for temp_dbname in validated:
            stats = Sretats(mode="blind")
            stats.open(os.path.join(main_folders["stats"], temp_dbname))
            
            if stats.statsdb:
                if stats.statsdb.get_attr("locked"):
                    deleted.append(temp_dbname)
                    os.remove(os.path.join(main_folders["stats"], temp_dbname))

        files = os.listdir(main_folders["stats"])
        for journal_fname in [fname for fname in files if".db-journal" in fname]:
            #deleted.append(temp_dbname)
            os.remove(os.path.join(main_folders["stats"], journal_fname))

        if deleted:
            print " Following not finished and locked statsDBs was deleted:"
            for dn in deleted:
                print "   |-> '{}';".format(dn)
            return True
        else:
            print " Locked or not finished statsDBs wasn't found."
            return False


    elif command1 == "names":
        #p("fghjk")
        files = get_stats_fname(main_folders)
        #p(files, "files")
        validated,possibly_encrypted,wrong,opened_db = validate_stats(main_folders,files)
        print ">>> {} DBs was found <<<  ".format(len(files))
        print " '{}'-From them was validated:".format(len(validated))
        for i, fname in enumerate(validated):
            print "       {}. '{}';".format(i, fname)
        if possibly_encrypted:
            print "\n  '{}'-From them are possibly encrypted/damaged/invalid:".format(len(possibly_encrypted))
            for i, fname in enumerate(possibly_encrypted):
                print "       {}. '{}';".format(i, fname)

        #p(files)

    elif command1 == "meta":
        if not stats_fname:
            logger.error("'--stats_fname' is not given. (you can also give tag 'all' instead of the stats_fname)")
            return False

        files = get_stats_fname(main_folders)
        validated,possibly_encrypted,wrong,opened_db = validate_stats(main_folders,files)
        if stats_fname == "all":
            for db in opened_db:
                print("\n >>>> {} <<<<".format(db.fname()))
                for k,v in db.get_all_attr().items():
                    print "    {} = '{}';".format(k,v)


            print "\n\nNotice! with 'all'-Argument could be checked just not-encrypted DBs. If you want to check encrypted DB use additional to stats_fname also  '--encryption_key'"

        else:
            if stats_fname in files:
                if stats_fname in validated:
                    ix = validated.index(stats_fname)
                    db = opened_db[ix]
                    print("\n >>>> {} <<<<".format(db.fname()))
                    for k,v in db.get_all_attr().items():
                        print "    {} = '{}';".format(k,v)
                elif stats_fname in possibly_encrypted:
                    if not encryption_key:
                        logger.error("Current DBFile is possibly encrypted/damaged. Please use '--encryption_key'-Option to decrypt it. ")
                    else:
                        h = DBHandler(mode="blind")
                        h.connect(os.path.join(main_folders["stats"],stats_fname),encryption_key=encryption_key)
                        try:
                            if h.typ() == "stats":
                                print("\n >>>> {} <<<<".format(h.fname()))
                                for k,v in h.get_all_attr().items():
                                    print "    {} = '{}';".format(k,v)
                            else:
                                logger.error("'{}'-DB is not an StatsDB or given encryption key ('{}') is wrong. ".format(stats_fname,encryption_key))
                                return False
                        except:
                            logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(stats_fname,encryption_key))
                            return False
                
            elif stats_fname in [os.path.splitext(fname)[0] for fname in files]:
                spl1 = [os.path.splitext(fname)[0] for fname in validated]
                spl2 = [os.path.splitext(fname)[0] for fname in possibly_encrypted]
                if stats_fname in spl1:
                    ix = spl1.index(stats_fname)
                    db = opened_db[ix]
                    print("\n >>>> {} <<<<".format(db.fname()))
                    for k,v in db.get_all_attr().items():
                        print "    {} = '{}';".format(k,v)
                
                elif stats_fname in spl2:
                    if not encryption_key:
                        logger.error("Current DBFile is possibly encrypted/damaged. Please use '--encryption_key'-Option to decrypt it. ")
                    else:
                        h = DBHandler(mode="blind")
                        h.connect(os.path.join(main_folders["stats"],stats_fname)+".db",encryption_key=encryption_key)
                        try:
                            if h.typ() == "stats":
                                print("\n >>>> {} <<<<".format(h.fname()))
                                for k,v in h.get_all_attr().items():
                                    print "    {} = '{}';".format(k,v)
                            else:
                                logger.error("'{}'-DB is not an StatsDB or given encryption key ('{}') is wrong. ".format(stats_fname,encryption_key))
                                return False
                        except:
                            logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(stats_fname,encryption_key))
                            return False


                else:
                    logger.error("Given fname ('{}') wasn't validated. It means, that possibly it is not a StatsDB or it is just encrypted!".format(stats_fname))
                    return False
            else:
                logger.error("Given fname ('{}') wasn't found!".format(stats_fname))
                return False


    elif command1 == "basic_stats":
        if not stats_fname:
            logger.error("'--stats_fname' is not given. (you can also give tag 'all' instead of the stats_fname)")
            return False

        files = get_stats_fname(main_folders)
        validated,possibly_encrypted,wrong,opened_db = validate_stats(main_folders,files)
        if stats_fname == "all":
            for db in opened_db:
                print("\n >>>> {} <<<<".format(db.fname()))
                print "    repl_num = '{}';".format(db.rownum("replications"))
                print "    redu_num = '{}';".format(db.rownum("reduplications"))
                print "    baseline_syntagma_num = '{}';".format(db.rownum("baseline"))

            print "\n\nNotice! with 'all'-Argument could be checked just not-encrypted DBs. If you want to check encrypted DB use additional to stats_fname also  '--encryption_key'"

        else:
            if stats_fname in files:
                if stats_fname in validated:
                    ix = validated.index(stats_fname)
                    db = opened_db[ix]
                    print("\n >>>> {} <<<<".format(db.fname()))
                    print "    repl_num = '{}';".format(db.rownum("replications"))
                    print "    redu_num = '{}';".format(db.rownum("reduplications"))
                    print "    baseline_syntagma_num = '{}';".format(db.rownum("baseline"))
                elif stats_fname in possibly_encrypted:
                    if not encryption_key:
                        logger.error("Current DBFile is possibly encrypted/damaged. Please use '--encryption_key'-Option to decrypt it. ")
                    else:
                        h = DBHandler(mode="blind")
                        h.connect(os.path.join(main_folders["stats"],stats_fname),encryption_key=encryption_key)
                        try:
                            if h.typ() == "stats":
                                print("\n >>>> {} <<<<".format(h.fname()))
                                print "    repl_num = '{}';".format(db.rownum("replications"))
                                print "    redu_num = '{}';".format(db.rownum("reduplications"))
                                print "    baseline_syntagma_num = '{}';".format(db.rownum("baseline"))
                            else:
                                logger.error("'{}'-DB is not an StatsDB or given encryption key ('{}') is wrong. ".format(stats_fname,encryption_key))
                                return False
                        except:
                            logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(stats_fname,encryption_key))
                            return False
                
            elif stats_fname in [os.path.splitext(fname)[0] for fname in files]:
                spl1 = [os.path.splitext(fname)[0] for fname in validated]
                spl2 = [os.path.splitext(fname)[0] for fname in possibly_encrypted]
                if stats_fname in spl1:
                    ix = spl1.index(stats_fname)
                    db = opened_db[ix]
                    print("\n >>>> {} <<<<".format(db.fname()))
                    print "    repl_num = '{}';".format(db.rownum("replications"))
                    print "    redu_num = '{}';".format(db.rownum("reduplications"))
                    print "    baseline_syntagma_num = '{}';".format(db.rownum("baseline"))

                elif stats_fname in spl2:
                    stats_fname = stats_fname+".db"
                    if not encryption_key:
                        logger.error("Current DBFile is possibly encrypted/damaged. Please use '--encryption_key'-Option to decrypt it. ")
                    else:
                        h = DBHandler(mode="blind")
                        h.connect(os.path.join(main_folders["stats"],stats_fname),encryption_key=encryption_key)
                        try:
                            if h.typ() == "stats":
                                print("\n >>>> {} <<<<".format(h.fname()))
                                print "    repl_num = '{}';".format(db.rownum("replications"))
                                print "    redu_num = '{}';".format(db.rownum("reduplications"))
                                print "    baseline_syntagma_num = '{}';".format(db.rownum("baseline"))
                            else:
                                logger.error("'{}'-DB is not an StatsDB or given encryption key ('{}') is wrong. ".format(stats_fname,encryption_key))
                                return False
                        except:
                            logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(stats_fname,encryption_key))
                            return False

                else:
                    logger.error("Given fname ('{}') wasn't validated. It means, that possibly it is not a StatsDB or it is just encrypted!".format(stats_fname))
                    return False
            else:
                logger.error("Given fname ('{}') wasn't found!".format(stats_fname))
                return False


    elif command1 == "update_attr":
        if not stats_fname or  not attr_name or not value:
            logger.error("Command is incomplete: '--stats_fname' or '--attr_name' or '--value' is not given.")
        else:
            files = get_stats_fname(main_folders)
            if stats_fname in files:
                pass
            elif stats_fname in [os.path.splitext(fname)[0] for fname in files]:
                stats_fname = stats_fname+".db"
            else:
                logger.error("Given fname ('{}') wasn't found.".format(stats_fname))
                return False
            
            try:
                db = DBHandler(mode="error")
                db.connect(os.path.join(main_folders["stats"],stats_fname),encryption_key=encryption_key)
                if db._db:
                    if db.typ() == "stats":
                        if attr_name not in db.get_all_attr():
                            logger.error("Given Attribute ('{}') is not exist in this DataBase.".format(attr_name))
                            return False

                        db.update_attr(attr_name,value)
                        db._commit()
                        updated_attr = db.get_attr(attr_name)
                        #p((updated_attr, value))
                        if str(value) != str(updated_attr):
                            logger.error("Update of the given Attribute ('{}') failed.".format(attr_name))
                            return 
                        else:
                            logger.info("Given Attribute ('{}') in the '{}'-DB was updated to '{}'.".format(attr_name,stats_fname, value))
                            return True
                    else:
                        logger.error("'{}'-DB is not an StatsDB or given encryption key ('{}') is wrong. ".format(stats_fname,encryption_key))
                        return False
                else:
                    #p(type(strtobool(encryption_key)), "strtobool(encryption_key)")
                    if strtobool(encryption_key):
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(stats_fname,encryption_key))
                    else:
                        logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(stats_fname,encryption_key))
                    return False
            except:
                if strtobool(encryption_key):
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or the encryption key was wrong'{}' ".format(stats_fname,encryption_key))
                else:
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(stats_fname,encryption_key))
                return False

    elif command1 == "export":
        if not stats_fname or  not export_file_type :
            logger.error("Command is incomplete:   '--stats_fname' or '--export_file_type'  is not given.")
            return False
        else:
            if not exp_repl and not  exp_redu:
                logger.error("No one Repetition Phanomen was selected. Please select minimum one phanomen. Ypu can use for that following options '--exp_redu', '--exp_repl' ")
                return False
            files = get_stats_fname(main_folders)

            if stats_fname in files:
                pass
            elif stats_fname in [os.path.splitext(fname)[0] for fname in files]:
                stats_fname = stats_fname+".db"
            else:
                logger.error("Given fname ('{}') wasn't found".format(stats_fname))
                return False

            stats = Stats(mode=mode, status_bar=status_bar)
            stats.open(os.path.join(main_folders["stats"],stats_fname),encryption_key=encryption_key)


            if stats.statsdb._db:
                export_dir = export_dir if export_dir else main_folders["export"]
                export_name = export_name if export_name else False

                #if syntagma_for_export != "*":
                    #syntagma_for_export = syntagma_for_export.strip("'")
                    #syntagma_for_export = syntagma_for_export.split(",")

                if additional_doc_cols:
                    if not corp_fname:
                        logger.error("'--corp_fname' wasn't given For additional extraction of the columns from CorpDB you need also to give CorpDB-Name.")
                        return False
                    additional_doc_cols = additional_doc_cols.strip("'")
                    additional_doc_cols = additional_doc_cols.split(",")
                    additional_doc_cols = [col.strip(" ") for col in additional_doc_cols]

                if corp_fname:
                    files = get_corp_fname(main_folders)
                    if corp_fname in files:
                        pass
                    elif corp_fname in [os.path.splitext(fname)[0] for fname in files]:
                        corp_fname = corp_fname+".db"
                    else:
                        logger.error("Given corp_fname ('{}') wasn't found and can not be opened.".format(corp_fname))
                        return False

                path_to_corpdb = os.path.join(main_folders["corp"],corp_fname) if corp_fname else False
                #p((export_dir, syntagma_for_export, exp_repl, exp_redu,exp_syntagma_typ, exp_sentiment, export_name, export_file_type, rows_limit_in_file, encryption_key_corp, output_table_type, additional_doc_cols,corp_fname, max_scope, stemmed_search,context_len_left, context_len_right, separator_syn,word_examples_sum_table,ignore_num,ignore_symbol), r=True)
                #p( {'path_to_corpdb': False, 'stemmed_search': False, 'redu': True, 'rewrite': False, 'ignore_num': False, 'additional_doc_cols': False, 'syntagma': u'*', 'baseline': True, 'sentiment': False, 'self': <zas_rep_tools.src.classes.stats.Stats object at 0x105f92b10>, 'encryption_key_for_exported_db': False, 'fname': False, 'word_examples_sum_table': True, 'syntagma_type': 'lexem', 'context_len_right': False, 'repl': True, 'max_scope': u'3', 'output_table_type': 'exhausted', 'path_to_export_dir': '/Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/prjdir/export', 'encryption_key_corp': False, 'separator_syn': u' || ', 'context_len_left': True, 'rows_limit_in_file': 50000, 'ignore_symbol': False, 'export_file_type': 'csv'}(syntagma_for_export, exp_repl, exp_redu, exp_syntagma_typ))
                #p(syntagma_for_export,"syntagma")
                stats.export(   export_dir, syntagma=syntagma_for_export, repl=exp_repl, redu=exp_redu,
                                baseline=True, syntagma_type=exp_syntagma_typ, sentiment=exp_sentiment,
                                fname=export_name, export_file_type=export_file_type, rows_limit_in_file=rows_limit_in_file,
                                encryption_key_corp=encryption_key_corp, output_table_type=output_table_type,
                                additional_doc_cols=additional_doc_cols,
                                path_to_corpdb=path_to_corpdb, max_scope=max_scope, stemmed_search=stemmed_search,rewrite=False,
                                context_len_left=context_len_left, context_len_right=context_len_right, separator_syn=separator_syn,
                                word_examples_sum_table=word_examples_sum_table,ignore_num=ignore_num,ignore_symbol=ignore_symbol)



            else:
                #p(type(strtobool(encryption_key)), "strtobool(encryption_key)")
                if strtobool(encryption_key):
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is locked or damaged or given  encryption key ('{}') is wrong. ".format(stats_fname,encryption_key))
                else:
                    logger.error("'{}'-DB wasn't opened. Possibly this DB is damaged or encrypted or locked. Please use '--encryption_key' option to set an encryption_key ".format(stats_fname,encryption_key))
                return False





@main.command('streamTwitter')
@click.argument('path_to_save',type=click.Path())
@click.option('--language', '-l', default="False", type=click.Choice(list(Streamer.supported_languages)+ ["False"]))
@click.option('--stop_words', '-sw', default=False)
@click.option('--terms', '-t', default=False)
@click.option('--encoding', '-e', default='utf_8', type=click.Choice(list(Streamer.supported_encodings_types)))
@click.option('--ignore_rt', '-irt', default=False, type=bool)
@click.option('--filter_strategie', '-f', default="False", help="Set Filter Strategy. 1) 't'-just search for terms/stop_words; 2) 't+l' - search for stop_words and language (recomended) ",type=click.Choice(list(["t", "t+l", "False", ])))
@click.option('--save_used_terms', '-sut', default=True, type=bool)

@click.option('--mode', '-m', default="prod" ,help="Set one of the Tool Modus", type=click.Choice(helpers.modi))
@click.option('--logdir', '-ld', default="logs", help="Choose the name of the Directory for log data.")
def streamTwitter( path_to_save,language,stop_words,terms,encoding,ignore_rt, filter_strategie, save_used_terms,  logdir, mode):
    logger = get_cli_logger(mode,logdir)
    func_name = sys._getframe().f_code.co_name

    # self.test_consumer_key = "97qaczWSRfaaGVhKS6PGHSYXh"
    # self.test_consumer_secret = "mWUhEL0MiJh7FqNlOkQG8rAbC8AYs4YiEOzdiCwx26or1oxivc"
    # self.test_access_token = "1001080557130932224-qi6FxuYwtvpbae17kCjAS9kfL8taNT"
    # self.test_access_token_secret = "jCu2tTVwUW77gzOtK9X9svbdKUFvlSzAo4JfIG8tVuSgX"

    #p(configer_obj._user_data["twitter_creditials"])
    try:
        configer_obj._user_data["twitter_creditials"]
        if not configer_obj._user_data["twitter_creditials"]:
            raise Exception, "STOP"
    except:
        configer_obj._cli_menu_get_from_user_twitter_credentials()


    try:
        if not configer_obj._user_data["twitter_creditials"]:
            logger.error("TwitterCreditials wasn't found. Please give TwitterCreditials before you can use this Tools.")
            return False
    except:
        logger.error("TwitterCreditials wasn't found. Please give TwitterCreditials before you can use this Tools.")
        return False

    language = strtobool(language)
    #p(configer_obj._user_data["twitter_creditials"])
    #p(configer_obj._user_data["twitter_creditials"][0])
    configer_obj._user_data["twitter_creditials"][0]
    consumer_key = configer_obj._user_data["twitter_creditials"][0]["consumer_key"]
    consumer_secret = configer_obj._user_data["twitter_creditials"][0]["consumer_secret"]
    access_token = configer_obj._user_data["twitter_creditials"][0]["access_token"]
    access_token_secret = configer_obj._user_data["twitter_creditials"][0]["access_token_secret"]

    #p((consumer_key, consumer_secret, access_token, access_token_secret, path_to_save))

    if stop_words and  not os.path.isfile(stop_words):
        if stop_words not in Streamer.stop_words_collection:
            stop_words = stop_words.split(",")
            logger.info("Recognized stop-words: {}".format(stop_words))

    if terms and not os.path.isfile(terms):
        terms = terms.split(",")
        logger.info("Recognized terms: {}".format(terms))


    stream = Streamer(consumer_key, consumer_secret, access_token, access_token_secret, path_to_save, platfrom="twitter",
                    language=language, email_addresse=email, stop_words=stop_words, terms=terms,
                    encoding=encoding, ignore_rt=ignore_rt, save_used_terms=save_used_terms, filterStrat=filter_strategie,
                    mode=mode)
    stream.stream_twitter()




@main.command('streamerInfo')
@click.argument('command')
@click.option('--mode', '-m', default="prod" ,help="Set one of the Tool Modus",  type=click.Choice(helpers.modi))
@click.option('--logdir', '-ld', default="logs", help="Choose the name of the Directory for log data.")
#@click.option('--logs_dir', '-l', default="logs")
def streamerInfo(command,  logdir, mode):
    # $ zas-vot-tools strat1 sets/train_set sets/eval_set  segments voiceless voiced vlwindow vcwindow experiments
    logger = get_cli_logger(mode,logdir)
    func_name = sys._getframe().f_code.co_name

    possible_commands = ["enc", "lang", "nltk_lang", "twitter_lang", "classiefier_lang", "stop_words", "platforms"]


    if command not in possible_commands:
        logger.error("Given Command {} is not exist. Please use one of the following commands: {}".format(command, possible_commands))
 
    if command == "enc":
        print Streamer.supported_encodings_types

    if command == "lang":
        print Streamer.supported_languages

    if command == "nltk_lang":
        print [k for k in Streamer.NLTKlanguages] 

    if command == "twitter_lang":
        print Streamer.supported_languages_by_twitter

    if command == "classiefier_lang":
        print Streamer.supported_languages_by_langid

    if command == "stop_words":
        print Streamer.supported_stop_words


    if command == "platforms":
        print Streamer.supported_platforms



@main.command('testspath')
def testspath():
    #print configer_obj.path_to_tests
    print configer_obj.path_to_tests





if __name__ == "__main__":
    main()
