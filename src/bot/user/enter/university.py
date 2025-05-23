from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.connection import client

import bot.core.states as states
from bot.core.callback_utility import create_callback_data, CallbackType
from bot.core.states import check_list_state


@check_list_state
async def location_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.core.states import uniLocations
    from bot.core.bot_handlers import LOCATION

    uni_idx = context.callback_data[0]  # university_idx
    uni_names_map = {0: "CityU", 1: "PolyU", 2: "HKUST", 3: "HKBU"}
    chosen_uni_name_for_logic = uni_names_map.get(uni_idx)

    # the ones who don't need to specify the location;
    if chosen_uni_name_for_logic == "HKUST" or chosen_uni_name_for_logic == "HKBU":
        import final_processing

        if context.user_data["phone"][-1] == "F":  # user wasn't in the group
            await final_processing.requestingForUser(
                update,
                context,
                dumping_data=(
                    context.user_data["phone"][:-1],
                    context.user_data["name"],
                    chosen_uni_name_for_logic,
                    update.effective_user.id,
                ),
            )
        else:
            await final_processing.addingUser(
                update,
                context,
                update.effective_user.id,
                context.user_data["name"],
                context.user_data["phone"][:-1],
                chosen_uni_name_for_logic,
            )
    # the ones who need it...
    else:
        buttons = []
        for location in uniLocations[uni_idx]:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=location,
                        callback_data=create_callback_data(
                            CallbackType.LOCATION, location
                        ),
                    )
                ]
            )
        await update.callback_query.message.reply_text(
            text="choose your location", reply_markup=InlineKeyboardMarkup(buttons)
        )
    return LOCATION
