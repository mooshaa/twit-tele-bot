# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 21:21:31 2021

@author: Moosa
"""



import telebot
import logging
import os


log_level = os.getenv("LOG_LEVEL")

telebot.logger.setLevel(log_level)

tw_token = os.getenv("TWITTER_TOKEN")
bot = telebot.AsyncTeleBot(tw_token, parse_mode=None)


def add_to_file(handle):
    
    with open('/twit-tele/handles.txt','a+') as tf:
        tf.seek(0)
        handles=tf.read()
        if handles=='':
            tf.write(str(handle)+',')
            return 1
        else:
            if handle in handles.split(','):
                return 0
            else:
                tf.write(str(handle)+',') 
                return 1

def remove_from_file(handle):
    
    with open('/twit-tele/handles.txt','r') as tf:
        tf.seek(0)
        handles=tf.read()
        if handle in handles:
            handles = handles.replace(handle+',','')
        else:
            return 0
    with open('/twit-tele/handles.txt','w') as tf:
        tf.write(handles)
        return 1
        
    

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing? Newly added twitter accounts will be monitored after 1 minute of adding")
    
@bot.message_handler(commands=['add'])
def add(message):
 	bot.reply_to(message, "Send twitter handle in the format: \nadd @[twitter_handle]")

@bot.message_handler(commands=['remove'])
def remove(message):
 	bot.reply_to(message, "Send twitter handle in the format: \nremove @[twitter_handle]")
     
@bot.message_handler(commands=['list'])
def send_list(message):
    with open('/twit-tele/handles.txt','r') as tf:
        tf.seek(0)
        handles=tf.read()
    if handles:
        bot.reply_to(message,'Here is a list of accounts followed:\n'+ str(handles))
    else:
        bot.reply_to(message,'Empty list' )
        
@bot.message_handler(content_types=["text"])
def check(message):
    m = message.text.strip()
    if m.startswith('add') and '@' in message.text:
        handle = m.replace('add @','')
        if add_to_file(handle):
            bot.reply_to(message,'Handle added to monitor list')
        else:
           bot.reply_to(message,'Handle already in list')
    if m.startswith('remove') and '@' in message.text:
        handle = m.replace('remove @','')
        if remove_from_file(handle):
            bot.reply_to(message,'Handle removed from monitor list')
        else:
           bot.reply_to(message,'Handle not in list')
    
bot.polling(none_stop=False, interval=0, timeout=20)

