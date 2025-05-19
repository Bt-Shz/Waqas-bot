from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from bot.user.add import add_choice, add_conversation, search, choose_variant
from bot.user.add import count_additions
from bot.user.edit import count_changes, edit_conversation, edit_choise
from bot.waqas.manage import admin
from bot.user import guide_info
from bot.waqas.edit import (
    update,
    quantity,
    message,
    choose_user,
    show_users,
    list_unis,
    choose_location,
)
from states import (
    admins_list,
    debted,
    restricted,
    verified_users,
)
from bot.waqas.manage.debt_process import (
    image_handler,
    receipt_verification,
)


from bot.user.enter import phone, name, validation, location, university


SEARCHING, COUNTING = range(2)  # for the list add

CHOOSING, EDITING = range(2)  # for the list edit

PHONE_NUMBER, NAME, UNI, LOCATION = range(4)  # for entering

SHOW_LOCATIONS, SHOW_USERS, CHOOSE_USER, CHOOSE_ITEM, QUANTITY, SEND_MESSAGE = range(
    6
)  # waqas edit

# first number = type of request, starting from 0
handlers = [
    ConversationHandler(
        allow_reentry=True,
        entry_points=[
            CommandHandler(
                "listShow",
                edit_conversation.list_edit,
                filters=~debted & verified_users,
            )
        ],
        states={
            CHOOSING: [
                CallbackQueryHandler(edit_choise.edit_choice, pattern="^.{1}0"),
            ],
            EDITING: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    count_changes.edit,
                )
            ],
        },
        fallbacks=[],
    ),
     
    ConversationHandler(
        entry_points=[
            CommandHandler(
                "listAdd",
                add_conversation.list_add,
                filters=~debted & verified_users,
            )
        ],
        states={
            SEARCHING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search.searching),
                CallbackQueryHandler(add_choice.choosing, pattern="^.{0}D"),
                CallbackQueryHandler(choose_variant.choose_variant, pattern="^.{0}M"),
            ],
            COUNTING: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    count_additions.counting,
                )
            ],
        },
        fallbacks=[],
        allow_reentry=True,
    ),
    # CHOOSE_USER, CHOOSE_ITEM, QUANTITY, SEND_MESSAGE = range(4)
    # at the end there should be return of the list_orders
    ConversationHandler(
        entry_points=[
            CommandHandler(
                "editOrders",
                list_unis.list_unis,
                filters=filters.User(admins_list),
            )
        ],
        states={
            SHOW_LOCATIONS: [
                CallbackQueryHandler(choose_location.choose_location, pattern="^.{0}9")
            ],
            SHOW_USERS: [CallbackQueryHandler(show_users.list_users, pattern="^.{0}7")],
            CHOOSE_USER: [
                CallbackQueryHandler(choose_user.choose_user, pattern="^.{0}2")
            ],
            CHOOSE_ITEM: [CallbackQueryHandler(quantity.edit_choice, pattern="^.{1}3")],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, update.edit)],
            SEND_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, message.message)
            ],
        },
        fallbacks=[],
        allow_reentry=True,
    ),
    # debted guys access this;
    MessageHandler(debted & ~restricted & verified_users, image_handler),  # bill
    # for admins
    CommandHandler("begin", admin.begin, filters=filters.User(admins_list)),
    CommandHandler("end", admin.end, filters=filters.User(admins_list)),
    CallbackQueryHandler(receipt_verification, pattern="^.{0}4"),
    CallbackQueryHandler(validation.entering_validation, pattern="^.{1}5"),
    # introductory
    ConversationHandler(
        entry_points=[
            CommandHandler("enter", guide_info.enter, filters=~verified_users)
        ],
        states={
            PHONE_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, phone.phone_callback)
            ],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name.name_callback)],
            UNI: [CallbackQueryHandler(university.location_callback, pattern="^.{0}6")],
            LOCATION: [
                CallbackQueryHandler(location.location_callback, pattern="^.{0}7")
            ],
        },
        fallbacks=[],
    ),
    CommandHandler("buttons", admin.buttons),
]
