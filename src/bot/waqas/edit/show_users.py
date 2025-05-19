from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database.database_connection import client

    # * The location_name is now fetched from context.callback_data
    # 0 -> Ma On Shan (example, actual value comes from callback)
    # 1 -> kowloong Tong, etc (example, actual value comes from callback)
    location_name = context.callback_data.get("location_name")

    from bot.core.states import uniLocations

    context.user_data["Orders"] = list(
        client.OnlineStore.Users.find(
            {"TotalP": {"$gt": 0}, "Loc": location_name},
            {"PNum": 0},
        )
    )
    if len(context.user_data["Orders"]) == 0:
        await update.callback_query.message.reply_text(
            "No orders yet! Wait until the waqas starts accepting orders"
        )
    else:
        buttons = []
        text = "Orders: \n"
        for user in context.user_data["Orders"]:
            user_id = str(user.get("_id"))
            user_info = user
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{user_info.get('Name')}({user_id})",
                        callback_data=create_callback_data(
                            CallbackType.CHOOSE_USER, user_id=user_id
                        ),
                    )
                ]
            )
            text += f"{user_info.get('Name')} {user_info.get('TotalP')} : \n"
            for order in user_info.get("Orders"):
                product_info = client.OnlineStore.Products.find_one(
                    {"Variants": {"$elemMatch": {"vID": order.get("ProductID")}}},
                    {"Name": 1, "Variants.$": 1},
                )
                text += f"- {product_info.get('Name')}[{product_info.get('Variants')[0].get('VName')}] : price = {product_info.get('Variants')[0].get('SellP')}$ x {order.get('Qnty')} = {product_info.get('Variants')[0].get('SellP') * order.get('Qnty')}$ \n"

        await update.callback_query.message.reply_text(
            text=text, reply_markup=InlineKeyboardMarkup(buttons)
        )
        await update.callback_query.answer()
        from bot.core.bot_handlers import CHOOSE_USER

        return CHOOSE_USER
