from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime


from database.connection import client  # Keep for Users collection access
from database.product_services import get_product_info_by_variant_id


async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot_data["order_date"] = datetime.now().date()
    if context.bot_data["list_state"] == True:
        await update.message.reply_text("You have already started the list.")
    else:
        context.bot_data["list_state"] = True
        keyboards = [[KeyboardButton("/listAdd"), KeyboardButton("/listShow")]]

        for id in client.OnlineStore.Users.find({}, {"_id": 1}):
            await context.bot.send_message(
                chat_id=id["_id"],
                text="You can now create your own list!",
                reply_markup=ReplyKeyboardMarkup(keyboard=keyboards),
            )

        await update.message.reply_text(
            f"Users can now create their own lists! ✅",
        )


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot_data["list_state"] == False:
        await update.message.reply_text("You have already ended the list.")
    else:

        from bson import (
            ObjectId,
        )  # Keep if other ObjectId uses exist, otherwise can be removed if only for productID

        context.bot_data["list_state"] = False
        ids = client.OnlineStore.Users.find(
            {"TotalP": {"$gt": 0}}, {"_id": 1, "TotalP": 1, "Orders": 1}
        )
        for id_data in ids:  # Renamed id to id_data to avoid conflict with built-in id
            text = "Ordering period is over. Delivery is incoming. You have ordered : "

            for count, order in enumerate(id_data.get("Orders"), start=1):
                product_variant_info = get_product_info_by_variant_id(
                    str(order.get("ProductID"))
                )

                if product_variant_info:
                    product_name = product_variant_info.get("Name")
                    variant_info = product_variant_info.get("Variant")
                    text_part = f"{count}. {product_name}[{variant_info.get('VName')}]"
                    text += f"{text_part} : price = {variant_info.get('SellP')}$ x {order.get('Qnty')} = {variant_info.get('SellP') * order.get('Qnty')}$ \n"
                else:
                    text += f"{count}. [Product not found for ID: {order.get('ProductID')}]\n"

            text += f"Your total is {id_data['TotalP']}HK$. After receiving your items, please pay to THERES SOME INFORMATION PALET, and send the proof (screenshot)"
            from telegram import ReplyKeyboardRemove

            await context.bot.send_message(
                chat_id=id_data["_id"], text=text, reply_markup=ReplyKeyboardRemove()
            )
            import main as main

            main.debted.add_user_ids(int(id_data["_id"]))

            # ! make it so that only admins saw this.
            # ! make the admins array or something like that.
        await update.message.reply_text(
            "Users can no longer now create their own lists! ⛔"
        )


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
