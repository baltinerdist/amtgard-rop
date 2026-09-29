"""Small statistics helpers shared by the analyses."""
from __future__ import annotations

import math


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion k/n."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (centre - half, centre + half)


def mean_ci(values: list[float], z: float = 1.96) -> tuple[float, float, float]:
    """Mean with a normal-approximation confidence interval."""
    n = len(values)
    if n == 0:
        return (float("nan"),) * 3
    m = sum(values) / n
    if n == 1:
        return (m, float("nan"), float("nan"))
    var = sum((v - m) ** 2 for v in values) / (n - 1)
    half = z * math.sqrt(var / n)
    return (m, m - half, m + half)
