from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType
from database.product_services import search_products_by_name
from bot.core.states import check_list_state


@check_list_state
async def searching(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
            print(
                create_callback_data(
                    CallbackType.ADD_CHOICE,
                    entry.get("vID"),  # variant_id
                    entry.get("SellP"),  # price_per_item
                )
            )
            # Single variant - show the variant name and price
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{entry.get('VName')} : {entry.get('SellP')}",
                        callback_data=create_callback_data(
                            CallbackType.ADD_CHOICE,
                            entry.get("vID"),  # variant_id
                            entry.get("SellP"),  # price_per_item
                        ),
                    )
                ]
            )
        # choose the product and then its variants
        else:
            # Multiple variants - show just the product name
            print(
                create_callback_data(
                    CallbackType.CHOOSE_VARIANT,
                    product.get("Name"),  # product_name
                    product.get("_id"),  # product_id
                )
            )
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{product.get('Name')}",
                        callback_data=create_callback_data(
                            CallbackType.CHOOSE_VARIANT,
                            product.get("Name"),  # product_name
                            product.get("_id"),  # product_id
                        ),
                    )
                ]
            )

    await update.message.reply_text(
        "Search results:", reply_markup=InlineKeyboardMarkup(buttons)
    )
