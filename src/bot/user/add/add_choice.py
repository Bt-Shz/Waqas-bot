from telegram import Update
from telegram.ext import ContextTypes



async def choosing(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.callback_query.answer()

    if not context.bot_data.get("list_state"):
        await update.callback_query.message.reply_text(
            "stopped the list creation process. Wait for the next time"
        )
        return -1
    from bot.bot_handlers import COUNTING

    context.user_data["chosen_order"] = update.callback_query.data[1:]
    # why? Cause the first char = pattern for CQH
    await update.callback_query.message.reply_text(f"Input the quantity")
    return COUNTING
