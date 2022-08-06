import argparse
import os
import time
import requests

import telebot

from rich.live import Live
from rich.table import Table
from rich.markdown import Markdown

import urllib3
urllib3.disable_warnings()


my_parser = argparse.ArgumentParser()

my_parser.add_argument('urls',
                       nargs='+',
                       help='URL you need to track.')

my_parser.add_argument('--request_int',
                       type=int,
                       default=1,
                       required=False,
                       help='How often we need to request data (minutes).')

my_parser.add_argument('--symbols_diff',
                       type=int,
                       default=10,
                       required=False,
                       help='How many symbols must change on page that we can say it changed.')

args = my_parser.parse_args()

BOT_TOKEN = os.getenv("BOT_TOKEN", None)
DESTINATION_CHAT_ID = os.getenv("MY_TELEGRAM_ID", None)


def get_table(result):
    table = Table()

    table.add_column("ID")
    table.add_column("Link")
    table.add_column("Updated")

    for idx, url in enumerate(result):
        table.add_row(
            f"{idx}", Markdown(f"[{url}]({url})"), "[green]:heavy_check_mark:" if result[url] else "[red]:cross_mark:",
            end_section=True
        )

    return table


bot = None
if BOT_TOKEN:
    bot = telebot.TeleBot(BOT_TOKEN)

result = {url: False for url in args.urls}
last_version = {url: requests.get(url, verify=False).text for url in args.urls}

with Live(get_table(result)) as live:
    while True:
        new_version = {url: requests.get(url, verify=False).text for url in args.urls}
        to_delete = set()

        for url in last_version:
            diff = sum(ch1 != ch2 for ch1, ch2 in zip(last_version[url], new_version[url]))
            if diff > args.symbols_diff:
                if bot:
                    bot.send_message(DESTINATION_CHAT_ID, f"Results published for {url}!")
                result[url] = True
                to_delete.add(url)

        for url in to_delete:
            del last_version[url]
            del new_version[url]

        live.update(get_table(result))
        time.sleep(60 * args.request_int)
