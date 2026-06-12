import pytest

from porinco.domain.models.range import Range


@pytest.mark.parametrize("minimum, maximum", [(1.0, 0), (1.0, 1.0)], ids=["gt", "eq"])
def test_raise_on_minimum_gte_maximum(minimum, maximum):
    with pytest.raises(
        ValueError, match="Maximum value must be strictly greater than minimum value."
    ):
        Range(minimum, maximum)


@pytest.mark.parametrize(
    "minimum, maximum, expected",
    [(70.0, 130.0, 60.0), (-1.0, 1.0, 2.0), (-130.0, -70.0, 60.0)],
)
def test_width(minimum, maximum, expected):
    assert Range(minimum, maximum).width == expected


@pytest.mark.parametrize(
    "minimum, maximum, expected",
    [(70.0, 130.0, 100.0), (-1.0, 1.0, 0.0), (-130.0, -70.0, -100.0)],
)
def test_midpoint(minimum, maximum, expected):
    assert Range(minimum, maximum).midpoint == expected
