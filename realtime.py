# processTweetsNew.py
# crawl the tweets, and compute the labMT vectors around keywords
# output with daily resolution
#
# NOTES
# uses the new 15-minute compressed format
# 
# USAGE 
# gzip -cd tweets.gz | python processTweetsNew.py 2014-01-01 keywords
#  
# this will read keywords.txt and the tweets from stdin
# and save a frequency file, labMT vector in keywords/[keyword]
# for each keyword

# we'll use most of these
from json import loads
import codecs
import datetime
import re
import numpy
import sys
import pickle

from labMTsimple.speedy import *
labMT = sentiDict('LabMT',stopVal=0.0)

def tweetreader(tweettext,wordDict):
    words = [x.lower() for x in re.findall(r"[\w\@\#\'\&\]\*\-\/\[\=\;]+",tweettext,flags=re.UNICODE)]
    for word in words:
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1
    
def gzipper():
    all_words = dict()
    f = sys.stdin
    for line in f:
        try:
            tweet = loads(line)
        except:
            print "failed to load a tweet"
        try:
            if tweet['text'] and tweet['lang'] == 'en':
                tweetreader(tweet['text'],all_words)
        except:
            # print "no text"
            pass
    return all_words

if __name__ == '__main__':
    # load the things
    # no need to parse and reformat the date...
    outfolder = sys.argv[1]
    outfile = sys.argv[2]
    
    all_word_dict = gzipper()
    pickle.dump(all_word_dict,open('word-dicts/{0}/{1}.dict'.format(outfolder,outfile),'w'))
    textFvec = labMT.wordVecifyTrieDict(all_word_dict)

    f = open("word-vectors/{0}/{1}.csv".format(outfolder,outfile),"w")
    f.write('{0:.0f}'.format(textFvec[0]))
    for k in xrange(1,len(textFvec)):
      f.write(',{0:.0f}'.format(textFvec[k]))
    f.close()








