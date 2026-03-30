import os
import pandas as pd

from bcrppull.pull import pull_dataset


def main():
    # --------------------------------------------------
    # CONFIG
    # --------------------------------------------------
    START = "1950-01"
    END = "2025-01"

    # limit=None → full dataset
    LIMIT = None   # set e.g. 20 for quick test

    # --------------------------------------------------
    # RUN
    # --------------------------------------------------
    print("\n[RUN] pulling monthly BCRP dataset...\n")

    df = pull_dataset(
        start=START,
        end=END,
        monthly_only=True,
        limit=LIMIT,
    )

    # --------------------------------------------------
    # PRINT SUMMARY
    # --------------------------------------------------
    print("\n[RESULT]")
    print("Shape:", df.shape)
    print("\nHead:")
    print(df.head())

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------
    os.makedirs("data/raw", exist_ok=True)

    path = "data/raw/bcrp_monthly.parquet"
    df.to_parquet(path, compression="zstd")

    print(f"\n[SAVED] → {path}")


if __name__ == "__main__":
    main()