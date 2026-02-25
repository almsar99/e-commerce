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
        self.price = price
        self.quantity = quantity


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
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


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
        for product in category.products:
            print(
                f" - {product.name} " f"({product.price} руб., {product.quantity} шт.)"
            )


if __name__ == "__main__":  # pragma: no cover
    demo()
