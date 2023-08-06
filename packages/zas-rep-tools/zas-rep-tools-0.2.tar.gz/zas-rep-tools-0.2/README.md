 
# ZAS-REP-TOOLS

Current Tool was developed in the frame of the linguistics Study/Project *"The Pragmatic Status of Iconic Meaning in Spoken Communication: Gestures, Ideophones, Prosodic Modulations* ([PSIMS](http://www.zas.gwz-berlin.de/psims.html)) as the Bachelor Thesis.
___



* **Project Members:**
     - [Susanne Fuchs](mailto:fuchs@leibniz-zas.de)
     - [Aleksandra Ćwiek](mailto:cwiek@leibniz-zas.de)
     - [Egor Savin](mailto:work@savin.berlin)
     - [Cornelia Ebert](mailto:ebert@leibniz-zas.de)
     - [Manfred Krifka](mailto:krifka@leibniz-zas.de)



*  **Bachelor Thesis Appraisers:**
    - [Ulf Leser](mailto:leser@informatik.hu-berlin.de)  
    - [Susanne Fuchs](mailto:fuchs@leibniz-zas.de)  


* **Tool-Developer:**
    - [Egor Savin](mailto:work@savin.berlin)

---



**ZAS-REP-TOOLS** is a bundle of Tools for automatic extraction and quantification of the repetitions from the unstructured textual Data Collections for different languages with additional Search Engine wrapped around extracted data +  on-board supplied Twitter Streamer to collect real-time tweets. 

<sub> (This ReadMe still to be in the developing process and still has grammatical errors. Please ignore them=) But if you have  any suggestions of improvement please contact [Egor Savin](mailto:work@savin.berlin) ) </sub>



---

