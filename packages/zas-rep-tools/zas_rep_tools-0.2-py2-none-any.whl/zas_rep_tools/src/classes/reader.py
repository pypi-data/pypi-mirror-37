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
from __future__ import division
from __future__ import absolute_import


import os
import copy
import sys
import regex
import logging
import codecs
import json
import csv
import unicodecsv as unicodecsv
from lxml import etree as ET
import psutil
import zipfile
import cStringIO
import json
import StringIO
#zipfile.ZipExtFile


from collections import defaultdict
from raven import Client
#from cached_property import cached_property
from encodings.aliases import aliases
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP, ROUND_HALF_DOWN, ROUND_DOWN

#from zas_rep_tools.src.utils.db_helper import *
#from zas_rep_tools.src.classes.configer import Configer
from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, LenGen, path_to_zas_rep_tools, get_number_of_streams_adjust_cpu, instance_info, SharedCounterExtern, SharedCounterIntern, Status, function_name,statusesTstring
#from zas_rep_tools.src.utils.logger import *
from zas_rep_tools.src.utils.zaslogger import ZASLogger
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.utils.helpers import get_file_list
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus
from zas_rep_tools.src.classes.basecontent import BaseContent


import platform
if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama

csv.field_size_limit(sys.maxsize)

class Reader(BaseContent):
    #supported_encodings_types = ["utf-8"]
    supported_encodings_types = set(aliases.values())
    supported_encodings_types.add("utf-8")
    supported_file_types = ["txt", "json", "xml", "csv"]
    supported_file_types_to_export = ["sqlite", "json", "xml", "csv"]

    regex_templates = {
                "blogger":r"(?P<id>[\d]*)\.(?P<gender>[\w]*)\.(?P<age>\d*)\.(?P<working_area>.*)\.(?P<star_constellation>[\w]*)",
                }

    reader_supported_formatter = {
                                "json":["TwitterStreamAPI".lower()],
                                "csv":["Sifter".lower()],
                                }

                            

    def __init__(self, inp_path, file_format,  regex_template=False,
                regex_for_fname=False, read_from_zip=False,
                end_file_marker = -1, send_end_file_marker=False,
                formatter_name=False, text_field_name = "text", id_field_name="id",
                ignore_retweets=True,stop_process_if_possible=True,
                **kwargs):

        #p(read_from_zip, "read_from_zip")
        super(type(self), self).__init__(**kwargs)
        #super(BaseContent, self).__init__(**kwargs)

        #p((regex_for_fname , regex_template))
        #Input: Encapsulation:
        self._inp_path = inp_path
        self._file_format = file_format.lower()
        #self._columns_source = columns_source
        self._regex_for_fname = regex_for_fname 
        self._regex_template =regex_template 
        #p((self._regex_for_fname,self._regex_template))
        self._formatter_name = formatter_name.lower() if formatter_name else formatter_name
        self._text_field_name = text_field_name
        self._id_field_name = id_field_name
        self._ignore_retweets = ignore_retweets
        self._read_from_zip = read_from_zip
        self._end_file_marker = end_file_marker
        self._send_end_file_marker = send_end_file_marker
        self._stop_process_if_possible = stop_process_if_possible


        #InstanceAttributes: Initialization
        self._created_streams = 0
        self._stream_done = 0
        self.xmlroottag = False
        self.xmlchildetag = False
        self.retweet_counter = SharedCounterIntern()
        self.files_to_read_orig = []
        self.files_to_read_leftover = None
        self.files_at_all_was_found = 0
        self.zips_to_read = []
        self.files_from_zips_to_read_orig = defaultdict(list)
        self.files_from_zips_to_read_left_over = None
        self.files_number_in_zips = 0
        self.counter_lazy_getted  = 0



        self.logger.debug('Intern InstanceAttributes was initialized')



        ## Validation 
        if not self._validate_given_file_format():
            sys.exit()

        if self._end_file_marker == -10:
            self.logger.error("Illegal value of the 'end_file_marker'. Please use another one.")
            #return False
            sys.exit()


        if not self._validation_given_path():
            sys.exit()

        if not self._validation_regex_treatment():
            sys.exit()

        self.logger.low_debug('Input was validated')

        # Extract Files from the given File Structure
        #p(self._inp_path)
        self._extract_all_files_according_given_file_format()


        self.logger.debug('An instance of Reader() was created ')
        
        #self.inp_obj = StringIO.StringIO()
        #self.inp_obj.write('{"id":123456}')

        ## Log Settings of the Instance
        attr_to_flag = ["files_from_zips_to_read_orig", "files_from_zips_to_read_left_over", ] 
        attr_to_len = ["files_to_read_orig", "files_to_read_leftover", "zips_to_read", ]
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



