#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Python wrapper for runTagger.sh script for CMU's Tweet Tokeniser and Part of Speech tagger: http://www.ark.cs.cmu.edu/TweetNLP/

Usage:
results=runtagger_parse(['example tweet 1', 'example tweet 2'])
results will contain a list of lists (one per tweet) of triples, each triple represents (term, type, confidence)
"""
import subprocess
import shlex
import os
import sys 
from zas_rep_tools.src.utils.helpers import path_to_zas_rep_tools
from zas_rep_tools.src.utils.debugger import p

# The only relavent source I've found is here:
# http://m1ked.com/post/12304626776/pos-tagger-for-twitter-successfully-implemented-in
# which is a very simple implementation, my implementation is a bit more
# useful (but not much).

# NOTE this command is directly lifted from runTagger.sh
path_to_zas_rep_tools
path_to_jar = os.path.join(path_to_zas_rep_tools, "src/extensions/tweet_nlp/ark_tweet_nlp/ark-tweet-nlp-0.3.2.jar")
RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar {}".format(path_to_jar)


def _split_results(rows):
    """Parse the tab-delimited returned lines, modified from: https://github.com/brendano/ark-tweet-nlp/blob/master/scripts/show.py"""
    for line in rows:
        line = line.strip()  # remove '\n'
        if len(line) > 0:
            if line.count('\t') == 2:
                parts = line.split('\t')
                tokens = parts[0]
                tags = parts[1]
                try:
                    confidence = float(parts[2])
                except ValueError:
                    confidence = float(parts[2].replace(",", ".") )
                yield tokens, tags, confidence


def _call_runtagger(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    """Call runTagger.sh using a named input file"""

    # remove carriage returns as they are tweet separators for the stdin
    # interface
    tweets_cleaned = [tw.replace('\n', ' ') for tw in tweets]
    message = "\n".join(tweets_cleaned)

    # force UTF-8 encoding (from internal unicode type) to avoid .communicate encoding error as per:
    # http://stackoverflow.com/questions/3040101/python-encoding-for-pipe-communicate
    message = message.encode('utf-8')

    # build a list of args
    args = shlex.split(run_tagger_cmd)
    args.append('--output-format')
    args.append('conll')
    po = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # old call - made a direct call to runTagger.sh (not Windows friendly)
    #po = subprocess.Popen([run_tagger_cmd, '--output-format', 'conll'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = po.communicate(message)
    # expect a tuple of 2 items like:
    # ('hello\t!\t0.9858\nthere\tR\t0.4168\n\n',
    # 'Listening on stdin for input.  (-h for help)\nDetected text input format\nTokenized and tagged 1 tweets (2 tokens) in 7.5 seconds: 0.1 tweets/sec, 0.3 tokens/sec\n')

    pos_result = result[0].strip('\n\n')  # get first line, remove final double carriage return
    pos_result = pos_result.split('\n\n')  # split messages by double carriage returns
    pos_results = [pr.split('\n') for pr in pos_result]  # split parts of message by each carriage return
    return pos_results


def runtagger_parse(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    """Call runTagger.sh on a list of tweets, parse the result, return lists of tuples of (term, type, confidence)"""
    pos_raw_results = _call_runtagger(tweets, run_tagger_cmd)
    #print "tweets=", tweets
    #print "pos_raw_results=",pos_raw_results
    #sys.exit()
    pos_result = []
    #print tweets
    for pos_raw_result in pos_raw_results:
        #p(pos_raw_results, "pos_raw_result")
        #sys.exit()
        #print "1pos_raw_result=", pos_raw_result
        splitted =  list(_split_results(pos_raw_result))[0]
        #print "splitted=", splitted
        #p((len(splitted),splitted), "splitted)")
        pos_result.append((splitted[0].decode("utf-8"),splitted[1].decode("utf-8")))
    #p(pos_result, "pos_result")
    return pos_result


def check_script_is_present(run_tagger_cmd=RUN_TAGGER_CMD):
    """Simple test to make sure we can see the script"""
    success = False
    try:
        args = shlex.split(run_tagger_cmd)
        #print args
        args.append("--help")
        po = subprocess.Popen(args, stdout=subprocess.PIPE)
        #print(po.communicate())
        # old call - made a direct call to runTagger.sh (not Windows friendly)
        #po = subprocess.Popen([run_tagger_cmd, '--help'], stdout=subprocess.PIPE)
        #p(po.poll(), "11po.poll()")
        i = -1
        while not po.poll():
            i+= 1
        #for answer in po.poll():
            #if not answer:
            #    break
            #p(po.poll(), "po.poll()")
            #_1 = repr(answer)
            #_2 = type(answer)
            #print "_1= ", _1, " _2= ", _2
            stdout = list(po.stdout)
            #p(stdout, "stdout")
            if i >= 2: break
            if not stdout: break
            lines = [l for l in stdout]
            return "RunTagger [options]" in lines[0]
            #p(lines,"lines")
            
        #print 
        # we expected the first line of --help to look like the following:
        
        #success = True
    except OSError as err:
        print "Caught an OSError, have you specified the correct path to runTagger.sh? We are using \"%s\". Exception: %r" % (run_tagger_cmd, repr(err))
    return success


if __name__ == "__main__":
    print "Checking that we can see \"%s\", this will crash if we can't" % (RUN_TAGGER_CMD)
    success = check_script_is_present()
    if success:
        print "Success."
        print "Now pass in two messages, get a list of tuples back:"
        tweets = ['this is a message', 'and a second message']
        print runtagger_parse(tweets)
