from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,

)
from telegram.ext import ContextTypes



async def list_unis(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # gt : 0 -> users who have ordered at least something

    buttons = [
        [  # [[states]]
            InlineKeyboardButton("CityU", callback_data="90"),
            InlineKeyboardButton("PolyU", callback_data="91"),
            InlineKeyboardButton("HKUST", callback_data="92"),
            InlineKeyboardButton("HKBU", callback_data="93"),
        ]
    ]

    await update.message.reply_text(
        text="choose order's university.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    from bot.bot_handlers import SHOW_LOCATIONS

    return SHOW_LOCATIONS
