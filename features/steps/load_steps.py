"""
Load steps for BDD tests
"""

import requests
from behave import given
from service.common import status

@given('the following products')
def load_products(context):
    """Load products from the BDD background table"""
    headers = {"Content-Type": "application/json"}

    # Delete all products (ignore status code)
    context.resp = requests.get(f"{context.base_url}/products")
    if context.resp.status_code == status.HTTP_200_OK:
        for product in context.resp.json():
            requests.delete(f"{context.base_url}/products/{product['id']}")

    # Load new products
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"].lower() == "true",
            "category": row["category"]
        }
        context.resp = requests.post(
            f"{context.base_url}/products",
            json=payload,
            headers=headers
        )
        assert context.resp.status_code == status.HTTP_201_CREATED
