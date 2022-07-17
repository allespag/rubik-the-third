from math import factorial


def binomial(n: int, k: int) -> int:
    return int(factorial(n) / (factorial(k) * factorial(n - k)))
