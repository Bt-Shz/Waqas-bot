from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import bot.core.states as states
from database.connection import client
from bot.core.callback_utility import create_callback_data, CallbackType


async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # print([u.message.photo for u in update if u.message.photo])
    print(update.message.photo)
    if update.message.photo or update.message.document:

        await update.message.reply_text(
            "Image received! Wait for the validation. You are not able to use any of the bot functions, until the verification is complete"
        )
        states.restricted.add_user_ids(update.effective_user.id)
        buttons = [
            [
                InlineKeyboardButton(
                    "Approve",
                    callback_data=create_callback_data(
                        CallbackType.RECEIPT_VERIFICATION,
                        user_id=update.effective_user.id,
                        action="approve",
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "Reject",
                    callback_data=create_callback_data(
                        CallbackType.RECEIPT_VERIFICATION,
                        user_id=update.effective_user.id,
                        action="reject",
                    ),
                )
            ],
        ]
        from main import bot
        from bot.core.states import admins_list

        if update.message.photo:
            # Get the file ID of the highest resolution photo
            await bot.send_photo(
                chat_id=admins_list[0],
                photo=update.message.photo[-1].file_id,
                caption="Validation image:",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            await bot.send_document(
                chat_id=admins_list[0],
                document=update.message.document.file_id,
                caption="Validation image:",
                reply_markup=InlineKeyboardMarkup(buttons),
            )

    else:
        await update.message.reply_text("Please send an image of the receipt instead.")


async def receipt_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    user_id = int(context.callback_data.get("user_id"))
    action = context.callback_data.get("action")

    if user_id not in states.debted.user_ids:
        await update.callback_query.message.reply_text(
            "This user was already validated or not marked as debted."
        )
    else:
        # either send another/they're chillin
        states.restricted.remove_user_ids(user_id=user_id)
        if action == "approve":
            await context.bot.send_message(
                chat_id=user_id, text="Your receipt has been validated!"
            )
            # after this, user is allowed to input messages as usual
            states.debted.remove_user_ids(user_id=user_id)
            # clean db

            client.OnlineStore.Users.update_one(
                {"_id": user_id}, {"$set": {"TotalP": 0, "Orders": []}}
            )
            await update.callback_query.message.reply_text(
                "You validated their receipt."
            )

        else:  # Assuming 'reject' is the other action
            await context.bot.send_message(
                chat_id=user_id,
                text="Your receipt has been canceled! Send the money and the proof!",
            )
            await update.callback_query.message.reply_text(
                "You canceled their receipt."
            )


# data = "85291275420;Shera;58731942Y"[0:-1]
# phone_number, name, userID = data.split(";")
# print(phone_number) 85291275420
# print(name) Shera
# print(userID) 58731942
