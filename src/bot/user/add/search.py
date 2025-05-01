from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def searching(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.bot_data.get("list_state"):
        await update.message.reply_text(
            "Waqas stopped the list creation process. Wait for the next time"
        )
        return -1
    if len(update.message.text) < 4:
        await update.message.reply_text("Too short. Try again.")
        return
    from database.database_connection import client
    from json import dumps

    products = list(
        client.OnlineStore.Products.find(
            {"Name": {"$regex": update.message.text, "$options": "i"}}
        )
    )  # Case-insensitive search

    if not products:
        await update.message.reply_text("No products found. Try different keywords.")
        return

    buttons = []
    for product in products:
        # no variants; choose the product right away
        if len(product["Variants"]) == 1:
            entry = product["Variants"][0]
            # Single variant - show the variant name and price
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"name : {product.get('Name')}[{entry.get("VName")}] \n price : {entry.get("SellP")}HK$ \n category : {product.get("Category")}",
                        callback_data=f"D{dumps([str(entry["vID"]), float(entry["SellP"])])}",
                        # D = done; chose the product
                    )
                ]
            )
        # choose the product and then its variants
        else:
            # Multiple variants - show just the product name
            # Convert ObjectIds in variants to str for JSON serialization

            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"name : {product.get('Name')}.\nChoose a variant",
                        callback_data=f"M{dumps([product.get("Name"), str(product['_id'])])}",
                        # M = more; need to specify the variant now
                    )
                ]
            )
            # M = more; need to specify the variant now

    await update.message.reply_text(
        "Search results:", reply_markup=InlineKeyboardMarkup(buttons)
    )
