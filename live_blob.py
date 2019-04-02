import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import sys
import time, datetime
style.use('ggplot')

# Step 1 - Authenticate
consumer_key= 'Hp92qr4FSsSH2jMk8Ty1GPrPZ'
consumer_secret= '2KCz8wapRNcefCjghKzbZf1dsuB6lzDbBZijAoPmN6hSwfaleq'

access_token='1108411125580873732-kM67qhq3DDUhJTsNRunmjAO0VNQAZl'
access_token_secret='ICkUHdDBrhhJTTYSpirA8ufJQD6aEt8v1YGFWmAH3CTAo'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

### live plotter skeleton from engineersportal.com...
def live_polarity_plotter(date_vec,pol_data,#pos_pol_data,neg_pol_data,
                          line1,identifier='',pause_time=5, title=''):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(7,3))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(date_vec,pol_data,'-o',alpha=0.8,label='avg polarity')
        #ax.plot(date_vec,pos_pol_data,'-o',alpha=0.8,label='avg positive polarity')
        #ax.plot(date_vec,neg_pol_data,'-o',alpha=0.8,label='avg negative polarity')
        #ax.plot(date_vec,pol_data[1],'-o',alpha=0.8)
        #ax.plot(date_vec,pol_data[2],'-o',alpha=0.8)
        min_date = np.min(date_vec) - datetime.timedelta(seconds=30)
        max_date = np.max(date_vec) + datetime.timedelta(seconds=30)
        ax.set_ylim([-1,1])
        ax.set_xlim([min_date, max_date])
        #update plot label/title
        plt.ylabel('polarity')
        plt.xlabel('date')
        plt.title('polarity of tweets matching \"%s\"' % title)
        plt.legend(loc='lower right', fancybox=True, framealpha=0.5)
        plt.show()

    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_data(date_vec, pol_data)
    # adjust limits if new data goes beyond bounds
    #if np.min(pol_data)<=line1.axes.get_ylim()[0] or np.max(pol_data)>=line1.axes.get_ylim()[1]:
    #        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # print(line1.axes.get_xlim()[0])
    # if np.min(date_vec)<=line1.axes.get_xlim()[0] or np.max(date_vec)>=line1.axes.get_xlim()[1]:
    #     plt.xlim([np.min(date_vec)-np.std(date_vec),np.max(date_vec)+np.std(date_vec)])
    min_date = np.min(date_vec)
    max_date = np.max(date_vec)
    if max_date - min_date > datetime.timedelta(hours=2):
        min_date = max_date - datetime.timedelta(hours=2)
    min_date -= datetime.timedelta(seconds=30)
    max_date += datetime.timedelta(seconds=30)
    plt.xlim([min_date, max_date])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1

# seach match
q = sys.argv[1]

dates, avg_pol, avg_sub, avg_w_pol = [], [], [], []
avg_pos_pol, avg_neg_pol, split_frac = [], [], []

# sleep interval between queries
sleepy = 30

n_updates = 0
max_updates = 100

line1 = []
#while n_updates < max_updates:
while True:
    tnum = 0
    last_id = 0
    n_tweets, n_with_polarity = 0, 0

    pols, subs = [], []
    iters, ids = [], []
    favs, retws = [], []

    public_tweets = api.search(q, count=100, since_id=last_id, lang='en') #, showuser=False)

    last_id = public_tweets[0].id

    for tweet in public_tweets:
        n_tweets += 1
        analysis = TextBlob(tweet.text)

        if analysis.sentiment.polarity != 0.0:
            pols.append(analysis.sentiment.polarity)
            subs.append(analysis.sentiment.subjectivity)
            favs.append(tweet.favorite_count)
            retws.append(tweet.retweet_count)
            ids.append(tweet.id)
            iters.append(tnum)
            n_with_polarity += 1
            tnum += 1

    pos_pols, neg_pols = [], []
    for p in pols:
        if p > 0:
            pos_pols.append(p)
        elif p < 0:
            neg_pols.append(p)

    dates.append(public_tweets[0].created_at)
    avg_pol.append(sum(pols) / len(pols))
    avg_sub.append(sum(subs) / len(subs))
    avg_w_pol.append(n_with_polarity / len(public_tweets))
    avg_pos_pol.append(sum(pos_pols) / len(pos_pols))
    avg_neg_pol.append(sum(neg_pols) / len(neg_pols))
    split_frac.append((len(pos_pols) - len(neg_pols)) /
                      (len(pos_pols) + len(neg_pols)))

    print(n_updates, dates[-1])

    n_updates += 1

    line1 = live_polarity_plotter(dates,
                                  avg_pol,
                                  #avg_pos_pol,
                                  #avg_neg_pol],
                                  line1,title=q)

    # f, axs = plt.subplots(2, 2, figsize=(9, 6))
    #
    # axs[0][0].plot(dates, avg_pol)
    # axs[0][0].plot(dates, avg_pos_pol)
    # axs[0][0].plot(dates, avg_neg_pol)
    # axs[0][0].set_xlabel('date')
    # axs[0][0].set_ylabel('avg_pol')
    # axs[0][0].set_ylim([-1,1])
    #
    # axs[0][1].plot(dates, split_frac)
    # axs[0][1].set_xlabel('date')
    # axs[0][1].set_ylabel('split')
    # axs[0][1].set_ylim([-1,1])
    #
    # axs[1][0].plot(dates, avg_sub)
    # axs[1][0].set_xlabel('date')
    # axs[1][0].set_ylabel('avg_sub')
    # axs[1][0].set_ylim([0,1])
    #
    # axs[1][1].plot(dates, avg_w_pol)
    # axs[1][1].set_xlabel('date')
    # axs[1][1].set_ylabel('avg w pol')
    # axs[1][1].set_ylim([0,1])
    #
    # plt.show()

    # if n_updates < max_updates:
    #     #print("retrieved %d tweets... sleeping for %f seconds" % (n_tweets, sleepy))
    #     time.sleep(sleepy)

print('\n- - - - - - - - - -')
# print('analyzed %d tweets, %0.4f with polarity' % (n_tweets, n_with_polarity/n_tweets))

# plt.hist(pols, 50, range=(-1.0,1.0), alpha=0.6, fill=False, histtype='step')
# plt.hist(subs, 50, range=(-1.0,1.0), alpha=0.6, fill=False, histtype='step')
# plt.show()
