# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 18:17:48 2021

@author: Moosa
"""
import os
import tweepy
import logging



logger = logging.getLogger()

def api():
    consumer_key=os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    
    auth = tweepy.OAuthHandler("gZV93qkxK6lvrxBOguoyx5arb","zbVxx1qSLoS8Y517DYTmYFuUUZtBtZbZviOWXRlXlA9Lc1qFVJ")
    auth.set_access_token("929957003929141248-a67kr90z44xBVjJiZTHtTgkEkC8kXbk","OPiPSWPNfWDNyHy7zPVYr6FUkxNO8SUK22n9jfFjfFqQb")
    api = tweepy.API(auth, wait_on_rate_limit=(True),wait_on_rate_limit_notify=(True))
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api