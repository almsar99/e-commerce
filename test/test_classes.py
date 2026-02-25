import json

import pytest

from src.main import Category, Product, demo, load_categories_from_json


@pytest.fixture(autouse=True)
def reset_category_counts():
    """Сбрасываем счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product(
        name="Iphone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=8,
    )

    assert product.name == "Iphone 15"
    assert product.description == "512GB, Gray space"
    assert product.price == 210000.0
    assert product.quantity == 8


def test_category_initialization():
    product = Product(
        name="Samsung",
        description="Описание",
        price=100000.0,
        quantity=5,
    )

    category = Category(
        name="Смартфоны",
        description="Телефоны",
        products=[product],
    )

    assert category.name == "Смартфоны"
    assert category.description == "Телефоны"
    assert len(category.products) == 1


def test_category_count():
    Category("Категория 1", "Описание", [])
    Category("Категория 2", "Описание", [])

    assert Category.category_count == 2


def test_product_count():
    product1 = Product("A", "Desc", 100.0, 1)
    product2 = Product("B", "Desc", 200.0, 2)

    Category("Категория", "Описание", [product1, product2])

    assert Category.product_count == 2


def test_load_categories_from_json(tmp_path):
    test_data = [
        {
            "name": "Тестовая категория",
            "description": "Описание",
            "products": [
                {
                    "name": "Товар 1",
                    "description": "Описание товара",
                    "price": 100.0,
                    "quantity": 2,
                }
            ],
        }
    ]

    file_path = tmp_path / "test.json"
    file_path.write_text(
        json.dumps(test_data, ensure_ascii=False),
        encoding="utf-8",
    )

    categories = load_categories_from_json(str(file_path))

    assert len(categories) == 1
    assert categories[0].name == "Тестовая категория"
    assert len(categories[0].products) == 1
    assert categories[0].products[0].name == "Товар 1"


def test_demo(monkeypatch, tmp_path):
    test_data = [
        {
            "name": "Категория",
            "description": "Описание",
            "products": [
                {
                    "name": "Товар",
                    "description": "Описание",
                    "price": 100.0,
                    "quantity": 1,
                }
            ],
        }
    ]

    file_path = tmp_path / "products.json"
    file_path.write_text(
        json.dumps(test_data, ensure_ascii=False),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    demo()

    assert Category.category_count == 1
    assert Category.product_count == 1
