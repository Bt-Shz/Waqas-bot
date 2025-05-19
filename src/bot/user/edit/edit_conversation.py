from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes


async def list_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.user.edit.show_list import show_list

    if context.bot_data.get("list_state"):
        await update.message.reply_text(
            text="Used for showing/deleting/changing the quantity of the items.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("/listAdd"), KeyboardButton("/listShow")]]
            ),
        )
        return await show_list(update, context)

    else:
        from bot.core.states import debted

        await update.message.reply_text("Waqas hasn't started list edition yet")
        return -1
