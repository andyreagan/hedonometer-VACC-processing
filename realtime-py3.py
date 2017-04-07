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

sys.path.append("/users/a/r/areagan/work/2014/03-labMTsimple/")
from labMTsimple.speedy import LabMT
my_LabMT = LabMT(stopVal=0.0)

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
    num_tweets = 0
    failed_loads = 0
    no_text = 0
    no_twitter_lang = 0
    no_user_lang = 0
    failed_parse = 0
    not_english_twitter = 0
    not_english_user = 0
    no_user = 0
    for line in f:
        num_tweets += 1
        try:
            tweet = loads(line)
        except:
            failed_loads += 1
            print("failed to load a tweet")
        try:
            if 'text' in tweet:
                if 'lang' in tweet:
                    if tweet['lang'] == 'en':
                        tweetreader(tweet['text'],all_words)
                    else:
                        not_english_twitter += 1
                else:
                    no_twitter_lang += 1
                    if 'lang' in tweet['user']:
                        if tweet['user']['lang'] == 'en':
                            tweetreader(tweet['text'],all_words)
                        else:
                            not_english_user += 1
                    else:
                        no_user_lang += 1
                        # assume that it is english then....
                        tweetreader(tweet['text'],all_words)
            # from GNIP...
            elif 'body' in tweet:
                if 'twitter_lang' in tweet["object"]:
                    if tweet["object"]['twitter_lang'] == 'en':
                        tweetreader(tweet['body'],all_words)
                    else:
                        not_english_twitter += 1
                else:
                    no_twitter_lang += 1
                    # if "actor" in 
                    if "actor" in tweet['object']:
                        if "languages" in tweet["object"]["actor"]:
                            if "en" in tweet["object"]["actor"]["languages"]:
                                tweetreader(tweet['body'],all_words)
                            else:
                                not_english_user += 1
                        else:
                            no_user_lang += 1
                    else:
                        no_user += 1
                    tweetreader(tweet['body'],all_words)
            else:
                no_text += 1
        except:
            failed_parse += 1
    print('read {0} tweets, failed loading {1} of them'.format(num_tweets,failed_loads))
    print('{0} had no text field (deletes most likely, but dont care to check that)'.format(no_text))
    print('{0} had no twitter lang, {1} has no user field, of those that did {2} had no user lang'.format(no_twitter_lang,no_user,no_user_lang))
    print('failed to parse {0}'.format(failed_parse))
    print('{0} werent english by twitter, {1} without twitter lang werent english users'.format(not_english_twitter,not_english_user))
    return all_words

if __name__ == '__main__':
    # load the things
    # no need to parse and reformat the date...
    outfolder = sys.argv[1]
    outfile = sys.argv[2]
    
    all_word_dict = gzipper()
    pickle.dump(all_word_dict,open('word-dicts/{0}/{1}.py3dict'.format(outfolder,outfile),'wb'))
    textFvec = my_LabMT.wordVecify(all_word_dict)

    f = open("word-vectors/{0}/{1}.csv".format(outfolder,outfile),"w")
    f.write("\n".join(list(map(lambda x: "{0:.7f}".format(x),textFvec))))
    f.close()








