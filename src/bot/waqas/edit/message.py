from telegram import Update, InputMediaPhoto
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
import asyncio
from bson import ObjectId
from dotenv import load_dotenv
import os
from telegram import Bot

from main import bot
from bot.core.states import check_list_state


@check_list_state
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot.send_message(
        chat_id=context.user_data["picked_user"],
        text=f"Waqas sent you a message :\n {update.message.text}",
    )

    await update.message.reply_text("Message sent ✅")
    from bot.waqas.edit.show_users import list_users

    return await list_users(update, context)
