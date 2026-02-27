import json
import runpy
import sys

import pytest

from src.main import (
    Category,
    LawnGrass,
    Product,
    Smartphone,
    load_categories_from_json,
)


@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.category_count = 0
    Category.product_count = 0


# =========================
# Product
# =========================


def test_product_initialization():
    product = Product("Iphone 15", "512GB", 210000.0, 8)

    assert product.name == "Iphone 15"
    assert product.description == "512GB"
    assert product.price == 210000.0
    assert product.quantity == 8


def test_product_str():
    product = Product("Test", "Desc", 100.0, 5)

    assert str(product) == "Test, 100.0 руб. Остаток: 5 шт."


def test_product_add_same_type():
    p1 = Product("A", "Desc", 100.0, 5)
    p2 = Product("B", "Desc", 200.0, 2)

    assert p1 + p2 == 900.0


def test_product_add_different_type():
    p1 = Product("A", "Desc", 100.0, 5)
    phone = Smartphone("S", "Desc", 1000.0, 1, 95.0, "Model", 256, "Black")

    with pytest.raises(TypeError):
        p1 + phone


def test_price_setter_positive():
    product = Product("A", "Desc", 100.0, 1)
    product.price = 200.0

    assert product.price == 200.0


def test_price_setter_negative(capsys):
    product = Product("A", "Desc", 100.0, 1)
    product.price = -50.0

    captured = capsys.readouterr()

    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 100.0


def test_new_product_classmethod():
    data = {
        "name": "Test",
        "description": "Desc",
        "price": 500.0,
        "quantity": 3,
    }

    product = Product.new_product(data)

    assert product.name == "Test"
    assert product.price == 500.0
    assert product.quantity == 3


# =========================
# Smartphone
# =========================


def test_smartphone_initialization():
    phone = Smartphone(
        "Samsung",
        "Desc",
        1000.0,
        2,
        95.5,
        "S23",
        256,
        "Black",
    )

    assert phone.efficiency == 95.5
    assert phone.model == "S23"
    assert phone.memory == 256
    assert phone.color == "Black"


def test_smartphone_add():
    p1 = Smartphone("A", "Desc", 100.0, 2, 90.0, "M1", 128, "Black")
    p2 = Smartphone("B", "Desc", 200.0, 1, 91.0, "M2", 256, "White")

    assert p1 + p2 == 400.0


# =========================
# LawnGrass
# =========================


def test_lawngrass_initialization():
    grass = LawnGrass(
        "Grass",
        "Desc",
        500.0,
        10,
        "Россия",
        "7 дней",
        "Зеленый",
    )

    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_lawngrass_add():
    g1 = LawnGrass("A", "Desc", 100.0, 5, "RU", "5 days", "Green")
    g2 = LawnGrass("B", "Desc", 200.0, 2, "RU", "6 days", "Dark")

    assert g1 + g2 == 900.0


def test_smartphone_and_grass_add_error():
    phone = Smartphone("A", "Desc", 100.0, 2, 90.0, "M1", 128, "Black")
    grass = LawnGrass("B", "Desc", 200.0, 2, "RU", "5 days", "Green")

    with pytest.raises(TypeError):
        phone + grass


# =========================
# Category
# =========================


def test_category_initialization():
    product = Product("A", "Desc", 100.0, 1)

    Category("Test", "Desc", [product])

    assert Category.category_count == 1
    assert Category.product_count == 1


def test_category_str():
    p1 = Product("A", "Desc", 100.0, 2)
    p2 = Product("B", "Desc", 200.0, 3)

    category = Category("Test", "Desc", [p1, p2])

    assert str(category) == "Test, количество продуктов: 5 шт."


def test_category_products_property():
    product = Product("A", "Desc", 100.0, 1)
    category = Category("Test", "Desc", [product])

    assert category.products == "A, 100.0 руб. Остаток: 1 шт.\n"


def test_add_product_valid():
    category = Category("Test", "Desc", [])
    product = Product("A", "Desc", 100.0, 1)

    category.add_product(product)

    assert Category.product_count == 1


def test_add_product_invalid():
    category = Category("Test", "Desc", [])

    with pytest.raises(TypeError):
        category.add_product("Not a product")


def test_category_iterator():
    p1 = Product("A", "Desc", 100.0, 1)
    p2 = Product("B", "Desc", 200.0, 1)

    category = Category("Test", "Desc", [p1, p2])

    assert list(category) == [p1, p2]


# =========================
# JSON loader
# =========================


def test_load_categories_from_json(tmp_path):
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

    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(test_data), encoding="utf-8")

    categories = load_categories_from_json(str(file_path))

    assert len(categories) == 1
    assert categories[0].name == "Категория"
    assert Category.product_count == 1


# =========================
# __main__ coverage (100% without warning)
# =========================


def test_main_block_execution():
    sys.modules.pop("src.main", None)
    runpy.run_module("src.main", run_name="__main__")
