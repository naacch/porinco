import pytest
from pandas.testing import assert_frame_equal

from porinco.domain.transformations.normalizations import z_score


@pytest.mark.parametrize(
    "normalization, kw",
    [(z_score, {}), (z_score, {"cost_columns": ["foo"]})],
    ids=["z_score", "z_score_with_cost_columns"],
)
class TestNormalizationBehavior:

    def test_returns_new_dataframe(self, df, normalization, kw):
        result = normalization(df, **kw)
        assert result is not df

    def test_does_not_modify_input_df(self, df, normalization, kw):
        original = df.copy(deep=True)
        normalization(df, **kw)
        assert_frame_equal(df, original)
