from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def choose_variant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.bot_handlers import SEARCHING

    await update.callback_query.answer()

    if not context.bot_data.get("list_state"):
        await update.callback_query.message.reply_text(
            "stopped the list creation process. Wait for the next time"
        )
        return -1

    from json import loads, dumps
    from bson import ObjectId
    from database.database_connection import client

    name, pID = loads(update.callback_query.data[1:])
    pID = ObjectId(pID)
    buttons = []
    for variant in client.OnlineStore.Products.find_one({"_id": pID}, {"Variants": 1})[
        "Variants"
    ]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"variant : {variant['VName']} \n price : {variant['SellP']}HK$",
                    callback_data=f"D{dumps([str(variant['vID']),float(variant['SellP'])])}",
                    # ! don't forget about the filter in the beggining!
                )
            ]
        )
    await update.callback_query.message.reply_text(
        text=f"Choose the variant of the {name}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return SEARCHING
