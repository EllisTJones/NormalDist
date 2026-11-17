"""All of the statistics live here. Edit this file and the web page picks up the change."""
import numpy as np
from scipy.stats import norm


def parse_float(raw, name):
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a number.")
    if not np.isfinite(value):
        raise ValueError(f"{name} must be a finite number.")
    return value


def compute(params):
    mean = parse_float(params.get("mean"), "Mean")
    standardDev = parse_float(params.get("sd"), "Standard deviation")
    if standardDev <= 0:
        raise ValueError("Standard deviation must be greater than 0.")

    area = params.get("area")
    if area not in ("1", "2", "3", "4"):
        raise ValueError("Area must be 1, 2, 3 or 4.")

    if area == "1":      # Above
        bottominterval = parse_float(params.get("value"), "Value")
        topinterval = np.inf
    elif area == "2":    # Below
        bottominterval = -np.inf
        topinterval = parse_float(params.get("value"), "Value")
    else:                # Between / Outside
        bottominterval = parse_float(params.get("left"), "Lefthand interval")
        topinterval = parse_float(params.get("right"), "Righthand interval")
        if topinterval <= bottominterval:
            raise ValueError("Righthand interval must be greater than the lefthand interval.")

    # --- Probability ---
    between = norm.cdf(topinterval, mean, standardDev) - norm.cdf(bottominterval, mean, standardDev)
    result = 1 - between if area == "4" else between

    # --- Z-Score ---
    zscores = []
    for label, bound in (("bottom", bottominterval), ("top", topinterval)):
        if np.isfinite(bound):
            zscores.append({"label": label, "z": (bound - mean) / standardDev})

    # --- Plot data ---
    lo = min(mean - 4 * standardDev, bottominterval if np.isfinite(bottominterval) else np.inf)
    hi = max(mean + 4 * standardDev, topinterval if np.isfinite(topinterval) else -np.inf)
    xs = np.linspace(lo, hi, 600)
    ys = norm.pdf(xs, mean, standardDev)
    if area == "4":
        shade = (xs <= bottominterval) | (xs >= topinterval)
    else:
        shade = (xs >= bottominterval) & (xs <= topinterval)

    return {
        "mean": mean,
        "sd": standardDev,
        "probability": float(result),
        "percent": float(result * 100),
        "zscores": zscores,
        "xs": xs.tolist(),
        "ys": ys.tolist(),
        "shade": shade.tolist(),
    }
