from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType
from database.product_services import get_product_info_by_variant_id


# username = update.message.from_user.username
async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database.connection import client

    orders = client.OnlineStore.Users.find_one(
        {"_id": update.effective_user.id},
        {
            "TotalP": 1,
            "Orders": 1,
        },
    )
    if orders.get("TotalP") == 0:
        await update.message.reply_text(
            text="your orders are empty, order something with the listadd command",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("/listAdd")]]),
        )
        return -1

    text = "You have ordered : \n"
    buttons = []
    for count, order in enumerate(orders.get("Orders"), start=1):
        product_variant_info = get_product_info_by_variant_id(
            str(order.get("ProductID"))
        )

        if product_variant_info:
            product_name = product_variant_info.get("Name")
            var = product_variant_info.get("Variant")
            text_part = f"{count}. {product_name}[{var.get('VName')}]"
            text += f"{text_part} : price = {var.get('SellP')}$ x {order.get('Qnty')} = {var.get('SellP') * order.get('Qnty')}$ \n"

            buttons.append(
                [
                    InlineKeyboardButton(
                        text_part,
                        callback_data=create_callback_data(
                            CallbackType.EDIT_CHOICE,
                            product_id=str(order.get("ProductID")),
                            sell_price=float(var.get("SellP")),
                            quantity=order.get("Qnty"),
                        ),
                    )
                ]
            )
        else:
            text += f"{count}. [Product not found for ID: {order.get('ProductID')}]\n"

    text += f"Total price : {orders.get('TotalP')}"
    await update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    from ...core.bot_handlers import CHOOSING

    return CHOOSING
