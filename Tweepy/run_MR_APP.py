# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 17:20:51 2020

@author: J. Dalmases
Projecte: Estudi Dia Mundial de les Malalties Rares
Objectiu: Procés de recollida de dades en Twitter.
Implementació: Streaming usant la llibreria Tweepy.
Framework: Spyder (Anaconda Framework)
Codi: Python v 3.8

"""
import tweepy
import codecs
import json

from secret1 import CONSUMER_KEY_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET_KEY;
from datetime import datetime

def get_auth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY_KEY, CONSUMER_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET_KEY)
    return auth

class MyStreamListener(tweepy.StreamListener):
    
#    def on_error(self, status_code):
#        if status_code == 420:
#            print("Error 420")
#        elif status_code == 503:
#            print("Error 503")
        #returning False in on_data disconnects the stream
#        return False
        
    def on_data(self, data):
        try:
            now=datetime.now()
            data_m = now.strftime("%Y/%m/%d - %H:%M:%S")
            print(data_m)
            data_actual = now.strftime("%Y_%m_%d")
            tweet = json.loads(data)
            id_tweet = tweet.get('id_str')
            data_tweet = str(tweet.get('created_at'))
            user_tweet_name = tweet.get('user').get('name')
            user_tweet_screen_name = tweet.get('user').get('screen_name')
            tweet_truncat=tweet.get("truncated")
            if tweet_truncat:
                text_tweet=tweet.get("extended_tweet").get("full_text")
            else:
                text_tweet = tweet.get('text')
                
            retweet="False"
            if tweet.get("retweeted_status") is not None:
                retweet = "True"
                if tweet.get("retweeted_status").get("truncated"):
                    text_tweet=tweet.get("retweeted_status").get("extended_tweet").get("full_text")
                else:
                    text_tweet = tweet.get("retweeted_status").get('text')
                    
            if tweet.get("retweet_count")>0 or tweet.get("is_quote_status"):
                retweet = "True"
            else:
                retweet = "False"
                
            print("------------------------------------------------------")
            regTweet=""
            regTweet = "Tweet ID: " + id_tweet
            regTweet = regTweet + "\nData: " + data_tweet 
            regTweet = regTweet + "\nUser_name: " + user_tweet_name 
            regTweet = regTweet + "\nUser_screen_name: " + user_tweet_screen_name
            regTweet = regTweet + "\nTweet:\n" + text_tweet
            regTweet = regTweet + "\nReTweet: " + retweet

            print(regTweet)
            
            with codecs.open("TWEETS_RAW_"+ data_actual +".txt", "a", encoding="utf-8") as myfile:
                #json.dump(data, myfile, ensure_ascii=False)
                myfile.write(data)
                myfile.close()
            with codecs.open("TWEETS_"+ data_actual +".txt", "a", encoding="utf-8") as myfile1:
                registre='{"data": "' + data_tweet + '",\n' 
                registre = registre + '"name": "' + user_tweet_name + '",\n' 
                registre = registre + '"screen_name": "' + user_tweet_screen_name + '",\n'
                registre = registre + '"text": "' + text_tweet + '",\n'
                registre = registre + '"ReTweet: "' + retweet + '"},\n'
                myfile1.write(registre)
                myfile1.close()
            
        except Exception as e:
            print(data_m)
            print("ERROR: {}".format(e))
        finally:
            return True  # Keep listening      
        

if __name__ == '__main__':
    print(" ----- Twitter Procés Captació ----- ")
    
    # Here starts my program
    # Get an API item using tweepy
    auth = get_auth()  # Retrieve an auth object using the function 'get_auth' above
    api = tweepy.API(auth)  # Build an API object.

    # Test it works
#    api.update_status('Importante ! Pronto se celebra el dia mundial de las enfermedades raras! #DiaMundialEnfermedadesRaras')    
    
    # Connect to the stream
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    print(">> Capturant tweets sobre:\n#DiaMundialEnfermedadesRaras\n#RareDiseaseDay\n#SomosFEDER\n#EnfermedadesRaras\n#DMEnfermedadesRaras2020\n#DM2020")
    #myStream.filter(track=['#DiaMundialEnfermedadesRaras,#DíaMundialEnfermedadesRaras,#SomosFEDER,#enfermedadesraras'],languages=['es'])    
    myStream.filter(track=['#DiaMundialEnfermedadesRaras,#RareDiseaseDay,#SomosFEDER,#EnfermedadesRaras,#DMEnfermedadesRaras2020,#DM2020'])
    