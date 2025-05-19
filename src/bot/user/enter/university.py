from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.database_connection import client

import bot.core.states as states


# 6
async def location_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.core.states import uniLocations
    from bot.core.bot_handlers import LOCATION

    # the ones who don't need to specify the location;
    if (
        uniLocations[int(update.callback_query.data[1])] == "HKUST"
        or uniLocations[int(update.callback_query.data[1])] == "HKBU"
    ):
        import final_processing

        if context.user_data["phone"][-1] == "F":  # user wasn't in the group
            await final_processing.requestingForUser(
                update,
                context,
                dumping_data=(
                    5,
                    context.user_data["phone"][:-1],
                    context.user_data["name"],
                    update.callback_query.data[1:],
                    update.effective_user.id,
                    #! i need to rewrite the whole logic for the location inclusion...
                ),
            )
        else:
            await final_processing.addingUser(
                update,
                context,
                update.effective_user.id,
                context.user_data["name"],
                context.user_data["phone"][:-1],
                uniLocations[int(update.callback_query.data[1])],
            )
    # the ones who need it...
    else:
        buttons = []
        for location in uniLocations[int(update.callback_query.data[1])]:
            buttons.append(
                [InlineKeyboardButton(text=location, callback_data=f"7{location}")]
            )
        await update.callback_query.message.reply_text(
            text="choose your location", reply_markup=InlineKeyboardMarkup(buttons)
        )
    return LOCATION
