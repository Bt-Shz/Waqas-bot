from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType
from bot.core.states import check_list_state


@check_list_state
async def list_unis(update: Update, context: ContextTypes.DEFAULT_TYPE):

    buttons = [
        [
            InlineKeyboardButton(
                "CityU",
                callback_data=create_callback_data(
                    CallbackType.SHOW_LOCATION, 0  # uni_idx for CityU
                ),
            ),
            InlineKeyboardButton(
                "PolyU",
                callback_data=create_callback_data(
                    CallbackType.SHOW_LOCATION, 1  # uni_idx for PolyU
                ),
            ),
        ],
        [
            InlineKeyboardButton(
                "HKUST",
                callback_data=create_callback_data(
                    CallbackType.SHOW_LOCATION, 2  # uni_idx for HKUST
                ),
            ),
            InlineKeyboardButton(
                "HKBU",
                callback_data=create_callback_data(
                    CallbackType.SHOW_LOCATION, 3  # uni_idx for HKBU
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
