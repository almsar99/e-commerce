from __future__ import annotations

import json
from pathlib import Path


class Product:
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
    def new_product(cls, product_data: dict) -> "Product":
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity


class Category:
    """Класс для представления категории товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[Product],
    ) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "".join(str(product) + "\n" for product in self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return iter(self.__products)


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

        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products,
        )

        categories.append(category)

    return categories


def demo() -> None:
    Category.category_count = 0
    Category.product_count = 0

    categories = load_categories_from_json("products.json")

    print(f"Количество категорий: {Category.category_count}")
    print(f"Количество товаров: {Category.product_count}")

    for category in categories:
        print(category)
        print(category.products)


if __name__ == "__main__":  # pragma: no cover
    demo()
