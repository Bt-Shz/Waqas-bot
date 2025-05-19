from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.database_connection import client


async def choose_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["picked_user"] = int(update.callback_query.data[1:])
    await update.callback_query.answer()

    for order in context.user_data["Orders"]:
        if order.get("_id") == context.user_data["picked_user"]:
            chosen_orders = order
            break
    text = f"Their order : \n"
    buttons = []
    for order in chosen_orders.get("Orders"):
        var = product_info.get("Variants")[0]
        product_info = client.OnlineStore.Products.find_one(
            {"Variants": {"$elemMatch": {"vID": order.get("ProductID")}}},
            {"Name": 1, "Variants.$": 1},
        )
        text_part = f"- {product_info.get("Name")}[{var.get("VName")}]"
        text += f"{text_part} : price = {var.get("SellP")}$ x {order.get("Qnty")} = {var.get("SellP") * order.get("Qnty")}$ \n"
        from json import dumps

        buttons.append(
            [
                InlineKeyboardButton(
                    text_part,
                    callback_data=dumps(
                        [
                            3,
                            str(order.get("ProductID")),
                            float(var.get("SellP")),
                            order.get("Qnty"),
                        ]
                    ),
                )
            ]
        )
    await update.callback_query.message.reply_text(
        text=text, reply_markup=InlineKeyboardMarkup(buttons)
    )
    from bot.core.bot_handlers import CHOOSE_ITEM

    return CHOOSE_ITEM
