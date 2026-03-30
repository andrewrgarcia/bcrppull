"""
Compare IPC series from two sources:

1. bcrpy (API via largeGET) — ground truth
2. Local parquet dataset — pipeline output

This script:
- Loads identical IPC series (mensual, core, transables) from both sources
- Aligns them on a common time index
- Computes numerical differences (max, mean, full diff matrix)
- Reports pass/fail based on tolerance
- Prints exact mismatches when discrepancies exist
- Plots overlay (API vs parquet) for visual validation
- Plots absolute differences if mismatch is detected

Purpose:
Ensure that the parquet dataset faithfully reproduces the raw API output
and detect any issues in the data ingestion / aggregation pipeline
(e.g., misalignment, wrong series selection, transformation errors).
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from bcrpy import Marco


PATH = "data/raw/bcrp_monthly.parquet"


def load_bcrpy():
    print("[LOAD BCRPY]")

    m = Marco()

    codes = [
        "PN01271PM",  # IPC mensual
        "PN01276PM",  # IPC sin alimentos y energía
        "PN09815PM",  # IPC transables
    ]

    labels = {
        "PN01271PM": "IPC mensual",
        "PN01276PM": "IPC core",
        "PN09815PM": "IPC transables",
    }

    df = m.largeGET(
        codes=codes,
        start="1950-01",
        end="2025-01",
    )

    df.columns = [labels[c] for c in codes]
    df = df.sort_index()

    return df


def load_parquet():
    print("[LOAD PARQUET]")

    df = pd.read_parquet(PATH)

    codes = [
        "PN01271PM",  # IPC mensual
        "PN01276PM",  # IPC sin alimentos y energía
        "PN09815PM",  # IPC transables
    ]

    labels = {
        "PN01271PM": "IPC mensual",
        "PN01276PM": "IPC core",
        "PN09815PM": "IPC transables",
    }

    cols = []
    for code in codes:
        matches = [c for c in df.columns if code in c]
        if not matches:
            raise RuntimeError(f"{code} not found in parquet")
        cols.append(matches[0])

    df = df[cols].copy()
    df.columns = [labels[c] for c in codes]
    df = df.sort_index()

    return df


def compare_frames(df_api: pd.DataFrame, df_parq: pd.DataFrame, tol: float = 1e-6):
    print("\n[ALIGN]")
    df_api, df_parq = df_api.align(df_parq, join="inner")

    print("Aligned shape:", df_api.shape)

    diff = df_api - df_parq
    abs_diff = diff.abs()

    print("\n[DIFFERENCE STATS]")
    print("\nMax abs diff per series:")
    print(abs_diff.max())

    print("\nMean abs diff per series:")
    print(abs_diff.mean())

    print("\nTotal max abs diff:", abs_diff.max().max())

    passed = not (abs_diff > tol).any().any()

    if passed:
        print("\n[PASS] parquet matches bcrpy within tolerance")
    else:
        print("\n[FAIL] mismatch detected")

        mask = abs_diff > tol
        idx = np.where(mask)

        print("\nFirst mismatches:")
        for i in range(min(10, len(idx[0]))):
            r = idx[0][i]
            c = idx[1][i]
            print(
                f"{df_api.index[r]} | {df_api.columns[c]} | "
                f"api={df_api.iloc[r, c]} vs parquet={df_parq.iloc[r, c]}"
            )

    return df_api, df_parq, abs_diff, passed


def plot_overlay(df_api: pd.DataFrame, df_parq: pd.DataFrame):
    print("\n[PLOT OVERLAY]")

    for col in df_api.columns:
        plt.figure()

        plt.plot(df_api.index, df_api[col], label=f"{col} (bcrpy)")
        plt.plot(df_parq.index, df_parq[col], linestyle="--", label=f"{col} (parquet)")

        plt.title(f"{col}: bcrpy vs parquet")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()


def plot_difference(abs_diff: pd.DataFrame):
    print("\n[PLOT ABS DIFFERENCE]")

    for col in abs_diff.columns:
        plt.figure()

        plt.plot(abs_diff.index, abs_diff[col])

        plt.title(f"Absolute difference: {col}")
        plt.xlabel("Date")
        plt.ylabel("|bcrpy - parquet|")
        plt.grid()
        plt.tight_layout()
        plt.show()


def main():
    df_api = load_bcrpy()
    df_parq = load_parquet()

    df_api, df_parq, abs_diff, passed = compare_frames(df_api, df_parq)

    plot_overlay(df_api, df_parq)

    if not passed:
        plot_difference(abs_diff)


if __name__ == "__main__":
    main()