from .connection import client
from bson import ObjectId


def get_product_info_by_variant_id(variant_id_str: str):
    """
    Fetches product information (name and specific variant) based on the variant ID.
    Args:
        variant_id_str: The string representation of the variant's ObjectId.
    Returns:
        A dictionary containing the product 'Name' and the matched 'Variant' object (dictionary),
        with the variant's 'vID' converted to a string. Returns None if not found.
    """
    variant_oid = ObjectId(variant_id_str)

    product_info = client.OnlineStore.Products.find_one(
        {"Variants": {"$elemMatch": {"vID": variant_oid}}},
        {"Name": 1, "Variants.$": 1},  # Project Name and the matched variant
    )
    if product_info and product_info.get("Variants"):
        # Variants.$ returns an array with one element, the matched variant
        variant = product_info.get("Variants")[0]
        if "vID" in variant and isinstance(variant["vID"], ObjectId):
            variant["vID"] = str(variant["vID"])
        return {
            "Name": product_info.get("Name"),
            "Variant": variant,  # Return the variant dictionary
        }
    return None


def get_product_with_variants(product_id_str: str):
    """
    Fetches variants for a given product ID.
    Args:
        product_id_str: The string representation of the product's ObjectId.
    Returns:
        A list of variant dictionaries, with 'vID' converted to string.
        Returns an empty list if the product or variants are not found.
    """
    product_oid = ObjectId(product_id_str)
    product_data = client.OnlineStore.Products.find_one(
        {"_id": product_oid}, {"Variants": 1, "_id": 0}  # Only fetch the Variants array
    )

    if product_data and "Variants" in product_data:
        variants = product_data["Variants"]
        for variant in variants:
            if "vID" in variant and isinstance(variant["vID"], ObjectId):
                variant["vID"] = str(variant["vID"])
        return variants
    return []


def search_products_by_name(name_query: str):
    """
    Searches for products by name (case-insensitive regex).
    Args:
        name_query: The search term for the product name.
    Returns:
        A list of product dictionaries, with '_id' and 'vID' (in variants)
        converted to strings. Returns an empty list if no products are found.
    """
    products_cursor = client.OnlineStore.Products.find(
        {"Name": {"$regex": name_query, "$options": "i"}}
    )

    result_products = []
    for product in products_cursor:
        if "_id" in product and isinstance(product["_id"], ObjectId):
            product["_id"] = str(product["_id"])

        if "Variants" in product and isinstance(product["Variants"], list):
            for variant_item in product[
                "Variants"
            ]:  # Renamed to avoid conflict with outer 'variant' if any
                if "vID" in variant_item and isinstance(variant_item["vID"], ObjectId):
                    variant_item["vID"] = str(variant_item["vID"])
        result_products.append(product)

    return result_products
