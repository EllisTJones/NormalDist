# Normal Distribution Calculator

A small web app that calculates probabilities for a normal distribution. The page shows the probability, the z-score(s), and a shaded plot of the curve. All of the math runs in Python (SciPy); the HTML page only sends inputs and displays what comes back.

## Features

- Four area types: **above**, **below**, **between** two values, or **outside** two values
- Probability shown as a decimal and a percentage
- Z-score for each finite bound
- Shaded bell curve that follows your inputs
- Input validation with clear error messages (non-numeric values, σ ≤ 0, reversed intervals)
- Light/dark mode toggle (remembers your choice)

## Project structure

```
your-project/
├── app.py            # Flask server: serves the page and the /api/calc endpoint
├── calc.py           # All statistics and validation (edit this to change the logic)
└── static/
    └── index.html    # The page: inputs, results, and the plot
```

`index.html` must be inside the `static` folder.

## Requirements

- Python 3.9 or newer
- Flask, SciPy, NumPy

```
pip install flask scipy numpy
```

In PyCharm, you can also install these under **Settings → Project → Python Interpreter**.

## Running it

1. Run `app.py` (in PyCharm: right-click the file → **Run 'app'**, or run `python app.py` in a terminal).
2. Open <http://127.0.0.1:5000> in your browser.

The page only works while `app.py` is running. Opening `index.html` directly from a folder will not work, because it can't reach Python.

## How it works

1. The page sends the inputs to `/api/calc` as query parameters.
2. `app.py` passes them to `compute()` in `calc.py`.
3. `compute()` validates the inputs, calculates the probability with `norm.cdf`, computes the z-scores, and builds the plot points.
4. The result goes back as JSON, and the page displays it.

### The endpoint

`GET /api/calc`

| Parameter | Meaning |
|-----------|---------|
| `mean` | Mean (μ) |
| `sd` | Standard deviation (σ), must be greater than 0 |
| `area` | `1` above, `2` below, `3` between, `4` outside |
| `value` | The bound for options 1 and 2 |
| `left`, `right` | The two bounds for options 3 and 4 (`right` must be greater than `left`) |

Example:

```
/api/calc?mean=0&sd=1&area=3&left=-1.96&right=1.96
```

A successful response includes `probability`, `percent`, `zscores`, and the plot data (`xs`, `ys`, `shade`). Invalid input returns status 400 with `{"error": "..."}`.

## Changing the logic

`app.py` runs with `debug=True`, so the server reloads automatically when you save a `.py` file. Edit `calc.py`, save, and click **Calculate** in the browser to see the change.

To add a new value to the page:

1. Compute it in `compute()` and add a key to the returned dictionary.
2. In `index.html`, display it in the `calculate()` function, for example `data.yourNewKey`.

## Quick check

With mean 0 and σ 1, a bound of 1.96 should give:

| Option | Probability |
|--------|-------------|
| Above 1.96 | 0.0250 |
| Below 1.96 | 0.9750 |
| Between −1.96 and 1.96 | 0.9500 |
| Outside −1.96 and 1.96 | 0.0500 |

## Notes

- `debug=True` is for local development only. Don't expose the app to the internet with it on.
- Infinite bounds (for above and below) are handled with `np.inf` inside `calc.py`, and are never sent to the page.
