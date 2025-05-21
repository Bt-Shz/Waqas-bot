from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.user_services import create_new_user

import bot.core.states as states
from bot.core.callback_utility import create_callback_data, CallbackType


# user was already in the group
async def addingUser(
    update: Update, context: ContextTypes.DEFAULT_TYPE, id, name, phone, location
):
    states.verified_users.add_user_ids(id)

    create_new_user(user_id=id, name=name, phone_number=phone, location=location)

    from bot.user.enter.guide import guide_callback

    await guide_callback(update, context)


# else:
async def requestingForUser(
    update: Update, context: ContextTypes.DEFAULT_TYPE, dumping_data
):
    user_id = update.effective_user.id

    user_details_for_validation = [
        dumping_data[0],  # phone
        dumping_data[1],  # name
        dumping_data[2],  # location
        str(dumping_data[3]),  # user_id_to_be_added (ensure it's string for JSON)
    ]

    buttons = [
        [
            InlineKeyboardButton(
                "Approve",
                callback_data=create_callback_data(
                    CallbackType.VALIDATION,
                    str(user_id),  # user_id_to_notify
                    "approve",  # action
                    user_details_for_validation,  # user_details_json
                ),
            )
        ],
        [
            InlineKeyboardButton(
                "Reject",
                callback_data=create_callback_data(
                    CallbackType.VALIDATION,
                    str(user_id),  # user_id_to_notify
                    "reject",  # action
                ),
            )
        ],
    ]
    await context.bot.send_message(
        chat_id=states.admins_list[0],
        text=f"New user request for User ID {dumping_data[3]}: \n - Phone number : {dumping_data[0]}\n - Name : {dumping_data[1]}\n - Location: {dumping_data[2]}. Do you want to add them? ",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
