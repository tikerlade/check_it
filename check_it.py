import os
import time
import requests

import telebot

from rich.live import Live

import urllib3

import utils

urllib3.disable_warnings()

# Load information about how system should work
config = utils.get_config()

# Setup bot if environmental variables exists
BOT_TOKEN = os.getenv("BOT_TOKEN", None)
DESTINATION_CHAT_ID = os.getenv("MY_TELEGRAM_ID", None)
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

# Get stop criteria for url to be "changed"
stop_criteria = utils.get_stop_criteria(config)


# Prepare table with first information
result = {url: False for url in config['urls']}
last_version = {url: requests.get(url, verify=False).text for url in config['urls']}
with Live(utils.get_table(result)) as live:
    while True:
        # Get condition on which we'll stop
        stop_criteria = utils.get_stop_criteria(config)
        new_version = {url: requests.get(url, verify=False).text for url in config['urls']}
        to_delete = set()

        for url in last_version:
            if stop_criteria(last_version[url], new_version[url], config):
                if bot:
                    bot.send_message(DESTINATION_CHAT_ID, f"Results published for {url}!")
                result[url] = True
                to_delete.add(url)

        for url in to_delete:
            del last_version[url]
            del new_version[url]

        live.update(utils.get_table(result))
        time.sleep(60 * config['request_int'])
