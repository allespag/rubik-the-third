from math import factorial


def cantor(a: int, b: int) -> int:
    return (a + b + 1) * (a + b) // 2 + b


def binomial(n: int, k: int) -> int:
    return int(factorial(n) / (factorial(k) * factorial(n - k)))
