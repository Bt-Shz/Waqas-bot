from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime


from database.database_connection import client


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

        from bson import ObjectId

        context.bot_data["list_state"] = False
        ids = client.OnlineStore.Users.find(
            {"TotalP": {"$gt": 0}}, {"_id": 1, "TotalP": 1, "Orders": 1}
        )
        for id in ids:
            text = "Ordering period is over. Delivery is incoming. You have ordered : "

            for count, order in enumerate(id.get("Orders"), start=1):

                product_info = client.OnlineStore.Products.find_one(
                    {"Variants": {"$elemMatch": {"vID": order.get("ProductID")}}},
                    {"Name": 1, "Variants.$": 1},
                )
                text_part = f"{count}. {product_info.get("Name")}[{product_info.get("Variants")[0].get("VName")}]"
                text += f"{text_part} : price = {product_info.get("Variants")[0].get("SellP")}$ x {order.get("Qnty")} = {product_info.get("Variants")[0].get("SellP") * order.get("Qnty")}$ \n"

            text += f"Your total is {id['TotalP']}HK$. After receiving your items, please pay to THERES SOME INFORMATION PALET, and send the proof (screenshot)"
            from telegram import ReplyKeyboardRemove

            await context.bot.send_message(
                chat_id=id["_id"], text=text, reply_markup=ReplyKeyboardRemove()
            )
            import main as main

            main.debted.add_user_ids(int(id["_id"]))

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
