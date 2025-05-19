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
from bot.core.callback_utility import CallbackType, callback_handler_factory
from bot.waqas.edit import (
    update,
    quantity,
    message,
    choose_user,
    show_users,
    list_unis,
    choose_location,
)
from bot.core.states import (
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
                callback_handler_factory(
                    CallbackType.EDIT_CHOICE, edit_choise.edit_choice
                ),
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
                callback_handler_factory(CallbackType.ADD_CHOICE, add_choice.choosing),
                callback_handler_factory(
                    CallbackType.CHOOSE_VARIANT, choose_variant.choose_variant
                ),
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
                callback_handler_factory(
                    CallbackType.SHOW_LOCATION, choose_location.choose_location
                )
            ],
            SHOW_USERS: [
                callback_handler_factory(CallbackType.SHOW_USER, show_users.list_users)
            ],
            CHOOSE_USER: [
                callback_handler_factory(
                    CallbackType.CHOOSE_USER, choose_user.choose_user
                )
            ],
            CHOOSE_ITEM: [
                callback_handler_factory(CallbackType.CHOOSE_ITEM, quantity.edit_choice)
            ],
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
    callback_handler_factory(CallbackType.RECEIPT_VERIFICATION, receipt_verification),
    callback_handler_factory(CallbackType.VALIDATION, validation.entering_validation),
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
            UNI: [
                callback_handler_factory(
                    CallbackType.UNIVERSITY, university.location_callback
                )
            ],
            LOCATION: [
                callback_handler_factory(
                    CallbackType.LOCATION, location.location_callback
                )
            ],
        },
        fallbacks=[],
    ),
    CommandHandler("buttons", admin.buttons),
]
