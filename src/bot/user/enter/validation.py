from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import bot.core.states as states
from database.user_services import create_new_user
from json import loads, dumps
from bot.core.states import check_list_state


@check_list_state
async def entering_validation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # entering
    await update.callback_query.answer()

    user_id_to_notify_str = context.callback_data[0]  # user_id_to_notify
    action = context.callback_data[1]  # action

    if action == "reject":
        if user_id_to_notify_str:
            await context.bot.send_message(
                chat_id=int(user_id_to_notify_str),
                text="Waqas declined your registration. Please ensure your data is correct or contact an admin.",
            )
            await context.bot.send_message(
                chat_id=states.admins_list[0],
                text=f"User {user_id_to_notify_str} registration has been declined.",
            )
        else:
            await context.bot.send_message(
                chat_id=states.admins_list[0],
                text=f"A user registration has been declined (ID not available in callback).",
            )
    elif action == "approve":
        # user_details_list is context.callback_data[2]
        if len(context.callback_data) > 2:
            user_details_list = context.callback_data[2]  # user_details_json
            if user_details_list and len(user_details_list) == 4:
                phone, name, loc, user_id_to_add_str = user_details_list
                user_id_to_add = int(user_id_to_add_str)

                if create_new_user(
                    user_id=user_id_to_add,
                    name=name,
                    phone_number=phone,
                    location=loc,
                ):
                    await context.bot.send_message(
                        chat_id=user_id_to_add,
                        text="You got registered!",
                    )
                    states.verified_users.add_user_ids(user_id_to_add)
                    await context.bot.send_message(
                        chat_id=states.admins_list[0],
                        text=f"User {name} ({user_id_to_add}) has been approved and registered.",
                    )
                else:
                    await context.bot.send_message(
                        chat_id=states.admins_list[0],
                        text=f"Failed to register user {name} ({user_id_to_add}) in the database.",
                    )
            else:
                await context.bot.send_message(
                    chat_id=states.admins_list[0],
                    text=f"Approval callback received but user details are missing or malformed.",
                )
