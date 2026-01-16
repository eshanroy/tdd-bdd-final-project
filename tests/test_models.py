# Copyright 2016, 2023 John J. Rofrano.
# Licensed under the Apache License, Version 2.0

"""
Test cases for Product Model
"""

import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Run before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """Run after each test"""
        db.session.remove()

    ##################################################################
    #  T E S T   C A S E S
    ##################################################################

    def test_create_a_product(self):
        """It should Create a product"""
        product = Product(
            name="Fedora",
            description="A red hat",
            price=12.50,
            available=True,
            category=Category.CLOTHS,
        )
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertIsNone(product.id)

    def test_add_a_product(self):
        """It should add a product to the database"""
        product = ProductFactory()
        product.id = None
        product.create()

        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """It should read a product"""
        product = ProductFactory()
        product.id = None
        product.create()

        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertEqual(Decimal(found.price), product.price)
        self.assertEqual(found.available, product.available)
        self.assertEqual(found.category, product.category)

    def test_update_a_product(self):
        """It should update a product"""
        product = ProductFactory()
        product.id = None
        product.create()

        product.description = "Updated description"
        product.update()

        found = Product.find(product.id)
        self.assertEqual(found.description, "Updated description")

    def test_delete_a_product(self):
        """It should delete a product"""
        product = ProductFactory()
        product.id = None
        product.create()

        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should list all products"""
        self.assertEqual(len(Product.all()), 0)

        for _ in range(5):
            product = ProductFactory()
            product.id = None
            product.create()

        self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        """It should find products by name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.id = None
            product.create()

        name = products[0].name
        expected = len([p for p in products if p.name == name])

        found = Product.find_by_name(name)
        self.assertEqual(found.count(), expected)

        for product in found:
            self.assertEqual(product.name, name)

    def test_find_by_availability(self):
        """It should find products by availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.id = None
            product.create()

        available = products[0].available
        expected = len([p for p in products if p.available == available])

        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), expected)

        for product in found:
            self.assertEqual(product.available, available)

    def test_find_by_category(self):
        """It should find products by category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.id = None
            product.create()

        category = products[0].category
        expected = len([p for p in products if p.category == category])

        found = Product.find_by_category(category)
        self.assertEqual(found.count(), expected)

        for product in found:
            self.assertEqual(product.category, category)
