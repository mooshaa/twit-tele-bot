#!/bin/bash

mv /bots/* /twit-tele/ && \
exec python3 /twit-tele/twitter.py > /twit-tele/twit-log.txt 2>&1 & \
exec python3 /twit-tele/telegram.py > /twit-tele/tele-log.txt 2>&1







