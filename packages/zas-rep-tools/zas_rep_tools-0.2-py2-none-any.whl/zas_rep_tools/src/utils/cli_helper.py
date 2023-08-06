#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : Utilities for Command Line Interface  
# Author:
# c(Student) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###Programm Info######

#from zas_rep_tools.src.utils.logger import Logger

import logging
import inspect
import os
import codecs
import ast
import re
import json
import sys
from blessings import Terminal
import enlighten


#from zas_rep_tools.src.classes.corpus import Corpus
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.helpers import set_class_mode
from zas_rep_tools.src.utils.zaslogger import ZASLogger

# path_to_zas_rep_tools = os.path.dirname(os.path.dirname(os.path.dirname(inspect.getfile(Corpus))))
# path_to_file_with_twitter_creditials = "user-config/twitter_api_credentials.json"
# path_to_file_with_user_agreements = "user-config/user_agreement.json"
# path_to_file_with_db_settings = "user-config/db_settings.json"

def cli_logger(level=logging.INFO, folder_for_log="stats", logger_usage=True,save_logs=False):
    L = ZASLogger("CLI", level=level,
                        folder_for_log=folder_for_log,
                        logger_usage=logger_usage,
                        save_logs=save_logs)
    logger = L.getLogger()
    return logger

def get_settings(mode):
    settings = tuple(set_class_mode(mode))
    level = settings[0]
    logger_usage = settings[6]
    save_logs = settings[2] 
    return level, logger_usage, save_logs


def get_cli_logger(mode,folder_for_log):
    level, logger_usage, save_logs = get_settings(mode)
    logger = cli_logger(level=logging.INFO, folder_for_log="logs", logger_usage=True,save_logs=False)
    return logger


def set_main_folders(project_folder):
    main_folders = {
                    "corp": os.path.join(project_folder, "corpora")  if project_folder else None,
                    "stats": os.path.join(project_folder, "stats")  if project_folder else None,
                    "export": os.path.join(project_folder, "export")  if project_folder else None,
                    }
    try:
        for t, path in main_folders.items():
            #p((t, path))
            if not path:
                continue
            if not os.path.isdir(path):
                os.makedirs(path)
    except Exception as e:
       print "ERROR: Folders in the ProjectDirectory wasn't created. ({}) Please select other ProjectDirectory.".format(repr(e))

    return main_folders



def strtobool(obj):
    #p(obj, "obj")
    try:
        return ast.literal_eval(obj)
    except:
        return obj

def get_corp_fname(main_folders):
    files = os.listdir(main_folders["corp"])
    files = [fname for fname in files if ".db" in fname and ".db-journal" not in fname]
    return files


def get_stats_fname(main_folders):
    files = os.listdir(main_folders["stats"])
    files = [fname for fname in files if ".db" in fname and ".db-journal" not in fname]
    return files

def _get_status_bars_manager():
    config_status_bar = {'stream': sys.stdout,
              'useCounter': True, 
              "set_scroll": True,
              "resize_lock": True
              }
    enableCounter_status_bar = config_status_bar['useCounter'] and config_status_bar['stream'].isatty()
    return enlighten.Manager(stream=config_status_bar['stream'], enabled=enableCounter_status_bar, set_scroll=config_status_bar['set_scroll'], resize_lock=config_status_bar['resize_lock'])

def _get_new_status_bar( total, desc, unit, counter_format=False, status_bars_manager=False):
    if counter_format:
        counter = status_bars_manager.counter(total=total, desc=desc, unit=unit, leave=True, counter_format=counter_format)
    else:
        counter = status_bars_manager.counter(total=total, desc=desc, unit=unit, leave=True)
    return counter


def validate_corp(main_folders,files=False,):
    files = files  if isinstance(files, (list, tuple)) else get_corp_dbname()
    validated = []
    possibly_encrypted = []
    wrong = []
    handl = DBHandler(mode="blind")
    opened_db = []
    for fname in files:
        status = handl._validation_DBfile(os.path.join(main_folders["corp"],fname))
        if status["status"]:
            h = DBHandler(mode="blind")
            h.connect(os.path.join(main_folders["corp"],fname))
            if h.typ() == "corpus":
                validated.append(fname)
                opened_db.append(h)
            else:
                wrong.append(fname)
        else:
            possibly_encrypted.append(fname)
    return validated,possibly_encrypted,wrong,opened_db



def validate_stats(main_folders,files=False):
    files = files  if isinstance(files, (list, tuple)) else get_corp_dbname()
    validated = []
    possibly_encrypted = []
    wrong = []
    handl = DBHandler(mode="blind")
    opened_db = []
    for fname in files:
        status = handl._validation_DBfile(os.path.join(main_folders["stats"],fname))
        if status["status"]:
            h = DBHandler(mode="blind")
            h.connect(os.path.join(main_folders["stats"],fname))
            if h.typ() == "stats":
                validated.append(fname)
                opened_db.append(h)
            else:
                wrong.append(fname)
        else:
            possibly_encrypted.append(fname)
    return validated,possibly_encrypted,wrong,opened_db








