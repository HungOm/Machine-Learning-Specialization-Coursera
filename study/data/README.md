# Datasets

The files the lessons actually read. Every `pd.read_csv('houses.csv')` on the
study site is reading something in this directory.

**Browse them with their shapes, columns and copy-paste snippets:**
[study/data.html](../data.html) — or on the published site,
`…/study/data.html`.

## No download required

`read_csv` takes a URL as readily as a path, so any lesson runs from a cold
notebook:

```python
import pandas as pd

DATA = ('https://raw.githubusercontent.com/HungOm/'
        'Machine-Learning-Specialization-Coursera/main/study/data/')

df = pd.read_csv(DATA + 'houses.csv')
df.shape        # (1000, 5)
```

## What is here

| file | shape | origin | used by |
|---|---|---|---|
| `houses.csv` | 1000 × 5 | generated | F0 W2 · pandas DataFrames, pandas → NumPy; C1 W2 · feature scaling |
| `houses_messy.csv` | 1000 × 5 | generated | F0 W2 · the traps in that lesson, made real |
| `coffee.csv` | 200 × 3 | generated | C2 W1 · the roasting example |
| `houses_lab.csv` | 100 × 5 | course | C1 W2 · the real 99 houses, with a header |
| `heart.csv` | 918 × 12 | course | C2 W4 · one-hot encoding, trees |
| `ratings.csv` | 39253 × 3 | course | C3 W2 · collaborative filtering |
| `movies.csv` | 4778 × 4 | course | C3 W2 · titles for the above |

**generated** — built from a seeded `default_rng` by
[`../_build/datakit.py`](../_build/datakit.py), so the shapes the lessons quote
are true by construction and rebuilding reproduces them byte for byte.

**course** — real data that already ships with the Coursera notebooks in this
repository, copied to one clean path. `ratings.csv` and `movies.csv` are the
recommender lab's two dense matrices reshaped into one tidy table of the ratings
that actually exist: 473 KB instead of 8.5 MB, and pivoting it back reproduces
the lab's `small_movies_Y.csv` exactly — asserted on every regeneration.

## Rebuilding

```bash
python3 study/_build/datakit.py    # rewrite the seven files
python3 study/_build/build.py      # re-measure them onto data.html
```

Shapes on `data.html` are read off these files at build time, not written down,
so the page cannot describe a file that no longer looks like that.
