from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType
from database.product_services import get_product_with_variants
from bot.core.states import check_list_state


@check_list_state
async def choose_variant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.core.bot_handlers import SEARCHING

    await update.callback_query.answer()

    product_name = context.callback_data[0]  # product_name
    pID_str = context.callback_data[1]  # product_id

    buttons = []
    variants = get_product_with_variants(pID_str)

    for variant in variants:
        buttons.append(
            [
                InlineKeyboardButton(
                    f"{variant.get('VName')} : {variant.get('SellP')}",
                    callback_data=create_callback_data(
                        CallbackType.ADD_CHOICE,
                        variant.get("vID"),  # variant_id
                        variant.get("SellP"),  # price_per_item
                    ),
                )
            ]
        )
    await update.callback_query.message.reply_text(
        text=f"Choose the variant of the {product_name}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
