from telegram import Update
from telegram.ext import ContextTypes

from bot.core.states import check_list_state


@check_list_state
async def add_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.callback_query.answer()

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
