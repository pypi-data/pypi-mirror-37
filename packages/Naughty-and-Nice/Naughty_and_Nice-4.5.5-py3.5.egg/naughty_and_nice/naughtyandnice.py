##IMPORTS
import tweepy
import json
import re
import string
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

##SET UP TWITTER
with open('/home/pi/Documents/twitter_auth.json') as f:
    keys = json.load(f)

## Or On Windows ##
#with open (r'C:\Users\username\path_to\twitter_auth.json')
#	keys = json.load(f)

consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

##TWITTER STREAM
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweets.append(status.text.rstrip())
        print(status.text.rstrip())
        if len(tweets) > int(howManyTweets):
            myStream.disconnect()


class naughty_and_nice():
    def __init__(self, tweets):
        #myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

        ##EMOJI DATA
        self.pos_emojis = [chr(uni) for uni in [128537, 10084, 128525, 128147, 128535, 9786, 128522, 128539, 128149, 128512, 128515, 128538]]
        self.neg_emojis = [chr(uni) for uni in [9785, 128533, 128553, 128530, 128544, 128528, 128550, 128547, 128555, 128534, 128542, 128148, 128546, 128543]]

        self.all_emojis = self.pos_emojis + self.neg_emojis

        ##FETCH SOME TWEETS
        myStream.filter(track=self.all_emojis, languages=['en'])

        ##MAKE SELF.TWEETS THE SAME AS TWEETS
        self.tweets = tweets

        ##RUN THE BOT
        self.bot()

        ##GENERATE EXIT CODE
        self.exit_code = random.randint(100,1000)
        print("PERFECT RUN! EXIT CODE: " + str(self.exit_code))
        print("Done")

    ##STORE TWEETS
    def store_tweets(self, file, tweets):
        with open(self.file, 'r') as f:
            self.old_tweets = f.readlines()
        self.all_tweets = self.old_tweets + self.tweets
        self.all_tweets = list(set(self.all_tweets))
        self.all_tweets = [self.tweet.replace('\n','')+"\n" for self.tweet in self.all_tweets]

        with open(self.file, 'w') as f:
            f.writelines(self.all_tweets)

        return self.all_tweets

    ##CLEAN TWEETS
    def clean_tweets(self, tweets):
        self.tweets = [self.tweet.rstrip() for self.tweet in self.tweets]
        self.tweets = [re.sub(r'http\S+', '', self.tweet) for self.tweet in self.tweets]
        self.tweets = [re.sub(r'@\S+', '', self.tweet) for self.tweet in self.tweets]
        self.tweets = [self.tweet.translate({ord(char): '' for char in string.punctuation}) for self.tweet in self.tweets]
        return self.tweets

    ##SORT TWEETS
    def sort_tweets(self, tweets):
        self.positive_tweets = [self.tweet for self.tweet in self.tweets if set(self.tweet) & set(self.pos_emojis)]
        self.negative_tweets = [self.tweet for self.tweet in self.tweets if set(self.tweet) & set(self.neg_emojis)]
        self.positive_tweets = [re.sub(r'[^\x00-\x7F]+','', self.tweet) for self.tweet in self.positive_tweets]
        self.negative_tweets = [re.sub(r'[^\x00-\x7F]+','', self.tweet) for self.tweet in self.negative_tweets]

        return self.positive_tweets, self.negative_tweets

    ##PARSE TWEETS
    def parse_tweets(self, words):
        self.words = words.lower()
        self.words = word_tokenize(self.words)
        self.words = [self.word for self.word in self.words if self.word not in stopwords.words("english")]
        self.word_dictionary = dict([(self.word, True) for self.word in self.words])
        return self.word_dictionary

    ##TRAIN THE CLASSIFIER
    def train_classifier(self, positive_tweets, negative_tweets):
        self.positive_tweets = [(self.parse_tweets(self.tweet),'positive') for self.tweet in self.positive_tweets]
        self.negative_tweets = [(self.parse_tweets(self.tweet),'negative') for self.tweet in self.negative_tweets]
        self.fraction_pos =  round(len(self.positive_tweets) * 0.8)
        self.fraction_neg =  round(len(self.negative_tweets) * 0.8)

        self.train_set = self.negative_tweets[:self.fraction_pos] + self.positive_tweets[:self.fraction_pos]
        self.test_set =  self.negative_tweets[self.fraction_neg:] + self.positive_tweets[self.fraction_neg:]
        self.classifier = NaiveBayesClassifier.train(self.train_set)
        self.accuracy = nltk.classify.util.accuracy(self.classifier, self.test_set)
        return self.classifier, self.accuracy

    ##CALCULATING NAUGHTINESS
    def calculate_naughty(self, classifier, accuracy, user):
        self.user_tweets = api.user_timeline(screen_name = self.user, count=200)
        self.user_tweets = [self.tweet.text for self.tweet in self.user_tweets]
        self.user_tweets = self.clean_tweets(self.user_tweets)
        self.rating = [self.classifier.classify(self.parse_tweets(self.tweet)) for self.tweet in self.user_tweets]
        self.percent_naughty = self.rating.count('negative') / len(self.rating)
        if self.percent_naughty > 0.5:
            print(self.user, "is", self.percent_naughty * 100, "percent NAUGHTY with an accuracy of", self.accuracy * 100)
            self.naughtiness = self.user, "is", self.percent_naughty * 100, "percent NAUGHTY with an accuracy of", self.accuracy * 100

        else:
            print(self.user, "is", 100 - (self.percent_naughty * 100), "percent NICE with an accuracy of", self.accuracy * 100)
            self.naughtiness = self.user, "is", 100 - (self.percent_naughty * 100), "percent NICE with an accuracy of", self.accuracy * 100

        return self.naughtiness

    ##EXECUTE THE PROGRAM AND THE BOT/SHELL
    def bot(self):
        print("You have entered the naughty and nice shell. Type \"Help\" for more info")
        while True:
            comm = input("> ")

            #if the command is "Help"
            if comm == "Help":
                print("Help: Type \"Help\" to get this menu. Type \"Store Tweets\" to store the tweets you have collected ", end="")
                print("in a file called tweets.txt. Type \"Calculate Naughtiness\" to calculate the naughtiness of one users's twitter profile. You will be prompted to give the user's username. Type \"Exit\" to exit the program.")

            #if the command is "Store Tweets"
            elif comm == "Store Tweets":
                print("Storing Tweets...")
                self.file = 'tweets.txt'
                self.tweets = self.store_tweets(self.file, self.tweets)
                print("Done")

            #if the command is "Calculate Naughtiness"
            elif comm == "Calculate Naughtiness":
                print("Cleaning Tweets...")
                self.tweets = self.clean_tweets(self.tweets)
                print("Done")
                print("Sorting Tweets...")
                self.pos_tweets, self.neg_tweets = self.sort_tweets(self.tweets)
                print("Done")
                print("Training Classifier...")
                self.classifier, self.accuracy = self.train_classifier(self.pos_tweets, self.neg_tweets)
                print("Done")
                self.user = input("Which user's account do you want to calculate their naughtiness? Enter a username. ")
                print("Calculating Naughtiness from " + self.user + "...")
                msg = self.calculate_naughty(self.classifier, self.accuracy, self.user)
                print("Done")
                ans = input("Do you want to tweet this person's naughtiness on twitter? Y/n ")
                if ans == "Y" or ans == "y":
                    self.msg = str(msg)
                    print("Tweeting " + self.msg)
                    api.update_status(self.msg)

                else:
                    print("Ok")

            #if the command is "Exit"
            elif comm == "Exit":
                print("Exiting...")
                break

            #Else
            else:
                print("That is not a command!")

while True:

    howManyTweets = input("How many tweets do you want? ")
    try:
        howManyTweets = int(howManyTweets)
        break

    except Exception as e:
        print(str(e) + " . Please try again!")

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)    
tweets = []
naughty_and_nice(tweets)
