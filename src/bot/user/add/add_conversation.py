from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def list_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.bot_handlers import SEARCHING

    if context.bot_data.get("list_state"):

        await update.message.reply_text(
            "the list is starting to be added!! Input the name of the product you want to add",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("/listShow")]]),
        )
        return SEARCHING
    else:
        await update.message.reply_text("Waqas hasn't started list addition yet")
        return -1
