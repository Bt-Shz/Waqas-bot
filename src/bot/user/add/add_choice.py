from telegram import Update
from telegram.ext import ContextTypes


async def add_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.callback_query.answer()

    if not context.bot_data.get("list_state"):
        await update.callback_query.message.reply_text(
            "stopped the list creation process. Wait for the next time"
        )
        return -1
    from bot.core.bot_handlers import COUNTING
    from json import dumps

    context.user_data["chosen_order"] = dumps(
        [
            context.callback_data[0],  # variant_id
            context.callback_data[1],  # price_per_item
        ]
    )
    await update.callback_query.message.reply_text(f"Input the quantity")
    return COUNTING
