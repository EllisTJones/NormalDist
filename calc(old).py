import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def get_float(prompt, positive=False):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a number.")
            continue
        if positive and value <= 0:
            print("Value must be greater than 0.")
            continue
        return value

def get_choice(prompt, options):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"Please enter one of: {', '.join(options)}")

mean = get_float("Mean (μ): ")
standardDev = get_float("Standard Deviation (σ): ", positive=True)

print("1: Above\n"
      "2: Below\n"
      "3: Between intervals\n"
      "4: Outside intervals")
area = get_choice("Input: ", ("1", "2", "3", "4"))

if area == "1":
    bottominterval = get_float("Value: ")
    topinterval = np.inf
elif area == "2":
    bottominterval = -np.inf
    topinterval = get_float("Value: ")
else:
    bottominterval = get_float("Lefthand interval: ")
    topinterval = get_float("Righthand interval: ")
    while topinterval <= bottominterval:
        print("right interval must be greater than the left interval.")
        topinterval = get_float("Righthand interval: ")

# --- Probability ---
between = norm.cdf(topinterval, mean, standardDev) - norm.cdf(bottominterval, mean, standardDev)
result = 1 - between if area == "4" else between
resultperc = result * 100
print(f"\nProbability: {result:.4f} or {resultperc:.2f}%")

# --- Z-Score ---
zscores = []
for label, bound in (("bottom", bottominterval), ("top", topinterval)):
    if np.isfinite(bound):
        z = (bound - mean) / standardDev
        zscores.append(z)
        print(f"Z-score ({label}): {z:.4f}")

# --- Plotting ---
lo = min(mean - 4 * standardDev, bottominterval if np.isfinite(bottominterval) else np.inf)
hi = max(mean + 4 * standardDev, topinterval if np.isfinite(topinterval) else -np.inf)
xs = np.linspace(lo, hi, 1000)
ys = norm.pdf(xs, mean, standardDev)

plt.plot(xs, ys)
plt.axhline(0, color="black")

if area == "4":
    plt.fill_between(xs, ys, where=(xs <= bottominterval) | (xs >= topinterval), alpha=0.4)
else:
    plt.fill_between(xs, ys, where=(xs >= bottominterval) & (xs <= topinterval), alpha=0.4)

z_text = ", ".join(f"{z:.4f}" for z in zscores)
plt.title(f"Normal(μ={mean}, σ={standardDev})\nz-score(s): {z_text}")
plt.show()