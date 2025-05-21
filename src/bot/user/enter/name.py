from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType
from bot.core.states import check_list_state


@check_list_state
async def name_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.core.states import verified_users, admins_list
    from main import bot

    buttons = [
        [
            InlineKeyboardButton(
                "CityU",
                callback_data=create_callback_data(
                    CallbackType.UNIVERSITY, 0  # uni_idx for CityU
                ),
            ),
            InlineKeyboardButton(
                "PolyU",
                callback_data=create_callback_data(
                    CallbackType.UNIVERSITY, 1  # uni_idx for PolyU
                ),
            ),
        ],
        [
            InlineKeyboardButton(
                "HKUST",
                callback_data=create_callback_data(
                    CallbackType.UNIVERSITY, 2  # uni_idx for HKUST
                ),
            ),
            InlineKeyboardButton(
                "HKBU",
                callback_data=create_callback_data(
                    CallbackType.UNIVERSITY, 3  # uni_idx for HKBU
                ),
            ),
        ],
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
