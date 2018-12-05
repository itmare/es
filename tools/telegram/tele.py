#!/usr/bin/python
# -*- coding: utf-8  -*-

import json
import urllib3
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import es_mod

my_token = '000000000:AAAAEFWEFWEFWEFWEF323F23E3E2323R23R'
print('start telegram chat bot')

def es_command(bot, update) :
    cmd = update.message.text.split(" ")
    rtn = es_mod.es(cmd)

    update.message.reply_text(rtn)

updater = Updater(my_token)

es_handler = CommandHandler('es', es_command)
updater.dispatcher.add_handler(es_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()
