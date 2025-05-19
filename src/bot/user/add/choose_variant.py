from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.core.callback_utility import create_callback_data, CallbackType
from database.product_services import get_product_with_variants


async def choose_variant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.core.bot_handlers import SEARCHING

    await update.callback_query.answer()

    if not context.bot_data.get("list_state"):
        await update.callback_query.message.reply_text(
            "stopped the list creation process. Wait for the next time"
        )
        return -1

    name = context.callback_data.get("product_name")
    pID_str = context.callback_data.get("product_id")

    buttons = []
    variants = get_product_with_variants(pID_str)

    for variant in variants:
        buttons.append(
            [
                InlineKeyboardButton(
                    f"{variant.get('VName')} : {variant.get('SellP')}",
                    callback_data=create_callback_data(
                        CallbackType.CHOOSE_VARIANT,
                        variant_id=variant.get("vID"),
                    ),
                )
            ]
        )
    await update.callback_query.message.reply_text(
        text=f"Choose the variant of the {name}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return SEARCHING
