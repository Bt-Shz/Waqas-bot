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
    from bot.core.bot_handlers import EDITING

    await update.callback_query.answer()

    if context.bot_data.get("list_state"):
        # ! [id of the product, price of that product, initial quantity]
        item_id = context.callback_data.get("item_id")
        price = context.callback_data.get("price")
        quantity = context.callback_data.get("quantity")
        context.user_data["EditChoice"] = [item_id, price, quantity]

        await update.callback_query.message.reply_text(f"Input the quantity")
        return EDITING
    else:
        await update.callback_query.message.reply_text(
            "stopped the list creation process. Wait for the next time"
        )
        return -1
