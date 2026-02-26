import json
import pytest

from src.main import Category, Product, demo, load_categories_from_json


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


def test_product_add():
    p1 = Product("A", "Desc", 100.0, 5)   # 500
    p2 = Product("B", "Desc", 200.0, 2)   # 400

    assert p1 + p2 == 900.0


def test_product_add_wrong_type():
    p1 = Product("A", "Desc", 100.0, 5)

    with pytest.raises(TypeError):
        p1 + 5


def test_product_add_not_implemented():
    p1 = Product("A", "Desc", 100.0, 5)

    assert Product.__add__(p1, 5) is NotImplemented


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
    assert product.description == "Desc"
    assert product.price == 500.0
    assert product.quantity == 3


# =========================
# Category
# =========================


def test_category_initialization():
    product = Product("Samsung", "Описание", 100000.0, 5)

    category = Category("Смартфоны", "Телефоны", [product])

    assert category.name == "Смартфоны"
    assert category.description == "Телефоны"
    assert Category.product_count == 1
    assert Category.category_count == 1


def test_category_str():
    p1 = Product("A", "Desc", 100.0, 5)
    p2 = Product("B", "Desc", 200.0, 3)

    category = Category("Смартфоны", "Описание", [p1, p2])

    assert str(category) == "Смартфоны, количество продуктов: 8 шт."


def test_products_property_format():
    product = Product("Samsung", "Описание", 100000.0, 5)

    category = Category("Смартфоны", "Телефоны", [product])

    assert category.products == "Samsung, 100000.0 руб. Остаток: 5 шт.\n"


def test_products_empty_category():
    category = Category("Empty", "None", [])

    assert category.products == ""


def test_add_product():
    category = Category("Смартфоны", "Телефоны", [])
    product = Product("Samsung", "Описание", 100000.0, 5)

    category.add_product(product)

    assert Category.product_count == 1
    assert category.products == "Samsung, 100000.0 руб. Остаток: 5 шт.\n"


def test_category_count():
    Category("Категория 1", "Описание", [])
    Category("Категория 2", "Описание", [])

    assert Category.category_count == 2


def test_product_count():
    p1 = Product("A", "Desc", 100.0, 1)
    p2 = Product("B", "Desc", 200.0, 2)

    Category("Категория", "Описание", [p1, p2])

    assert Category.product_count == 2


# =========================
# Iterator
# =========================


def test_category_iterator():
    p1 = Product("A", "Desc", 100.0, 1)
    p2 = Product("B", "Desc", 200.0, 2)

    category = Category("Test", "Desc", [p1, p2])

    assert list(category) == [p1, p2]


# =========================
# JSON loader
# =========================


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
    file_path.write_text(json.dumps(test_data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(str(file_path))

    assert len(categories) == 1
    assert categories[0].name == "Тестовая категория"
    assert Category.product_count == 1


# =========================
# Demo
# =========================


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
    file_path.write_text(json.dumps(test_data, ensure_ascii=False), encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    demo()

    assert Category.category_count == 1
    assert Category.product_count == 1
