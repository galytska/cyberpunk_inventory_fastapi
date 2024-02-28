import random


def generate_random_number():
    """
    generate random 6 digits number e.g. 123456
    """
    return random.randint(100000, 999999)


def update_item(item: dict) -> dict:
    return {k: v + ' updated' if isinstance(v, str) else v + 1
            for k, v in item.items()
            }
