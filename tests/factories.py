"""
Factories for Product model tests
"""

# pylint: disable=missing-class-docstring, too-few-public-methods

from factory import Factory, Faker, fuzzy
from service.models import Product, Category


class ProductFactory(Factory):
    """Factory class for creating Product instances"""

    class Meta:
        model = Product

    name = Faker("word")
    description = Faker("sentence")
    price = fuzzy.FuzzyDecimal(0.50, 2000.00, 2)
    available = Faker("boolean")
    category = fuzzy.FuzzyChoice(
        [
            Category.CLOTHS,
            Category.FOOD,
            Category.TOOLS,
        ]
    )
