from datetime import datetime
from decimal import Decimal

def format_timestamp(timestamp: datetime) -> str:
    """Форматирует datetime в строку."""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def generate_random_string(length: int = 8) -> str:
    """Генерирует случайную строку заданной длины."""
    import random
    import string
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

def decimal_to_float(products):
    """Переводит Decimal в float, если Decimal встречено в значениях словаря."""
    for product in products:
        for key, value in product.items():
            if isinstance(value, Decimal):
                product[key] = float(value)
    return products