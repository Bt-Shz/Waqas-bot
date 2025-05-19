from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import bot.core.states as states
from database.connection import client
from json import loads


async def entering_validation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # entering
    await update.callback_query.answer()
    action = context.callback_data.get("action")

    if action == "N":
        user_id_to_notify = context.callback_data.get("user_id_to_notify")
        await context.bot.send_message(
            chat_id=int(user_id_to_notify),
            text="Waqas declined your regestration. Write normal data or som!",
        )

        await context.bot.send_message(
            chat_id=states.admins_list[0],
            text=f"User {user_id_to_notify} regestration has been declined",
        )
    else:
        user_details_json = context.callback_data.get("user_details_json")
        data = loads(user_details_json)
        client.OnlineStore.Users.insert_one(
            {
                "_id": int(data[3]),
                "Name": data[1],
                "PNum": data[0],
                "Loc": data[2],
                "Orders": [],
                "TotalP": 0,
            }
        )
        await context.bot.send_message(
            chat_id=int(data[3]),
            text="You got regged!",
        )
        states.verified_users.add_user_ids(int(data[3]))
