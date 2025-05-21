from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime

from database.user_services import get_all_user_ids, get_all_users_with_order_details
from database.product_services import get_product_info_by_variant_id
from bot.core.states import check_list_state


@check_list_state
async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot_data["order_date"] = datetime.now().date()
    if context.bot_data.get("list_state") == True:  # Use get for safety
        await update.message.reply_text("You have already started the list.")
    else:
        context.bot_data["list_state"] = True
        keyboards = [[KeyboardButton("/listAdd"), KeyboardButton("/listShow")]]

        all_user_ids = get_all_user_ids()
        for user_id_val in all_user_ids:
            try:
                await context.bot.send_message(
                    chat_id=user_id_val,
                    text="You can now create your own list!",
                    reply_markup=ReplyKeyboardMarkup(keyboard=keyboards),
                )
            except Exception as e:
                print(f"Failed to send message to user {user_id_val}: {e}")

        await update.message.reply_text(
            f"Users can now create their own lists! ✅",
        )


@check_list_state
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot_data.get("list_state") == False:  # Use get for safety
        await update.message.reply_text("You have already ended the list.")
    else:
        context.bot_data["list_state"] = False
        users_with_orders = get_all_users_with_order_details()

        for user_data in users_with_orders:
            text = (
                "Ordering period is over. Delivery is incoming. You have ordered : \n"
            )

            for count, order in enumerate(user_data.get("Orders", []), start=1):
                product_variant_info = get_product_info_by_variant_id(
                    order.get("ProductID")
                )

                if product_variant_info:
                    product_name = product_variant_info.get("Name")
                    variant_info = product_variant_info.get("Variant")
                    text_part = f"{count}. {product_name}[{variant_info.get('VName')}]"
                    text += f"{text_part} : price = {variant_info.get('SellP')}$ x {order.get('Qnty')} = {variant_info.get('SellP') * order.get('Qnty')}$ \n"
                else:
                    text += f"{count}. [Product not found for ID: {order.get('ProductID')}]\n"

            text += f"Your total is {user_data['TotalP']}HK$. After receiving your items, please pay to THERES SOME INFORMATION PALET, and send the proof (screenshot)"
            from telegram import ReplyKeyboardRemove

            user_id_val = user_data["_id"]
            try:
                await context.bot.send_message(
                    chat_id=user_id_val, text=text, reply_markup=ReplyKeyboardRemove()
                )
                from bot.core.states import debted

                debted.add_user_ids(user_id_val)
            except Exception as e:
                print(
                    f"Failed to send end message or update debted status for user {user_id_val}: {e}"
                )

        await update.message.reply_text(
            "Users can no longer now create their own lists! ⛔"
        )


@check_list_state
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="Your buttons : ",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("/begin"), KeyboardButton("/end")],
                [KeyboardButton("/editOrders")],
            ]
        ),
    )
