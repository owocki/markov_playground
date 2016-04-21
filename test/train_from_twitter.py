#generates a markov chain based upon a username in twitter
from pymarkovchain import MarkovChain
import re
import time
import sys

import twitter

from local_settings import access_secret, access_token, consumer_key, consumer_secret
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret)


username = sys.argv[1]

get_count = 4000
run_regex = r'[^a-zA-Z. #@]+'

max_id = None
text_statuses = []
statuses = [1]

while len(text_statuses) < get_count and len(statuses) != 0:
    if max_id:
        statuses = api.GetUserTimeline(screen_name=username, count=10000, max_id=max_id, include_rts=False)
    else:
        statuses = api.GetUserTimeline(screen_name=username, count=10000, include_rts=False)
    if len(statuses) > 0:
        max_id = min([status.id for status in statuses]) - 1
        text_statuses = text_statuses + [status.text for status in statuses]
    print("got {} of {} statuses".format(len(text_statuses), get_count))


train_text = ".".join(text_statuses)
if run_regex:
    train_text = re.sub(run_regex, ' ', train_text).replace('\n', '')

print('generating db on ' + username)
mc = MarkovChain("./markov")
mc.generateDatabase(train_text)
print('done generating db')

while True:
    output = mc.generateString()
    print(output)
    time.sleep(1)
