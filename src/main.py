from database.user_services import get_all_user_ids
from dotenv import load_dotenv
import os
from telegram.ext import Application
from telegram import Bot
from bot.core.states import (
    debted,
    restricted,
    verified_users,
)

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)


def init_constants():
    all_user_ids = get_all_user_ids()
    for user_id_val in all_user_ids:
        verified_users.add_user_ids(user_id_val)


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
