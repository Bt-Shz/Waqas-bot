from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType

# * what do the string numbers mean?
# 1. value for the pattern
# 2. Code, mapping to the certain location :
# 0 -> Ma on Shan; 1 -> Kowloong tong; 2 -> next... (not done yet). i++


async def list_locations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database.database_connection import client

    # gt : 0 -> users who have ordered at least something

    buttons = [
        [
            InlineKeyboardButton(
                text="Ma On Shan",
                callback_data=create_callback_data(
                    CallbackType.SHOW_USER, location_name="Ma On Shan"
                ),
            ),
            InlineKeyboardButton(
                text="Kowloon Tong",
                callback_data=create_callback_data(
                    CallbackType.SHOW_USER, location_name="Kowloon Tong"
                ),
            ),
        ]
    ]
    await update.message.reply_text(
        text="You can go back to this (location choosing) message, by pressing the /editOrders button or writing it out : ",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("/editOrders")]]),
    )
    await update.message.reply_text(
        text="choose the delivery location : ",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    from bot.core.bot_handlers import SHOW_USERS

    return SHOW_USERS