**<span style="color:red;">For a quick-start,</span>** first [download and install all dependencies](#dependencies) , then [install the tool](#settingup) and afterwards go to the [Workflow](#workflow)   and  [Tutorials](#tutorials) section to begin.

___


<br/>
<br/>


<a name="toc"/>

## Table of Contents

1. [Hardware Requirements](#requirements)

2. [Dependencies Installation](#dependencies)
    - On Linux 
    - On Windows 
    - On MacOS 

3. [Setting up](#settingup)

4. [Definitions](#definitions)
   -  Repetition
   -  Full Repetitiveness

5. [Functionality](#functionality)
   - [CLI-Commands](#cli-commands)
   - [CLI-Options](#cli-options)
   - [CLI-Usage](#cli-usage)
   - [Multiprocessing](#multiprocessing)
   - [NLP-Methods](#nlp-methods)
   - [InternDataBase-Structure](#db)
   -  [Additional Features](#additional_features)
        - Formatters
        - Templates

6. [WorkFlow](#workflow)

7. [Tutorials](#tutorials)
   - Python Package Tutorial 
   -  Command line Tutorial

8. [Input/Output](#input/output)
   - File Formats
   - Columns Explanation in the Output Tables

9. [Restrictions](#restrictions)

10. [Citing ZAS-REP-TOOLS](#citing)

11. [Possible errors and warnings](#errors)

12. [Data-Examples](#data)

13. [Acknowledgements](#acknowledgements)



<br/>

---
---
---
---

<br/>

<a name="requirements"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 1. Hardware Requirements
 


||  Minimum:    | Average:  |
|:--------------:   |:----------------: | :----------------:    |
| CPU | 2 Core 2 GHz | 4 Core 2.6 GHz  |
| RAM | 8 GB | 16 GB    |



<br/>



---
---
---
---

<br/>



<a name="dependencies"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 2. Dependencies


In order to use ZAS-REP-TOOLS you'll need the following installed Dependencies in addition to the source code provided here:

* [Python (both Versions: 2.7 + 3.5 or later)](https://www.python.org/download/releases/2.7.6>)
* [JAVA JDC](https://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase6-419409.html) 
* [GCC, the GNU Compiler Collection](http://gcc.gnu.org/install/download.html)
* [SQLite3](https://www.sqlite.org/download.html)
* [NoseTests](https://nose.readthedocs.io/en/latest/)
* [Pysqlcipher](https://github.com/leapcode/pysqlcipher)
* Git



#### Dependencies Installation 
following installation commands should be seeing as just an idea how and could become incorrect with time. Important is, that all above listed Dependencies are installed, before you can start to SetUp the Tool. 

<sub>*$ - symbol ensure the begin of the command, which should be copy-pasted into the terminal window.*</sub>

##### On Linux (UbuntuOS 16.04.5 LTS)
    0. open Terminal/Bash/Shell

    1. Add other repositories
        $  sudo add-apt-repository "deb http://archive.canonical.com/ubuntu saucy partner"
        $ sudo add-apt-repository "deb http://us.archive.ubuntu.com/ubuntu/ saucy universe multiverse"
        $ sudo add-apt-repository "deb http://us.archive.ubuntu.com/ubuntu/ saucy-updates universe multiverse"

    2. Upgrade default linux tools
        $ sudo apt-get update
        $ sudo apt-get upgrade

    3. Install additional SW
        $ sudo apt-get install python-setuptools python-dev  build-essential autoconf libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk  libtool pkg-config python-opengl python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev g++ openssl git

    2. Python Installation
        -> python + pip 
            $ sudo add-apt-repository ppa:jonathonf/python-3.6
            $ sudo apt-get update
            $ sudo apt install python2.7 python-pip python3.6 python3-pip  virtualenv curl
            $ sudo -H pip2 install --upgrade pip setuptools
            $ sudo -H pip3 install --upgrade pip setuptools
                --- ensure to have python3.6 http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/
            $ alias python3=python3.6

        -> Additional Python3 packages, which will not be installed automatically 
            $ sudo -H python3 -m pip install somajo someweta

        
    4. Sqlite + Pysqlcipher
        $ sudo apt-get install sqlite3 sqlcipher
        $ sudo -H python2 -m pip install pysqlcipher --install-option="--bundled"
        

    5. JAVA 
        $ sudo add-apt-repository ppa:linuxuprising/java
        $ sudo apt-get update
        $ sudo apt-get install oracle-java11-installer 
            
    6. GIT LFS
        $ sudo apt-get install software-properties-common
        $ sudo add-apt-repository ppa:git-core/ppa
        $ apt-get update
        $ curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
        $ sudo apt-get install git-lfs
        $ git lfs install



<br/>

##### On Windows (Win10)
  (this tool could be invoked just up from the Windows10 Version)


    1. Microsoft Visual C++ Compiler for Python 2.7
       (https://www.microsoft.com/en-us/download/details.aspx?id=44266)
    2. Enable in Features - "Windows Subsystem for Linux"
        (https://docs.microsoft.com/en-us/windows/wsl/install-win10)
    3. Enable in Settings - "Developer Mode"
        (https://www.wikihow.com/Enable-Developer-Mode-in-Windows-10)
    4. Install Ubuntu 16.04 from the Windows Store
        (https://devtidbits.com/2017/11/09/ubuntu-linux-on-windows-10-how-to/)
    5. goes to Ubuntu Bash 
    6. goes now above to the part with instructions for Linux
    *** root path to Ubuntu Directory on Windows: C:\Users\<username>\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\LocalState\rootfs\home




<br/>

##### On macOS (10.13.6)
    0. open Terminal
    1. Install brew
        $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    2. Install Python
        -> python ( pip (2+3)
            $ brew install python2 python3
            $ sudo python2 -m ensurepip
            $ sudo python3 -m ensurepip

         Ensure to have Python3.6 and not later version:
            $ brew unlink python3
            $ brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
            $ brew link python3

            $ pip2 install --upgrade pip setuptools wheel 
            $ pip3 install --upgrade pip setuptools wheel
            $ pip2 install virtualenv
        -> Additional python packages (for Python3)
            (which will not be installed automatically)  
            $ sudo python3 -m pip install somajo someweta


    3. Sqlite + Pysqlcipher + Git LFS
            $ brew install sqlite openssl sqlcipher git-lfs
            $ sudo -H python2 -m pip install pysqlcipher --install-option="--bundled"
            $ git lfs install
            
     4. Last Java Version (for TweetNLP Tokenizer and POS Tagger)
            $ brew cask install java


<br/>



---
---
---
---

<br/>

<a name="settingup"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 3. Setting up

<sub>*Set background color of your terminal to dark (ex. black, dark blue etc.)*</sub>


##### 1. Package Installation 

    0. open Terminal
    2. pip install zas-rep-tools



##### 2. User Configuration
<sub> Before you can test and work with this tool you need before to confige it. To make it easy set '.' while setttinh up of the project folder, if you want to user current folder as your project folder.</sub>

        $ cd <path_to_the_project_folder>
        $ sudo zas-rep-tools configer prjdir print



###### 3. Package Tests
<sub>  To be sure if your installation  in the current system could work error free please run tests. Be aware that it could take around 10-20 min.</sub>
   
        sudo zas-rep-tools testspath | sudo xargs -I {} nosetests -s -v --rednose {}



<br/>



---
---
---
---

<br/>

<a name="definitions"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 4. Definitions




   -  **Repetitions** (rep)
    We differentiate between two main types of repetitions:

     * **Replications** (repl)
        -> every Repetition on the letter level up from 3 repetitions (excluded: web links)
        -       ex. 'veeeeeerrrry'
                    (Following letters was replicated: 'e', 'r')
     * **Reduplications** (redu)
        -> every Repetition on the word level
        -       ex. 'very very very'
                    (Following word was reduplicated: 'very' ) 

    And one additional compound repetitions:
    * **Replications in Reduplications**
        -        ex. 'veeeerrrryyy veeery very vvvverryyy'
                    (Here is to see one reduplication of the word 'very' with the length 4 and also 3 uniq and 6 exhausted replications)

   - ****Length**** 
     * **Replications**
        -> The Number of the replicated letters 
        -       ex: 'verrrry'
                    ('r' was replicated and has length of 4)
     * **Reduplications**
        -> The Number of the words in one reduplication
        -       ex: 'very very very much much much much'
                    (There is two reduplications: 'very', 'much'. Reduplication of 'very' has length of 3 and the length of the reduplication for 'much' = 4.)



   - **Uniq vs. Exhausted Re(du)plication**
     <sub>(Every repetitions could be quantified in the uniq or exhausted way)</sub>
     
     * **Replications**
        -> Every reduplicated letter will be counted once as exhausted replication and each word contained one or many replications will be counted once as uniq replication. 
        -        ex: 'vvvvveeery'
                    **Exhausted**
                        = 2, ('v', 'e' was replicated)
                    **Uniq**
                        = 1 (because word 'very' contain any replications, but the word will be counted just once for this category)
                
     * **Reduplications**
        -> Every reduplicated word will be counted once as uniq reduplication and the length of the reduplication will be counted as exhausted reduplication. 
        -       ex: 'very very very or not very very but very'
                    **Uniq**
                        For 'very' = 2 (not 3) 
                    **Exhausted**
                        For 'very' = 5 (not 6)


   - **Syntagma**
        Combination/Group of words according to the rules of syntax for current language (each word could be also combinated with an empty word).
            -   ex: 'very much', 'very'

   - **Scope**
        The length of syntagma
        -       ex: 'very much' = 2; 'very'=1;

<a name="full"/>

   -  **Full Repetitiveness**
    <sub>(Each syntagma with scope > 1 have an additional attribute - full-repetitiveness.)</sub>
    
     - **Replications**
        If Every element of an syntagma was replicated, than Full-Repetitiveness for this Syntagma is True.
            -   ex: 'iiii llllovvveee verrry muuuuch', 'veryyyy verrryy muccchhhh', 'verrrrryyy muchhhhhh'
     - **Reduplications**
        If every element of an syntagma was reduplicated, than Full-Repetitiveness for this Syntagma is True.
            -   ex: 'very very very much much', "veeeerrryyy veeerryy mmmuuccc muuucch much "

    Current function could be switch on/off in StatsDB with following Options '--full_repetativ_syntagma'. If this option is on, than the just full-repetativ syntagmas will be available/matched with the export function. If it is on, than all syntagmas could be matched/exported, which contain at list one re(du)plication.


<br/>



---
---
---
---

<br/>
            
<a name="functionality"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 5. Functionality

<a name="cli-commands"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

### 5.1 CLI-Commands
Current CommandLineInterface support interaction for following entry points: 

- configer
    <sub>Set/Delete/reset all user information</sub>
- corpora
    <sub>Working with corpus DataBases</sub>
- stats
    <sub>Working with Statistics DataBases</sub>
- streamer
    <sub>Stream Twitter Data</sub>

In the following part you can see a small explanation to each entry point:

-           $ zas-rep-tools configer
     - prjdir
        <sub>Folder where all User Data will be saved for current copy of the Tool.</sub>
        - clean
        - set
        - reset
        - print
     - error_track 
        <sub>current tool support error tracking and report to the developers</sub>
        - set
        - reset
        - respeak
        - print
     - twitter
        <sub>This function set twitter credentials for the streamer</sub>
        - set
        - reset
        - respeak
        - print
     - email 
        <sub>to get error reports from twitter streamer per email, please give your emails</sub>
        - set
        - reset
        - respeak
        - print
     - user_data 
        - clean
        - location
        - print 

<br>

-           $ zas-rep-tools corpora

    - add
        <sub>create and add new corpus into project folder from given text collection</sub>
    - del
        <sub> delete existing corpus via name from project folder</sub>
    - names
        <sub> print all names from existing corpora in the project folder</sub>
    - meta
        <sub> print all meta-data for corpus via corp-name</sub>
    - basic_stats
        <sub> print all general statistics for corpus via corp-name</sub>
    - update_attr
        <sub> change meta-data for corpus via  corp-name</sub>
    - export
        <sub> export corpus into other file type (xml, csv, json) </sub>
    - used_tools
        <sub> print all used NLP methods and tools</sub>
    - clean_dir 
        <sub> delete corrupted corpora from project folder </sub>
    - cols
        <sub> print column names for given table in corpus</sub>
    - doc
        <sub> print all content for given doc via doc_id </sub>
    - ids
        <sub> print ids for all docs in corpus via corp-name</sub>


 <br>

-           $ zas-rep-tools stats

    - compute
        <sub>create and add compute (from given corpus) new stats-db and locate into project folder</sub>
    - del
        <sub> delete existing stats-db via name from project folder</sub>
    - names
        <sub> print all names of existing stats-db in the project folder</sub>
    - meta
        <sub> print all meta-data for stats-db via name</sub>
    - basic_stats
        <sub> print all general statistics for stats-db via name</sub>
    - update_attr
        <sub> change meta-data in stats-db via name</sub>
    - export
        <sub> export statistics as csv, xml, json </sub>
    - clean_dir
        <sub> delete corrupted stats-db from project folder </sub>
    - recompute
        <sub> recompute stats-db with other full-repetativenes marker </sub>
    - optimize
        <sub> spaces and speed optimization via stats-db freezing </sub>
    - recreate_indexes
        <sub> recreate indexes in an stats-db for better performance </sub>



-           $ zas-rep-tools streamTwitter


 
-           $ zas-rep-tools streamerInfo
    - enc
        <sub> Supported Encodings </sub>
    - lang
        <sub> Supported Languages for Streamer </sub>
    - nltk_lang
         <sub> Supported Languages for NLTK </sub>
    - twitter_lang
        <sub> Supported Languages for TwitterAPI </sub>
    - classiefier_lang
        <sub> Supported Languages for Language Classifier </sub>
    - stop_words
        <sub> Predefined Stopwords  </sub>
    - platforms
        <sub> Supported Platforms </sub>



 
-           $ zas-rep-tools help

---


<br>

<a name="cli-options"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

### 5.2 CLI-Options

- ***zas-rep-tools configer --help***

        Usage: zas-rep-tools configer [OPTIONS] COMMAND1 COMMAND2

        Options:
          -m, --mode [error|test|dev|dev+|dev-|prod|free|prod+t|test+s+|test+s-|silent|prod+|prod-|blind]
                                          Set one of the Tool Modus
          -ld, --logdir TEXT              Choose the name of the Directory for log
                                          data.
          --help                          Show this message and exit.


<br>

- ***zas-rep-tools corpora --help***

        Usage: zas-rep-tools corpora [OPTIONS] COMMAND1

        Options:
          -sb, --status_bar BOOLEAN       Enable/Disable the Status Bat
          -uefm, --use_end_file_marker BOOLEAN
                                          Enable/Disable usage of endfilemarker to
                                          change the couter unit from rows to files in
                                          the status bar
          -tscc, --tok_split_camel_case BOOLEAN
                                          Enable/Disable the option for Tokenizer to
                                          convertion and split of the CamelCase (ex.
                                          'CamelCase')
          -backup, --make_backup BOOLEAN  Enable/Disable making BackUp of the whole
                                          Corpus before the new Insetions
          -lb, --lazyness_border INTEGER  Set the number of the border, which ensure
                                          when exactly data collector should save data
                                          on the disk. If you have a big RAM than
                                          select the high number, to ensure the hight
                                          performance.
          -rw, --rewrite BOOLEAN          Enable/Disable rewrite option, which ensure
                                          the file replacing/rewriting during the
                                          export, if the same filename was found in
                                          the same directory.
          -uc, --use_cash BOOLEAN         Enable/Disable during the insertion process
                                          write direct on the disk or first into cash.
                                          It is a good performance booster, but just
                                          in the case of the big RAM.
          -opt, --optimizer TEXT          Enable/Disable DB Optimizer, which makes
                                          current DB much faster, but less safety.
          -optps, --optimizer_page_size INTEGER
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optcs, --optimizer_cache_size INTEGER
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optlm, --optimizer_locking_mode [normal|exclusive]
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optsyn, --optimizer_synchronous [1|0|3|2|normal|off|extra|full]
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optjm, --optimizer_journal_mode [delete|truncate|persist|memory|wal|off]
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optts, --optimizer_temp_store [1|0|2|file|default|memory]
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -gr, --gready BOOLEAN           If False -> Stop Process immediately if
                                          error was returned. If True -> Try to
                                          execute script so long as possible, without
                                          stopping the main process.
          -cn, --corp_fname TEXT          File Name of the CorpusDB (with or without
                                          extention)
          -lang, --language [test|de|en|False]
                                          Give language acronym according to standard
                                          ISO639_2.
          -vis, --visibility [extern|intern|False]
                                          Is that an intern or extern Corpus?
          -platf, --platform_name TEXT
          -encrkey, --encryption_key TEXT
                                          For encryption of the current DB please
                                          given an key. If key is not given, than the
                                          current DB will be not encrypted.
          -cname, --corp_intern_dbname TEXT
                                          Intern Name of the DB, which will be saved
                                          as tag inside the DB.
          -src, --source TEXT             Source of the text collection.
          -lic, --license TEXT            License, under which this corpus will be
                                          used.
          -templ, --template_name [blogger|twitter|False]
                                          Templates are there for initialization of
                                          the preinitialized Document Table in the DB.
                                          Every Columns in the DocumentTable should be
                                          initialized. For this you can use Templates
                                          (which contain preinitialized Information)
                                          or initialize manually those columns
                                          manually with the   '--
                                          cols_and_types_in_doc'-Option.
          -ver, --version INTEGER         Version Number of the DB
          -additcols, --cols_and_types_in_doc TEXT
                                          Additional Columns from input text
                                          Collections. Every Columns in the
                                          DocumentTable should be initialized. Every
                                          Document Table has already two default
                                          columns (id, text) if you want to insert
                                          also other columns, please define them here
                                          with the type names. The colnames should
                                          correspond to the colnames in the input text
                                          data and be given in the following form: 'co
                                          lname1:coltype1,colname2:coltype2,colname3:c
                                          oltype3'
          -cid, --corpus_id_to_init TEXT  Manually given corpid
          -tok, --tokenizer [somajo|nltk|False|True]
                                          Select Tokenizer by name
          -ptager, --pos_tagger [someweta|tweetnlp|False|True]
                                          Select POS-Tagger by name
          -sentim, --sentiment_analyzer [textblob|False|True]
                                          Select Sentiment Analyzer by name
          -sentspl, --sent_splitter [pystemmer|False|True]
                                          Select Stemmer by name
          -preproc, --preprocession BOOLEAN
                                          Enable/disable Proprocessing of the text
                                          elements.
          -langclas, --lang_classification TEXT
                                          Enable/disable Language Classification
          -durl, --del_url BOOLEAN        Enable/disable Hiding of all URLs
          -dpnkt, --del_punkt BOOLEAN     Enable/disable Hiding of all Punctuation
          -dnum, --del_num BOOLEAN        Enable/disable Hiding of all Numbers
          -dment, --del_mention BOOLEAN   Enable/disable Hiding of all Mentions
          -dhash, --del_hashtag BOOLEAN   Enable/disable Hiding of all Hashtags
          -dhtml, --del_html BOOLEAN      Enable/disable cleaning of all  not needed
                                          html tags
          -case, --case_sensitiv BOOLEAN  Enable/disable the case sensitivity in the
                                          Corpus during initialization.
          -emojnorm, --emojis_normalization BOOLEAN
                                          Enable/disable restructure of all Emojis.
                                          (could cost much time)
          -texname, --text_field_name TEXT
                                          If new input data has different name with
                                          text or id information, than use this
                                          options to ensure correct use of data.
          -idname, --id_field_name TEXT   If new input data has different name with
                                          text or id information, than use this
                                          options to ensure correct use of data.
          -heal, --heal_me_if_possible BOOLEAN
                                          If '--template_name' and  '--
                                          cols_and_types_in_doc' wasn't selected, than
                                          with this option ('--heal_me_if_possible')
                                          DB will try to initialize those information
                                          automatically. But be careful with this
                                          option, because it could also return
                                          unexpected  errors.
          -ptr, --path_to_read TEXT       Path to folder with text collection, which
                                          should be collected and transformed into
                                          CorpusDB.
          -readtyp, --file_format_to_read [txt|json|xml|csv|False]
                                          File Format which should be read.
          -readregextempl, --reader_regex_template [blogger|False]
                                          Name of the template for Reading of the TXT
                                          Files.
          -readregexpattern, --reader_regex_for_fname TEXT
                                          Regex Pattern for Extraction of the Columns
                                          from the filenames.
          -zipread, --read_from_zip BOOLEAN
                                          Enable/Disable the possibly also to search
                                          and read automatically from *.zip Achieves.
          -formatter, --formatter_name [twitterstreamapi|sifter|False]
                                          Give the name of the predefined Formatters
                                          and Preprocessors for different text
                                          collections.
          -retweetsignr, --reader_ignore_retweets BOOLEAN
                                          Ignore Retweets, if original JsonTweet was
                                          given.
          -minfile, --min_files_pro_stream INTEGER
                                          The Limit, when Multiprocessing will be
                                          start to create a new stream.
          -csvd, --csvdelimiter TEXT      CSV Files has offten different dialects and
                                          delimiters. With this option, it is
                                          possible, to set an delimiter, which ensure
                                          correct processing of the CSV File Data.
          -enc, --encoding [bz2_codec|cp1140|rot_13|cp932|euc_jisx0213|cp037|hex_codec|cp500|uu_codec|big5hkscs|mbcs|euc_jis_2004|iso2022_jp_3|iso2022_jp_2|iso2022_jp_1|gbk|iso2022_jp_2004|quopri_codec|cp424|iso2022_jp|mac_iceland|hp_roman8|iso2022_kr|euc_kr|cp1254|utf_32_be|gb2312|cp850|shift_jis|cp852|cp855|utf_16_le|cp857|cp775|cp1026|mac_latin2|utf_32|mac_cyrillic|base64_codec|ptcp154|euc_jp|hz|utf_8|utf_32_le|mac_greek|utf_7|mac_turkish|cp949|zlib_codec|big5|iso8859_9|iso8859_8|iso8859_5|iso8859_4|iso8859_7|iso8859_6|iso8859_3|iso8859_2|gb18030|shift_jis_2004|mac_roman|cp950|utf_16|iso8859_15|iso8859_14|tis_620|iso8859_16|iso8859_11|iso8859_10|iso8859_13|ascii|cp869|utf-8|cp860|cp861|cp862|cp863|cp864|cp865|cp866|shift_jisx0213|cp1255|latin_1|cp1257|cp1256|cp1251|cp1250|cp1253|cp1252|cp437|cp1258|tactis|koi8_r|utf_16_be|johab|iso2022_jp_ext|cp858]
                                          All Text Files are encoded with help of the
                                          EncodingTables. If you input files are not
                                          unicode-compatible, please give the encoding
                                          name, which was used for encoding the input
                                          data.
          -docid, --doc_id TEXT           Document ID in the Corpus DB.
          -attr, --attr_name TEXT         Stats and Corpus DBs has intern Attributes.
                                          For changing of getting them you need to get
                                          the name of this attribute.
          -val, --value TEXT              For setting of the new Value for one
                                          Attribute.
          -exptyp, --type_to_export [sqlite|json|xml|csv|False]
                                          FileType for the export function.
          -expdir, --export_dir TEXT      Directory where Exports will be saved. If
                                          False, than they will be saved in the
                                          default ProjectDirectory.
          -expname, --export_name TEXT    FileName for ExportData.
          -rowlim, --rows_limit_in_file INTEGER
                                          Number of the Rows Max in the Files to
                                          export.
          -sn, --stream_number INTEGER    Enable or Disable the Multiprocessing. If
                                          Number > 1, than tool try to compute every
                                          thing parallel. This function could bring
                                          much better performance on the PC with multi
                                          cores and big Operation Memory.
          -m, --mode [error|test|dev|dev+|dev-|prod|free|prod+t|test+s+|test+s-|silent|prod+|prod-|blind]
                                          Set one of the Tool Modus. Modi ensure the
                                          communication behavior of this Tool.
          -ld, --logdir TEXT              Choose the name of the Directory for log
                                          data.
          --help                          Show this message and exit.



<br>


- ***zas-rep-tools stats --help***

        Usage: zas-rep-tools stats [OPTIONS] COMMAND1

        Options:
          -sb, --status_bar BOOLEAN       Enable/Disable the Status Bat
          -uefm, --use_end_file_marker BOOLEAN
                                          Enable/Disable usage of endfilemarker to
                                          change the couter unit from rows to files in
                                          the status bar
          -backup, --make_backup BOOLEAN  Enable/Disable making BackUp of the whole
                                          Corpus before the new Insetions
          -lb, --lazyness_border INTEGER  Set the number of the border, which ensure
                                          when exactly data collector should save data
                                          on the disk. If you have a big RAM than
                                          select the high number, to ensure the hight
                                          performance.
          -rw, --rewrite BOOLEAN          Enable/Disable rewrite option, which ensure
                                          the file replacing/rewriting during the
                                          export, if the same filename was found in
                                          the same directory.
          -uc, --use_cash BOOLEAN         Enable/Disable during the insertion process
                                          write direct on the disk or first into cash.
                                          It is a good performance booster, but just
                                          in the case of the big RAM.
          -opt, --optimizer TEXT          Enable/Disable DB Optimizer, which makes
                                          current DB much faster, but less safety. See
                                          more: https://www.sqlite.org/pragma.html
          -optps, --optimizer_page_size INTEGER
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optcs, --optimizer_cache_size INTEGER
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optlm, --optimizer_locking_mode [normal|exclusive]
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optsyn, --optimizer_synchronous [1|0|3|2|normal|off|extra|full]
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optjm, --optimizer_journal_mode [delete|truncate|persist|memory|wal|off]
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -optts, --optimizer_temp_store [1|0|2|file|default|memory]
                                          Setting for DBOptimizer. See more in the
                                          Hell-text for  optimizer.
          -gr, --gready BOOLEAN           If False -> Stop Process immediately if
                                          error was returned. If True -> Try to
                                          execute script so long as possible, without
                                          stopping the main process.
          -cn, --corp_fname TEXT          File Name of the CorpusDB (with or without
                                          extention)
          -sn, --stream_number INTEGER    Enable or Disable the Multiprocessing. If
                                          Number > 1, than tool try to compute every
                                          thing parallel. This function could bring
                                          much better performance on the PC with multi
                                          cores and big Operation Memory.
          -crtix, --create_indexes BOOLEAN
                                          For better performance it is highly
                                          recommended to create indexes. But their
                                          creation could also cost time  once during
                                          their creation and also space.
          -freeze, --freeze_db BOOLEAN    Freeze current DB and close for all next
                                          possible insertion of the new data. This
                                          option also triggers the DB Optimization
                                          Porcess, which could cost a lost of time,
                                          but make this DB much space and time
                                          efficient. Once this process is done, it is
                                          not possible anymore to decline it.
          -optlongsyn, --optimized_for_long_syntagmas BOOLEAN
                                          If you are planing to search in the big
                                          syntagmas, than set this to True. It will
                                          optimize DB to be fast with long syntagmas.
          -minfile, --min_files_pro_stream INTEGER
                                          The Limit, when Multiprocessing will be
                                          start to create a new stream.
          -basdelim, --baseline_delimiter TEXT
                                          Delimiter for Syntagmas in intern Baseline
                                          Table. Change here if you really know, that
                                          you need it.
          -sfn, --stats_fname TEXT        File Name of the StatsDB.
          -vis, --visibility [extern|intern|False]
                                          Is that an intern or extern Corpus?
          -encrkey, --encryption_key TEXT
                                          For encryption of the current DB please
                                          given an key. If key is not given, than the
                                          current DB will be not encrypted.
          -ver, --version INTEGER         Version Number of the DB
          -stats_id, --stats_id TEXT      Possibilty to set StatsId manually.
                                          Otherwise it will be setted automatically.
          -cname, --stats_intern_dbname TEXT
                                          Intern Name of the DB, which will be saved
                                          as tag inside the DB.
          -conlen, --context_lenght INTEGER
                                          This number mean how much tokens left and
                                          right will be also captured and saved for
                                          each found re(du)plication. This number
                                          should be >=3
          -fullrep, --full_repetativ_syntagma BOOLEAN
                                          Disable/Enable FullRepetativnes. If it is
                                          True, than just full repetativ syntagmas
                                          would be considered.  FullRepetativ syntagma
                                          is those one, where all words was ongoing
                                          either replicated or replicated. (ex.:
                                          FullRepRedu: 'klitze klitze kleine kleine' ,
                                          FullRepRepl: 'kliiitzeee kleeeinee') (See
                                          more about it in Readme -> Definitions)
          -ru, --repl_up INTEGER          Up this number this tool recognize repetativ
                                          letter as replication.
          -ignht, --ignore_hashtag BOOLEAN
                                          Enable/disable Hiding of all Hashtags, if it
                                          wasn't done during CorpusCreationProcess.
          -case, --case_sensitiv BOOLEAN  Enable/disable the case sensitivity during
                                          Stats Computation Process.
          -ignurl, --ignore_url BOOLEAN   Enable/disable Hiding of all URLS, if it
                                          wasn't done during CorpusCreationProcess.
          -ignment, --ignore_mention BOOLEAN
                                          Enable/disable Hiding of all Mentions, if it
                                          wasn't done during CorpusCreationProcess.
          -ignp, --ignore_punkt BOOLEAN   Enable/disable Hiding of all Punctuation, if
                                          it wasn't done during CorpusCreationProcess.
          -ignnum, --ignore_num BOOLEAN   Enable/disable Hiding of all Numbers, if it
                                          wasn't done during CorpusCreationProcess.
          -bliti, --baseline_insertion_border INTEGER
                                          Number of the limit, when syntagmas will be
                                          delete from cash and saved on the disk.
          -expdir, --export_dir TEXT      Set Path to export dir. If it is not given,
                                          than all export will be saved into
                                          ProjectFolder.
          -exp_fname, --export_name TEXT  Set fname for export files.
          -syn, --syntagma_for_export TEXT
                                          Set Syntagmas for search/extract. Default:
                                          '*'-match all syntagmas. Example: 'very|huge
                                          |highly,pitty|hard|happy,man|woman|boy|perso
                                          n' ('|' - as delimiter in paradigm; ',' - as
                                          delimiter of the syntagmas part.)  Notice:
                                          Now white space is allow.
          -repl, --exp_repl BOOLEAN       Disable/Enable Replications Extraction
          -redu, --exp_redu BOOLEAN       Disable/Enable Reduplications Extraction
          -styp, --exp_syntagma_typ [pos|lexem]
                                          Ensure type of the given components in
                                          Syntagma_to_search. It is possible to search
                                          in pos-tags or in lexems.
          -sent, --exp_sentiment [neutral|positive|negative|False]
                                          Search in Sentiment tagged data.
          -ftyp, --export_file_type [csv|json|xml]
          -rowlim, --rows_limit_in_file INTEGER
                                          Number of the Rows Max in the Files to
                                          export.
          -exp_encrkey, --encryption_key_corp TEXT
                                          For export additional columns
                                          (--additional_doc_cols) from encrypted
                                          CorpDB or for compution of the new StatsDb
                                          from the encrypted CorpDB
          -ott, --output_table_type [exhausted|sum]
          -doccols, --additional_doc_cols TEXT
                                          For export of stats with additional columns
                                          from document from CorpDB. Don't forget to
                                          give also the FName of CorpusDB for which
                                          current statsDB was computed. (--corp_fname)
                                          Please give it in the following Form:
                                          'gender,age,' (NO WHITE SPACES ARE ALLOW)
          -mscope, --max_scope TEXT       Upper Limit of the syntagma length to
                                          search. Example: if max_scope = 1, than tool
                                          will search just in those syntagmas, which
                                          contain just 1 word.
          -stemm, --stemmed_search BOOLEAN
                                          Search in lemantisated/stemmed syntagmas. Be
                                          careful and don't give different
                                          conjugations of one lemma, if current
                                          options is True.  Because you could get
                                          duplicates.
          -conleft, --context_len_left TEXT
                                          The length of context In Output Tables.
                                          Could be also Disabled (False).
          -conright, --context_len_right TEXT
                                          The length of context In Output Tables.
                                          Could be also Disabled (False).
          -sepsyn, --separator_syn TEXT   Separator inside syntagma in baseline.
          -wordex, --word_examples_sum_table BOOLEAN
                                          Enable/disable Word Examples in Exported
                                          Output. (Just For SumOutputTables)
          -ignsym, --ignore_symbol TEXT   Enable/disable Symbols in Exported Outputs.
                                          (Just For SumOutputTables)
          -recflag, --recompute_flag TEXT
                                          For 'recompute' command. This command
                                          recompute the FullRepetativnes in given
                                          StatsDB. True - full_repetativnes, False -
                                          no_full_repetativnes/all_syntagmas
          -attr, --attr_name TEXT         Stats and Corpus DBs has intern Attributes.
                                          For changing of getting them you need to get
                                          the name of this attribute.
          -val, --value TEXT              For setting of the new Value for one
                                          Attribute.
          -m, --mode [error|test|dev|dev+|dev-|prod|free|prod+t|test+s+|test+s-|silent|prod+|prod-|blind]
                                          Set one of the Tool Modus
          -ld, --logdir TEXT              Choose the name of the Directory for log
                                          data.
          --help                          Show this message and exit.


<br>

- ***zas-rep-tools streamTwitter --help***

        Usage: zas-rep-tools streamTwitter [OPTIONS] PATH_TO_SAVE

        Options:
          -l, --language [en|it|ar|id|es|ru|nl|pt|no|tr|th|pl|fr|de|da|fa|hi|fi|hu|ja|he|ko|sv|ur|False]
          -sw, --stop_words TEXT
          -t, --terms TEXT
          -e, --encoding [bz2_codec|cp1140|rot_13|cp932|euc_jisx0213|cp037|hex_codec|cp500|uu_codec|big5hkscs|mbcs|euc_jis_2004|iso2022_jp_3|iso2022_jp_2|iso2022_jp_1|gbk|iso2022_jp_2004|quopri_codec|cp424|iso2022_jp|mac_iceland|hp_roman8|iso2022_kr|euc_kr|cp1254|utf_32_be|gb2312|cp850|shift_jis|cp852|cp855|utf_16_le|cp857|cp775|cp1026|mac_latin2|utf_32|mac_cyrillic|base64_codec|ptcp154|euc_jp|hz|utf_8|utf_32_le|mac_greek|utf_7|mac_turkish|cp949|zlib_codec|big5|iso8859_9|iso8859_8|iso8859_5|iso8859_4|iso8859_7|iso8859_6|iso8859_3|iso8859_2|gb18030|shift_jis_2004|mac_roman|cp950|utf_16|iso8859_15|iso8859_14|tis_620|iso8859_16|iso8859_11|iso8859_10|iso8859_13|ascii|cp869|cp860|cp861|cp862|cp863|cp864|cp865|cp866|shift_jisx0213|cp1255|latin_1|cp1257|cp1256|cp1251|cp1250|cp1253|cp1252|cp437|cp1258|tactis|koi8_r|utf_16_be|johab|iso2022_jp_ext|cp858]
          -irt, --ignore_rt BOOLEAN
          -f, --filter_strategie [t|t+l|False]
                                          Set Filter Strategy. 1) 't'-just search for
                                          terms/stop_words; 2) 't+l' - search for
                                          stop_words and language (recomended)
          -sut, --save_used_terms BOOLEAN
          -m, --mode [error|test|dev|dev+|dev-|prod|free|prod+t|test+s+|test+s-|silent|prod+|prod-|blind]
                                          Set one of the Tool Modus
          -ld, --logdir TEXT              Choose the name of the Directory for log
                                          data.
          --help                          Show this message and exit.



- ***zas-rep-tools streamerInfo --help***

        Usage: zas-rep-tools streamerInfo [OPTIONS] COMMAND

        Options:
          -m, --mode [error|test|dev|dev+|dev-|prod|free|prod+t|test+s+|test+s-|silent|prod+|prod-|blind]
                                          Set one of the Tool Modus
          -ld, --logdir TEXT              Choose the name of the Directory for log
                                          data.
          --help                          Show this message and exit.


---
<br>

<a name="cli-usage"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

### 5.3 CLI-Usage
<sub> Usage examples for each CLI-Command with belonging to it options.
Notice: this tool is quite user friendly and if something goes wrong this Tool try to predict, what was wrong and try to give the useful information, about how to solve the current problem.  </sub>

#### Necessary Options
<sub> List of the minimum/necessary options, which needed to run certain command.</sub>

-           $ zas-rep-tools corpora

    - **add**
        -  *\--path_to_read*
        -  *\--file_format_to_read*
        -  *\--corp_intern_dbname*
        -  *\--language*
        -  *\--visibility*
        -  *\--platform_name*


    - **del**
        - *\--corp_fname*

    - **names**
    <sub>None additional option</sub>

    - **meta**
        - *\--corp_fname*

    - **basic_stats**
        - *\--corp_fname*
    - **update_attr**
        - *\--corp_fname*
        - *\--attr_name*
        - *\--value*
    - **export**
        - *\--corp_fname*
        - *\--type_to_export*
    - **used_tools**
        <sub>None additional option</sub>
    - **clean_dir**
        <sub>None additional option</sub>
    - **cols**
        - *\--corp_fname*
    - **doc**
        - *\--corp_fname*
        - *\--doc_id*
    - **ids**
        - *\--corp_fname*


 <br>

-           $ zas-rep-tools stats

    - **compute**
        - *\--corp_fname*
        - *\--stats_intern_dbname*
        - *\--visibility*

    - **del**
        - *\--stats_fname*
    - **names**
        <sub>None additional option</sub>
    - **meta**
        - *\--stats_fname*
    - **basic_stats**
        - *\--stats_fname*
    - **update_attr**
        - *\--stats_fname*
        - *\--attr_name*
        - *\--value*
    - **export**
        - *\--stats_fname*
        - *\--export_file_type*
    - **clean_dir**
        <sub>None additional option</sub>
    - **recompute**
        - *\--stats_fname*
        - *\--recompute_flag*
    - **optimize**
        - *\--stats_fname*
    - **recreate_indexes**
        - *\--stats_fname*



-           $ zas-rep-tools streamTwitter

     - *\--path_to_save*
     - *\--filter_strategie*

<br>
<br>

#### Exhausted Options
<sub> List of the exhausted/additional options, which needed to run certain command. (just for those commands which are different to the category before)</sub>

-           $ zas-rep-tools corpora

    - **add**
        - *\--path_to_read*
        - *\--file_format_to_read*
        - *\--reader_regex_template*
        - *\--reader_regex_for_fname*
        - *\--end_file_marker*
        - *\--use_end_file_marker*
        - *\--stop_process_if_possible*
        - *\--formatter_name*
        - *\--text_field_name*
        - *\--id_field_name*
        - *\--reader_ignore_retweets*
        - *\--mode*
        - *\--status_bar*
        - *\--tok_split_camel_case*
        - *\--make_backup*
        - *\--lazyness_border*
        - *\--rewrite*
        - *\--stop_if_db_already_exist*
        - *\--use_cash*
        - *\--optimizer*
        - *\--optimizer_page_size*
        - *\--optimizer_cache_size*
        - *\--optimizer_locking_mode*
        - *\--optimizer_synchronous*
        - *\--optimizer_journal_mode*
        - *\--optimizer_temp_store*
        - *\--stop_process_if_possible*
        - *\--heal_me_if_possible*
        - *\--corp_intern_dbname*
        - *\--language*
        - *\--visibility*
        - *\--encryption_key*
        - *\--corp_fname*
        - *\--source*
        - *\--license*
        - *\--template_name*
        - *\--version*
        - *\--cols_and_types_in_doc*
        - *\--corpus_id_to_init*
        - *\--tokenizer*
        - *\--pos_tagger*
        - *\--sentiment_analyzer*
        - *\--sent_splitter*
        - *\--preprocession*
        - *\--lang_classification*
        - *\--del_url*
        - *\--del_punkt*
        - *\--del_num*
        - *\--del_mention*
        - *\--del_hashtag*
        - *\--del_html*
        - *\--case_sensitiv*
        - *\--emojis_normalization*
        - *\--stream_number*
        - *\--min_files_pro_stream*
        - *\--csvdelimiter*
        - *\--encoding*
        - *\--del_hashtag*
        - *\--del_html*
        - *\--case_sensitiv*
        - *\--read_from_zip*

    - **meta**
        - *\--corp_fname*
        - *\--encryption_key*
    - **basic_stats**
        - *\--corp_fname*
        - *\--encryption_key*
    - **update_attr**
        - *\--corp_fname*
        - *\--attr_name*
        - *\--value*
        - *\--encryption_key*

    - **export**
        - *\--corp_fname*
        - *\--type_to_export*
        - *\--encryption_key*
        - *\--export_dir*

    - **cols**
        - *\--corp_fname*
        - *\--encryption_key*
    - **doc**
        - *\--corp_fname*
        - *\--doc_id*
        - *\--encryption_key*
    - **ids**
        - *\--corp_fname*
        - *\--encryption_key*


 <br>

-           $ zas-rep-tools stats

    - **compute**
        - *\--corp_fname*
        - *\--encryption_key_corp*
        - *\--mode*
        - *\--status_bar*
        - *\--make_backup*
        - *\--lazyness_border*
        - *\--rewrite*
        - *\--stop_if_db_already_exist*
        - *\--use_cash*
        - *\--optimizer*
        - *\--optimizer_page_size*
        - *\--optimizer_cache_size*
        - *\--optimizer_locking_mode*
        - *\--optimizer_synchronous*
        - *\--optimizer_journal_mode*
        - *\--optimizer_temp_store*
        - *\--stats_intern_dbname*
        - *\--visibility*
        - *\--encryption_key*
        - *\--stats_fname*
        - *\--gready*
        - *\--version*
        - *\--context_lenght*
        - *\--full_repetativ_syntagma*
        - *\--repl_up*
        - *\--ignore_hashtag*
        - *\--case_sensitiv*
        - *\--ignore_url*
        - *\--ignore_mention*
        - *\--ignore_punkt*
        - *\--ignore_num*
        - *\--baseline_delimiter*
        - *\--min_files_pro_stream*
        - *\--create_indexes*
        - *\--freeze_db*
        - *\--baseline_insertion_border*
        - *\--optimized_for_long_syntagmas*


    - **meta**
        - *\--stats_fname*
        - *\--encryption_key*
    - **basic_stats**
        - *\--stats_fname*
        - *\--encryption_key*
    - **update_attr**
        - *\--stats_fname*
        - *\--attr_name*
        - *\--value*
        - *\--encryption_key*
    - **export**
        - *\--mode*
        - *\--status_bar*
        - *\--stats_fname*
        - *\--encryption_key*
        - *\--export_dir*
        - *\--syntagma_for_export*
        - *\--exp_repl*
        - *\--exp_redu*
        - *\--exp_syntagma_typ*
        - *\--exp_sentiment*
        - *\--encryption_key_corp*
        - *\--output_table_type*
        - *\--additional_doc_cols*
        - *\--path_to_corpdb*
        - *\--max_scope*
        - *\--stemmed_search*
        - *\--context_len_left*
        - *\--context_len_right*
        - *\--separator_syn*
        - *\--word_examples_sum_table*
        - *\--ignore_num*
        - *\--ignore_symbol*
    - **recompute**
        - *\--stats_fname*
        - *\--recompute_flag*
        - *\--encryption_key*
    - **optimize**
        - *\--stats_fname*
        - *\--encryption_key*
    - **recreate_indexes**
        - *\--stats_fname*
        - *\--encryption_key*


<br>

-           $ zas-rep-tools streamTwitter <path_to_save>

     - *\--language*
     - *\--filter_strategie*
     - *\--stop_words*
     - *\--terms*
     - *\--encoding*
     - *\--ignore_rt*
     - *\--save_used_terms*
     - *\--mode*
     - *\--logdir*



<br>

---

<a name="multiprocessing"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

### 5.4 Multiprocessing
    Current Tool support multiprocessing. Just set 'stream_number'-Option to more as 1 to ensure the process to be executed parallel.

<br>

---

<a name="nlp-methods"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

### 5.5 NLP-Methods
Used NLP-Methods:

- Tokenization 
- Sent-Segmentation
- POS-Tagging
- Sentiment Analysis
- Steaming
- RLE (run length encoding)

<br>

---

<a name="db"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

### 5.6 InternDataBase-Structure (SQLite)

- **Corpus**
    - Tables: 
        - Documents
        - Info
    - Meta-Data:
     (id,name,platform_name,template_name,version,language,created_at,source,license,visibility,typ,tokenizer,sent_splitter,pos_tagger,sentiment_analyzer,preprocession,del_url,del_punkt,del_num,del_mention,del_hashtag,del_html,case_sensitiv,lang_classification,emojis_normalization,sent_num,token_num,doc_num,text_field_name,id_field_name,locked)



- **Stats**
    - Tables: 
        - Replications
        - Reduplications 
        - Baseline 
        - Info 
    - Meta-Data:
        (id, corpus_id, name, version, created_at, visibility, typ, db_frozen, context_lenght, language, repl_up, ignore_hashtag, ignore_url, ignore_mention, ignore_punkt, ignore_num, force_cleaning, case_sensitiv, full_repetativ_syntagma, min_scope_for_indexes, locked, pos_tagger, sentiment_analyzer, baseline_delimiter)

<br>

---

<a name="additional_features"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

### 5.7 Additional Features

 - **Formatters**
    Are there to help for better reading or the unstructured data.
    Existing Formatters: ["twitterstreamapi", "sifter"]

 - **Templates**
    Predefinition of corpus-DB for different exiting projects, which contain information about columns for the documents-table
    Existing Templates: ["twitter","blogger"]



<br/>


---
---
---
---

<br/>

<a name="workflow"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 6. WorkFlow

Step 1: Corpus Data Base Creation 

        $ zas-rep-tools corpora add

Step 2: Stats DataBase Computation 

        $ zas-rep-tools stats compute

Step 3: Export of the computed Statistics 

        $ zas-rep-tools stats export


<br/>


---
---
---
---

<br/>

<a name="tutorials"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 7. Tutorials

**Notice**

    1. Don't use following symbols in the namespaces: '-,;:=)({}¢[];
    2. All DataBases will be saves into the given ProjectFolders';
    3. To Stop Executions please use 'Ctrl+C';
    4. To ensure the fast corpus creation try to use minimum of preprocessing 
    functions;
    5. Following command are just example and have as a goal to inspire the user;



## Python Package Tutorial

***-work_in_progress-*** <sub>(API could be found in the tests-folder. If you interested to use this Tool also as Python Package please contact the developer and ask for better API Explanation.)</sub>

---
---

<br/>



## Command line Tutorial

<br/>

#### Add/Create Corpus
<sub>Following examples ensure corpora creation process from current directory and with maximal preprocessing steps.
</sub>


   - From Certain (predefined) Sources
      <sub>Predifinition is done through following options:'\--formatter_name','\--reader_regex_template', '\--template_name'</sub>

       - [Sifter-Twitter-Data (csv)](https://sifter.texifter.com)
        
           -        $ zas-rep-tools corpora add --path_to_read . --file_format_to_read csv --corp_intern_dbname sifter_twitter_2014 --language de  --visibility intern --platform_name twitter --read_from_zip True --mode prod --heal_me_if_possible True --formatter_name sifter --sent_splitter True --pos_tagger True  --read_from_zip True   --version 1 --sentiment_analyzer True --del_url True --del_punkt True --del_num True --del_html True --case_sensitiv False

      - [Blogger Autorship Corpus (txt)](http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm)

           -        $ zas-rep-tools corpora add --path_to_read . --file_format_to_read txt --corp_intern_dbname blogger_txt --language en --visibility extern --platform_name blogger  --reader_regex_template blogger --sent_splitter True --pos_tagger True --del_html True --mode prod+ --read_from_zip True  --source LanguageGoldMine  --version 1 --sentiment_analyzer True --del_url True --del_punkt True --del_num True --del_html True --case_sensitiv False

      - [Twitter Stream API (json)](https://developer.twitter.com/en/docs/tweets/filter-realtime/overview.html)
        -        $ zas-rep-tools corpora add --path_to_read . --file_format_to_read json --corp_intern_dbname twitter_streamed_2019 --language en --visibility extern --platform_name twitter --template_name twitter --stream_number 1 --formatter_name twitterstreamapi --sent_splitter True --pos_tagger True --mode prod+ --read_from_zip True  --source TwitterAPI --license Twitter_Developer_Agreement_and_Policy --version 1 --sentiment_analyzer True --del_url True --del_punkt True --del_num True --del_html True --case_sensitiv False

  
   - From Scratch
      - txt
        <sub>This tool can just work with those TXT-Text-Collections, which have all meta-data in the filename, which could be matched with an regex.</sub>
           -        $ zas-rep-tools corpora add --path_to_read . --file_format_to_read txt --corp_intern_dbname txt_corp --language en --visibility extern --platform_name blogger --del_html True --reader_regex_for_fname "(?P<id>[\d]*)\.(?P<gender>[\w]*)\.(?P<age>\d*)\.(?P<working_area>.*)\.(?P<star_constellation>[\w]*)" --sent_splitter True --pos_tagger True --mode prod+ --read_from_zip True  --source LanguageGoldMine  --version 1 --sentiment_analyzer True --del_url True --del_punkt True --del_num True --del_html True --case_sensitiv False

      - csv/json/json
           -        $ zas-rep-tools corpora add --path_to_read . --file_format_to_read json --corp_intern_dbname twitter_streamed_2019 --language en --visibility extern --platform_name twitter --stream_number 1 --sent_splitter True --pos_tagger True --mode prod+ --read_from_zip True  --source TwitterAPI --license Twitter_Developer_Agreement_and_Policy --version 1 --sentiment_analyzer True --del_url True --del_punkt True --del_num True --del_html True --case_sensitiv False --heal_me_if_possible False --cols_and_types_in_doc 't_created_at:TEXT,t_language:TEXT,t_used_client:TEXT,u_created_at:TEXT,u_description:TEXT,u_favourites:INTEGER,u_followers:INTEGER,u_friends:INTEGER,u_id:INTEGER'
        
          <sub>or (let tool extract the columns from input text collection automatically (\--heal_me_if_possible True), but if input data is not consistent and every document have different number of columns, than it could ensure unpredictable errors)</sub> 

          -        $ zas-rep-tools corpora add --path_to_read . --file_format_to_read csv --corp_intern_dbname twitter_streamed_2019 --language en --visibility extern --platform_name twitter --stream_number 1 --sent_splitter True --pos_tagger True --mode prod+ --read_from_zip True  --source unknown --license Twitter_Developer_Agreement_and_Policy --version 1 --sentiment_analyzer True --del_url True --del_punkt True --del_num True --del_html True --case_sensitiv False  --heal_me_if_possible True

---

<br/>

#### Compute StatsDB 

- with Preprocessing

                    $ zas-rep-tools stats compute --corp_fname 7728_corpus_twitter_sifter_de_intern_plaintext.db --stats_intern_dbname sifter --visibility intern --full_repetativ_syntagma True --optimizer True --use_cash True --status_bar True --context_lenght 5 --ignore_url True --ignore_punkt True --ignore_num True


- without Preprocessing

                    $ zas-rep-tools stats compute --corp_fname 7728_corpus_twitter_sifter_de_intern_plaintext.db --stats_intern_dbname sifter --visibility intern --full_repetativ_syntagma True --optimizer True --use_cash True --status_bar True 


- compute for non-full-repetativ syntagmas (see more in definitions)

                    $ zas-rep-tools stats compute --corp_fname 7728_corpus_twitter_sifter_de_intern_plaintext.db --stats_intern_dbname sifter --visibility intern --full_repetativ_syntagma False --optimizer True --use_cash True --status_bar True




---


<br/>


#### Export Statistics from StatsDB

**Exhausted Output-Tables**

- **For scope = 1** (just those syntagmas which have length/scope = 1)

        $ git s

- **For all syntagmas**

        $ zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_en_extern_plaintext.db  --export_file_type csv --output_table_type exhausted --exp_redu True --exp_repl True

- **With additional columns from CorpusDB**

        $ zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_en_extern_plaintext.db  --export_file_type csv --exp_redu True --exp_repl True --max_scope 1 --additional_doc_cols 'gender,age' --corp_fname 7614_corpus_blogs_bloggerCorpus_test_extern_plaintext.db

- **Search in certain syntagmas**
    <sub> ('|' = 'or';  ',' = 'delimiter between words in syntagma'; )</sub> 

     - Stemmed-Search (in lexical basic from) <sub>(syntagma_for_export will be first stemmed)</sub>

                $  zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_de_extern_plaintext.db --export_file_type csv --exp_repl True --exp_redu True --output_table_type exhausted --syntagma_for_export 'klitze,kleine' --exp_syntagma_typ lexem --stemmed_search True


     - POS-search (search in part of speech tags)
            
                $ zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_de_extern_plaintext.db --export_file_type csv  --exp_repl True --exp_redu True --max_scope 1 --output_table_type exhausted --syntagma_for_export 'EMOIMG|EMOASC,number' --exp_syntagma_typ pos


     - Normal-search (search in non-stemmed lexems)

                $  zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_de_extern_plaintext.db --export_file_type csv  --exp_repl True --exp_redu True --output_table_type exhausted --syntagma_for_export 'klitze,kleine' --exp_syntagma_typ lexem

     - Sentiment Search
        <sub> Additional to each export command you can use following options to search just in certain sentiment </sub>

            '--exp_sentiment'

        There was implemented 3 different sentiment polarity:

            ["neutral", "positive","negative"]


<br>

**Summary Output-Tables**

   - ***Replications*** (Letters)
      - Normal search 

            $ zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_en_extern_plaintext.db  --export_file_type csv --output_table_type sum --exp_repl True --word_examples_sum_table True

      - POS-search 

            $ zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_de_extern_plaintext.db --export_file_type csv --exp_redu False --exp_repl True --max_scope 1 --output_table_type sum --syntagma_for_export 'EMOIMG|EMOASC' --exp_syntagma_typ pos

      - Stemmed-Search 

            $  zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_de_extern_plaintext.db --export_file_type csv --exp_repl True --output_table_type sum --syntagma_for_export 'klitze,kleine' --exp_syntagma_typ lexem --stemmed_search True

       - Sentiment Search
            <sub> See before</sub>

   - ***Reduplications*** (Words)
     - Normal search 

            $ zas-rep-tools stats export --stats_fname 7614_3497_stats_bloggerCorpus_en_extern_plaintext.db  --export_file_type csv --output_table_type sum --exp_redu True  --word_examples_sum_table True

     - POS-search + Stemmed-Search + Sentiment Search
        <sub> See before  </sub>



---


<br/>


#### Stream Twitter

            $ zas-rep-tools streamTwitter .   --language de --filter_strategie "t+l"


<br/>


---
---
---
---

<br/>

<a name="input/output"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 8. Input/Output

### Input

 - **FileTypes:**

    - csv
    - xml
    - json
    - txt
    - zip

### Output

 - **FileTypes:**
    - csv
    - xml
    - json

 - **Columns in the Output Tables**
    - **Baseline**
        - syntagma
            <sub>Search Syntagma</sub>
        - stemmed
             <sub>stemmed syntagma</sub>
        - occur_syntagma_all
             <sub>Occurrence Number of the current syntagma in the whole corpus</sub>
        - occur_repl_uniq
             <sub>Occurrence Number of the uniq replication in the current syntagma</sub>
        - occur_repl_exhausted
             <sub>Occurrence Number of the exhausted replication in the current syntagma</sub>
        - occur_redu_uniq
             <sub>Occurrence Number of the uniq reduplication in the current syntagma</sub>
        - occur_redu_exhausted
             <sub>Occurrence Number of the exhausted reduplication in the current syntagma</sub>
        - occur_full_syn_repl
             <sub>Occurrence Number of the full-repetativ syntagma according replications</sub>
        - occur_full_syn_redu
             <sub>Occurrence Number of the full-repetativ syntagma according reduplications</sub>

    - **Document**
        
        - doc_id
             <sub>ID-Number of the current Document</sub>
        - redufree_len
             <sub>Length of the current Text Element from the current Document</sub>

    - **Word**
        
        - normalized_word
             <sub>Repetitions-Free word</sub>
        - rle_word
             <sub>RunLengthEncoded Word</sub>
        - stemmed
             <sub>Stemmed Words</sub>
        - pos
             <sub>Part of Speech Tag</sub>
        - polarity
             <sub>Polarity/Sentiment of the word context and also word it self.</sub>

    - **Repl**
        
        - id
             <sub>Replications ID Number</sub>
        - index_in_corpus
             <sub>Address of the current Word in the corpus.</sub>
        - index_in_redufree
              <sub>Address of the current Word in the reduplications free text element.</sub>
        - repl_letter
             <sub>Replicated letter</sub>
        - repl_length
             <sub>Length of the replication</sub>
        - index_of_repl
             <sub>Index of the current replicated letter in the current normalized_word started from 0</sub>
        - in_redu
             <sub>If current word, which contain an replication is also a part of one reduplication, than here will be the Address of this reduplication</sub>

    - **Redu**
        
        - id
             <sub>Reduplications ID Number</sub>
        - index_in_corpus
             <sub>Address of the current reduplication in the corpus, which </sub>
        - index_in_redufree
              <sub>Address of the current reduplications in the reduplications free text element.</sub>
        - orig_words
             <sub>rle_words and their occurrence number  contained in the current reduplication </sub>
        - redu_length
             <sub>The Length of the current reduplication</sub>

    - **context**
        
        - contextL{number}
             <sub>Context Word left from the current token</sub>
        - context_infoL{number}
             <sub>Additional Data for the Context Word  left from the current token</sub>
        - contextR{number}
             <sub>Context Word right from the current token</sub>
        - context_infoR{number}
            <sub>Additional Data for the Context Word  right from the current token</sub>

 - **Precomputed Example Tables**

    In the Folder 'zas_rep_tools/examples' you could found precomputed examples of the output tables and also the input text collection. 





<br/>

---
---
---
---

<br/>

<a name="restrictions"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 9. Restrictions

**Input:**

 - TXT:
        currently this tool-set support just those txt-files, which has all meta-data in the filename, which could be matched with an regex expression. 




<br/>

---
---
---
---

<br/>

<a name="citing"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 10. Citing ZAS-REP-TOOLS


### How do I Cite AutoVOT in my articles?

***If possible to cite a program, the following format is recommended (adjusting retrieval dates and versions as necessary):***

* Savin, E., Fuchs, S., Ćwiek, A. (2018). ZAS-VOT-TOOLS: A tool for automatic extraction and quantification of the repetition from the written language. [Computer program]. Version 0.1, retrieved August 2018 from https://github.com/savin-berlin/zas-rep-tools.

<br/>



---
---
---
---

<br/><br/>



<a name="errors"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 11. Possible errors and warnings




#### 1. Error: 'Too many open files:'
#####Solutions: 
1. Increase the max number of open files in system:

###### macOS:
    $ sudo launchctl limit maxfiles 3000000 3000000
    $ sysctl -a | grep kern.maxfiles

    (If still not be worked, that test every component separated)


###### Ubuntu:
    $ cat /proc/sys/fs/file-max
    $ ulimit -n 300000
    $ ulimit -n

#### 2. Error: "MemoryError"
It means that your Computer dont have enought of the RAM or the Swap is to short. Please try to increase Swap on your computer. 

###### Ubuntu:
    $ size="8G" && file_swap=/swapfile_$size.img && sudo touch $file_swap && sudo fallocate -l $size /$file_swap && sudo mkswap /$file_swap && sudo swapon -p 20 /$file_swap

    $ sudo swapon --show
    $ free -h

#### 3. Error: In Windows Environment - to long reaction 

    If during the installation process some commands needs more as 5-10 min than try to push "ENTER" Button to ensure the refreshing of the command line 


#### 4. UnicodeDecodeError: 'ascii' codec can't decode byte  in position : ordinal not in range(128)
    - It could be a Problem with the choiced encoding 
    - or the input command wasn't recognized in the right way (corrupt syntax). 


#### 5. 'Permission Error' or 'UserConfigDBGetterError:'
    - execute the command with the admin rights (with following prefix "sudo")


<br/>



---
---
---
---

<br/>


<a name="data"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 12. Data-Examples

There are  also available following examples:

- ***StatdDBs*** and ***CorpusDBs***
    <sub> You can copy-paste this data in your project folders and try to work with that. </sub>
    -       'zas_rep_tools/data/tests_data/testDBs/testFolder'

- ***Output tables*** (csv)
    -       'zas_rep_tools/examples'





<br/>



---
---
---
---

<br/>


<a name="acknowledgements"/>
<p style='text-align: right;'>  <sub> <a href="#toc">Back to top</a>
</sub> </p>

## 13. Acknowledgements


#### A big Thank to the following Peoples, who makes this work and current results possible:

- [Susanne Fuchs](mailto:fuchs@leibniz-zas.de) <sup>*(Linguistic & Organization )*</sup>
- [Ulf Leser](mailto:leser@informatik.hu-berlin.de) <sup>*(Computer Science & Organization )*</sup>
- [Aleksandra Ćwiek](mailto:cwiek@leibniz-zas.de) <sup>*(Linguistic)*</sup>
- [Bodo Winter](mailto:bodo@bodowinter.com) <sup>*(Statistical & linguistic Expertise)*</sup>
- [Stephanie Solt](mailto:solt@leibniz-zas.de) <sup>*(Semantics&Pragmatics)*</sup>
- [Cornelia Ebert](mailto:ebert@leibniz-zas.de) <sup>*(Phonology&Semantics&Pragmatics)*</sup>
- [Manfred Krifka](mailto:krifka@leibniz-zas.de) <sup>*(Semantics&Pragmatics)*</sup>
- [Dominik Koeppl](mailto:dominik.koeppl@uni-dortmund.de) <sup>*(Combinatorics on Words)*</sup>
- [Tatjana Scheffler](mailto:tatjana.scheffler@uni-potsdam.de) <sup>*(NLP+Twitter expertise)*</sup>
- [Stefan Thater](mailto:stth@coli.uni-saarland.de) <sup>*(NLP expertise)*</sup>
- [Katarzyna Stoltmann](mailto:stoltmann@leibniz-zas.de) <sup>*(Linguistic & NLP&Organisation)*</sup>
- [Christina Beckmann](mailto:beckmann@leibniz-zas.de) <sup>*(Bibliographical Expertise)*</sup>
- [Tomasz Kociumaka](mailto:kociumaka@mimuw.edu.pl) <sup>*(Combinatorics on Words)*</sup>
- [Frantisek Franek](mailto:franek@mcmaster.ca) <sup>*(Combinatorics on Words)*</sup>


<br/>


<p align="center">
<table style="width:100%">

  <tr>
    <th><img src="http://www.zas.gwz-berlin.de/uploads/pics/dfg_logo_blau_klein_1a3937.jpg"></th>
    <th><img src="http://www.zas.gwz-berlin.de/uploads/pics/xprag_logo_32.jpg"></th> 
    <th><img src="http://www.zas.gwz-berlin.de/typo3temp/pics/6969c56953.png"></th>
  </tr>
  <tr>
  <td colspan = "3">
    <center>
    <img src="http://www.zas.gwz-berlin.de/fileadmin/images/logo2011.png">
    </center>
  </td>
</tr>
    <tr>
   <td colspan = "3">
    <p>
      <center>
        This research was supported  by an DFG and XPRAG.de  grants   <br/>  to the Leibniz-Center General Linguistics.
      </center>
    </p>
  </td>
</tr>
</table>
</p>


