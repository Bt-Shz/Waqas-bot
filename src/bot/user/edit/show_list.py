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
from database.user_services import get_user_orders_and_total_price
from bot.core.states import check_list_state


# username = update.message.from_user.username
@check_list_state
async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders_data = get_user_orders_and_total_price(update.effective_user.id)

    if not orders_data or orders_data.get("TotalP") == 0:
        await update.message.reply_text(
            text="your orders are empty, order something with the listadd command",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("/listAdd")]]),
        )
        return -1

    text = "You have ordered : \n"
    buttons = []
    for count, order in enumerate(orders_data.get("Orders", []), start=1):
        product_variant_info = get_product_info_by_variant_id(order.get("ProductID"))

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
                            order.get("ProductID"),  # product_id
                            float(var.get("SellP")),  # sell_price
                            order.get("Qnty"),  # quantity
                        ),
                    )
                ]
            )
        else:
            text += f"{count}. [Product not found for ID: {order.get('ProductID')}]\n"

    text += f"Total price : {orders_data.get('TotalP')}"
    await update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    from ...core.bot_handlers import CHOOSING

    return CHOOSING