###########################+++++++++############################
    
    def _generator_helper(self, inp_obj, colnames=False, encoding="utf-8", csvdelimiter=',',f_name=False ):
        #try:
        
        #output.write('{"id":123456}')
        if self._file_format == "txt":
            row =  self._readTXT(inp_obj, encoding=encoding, columns_extract_from_fname=True, colnames=colnames)
            yield row
            if self._send_end_file_marker:
                yield self._end_file_marker

        elif self._file_format == "json":
            for row in self._readJSON(inp_obj, encoding=encoding, colnames=colnames,):
                if row == -10:
                    yield -10
                    self.logger.error("ReaderError: Probably Invalid InputData. Please check logs for more information.")
                    return
                yield row
            if self._send_end_file_marker:
                yield self._end_file_marker

        elif self._file_format == "xml":
            for row in self._readXML(inp_obj, encoding=encoding, colnames=colnames):
                if row == -10:
                    yield -10
                    self.logger.error("ReaderError: Probably Invalid InputData. Please check logs for more information.")
                    return 
                yield row
            if self._send_end_file_marker:
                yield self._end_file_marker

        elif self._file_format == "csv":
            for row in self._readCSV(inp_obj, encoding=encoding, colnames=colnames, delimiter=csvdelimiter,f_name=f_name):
                if row == -10:
                    self.logger.error("ReaderError: Probably Invalid InputData. Please check logs for more information.")
                    yield -10
                    return 
                yield row
            if self._send_end_file_marker:
                yield self._end_file_marker

        else:
            self.logger.error("'{}'-Format not supported.".format(self._file_format), exc_info=self._logger_traceback)
            yield False
            return 
 

    def getgenerator(self, colnames=False, encoding="utf-8", csvdelimiter=',', input_path_list=False, input_zip_file_list = False):
        if not input_path_list and not input_zip_file_list:
            self.logger.warning("Given Generator is empty.")
            yield False

        if input_path_list:
            for path_to_file in input_path_list:
                for row in self._generator_helper(path_to_file, colnames=colnames, encoding=encoding, csvdelimiter=csvdelimiter):
                    if row == -10:
                        yield {}
                        return 
                    yield row

        if self._read_from_zip:
            if input_zip_file_list:
                for path_to_zip, list_with_path_to_files in input_zip_file_list.iteritems():
                    archive = zipfile.ZipFile(path_to_zip, 'r')
                    for path_to_file in list_with_path_to_files:
                        f = archive.open(path_to_file)
                        for row in self._generator_helper(f, colnames=colnames, encoding=encoding, csvdelimiter=csvdelimiter, f_name=f.name):
                            if row == -10:
                                yield {}
                                return 
                            yield row

        self._stream_done += 1
        self._print_once_ignore_retweets_counter()


    def getlazy(self,colnames=False, encoding="utf-8", csvdelimiter=',', stream_number=1, adjust_to_cpu=True, min_files_pro_stream=1000, restart=True, cpu_percent_to_get=50):
        self._stream_done = 0
        self.retweet_counter.clear()
        wish_stream_number = stream_number
        if self.counter_lazy_getted>0 and restart:
            self.files_from_zips_to_read_left_over = copy.deepcopy(self.files_from_zips_to_read_orig)
            self.files_to_read_leftover = copy.deepcopy(self.files_to_read_orig)
        self.counter_lazy_getted +=1
        if stream_number <1:
            stream_number = 10000
            adjust_to_cpu = True
            self.logger.debug("StreamNumber is less as 1. Automatic computing of strem number according cpu was enabled.")
        #p(stream_number, "stream_number")
        if self._get_number_of_left_over_files() == 0:
            self.logger.error("No one file was found in the given path ('{}'). Please check the correctness of the given path or  give other (correct one) path to the text data.".format(self._inp_path))
            return []
        if adjust_to_cpu:
            stream_number= get_number_of_streams_adjust_cpu( min_files_pro_stream, self._get_number_of_left_over_files(), stream_number, cpu_percent_to_get=cpu_percent_to_get)
            if stream_number is None:
                #p((self._get_number_of_left_over_files(),self.counter_lazy_getted),"self._get_number_of_left_over_files()")
                self.logger.error("Number of input files is 0. Not generators could be returned.", exc_info=self._logger_traceback)
                return []

        #p(stream_number, "stream_number")
        if stream_number > self._get_number_of_left_over_files():
            self.logger.error("StreamNumber is higher as number of the files to read. This is not allowed.", exc_info=self._logger_traceback)
            return False

        list_with_generators = []

        number_of_files_per_stream = int(Decimal(float(self._get_number_of_left_over_files()/stream_number)).quantize(Decimal('1.'), rounding=ROUND_DOWN))
        #p((stream_number, number_of_files_per_stream), c="m")

        #self.files_from_zips_to_read_orig
        for i in range(stream_number):
            if i < (stream_number-1): # for gens in between 
                files_to_read_non_zip, files_from_zips_to_read_orig = self._get_files_for_stream(number_of_files_per_stream)

            else: # for the last generator
                files_to_read_non_zip, files_from_zips_to_read_orig = self._get_files_for_stream(-1)

            input_path_list= files_to_read_non_zip if files_to_read_non_zip else False
            input_zip_file_list = files_from_zips_to_read_orig if files_from_zips_to_read_orig else False
            gen = self._getlazy_single(input_path_list=input_path_list, input_zip_file_list=input_zip_file_list,colnames= colnames, encoding=encoding, csvdelimiter=csvdelimiter)

            if stream_number == 1:
                #p(wish_stream_number)
                if wish_stream_number > 1:
                    return [gen]
                else:
                    return gen

            list_with_generators.append(gen)

        self._created_streams = stream_number
        
        self.logger.info(" '{}'-streams was created. (adjust_to_cpu='{}')".format(stream_number, adjust_to_cpu))
        return list_with_generators


    def _print_once_ignore_retweets_counter(self):
        if int(self.retweet_counter) > 0:
            if self._stream_done >= self._created_streams:
                self.logger.info("'{}'-retweets in total was ignored.".format(int(self.retweet_counter)))


    def _get_number_of_left_over_files(self):
        #p(len(self.files_to_read_leftover), c="m")
        #p(sum([len(v) for v in self.files_from_zips_to_read_left_over.values() ]), c="m")
        return len(self.files_to_read_leftover) + sum([len(v) for v in self.files_from_zips_to_read_left_over.values() ])

    def _get_files_for_stream(self,number_to_get):
        number_files_leftover = self._get_number_of_left_over_files()
        if number_to_get == -1:
            number_to_get = number_files_leftover

        if not (number_to_get <= number_files_leftover):
            self.logger.error("Given Number '{}' is higher than number of leftover '{}' files to get.".format(number_to_get, number_files_leftover), exc_info=self._logger_traceback)
            return False, False

        files_to_read_non_zip = []
        files_from_zips_to_read_orig = defaultdict(list)
        
        getted_number = 0
        while getted_number< number_to_get:
            try:
                files_to_read_non_zip.append(self.files_to_read_leftover.pop()) 
                getted_number += 1
            except IndexError:
                try:
                    for k in self.files_from_zips_to_read_left_over.keys():
                        #if len(l[k]) != 0:
                        files_from_zips_to_read_orig[k].append( self.files_from_zips_to_read_left_over[k].pop() )
                        getted_number += 1
                        break
                except IndexError:
                    del self.files_from_zips_to_read_left_over[k]

        return files_to_read_non_zip, files_from_zips_to_read_orig






    def _getlazy_single(self,colnames=False, encoding="utf-8", csvdelimiter=',', input_path_list=False, input_zip_file_list=False):        
        len_unzipped_files = len(input_path_list) if input_path_list else 0 
        len_zipped_files = sum([len(v) for v in input_zip_file_list.values() ]) if input_zip_file_list else 0
        length = len_unzipped_files + len_zipped_files
        gen = self.getgenerator(colnames=colnames, encoding=encoding, csvdelimiter=csvdelimiter, input_path_list=input_path_list, input_zip_file_list=input_zip_file_list)
        #p(type(gen))
        return LenGen(gen, length)



