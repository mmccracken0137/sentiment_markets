import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import sys
import time

# Step 1 - Authenticate
consumer_key= 'Hp92qr4FSsSH2jMk8Ty1GPrPZ'
consumer_secret= '2KCz8wapRNcefCjghKzbZf1dsuB6lzDbBZijAoPmN6hSwfaleq'

access_token='1108411125580873732-kM67qhq3DDUhJTsNRunmjAO0VNQAZl'
access_token_secret='ICkUHdDBrhhJTTYSpirA8ufJQD6aEt8v1YGFWmAH3CTAo'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

q = sys.argv[1]
max_tweets = 10000

pols, subs = [], []
iters, ids = [], []
favs, retws = [], []

tnum = 0
last_id = 0
n_tweets, n_with_polarity = 0, 0

while n_tweets < max_tweets:
    public_tweets = api.search(q, count=100, since_id=last_id, lang='en') #, showuser=False)

    last_id = public_tweets[0].id
    print(last_id)

    #print('tweet_id\t\tpolarity\tsubjectivity')
    # for tweet in public_tweets:
    #     #print('\n- - - - - - - - - -')
    #     print(tweet.text)
    #print('\n- - - - - - - - - -')

    for tweet in public_tweets:
        n_tweets += 1
        analysis = TextBlob(tweet.text)
        #print("%d  \t%0.4f  \t%0.4f" % (tweet.id,
        #                                analysis.sentiment.polarity,
        #                                analysis.sentiment.subjectivity))
        if analysis.sentiment.polarity != 0.0:
            pols.append(analysis.sentiment.polarity)
            subs.append(analysis.sentiment.subjectivity)
            favs.append(tweet.favorite_count)
            retws.append(tweet.retweet_count)
            ids.append(tweet.id)
            iters.append(tnum)
            n_with_polarity += 1
            tnum += 1
        #print("")
    if n_tweets < max_tweets:
        print("retrieved %d tweets... sleeping for 2 seconds" % n_tweets)
        time.sleep(5)

print('\n- - - - - - - - - -')
print('analyzed %d tweets, %0.4f with polarity' % (n_tweets, n_with_polarity/n_tweets))

plt.hist(pols, 50, range=(-1.0,1.0), alpha=0.6, fill=False, histtype='step')
plt.hist(subs, 50, range=(-1.0,1.0), alpha=0.6, fill=False, histtype='step')
plt.show()

plt.plot(iters, ids)
plt.xlabel('iter')
plt.ylabel('tweet id')
plt.show()

plt.plot(ids, pols, 'r.')
plt.xlabel('tweet id')
plt.ylabel('polarity')
plt.show()

plt.plot(subs, pols, 'r.')
plt.xlabel('subjectivity')
plt.ylabel('polarity')
plt.show()

plt.plot(pols, favs, 'r.')
plt.xlabel('polarity')
plt.ylabel('likes')
plt.show()
