import pytest

from porinco.domain.transformations.normalizations.z_score import z_score

TOLERANCE = 1e-6


def test_raises_on_zero_std(zero_df):
    with pytest.raises(
        ValueError,
        match=(
            "Cannot apply z-score normalization: standard deviation "
            "is zero for at least one column."
        ),
    ):
        z_score(zero_df)


@pytest.mark.parametrize(
    "cost_columns",
    [[], ["foo"], ["foo", "bar"]],
    ids=["no_cost_columns", "some_cost_column", "all_cost_columns"],
)
def test_mean_eq_zero(df, cost_columns):
    normalized = z_score(df, cost_columns)
    assert normalized.mean().abs().lt(TOLERANCE).all()


@pytest.mark.parametrize(
    "cost_columns",
    [[], ["foo"], ["foo", "bar"]],
    ids=["no_cost_columns", "some_cost_column", "all_cost_columns"],
)
def test_std_eq_one(df, cost_columns):
    normalized = z_score(df, cost_columns)
    assert normalized.std(ddof=0).sub(1).abs().lt(TOLERANCE).all()
