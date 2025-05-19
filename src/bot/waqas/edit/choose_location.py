from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import ContextTypes


async def choose_location(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # gt : 0 -> users who have ordered at least something
    from bot.core.states import uniLocations

    buttons = []
    for location in uniLocations[int(update.callback_query.data[1])]:
        buttons.append(
            [
                InlineKeyboardButton(location, callback_data=f"7{str(location)}"),
            ]
        )
    await update.callback_query.message.reply_text(
        text="choose choose delivery location.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    from bot.core.bot_handlers import SHOW_USERS

    return SHOW_USERS
