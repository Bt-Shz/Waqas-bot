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
    if context.bot_data.get("list_state"):

        text = update.message.text
        if text.isdigit():
            from database.database_connection import client
            from bson import ObjectId

            text = int(text)  # qnty
            if text < 0:
                await update.message.reply_text("Only positive integers")
            elif text > 100:
                await update.message.reply_text("That's too much :v")
            db = client.OnlineStore.Users
            if text == 0:
                db.update_one(
                    {"_id": update.effective_user.id},
                    {
                        "$pull": {
                            "Orders": {
                                "ProductID": ObjectId(
                                    context.user_data["EditChoice"][0]
                                )
                            }
                        },
                        "$inc": {
                            "TotalP": -(
                                context.user_data["EditChoice"][2]
                                * context.user_data["EditChoice"][1]
                            )
                        },
                    },
                )
                await update.message.reply_text("successfully deleted the item!")
            else:

                db.update_one(
                    {
                        "_id": update.effective_user.id,
                        "Orders.ProductID": ObjectId(
                            context.user_data["EditChoice"][0]
                        ),
                    },
                    {
                        "$set": {
                            "Orders.$.Qnty": text
                        },  # change the quantity to the matching one
                        "$inc": {
                            "TotalP": (text - context.user_data["EditChoice"][2])
                            * context.user_data["EditChoice"][1]
                        },  # += (new_quantity - old_quantity)*price
                    },
                )
                await update.message.reply_text("successfully changed the quantity!")
                # is putting the below 2 outside of the if statements - correct?
            from bot.user.edit import show_list

            return await show_list.show_list(update, context)

        else:
            await update.message.reply_text(
                f"this isn't the number. Input only number. ⛔"
            )
    else:
        await update.message.reply_text(
            "Waqas stopped the list creation process. Wait for the next time ⛔"
        )
        return -1
