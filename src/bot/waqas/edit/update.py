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
import asyncio
from bson import ObjectId
from database.user_services import (
    remove_product_from_order,
    set_product_quantity_in_order,
    get_user_name,
)
from bot.core.states import check_list_state


# update contains amount of id they want to change to
@check_list_state
async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    if text.isdigit():
        from main import bot

        text = int(text)  # qnty
        if text < 0:
            await update.message.reply_text("Only positive integers")
        elif text > 50:
            await update.message.reply_text("That's too much :v")

        picked_user_id = int(context.user_data["picked_user"])
        product_id_str = context.user_data["wEditChoice"][0]
        price_per_item = context.user_data["wEditChoice"][1]
        old_quantity = context.user_data["wEditChoice"][2]

        user_name_for_notification = get_user_name(picked_user_id)

        if text == 0:
            if remove_product_from_order(
                user_id=picked_user_id,
                product_id_str=product_id_str,
                quantity_of_removed_item=old_quantity,
                price_per_item=price_per_item,
            ):
                await update.message.reply_text("successfully deleted the item!")
                await bot.send_message(
                    chat_id=picked_user_id,
                    text=f"Waqas deleted an item from your order.",
                )
            else:
                await update.message.reply_text("Failed to delete the item.")
        else:
            if set_product_quantity_in_order(
                user_id=picked_user_id,
                product_id_str=product_id_str,
                new_quantity=text,
                old_quantity=old_quantity,
                price_per_item=price_per_item,
            ):
                await update.message.reply_text("successfully changed the quantity!")
                await bot.send_message(
                    chat_id=picked_user_id,
                    text=f"Waqas changed the quantity of an item from {old_quantity} to {text} in your order.",
                )
            else:
                await update.message.reply_text("Failed to change the quantity.")

        from bot.core.bot_handlers import SEND_MESSAGE

        return SEND_MESSAGE
    else:
        await update.message.reply_text(f"this isn't the number. Input only number. ⛔")
