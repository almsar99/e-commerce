from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any

# =========================
# Base classes
# =========================


class BaseProduct(ABC):
    """Абстрактный базовый класс продукта."""

    @property
    @abstractmethod
    def price(self) -> float:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other: object) -> float:  # pragma: no cover
        raise NotImplementedError


class BaseModel(ABC):
    """Абстрактный базовый класс бизнес-сущности."""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:  # pragma: no cover
        raise NotImplementedError


# =========================
# Mixin
# =========================


class CreationLoggerMixin:
    """Миксин логирования создания объекта."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        print(f"{self.__class__.__name__}{args}")
        super().__init__(*args, **kwargs)


# =========================
# Products
# =========================


class Product(CreationLoggerMixin, BaseProduct):
    """Класс для представления продукта."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__()

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    @classmethod
    def new_product(cls, product_data: dict[str, Any]) -> Product:
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")

        assert isinstance(other, Product)
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


# =========================
# Category & Order
# =========================


class Category(BaseModel):
    """Класс категории товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[Product],
    ) -> None:
        super().__init__(name, description)
        self.__products: list[Product] = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследников")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "".join(str(product) + "\n" for product in self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> Iterator[Product]:
        return iter(self.__products)


class Order(BaseModel):
    """Класс заказа (может содержать только один товар)."""

    def __init__(self, product: Product, quantity: int) -> None:
        super().__init__(product.name, product.description)
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __str__(self) -> str:
        return (
            f"Заказ: {self.product.name}, "
            f"Количество: {self.quantity}, "
            f"Итого: {self.total_price} руб."
        )


# =========================
# JSON Loader
# =========================


def load_categories_from_json(file_path: str) -> list[Category]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    categories: list[Category] = []

    for category_data in data:
        products = [
            Product(
                name=p["name"],
                description=p["description"],
                price=p["price"],
                quantity=p["quantity"],
            )
            for p in category_data["products"]
        ]

        categories.append(
            Category(
                name=category_data["name"],
                description=category_data["description"],
                products=products,
            )
        )

    return categories


# =========================
# Demo
# =========================


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB", 210000.0, 8)

    category = Category("Смартфоны", "Категория смартфонов", [product1, product2])
    order = Order(product1, 2)

    print(category)
    print(order)
