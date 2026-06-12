import pandas as pd


def z_score(df: pd.DataFrame, cost_columns: list[str] | None = None) -> pd.DataFrame:

    mean = df.mean()
    std = df.std(ddof=0)

    if (std == 0).any():
        raise ValueError(
            "Cannot apply z-score normalization: standard deviation "
            "is zero for at least one column."
        )

    normalized = (df - mean) / std

    if cost_columns:
        normalized[cost_columns] = -normalized[cost_columns]

    return normalized
