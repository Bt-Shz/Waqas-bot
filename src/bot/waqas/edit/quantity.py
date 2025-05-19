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


async def edit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.callback_query.answer()

    # ! [id of the product, price of that product, initial quantity]
    item_id = context.callback_data.get("item_id")
    price = context.callback_data.get("price")
    quantity = context.callback_data.get("quantity")
    context.user_data["wEditChoice"] = [item_id, price, quantity]

    await update.callback_query.message.reply_text(f"Input the quantity")

    from bot.core.bot_handlers import QUANTITY

    return QUANTITY
