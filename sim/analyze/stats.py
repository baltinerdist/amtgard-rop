"""Small statistics helpers shared by the analyses.

Players in the same game share an outcome (a whole team wins or loses together), so a player-level
interval that treats each player-game as independent is too narrow. The helpers here treat the
**game** as the unit of resampling:

- `cluster_ratio_ci`   cluster-robust (sandwich) interval for a ratio of sums, e.g. wins / player-games,
                       with each game as one cluster. Fast and deterministic; used for class win rates.
- `cluster_bootstrap_ci` percentile interval from resampling whole games with replacement, for any
                       statistic of the per-game values.
- `bootstrap_weights`  the resampling as a (B x G) matrix of how often each game is drawn, so several
                       statistics can share the same resamples (the paired ablation uses this: base and
                       ablated games with the same seed are always drawn together).
- `paired_ci`          mean paired difference over seeds with a normal interval; each seed is one pair.
"""
from __future__ import annotations

import math
from collections import defaultdict
from typing import Callable, Hashable, Sequence

import numpy as np


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion k/n (assumes independent trials)."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (centre - half, centre + half)


def mean_ci(values: list[float], z: float = 1.96) -> tuple[float, float, float]:
    """Mean with a normal-approximation confidence interval (assumes independent values)."""
    n = len(values)
    if n == 0:
        return (float("nan"),) * 3
    m = sum(values) / n
    if n == 1:
        return (m, float("nan"), float("nan"))
    var = sum((v - m) ** 2 for v in values) / (n - 1)
    half = z * math.sqrt(var / n)
    return (m, m - half, m + half)


def cluster_ratio_ci(y: Sequence[float], n: Sequence[float], z: float = 1.96,
                     bounds: tuple[float, float] | None = None) -> dict:
    """Ratio estimate sum(y) / sum(n) with a cluster-robust interval.

    `y[g]` and `n[g]` are the totals for cluster g (for a win rate: wins and player-games in game g).
    The variance is the linearised (sandwich) estimator with the usual G/(G-1) small-sample factor:
        r = sum y / sum n,  e_g = y_g - r n_g,  var(r) = G/(G-1) * sum e_g^2 / (sum n)^2
    With one trial per cluster this reduces to the ordinary binomial variance, so the design effect
    (`deff`, the variance ratio against treating every trial as independent) is 1 for independent
    data and grows with within-game correlation. `bounds` clips the interval (e.g. (0, 1)).
    """
    y = np.asarray(y, dtype=float)
    n = np.asarray(n, dtype=float)
    keep = n > 0
    y, n = y[keep], n[keep]
    g, total = len(n), n.sum()
    if g == 0 or total == 0:
        nan = float("nan")
        return {"est": nan, "lo": nan, "hi": nan, "se": nan, "deff": nan, "clusters": 0, "trials": 0}
    r = y.sum() / total
    if g == 1:
        se = float("nan")
    else:
        e = y - r * n
        se = math.sqrt(g / (g - 1) * float((e * e).sum())) / total
    lo, hi = r - z * se, r + z * se
    if bounds is not None:
        lo, hi = max(bounds[0], lo), min(bounds[1], hi)
    naive_var = r * (1 - r) / total if 0 <= r <= 1 else float("nan")
    deff = (se * se / naive_var) if naive_var and naive_var > 0 and not math.isnan(se) else float("nan")
    return {"est": float(r), "lo": float(lo), "hi": float(hi), "se": float(se), "deff": float(deff),
            "clusters": int(g), "trials": int(total)}


def cluster_mean_ci(values: Sequence[float], clusters: Sequence[Hashable], z: float = 1.96) -> dict:
    """Mean of trial-level values with a cluster-robust interval (clusters = game ids)."""
    ys: dict = defaultdict(float)
    ns: dict = defaultdict(float)
    for v, c in zip(values, clusters):
        ys[c] += v
        ns[c] += 1
    keys = list(ys)
    return cluster_ratio_ci([ys[k] for k in keys], [ns[k] for k in keys], z)


def bootstrap_weights(n_clusters: int, n_boot: int, seed: int = 0) -> np.ndarray:
    """(n_boot x n_clusters) matrix: how many times each cluster is drawn in each resample."""
    rng = np.random.default_rng(seed)
    return rng.multinomial(n_clusters, np.full(n_clusters, 1.0 / n_clusters), size=n_boot).astype(float)


def percentile_ci(samples: np.ndarray, level: float = 0.95) -> tuple[float, float]:
    s = np.asarray(samples, dtype=float)
    s = s[~np.isnan(s)]
    if len(s) == 0:
        return (float("nan"), float("nan"))
    a = (1 - level) / 2
    return (float(np.quantile(s, a)), float(np.quantile(s, 1 - a)))


def cluster_bootstrap_ci(values: Sequence[float], clusters: Sequence[Hashable],
                         stat: Callable[[np.ndarray], float] = np.mean, n_boot: int = 1000,
                         seed: int = 0, level: float = 0.95) -> dict:
    """Percentile interval for `stat(values)` resampling whole clusters with replacement."""
    groups: dict = defaultdict(list)
    for v, c in zip(values, clusters):
        groups[c].append(v)
    keys = list(groups)
    arrays = [np.asarray(groups[k], dtype=float) for k in keys]
    est = float(stat(np.concatenate(arrays))) if arrays else float("nan")
    if len(keys) < 2:
        return {"est": est, "lo": float("nan"), "hi": float("nan"), "clusters": len(keys)}
    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.integers(0, len(keys), len(keys))
        boots[b] = stat(np.concatenate([arrays[i] for i in pick]))
    lo, hi = percentile_ci(boots, level)
    return {"est": est, "lo": lo, "hi": hi, "clusters": len(keys)}


def paired_ci(base: Sequence[float], other: Sequence[float], z: float = 1.96) -> dict:
    """Mean of other - base over paired units (seeds), with a normal interval over the pairs."""
    d = [o - b for b, o in zip(base, other)]
    m, lo, hi = mean_ci(d, z)
    return {"est": m, "lo": lo, "hi": hi, "pairs": len(d)}
