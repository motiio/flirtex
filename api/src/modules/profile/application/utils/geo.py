import random


def add_random_offset(value: float, offset: float = 0.04) -> float:
    """
    Add a random offset to the coordinate.
    The offset value is the maximum possible deviation.
    """
    return value + random.uniform(-offset, offset)
