from bson import ObjectId
from .connection import client

USERS_COLLECTION = client.OnlineStore.Users


def increment_product_quantity_in_order(
    user_id: int,
    product_id_str: str,
    quantity_to_add: int,
    total_price_increment: float,
) -> int:
    """
    Increments the quantity and total price if a product already exists in a user's order.
    Returns the number of documents matched by the update query.
    """
    product_object_id = ObjectId(product_id_str)
    result = USERS_COLLECTION.update_one(
        { 
            "_id": user_id,
            "Orders.ProductID": product_object_id,
        },
        {
            "$inc": {"Orders.$.Qnty": quantity_to_add, "TotalP": total_price_increment},
        },
    )
    return result.matched_count


def add_product_to_order(
    user_id: int, product_id_str: str, quantity: int, total_price_increment: float
) -> bool:
    """
    Adds a new product to a user's order and updates the total price.
    Returns True if the update was successful, False otherwise.
    """
    product_object_id = ObjectId(product_id_str)
    result = USERS_COLLECTION.update_one(
        {"_id": user_id},
        {
            "$push": {
                "Orders": {
                    "ProductID": product_object_id,
                    "Qnty": quantity,
                }
            },
            "$inc": {"TotalP": total_price_increment},
        },
    )
    return result.modified_count > 0


def remove_product_from_order(
    user_id: int,
    product_id_str: str,
    quantity_of_removed_item: int,
    price_per_item: float,
) -> bool:
    """
    Removes a product from a user's order and adjusts the total price.
    Returns True if the update was successful, False otherwise.
    """
    product_object_id = ObjectId(product_id_str)
    total_price_decrement = quantity_of_removed_item * price_per_item
    result = USERS_COLLECTION.update_one(
        {"_id": user_id},
        {
            "$pull": {"Orders": {"ProductID": product_object_id}},
            "$inc": {"TotalP": -total_price_decrement},
        },
    )
    return result.modified_count > 0


def set_product_quantity_in_order(
    user_id: int,
    product_id_str: str,
    new_quantity: int,
    old_quantity: int,
    price_per_item: float,
) -> bool:
    """
    Sets a new quantity for a product in a user's order and adjusts the total price.
    Returns True if the update was successful, False otherwise.
    """
    product_object_id = ObjectId(product_id_str)
    total_price_change = (new_quantity - old_quantity) * price_per_item
    result = USERS_COLLECTION.update_one(
        {
            "_id": user_id,
            "Orders.ProductID": product_object_id,
        },
        {
            "$set": {"Orders.$.Qnty": new_quantity},
            "$inc": {"TotalP": total_price_change},
        },
    )
    return result.modified_count > 0


def get_user_orders_and_total_price(user_id: int) -> dict | None:
    """
    Fetches a user's orders and their total price.
    Orders' ProductID will be converted to string.
    """
    user_data = USERS_COLLECTION.find_one(
        {"_id": user_id},
        {"TotalP": 1, "Orders": 1, "_id": 0},
    )
    if user_data and "Orders" in user_data:
        for order in user_data["Orders"]:
            if "ProductID" in order and isinstance(order["ProductID"], ObjectId):
                order["ProductID"] = str(order["ProductID"])
    return user_data


def create_new_user(user_id: int, name: str, phone_number: str, location: str) -> bool:
    """
    Inserts a new user document.
    Returns True if insertion was successful, False otherwise.
    """
    result = USERS_COLLECTION.insert_one(
        {
            "_id": user_id,
            "Name": name,
            "PNum": phone_number,
            "Loc": location,
            "Orders": [],
            "TotalP": 0,
        }
    )
    return result.inserted_id is not None


def find_users_by_location_with_orders(location_name: str) -> list:
    """
    Finds users in a specific location who have orders (TotalP > 0).
    _id and Orders.ProductID will be converted to string.
    """
    users_cursor = USERS_COLLECTION.find(
        {"TotalP": {"$gt": 0}, "Loc": location_name},
        {"PNum": 0},  # Exclude PNum
    )
    result_users = []
    for user in users_cursor:
        if "_id" in user and isinstance(
            user["_id"], ObjectId
        ):  # Should be int based on schema
            user["_id"] = str(user["_id"])
        elif "_id" in user:  # Assuming _id is int
            user["_id"] = int(user["_id"])

        if "Orders" in user and isinstance(user["Orders"], list):
            for order in user["Orders"]:
                if "ProductID" in order and isinstance(order["ProductID"], ObjectId):
                    order["ProductID"] = str(order["ProductID"])
        result_users.append(user)
    return result_users


def get_user_name(user_id: int) -> str | None:
    """
    Fetches a user's name by their _id.
    """
    user_doc = USERS_COLLECTION.find_one({"_id": user_id}, {"Name": 1, "_id": 0})
    return user_doc.get("Name") if user_doc else None


def get_all_user_ids() -> list[int]:
    """
    Fetches the _id of all users.
    """
    users_cursor = USERS_COLLECTION.find({}, {"_id": 1})
    return [int(user["_id"]) for user in users_cursor]


def get_all_users_with_order_details() -> list:
    """
    Fetches users who have orders (TotalP > 0), including their _id, TotalP, and Orders.
    _id and Orders.ProductID will be converted to string.
    """
    users_cursor = USERS_COLLECTION.find(
        {"TotalP": {"$gt": 0}}, {"_id": 1, "TotalP": 1, "Orders": 1}
    )
    result_users = []
    for user in users_cursor:
        if "_id" in user and isinstance(user["_id"], ObjectId):  # Should be int
            user["_id"] = str(user["_id"])
        elif "_id" in user:  # Assuming _id is int
            user["_id"] = int(user["_id"])

        if "Orders" in user and isinstance(user["Orders"], list):
            for order in user["Orders"]:
                if "ProductID" in order and isinstance(order["ProductID"], ObjectId):
                    order["ProductID"] = str(order["ProductID"])
        result_users.append(user)
    return result_users


def reset_user_orders_and_total_price(user_id: int) -> bool:
    """
    Sets a user's TotalP to 0 and empties their Orders list.
    Returns True if the update was successful, False otherwise.
    """
    result = USERS_COLLECTION.update_one(
        {"_id": user_id}, {"$set": {"TotalP": 0, "Orders": []}}
    )
    return result.modified_count > 0
