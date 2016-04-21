#trains on erowid trip reports, donald trump speeches. and tweets things
# https://twitter.com/TrumpErowid

from local_settings import access_secret, access_token, consumer_key, consumer_secret

from pymarkovchain import MarkovChain

import re
import time
import sys
import os
import random
import twitter

#config
wait_time_between_tweets_in_secs = 60
num_tweets = 3
remove_words = ['LAUGHTER', 'CHEERS', 'APPLAUSE', 'AUDIENCE','MUSIC','COOPER','WALLACE','TRUMP']
src_dirs = [
    ("src/trump",6),
    ("src/erowid",1300),
#    ("src/cover_letter",5),
]
seed_words = ['Obama', 'Christie', 'Bush', "Rubio", 'Obamacare']

#helper functions
def ucfirst(sentence):
    return sentence[0].upper() + sentence[1:]

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def validate_tweet(status):
    num_words = len(status.split(" ")) + 1
    if num_words < 3:
        return False;
    return True

#setup 
mc = MarkovChain("./markov")
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret)

#pull train_text
train_text = ""
for meta in src_dirs:
    _dir = meta[0]
    num_files = meta[1]
    for root, dirs, files in os.walk(_dir, topdown=False):
        random.shuffle(files)
        for name in files:
            num_files -= 1
            if num_files > 0:
                _path = "{}/{}".format(_dir,name)
                train_text += file_get_contents(_path)


#scrub train_text
train_text = re.sub('<[^<]+?>', '', train_text) #remove html
train_text = re.sub(r'[^a-zA-Z. ]+', ' ', train_text).replace('\n', '') #remove non-alphanumeric chars
for word in remove_words:
    train_text = train_text.replace(word,'') #remove words

#create markov db
mc.generateDatabase(train_text)

#tweet
for x in range(0,num_tweets):
    random.shuffle(seed_words)
    status = (ucfirst(mc.generateStringWithSeed(seed_words[0])) + ".  ")
    if not validate_tweet(status):
        continue;
    try:
        status = api.PostUpdate(status)
    except:
        pass
    time.sleep(wait_time_between_tweets_in_secs)

