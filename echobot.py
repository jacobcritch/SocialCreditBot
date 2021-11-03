#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging
import json
from time import sleep
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# # #   Enable logging   # # #
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
# # #                # # #


# # #   Members   # # #
token = ""
db = {}

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
    if (not validate_add_remove(update, context)): return
    else:
        creds = abs(int(context.args[1]))
        db[user] += creds
        update.message.reply_text("Gave " + user + " " + str(creds) + " credits. 最尊貴！")
        save_db()
        sleep(2)

def remove(update: Update, context: CallbackContext) -> None:
    user = context.args[0].lower()
    if (not validate_add_remove(update, context)): return
    else:
        creds = abs(int(context.args[1]))
        db[user] -= creds
        update.message.reply_text("Deducted " + str(creds) + " from " + user + ". 可恥！")
        save_db()
        sleep(2)

""" Must have known names for all users for this
def donate(update: Update, context: CallbackContext) -> None:
    donater = update.effective_user
    user = context.args[0].lower()
    creds = context.args[1]
    if (not is_user_valid(user) or not is_credits_valid(creds)): return
    else:
        creds = abs(int(creds))
        db[user] -= creds
        update.message.reply_text("Deducted " + str(creds) + " from " + user + ". 可恥！")
        save_db()
"""
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
def validate_add_remove(update: Update, context: CallbackContext) -> bool:
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



# # #   Database mutations   # # #
def save_db():
    with open("/root/SocialCreditBot/db.json", "w") as f:
        json.dump(db, f)
# # #                # # #



# # #   Config   # # #
def load_token_file() -> str:
    with open("/root/SocialCreditBot/config.json") as f:
        data = json.load(f)
        return data["token"]
    
def load_db_file() -> dict:
    with open("/root/SocialCreditBot/db.json") as f:
        data = json.load(f)
        return data
# # #                # # #


# # #   Setup   # # #
def main() -> None:
    """Start the bot."""
    global token, db
    # Create the Updater and pass it your bot's token.
    token = load_token_file()
    sleep(2)
    db = load_db_file()
    sleep(2)
    updater = Updater(token)

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
