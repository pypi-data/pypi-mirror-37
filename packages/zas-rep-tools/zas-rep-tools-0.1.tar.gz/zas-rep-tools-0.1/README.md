 
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

<br/>
<br/>
**ZAS-REP-TOOLS** is a bundle of Tools for automatic extraction and quantification of the repetitions from the unstructured textual Data Collections for different languages with additional Search Engine wrapped around extracted data +  on-board supplied Twitter Streamer to collect real-time tweets. 


<br/>
<br/>

---

**<span style="color:red;">For a quick-start,</span>** first [download and install all dependencies](#dependencies) , then [download and compile the code](#settingup) and afterwards go to the [Tutorials](#tutorials) section to begin.

___


<br/>
<br/>


<a name="toc"/>
## Table of Contents
1. [Dependencies Installation](#dependencies)
    - On Linux 
    - On Windows 
    - On MacOS 

2. [Setting up](#settingup)
3. [Definitions](#definitions)
   -  Repetition
   -  Full Repetitiveness

4. [Functionality](#functionality)
   - Classes
   - Multiprocessing
   - NLP-Methods
   - InternDataBase-Structure
     - SQLite
     - ZODB
   - Additional Features
     - Formatters
     - Templates

5. [WorkFlow](#workflow)

6. [Tutorials](#tutorials)
   - Python Package Tutorial 
   -  Command line Tutorial

7. [Input/Output](#input/output)
   - File Formats
   - Output Statistics

8. [Citing ZAS-REP-TOOLS](#citing)

9. [Acknowledgements](#acknowledgements)

---
---


<br/>
<br/>
<br/>




<a name="dependencies"/>
## 1. Dependencies
In order to use ZAS-REP-TOOLS you'll need the following installed in addition to the source code provided here:
* [Python (both Versions: 2.7 + 3.5 or later)](https://www.python.org/download/releases/2.7.6>)
* [JAVA JDC 6](https://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase6-419409.html) 
* [GCC, the GNU Compiler Collection](http://gcc.gnu.org/install/download.html)
* [SQLite3](https://www.sqlite.org/download.html)
* [NoseTests](https://nose.readthedocs.io/en/latest/)
* [Pysqlcipher](https://github.com/leapcode/pysqlcipher)
* Git


#### Dependencies Installation 
following installation commands should be seeing as just an idea how and could become incorrect with time. Important is, that all above listed Dependencies are installed, before you can start to SetUp the Tool.

##### On Linux (UbuntuOS 16.04.5 LTS)
    1. open Terminal/Bash/Shell
    2. Upgrade default linux tools
        $ sudo apt-get update
        $ sudo apt-get upgrade
    2. Python Installation
        -> python + pip 
            $ sudo apt install python2.7 python-pip
            $ sudo apt install python3 python3-pip
            $ sudo apt-get install python-setuptools python-dev  build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev
            (https://stackoverflow.com/questions/26053982/setup-script-exited-with-error-command-x86-64-linux-gnu-gcc-failed-with-exit)

            $ sudo apt-get install python-software-properties
            $ sudo -H pip2 install --upgrade pip
            $ sudo -H pip3 install --upgrade pip
            $ sudo -H pip install --upgrade setuptools
        -> Additional Python3 packages, which will not be installed automatically 
            $ sudo -H python3 -m pip install somajo
            $ sudo -H python3 -m pip install someweta
     
    3. GCC Compiler
        $ sudo apt-get install g++

    4. OpenSSL
        $ sudo apt-get install openssl

    5. Git
        $ sudo apt install git
        
    4. Sqlite + Pysqlcipher
        $ sudo apt-get install sqlite3
        $ sudo apt-get install sqlcipher
        $ sudo -H python2 -m pip install pysqlcipher --install-option="--bundled"
        compile json1 - extention 

      5. JAVA
            LINK: (https://wiki.ubuntuusers.de/Archiv/Java/Installation/Oracle_Java/Java_6/) 
            $ sudo add-apt-repository ppa:webupd8team/java
            $ sudo apt-get update
            $ sudo apt-get install oracle-java6-installer 
            
            


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




<br/>
##### On macOS (10.13.6)
    1. Install brew
        $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    2. Install Python
        -> python ( pip (2+3)
            $ brew install python2
            $ brew install python3
            $ sudo python2 -m ensurepip
            $ sudo python3 -m ensurepip
            $ pip2 install --upgrade pip
            $ pip3 install --upgrade pip
        ->  Command Line Tools for Xcode
            (https://developer.apple.com/download/more/)
            (You will need a registered Apple ID to download either package.3)
        -> Additional python packages (for Python3)
            (which will not be installed automatically)  
            $ sudo python3 -m pip install somajo
            $ sudo python3 -m pip install someweta

    3. Sqlite + Pysqlcipher
            $ brew install sqlite
            $ brew install openssl
            $ brew install sqlcipher
            $ sudo python2 -m pip install pysqlcipher --install-option="--bundled"
            compile json1 - extention 
                $ gcc -g -fPIC -dynamiclib sqlite-src-3140100/ext/misc/json1.c -o json1
       
     4. Java (for TweetNLP Tokenizer and POS Tagger)
            $ brew cask install java





<br/>
---


<a name="settingup"/>
## 2. Setting up

<br/>

---

<a name="definitions"/>
## 3. Definitions

We differentiate between two types of repetitions:

 * **Replications** (every Repetition on the letter level)
 * **Reduplications** (every Repetition on the word level)



<br/>

---

<a name="functionality"/>
## 4. Functionality

This Tool:
 - read Data from
and also automatic annotation of those data (POS-Tagging, Sentiment Analysis etc. )



<br/>

---

<a name="workflow"/>
## 5. WorkFlow

<br/>

---

<a name="tutorials"/>
## 6. Tutorials

<br/>

---

<a name="input/output"/>
## 7. Input/Output

<br/>

---

<a name="citing"/>
## 8. Citing ZAS-REP-TOOLS

<br/>

---

<a name="acknowledgements"/>
## 9. Acknowledgements



---


----

Acknowledgements



Was helped:
- Bodo Winter (Statistical & lingusitical Expertise)
- Stephanie Solt (solt@leibniz-zas.de)


- Dominik Koeppl (dominik.koeppl@uni-dortmund.de) {Combinatorics on Words}
- Tatjana Scheffler (tatjana.scheffler@uni-potsdam.de) {NLP+Twitter expertise}
- Stefan Thater (stth@coli.uni-saarland.de) {NLP expertise}
- Katarzyna Stoltmann (stoltmann@leibniz-zas.de) {Lingustics & NLP}
- Christina Beckmann (beckmann@leibniz-zas.de) {Bibliographical Expertise}
- Tomasz Kociumaka (kociumaka@mimuw.edu.pl) {Combinatorics on Words}
- Frantisek Franek (franek@mcmaster.ca) {Combinatorics on Words}


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