##################################################################################
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


    def _get_col_and_values_from_fname(self, fname, compiled_regex_for_fname):
        try:
            col_and_values_dicts = {}
            try:
                for m in compiled_regex_for_fname.finditer(fname):
                    for k,v in m.groupdict().iteritems():
                        if v.isdigit():
                            col_and_values_dicts[unicode(k)]= int(v)
                        elif isinstance(v, (int, float)):
                            col_and_values_dicts[unicode(k)]= v
                        else:
                            col_and_values_dicts[unicode(k)]= unicode(v)

                #p(col_and_values_dicts)
                #col_and_values_dicts = [{unicode(k): unicode(v) for k,v in m.groupdict().iteritems()} for m in compiled_regex_for_fname.finditer(fname)]
            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("RegexError: RegexDictExtractor throw following Error: '{}'. ".format(e), exc_info=self._logger_traceback)
                return False
            #col_and_values_dicts = [m.groupdict() for m in compiled_regex_for_fname.finditer(fname)]
            #p(col_and_values_dicts)
            if  len(col_and_values_dicts)==0:
                self.logger.critical("ColumnsExctractionFromFileNameError: Some of the columns in the given Fname '{}' wasn't detected. Following RegEx-Expression was used: '{}'. ".format(fname,self._regex_for_fname))
                return False

            return col_and_values_dicts
        except Exception as  exception:
            print_exc_plus() if self._ext_tb else ""
            self.logger.critical("ColumnsExctractionFromFileNameError: Following Error was raised: '{}'. ".format(repr(exception)))
            return False


    def _validation_regex_treatment(self):
        if self._regex_template and self._regex_for_fname:
            self.logger.error("InputValidationError: Template for Regex and Regex_for_Fname was given parallel. Please give just one of them.", exc_info=self._logger_traceback)
            return False

        if self._file_format == "txt":
            if not self._regex_template and not self._regex_for_fname:
                self.logger.error("InputValidationError: Template_for_Regex or Regex_for_Fname wasn't given. Please give one of them.", exc_info=self._logger_traceback)
                return False

            if self._regex_template and ( self._regex_template.lower() not in Reader.regex_templates):
                self.logger.error("InputValidationError: Given RegexTemplateName '{}' is not supporting! ".format(self._regex_template.lower()), exc_info=self._logger_traceback)
                return False

            if self._regex_for_fname and  not isinstance(self._regex_for_fname, (str, unicode)):
                self.logger.error("InputValidationError: RegexForFname should be an str or unicode object. Given: '{}'.".format(self._regex_for_fname), exc_info=self._logger_traceback)
                return False

            if self._regex_template and not self._regex_for_fname:
                try:
                    self._regex_for_fname = Reader.regex_templates[self._regex_template]
                    ### set given id_field_name
                    self._regex_for_fname = self._regex_for_fname.replace("id", self._id_field_name)
                    self._compiled_regex_for_fname = regex.compile(self._regex_for_fname, regex.UNICODE)

                except Exception, e:
                    print_exc_plus() if self._ext_tb else ""
                    self.logger.error("InputValidationError: Given RegEx-Template '{}' is not exist or it wasn't possible to compile it. Check this Exception: '{}'. ".format(self._regex_template, e), exc_info=self._logger_traceback)
                    return False

            elif not self._regex_template and self._regex_for_fname:
                try:
                    self._compiled_regex_for_fname = regex.compile(self._regex_for_fname, regex.UNICODE)

                except Exception, e:
                    print_exc_plus() if self._ext_tb else ""
                    self.logger.error("InputValidationError: Given RegEx-Template '{}' is not exist or it wasn't possible to compile it.  Check this Exception: '{}'.".format(self._regex_template, e), exc_info=self._logger_traceback)
                    return False



        return True





    # def _extract_colnames_from_regex(self, regex_for_fname):
    #     p(repr(regex_for_fname), c="m")
    #     columns_name = regex.findall(regex_for_fname, fname.strip())
    #     p(columns_name, c="r")
    #     if not isinstance(columns_name, list) or len(columns_name)==0 or len(columns_name[0])<5:
    #         self.logger.critical("ColumnsExctractionFromFileNameError: Some of the columns in the given Fname '{}' wasn't detected. Following RegEx-Expression was used: '{}'. ".format(fname,regex_for_fname))
    #         return False


    #     return columns_name

 
    def _get_data_from_dic_for_given_keys(self, colnames_to_extract, given_row_data ):
        if  isinstance(colnames_to_extract, list):
            outputdict = {}
            if given_row_data:
                for col in  colnames_to_extract:
                    if col in given_row_data:
                        outputdict[col] =given_row_data[col]
                        #p(outputdict)
                    else:
                        self.logger.critical("ColumnsGetter: '{}'-Column wasn't found in the given Structure and was ignored.".format(col))
                
                return outputdict
        else:
            self.logger.error("ColumnsGetterError: Given 'colnames_to_extract' are not from type 'list' ", exc_info=self._logger_traceback)
            return {}




    def _readTXT(self, inp_object,encoding="utf-8", columns_extract_from_fname=True, colnames=False,  string_was_given=False):
        try:
            if isinstance(inp_object, (unicode,str)):
                if not  os.path.isfile(inp_object):
                    self.logger.error("TXTFileNotExistError: Following File wasn't found: '{}'. ".format(inp_object), exc_info=self._logger_traceback)
                    return False
                else:
                    f = open(inp_object, "r")
                    as_file_handler = False
            else:
                f = inp_object
                as_file_handler = True
                #data = json.load(f) 

            if columns_extract_from_fname:
                #file = open(inp_object, "r")
                #f = codecs.open(inp_object, "r", encoding=encoding)
                fname = os.path.splitext(os.path.basename(f.name))
                output_data = self._get_col_and_values_from_fname(fname[0],self._compiled_regex_for_fname)
                #p(output_data)
                if not output_data or not isinstance(output_data, dict):
                    self.logger.critical("ReadTXTError: '{}' wasn't readed.".format(fname))
                    return {}
                file_data = f.read().decode(encoding)


                output_data.update({self._text_field_name:file_data})
                try:
                    f.close()
                    del f
                except:
                    pass
                    
                if colnames:
                    return self._get_data_from_dic_for_given_keys(colnames, output_data)
                else:
                    return output_data
            else:
                self.logger.error("ReadTXTError: Other sources of Columns as from FName are not implemented!", exc_info=self._logger_traceback)
                return False 

        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("TXTReaderError: Following Exception was throw: '{}'. ".format(e), exc_info=self._logger_traceback)
            return False
            #return


    def _readCSV(self, inp_object,encoding="utf_8", delimiter=',', colnames=False,  string_was_given=False,f_name=False):
        try:
            if isinstance(inp_object, (unicode,str)):
                if not  os.path.isfile(inp_object):
                    self.logger.error("CSVFileNotExistError: Following File wasn't found: '{}'. ".format(inp_object), exc_info=self._logger_traceback)
                    yield False
                    return
                else:
                    f = open(inp_object, "r")
                    as_file_handler = False
                    f_name = f_name if f_name else f.name
            else:
                f = inp_object
                try:
                    f_name = f_name if f_name else f.name 
                except:
                    f_name = None
                as_file_handler = True

            delimiter = str(delimiter)
            readCSV = unicodecsv.DictReader(f, delimiter=delimiter, encoding=encoding)

            if self._formatter_name == "sifter":
                #readCSV.fieldnames = [col.lower() for col in readCSV.fieldnames]
                #p(readCSV.fieldnames, "readCSV.fieldnames")
                fieldnames = readCSV.fieldnames if readCSV.fieldnames else readCSV.unicode_fieldnames
                cleaned = [col.lower().replace("[m]", " ").strip().strip(":").strip("_") for col in fieldnames]
                readCSV.unicode_fieldnames = cleaned

            #readCSV.renew_fieldnames()
                    #sys.exit()

            #p(dict(readCSV), "readCSV")

            to_check = True
            for row_dict in readCSV:
                if self._formatter_name:
                    if self._formatter_name in Reader.reader_supported_formatter["csv"]:
                        #readCSV.fieldnames = [col.lower() for col in readCSV.fieldnames]
                        #p(readCSV.fieldnames, "readCSV.fieldnames")
                        #fieldnames = readCSV.fieldnames if readCSV.fieldnames else readCSV.unicode_fieldnames
                        #cleaned = [col.lower().replace("[m]", " ").strip().strip(":").strip("_") for col in fieldnames]
                        #readCSV.unicode_fieldnames = cleaned
                        row_dict = self._csv_sifter_formatter(row_dict,f_name=f_name)
                        if row_dict == -10:
                            yield -10

                            return 
                    else:
                        self.logger.critical("CSVReaderError: Given '{}'-FormatterName is invalid for CSVFiles. Please choice one of the following: '{}'. Execution of the Program was stopped. (fname: '{}')".format(self._formatter_name, Reader.reader_supported_formatter["csv"], f_name))
                        yield -10
                        return

                try:
                    if to_check:
                        to_check = False
                        if None in  row_dict.keys():
                            #raise Exception
                            self.logger.error("CSVReaderError: The structure of the given File is invalid. Probably wrong 'csvdelimiter'  was given. Please try other one. (given csvdelimiter: '{}') (fname: '{}')  ".format(delimiter,f_name))
                            yield -10
                            return
                        if len(row_dict) <=2 or row_dict.keys()<=2:
                            self.logger.critical("CSVReaderError: Probably the structure of the given File is wrong or File contain just few items.  Probably wrong 'csvdelimiter'  was given. Please check the correctness of the given CSV File and give right csvdelimiter. (given csvdelimiter: '{}') (fname: '{}')  ".format(delimiter, f_name))
                        
                except AttributeError as e:
                    self.logger.error("Returned Row is not an Dict. Probably Wrongs Structure of the current CSVFileName: '{}'".format(f_name), exc_info=self._logger_traceback)
                    yield -10 
                    return 





                #p(row_dict, "row_dict")


                if row_dict:
                    if (self._text_field_name not in row_dict) or (self._id_field_name not in row_dict):
                        if not self._log_content:
                            keys = ":HidedContent:"
                        else:
                            keys = row_dict.keys()
                        #p(self._formatter_name, "self._formatter_name")
                        if self._formatter_name:
                            self.logger.error("CSVReader: Given CSV '{}' has wrong structure. Text or Id element wasn't found.\n Reasons:\n  1) Probably wrong 'text_field_name' and 'id_field_name' was given. (text_field_name: '{}'; id_field_name: '{}'); If this tags are wrong please use options and set right tags name.\n\n  Following columns was found: '{}'.".format(f.name,self._text_field_name,self._id_field_name, keys ))
                        else:
                            self.logger.error("CSVReader: Given CSV '{}' has wrong structure. Text or Id element wasn't found.\n Reasons:\n  1) Probably wrong 'text_field_name' and 'id_field_name' was given. (text_field_name: '{}'; id_field_name: '{}'); If this tags are wrong please use options and set right tags name.\n 2) 'formatter_name'-Option wasn't given. If this CSV has contain Tweets, which comes  from Sifter/TextDiscovery-Services than please set 'sifter' to  'formatter_name'-Option. \n\n  Following columns was found: '{}'.".format(f.name,self._text_field_name,self._id_field_name, keys ))
                            
                        #self.logger.error()
                        yield -10
                        return 

                if colnames:
                    yield self._get_data_from_dic_for_given_keys(colnames, row_dict)
                else:
                    yield row_dict

            try:
                f.close()
                del f
            except:
                pass

        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("CSVReaderError: Following Exception was throw: '{}'.  For following File: '{}'.".format(e, f_name), exc_info=self._logger_traceback)
            yield False
            return



    def _csv_sifter_formatter(self, dict_row,f_name=False):
        #self.logger.info(repr(dict_row))
        try:
            ### Step 1:  Variables Initialization
            is_extended = None
            is_retweet = None
            is_answer = None
            t_id = dict_row["twitter_id"]
            t_created_at = dict_row["posted_time"]
            t_language = dict_row["language"]
            t_used_client = dict_row["source"]
            t_text = dict_row["text"]
            u_created_at = None
            u_description = dict_row["user_bio_summary"]
            u_favourites = dict_row["favorites_count"]
            u_followers = dict_row["followers_count"]
            u_friends = dict_row["friends_count"]
            u_id = dict_row["user_id"].split(":")[-1]
            u_lang = dict_row["actor_languages"]
            u_given_name = dict_row["real_name"]
            u_username = dict_row["username"]
            u_verified = dict_row["user_is_verified"]
            u_location = dict_row["user_location"]

            try:
                t_id = int(t_id)
                u_id = int(u_id)
            except:
                self.logger.error("CSVIDConverter: It wasn't possible to convert IDs into integer. Probably illegal CSV Structure.")
                return -10


            ### Initialization fron new Tweet-Dict
            new_structure = {}            
            ## main paarameters
            new_structure[self._id_field_name] = t_id
            new_structure["t_created_at"] = t_created_at if t_created_at else None
            new_structure["t_language"] = t_language
            new_structure["t_used_client"] = t_used_client 
            new_structure[self._text_field_name] = t_text
            new_structure["u_created_at"] = u_created_at
            new_structure["u_description"] = u_description if u_description else None
            new_structure["u_favourites"] = u_favourites
            new_structure["u_followers"] = u_followers
            new_structure["u_friends"] = u_friends
            new_structure["u_id"] = u_id
            new_structure["u_lang"] = u_lang 
            new_structure["u_given_name"] = u_given_name
            new_structure["u_username"] = u_username
            new_structure["u_verified"] = u_verified 
            new_structure["u_location"] = u_location if u_location else None

            # additional parameters
            new_structure["is_extended"] = is_extended
            new_structure["is_retweet"] = is_retweet
            new_structure["is_answer"] = is_answer

            return new_structure
        except KeyError as e:
            if not self._log_content:
                #data = data
                dict_row = ":HidedContent:"
            self.logger.error("CSVReaderKeyError: Current CsvFile was ignored '{}', probably because it is not valid/original SifterCSVFile. Or the wrong delimiter was given. See Exception: '{}'.\n  ContentOfTheCsvElement: '{}' ".format(f_name, repr(e), dict_row), exc_info=self._logger_traceback)
            #p(dict_row.items(), "dict_row")
            #sys.exit()
            return -10
        except Exception as e:
            #p(dict_row.items(), "dict_row")
            
            if not self._log_content:
                dict_row = ":HidedContent:"
            self.logger.error_insertion("CSVReaderError: For current File '{}' following Exception was throw: '{}'.  DataContent: '{}' ".format(f_name, repr(e), dict_row), exc_info=self._logger_traceback)
            #p(dict_row.items(), "dict_row")
            #sys.exit()
            return -10





    def _readXML(self, inp_object,encoding="utf_8", colnames=False, string_was_given=False):
        try:
            if isinstance(inp_object, (unicode,str)):
                if not  os.path.isfile(inp_object):
                    self.logger.error("XMLFileNotExistError: Following File wasn't found: '{}'. ".format(inp_object), exc_info=self._logger_traceback)
                    yield False
                    return
                else:
                    f = open(inp_object, "r")
                    as_file_handler = False
            else:
                f = inp_object
                as_file_handler = True

            tree = ET.parse(inp_object)
            root = tree.getroot()
            self.xmlroottag = root.tag
            #root.attrib
            for child in root:
                row_dict = {}
                if not self.xmlchildetag:
                    self.xmlchildetag = child.tag

                if self.xmlchildetag != child.tag:
                    self.logger.critical("XMLReaderError: Child Tags in the the XML-root are different and was ignored. ('{}'!='{}')".format(self.xmlchildetag, child.tag))
                    break
                
                # collect all columns into dict from the current child
                for column in child:
                        row_dict[column.tag] = column.text
                if row_dict:
                    if (self._text_field_name not in  row_dict) or self._id_field_name not in row_dict:
                        self.logger.outsorted_reader("XMLReader: Given XML '{}' has wrong structure. Not one text or id element was found.".format(f.name))
                        yield -10
                        return 

                if colnames:
                    yield self._get_data_from_dic_for_given_keys(colnames, row_dict)
                else:
                    yield row_dict

            try:
                f.close()
                del f
            except:
                pass


        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("XMLReaderError: Following Exception was throw: '{}'.  For following File: '{}'.".format(e, f.name), exc_info=self._logger_traceback)
            yield False
            return


    def _json_tweets_preprocessing(self, data,f_name=False):
        try:
            if isinstance(data, dict):
                data = [data]
            output_json_list = []
            if isinstance(data, (list, tuple)):
                for json in data:
                    #p(json.keys())
                    output_json_list.append(self._clean_json_tweet(json))
                return output_json_list
            else:
                self.logger.critical("JsonTweetsPreparationError: Given '{}'-JSON-Type is from not right type.".format(type(data)))
                return {}
                #return 
        except KeyError as e:
            if not self._log_content:
                #data = data
                json = ":HidedContent:"
            self.logger.outsorted_reader("JSONReaderKeyError: Current JsonFile was ignored '{}', probably because it is not valid/original TwitterJSONFile. See Exception: '{}'.  ContentOfTheJsonElement: '{}' ".format(f_name, repr(e), json), exc_info=self._logger_traceback)
            return {}
        except Exception as e:
            if self._log_content:
                data = data
            else:
                data = ":HidedContent:"
            self.logger.error_insertion("JSONReaderError: For current File '{}' following Exception was throw: '{}'.  DataContent: '{}' ".format(f_name, repr(e), data), exc_info=self._logger_traceback)
            return {}

    def _clean_json_tweet(self, json_tweet):
        #self.logger.info(repr(json_tweet))
        
        #sys.exit()

        ### Step 1:  Variables Initialization
        is_extended = False
        is_retweet = False
        is_answer = False
        t_id = json_tweet["id"]
        t_created_at = json_tweet["created_at"]
        t_language = json_tweet["lang"]
        t_used_client = json_tweet["source"]
        t_text = json_tweet["text"]
        u_created_at = json_tweet["user"]["created_at"]
        u_description = json_tweet["user"]["description"]
        u_favourites = json_tweet["user"]["favourites_count"]
        u_followers = json_tweet["user"]["followers_count"]
        u_friends = json_tweet["user"]["friends_count"]
        u_id = json_tweet["user"]["id"]
        u_lang = json_tweet["user"]["lang"]
        u_given_name = json_tweet["user"]["name"]
        u_username = json_tweet["user"]["screen_name"]
        u_verified = json_tweet["user"]["verified"]
        u_location = json_tweet["user"]["location"]


        ### Initialization fron new Tweet-Dict
        new_structure = {}

        # Step 2: Extraction of the additional Information
        # "extended_tweet"."full_text" ( 280>len(text)>140)
        if "extended_tweet" in json_tweet:
            t_text = json_tweet["extended_tweet"]["full_text"]
            #p(json_tweet["extended_tweet"])
            is_extended = True

        if "retweeted_status" in json_tweet:
            #p(json_tweet)
            #p(json_tweet["retweeted_status"])
            is_retweet = True
            if self._ignore_retweets:
                self.retweet_counter.incr()
                self.logger.outsorted_reader("RetweetIgnoring: Retweet with ID:'{}' was ignored. ".format(json_tweet["id"]))
                #self.logger.warning("RetweenIgnoring: Current RETweet with ID='{}' was ignored. (for allowing retweets please use 'ignore_retweets' option.)".format(json_tweet["id"]))
                return {}


        if "quoted_status" in json_tweet:
            #p(json_tweet)
            #p(json_tweet["quoted_status"])
            is_answer = True


        # Step 3: Write into new Object
        
        ## main paarameters
        new_structure[self._id_field_name] = t_id
        new_structure["t_created_at"] = t_created_at
        new_structure["t_language"] = t_language
        new_structure["t_used_client"] = t_used_client
        new_structure[self._text_field_name] = t_text
        new_structure["u_created_at"] = u_created_at
        new_structure["u_description"] = u_description
        new_structure["u_favourites"] = u_favourites
        new_structure["u_followers"] = u_followers
        new_structure["u_friends"] = u_friends
        new_structure["u_id"] = u_id
        new_structure["u_lang"] = u_lang 
        new_structure["u_given_name"] = u_given_name
        new_structure["u_username"] = u_username
        new_structure["u_verified"] = u_verified 
        new_structure["u_location"] = u_location 

        # additional parameters
        new_structure["is_extended"] = is_extended
        new_structure["is_retweet"] = is_retweet
        new_structure["is_answer"] = is_answer

        return new_structure
        # except Exception, e:
        #     p(json_tweet.keys())
        #     self.logger.error(str(repr(e)), exc_info=self._logger_traceback)
        #     sys.exit()
        #     #p(json_tweet)




    def _readJSON(self, inp_object, encoding="utf_8", colnames=False, str_to_reread=False ):
        try: 
            #p(inp_object, "inp_object")
            #p(raw_str, "raw_str")
            if not  str_to_reread:
                if isinstance(inp_object, (str,unicode)):
                    if not  os.path.isfile(inp_object):
                        self.logger.error("JSONFileNotExistError: Following File wasn't found: '{}'. This File was ignored.".format(inp_object), exc_info=self._logger_traceback)
                        yield {}
                        return 
                        #return 
                    else:
                        f = open(inp_object, "r")
                        as_file_handler = False
                        raw_str = f.read()
                        f_name = f.name
                else:
                    f = inp_object
                    raw_str = f.read()
                    as_file_handler = True
                    f_name = str(f)
            else:
                raw_str = str_to_reread
                f_name = None
            #inp_object + {}
            #del data
            temp_json_data = json.loads(raw_str)
            if len(temp_json_data) == 0:
                self.logger.outsorted_reader("JSONReader: Given JSON '{}' is empty.".format(f.name))
                yield {}
                return 

            if self._formatter_name:
                if self._formatter_name in Reader.reader_supported_formatter["json"]:
                    try:
                        temp_json_data = self._json_tweets_preprocessing(temp_json_data,f_name=f_name)

                        if len(temp_json_data) == 0:
                            self.logger.debug("TweetsPreprocessing out-sorted current file: '{}' .".format(f.name))
                            yield {}
                            return 
                    except Exception, e:
                        self.logger.error("JSONReader: Exception encountered during cleaning Twitter-JSON. This File was ignoren. Exception: '{}'.".format(repr(e)))
                        yield {}
                        return 
                else:
                    self.logger.critical("JSONReaderError: Given '{}'-FormatterName is not supported for JSONFormat. Please choice one of the following: '{}'. Execution of the Program was stopped- ".format(self._formatter_name, Reader.reader_supported_formatter["json"]))
                    yield -10
                    return

            if isinstance(temp_json_data, dict):
                temp_json_data = [temp_json_data]

            for row_dict in temp_json_data:
                if row_dict:
                    if (self._text_field_name not in  row_dict) or self._id_field_name not in row_dict:
                        self.logger.outsorted_reader("JSONReader: Given JSON '{}' has wrong structure. Not one text or id element was found.".format(f.name))
                        yield -10
                        return 

                if colnames: 
                    yield self._get_data_from_dic_for_given_keys(colnames, row_dict)
                else:
                    yield row_dict 
            try:
                f.close()
                del f
            except:
                pass

        except ValueError, e: # this was implemented, because twitter streamer send sometimes inconsistent tweets, where json is not correct
            print_exc_plus() if self._ext_tb else ""
            if not str_to_reread:
                try:
                    splitted = raw_str.split("}{")
                    if len(splitted) > 1:
                        temp_items = []
                        for item in splitted:
                            if item[0] != "{":
                                item= "{{{}".format(item)
                            if item[-1]!= "}":
                                item= "{}}}".format(item)
                            temp_items.append(json.loads(item))
                        json_str = json.dumps(temp_items)
                        #self.logger.critical(temp_items)
                        #self.logger.critical(json_str)
                        #sys.exit()
                        for row in self._readJSON(inp_object, encoding=encoding, colnames=colnames, str_to_reread=json_str):
                            yield row
                    self.logger.healed("JSONDoktorSuccess: 'not-valid'-JSON File was getted: '{}'. It was possible to heal it up. ".format(f.name))

                except Exception, e:
                    self.logger.error("JSONDoktorError: It wasn't possible to heal up current 'not-valid'-JSON File: '{}' (was ignored)\n --->See Exception:  '{}';\n --->DataFromFile:'{}'; \n".format(f.name, e, raw_str), exc_info=self._logger_traceback)
            else:
                raw_str= raw_str if self._log_content else "log_content is disable. Switch on this Option, if you want see file data here"
                if "Expecting , delimiter" in str(e) or "No JSON object could be decoded" in str(e):
                    self.logger.error_insertion("JSONReaderError: Current File is not valid JSON: ('{}' was ignored)\n --->See Exception:  '{}';\n --->DataFromFile:'{}'; \n".format(f.name, e, raw_str), exc_info=self._logger_traceback)
                elif "Extra data"  in str(e):
                    self.logger.error_insertion("JSONReaderError: Probably inconsistent JSON File. ('{}' was ignored)\n --->See Exception:  '{}';\n --->DataFromFile:'{}'; \n".format(f.name, e, raw_str), exc_info=self._logger_traceback)
                else:
                    self.logger.error_insertion("JSONReaderError:  ('{}' was ignored)\n --->See Exception:  '{}';\n --->DataFromFile:'{}'; \n".format(f.name, e, raw_str), exc_info=self._logger_traceback)
        #except AttributeError,e:

        except Exception, e:
            #p(f,"f")

            try:
                if isinstance(f, (unicode, str)):
                    fname = f
                else:
                    fname = f.name
            except AttributeError:
                fname = f

            print_exc_plus() if self._ext_tb else ""
            self.logger.error("JSONReaderError: For current File '{}' following Exception was throw: '{}'. ".format(fname, e), exc_info=self._logger_traceback)



    def _validation_given_path(self):
        if not os.path.isdir(self._inp_path):
            self.logger.error("ValidationError: Given PathToCorpus is not exist: '{}'. ".format(self._inp_path), exc_info=self._logger_traceback)
            return False

        return True


    def _validate_given_file_format(self):
        if self._file_format.lower() not in Reader.supported_file_types:
            self.logger.error("ValidationError: Given FileFormat '{}' is not supported by this Reader.".format(self._file_format.lower()), exc_info=self._logger_traceback)
            return False

        return True



    def _extract_all_files_according_given_file_format(self):
        #p(self._read_from_zip, "read_from_zip")
        try:
            output_path_to_file = []
            #self.files_to_read_orig = []
            #self.zips_to_read = []
            
            for root, dirs, files in os.walk(self._inp_path, topdown=False):
                for name in files:
                    #p(  name)
                    if "."+self._file_format in name.lower():
                        self.files_to_read_orig.append(os.path.join(root, name))
                        #print root, name
                    if self._read_from_zip:
                        if ".zip" in name.lower():
                            self.zips_to_read.append(os.path.join(root, name))
                            #print root, name

            if len(self.files_to_read_orig)==0 and len(self.zips_to_read)==0:
                #p((self._inp_path))
                self.logger.warning("FilesExtractionProblem: No '{}'-Files or ZIPs was found. (check given FileFormat or given path to text collection).".format(self._file_format))
                #return self.files_to_read_orig
            self.files_to_read_leftover = copy.deepcopy(self.files_to_read_orig)
            #p(read_from_zip, "444read_from_zip")
            #p(self._read_from_zip, "read_from_zip")
            if self._read_from_zip:
                for path_to_zip in self.zips_to_read:
                    archive = zipfile.ZipFile(path_to_zip, 'r')
                    for name in  archive.namelist():
                        if "."+self._file_format in name:
                            #f = archive.open(name)
                            self.files_from_zips_to_read_orig[path_to_zip].append(name)


                self.files_from_zips_to_read_left_over = copy.deepcopy(self.files_from_zips_to_read_orig)

            self.logger.info("FilesExtraction: '{}' '{}'-Files (unzipped) was found in the given folder Structure: '{}'. ".format(len(self.files_to_read_orig),self._file_format, self._inp_path))
            #p(repr(self._read_from_zip), "------1-1-1-1-read_from_zip")
            if self._read_from_zip:
                if self.zips_to_read:
                    self.files_number_in_zips = sum([len(v) for v in self.files_from_zips_to_read_orig.values() ])
                    self.logger.info("ZIPsExtraction: Additional it was found '{}' ZIP-Archives, where '{}' '{}'-Files was found.".format(len(self.zips_to_read), self.files_number_in_zips,self._file_format))
                
            self.files_at_all_was_found =  len(self.files_to_read_orig) + self.files_number_in_zips
            self.files_from_zips_to_read_left_over = copy.deepcopy(self.files_from_zips_to_read_orig)
            self.files_to_read_leftover = copy.deepcopy(self.files_to_read_orig)

        except Exception, e:
            self.logger.error("FilesExtractionError: Encountered Exception '{}'. ".format(e), exc_info=self._logger_traceback)
            return False   





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



