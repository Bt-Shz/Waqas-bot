from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.connection import client  # Keep for Users collection access
from database.product_services import get_product_info_by_variant_id
from bot.core.callback_utility import create_callback_data, CallbackType
from bot.core.states import check_list_state


@check_list_state
async def choose_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["picked_user"] = int(context.callback_data[0])  # user_id
    await update.callback_query.answer()

    for order in context.user_data["Orders"]:
        if order.get("_id") == context.user_data["picked_user"]:
            chosen_orders = order
            break
    text = f"Their order : \n"
    buttons = []
    for order in chosen_orders.get("Orders"):
        product_variant_info = get_product_info_by_variant_id(
            str(order.get("ProductID"))
        )

        if product_variant_info:
            product_name = product_variant_info.get("Name")
            var = product_variant_info.get("Variant")
            text_part = f"- {product_name}[{var.get('VName')}]"
            text += f"{text_part} : price = {var.get('SellP')}$ x {order.get('Qnty')} = {var.get('SellP') * order.get('Qnty')}$ \n"

            buttons.append(
                [
                    InlineKeyboardButton(
                        text=text_part,
                        callback_data=create_callback_data(
                            CallbackType.CHOOSE_ITEM,
                            str(order.get("ProductID")),  # item_id
                            float(var.get("SellP")),  # price
                            order.get("Qnty"),  # quantity
                        ),
                    )
                ]
            )
        else:
            # Handle case where product info might not be found
            text += f"- [Product not found for ID: {order.get('ProductID')}]\n"
    await update.callback_query.message.reply_text(
        text=text, reply_markup=InlineKeyboardMarkup(buttons)
    )
    from bot.core.bot_handlers import CHOOSE_ITEM

    return CHOOSE_ITEM
