from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from bot.core.states import check_list_state


@check_list_state
async def guide_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        text="now, just use the keyboards provided; ++guide",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("/listAdd"), KeyboardButton("/listShow")]]
        ),
    )
