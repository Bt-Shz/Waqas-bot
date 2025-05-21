from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType
from database.product_services import get_product_info_by_variant_id
from database.user_services import find_users_by_location_with_orders
from bot.core.states import check_list_state


@check_list_state
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # * The location_name is now fetched from context.callback_data
    # context.callback_data[0] will be location_name
    location_name = context.callback_data[0]  # location_name

    users_with_orders = find_users_by_location_with_orders(location_name)
    context.user_data["Orders"] = users_with_orders

    if not users_with_orders:
        await update.callback_query.message.reply_text(
            f"No orders yet for {location_name}! Wait until users start placing orders."
        )
        await update.callback_query.answer()
        return
    else:
        buttons = []
        text = f"Orders for {location_name}: \n"
        for user_info in users_with_orders:
            user_id = str(user_info.get("_id"))

            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user_info.get('Name')}({user_id})",
                        callback_data=create_callback_data(
                            CallbackType.CHOOSE_USER, user_id  # user_id
                        ),
                    )
                ]
            )
            text += f"\nUser: {user_info.get('Name')} (ID: {user_id}) - Total: {user_info.get('TotalP')}HK$\n"
            for order in user_info.get("Orders", []):
                product_variant_info = get_product_info_by_variant_id(
                    order.get("ProductID")
                )
                if product_variant_info:
                    product_name = product_variant_info.get("Name")
                    variant_info = product_variant_info.get("Variant")
                    text += f"  - {product_name}[{variant_info.get('VName')}] : price = {variant_info.get('SellP')}$ x {order.get('Qnty')} = {variant_info.get('SellP') * order.get('Qnty')}$ \n"
                else:
                    text += (
                        f"  - [Product not found for ID: {order.get('ProductID')}]\n"
                    )

        await update.callback_query.message.reply_text(
            text=text, reply_markup=InlineKeyboardMarkup(buttons)
        )
        await update.callback_query.answer()
        from bot.core.bot_handlers import CHOOSE_USER

        return CHOOSE_USER
