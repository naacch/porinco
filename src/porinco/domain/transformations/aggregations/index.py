import pandas as pd

__all__ = ["arithmetic_mean"]


def arithmetic_mean(df: pd.DataFrame) -> pd.Series:
    return df.mean(axis=1)
