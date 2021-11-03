#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# # #   Enable logging   # # #
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
# # #                # # #


# # #   Members   # # #
db = {"mk": 100, "jewke": 100, "dave": 100, "oob": 100, "coon": 100}
leaderUsernames = {"Dear_LeaderMK", "Jewkorius"}
# # #                # # #



# # #   Commands   # # #
def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Commands:\n/give name numberOfCredits\n/deduct name numberOfCredits\n/leaderboard\n/help')

def list_all(update: Update, context: CallbackContext) -> None:
    result = ""
    for key, value in db.items():
        result += key + ": " + str(value) + " credits\n"
        
    update.message.reply_text(result)

def add(update: Update, context: CallbackContext) -> None:
    user = context.args[0].lower()
    if (not validate(update, context)): return
    else:
        creds = abs(int(context.args[1]))
        db[user] += creds
        update.message.reply_text("Gave " + user + " " + str(creds) + " credits. 最尊貴！")

def remove(update: Update, context: CallbackContext) -> None:
    user = context.args[0].lower()
    if (not validate(update, context)): return
    else:
        creds = abs(int(context.args[1]))
        db[user] -= creds
        update.message.reply_text("Deducted " + str(creds) + " from " + user + ". 可恥！")
# # #                # # #


# # #   Replies   # # #
def reply_invalid_number(update: Update):
    update.message.reply_text("Must enter a number (unsigned integer) value of credits. 最尊貴！")

def reply_invalid_user(update: Update):
    names = "["
    for key, value in db.items():
        names += "'" + key + "' "
    names += "]"
    update.message.reply_text("User invalid! Valid users are: " + names + ". 可恥！")

def reply_only_leader_can_update(update: Update):
    update.message.reply_text("Only MK can update the social credit system! 可恥！")
# # #                # # #


# # #   Validation   # # #
def validate(update: Update, context: CallbackContext) -> bool:
    user = context.args[0].lower()
    creds = context.args[1]

    if (not is_user_valid(user)):
        reply_invalid_user(update)
        return False

    elif (not is_credits_valid(creds)):
        reply_invalid_number(update)
        return False

    elif (not is_user_leader(update.effective_user.username)):
        reply_only_leader_can_update(update)
        return False

    else: 
        return True

def is_user_valid(name: str) -> bool:
    if name.lower() not in db:
        return False
    else:
        return True

def is_credits_valid(creds: str) -> bool:
    try:
        abs(int(creds))
    except:
        return False
    else:
        return True
        
def is_user_leader(name: str) -> bool:
    return name in leaderUsernames
# # #                # # #


# # #   Setup   # # #
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2061370543:AAF_UaBN4Ye5wES45wsmtFPKsUm625jnTlI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("give", add))
    dispatcher.add_handler(CommandHandler("deduct", remove))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("leaderboard", list_all))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
# # #                # # #

if __name__ == '__main__':
    main()
