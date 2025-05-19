import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from database.database_connection import client


async def enter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from bot.core.bot_handlers import PHONE_NUMBER
  

    await update.message.reply_text(
        text="Enter your phone number. If you were in the whatsapp group, you will be automatically added, without needing verification. Otherwise, you will have to wait for aproval"
    )
    return PHONE_NUMBER


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["state"]
    await update.message.reply_text("help text...")
