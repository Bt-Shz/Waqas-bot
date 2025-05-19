from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.database_connection import client


async def phone_callback(update: Update, context: ContextTypes):
    from bot.core.bot_handlers import NAME

    context.user_data["phone"] = update.message.text  # this is the phone number

    if not update.message.text.isdigit():
        await update.message.reply_text(
            "Please enter a valid phone number without any special characters."
        )
    else:
        from bot.core.states import unregistered_verified

        if int(update.message.text) in unregistered_verified:
            await update.message.reply_text(
                text="congrats, you were in the whtsapp group. Now, write your name, displayed in the package"
            )
            context.user_data["phone"] += "T"
        else:
            await update.message.reply_text(
                "you werent in the whatsapp group; you will have to wait for verification. Proceed with registeration for now. Now, write your name, displayed in the package"
            )
            context.user_data["phone"] += "F"

        return NAME
