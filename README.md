# bcrppull

Minimal pipeline to build large-scale macroeconomic panels from the  
[Banco Central de Reserva del Perú (BCRP)](https://www.bcrp.gob.pe/).

---

## What is this?

`bcrppull` is a lightweight dataset builder on top of `bcrpy`.

It lets you:

- Extract thousands of BCRP time series
- Filter for monthly macroeconomic variables
- Build a unified panel (Parquet)
- Quickly inspect and clean the dataset

---

## Data source

BCRP API:
https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api

Explore data:
https://estadisticas.bcrp.gob.pe/estadisticas/series/

---

## Installation

Clone and install locally (recommended with uv):

```bash
git clone https://github.com/yourname/bcrppull
cd bcrppull

# install local bcrpy (dev mode)
uv pip install -e ../bcrpy

# install dependencies
uv sync
````

---

## Usage

### Build dataset

```bash
make run_pull
```

Output:

```
data/raw/bcrp_monthly.parquet
```

---

### Quick test

```bash
make run_pull LIMIT=10
```

---

### Inspect dataset

```bash
make inspect
```

This prints:

* missingness statistics
* observation counts
* variance diagnostics
* correlation structure
* data density over time

---

## Output

The dataset is a wide panel:

```
rows    = time (monthly)
columns = macroeconomic series
```

Example:

```
(277, 8027)
```

---

## Important notes

### 1. Raw data is sparse

BCRP data is highly heterogeneous:

* different start dates
* missing values across series
* varying coverage

Typical stats:

* ~45–80% missing values
* many short-lived series
* high redundancy

---

### 2. Raw dataset is NOT model-ready

You must clean it before use.

Recommended pipeline:

```python
df = df.loc[:, df.notna().sum() >= 200]  # keep sufficiently long series

density = df.notna().mean(axis=1)
df = df.loc[density > 0.3]              # keep dense time range

df = df.ffill()                         # fill missing
```

---

### 3. Two regimes

You can build:

**Dense panel (~2000+)**

* shorter time span
* usable for modeling

**Long panel (~1950+)**

* very sparse
* archival / exploratory use

---

## Project structure

```
bcrppull/
├── bcrppull/
│   ├── pull.py        # dataset builder
│   └── metadata.py    # filtering + selection
│
├── scripts/
│   ├── run_pull.py    # main execution
│   └── analyze.py     # diagnostics
│
├── data/
│   └── raw/
│
├── Makefile
└── pyproject.toml
```

---

## Design principles

* Minimal pipeline (no overengineering)
* Reproducible dataset builds
* Explicit filtering (no hidden magic)
* Separation: metadata → pull → analysis

---

## Relationship to other projects

* `bcrpy` → API client
* `bcrppull` → dataset builder
* `fredpull` → global macro ingestion

Together:
→ macroeconomic data pipeline stack

---

## License

MIT
