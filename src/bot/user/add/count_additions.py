import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bson import ObjectId

# ! Constant ones that are always going to be true:
"""
1. there's always going to be user. Only users can use this
2. The TotalP's (total price's) initial value is always 0 
"""


async def counting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.bot_handlers import SEARCHING

    if not context.bot_data.get("list_state"):
        await update.message.reply_text(
            "Waqas stopped the list creation process. Wait for the next time ⛔"
        )
        return -1

    qnty = update.message.text
    if not qnty.isdigit():
        await update.message.reply_text("This isn't a number. Try again.")
        return

    from database.database_connection import client

    qnty = int(qnty)
    if qnty <= 0:
        await update.message.reply_text("Only positive integers")
        return
    if qnty > 1000:
        await update.message.reply_text(
            "Stop playing with me. You can't handle this much lol."
        )
        return

    from json import loads

    vID, price = loads(context.user_data["chosen_order"])
    db = client.OnlineStore.Users
    result = db.update_one(  # if it finds, it updates
        {
            "_id": update.effective_user.id,
            "Orders.ProductID": ObjectId(vID),
        },
        {
            "$inc": {"Orders.$.Qnty": qnty, "TotalP": (qnty * price)},
        },
    )

    if (
        result.matched_count == 0
    ):  # if it updated nothing - the firt time ordering this; no input of this yet -, then it will add it.
        db.update_one(
            {"_id": update.effective_user.id},
            {
                "$push": {
                    "Orders": {
                        "ProductID": ObjectId(vID),
                        "Qnty": qnty,
                    }
                },
                "$inc": {"TotalP": (qnty * price)},
            },
        )

        await update.message.reply_text(f"Order's added ✅")
    else:
        await update.message.reply_text(
            f"The list already contained this item; the quantity has been increased by {qnty} ✅"
        )

    return SEARCHING
