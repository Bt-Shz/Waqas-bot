from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType


async def choose_location(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # gt : 0 -> users who have ordered at least something
    from bot.core.states import uniLocations

    uni_idx = context.callback_data.get("uni_idx")  # Assuming uni_idx is passed
    buttons = []
    print(f"uni_idx: {uni_idx}")
    # uniLocations[uni_idx] should be a list of specific locations for that university/area
    for location in uniLocations[uni_idx]:
        buttons.append(
            [
                InlineKeyboardButton(
                    location,
                    callback_data=create_callback_data(
                        CallbackType.SHOW_USER, location_name=str(location)
                    ),
                )
            ]
        )
    await update.callback_query.message.reply_text(
        text="choose choose delivery location.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    from bot.core.bot_handlers import SHOW_USERS

    return SHOW_USERS
