from telegram.ext import filters
import functools
from telegram import Update

admins_list = (1048872421, 1)  # first one will receive verifications

debted = filters.User(set())
restricted = filters.User(set())

verified_users = filters.User(set())
unregistered_verified = (85291275420, ...)

# notes :
# add data and time input in the /begin
# before day of delivery and after the  the day of delivery, give reminder (import date)
# reminder : auto + button
# FIXME : callbackquery data ()
# add each university choosingi n the /enter
# FIXME : /buttons

# * array for mapping
uniLocations = [
    ["Ma On Shan", "Kowloon Tong"],  # cityu
    ["Hung Hom", "Homantin"],  # polyu
    "HKUST",  # hkust
    "HKBU",  # hkbu
    # TODO : add others (bit more sophisticated ones)
    # Education U + villages ( location + connect it with CU Mos)
    # Sai Kung ( add additional question of giving full address or village name)
]


def check_list_state(handler_func):
    @functools.wraps(handler_func)
    async def wrapper(update: Update, context, *args, **kwargs):
        if not context.bot_data.get("list_state"):
            reply_target = None
            if update.callback_query:
                reply_target = update.callback_query.message
            elif update.message:
                reply_target = update.message

            if reply_target:
                await reply_target.reply_text(
                    "Stopped the list creation process. Wait for the next time."
                )
            return -1
        return await handler_func(update, context, *args, **kwargs)

    return wrapper
