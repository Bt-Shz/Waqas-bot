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
    from json import loads

    context.user_data["wEditChoice"] = loads(update.callback_query.data)[
        1:
    ]  # remove the first, pattern element

    await update.callback_query.message.reply_text(f"Input the quantity")

    from bot.bot_handlers import QUANTITY

    return QUANTITY
