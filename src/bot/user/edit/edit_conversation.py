from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from bot.core.states import check_list_state


@check_list_state
async def list_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.user.edit.show_list import show_list

    await update.message.reply_text(
        text="Used for showing/deleting/changing the quantity of the items.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("/listAdd"), KeyboardButton("/listShow")]]
        ),
    )
    return await show_list(update, context)
