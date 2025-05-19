from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    filters,
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
)
import asyncio
from bson import ObjectId


# update contains amount of id they want to change to
async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    if text.isdigit():
        from bot.core.main import bot
        from database.database_connection import client
        from bson import ObjectId

        text = int(text)  # qnty
        if text < 0:
            await update.message.reply_text("Only positive integers")
        elif text > 50:
            await update.message.reply_text("That's too much :v")
        db = client.OnlineStore.Users
        item_name = db.find_one(
            {"_id": int(context.user_data["picked_user"])}, {"Name": 1}
        )
        if text == 0:
            db.update_one(
                {"_id": context.user_data["picked_user"]},
                {
                    "$pull": {
                        "Orders": {
                            "ProductID": ObjectId(context.user_data["wEditChoice"][0])
                        }
                    },
                    "$inc": {
                        "TotalP": -(
                            context.user_data["wEditChoice"][2]
                            * context.user_data["wEditChoice"][1]
                        )
                    },
                },
            )
            await update.message.reply_text("successfully deleted the item!")
            await bot.send_message(
                chat_id=context.user_data["picked_user"],
                text=f"Waqas deleted the {item_name} from your order.",
            )
        else:

            db.update_one(
                {
                    "_id": context.user_data["picked_user"],  # specific user's
                    "Orders.ProductID": ObjectId(
                        context.user_data["wEditChoice"][0]
                    ),  # product
                },
                {
                    "$set": {
                        "Orders.$.Qnty": text
                    },  # change the quantity to the matching one
                    "$inc": {
                        "TotalP": (text - context.user_data["wEditChoice"][2])
                        * context.user_data["wEditChoice"][1]
                    },  # += (new_quantity - old_quantity)*price
                },
            )
            await update.message.reply_text("successfully changed the quantity!")
            await bot.send_message(
                chat_id=context.user_data["picked_user"],
                text=f"Waqas changed the quantity of the {item_name} from the {context.user_data["wEditChoice"][2]} to the {text}, in your order.",
            )
            # is putting the below 2 outside of the if statements - correct?

        from bot.core.bot_handlers import SEND_MESSAGE

        return SEND_MESSAGE
    else:
        await update.message.reply_text(f"this isn't the number. Input only number. ⛔")
