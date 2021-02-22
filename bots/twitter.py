# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 11:02:35 2021

@author: Moosa
"""

import tweepy
import logging 
import os
import telebot
import logging
import threading
import time
import sys
from config import api

log_level = os.getenv("LOG_LEVEL")

logger1 = telebot.logger
telebot.logger.setLevel(log_level)


tw_token = os.getenv("TWITTER_TOKEN")

chat_id = os.getenv("CHAT_ID")
group_id = os.getenv("GROUP_ID")
bot = telebot.AsyncTeleBot(tw_token, parse_mode=None)
logger = logging.getLogger()
logger.setLevel(log_level)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

twits = []
user_ids=[]
handles=[]
api1=None
t2=None
mod_time = None
stream = None

class reload_ids(threading.Thread):
    def __init__(self, sleep_interval=1):
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval

    def run(self):
        while True:
            logger.info('Thread Running/ Checking for file modification')
            global mod_time
            if os.stat('/twit-tele/handles.txt').st_mtime != mod_time:   
                logger.info('File modified')
                mod_time = os.stat('/twit-tele/handles.txt').st_mtime
                reload()
            else: logger.info('No modification')
            is_killed = self._kill.wait(self._interval)
            if is_killed:   
                break
        
    def kill(self):
        logger.info("Killing Thread/ Twitter Bot")
        self._kill.set()
        

class reload_stream(threading.Thread):

    def run(self):
        logger.info('Thread Running/ Reload Stream')
        stream_start()


def send_tele(post):
    logger.info("Sending message to telegram")
    bot.send_message(chat_id,post)
    time.sleep(2)
    bot.unpin_all_chat_messages(group_id)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        twits.append(tweet)
        post = f"{tweet.user.name}:\n{tweet.text}:\nhttps://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"

        with open('/twit-tele/fetched_tweets.txt','a') as tf:
            tf.write('\n'+str(tweet))
            
        logger.debug("Tweet user ID "+str(tweet.user.id))
        
        if not tweet.in_reply_to_user_id and tweet.user.id in user_ids: 
            if 'RT @' in tweet.text:
                logger.info('Retweet RT')
                return
            else:
                logger.info('Empty user reply id')
                send_tele(post)
                return
        
        else:
            if (str(tweet.user.id)  in user_ids):           
                logger.info('User Id in reply')
                send_tele(post)    
                return
            else:
                logger.info('Other reply')
                return

    def on_error(self, status):
        logger.critical("Error detected: "+str(status))
        if status == 420:
            return False




def get_ids(api1):
    user_objects= []
    try:
        user_objects = api1.lookup_users(screen_names=
                                          handles)
    except Exception as e:
        logger.error("user_id Error")
        raise e
                                        
    user_ids = [user.id_str for user in user_objects]
    logger.info("User IDs = "+str(user_ids))
    return user_ids

def stream_start():
    global stream
    if stream:
        stream.running = False  
        logger.info('Stream closing')
        time.sleep(2)
    logger.info('Starting Stream')
    tweets_listener = MyStreamListener(api1)
    stream = tweepy.Stream(api1.auth, tweets_listener)
    stream.filter(follow=user_ids,is_async=True)

def reload():
    logger.info('Reloading IDs/ Twitter Bot')
    with open('/twit-tele/handles.txt','r') as tf:
        tf.seek(0)
        global handles
        handles=tf.read()
        if not handles=='':
            h=[]
            for i in filter(None,handles.split(',')):
                h.append(i)
            handles=h
        else:
            handles='test'
        logger.info('Handles are '+str(handles))
        global user_ids
        user_ids = get_ids(api1)
    global t2
    t2 = reload_stream()
    t2.start()




def main():
    global api1
    try:
        api1 = api()
    except Exception as e:
        logger1.critical("Api Error")
        raise e
    global t
    t1 = reload_ids(sleep_interval=5)
    t1.start()
    # time.sleep(1)

    
    # t.kill()

if __name__ == "__main__":
    main()
    