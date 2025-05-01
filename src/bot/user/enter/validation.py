from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import states
from database.database_connection import client


async def entering_validation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # entering
    await update.callback_query.answer()

    if update.callback_query.data[-2] == "N":

        await context.bot.send_message(
            chat_id=int(update.callback_query.data[2:-2]),
            text="Waqas declined your regestration. Write normal data or som!",
        )

        await context.bot.send_message(
            chat_id=states.admins_list[0],
            text=f"User {update.callback_query.data[2:-2]} regestration has been declined",
        )
    else:  # they're chill, actually
        from json import loads

        data = loads(update.callback_query.data[2:-2])
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
        import states

        states.verified_users.add_user_ids(int(data[4]))
