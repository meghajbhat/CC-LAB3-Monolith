import json
from typing import List, Optional
import products
from cart import dao
from products import Product


class Cart:
    def init(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=data['contents'],  # Ensure the contents is properly loaded
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """
    Retrieves the cart details for the given username.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    try:
        items = [
            item_id
            for cart_detail in cart_details
            for item_id in json.loads(cart_detail['contents'])  # Replace eval with json.loads
        ]

        # Fetch products for all item IDs in a single loop
        return [products.get_product(item_id) for item_id in items]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error while processing cart data: {e}")
        return []


def add_to_cart(username: str, product_id: int) -> None:
    """
    Adds a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """
    Removes a product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """
    Deletes the user's cart.
    """
    dao.delete_cart(username)