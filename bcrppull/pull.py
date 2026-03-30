from bcrpy import large_get
from bcrppull.metadata import prepare_codes


def pull_dataset(
    start="2000-01",
    end="2023-01",
    monthly_only=True,
    keyword=None,
    min_obs=None,
    limit=None,
):

    codes = prepare_codes(
        monthly_only=monthly_only,
        keyword=keyword,
        min_obs=min_obs,
        limit=limit,
    )

    print(f"[pull] fetching {len(codes)} series")

    df = large_get(
        codes=codes,
        start=start,
        end=end,
        chunk_size=50,
        workers=4,
    )

    return df