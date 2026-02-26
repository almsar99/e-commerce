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
        """Геттер цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер цены с проверкой."""
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """Создание продукта из словаря."""
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )


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
        """Добавление продукта в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер списка продуктов в формате строки."""
        result = ""
        for product in self.__products:
            result += (
                f"{product.name}, "
                f"{product.price} руб. "
                f"Остаток: {product.quantity} шт.\n"
            )
        return result


def load_categories_from_json(file_path: str) -> list[Category]:
    """Загружает категории и товары из JSON-файла."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    categories: list[Category] = []

    for category_data in data:
        products: list[Product] = []

        for product_data in category_data["products"]:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            products.append(product)

        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products,
        )

        categories.append(category)

    return categories


def demo() -> None:
    """Демонстрация загрузки данных из products.json."""
    Category.category_count = 0
    Category.product_count = 0

    categories = load_categories_from_json("products.json")

    print(f"Количество категорий: {Category.category_count}")
    print(f"Количество товаров: {Category.product_count}")

    for category in categories:
        print(f"\nКатегория: {category.name}")
        print(f"Описание: {category.description}")
        print("Товары:")
        print(category.products)


if __name__ == "__main__":  # pragma: no cover
    demo()
