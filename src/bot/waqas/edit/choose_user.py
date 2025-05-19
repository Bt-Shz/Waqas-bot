from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.database_connection import client
from bot.core.callback_utility import create_callback_data, CallbackType


async def choose_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["picked_user"] = int(context.callback_data.get("user_id"))
    await update.callback_query.answer()

    for order in context.user_data["Orders"]:
        if order.get("_id") == context.user_data["picked_user"]:
            chosen_orders = order
            break
    text = f"Their order : \n"
    buttons = []
    for order in chosen_orders.get("Orders"):
        product_info = client.OnlineStore.Products.find_one(
            {"Variants": {"$elemMatch": {"vID": order.get("ProductID")}}},
            {"Name": 1, "Variants.$": 1},
        )
        var = product_info.get("Variants")[0]
        text_part = f"- {product_info.get('Name')}[{var.get('VName')}]"
        text += f"{text_part} : price = {var.get('SellP')}$ x {order.get('Qnty')} = {var.get('SellP') * order.get('Qnty')}$ \n"

        buttons.append(
            [
                InlineKeyboardButton(
                    text=text_part,
                    callback_data=create_callback_data(
                        CallbackType.CHOOSE_ITEM,
                        item_id=str(order.get("ProductID")),
                        price=float(var.get("SellP")),
                        quantity=order.get("Qnty"),
                    ),
                )
            ]
        )
    await update.callback_query.message.reply_text(
        text=text, reply_markup=InlineKeyboardMarkup(buttons)
    )
    from bot.core.bot_handlers import CHOOSE_ITEM

    return CHOOSE_ITEM
