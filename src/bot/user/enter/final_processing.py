from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.database_connection import client

import states


# user was already in the group
async def addingUser(
    update: Update, context: ContextTypes.DEFAULT_TYPE, id, name, phone, location
):
    states.verified_users.add_user_ids(id)

    client.OnlineStore.Users.insert_one(
        {
            "_id": id,
            "Name": name,
            "PNum": phone,
            "Loc": location,
            "Orders": [],
            "TotalP": 0,
        }
    )

    from bot.user.enter.guide import guide_callback

    await guide_callback(update, context)


# else:
async def requestingForUser(
    update: Update, context: ContextTypes.DEFAULT_TYPE, dumping_data
):
    from json import dumps

    buttons = [
        [
            InlineKeyboardButton(
                "Validate", callback_data=f" 5{dumps(dumping_data)}Y "
            ),
            InlineKeyboardButton(
                "Cancel",
                callback_data=f" 5{update.effective_user.id}N ",  # to match the above one and have same conditions
            ),
        ],
    ]
    await context.bot.send_message(
        chat_id=states.admins_list[0],
        text=f"new user request : \n - phone number : {dumping_data[0]}\n - Name : {dumping_data[1]}. Do you want to add him? ",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
