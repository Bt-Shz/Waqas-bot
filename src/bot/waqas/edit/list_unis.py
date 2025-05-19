from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType


async def list_unis(update: Update, context: ContextTypes.DEFAULT_TYPE):

    buttons = [
        [
            InlineKeyboardButton(
                "CityU",
                callback_data=create_callback_data(
                    CallbackType.SHOW_LOCATION, uni_name="CityU"
                ),
            ),
            InlineKeyboardButton(
                "PolyU",
                callback_data=create_callback_data(
                    CallbackType.SHOW_LOCATION, uni_name="PolyU"
                ),
            ),
        ],
        [
            InlineKeyboardButton(
                "HKUST",
                callback_data=create_callback_data(
                    CallbackType.SHOW_LOCATION, uni_name="HKUST"
                ),
            ),
            InlineKeyboardButton(
                "HKBU",
                callback_data=create_callback_data(
                    CallbackType.SHOW_LOCATION, uni_name="HKBU"
                ),
            ),
        ],
    ]

    await update.message.reply_text(
        text="choose order's university.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    from bot.core.bot_handlers import SHOW_LOCATIONS

    return SHOW_LOCATIONS
