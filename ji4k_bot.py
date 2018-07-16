#!/usr/bin/env python

import json
import requests
import os
import time
import urllib
from dbhelper import DBHelper
import datetime

db = DBHelper()

# 618752765:AAE-z-cWQI-hVSZb7h22pQxCpDbCdJawPEw
TOKEN = os.getenv("TOKEN")
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def handle_updates(updates, makan_places, kakis):
    for update in updates["result"]:
        print(update)
        if("message" in update):
            text = update["message"]["text"]
            print("text={}".format(text))
            chat_id = update["message"]["chat"]["id"]
            print("chat_id={}".format(chat_id))
            first_name = update["message"]["from"]["first_name"]
            date = datetime.datetime.utcfromtimestamp(update["message"]["date"])
            session_date = date.strftime("%d-%m-%y")
            print("date={}".format(date))
            ##from_id = update["message"]["from"]["id"]
            ##print("from_id={}".format(from_id))
            jiak_sessions = db.get_jiak_sessions(session_date)  ##
            print("jiak_sessions={}".format(jiak_sessions))
            if text == "/start":
                print("makan_places={}".format(makan_places))
                if makan_places:
                    keyboard = build_keyboard(makan_places)
                    send_message("Hello! Time to Jiak, lai choose venue: ", chat_id, keyboard)
            if text == "/done":
                kakis.clear()
                if jiak_sessions:
                    keyboard = build_keyboard(jiak_sessions)
                    send_message("Select an item to delete", chat_id, keyboard)
                else:
                    send_message("To Do list is empty!  Send any text to me and I'll store it as an item.", chat_id)

            elif text.startswith("/"):
                continue
            elif text in makan_places:
                '''if first_name in kakis:
                    message = "{} already voted!".format(first_name)
                    send_message(message, chat_id)
                
                else:'''
                kakis.append(first_name)
                db.add_vote(text, chat_id, session_date)  ##
                message = "{} votes {} \n".format(first_name, text)
                send_message(message, chat_id)
        else:
            print("message not in update")

    print("kakis = {}".format(kakis))


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def main():
    db.setup()
    makan_places = db.get_makan_places()
    last_update_id = None
    kakis = []

    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates, makan_places, kakis)


if __name__ == '__main__':
    main()
