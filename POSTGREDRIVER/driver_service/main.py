#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
vendor aggregator proof of concept. restucturized and fixed project.
"""
#logging errors to console output
import logging
# Enable logging
logging.basicConfig(
    # filename='my_runtime_log.log', # saving log to filename
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO # DEBUG 
)
logging.info('logger started')
logger = logging.getLogger(__name__)

#python-telegram-bot imports
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler)

import os

# import other files for bot

import handlers
from dialoghandlers import *
import token
from token_extractor import token


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", handlers.start))
    dispatcher.add_handler(CommandHandler("help", handlers.help_command))
    dispatcher.add_handler(CommandHandler("dump", handlers.dump))
    dispatcher.add_handler(CommandHandler("update", handlers.update_vendors_db))
    dispatcher.add_handler(CommandHandler("struc_search", handlers.struc_search))

    # dispatcher.add_handler(CommandHandler("sim_search", sim_search))
    dispatcher.add_handler(similarity_search, 1)

    # dispatcher.add_handler(CommandHandler("test", handlers.gDriveTest))
    
    # dialog handlers
    dispatcher.add_handler(purge_dialog, 1) # this numeration is IMPORTANT! https://github.com/python-telegram-bot/python-telegram-bot/issues/1447

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()