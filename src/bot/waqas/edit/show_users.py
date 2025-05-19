from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database.database_connection import client

    # * int(update.callback_query.data[1]) : location, where :
    # 0 -> Ma On Shan
    # 1 -> kowloong Tong, etc

    from bot.core.states import uniLocations

    context.user_data["Orders"] = list(
        client.OnlineStore.Users.find(
            {"TotalP": {"$gt": 0}, "Loc": update.callback_query.data[1:]},
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
            buttons.append(
                [
                    InlineKeyboardButton(
                        user.get("Name"),
                        callback_data=f"2{str(user.get("_id"))}",
                    )
                ]
            )
            text += f"{user.get("Name")} {user.get("TotalP")} : \n"
            for order in user.get("Orders"):
                product_info = client.OnlineStore.Products.find_one(
                    {"Variants": {"$elemMatch": {"vID": order.get("ProductID")}}},
                    {"Name": 1, "Variants.$": 1},
                )
                text += f"- {product_info.get("Name")}[{product_info.get("Variants")[0].get("VName")}] : price = {product_info.get("Variants")[0].get("SellP")}$ x {order.get("Qnty")} = {product_info.get("Variants")[0].get("SellP") * order.get("Qnty")}$ \n"

        await update.callback_query.message.reply_text(
            text=text, reply_markup=InlineKeyboardMarkup(buttons)
        )
        await update.callback_query.answer()
        from bot.core.bot_handlers import CHOOSE_USER

        return CHOOSE_USER
