from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class ZeroQuantityError(Exception):
    """Исключение для обработки товара с нулевым количеством."""


class BaseProduct(ABC):
    @property
    @abstractmethod
    def price(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other: object) -> float:
        raise NotImplementedError


class BaseModel(ABC):
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class CreationLoggerMixin:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        print(f"{self.__class__.__name__}{args}")
        super().__init__(*args, **kwargs)


class Product(CreationLoggerMixin, BaseProduct):
    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

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


class Category(BaseModel):
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        super().__init__(name, description)
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследников")

        try:
            if product.quantity == 0:
                raise ZeroQuantityError("Нельзя добавить товар с нулевым количеством")

            self.__products.append(product)
            Category.product_count += 1

        except ZeroQuantityError as e:
            print(e)
        else:
            print("Товар добавлен")
        finally:
            print("Обработка добавления товара завершена")

    def middle_price(self) -> float:
        try:
            total = sum(product.price for product in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0

    @property
    def products(self) -> str:
        return "".join(str(product) + "\n" for product in self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> Iterator[Product]:
        return iter(self.__products)


class Order(BaseModel):
    def __init__(self, product: Product, quantity: int) -> None:
        super().__init__(product.name, product.description)

        try:
            if quantity == 0:
                raise ZeroQuantityError(
                    "Нельзя создать заказ с нулевым количеством товара"
                )

            self.product = product
            self.quantity = quantity
            self.total_price = product.price * quantity

        except ZeroQuantityError as e:
            print(e)
            self.quantity = quantity
            self.total_price = 0
        else:
            print("Заказ успешно создан")
        finally:
            print("Обработка создания заказа завершена")

    def __str__(self) -> str:
        return (
            f"Заказ: {self.product.name}, "
            f"Количество: {self.quantity}, "
            f"Итого: {self.total_price} руб."
        )


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


def main() -> None:
    try:
        Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError:
        print(
            "Возникла ошибка ValueError прерывающая работу программы "
            "при попытке добавить продукт с нулевым количеством"
        )

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB", 31000.0, 14)

    category1 = Category(
        "Смартфоны", "Категория смартфонов", [product1, product2, product3]
    )
    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())


if __name__ == "__main__":  # pragma: no cover
    main()
