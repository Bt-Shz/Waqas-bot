from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    filters,
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
)

from bot.core.states import check_list_state


@check_list_state
async def edit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.callback_query.answer()

    # ! [item_id, price, quantity]
    item_id = context.callback_data[0]  # item_id
    price = context.callback_data[1]  # price
    quantity = context.callback_data[2]  # quantity
    context.user_data["wEditChoice"] = [item_id, price, quantity]

    await update.callback_query.message.reply_text(f"Input the quantity")

    from bot.core.bot_handlers import QUANTITY

    return QUANTITY
