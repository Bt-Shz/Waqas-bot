from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType
from database.product_services import search_products_by_name


async def searching(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.bot_data.get("list_state"):
        await update.message.reply_text(
            "Waqas stopped the list creation process. Wait for the next time"
        )
        return -1
    if len(update.message.text) < 4:
        await update.message.reply_text("Too short. Try again.")
        return

    # Use the service function to search for products
    products = search_products_by_name(update.message.text)

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
                        f"{entry.get('VName')} : {entry.get('SellP')}",
                        callback_data=create_callback_data(
                            CallbackType.CHOOSE_VARIANT,
                            variant_id=entry.get("vID"),  # vID is already a string
                        ),
                    )
                ]
            )
        # choose the product and then its variants
        else:
            # Multiple variants - show just the product name
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{product.get('Name')}",
                        callback_data=create_callback_data(
                            CallbackType.ADD_CHOICE,
                            product_id=product.get("_id"),  # _id is already a string
                        ),
                    )
                ]
            )
            # M = more; need to specify the variant now

    await update.message.reply_text(
        "Search results:", reply_markup=InlineKeyboardMarkup(buttons)
    )
