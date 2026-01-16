######################################################################
# Copyright 2016, 2023 John J. Rofrano
######################################################################
"""
Product API Service Test Suite
"""
from urllib.parse import quote_plus
import os
import logging
from decimal import Decimal
from unittest import TestCase
from service import app
from service.common import status
from service.models import db, init_db, Product
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/products"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductRoutes(TestCase):
    """Product Service tests"""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        db.session.close()

    def setUp(self):
        self.client = app.test_client()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    ############################################################
    # Utility function
    ############################################################
    def _create_products(self, count=1):
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ############################################################
    # READ
    ############################################################
    def test_get_product(self):
        """It should Read a single Product"""
        test_product = self._create_products()[0]

        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)
        self.assertEqual(data["description"], test_product.description)
        self.assertEqual(Decimal(data["price"]), test_product.price)
        self.assertEqual(data["available"], test_product.available)
        self.assertEqual(data["category"], test_product.category.name)

    def test_get_product_not_found(self):
        """It should not Read a Product that does not exist"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############################################################
    # UPDATE
    ############################################################
    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = self._create_products()[0]

        updated_data = test_product.serialize()
        updated_data["description"] = "Updated description"

        response = self.client.put(
            f"{BASE_URL}/{test_product.id}",
            json=updated_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["description"], "Updated description")

    ############################################################
    # DELETE
    ############################################################
    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products()[0]

        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############################################################
    # LIST
    ############################################################
    def test_list_all_products(self):
        """It should List all Products"""
        self._create_products(3)

        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(len(data), 3)

    def test_list_products_by_name(self):
        """It should List Products by name"""
        products = self._create_products(5)
        name = products[0].name

        response = self.client.get(f"{BASE_URL}?name={quote_plus(name)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        for product in data:
            self.assertEqual(product["name"], name)

    def test_list_products_by_category(self):
        """It should List Products by category"""
        products = self._create_products(5)
        category = products[0].category.name

        response = self.client.get(f"{BASE_URL}?category={category}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        for product in data:
            self.assertEqual(product["category"], category)

    def test_list_products_by_availability(self):
        """It should List Products by availability"""
        products = self._create_products(10)
        available = products[0].available

        response = self.client.get(f"{BASE_URL}?available={available}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        for product in data:
            self.assertEqual(product["available"], available)
