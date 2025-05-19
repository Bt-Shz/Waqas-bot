from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def name_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from states import verified_users, admins_list
    from bot.core.main import bot

    buttons = [
        [  # [[states]]
            InlineKeyboardButton("CityU", callback_data="60"),
            InlineKeyboardButton("PolyU", callback_data="61"),
            InlineKeyboardButton("HKUST", callback_data="62"),
            InlineKeyboardButton("HKBU", callback_data="63"),
        ]
    ]
    if context.user_data["phone"][-1] == "T":
        # user was already in the whatsapp group
        context.user_data["name"] = update.message.text
        await update.message.reply_text(
            text="received your data; thank you, you will be able to use everything as normal, after specifying your university : ",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        context.user_data["name"] = update.message.text
        await update.message.reply_text(
            text="you were not in the whatsapp group. Sorry, you would have to wait. Next, input your university ",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    from bot.core.bot_handlers import UNI

    return UNI
