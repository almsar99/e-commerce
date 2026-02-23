import pytest
from main import Product, Category


@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("iPhone", "Смартфон", 999.99, 5)

    assert product.name == "iPhone"
    assert product.description == "Смартфон"
    assert product.price == 999.99
    assert product.quantity == 5


def test_category_initialization():
    product = Product("iPhone", "Смартфон", 999.99, 5)

    category = Category("Телефоны", "Смартфоны", [product])

    assert category.name == "Телефоны"
    assert category.description == "Смартфоны"
    assert len(category.products) == 1


def test_category_count():
    product = Product("iPhone", "Смартфон", 999.99, 5)

    Category("Телефоны", "Смартфоны", [product])
    Category("Ноутбуки", "ПК", [])

    assert Category.category_count == 2


def test_product_count():
    product1 = Product("iPhone", "Смартфон", 999.99, 5)
    product2 = Product("Samsung", "Смартфон", 899.99, 3)

    Category("Телефоны", "Смартфоны", [product1, product2])

    assert Category.product_count == 2
