from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.connection import client

import bot.core.states as states
from bot.core.states import check_list_state

from . import final_processing


# 6
@check_list_state
async def location_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # callbackquery data is their chosen location
    location_name = context.callback_data[0]  # location_name
    if context.user_data["phone"][-1] == "F":  # user wasn't in the group

        await final_processing.requestingForUser(
            update,
            context,
            dumping_data=(
                context.user_data["phone"][:-1],
                context.user_data["name"],
                location_name,
                update.effective_user.id,
            ),
        )
        await update.callback_query.message.reply_text(text="Request sent to admins.")

    else:  # user was in the group :)
        await final_processing.addingUser(
            update,
            context,
            update.effective_user.id,
            context.user_data["name"],
            context.user_data["phone"][:-1],
            location_name,
        )
        await update.callback_query.message.reply_text(
            text="You have been added to the group. Welcome!"
        )

    return -1
