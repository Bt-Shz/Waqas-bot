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
)
from bot.core.states import check_list_state


# update contains amount of id they want to change to
@check_list_state
async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.isdigit():
        text = int(text)  # qnty
        if text < 0:
            await update.message.reply_text("Only positive integers")
        elif text > 100:
            await update.message.reply_text("That's too much :v")
        product_id_str = context.user_data["EditChoice"][0]
        price_per_item = context.user_data["EditChoice"][1]
        old_quantity = context.user_data["EditChoice"][2]

        if text == 0:
            if remove_product_from_order(
                user_id=update.effective_user.id,
                product_id_str=product_id_str,
                quantity_of_removed_item=old_quantity,
                price_per_item=price_per_item,
            ):
                await update.message.reply_text("successfully deleted the item!")
            else:
                await update.message.reply_text("Failed to delete the item.")

        else:
            if set_product_quantity_in_order(
                user_id=update.effective_user.id,
                product_id_str=product_id_str,
                new_quantity=text,
                old_quantity=old_quantity,
                price_per_item=price_per_item,
            ):
                await update.message.reply_text("successfully changed the quantity!")
            else:
                await update.message.reply_text("Failed to change the quantity.")
            # is putting the below 2 outside of the if statements - correct?
        from bot.user.edit import show_list

        return await show_list.show_list(update, context)

    else:
        await update.message.reply_text(f"this isn't the number. Input only number. ⛔")
