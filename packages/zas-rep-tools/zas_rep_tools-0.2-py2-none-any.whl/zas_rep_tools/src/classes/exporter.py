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
from __future__ import absolute_import


import os
#import copy
import sys
#import regex
import logging
#import collections
#import types
import csv
#import unicodecsv as csv
import codecs
from lxml import etree as ET
import json
import inspect
import traceback
import re
import gc

from collections import defaultdict
from raven import Client

from zas_rep_tools.src.utils.helpers import set_class_mode, print_mode_name, LenGen, path_to_zas_rep_tools,instance_info, SharedCounterExtern, SharedCounterIntern, Status, function_name
from zas_rep_tools.src.classes.dbhandler import DBHandler
from zas_rep_tools.src.utils.zaslogger import ZASLogger
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.error_tracking import initialisation
from zas_rep_tools.src.utils.traceback_helpers import print_exc_plus
from zas_rep_tools.src.classes.basecontent import BaseContent



import platform
if platform.uname()[0].lower() !="windows":
    import colored_traceback
    colored_traceback.add_hook()
else:
    import colorama


class Exporter(BaseContent):

    supported_file_formats = ["csv", "json", "sqlite",  "xml"]
    unsupported_file_formats = ["txt",]

    def __init__(self, inpdata, rewrite=False, silent_ignore=False,**kwargs):
        super(type(self), self).__init__(**kwargs)


        #Input: Encapsulation:
        self._inpdata = inpdata
        self._rewrite = rewrite
        self._silent_ignore = silent_ignore
        

        #InstanceAttributes: Initialization
        self._used_fnames = {}
        self.sqlite_db = False
        self._numbers_of_alredy_created_files = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self._number_of_inserts_in_the_current_file = 0

        self.logger.debug('Intern InstanceAttributes was initialized')


        if not self._eval_input_data():
            sys.exit()


        self.logger.debug('An instance of Exporter() was created ')


        ## Log Settings of the Instance
        self._log_settings(attr_to_flag = False,attr_to_len = False)



        ############################################################
        ####################__init__end#############################
        ############################################################

    # def __del__(self):
    #     super(type(self), self).__del__()

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





    def tocsv(self, path_to_export_dir , fname, fieldnames,  rows_limit_in_file=50000, encoding="utf-8"):
        self.current_csvfile = False
        rows_was_exported = 0
        #p((len(self._inpdata), self._inpdata))
        #p("NEW\n\n", "NEW", c="r")
        #if 

        #p((path_to_export_dir , fname, fieldnames,  rows_limit_in_file))
        #p(self._inpdata)
        for row in self._inpdata:
            #p("333")
            if not row:
                continue
            #p(row, "row")
            if row == -1:
                continue
            #p(row)
            try:
                if not self._write_to_csv_files(row, fieldnames, path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file, encoding=encoding):
                    if self._silent_ignore:
                        self.logger.debug("toCSV: File is already exist and extraction was aborted. ('silent_ignore' is 'on')")
                    else:    
                        self.logger.info("toCSV: Test Files are already exist. Extraction to_csv was stopped. Please remove those files or use 'rewrite' option. ")
                    return False
                
                rows_was_exported += 1
            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("CSVWriterError: Not possible to Export into CSV. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
                return False
        #p(self.current_csvfile, "000self.current_csvfile")
        if self.current_csvfile:
            self.current_csvfile.close()
            del self.current_csvfile
            self.logger.info("CSVWriter: '{}' rows  was exported into CSV File(s) in '{}'.".format(rows_was_exported,path_to_export_dir))
            #p(self.current_csvfile, "11self.current_csvfile")
            return True
        else:
            self.logger.error("No File was exported. Probably Data for export was empty.")
            #p(self.current_csvfile, "22self.current_csvfile")
            return False







    def toxml(self, path_to_export_dir , fname, rows_limit_in_file=50000, encoding="utf-8", root_elem_name="Docs", row_elem_name="Doc"):
        self.current_xmlfile = False
        rows_was_exported = 0
        for row in self._inpdata:
            if row == -1:
                continue
            try:
                if not self._write_to_xml_files(row,  path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file, encoding=encoding, root_elem_name=root_elem_name, row_elem_name=row_elem_name):
                    if self._silent_ignore:
                        self.logger.debug("toXML: File is already exist and extraction was aborted. ('silent_ignore' is 'on')")
                    else:    
                        self.logger.info("toXML: Test Files are already exist. Extraction to_json was stopped. Please remove those files or use 'rewrite' option. ")
                    #p("ghjkl")
                    return False
                rows_was_exported += 1
            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("XMLWriterError: Not possible to Export into XML. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
                return False
        #to save all last data
        self._save_output_into_current_xml_file()
        self.logger.info("XMLWriter: '{}' rows  was exported into XML File(s) in '{}'.".format(rows_was_exported,path_to_export_dir))
        return True



    def tojson(self, path_to_export_dir , fname, rows_limit_in_file=50000, encoding="utf-8", unicode_encode=True):
        self.current_jsonfile = False
        rows_was_exported = 0
        for row in self._inpdata:
            if row == -1:
                continue
            try:
            #p((row,  path_to_export_dir, fname))
                if not self._write_to_json_files(row,  path_to_export_dir, fname, rows_limit_in_file=rows_limit_in_file, encoding=encoding, unicode_encode=unicode_encode):
                    if self._silent_ignore:
                        self.logger.debug("toJSON: File is already exist and extraction was aborted. ('silent_ignore' is 'on')")
                    else:    
                        self.logger.info("toJSON: Test Files are already exist. Extraction to_json was stopped. Please remove those files or use 'rewrite' option. ")
                    return False
                rows_was_exported += 1

            except Exception, e:
                print_exc_plus() if self._ext_tb else ""
                self.logger.error("JSONWriterError: Not possible to Export into JSON. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
                return False


        if self.current_jsonfile:
            self.current_jsonfile.seek(-1, os.SEEK_END)
            self.current_jsonfile.write("\n\n ]")
            self.current_jsonfile.close()
            del self.current_jsonfile
            self.logger.info("JSONWriter: '{}' rows  was exported into JSONS File(s) in '{}'.".format(rows_was_exported,path_to_export_dir))
            return True
        else:#
            self.logger.error("No File was exported. Probably Data for export was empty.")
            return False




    def tosqlite(self, path_to_export_dir, dbname, fieldnames,  encoding="utf-8", encryption_key=False, table_name= "Documents", attributs_names_with_types_as_str=False):
        self.current_jsonfile = False
        rows_was_exported = 0
        #p("fghjkl")
        if not  attributs_names_with_types_as_str:
            attributs_names_with_types_as_str = self._create_list_with_columns_and_types_for_sqlite(fieldnames)
            #p(attributs_names_with_types_as_str)

        if not os.path.isdir(path_to_export_dir):
            os.makedirs(path_to_export_dir)

        if not self.sqlite_db: 
            self.sqlite_db = DBHandler( rewrite=self._rewrite, stop_if_db_already_exist=True, logger_level= self._logger_level,logger_traceback=self._logger_traceback, logger_folder_to_save=self._logger_folder_to_save,logger_usage=self._logger_usage, logger_save_logs= self._logger_save_logs, mode=self._mode ,  error_tracking=self._error_tracking,  ext_tb= self._ext_tb) 
            
            if not self.sqlite_db.initempty(path_to_export_dir, dbname, encryption_key=encryption_key)["status"]:
                if self._silent_ignore:
                    self.logger.debug("toSQLLITE: File is already exist and extraction was aborted. ('silent_ignore' is 'on')")
                else:    
                    self.logger.info("toSQLITE: Test Files are already exist. Extraction to_json was stopped. Please remove those files or use 'rewrite' option. ")
                return False

            self.sqlite_db.addtable(table_name, attributs_names_with_types_as_str)

        for row in self._inpdata:
            if row == -1:
                continue
            #p(row)
            #try:
            self._write_to_sqliteDB(row,  path_to_export_dir, table_name,  encoding=encoding)
            rows_was_exported += 1

            # except Exception, e:
            #    self.logger.error("SQLITEWriterError: Not possible to Export into SQLITE-DB. Following Exception was throw: '{}'.".format(e), exc_info=self._logger_traceback)
            #    return False

        try:
            self.sqlite_db.close()
            del self.sqlite_db
        except Exception, e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("SQLITEWriterError: Following Exception was throw: '{}'. ".format(e), exc_info=self._logger_traceback)

        self.logger.info("SQLITEWriter: '{}' rows  was exported into SQLITE-DB in '{}'.".format(rows_was_exported,path_to_export_dir))
        return True






    def totxt(self):
        self.logger.error("TXTReader is not implemented!", exc_info=self._logger_traceback)
        sys.exit()



####################################################################################
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




    def _write_to_json_files(self,row_as_dict, path_to_dir, fname, rows_limit_in_file=50000, encoding="utf-8",unicode_encode=True):
        # check if current file has not more row as given rows limits
        

        if self.current_jsonfile:
            if self._number_of_inserts_in_the_current_file >= rows_limit_in_file:
                self.current_jsonfile.seek(-1, os.SEEK_END)
                self.current_jsonfile.write("\n\n ]")
                self.current_jsonfile.close()
                self._number_of_inserts_in_the_current_file = 0
                try:
                    self.current_jsonfile.close()
                    del self.current_jsonfile
                except:
                   pass
                self.current_jsonfile = self._get_new_file(path_to_dir , fname, "json", encoding=encoding, file_flag="a+", open_file_with_codecs=unicode_encode)
                if not self.current_jsonfile:
                    return False
                self.current_jsonfile.write("[ \n\n")
        
        else:
            self.current_jsonfile = self._get_new_file(path_to_dir , fname, "json", encoding=encoding, file_flag="a+", open_file_with_codecs=unicode_encode)
            #p(self.current_jsonfile, c="m")
            if not self.current_jsonfile:
                return False
            self.current_jsonfile.write("[ \n\n")


        #json.dump(row_as_dict, self.current_jsonfile,indent=4)
        json.dump(row_as_dict, self.current_jsonfile,indent=4, ensure_ascii=False)
        self.current_jsonfile.write(",")
        self._number_of_inserts_in_the_current_file += 1
        return True





    def _get_new_file(self, path_to_dir, fname, file_extention, encoding="utf-8", file_flag="w", open_file_with_codecs=False):
        #p(fname, "fname")
        if file_extention not in Exporter.supported_file_formats:
            self.logger.error("NewFileGetterError: Given file_format '{}' is not supported. Please use one of the following file formats: '{}'. ".format(file_extention,Exporter.supported_file_formats ), exc_info=self._logger_traceback)
            sys.exit()

        pattern = re.compile("^(.+)_\d{,4}\..+")
        matched_fname_current = pattern.findall(fname)
        #p(matched_fname_current, "matched_fname_current")
        matched_fname_current = matched_fname_current[0] if matched_fname_current else fname
        count_of_existing_files = self._numbers_of_alredy_created_files[path_to_dir][file_extention][matched_fname_current]
        new_fname_without_extention = fname+ "_{}".format(count_of_existing_files)
        new_fname_with_extention =new_fname_without_extention+ "." + file_extention
        path_to_file = os.path.join(path_to_dir, new_fname_with_extention)
        

        if not os.path.isdir(path_to_dir):
            os.makedirs(path_to_dir)
            self.logger.warning("NewFileGetterProblem: '{}' Folder are not exist. It was created.".format(path_to_file))
        
        else:

            if count_of_existing_files == 0:
                exist_fnames_in_dir = os.listdir(path_to_dir)
                exist_fnames_in_dir = set([pattern.findall(fname)[0] if pattern.findall(fname) else fname for fname in exist_fnames_in_dir])
                #p((fname,new_fname_without_extention,exist_fnames_in_dir),"fname")

                for exist_fname in  exist_fnames_in_dir:
                    matched_fname_from_listdir = pattern.findall(exist_fname)
                    matched_fname_from_listdir = matched_fname_from_listdir[0] if matched_fname_from_listdir else exist_fname
                    #if fname != "export":
                    if matched_fname_current == matched_fname_from_listdir:
                        if self._rewrite:
                            exist_fnames_in_dir = os.listdir(path_to_dir)
                            #for 
                            for exist_fname in  exist_fnames_in_dir:
                                matched = pattern.findall(exist_fname)
                                if matched:
                                    matched = matched[0]
                                    if matched == matched_fname_current:
                                        os.remove(os.path.join(path_to_dir, exist_fname))
                            #os.remove(os.path.join(path_to_dir, exist_fname))
                            self.logger.debug("NewFileRewriter: '{}' File is already exist and  was removed from '{}'.  ('rewrite'-option is enabled.)".format(exist_fname,  path_to_dir))
                        else:
                            if not self._silent_ignore:
                                self.logger.error("NewFileGetterProblem: '*{}*' NamePattern is already exist in '{}'-directory.  Please delete those files or give other fname, before you can process Export.".format(matched_fname_current,  path_to_dir))
                                return False
                            else:
                                self.logger.debug("NewFileGetter: '{}' NamePattern is already exist in '{}'-directory and was silent ignored.".format(matched_fname_current, path_to_file))
                            return False
        if open_file_with_codecs:
            current_file = codecs.open(path_to_file, 'w', encoding)
        else:
            current_file = open(path_to_file, file_flag)
        #p(current_file,  c="r")
        self._numbers_of_alredy_created_files[path_to_dir][file_extention][matched_fname_current] += 1
        # if file_extention == "csv":
        #     p(self._numbers_of_alredy_created_files,"222self._numbers_of_alredy_created_files")
        self.logger.debug("NewFileGetter: New File  '{}' was created in '{}'.".format(new_fname_with_extention, path_to_dir))
        return current_file




    
    def _write_to_csv_files(self, row_as_dict, fieldnames, path_to_dir , fname,  rows_limit_in_file=50000, encoding="utf-8"):
        # check if current file has not more row as given rows limits
        
        if self.current_csvfile:
            if self._number_of_inserts_in_the_current_file >= rows_limit_in_file:
                #self.current_csvfile.close()
                self._number_of_inserts_in_the_current_file = 0
                try:
                    self.current_csvfile.close()
                    del self.current_csvfile
                except:
                    pass
                self.current_csvfile = self._get_new_file(path_to_dir , fname, "csv", encoding=encoding)
                #p(self.current_csvfile, "self.current_csvfile")
                if not self.current_csvfile:
                    return False
                #p((self.current_csvfile, fieldnames))
                #self.current_csv_writer = csv.DictWriter(self.current_csvfile, fieldnames=fieldnames, encoding=encoding)
                self.current_csv_writer = csv.DictWriter(self.current_csvfile, fieldnames=fieldnames)
                self.current_csv_writer.writeheader()
        else:
            self.current_csvfile = self._get_new_file(path_to_dir , fname, "csv", encoding=encoding)
            #p(self.current_csvfile, "self.current_csvfile")
            if not self.current_csvfile:
                return False
            #self.current_csv_writer = csv.DictWriter(self.current_csvfile, fieldnames=fieldnames, encoding=encoding)
            self.current_csv_writer = csv.DictWriter(self.current_csvfile, fieldnames=fieldnames)
            self.current_csv_writer.writeheader()


        encoded_into_str = {}
        for k,v in row_as_dict.iteritems():
            if isinstance(k, unicode):
                k = k.encode(encoding)
            if isinstance(v, unicode):
                v = v.encode(encoding)
            encoded_into_str[k] = v
        #encoded_into_str = {k.encode(encoding): v.encode(encoding) for k,v in row_as_dict.iteritems()}
        #p(encoded_into_str)
        self.current_csv_writer.writerow(encoded_into_str)
        #self.current_csv_writer.close()
        #self.current_csv_writer.writerow(row_as_dict)
        self._number_of_inserts_in_the_current_file += 1
        return True


    def _write_row_to_xml(self,root_elem, row_as_dict, row_elem_name="Doc"):
        try:
            row_element = ET.SubElement(root_elem, row_elem_name)
            for col_name, value in row_as_dict.iteritems():
                # if "324114" in str(value):
                #     p((repr(value),col_name), c="r")
                tag = ET.SubElement(row_element, col_name)
                tag.text = unicode(value)
        except Exception as e:
            print_exc_plus() if self._ext_tb else ""
            self.logger.error("WriterRowIntoXMLError: Following Exception was throw: '{}'. ".format(repr(e)), exc_info=self._logger_traceback)
            return False

        return True


    def _save_output_into_current_xml_file(self):
        if self.current_xmlfile:
            tree = ET.ElementTree(self.current_xml_root_elem)
            output_xml = ET.tostring(tree, pretty_print=True, xml_declaration=True,  encoding="utf-8")
            #p(output_xml)
            self.current_xmlfile.write(output_xml)
            self.current_xmlfile.close()
            del self.current_xmlfile
            self.current_xmlfile = False
        else:
            self.logger.error("SaveOutputIntoXMLError: There is not activ XML-Files", exc_info=self._logger_traceback)
            return False
        return True


    def _write_to_xml_files(self,row_as_dict, path_to_dir, fname, rows_limit_in_file=50000, encoding="utf-8", root_elem_name="Docs", row_elem_name="Doc"):
        # check if current file has not more row as given rows limits
        #p(self.current_xmlfile)
        if self.current_xmlfile:
            if self._number_of_inserts_in_the_current_file >= rows_limit_in_file:
                self._save_output_into_current_xml_file()
                self._number_of_inserts_in_the_current_file = 0
                try:
                    self.current_xmlfile.close()
                    del self.current_xmlfile
                except:
                    pass
                self.current_xmlfile = self._get_new_file(path_to_dir , fname, "xml", encoding=encoding)
                if not self.current_xmlfile:
                    return False
        
                self.current_xml_root_elem = ET.Element(root_elem_name)

        else:
            self.current_xmlfile = self._get_new_file(path_to_dir , fname, "xml", encoding=encoding)
            if not self.current_xmlfile:
                return False
            self.current_xml_root_elem = ET.Element(root_elem_name)

        self._write_row_to_xml(self.current_xml_root_elem, row_as_dict,row_elem_name=row_elem_name)
        #self.current_xml_root_elem.writerow(row_as_dict)
        self._number_of_inserts_in_the_current_file += 1
        return True




    def _write_to_sqliteDB(self,row_as_dict, path_to_export_dir, tablename,  encoding="utf-8"):
        if not self.sqlite_db:
            self.logger.error("SQLITEWriterError: No Active DB to write in exist! Please Initialize first an Empty DB.", exc_info=self._logger_traceback)
            sys.exit()

        # col=[]
        # val=[]

        # for k, v in row_as_dict.iteritems():
        #     col.append(k)
        #     val.append(v)

        self.sqlite_db.lazyinsert(tablename,  row_as_dict)
        return True



    def _create_list_with_columns_and_types_for_sqlite(self, fieldnames):
        outputlist = []
        if isinstance(fieldnames, list):
            for colname in fieldnames:
                outputlist.append((colname,"TEXT"))
            return outputlist
        else:
            self.logger.error("SQLITECreaterError: Given Fieldnames are not from List Type.", exc_info=self._logger_traceback)
            return False




    def _eval_input_data(self):
        #p((isinstance(self._inpdata, list), isinstance(self._inpdata, types.GeneratorType)))
        import types
        check = (isinstance(self._inpdata, list), isinstance(self._inpdata, LenGen),isinstance(self._inpdata, types.GeneratorType))

        if True not in check:
            self.logger.error("InputValidationError: Given 'inpdata' is not iterable. ", exc_info=self._logger_traceback)
            return False


        return True







