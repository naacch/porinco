"""Weighting functions for the processing module."""

import pandas as pd


# TODO: cambiar nombre
def std_weighting(df: pd.DataFrame) -> pd.Series:
    """Calculate the standard deviation weighting."""
    std = df.std()
    if (total_std := std.sum()) == 0:
        raise ValueError("The sum of the standard deviation is zero.")
    return std / total_std


def coefficient_of_variation(df: pd.DataFrame) -> pd.Series:
    """Calculate the coefficient of variation weighting."""
    cv = df.std() / df.mean()
    if (total_cv := cv.sum()) == 0:
        raise ValueError("The sum of the coefficient of variation is zero.")
    return cv / total_cv


WEIGHTINGS = {
    "std": std_weighting,
    "coefficient_of_variation": coefficient_of_variation,
}
