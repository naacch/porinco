import pandas as pd


def equal(df: pd.DataFrame) -> pd.Series:
    n = len(df.columns)
    if n == 0:
        raise ValueError("Cannot calculate weights without variables.")
    return pd.Series(1 / n, index=df.columns)
