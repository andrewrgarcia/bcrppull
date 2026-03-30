import argparse
import os

from bcrppull.pull import pull_dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2000-01")
    parser.add_argument("--end", default="2023-01")
    parser.add_argument("--limit", type=int, default=None)

    args = parser.parse_args()

    df = pull_dataset(
        start=args.start,
        end=args.end,
        limit=args.limit
    )

    os.makedirs("data/raw", exist_ok=True)

    path = "data/raw/bcrp_monthly.parquet"
    df.to_parquet(path)

    print(f"Saved → {path}")


if __name__ == "__main__":
    main()