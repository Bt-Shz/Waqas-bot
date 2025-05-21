from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.core.states import check_list_state


@check_list_state
async def list_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.core.bot_handlers import SEARCHING

    await update.message.reply_text(
        "the list is starting to be added!! Input the name of the product you want to add",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("/listShow")]]),
    )
    return SEARCHING
