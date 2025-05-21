from enum import Enum
import json
from telegram.ext import CallbackQueryHandler


class CallbackType(Enum):
    EDIT_CHOICE = "1"
    ADD_CHOICE = "2"
    CHOOSE_VARIANT = "3"
    SHOW_LOCATION = "4"
    SHOW_USER = "5"
    CHOOSE_USER = "6"
    CHOOSE_ITEM = "7"
    RECEIPT_VERIFICATION = "8"
    VALIDATION = "9"
    UNIVERSITY = "0"
    LOCATION = "a"


def callback_handler_factory(callback_type, handler_func):
    """Create a CallbackQueryHandler for a specific callback type"""

    def check_type(callback_data_str):
        # Check if the first character of the callback_data string matches the type
        return callback_data_str[0] == callback_type.value

    def wrapped_handler(update, context):
        # First char is type, rest is JSON payload of a list of values
        callback_string = update.callback_query.data

        # Store parsed list of values in context
        context.callback_data = json.loads(callback_string[1:])
        return handler_func(update, context)

    return CallbackQueryHandler(wrapped_handler, pattern=check_type)


def create_callback_data(callback_type, *args):
    """Create standardized callback data with type prefix and JSON array payload of values"""
    # Prepend the type character to the JSON string of the values list
    return callback_type.value + json.dumps(list(args))


def parse_callback_data(callback_data):
    """Parse callback data into a dictionary"""
    try:
        return json.loads(callback_data)
    except:
        return {"raw": callback_data}
