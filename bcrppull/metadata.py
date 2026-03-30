import pandas as pd
from bcrpy import Marco


# ============================================================
# LOAD METADATA
# ============================================================

def get_metadata() -> pd.DataFrame:
    """
    Load metadata from BCRP via bcrpy.
    """
    m = Marco()
    m.get_metadata()

    if m.metadata.empty:
        raise RuntimeError("Failed to load BCRP metadata.")

    return m.metadata


# ============================================================
# FILTERS
# ============================================================

def filter_monthly(meta: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only monthly series.
    """
    if "Frecuencia" not in meta.columns:
        raise ValueError("Metadata does not contain 'Frecuencia' column.")

    return meta[
        meta["Frecuencia"].astype(str).str.contains("Mensual", case=False, na=False)
    ]


def filter_by_keyword(meta: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    Filter metadata rows that contain a keyword anywhere.
    """
    return meta[
        meta.apply(
            lambda row: row.astype(str).str.contains(keyword, case=False, na=False).any(),
            axis=1
        )
    ]


def filter_min_length(meta: pd.DataFrame, min_obs: int = 60) -> pd.DataFrame:
    """
    Filter series with minimum number of observations if column exists.
    """
    possible_cols = ["Nro. Observaciones", "Observaciones", "obs"]

    for col in possible_cols:
        if col in meta.columns:
            return meta[meta[col] >= min_obs]

    # if no such column exists → return unchanged
    return meta


# ============================================================
# EXTRACT
# ============================================================

def extract_codes(meta: pd.DataFrame) -> list[str]:
    """
    Extract series codes (first column assumed to be code).
    """
    if meta.shape[1] == 0:
        raise ValueError("Metadata has no columns.")

    return meta.iloc[:, 0].astype(str).tolist()


# ============================================================
# PIPELINE
# ============================================================

def prepare_codes(
    monthly_only: bool = True,
    keyword: str | None = None,
    min_obs: int | None = None,
    limit: int | None = None,
) -> list[str]:
    """
    Full pipeline to generate a list of series codes.
    """

    meta = get_metadata()

    if monthly_only:
        meta = filter_monthly(meta)

    if keyword:
        meta = filter_by_keyword(meta, keyword)

    if min_obs:
        meta = filter_min_length(meta, min_obs)

    codes = extract_codes(meta)

    if limit:
        codes = codes[:limit]

    print(f"[metadata] selected {len(codes)} series")

    return codes