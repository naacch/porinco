from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Range:

    minimum: float
    maximum: float

    def __post_init__(self) -> None:
        if self.maximum <= self.minimum:
            raise ValueError(
                "Maximum value must be strictly greater than minimum value."
            )

    @property
    def width(self) -> float:
        return self.maximum - self.minimum

    @property
    def midpoint(self) -> float:
        return (self.maximum + self.minimum) / 2
