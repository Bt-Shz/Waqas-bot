from database.database_connection import client
from dotenv import load_dotenv
import os
from telegram.ext import Application
from telegram import Bot
from telegram.ext import filters
from bot.core.states import (
    debted,
    restricted,
    verified_users,
)

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

# * all the constants used in the project


def init_constants():
    users = client.OnlineStore.Users.find({}, {"_id": 1})

    for user in users:
        verified_users.add_user_ids(int(user["_id"]))


def main():
    init_constants()
    from bot.core.bot_handlers import handlers

    print("starting the server")
    app = Application.builder().token(TOKEN).build()
    app.bot_data["list_state"] = True
    # ! make this False afterwards
    #! [0] is going to receive all the validation images
    app.add_handlers(handlers)

    app.run_polling(poll_interval=1)


if __name__ == "__main__":
    main()
