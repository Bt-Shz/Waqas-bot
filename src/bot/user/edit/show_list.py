from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import ContextTypes


# username = update.message.from_user.username
async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database.database_connection import client

    orders = client.OnlineStore.Users.find_one(
        {"_id": update.effective_user.id},
        {
            "TotalP": 1,
            "Orders": 1,
        },
    )

    if orders.get("TotalP") == 0:
        await update.message.reply_text(
            "your orders are empty, order something with the /listadd command!!",
            ReplyKeyboardMarkup([[KeyboardButton("/listAdd")]]),
        )
        return -1

    text = "You have ordered : \n"
    buttons = []
    for count, order in enumerate(orders.get("Orders"), start=1):
        var = product_info.get("Variants")[0]
        product_info = client.OnlineStore.Products.find_one(
            {"Variants": {"$elemMatch": {"vID": order.get("ProductID")}}},
            {"Name": 1, "Variants.$": 1},
        )
        text_part = f"{count}. {product_info.get("Name")}[{var.get("VName")}]"
        text += f"{text_part} : price = {var.get("SellP")}$ x {order.get("Qnty")} = {var.get("SellP") * order.get("Qnty")}$ \n"

        from json import dumps

        buttons.append(
            [
                InlineKeyboardButton(
                    text_part,
                    callback_data=dumps(
                        [
                            0,
                            str(order.get("ProductID")),
                            float(var.get("SellP")),
                            order.get("Qnty"),
                        ]
                    ),
                )
            ]
        )
    text += f"Total price : {orders.get("TotalP")}"
    await update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    from ...bot_handlers import CHOOSING

    return CHOOSING
