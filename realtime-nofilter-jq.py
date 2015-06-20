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
    replaceStrings = ['---','--','\'\'']
    for replaceString in replaceStrings:
        tweettext = tweettext.replace(replaceString,' ')
    words = [x.lower() for x in re.findall(r"[\w\@\#\'\&\]\*\-\/\[\=]+",tweettext,flags=re.UNICODE)]
    for word in words:
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1
    
def gzipper():
    all_words = dict()
    f = sys.stdin
    numtweets = 0
    failedloads = 0
    notext = 0
    failedchecktext = 0
    notenglish = 0
    nolang = 0
    failedlangcheck = 0
    failedparse = 0
    for line in f:
        numtweets+=1
        tweet = loads(line)
        tweetreader(tweet['text'],all_words)

    print('read {0} tweets, failed loading {1} of them'.format(numtweets,failedloads))
    print('{0} had no text, {1} failed checking the text field'.format(notext,failedchecktext))
    print('{0} were not english, {1} had no lang field, and {2} failed to check lang at all'.format(notenglish,nolang,failedlangcheck))
    print('failed to parse {0}'.format(failedparse))
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








