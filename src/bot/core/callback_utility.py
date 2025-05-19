from enum import Enum
import json
from telegram.ext import CallbackQueryHandler


class CallbackType(Enum):
    EDIT_CHOICE = "EDIT"
    ADD_CHOICE = "ADD"
    CHOOSE_VARIANT = "VARIANT"
    SHOW_LOCATION = "LOC"
    SHOW_USER = "USER"
    CHOOSE_USER = "CUSER"
    CHOOSE_ITEM = "ITEM"
    RECEIPT_VERIFICATION = "RECEIPT"
    VALIDATION = "VALID"
    UNIVERSITY = "UNI"
    LOCATION = "LOCATE"


def callback_handler_factory(callback_type, handler_func):
    """Create a CallbackQueryHandler for a specific callback type"""

    def check_type(callback_data):
        try:
            data = json.loads(callback_data)
            return data.get("type") == callback_type.value
        except:
            return False

    def wrapped_handler(update, context):
        data = json.loads(update.callback_query.data)
        # Store parsed data in context for easy access in handler
        context.callback_data = {k: v for k, v in data.items() if k != "type"}
        return handler_func(update, context)

    return CallbackQueryHandler(wrapped_handler, pattern=check_type)


def create_callback_data(callback_type, **kwargs):
    """Create standardized callback data with type and parameters"""
    data = {"type": callback_type.value, **kwargs}
    return json.dumps(data)


def parse_callback_data(callback_data):
    """Parse callback data into a dictionary"""
    try:
        return json.loads(callback_data)
    except:
        return {"raw": callback_data}
