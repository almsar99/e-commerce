import json
import runpy
import sys

import pytest

from src import main as m
from src.main import (
    BaseModel,
    BaseProduct,
    Category,
    LawnGrass,
    Order,
    Product,
    Smartphone,
    load_categories_from_json,
)


@pytest.fixture(autouse=True)
def reset_counts():
    Category.category_count = 0
    Category.product_count = 0


# =========================
# ABSTRACT CLASSES
# =========================


def test_abstract_classes():
    with pytest.raises(TypeError):
        BaseProduct()

    class Dummy(BaseProduct):
        @property
        def price(self):
            return 1

        def __str__(self):
            return "x"

        def __add__(self, other):
            return 0

    d = Dummy()

    with pytest.raises(NotImplementedError):
        BaseProduct.__str__(d)

    with pytest.raises(NotImplementedError):
        BaseProduct.__add__(d, d)

    with pytest.raises(NotImplementedError):
        BaseProduct.price.fget(d)

    class DummyModel(BaseModel):
        def __str__(self):
            return "ok"

    model = DummyModel("n", "d")

    with pytest.raises(NotImplementedError):
        BaseModel.__str__(model)


# =========================
# PRODUCT
# =========================


def test_product_all_branches(capsys):
    p = Product("A", "Desc", 100, 2)

    # __str__
    assert "A" in str(p)

    # setter positive
    p.price = 200
    assert p.price == 200

    # setter negative
    p.price = -10
    assert p.price == 200

    # zero quantity exception
    with pytest.raises(ValueError):
        Product("Bad", "Desc", 100, 0)

    # add
    p2 = Product("B", "Desc", 200, 1)
    assert p + p2 == 600  # 200*2 + 200*1

    # add different type
    phone = Smartphone("S", "Desc", 1000, 1, 90, "Model", 256, "Black")
    with pytest.raises(TypeError):
        p + phone

    # classmethod
    data = {
        "name": "X",
        "description": "Y",
        "price": 300,
        "quantity": 1,
    }
    assert Product.new_product(data).price == 300

    capsys.readouterr()


# =========================
# SMARTPHONE & LAWN
# =========================


def test_smartphone_and_lawn():
    phone = Smartphone("S", "Desc", 1000, 1, 95, "Model", 256, "Black")
    grass = LawnGrass("G", "Desc", 500, 3, "RU", "7 дней", "Green")

    assert phone.memory == 256
    assert grass.country == "RU"


# =========================
# CATEGORY
# =========================


def test_category_all_branches(capsys):
    p1 = Product("A", "Desc", 100, 2)
    p2 = Product("B", "Desc", 300, 3)

    c = Category("Test", "Desc", [p1, p2])

    # __str__
    assert "Test" in str(c)

    # iterator
    assert list(c) == [p1, p2]

    # products property
    assert "A" in c.products

    # middle_price
    assert c.middle_price() == 200

    # empty branch
    empty = Category("Empty", "Desc", [])
    assert empty.middle_price() == 0

    # add success
    c2 = Category("New", "Desc", [])
    p = Product("X", "Desc", 100, 1)

    initial = Category.product_count
    c2.add_product(p)
    assert Category.product_count == initial + 1

    # zero quantity branch
    p.quantity = 0
    c2.add_product(p)

    # wrong type
    with pytest.raises(TypeError):
        c2.add_product("not product")

    out = capsys.readouterr().out
    assert "Обработка добавления товара завершена" in out


# =========================
# ORDER
# =========================


def test_order_all_branches(capsys):
    p = Product("A", "Desc", 100, 5)

    # success
    o = Order(p, 2)
    assert o.total_price == 200
    assert "Заказ:" in str(o)

    # zero quantity
    Order(p, 0)

    out = capsys.readouterr().out
    assert "Обработка создания заказа завершена" in out


# =========================
# JSON
# =========================


def test_json_loader(tmp_path):
    data = [
        {
            "name": "Категория",
            "description": "Описание",
            "products": [
                {
                    "name": "Товар",
                    "description": "Описание",
                    "price": 100,
                    "quantity": 1,
                }
            ],
        }
    ]

    file = tmp_path / "test.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    cats = load_categories_from_json(str(file))
    assert len(cats) == 1


# =========================
# MAIN
# =========================


def test_main_direct(capsys):
    m.main()
    assert "0" in capsys.readouterr().out


def test_run_module_clean():
    sys.modules.pop("src.main", None)
    runpy.run_module("src.main", run_name="__main__")
