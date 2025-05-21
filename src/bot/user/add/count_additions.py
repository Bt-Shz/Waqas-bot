import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.core.states import check_list_state

# ! Constant ones that are always going to be true:
"""
1. there's always going to be user. Only users can use this
2. The TotalP's (total price's) initial value is always 0 
"""


@check_list_state
async def counting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.core.bot_handlers import SEARCHING

    qnty = update.message.text
    if not qnty.isdigit():
        await update.message.reply_text("This isn't a number. Try again.")
        return

    qnty = int(qnty)
    if qnty <= 0:
        await update.message.reply_text("Only positive integers")
        return
    if qnty > 1000:
        await update.message.reply_text("This quantity is too large. Please reduce it.")
        return

    from json import loads
    from database.user_services import (
        increment_product_quantity_in_order,
        add_product_to_order,
    )

    vID_str, price_per_item = loads(context.user_data["chosen_order"])

    total_price_increment = qnty * price_per_item

    matched_count = increment_product_quantity_in_order(
        user_id=update.effective_user.id,
        product_id_str=vID_str,
        quantity_to_add=qnty,
        total_price_increment=total_price_increment,
    )

    if matched_count == 0:
        # If it updated nothing (item not in order yet), then add it.
        add_success = add_product_to_order(
            user_id=update.effective_user.id,
            product_id_str=vID_str,
            quantity=qnty,
            total_price_increment=total_price_increment,
        )
        if add_success:
            await update.message.reply_text(f"Order's added ✅")
        else:
            # This case should ideally not happen if increment failed due to non-existence
            # and then add somehow also fails. Log error or notify user.
            await update.message.reply_text(
                f"Failed to add the order. Please try again. 🆘"
            )
    else:
        await update.message.reply_text(
            f"The list already contained this item; the quantity has been increased by {qnty} ✅"
        )

    return SEARCHING
